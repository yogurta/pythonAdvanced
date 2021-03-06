import getpass
import requests
import configparser
import click

config = configparser.ConfigParser()

with open('auth.cfg') as f:
    config.read_file(f)
token = config['github']['token']

username = 'yogurta' # username
#password = getpass.getpass() # ask for password
password = token
#r = requests.get('https://api.github.com/users', auth = (username,password))

session = requests.Session()
session.get('https://api.github.com/users', auth = (username,password))

# přidá mě do toho tokenu, dokud to připojení existuje, tak mě to authentifikuje jako mě
session.headers = {'Authorization':'token '+ token, 'User-Agent':'Python'}

import click
@click.group()
#@click.option('-c',type = str, default = './auth.cfg',help = 'Select path to config file')
def main():
    return

@main.command() # funkce s dekorátorem je příkaz, click zpracuje argumenty př. řádky a zavolá původní funkci s příslušnými pythoními hodnotami
@click.argument('directories',nargs=-1) # type=click.Path(exists=True)
def add(directories):
    """add star to current address"""
    for directory in directories:
        session.put('https://api.github.com/user/starred/' + directory, auth = (username,password))
        click.echo('Adding star to {}'.format(directory))

@main.command()
@click.argument('directories',nargs=-1)
def remove(directories):
    """removes star from current address"""
    for directory in directories:
        session.delete('https://api.github.com/user/starred/' + directory, auth = (username,password))
        click.echo('Removing star from {}'.format(directory))

@main.command()
@click.argument('directories',nargs=-1)  #nargs = -1, znamená nekonečně argumentů
def show(directories):
    """Shows repository name with or without star"""
    #r = session.get('https://api.github.com/user/starred/pyvec/naucse.python.cz', auth = (username,password))
    for directory in directories:
        r = session.get('https://api.github.com/user/starred/'+ directory, auth = (username,password))# + input() funguje, ale musim to tam pak napsat
        print(r.status_code)
        if r.status_code == 204:
            click.echo('* ' + '{}'.format(directory))
        else:
            click.echo('{}'.format(directory))
main()
