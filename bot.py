#!/usr/bin/python3

import botogram
import subprocess
from dotenv import load_dotenv
import os

load_dotenv()

bot = botogram.create(os.environ.get('TOKEN'))

def checkid(id):
    if (id != 150816282):
        return False
    else:
        return True

def ping(chat, message, args, times):
    for i in range(times):
        if not (checkid(message.sender.id)): 
            chat.send("Utente non autorizzato")
            return
        connected = False
        while not connected:
            try:
                chat.send("Connesso!")
                connected = True
            except:
                chat.send("Tentativo di connessione...")
                pass

#funzioni

@bot.command("wake")
def wake(chat, message, args):
    ping(chat, message, args, 3)
    


@bot.command("temperatura")
def showTemp(chat, message, args):
    """Mostra la temperatura della CPU"""
    if not (checkid(message.sender.id)): 
        chat.send("Utente non autorizzato")
        return
    try:
        command = "vcgencmd measure_temp"
        sub_ = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        subprocess_return = sub_.stdout.read()
        output = subprocess_return.decode("utf-8")
        chat.send(output)
    except:
        chat.send("C'è stato un errore nell'esecuzione del comando")




@bot.timer(600)
def checkTemp(bot):
    """Se la temperatura della cpu supera i 70 gradi viene inviato un messaggio. Controllo ogni 10 minuti"""
    command = "vcgencmd measure_temp"
    sub_ = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    subprocess_return = sub_.stdout.read()
    output = subprocess_return.decode("utf-8")
    output = output.split("=")[1][:-3]
    if float(output) > 70:
        bot.chat(150816282).send("Temperatura alta!")



@bot.command("startaltserver")
def startaltserver(chat, message, args):
    """ Avvia altserver """
    if not (checkid(message.sender.id)): 
        chat.send("Utente non autorizzato")
        return 
    try:
        command = "./run.sh"
        sub_ = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd="/home/pi/altserver")
        chat.send("Altserver avviato")
    except:
        chat.send("C'è stato un problema nell'avvio di altserver")



@bot.command("stopaltserver")
def stopaltserver(chat, message, args):
    """ Ferma altserver """
    if not (checkid(message.sender.id)): 
        chat.send("Utente non autorizzato")
        return   
    try:
        command1 = """for session in $(screen -ls | grep -o '[0-9]*\.altserver'); do screen -S "${session}" -X quit; done"""
        command2 = """for session in $(screen -ls | grep -o '[0-9]*\.netmuxd'); do screen -S "${session}" -X quit; done"""
        sub_ = subprocess.Popen(command1, shell=True, stdout=subprocess.PIPE)
        sub_ = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE)
        chat.send("Altserver fermato")
    except:
        chat.send("C'è stato un problema nel fermare altserver")


@bot.command("usage")
def usage(chat, message, args):
    """ Mostra statistiche sull'utilizzo delle risorse di sistema """
    if not (checkid(message.sender.id)): 
        chat.send("Utente non autorizzato")
        return
    try:
        command_cpu = "top -n 1 -b | awk '/^%Cpu/{print $2}'"
        command_mem = "free | grep Mem | awk '{print $3/$2 * 100.0}'"
        command_temp = "vcgencmd measure_temp"
        #command_ram_GB = "free -h |grep Mem| cut -c 20-32 | sed -e 's/^[ \t]*//'"

        sub_ = subprocess.Popen(command_cpu, shell=True, stdout=subprocess.PIPE)
        subprocess_return = sub_.stdout.read()
        cpu = subprocess_return.decode("utf-8")

        sub_ = subprocess.Popen(command_mem, shell=True, stdout=subprocess.PIPE)
        subprocess_return = sub_.stdout.read()
        mem = subprocess_return.decode("utf-8")

        """sub_ = subprocess.Popen(command_ram_GB, shell=True, stdout=subprocess.PIPE)
        subprocess_return = sub_.stdout.read()
        mem_gb = subprocess_return.decode("utf-8")"""

        sub_ = subprocess.Popen(command_temp, shell=True, stdout=subprocess.PIPE)
        subprocess_return = sub_.stdout.read()
        temp = subprocess_return.decode("utf-8")
        temp = temp.split("=")[1][:-3]

        string = "CPU: " + cpu.strip('\n') + "%" + "\nRAM %: " + mem.strip('\n') + "%" + "\nTEMP: " + temp + "C"
        chat.send(string)
    except:
        chat.send("Errore nella raccolta delle statistiche")



            

def runBot():
    bot.run()

if __name__ == "__main__":
    runBot()
