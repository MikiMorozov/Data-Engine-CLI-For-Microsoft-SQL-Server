# #!/usr/bin/env python

import click
import database
# from app.cli.commands import generate_dummy_data

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
def main():
    click.clear()
    """Welcome to the Dummy Data Generator CLI.

    This program generates dummy data for your application.
    """
    click.echo("****************************************")
    click.echo("Welcome to the Dummy Data Generator CLI.")
    click.echo("****************************************")
    click.echo("This program generates dummy data for your application.")

    # Prompt the user for input
    connection_string = r"DRIVER={ODBC Driver 17 for SQL Server};Server=michael\SQLEXPRESS01;Database=Hotel;Trusted_Connection=yes;"
    # connection_string = click.prompt("Please provide the connection string for your database")
                                 
    output_dir = click.prompt("Please provide the output directory for the generated data")

    # Now you can use the provided input (connection_string, output_dir) as needed

    click.echo("----------------------------------------")
    click.echo(f"Connection String: {connection_string}")
    click.echo(f"Output Directory: {output_dir}")
    click.echo("----------------------------------------")

    database.extract_database_schema(connection_string)
    database.get_table_order(connection_string)

    click.echo("\nData Engine will now start generating test data for your database. ")

if __name__ == "__main__":
    main()