# -*- coding: utf-8 -*-
import typer
from rich import print
from rich.console import Console
from rich.table import Table
from checkmysql.connector import MySQLConn

app = typer.Typer()
console = Console()

@app.command()
def check(host: str = typer.Argument('localhost'),
            user: str = typer.Argument('root'),
            password: str = typer.Argument(None),
            db: str = typer.Argument('sys'),
            port: int = typer.Argument(3306)):
    '''
    Check database connection
    '''
    con = MySQLConn.create(host, user, password, db, port)
    try:
        res = con.fetch("select 1 as checkin;")
        table = Table("MySQL test connection")
        table.add_row(f"host: {host}")
        table.add_row(f"port: {port}")
        if res[0].get('checkin', None) == 1:
            table.add_row('state: [green]OK[/green]')
        else:
            table.add_row('state: [red]KO[/red]')
            table.add_row(f'res: [red]{res}[/red]')
        console.print(table)
    except Exception as e:
        print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")


if __name__ == "__main__":
    app()
