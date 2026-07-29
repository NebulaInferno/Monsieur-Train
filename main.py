from calendar import c
import responses
from math import e
from numbers import Number
import operator
import shutil
import sqlite3
from tracemalloc import stop
from cycler import V
from discord.ext import commands, tasks
from discord import app_commands
import discord
import json
import requests
import asyncio
import threading
from datetime import datetime
import time
import csv
import random
from typing import Literal, Optional
import typing
from re import A
import traceback
import os
import zipfile
from pathlib import Path
import pandas as pd
import builtins
from dotenv import dotenv_values
from keep_alive import keep_alive

# thing to make it work on all oses
import sys

keep_alive()

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)

def get_next_train_log(user_name: int):
    try:
        with open("trainlogs.csv", mode="r") as file:
            reader = list(csv.reader(file))
            # Safety: Ensure row has enough columns before checking the ID
            user_logs = [row for row in reader if len(row) > 1 and row[1] == str(user_name)]
            
            return len(user_logs) + 1
    except (FileNotFoundError, IndexError):
        return 1
    
def get_next_user_train_log(user: int):
    try:
        with open("trainlogs.csv", mode="r") as file:
            reader = list(csv.reader(file))
            # Safety: Ensure row has enough columns before checking the ID
            user_logs = [row for row in reader if len(row) > 1 and row[1] == str(user)]
            
            return len(user_logs) + 1
    except (FileNotFoundError, IndexError):
        return 1

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

required_files = [os.path.join(BASE_DIR, 'logs.csv')]
for file in required_files:
    file_name = os.path.dirname(file)
    if file_name:
        os.makedirs(file_name, exist_ok=True)
    if os.path.exists(file):
        print(f"{file} exists")
    else:
        open(file, "w").close()
        print(f"Created {file}")
        

config = dotenv_values(".env")

TOKEN = config.get['TOKEN']

def run_discord_bot():

    intents = discord.Intents.default()
    intents.typing = False
    intents.message_content = True
    intents.presences = False

    client = discord.Client(intents=intents)
    log = app_commands.Group(name='log', description='train stuff')
    bus = app_commands.Group(name='bus', description='bus stuff')
    siemens = app_commands.Group(name='siemens', description='Siemens stuff')
    tree = app_commands.CommandTree(client)
    @client.event
    async def on_ready():
        tree.add_command(log)
        tree.add_command(bus)
        tree.add_command(siemens)
        print(f'{client.user}')
        await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.CustomActivity(name="Reading peoples logs"))
        await tree.sync()
    
    @bus.command(name="log", description="log a bus")
    @app_commands.describe(busnumber="Choose bus number", route="Choose route", start="Where got on the bus", end="Where you got off the bus", date="When you took the bus", generation="Myki Generation")
    @app_commands.choices(generation=[
        app_commands.Choice(name="N", value="n"),
        app_commands.Choice(name="1", value="1"),
        app_commands.Choice(name="2", value="2"),
        app_commands.Choice(name="3", value="3")
    ])
    async def create(interaction: discord.Interaction, busnumber: str, route: str, start: str, end: str, date: str="", generation: Optional[app_commands.Choice[str]] = None):
        generation_name = generation.name if generation else "n/a"
        if interaction.user.id == 1065872885559861289:
            await interaction.response.defer()
            with open("Fleetlist.csv", mode="r") as file:
                reader = csv.reader(file)
                last_row = None
                for row in reader:
                    last_row = row
                log_number = int(last_row[0]) + 1
                # print(log_number)
            newlog = [log_number, busnumber, route, start, end, date, generation_name]
            with open("Fleetlist.csv", mode="a", newline="") as fleetlist: 
                writer = csv.writer(fleetlist) 
                writer.writerow(newlog)
            await interaction.edit_original_response(content=f"Logged {busnumber} on {route}!")
        else:
            await interaction.edit_original_response(content=f"You aren't Monsieur NebulaFire")

        

    @bus.command(name="view", description="Review a bus log!")
    @app_commands.describe(log_number="The number log you want to view")
    async def search(interaction: discord.Interaction, log_number: str):
        if interaction.user.id == 1065872885559861289:
            await interaction.response.defer()
            with open("Fleetlist.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == log_number:
                        await interaction.edit_original_response(content=f"This is log {log_number}\n{row}")
                        return
        else:
            await interaction.edit_original_response(content=f"You aren't Monsieur NebulaFire")
            return
                    
    @log.command(name="train", description="Log a train!")
    @app_commands.describe(trainset="Carriage number", line="Choose train line", start="Where you get on!", finish="Where you got off!", train="Type of train!", date="date of transit")
    @app_commands.choices(line=[
        app_commands.Choice(name="Hurstbridge", value="Hurstbridge"),
        app_commands.Choice(name="Mernda",value="Mernda"),
        app_commands.Choice(name="Craigieburn",value="Craigieburn"),
        app_commands.Choice(name="Sunbury",value="Sunbury"),
        app_commands.Choice(name="Upfield",value="Upfield"),
        app_commands.Choice(name="Cranbourne",value="Cranbourne"),
        app_commands.Choice(name="Pakenham",value="Pakenham"),
        app_commands.Choice(name="Frankston",value="Frankston"),
        app_commands.Choice(name="Stony Point",value="Stony Point"),
        app_commands.Choice(name="Werribee",value="Werribee"),
        app_commands.Choice(name="Williamstown",value="Williamstown"),
        app_commands.Choice(name="Sandringham",value="Sandringham"),
        app_commands.Choice(name="Alamein",value="Alamein"),
        app_commands.Choice(name="Belgrave",value="Belgrave"),
        app_commands.Choice(name="Glen Waverly",value="Glen Waverly"),
        app_commands.Choice(name="Lilydale",value="Lilydale"),
        app_commands.Choice(name="Flemington Racecourse",value="Flemington Racecourse"),
    ])
    @app_commands.choices(train=[
        app_commands.Choice(name="Comeng", value="Comeng"),
        app_commands.Choice(name="Siemens", value="Siemens"),
        app_commands.Choice(name="X'Trapolis 100", value="X'Trapolis 100"),
        app_commands.Choice(name="High Capacity Metro Train", value="HCMT"),
        app_commands.Choice(name="X'Trapolis 2.0", value="X'Trapolis 2.0")
    ])
    # @app_commands.choices(start=[

    # ])
    # @app_commands.choices(finish=[

    # ])
    async def blah(interaction: discord.Interaction, trainset: str, line: Optional[app_commands.Choice[str]] = None, train: Optional[app_commands.Choice[str]] = None, start: str="", finish: str="", date: Optional[str] = None):
        log_date = date or datetime.now().strftime("%d/%m/%y")
        line_name = line.name if line else "n/a"
        train_name = train.name if train else "n/a"
        user_name = interaction.user.name
        # 2. Get the next log number for THIS user
        log_number = get_next_train_log(user_name)
        await interaction.response.defer()
        with open("trainsblahblajblah.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if trainset in row[0]:
                    toast = row[0]
                    newlog = [log_number, user_name, toast, line_name, train_name, start, finish, log_date]
        with open("trainlogs.csv", mode="a", newline="") as trainlog:
            writer = csv.writer(trainlog)
            writer.writerow(newlog)
        await interaction.edit_original_response(content=f"Logged {trainset}! thats log number {log_number}!")
        return
    
    
    @log.command(name="train_admin", description="Log a train! (for anybody)")
    @app_commands.describe(trainset="Carriage number", line="Choose train line", start="Where you get on!", finish="Where you got off!", train="Type of train!", date="date of transit", user="User to log for")
    @app_commands.choices(line=[
        app_commands.Choice(name="Hurstbridge", value="Hurstbridge"),
        app_commands.Choice(name="Mernda",value="Mernda"),
        app_commands.Choice(name="Craigieburn",value="Craigieburn"),
        app_commands.Choice(name="Sunbury",value="Sunbury"),
        app_commands.Choice(name="Upfield",value="Upfield"),
        app_commands.Choice(name="Cranbourne",value="Cranbourne"),
        app_commands.Choice(name="Pakenham",value="Pakenham"),
        app_commands.Choice(name="Frankston",value="Frankston"),
        app_commands.Choice(name="Stony Point",value="Stony Point"),
        app_commands.Choice(name="Werribee",value="Werribee"),
        app_commands.Choice(name="Williamstown",value="Williamstown"),
        app_commands.Choice(name="Sandringham",value="Sandringham"),
        app_commands.Choice(name="Alamein",value="Alamein"),
        app_commands.Choice(name="Belgrave",value="Belgrave"),
        app_commands.Choice(name="Glen Waverly",value="Glen Waverly"),
        app_commands.Choice(name="Lilydale",value="Lilydale"),
        app_commands.Choice(name="Flemington Racecourse",value="Flemington Racecourse"),
    ])
    @app_commands.choices(train=[
        app_commands.Choice(name="Comeng", value="Comeng"),
        app_commands.Choice(name="Siemens", value="Siemens"),
        app_commands.Choice(name="X'Trapolis 100", value="X'Trapolis 100"),
        app_commands.Choice(name="High Capacity Metro Train", value="HCMT"),
        app_commands.Choice(name="X'Trapolis 2.0", value="X'Trapolis 2.0")
    ])
    # @app_commands.choices(start=[

    # ])
    # @app_commands.choices(finish=[

    # ])
    async def admintrain(interaction: discord.Interaction, user: discord.Member, trainset: str, line: Optional[app_commands.Choice[str]] = None, train: Optional[app_commands.Choice[str]] = None, start: str="", finish: str="", date: Optional[str] = None):
        log_date = date or datetime.now().strftime("%d/%m/%y")
        line_name = line.name if line else "n/a"
        train_name = train.name if train else "n/a"
        # 2. Get the next log number for THIS user
        log_number = get_next_user_train_log(user)
        ADMIN_ID = 1065872885559861289 
        if user is interaction.user.id != ADMIN_ID:
            await interaction.response.send_message("You do not have permission to log for others.", ephemeral=True)
            return
        await interaction.response.defer()
        with open("trainsblahblajblah.csv", 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if trainset in row[0]:
                    toast = row[0]
                    newlog = [log_number, user, toast, line_name, train_name, start, finish, log_date]
        with open("trainlogs.csv", mode="a", newline="") as trainlog:
            writer = csv.writer(trainlog)
            writer.writerow(newlog)
        await interaction.edit_original_response(content=f"Logged {trainset}! thats log number {log_number}!")
        return


    @log.command(name="view", description="View a specific log or all logs in a thread!")
    @app_commands.describe(id="The log number you want to see (Leave blank for ALL)", user="The user whose logs you are viewing")
    async def trainlog(interaction: discord.Interaction, id: Optional[str] = None, user: Optional[discord.Member] = None):
        
        ADMIN_ID = 1065872885559861289
        
        if user is not None and interaction.user.id != ADMIN_ID:
            await interaction.response.send_message("You do not have permission to view other users' logs.", ephemeral=True)
            return
        
        await interaction.response.defer()

        target_member = user or interaction.user
        target_name = target_member.name
        
        try:
            with open("trainlogs.csv", "r") as file:
                reader = list(csv.reader(file))
                
                # --- CASE 1: No ID provided, show ALL logs in a thread ---
                if id is None:
                    user_logs = [row for row in reader if len(row) > 1 and row[1] == target_name]
                    
                    if not user_logs:
                        await interaction.edit_original_response(content=f"{target_member.display_name} has no logs.")
                        return

                    # Create the initial message to attach the thread to
                    base_msg = await interaction.edit_original_response(content=f"Found {len(user_logs)} logs for {target_member.display_name}. View them in the thread below! ↓")
                    
                    # Create a thread
                    thread = await base_msg.create_thread(name=f"Logs for {target_member.display_name}", auto_archive_duration=60)
                    
                    # Post logs in chunks (Discord has a 2000 character limit per message)
                    log_text = ""
                    for row in user_logs:
                        print(row)

                # --- CASE 2: Specific ID provided ---
                for row in reader:
                    if len(row) > 1 and row[0] == id and row[1] == target_name:
                        await interaction.edit_original_response(
                            content=f"**#{row[0]}**: {row[2]}, on: {row[3]}, riding: {row[4]}, ({row[7]})\n"
                        )
                        return
                
                await interaction.edit_original_response(content=f"Could not find log #{id} for {target_member.display_name}.")
                
        except FileNotFoundError:
            await interaction.edit_original_response(content="No train logs have been created yet.")

    @log.command(name="edit", description="Edit an existing log!")
    @app_commands.describe(id="Id of the log you want to edit", carriagenumber="The Fancy numbers which says what train you were on")
    async def logedit(interaction: discord.Interaction, id: str, carriagenumber: str):
        user_name = interaction.user.name
        found = False
        

        try:
            with open("trainlogs.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == id and row[1] == user_name:
                        found = True
                    if found:
                            id = row[0]
                            user_name = row[1]
                            line_name = row[3]
                            train_name = row[4]
                            start = row[5]
                            end = row[6]
                            date = row[7]
            with open("trainsblahblajblah.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if carriagenumber in row[0]:
                        carriage = row[0]
            with open("trainlogs.csv", "w") as file:
                writer = csv.writer(file)
                replaced_log = [id, user_name, carriage, line_name, train_name, start, end, date]
                

        except FileNotFoundError:
            await interaction.edit_original_response("")



    @log.command(name="delete", description="Delete a Log")
    @app_commands.describe(id="Log you want to delete")
    async def byebyelog(interaction: discord.Interaction, id: str):
        user_name = interaction.user.name
        found = False

        try:
            # 1. Read the existing logs
            with open("trainlogs.csv", "r", newline='') as file:
                rows = list(csv.reader(file))

            # 2. Filter out the row that matches the ID AND the User Name
            # This keeps everything EXCEPT the row you want to delete
            new_rows = []
            for row in rows:
                # Check if this is the row to delete
                if len(row) > 1 and row[0] == id and row[1] == user_name:
                    found = True
                    continue # Skip adding this row to new_rows
                new_rows.append(row)

                if found:
                    try:
                        current_id = int(row[0])
                        user = str(row[1])
                        if user == user_name:
                            row[0] = str(current_id - 1)
                    except ValueError:
                        pass # Skip if row[0] isn't a number (like a header)

            if not found:
                await interaction.response.send_message(f"Log ID `{id}` not found", ephemeral=True)
                return

            # 3. Write the updated list back to the file
            with open("trainlogs.csv", "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerows(new_rows)

            await interaction.response.send_message(f"Log `{id}` has been deleted.")

        except FileNotFoundError:
            await interaction.response.send_message("The log file does not exist yet.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)


    @siemens.command(name="runs", description="find the runs of unlogged siemens")
    async def trains(interaction: discord.Interaction):

        links = []
        with open("siemenlist.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                set = row[0]
                links.append(f'https://transportvic.me/metro/tracker/consist?consist={set}&date=')
        runs = "Runs for unlogged Siemens\n" + "\n".join(links)
        await interaction.response.send_message(runs)

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        user_message = str(message.content)
        if not user_message:
            return

        # Handle the '?' prefix for private responses
        if user_message[0] == '?':
            await send_message(message, user_message[1:], is_private=True)
        # Handle the !ping command
        elif user_message.lower() == "!ping":
            latency = round(client.latency * 1000)
            await message.channel.send(f"pong! {latency}ms")
        # All other messages go through the standard handler
        elif 'log' in user_message and 'logs' not in user_message:
            log = user_message.replace("log ", "")
            with open("trainsblahblajblah.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if log in row[0]:
                        log = row[0]
                        quicklog = [log]
            with open("logs.csv", mode="a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(quicklog)
            await message.channel.send(f"logged {log}!")
        elif user_message.lower() == "get logs":
            with open("logs.csv", mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    print(row)
                    log = row[0]
                    await message.channel.send(f"{log}")
        elif user_message.lower() == "clear logs":
            with open("logs.csv", "r+") as file:
                file.truncate(file.tell())
                await message.channel.send(f"Deleted Logs")
        elif user_message.lower() == "<@1451051373935329392> kill":
            if message.author.id == 1065872885559861289:
                await message.channel.send(f"Killing Bot...")
                time.sleep(3)
                await message.channel.send("Killed")
                await client.close()
        elif user_message.lower() == "<@1451051373935329392> ping zarni":
            if message.author.id == 1065872885559861289:
                for i in range(10):
                    await message.channel.send("<@1517100309686653019> send 1377544725933854800 <@1377544725933854800>")
        else:
            await send_message(message, user_message, is_private=False)


    client.run(TOKEN)

run_discord_bot()
