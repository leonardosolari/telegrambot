#!/usr/bin/python3

import botogram
import os
import subprocess

bot = botogram.create("5814099651:AAGL4500bbbNOo9MC_OIQYFTzcEdJY7EN3g")

#funzioni
@bot.command("temperatura")
def showTemp(chat, message, args):
    """Mostra la temperatura della CPU"""
    try:
        command = "vcgencmd measure_temp"
        sub_ = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        subprocess_return = sub_.stdout.read()
        output = subprocess_return.decode("utf-8")
        chat.send(output)
    except:
        return "C'è stato un errore nell'esecuzione del comando"




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
    try:
        command = "./run.sh"
        sub_ = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd="/home/pi/altserver")
        chat.send("Altserver avviato")
    except:
        chat.send("C'è stato un problema nell'avvio di altserver")



@bot.command("stopaltserver")
def stopaltserver(chat, message, args):
    """ Ferma altserver """
    try:
        command1 = "screen -S altserver -X quit"
        command2 = "screen -S netmuxd -X quit"
        sub_ = subprocess.Popen(command1, shell=True, stdout=subprocess.PIPE)
        sub_ = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE)
        chat.send("Altserver fermato")
    except:
        chat.send("C'è stato un problema nel fermare altserver")


@bot.command("usage")
def usage(chat, message, args):
    """ Mostra statistiche sull'utilizzo delle risorse di sistema """
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



            

if __name__ == "__main__":
    bot.run()
