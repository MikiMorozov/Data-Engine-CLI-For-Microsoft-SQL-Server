import inspect
import re
import printer_util
from database_manager import Database_Manager
from data_engine import Data_Engine
from colorama import Fore, Style
import time
from halo import Halo

engine_running = [False]
program_running = [True]
db_manager = Database_Manager()
data_engine = Data_Engine(db_manager)

def has_param(func):
    signature = inspect.signature(func)
    params = signature.parameters
    if len(params) > 0:
        return True

def write_data(output_directory):
    try:
        data_engine.write_to_file(output_directory)
    except Exception as e:  
        print(f"An unexpected error occurred: {e}")

def insert_into_db():
    try:
        db_manager.insert_into_db(data_engine.insert_script)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def generate(nr_of_lines, table_index=None):
    try: 
        with Halo(text='generating data...'):
            start_time = time.time()
            data_engine.generate(nr_of_lines, table_index)
            end_time = time.time()
            print('\n')
            print(Fore.LIGHTBLUE_EX + data_engine.insert_script)
            print('\n')
            print(f"Time elapsed: {round(end_time - start_time, 3)} seconds\n")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def add_requirement(prompt):
        data_engine.add_requirement(prompt)
        printer_util.print_req_added(prompt)

def delete_requirement(index):
    data_engine.delete_requirement(index)
    printer_util.print_req_deleted()

def print_requirements():
    printer_util.print_reqs(data_engine)

def add_table(index):
    data_engine.add_table(index)

def remove_table(index):
    data_engine.remove_table(index)

def see_tables():
    try:
        printer_util.see_tables_added(data_engine)
    except Exception as e:
        print('Invalid input for -rt command')

def print_prompt():
    if len(data_engine.table_dict) == 0:
        printer_util.print_db_prompt(data_engine)
    else:
        printer_util.print_tables_prompt(data_engine)

def clear_tables():
    data_engine.clear_tables()
    printer_util.print_tables_cleared()

def print_help():
    printer_util.print_help()

def print_tables():
    printer_util.print_tables(db_manager)

def print_table_relationships():
    printer_util.print_table_relationships(db_manager)

def print_table_order():
    printer_util.print_table_order(db_manager)

def start_engine():
    engine_running[0] = True 
    printer_util.print_engine_started()

def stop_engine():
    engine_running[0] = False
    printer_util.print_engine_stopped()
    data_engine.clear()

def quit():
   program_running[0] = False

def print_models():
    try:
        printer_util.print_models()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def set_model(model_index):
        data_engine.set_model(model_index)

def print_get_model():
    printer_util.print_get_model(data_engine)

def command_valid(user_input):
    from command_registry import engine_commands, non_engine_commands
    # Check if user input matches any key in non_engine_commands
    non_engine_match = any(re.match(command, user_input) for command in non_engine_commands.keys())
    
    # Check if user input matches any key in engine_commands
    engine_match = any(re.match(command, user_input) for command in engine_commands.keys())

    if not (non_engine_match or engine_match):
        return False
        
    return True

def engine_command_handler(user_input):
    import command_registry
    if user_input in command_registry.engine_commands.values() and engine_running[0] == False:
        printer_util.print_engine_not_running()
        return
    
def engine_check(user_input):
    from command_registry import engine_commands, non_engine_commands
    engine_match = any(re.match(command, user_input) for command in engine_commands.keys())

    if(engine_match and engine_running[0] == False):
        return False
    return True

def get_command(user_input):
    from command_registry import engine_commands, non_engine_commands

    non_engine_match = next((command for command in non_engine_commands.keys() if re.match(command, user_input)), None)
    engine_match = next((command for command in engine_commands.keys() if re.match(command, user_input)), None)

    if non_engine_match:
        command_function = non_engine_commands.get(non_engine_match)
        if command_function:
            if has_param(command_function):
                match = re.match(non_engine_match, user_input)
                if match:
                    return command_function(match.group(1))
            else:
                return command_function()

    elif engine_match:
        command_function = engine_commands.get(engine_match)
        if command_function:
            if has_param(command_function):
                match = re.match(engine_match, user_input)
                if match:
                    return command_function(*match.groups())
            else:
                return command_function()

def set_terminal():
    if engine_running[0] == False:
        return input('> ').strip().lower()
    else:
        return input(Fore.LIGHTBLUE_EX + '>>> ' + Style.RESET_ALL).strip().lower()