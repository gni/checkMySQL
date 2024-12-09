# -*- coding: utf-8 -*-
import typer
from rich import print
from rich.console import Console
from rich.table import Table
from checkmysql.connector import MySQLConn
import traceback
import json

app = typer.Typer()
console = Console()

@app.command()
def check(
    host: str = typer.Argument('localhost', help="MySQL server host."),
    user: str = typer.Argument('root', help="MySQL user."),
    password: str = typer.Argument(..., help="MySQL password."),
    db: str = typer.Argument('sys', help="Database to connect to."),
    port: int = typer.Argument(3306, help="MySQL server port."),
    output_json: bool = typer.Option(False, "--json", help="Output the results in JSON format."),
):
    """
    Check MySQL database connection and retrieve server details.
    """
    try:
        # Create MySQL connection
        con = MySQLConn.create(host, user, password, db, port)
        server_info = con.fetch("SELECT VERSION() as version, DATABASE() as current_db;")
        test_connection = con.fetch("SELECT 1 as checkin;")

        # Prepare data for output
        result = {
            "Host": host,
            "Port": port,
            "User": user,
            "Database": server_info[0].get('current_db', 'N/A'),
            "Server Version": server_info[0].get('version', 'Unknown'),
            "Connection State": "OK" if test_connection[0].get('checkin') == 1 else "FAILED",
        }

        # Output in JSON format if --json is used
        if output_json:
            print(json.dumps(result, indent=4))
        else:
            # Create a Rich table for output
            table = Table(title="MySQL Connection Details")
            table.add_column("Parameter", justify="right", style="cyan", no_wrap=True)
            table.add_column("Value", style="magenta")

            # Add basic connection details
            for key, value in result.items():
                table.add_row(key, str(value))

            # Print the table
            console.print(table)

    except Exception as e:
        if output_json:
            error_result = {
                "Error Type": type(e).__name__,
                "Error Details": str(e),
                "Traceback": traceback.format_exc(),
            }
            print(json.dumps(error_result, indent=4))
        else:
            # Handle exceptions gracefully
            error_table = Table(title="Error Details", show_header=True, header_style="bold red")
            error_table.add_column("Type", justify="center")
            error_table.add_column("Details")
            error_table.add_row(type(e).__name__, str(e))

            console.print(error_table)
            console.print("[red]Traceback:[/red]")
            console.print(traceback.format_exc())

if __name__ == "__main__":
    app()
