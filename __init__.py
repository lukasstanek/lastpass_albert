""" LastPass Extension """

import subprocess
from albertv0 import *
import re
import os

__iid__ = "PythonInterface/v0.2"
__prettyname__ = "LastPass"
__version__ = "0.1"
__trigger__ = "lp "
__author__ = "Lukas Stanek"
__dependencies__ = []

termIcon = "%s/%s.svg" % (os.path.dirname(__file__), 'terminal')
lockIcon = "%s/%s.svg" % (os.path.dirname(__file__), 'unlock')

ls_pattern = re.compile('^(.*)\/(.+) \[id: ([0-9]{19})]')

def handleQuery(query):

    if query.isTriggered:
        items = []

        statusProcess = subprocess.run(['lpass', 'status'], stdout=subprocess.DEVNULL)

        #not logged in
        if statusProcess.returncode != 0:
            items.extend(handle_query_while_logged_out(query))
        else:
            items.extend(handle_query_while_logged_in(query))

        items.extend(handle_cli_commands(query))

        return items
    
def handle_query_while_logged_in(query):
    items = []
    # query lastpass for passwords
    result = subprocess.run(["lpass", "ls"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)            

    lines = result.stdout.splitlines()
    for line in lines:
        line = line.decode('utf-8')
        # info(line)
        matches = ls_pattern.match(line)
        if matches is None:
            continue
        
        group = matches.group(1)
        domain = matches.group(2)
        lp_id = matches.group(3)

        if query.string not in domain:
            continue

        username = subprocess.run(['lpass', 'show', '--username', lp_id], stdout=subprocess.PIPE).stdout.decode('utf-8')

        items.append(
            Item(
                text=f"{domain}", 
                subtext=f"{username} - Group: {group}", 
                icon=lockIcon,
                actions=[
                    FuncAction("Copy Password", lambda id=lp_id: subprocess.run(['lpass', 'show', '--password', '-c', id]))
                ]))
    return items


def handle_query_while_logged_out(query):
    return [Item(text="You are not logged in, try 'lp login {email}'", icon=termIcon)]

def handle_cli_commands(query):
    items = []
    splits = query.string.split(' ')
    if splits[0] in "login":
        email = splits[1] if len(splits) > 1 else ""
        items.append(
            Item(
                text="Login", 
                subtext="lp login {email}", 
                completion="lp login ", 
                icon=termIcon,
                actions=[
                    ProcAction("Login", ["lpass", "login", email])
            ]))
    if splits[0] in "logout":
        items.append(
            Item(
                text="Logout", 
                subtext="lp logout", 
                completion="lp logout", 
                icon=termIcon,
                actions=[
                    ProcAction("Logout", ["lpass", "logout", "-f"])
            ]))
    # if splits[0] in "sync":
    #     items.append(
    #         Item(
    #             text="Sync", 
    #             subtext="lp sync", 
    #             completion="lp sync", 
    #             actions=[
    #                 ProcAction("Sync", ["lpass", "sync"])
            # ]))
    return items