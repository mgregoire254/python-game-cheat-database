import sqlite3
import typer
from colorama import Fore, Style, init
from prettytable import PrettyTable , ALL
import os

# Connect to the database
conn = sqlite3.connect('cheat_database.db')
cursor = conn.cursor()

# Create the game_cheats table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_cheats (
        id INTEGER PRIMARY KEY,       
        title TEXT,       
        cheat_code TEXT,
        tip TEXT
               
    )
''')

# Commit changes and close the database connection
conn.commit()
conn.close()

# Initialize colorama
init(autoreset=True)

# Initialize typer
app = typer.Typer()

# Function to add a new cheat code and tip to the database
def add_cheat_code(title: str, cheat_code: str, tip: str):
    conn = sqlite3.connect('cheat_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO game_cheats (title, cheat_code, tip)
        VALUES (?, ?, ?)
    ''', (title, cheat_code, tip))

    conn.commit()
    conn.close()

# Function to search for cheat codes and tips based on the game title
def search_cheats(title: str):
    conn = sqlite3.connect('cheat_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT title, cheat_code, tip
        FROM game_cheats
        WHERE title LIKE ?
    ''', (f'%{title}%',))

    results = cursor.fetchall()
    conn.close()

    if results:
        display_cheats_as_table(results)
    else:
        typer.echo("No cheat codes or tips found for the given title.")

# Function to update cheat code and tip for a game
def update_cheat_code(title: str, cheat: str, tip: str):
    conn = sqlite3.connect('cheat_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE game_cheats
        SET cheat_code = ?, tip = ?
        WHERE title = ?
    ''', (cheat, tip, title))

    conn.commit()
    conn.close()
    typer.echo(Fore.GREEN + f"Cheat code and tip updated for {title}.")

# Function to display a table of cheat results    
def display_cheats_as_table(data):
    table = PrettyTable()
    table.field_names = ["Title", "Cheat Code", "Tip"]

    for row in data:
        table.add_row(row)

    typer.echo(table)    

# Function to create a title and display it
def display_title():
    title = """
++------------------------------------------------------------------------------++
++------------------------------------------------------------------------------++
|| .o88b. db   db d88888b  .d8b.  d888888b      d8888b.  .d8b.  .d8888. d88888b ||
||d8P  Y8 88   88 88'     d8' `8b `~~88~~'      88  `8D d8' `8b 88'  YP 88'     ||
||8P      88ooo88 88ooooo 88ooo88    88         88oooY' 88ooo88 `8bo.   88ooooo ||
||8b      88~~~88 88~~~~~ 88~~~88    88         88~~~b. 88~~~88   `Y8b. 88~~~~~ ||
||Y8b  d8 88   88 88.     88   88    88         88   8D 88   88 db   8D 88.     ||
|| `Y88P' YP   YP Y88888P YP   YP    YP         Y8888P' YP   YP `8888Y' Y88888P ||
++------------------------------------------------------------------------------++
++------------------------------------------------------------------------------++

Written by Michael Gregoire
"""
    os.system('clear')
    print(title)


@app.command()
# Function that creates the main menu
def menu():
    # Calls the title function
    display_title()
    # Main menu for cheat code and tips manager.
    while True:
        typer.echo(Style.BRIGHT + Fore.GREEN + "=== Cheat Code and Tips Manager ===")
        typer.echo(Style.DIM + Fore.GREEN + "1. Add Cheat Code and Tip")
        typer.echo(Style.DIM + Fore.GREEN + "2. Search Cheat Codes and Tips")
        typer.echo(Style.DIM + Fore.GREEN + "3. Update Cheat Code and Tip")
        typer.echo(Style.DIM + Fore.GREEN + "4. Exit")

        choice = typer.prompt(Style.BRIGHT + Fore.GREEN + "Enter your choice (1/2/3/4): ")

        if choice == "1":
            os.system('clear')
            display_title()
            title = typer.prompt(Style.BRIGHT + Fore.GREEN + "Enter the game title: ")
            cheat = typer.prompt(Style.BRIGHT + Fore.GREEN + "Enter the cheat code: ")
            tip = typer.prompt(Style.BRIGHT + Fore.GREEN + "Enter the game tip: ")
            add_cheat_code(title, cheat, tip)
            os.system('clear')
            typer.echo(Style.BRIGHT + Fore.GREEN + "Cheat code and tip added successfully.")

        elif choice == "2":
            os.system('clear')
            display_title()
            title = typer.prompt(Style.BRIGHT + Fore.GREEN + "Enter the game title to search: ")
            search_cheats(title)

        elif choice == "3":
            os.system('clear')
            display_title()
            title = typer.prompt(Style.BRIGHT + Fore.GREEN + "Enter the game title to update: ")
            cheat = typer.prompt(Style.BRIGHT + Fore.GREEN + "Enter the new cheat code: ")
            tip = typer.prompt(Style.BRIGHT + Fore.GREEN + "Enter the updated game tip: ")
            update_cheat_code(title, cheat, tip)

        elif choice == "4":
            os.system('clear')
            break

        else:
            typer.echo(Style.BRIGHT + Fore.RED + "Invalid choice. Please select a valid option.")

if __name__ == '__main__':
    app()
