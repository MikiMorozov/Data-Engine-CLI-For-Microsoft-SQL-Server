# #!/usr/bin/env python
import printer_util
import commands
from database_manager import Database_Manager
from data_engine import Data_Engine
from colorama import Fore, Style

def main():

    printer_util.welcome()

    connection_string = r"DRIVER={ODBC Driver 17 for SQL Server};Server=michael\SQLEXPRESS01;Database=Hotel;Trusted_Connection=yes;"
    output_directory = r"C:\Users\micha\OneDrive\Documents\DataEngineTests"

    db_manager = Database_Manager(connection_string)
    data_engine = Data_Engine(db_manager)

    commands.data_engine = data_engine
    commands.db_manager = db_manager

    # for table in db_manager.table_props:
    #     printer_util.print_table(table_prop)

    engine_running = [False]

    while True:
        if engine_running[0] == False:
            user_input = input('> ').strip().lower()
        else:
            user_input = input(Fore.LIGHTBLUE_EX + '>>> ' + Style.RESET_ALL).strip().lower()
        commands.execute_command(user_input, db_manager, data_engine, engine_running)
        if user_input == commands.non_engine_commands['QUIT']:
            break

if __name__ == "__main__":
    main()