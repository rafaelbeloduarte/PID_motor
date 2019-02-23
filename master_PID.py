# -*- coding: utf-8 -*-
import tkinter
import serial
import serial.tools.list_ports
import datetime
import time
import threading
from tkinter.filedialog import asksaveasfilename
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import sys
import os
import numpy as np
import warnings
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import webbrowser

# funções-------------------------------------------------------------------------------------

def sel():
    # LISTA AS PORTAS DISPONÍVEIS
    comlist = serial.tools.list_ports.comports()
    connected = []
    for element in comlist:
        connected.append(element.device)
    selecao = "Porta selecionada: \n" + str(var.get())
    label = Label(top)
    label.grid(row=2, column=1)
    label.configure(background = '#6689da', foreground='white', borderwidth = 3, relief = 'groove')
    label.config(text=selecao)

# def graficoinst():
#     graf_Temperatura = open('grafico.txt', 'r').read()
#     linha1 = graf_Temperatura.split('\n')
#     Temp = filter(None, linha1)
#     Temp = list(Temp)
#     temperatura1 = []
#     temperatura2 = []
#     for i in range(len(Temp)):
#         if Temp[i].startswith('Sensor 2'):
#             temporario = Temp[i].split(':')
#             temperatura1.append(temporario[1])
#         if Temp[i].startswith('Sensor 3'):
#             temporario = Temp[i].split(':')
#             temperatura2.append(temporario[1])
#     graf_tempo = open('tempo.txt', 'r').read()
#     t = graf_tempo.split('\n')
#     tempo = filter(None, t)
#     tempo = list(tempo)
#     t1 = []
#     t2 = []
#     for i in range(len(tempo)):
#         if tempo[i].startswith('t1'):
#             temporario = tempo[i].split(':')
#             t1.append(temporario[1])
#         if tempo[i].startswith('t2'):
#             temporario = tempo[i].split(':')
#             t2.append(temporario[1])
#     for i in range(len(t1)):
#         t1[i] = float(t1[i])
#     for i in range(len(t2)):
#         t2[i] = float(t2[i])
#     tempo1 = []
#     tempo2 = []
#     menor_tamanho_vetor = min(len(t1), len(t2), len(temperatura1), len(temperatura2))
#     for i in range(menor_tamanho_vetor):
#         tempo1.append(t1[i] - t1[0])
#     for i in range(menor_tamanho_vetor):
#         tempo2.append(t2[i] - t1[0])
#     temp1 = []
#     temp2 = []
#     for i in range(menor_tamanho_vetor):
#         temp1.append(float(temperatura1[i]))
#     for i in range(menor_tamanho_vetor):
#         temp2.append(float(temperatura2[i]))
#     plt.close()
#     fig1 = plt.figure()
#     ex1 = plt.subplot(2, 1, 1)
#     ex1.plot(tempo1, temp1, '-b')
#     ex1.set_ylabel('T2')
#     plt.ylabel('T2', axes=ex1)
#
#     ex2 = plt.subplot(2, 1, 2)
#     ex2.plot(tempo2, temp2, '-g')
#     ex2.set_ylabel('T3')
#     plt.ylabel('T3', axes=ex2)
#
#     plt.xlabel('Tempo (s)')
#     fig1.show()

# def grafico():
#     plt.close()
#     fig = plt.figure()
#     def animar(i):
#         plt.clf()
#         eixo1 = fig.add_subplot(2, 1, 1)
#         eixo1.plot(tempo1, temp1, '-b')
#         eixo1.set_ylabel('T2')
#         plt.ylabel('T2', axes = eixo1)
#
#         eixo2 = fig.add_subplot(2, 1, 2)
#         eixo2.plot(tempo2, temp2, '-g')
#         eixo2.set_ylabel('T3')
#         plt.ylabel('T3', axes = eixo2)
#
#         plt.xlabel('Tempo (s)')
#     ani = animation.FuncAnimation(fig, animar, interval=1000)
#     plt.show()

def selbaud():
    selection = "Baudrate: " + str(varbaud.get())
    labelbaud = Label(top)
    labelbaud.grid(row=4, column=1)
    labelbaud.config(background = '#6689da', foreground='white', borderwidth = 3, relief = 'groove', width = 14)
    labelbaud.config(text=selection)

def handle_leitura():

    try:
        ser = serial.Serial(var.get(), baudrate=varbaud.get(), timeout=1, parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS)
        ser.close()
    except Exception as e:
        messagebox.showinfo("Eita!", "Erro: " + str(e) + "\nProvável causa: a porta já está sendo utilizada.",
                            icon='error')
        return None

    if not var.get() or not varbaud.get():
        messagebox.showinfo("Aviso!", "Selecione uma porta/baudrate.")
        return None

    try:
        salvararquivo = asksaveasfilename(defaultextension=".txt", initialfile="dados")
        arquivousuario = open(salvararquivo, 'w')
    except:
        return None
    ser = serial.Serial(var.get(), baudrate=varbaud.get(), timeout=1, parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

    instr_arquivo = Label(top, text="Para finalizar a leitura apenas feche o programa, seus dados são salvos automaticamente.")
    instr_arquivo.grid(row=2, column = 2, columnspan= 5)
    instr_arquivo.configure(background='blue', foreground='white', borderwidth = 3, relief = 'groove')


    def iniciar():  # Esta função lê o inpu
        # t da porta selecionada
        arquivousuario = open(salvararquivo, 'a')
        arquivousuario.write('set point;           '.rstrip('\n'))
        arquivousuario.write('soma erro;            '.rstrip('\n'))
        arquivousuario.write('LDR;           '.rstrip('\n'))
        arquivousuario.write('r;            '.rstrip('\n'))
        arquivousuario.write('kp;            '.rstrip('\n'))
        arquivousuario.write('ki;            '.rstrip('\n'))
        arquivousuario.write('kd;            ' + '\n')
        try:
            # LOOP DE LEITURA
            while True:
                serial_bytes = ser.readline()
                serial_texto = serial_bytes.decode('utf-8')
                a = serial_texto.split(':')
                dados = '[%s]' % ', '.join(map(str, a)) + "\n"
                # ordem: set_point, soma_erro, LDR_valor, r, kp, ki, kd
                arquivousuario.write(dados + '\n')
                text.insert(INSERT, dados)
                text.see(END)
                time.sleep(1)
        except Exception as e:
            messagebox.showinfo("Erro!", "Erro: " + str(e), icon = 'error')
            pass
        ser.close()

    t = threading.Thread(target=iniciar)
    t.daemon = True
    t.start()
    arquivousuario.close()

def atualizarporta():
    comlist = serial.tools.list_ports.comports()
    connected = []
    for element in comlist:
        connected.append(element.device)
    if not connected:
        messagebox.showinfo("Aviso!", "Nenhuma porta disponível, verifique se seu dispositivo está conectado.")
    # exibe as portas disponíveis
    ports = list(serial.tools.list_ports.comports())
    for i in range(len(ports)):
        ports[i] = str(ports[i])
    for i in range(len(connected)):
        R = Radiobutton(top, text=connected[i], variable=var, value=str(connected[i]), command=sel)
        R.grid(row=1, column=2 + i)
        R.configure(background='#F2F2F2', indicatoron=0, width = 12)
        if "Arduino" in ports[i]:
            # print(ports[i])
            R.select()
            selecao = "Porta selecionada:\n" + ports[i]
            label = Label(top)
            label.grid(row=2, column=1)
            label.configure(background = '#6689da', foreground='white', borderwidth=3, relief='groove')
            label.config(text=selecao)

def reiniciar():
    confirma = messagebox.askquestion("Aviso!", "Tem certeza?",
                                      icon='warning')
    if confirma == 'yes':
        python = sys.executable
        os.execl(python, python, * sys.argv)
    else:
        return None

# fim das funções-----------------------------------------------------------------------------

# Código para os widgets vai aqui.------------------------------------------------------------

# define a janela principal----------------------------------
top = tkinter.Tk()
top.wm_title("Leitor de dados - portas serial - DEQ - UEM")
top.minsize(800, 600)
top.geometry("750x250")
top.configure(background='#6689da')
# -----------------------------------------------------------

comlist = serial.tools.list_ports.comports()
connected = []
for element in comlist:
    connected.append(element.device)
if not connected:
    messagebox.showinfo("Aviso!", "Nenhuma porta disponível, verifique se seu dispositivo está conectado.")

# var1 é uma label ("Selecione a porta:")
var1 = StringVar()
label1 = Label(top, textvariable=var1, relief=RAISED, bd=0)
var1.set("Selecione a porta:")
label1.grid(row=1, column=1)
label1.configure(background = '#6689da', foreground = 'white')

# exibe as portas disponíveis
ports = list(serial.tools.list_ports.comports())
for i in range(len(ports)):
    ports[i] = str(ports[i])
var = StringVar()  # var armazena a porta que o usuário informa
for i in range(len(connected)):
    R = Radiobutton(top, text=connected[i], variable=var, value=str(connected[i]), command=sel)
    R.grid(row=1, column=2 + i)
    R.configure(indicatoron=0, width = 12, activebackground='white', activeforeground='black')
    if "Arduino" or "Serial USB" in ports[i]:
        print(ports[i])
        R.select()
        selecao = "Porta selecionada:\n" + str(var.get())
        label = Label(top)
        label.grid(row=2, column=1)
        label.configure(background = '#6689da', foreground='white', borderwidth=3, relief='groove')
        label.config(text=selecao)
# pega o baud rate, varbaud é o baudrate e var2 é uma label============================
var2 = StringVar()
label2 = Label(top, textvariable=var2, bd=0)
var2.set("Selecione a taxa \n de transferência de \n dados (Baudrate):")
label2.grid(row=3, column=1)
label2.configure(background = '#6689da', foreground = 'white')
varbaud = IntVar()
R1 = Radiobutton(top, text="4800", variable=varbaud, value=4800, command=selbaud)
R1.grid(row=3, column=2)
R1.configure(indicatoron=0, width = 12)
R2 = Radiobutton(top, text="9600", variable=varbaud, value=9600, command=selbaud)
R2.grid(row=3, column=3)
R2.configure(indicatoron=0, width = 12)
R3 = Radiobutton(top, text="38400", variable=varbaud, value=38400, command=selbaud)
R3.grid(row=3, column=4)
R3.configure(indicatoron=0, width = 12)
R4 = Radiobutton(top, text="57600", variable=varbaud, value=57600, command=selbaud)
R4.grid(row=3, column=5)
R4.configure(indicatoron=0, width = 12)
R5 = Radiobutton(top, text="115200", variable=varbaud, value=115200, command=selbaud)
R5.grid(row=3, column=6)
R5.configure(indicatoron=0, width = 12)
R5.select()
R6 = Radiobutton(top, text="230400", variable=varbaud, value=230400, command=selbaud)
R6.grid(row=3, column=7)
R6.configure(indicatoron=0, width = 12)

selection = "Baudrate: " + str(varbaud.get())
labelbaud = Label(top)
labelbaud.grid(row=4, column=1)
labelbaud.config(background = '#6689da', foreground='white', borderwidth = 3, relief = 'groove', width = 14)
labelbaud.config(text=selection)
# =====================================================================================

espaco = Label(top, text=" ") # apenas coloca um espaço vazio no grid
espaco.grid(row=5, column=1)
espaco.configure(background = '#6689da', foreground = 'white')
# botão que chama o gráfico dos dados
# botaograf = tkinter.Button(top, text="Exibir gráfico em tempo real", command=grafico)
# botaograf.grid(row=7, column=3, columnspan = 2)
# botaograf.configure(activebackground='#000000', activeforeground='#FFFFFF', width = 25)
#
# botaograf_inst = tkinter.Button(top, text="Exibir gráfico", command=graficoinst)
# botaograf_inst.grid(row=6, column=3, columnspan = 2)
# botaograf_inst.configure(activebackground='#000000', activeforeground='#FFFFFF', width = 25)

inicia = tkinter.Button(top, text="Iniciar leitura", command=handle_leitura)
inicia.grid(row=6, column=1)
inicia.configure(activebackground='#000000', activeforeground='#FFFFFF', width = 12)

reinicia = tkinter.Button(top, text="Reiniciar", command=reiniciar, width = 12)
reinicia.grid(row=6, column=7)
reinicia.configure(activebackground='#000000', activeforeground='#FFFFFF', width = 12)

atporta = tkinter.Button(top, text="Atualizar portas", command=atualizarporta)  # botão atualizar portas
atporta.grid(row=6, column=5)
atporta.configure(activebackground='#000000', activeforeground='#FFFFFF', width = 12)

espaco2 = Label(top, text=" ") # apenas coloca um espaço vazio no grid
espaco2.grid(row=8, column=1)
espaco2.configure(background = '#6689da', foreground = 'white')


text = ScrolledText(top, width=60, height=20)
text.grid(row=9, column=3, columnspan=5, rowspan = 10)

# chama o mainloop -> abre a janela com os itens anteriores
top.mainloop()