# -*- coding: utf-8 -*-
import tkinter
import serial
import serial.tools.list_ports
import threading
from tkinter.filedialog import asksaveasfilename
from tkinter import *
import sys
import os
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
    label.configure(background='#6689da', foreground='white', borderwidth=3, relief='groove')
    label.config(text=selecao)

def graficoinst():
    plt.close()
    fig = plt.figure()
    grafico_setpoint = open('grafico_setpoint.txt', 'r').read()
    setpoint = grafico_setpoint.split('\n')
    setpoint = filter(None, setpoint)
    lista_setpoint = list(setpoint)
    for i in range(len(lista_setpoint)):
        lista_setpoint[i] = float(lista_setpoint[i])

    grafico_LDR = open('grafico_LDR.txt', 'r').read()
    LDR = grafico_LDR.split('\n')
    LDR = filter(None, LDR)
    lista_LDR = list(LDR)
    # Deve-se alimentar números ao plot, se for str o plot não consegue ordenar o eixo
    for i in range(len(lista_LDR)):
        lista_LDR[i] = float(lista_LDR[i])

    grafico_r = open('grafico_r.txt', 'r').read()
    r = grafico_r.split('\n')
    r = filter(None, r)
    lista_r = list(r)
    for i in range(len(lista_r)):
        lista_r[i] = float(lista_r[i])

    plt.clf()
    eixo = fig.add_subplot(1, 1, 1)
    eixo.plot(lista_setpoint, '-b', label='Set point')
    eixo.plot(lista_LDR, '-g', label='LDR')
    eixo.plot(lista_r, '-r', label='Resposta')
    eixo.legend()
    fig.show()

def grafico():
    plt.close()
    fig = plt.figure()
    def animar(i):
        grafico_setpoint = open('grafico_setpoint.txt', 'r').read()
        setpoint = grafico_setpoint.split('\n')
        setpoint = filter(None, setpoint)
        lista_setpoint = list(setpoint)
        for i in range(len(lista_setpoint)):
            lista_setpoint[i] = float(lista_setpoint[i])

        grafico_LDR = open('grafico_LDR.txt', 'r').read()
        LDR = grafico_LDR.split('\n')
        LDR = filter(None, LDR)
        lista_LDR = list(LDR)
        for i in range(len(lista_LDR)):
            lista_LDR[i] = float(lista_LDR[i])

        grafico_r= open('grafico_r.txt', 'r').read()
        r = grafico_r.split('\n')
        r = filter(None, r)
        lista_r = list(r)
        for i in range(len(lista_r)):
            lista_r[i] = float(lista_r[i])

        plt.clf()
        eixo = fig.add_subplot(1, 1, 1)
        eixo.plot(lista_setpoint, '-b', label='Set point')
        eixo.plot(lista_LDR, '-g', label='LDR')
        eixo.plot(lista_r, '-r', label='Resposta')
        eixo.legend()
    ani = animation.FuncAnimation(fig, animar, interval=1000)
    plt.show()

def selbaud():
    selection = "Baudrate: " + str(varbaud.get())
    labelbaud = Label(top)
    labelbaud.grid(row=4, column=1)
    labelbaud.config(background='#6689da', foreground='white', borderwidth=3, relief='groove', width=14)
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
        arquivousuario.close()
    except Exception as e:
        messagebox.showinfo(e)
        return None
    ser = serial.Serial(var.get(), baudrate=varbaud.get(), timeout=1, parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

    instr_arquivo = Label(top, text="Para finalizar a leitura apenas feche o programa, seus dados são salvos automaticamente.")
    instr_arquivo.grid(row=2, column=2, columnspan=5)
    instr_arquivo.configure(background='blue', foreground='white', borderwidth=3, relief='groove')

    def iniciar():  # Esta função lê o inpu
        # t da porta selecionada
        arquivousuario = open(salvararquivo, 'w')
        arquivousuario.write('set_point, soma_erro, LDR_valor, r, kp, ki, kd \n')
        arquivousuario.close()

        texto_lb_kp = StringVar()
        texto_lb_kp.set("Kp:")
        label_kp = Label(top, textvariable=texto_lb_kp, relief=GROOVE, bd=2)
        label_kp.grid(row=10, column=6)
        label_kp.configure(background='#6689da', foreground='white')

        texto_lb_ki = StringVar()
        texto_lb_ki.set("Ki:")
        label_ki = Label(top, textvariable=texto_lb_ki, relief=GROOVE, bd=2)
        label_ki.grid(row=12, column=6)
        label_ki.configure(background='#6689da', foreground='white')

        texto_lb_kd = StringVar()
        texto_lb_kd.set("Kd:")
        label_kd = Label(top, textvariable=texto_lb_kd, relief=GROOVE, bd=2)
        label_kd.grid(row=14, column=6)
        label_kd.configure(background='#6689da', foreground='white')

        kp = Entry(top)
        kp.grid(row=10, column=7)

        ki = Entry(top)
        ki.grid(row=12, column=7)

        kd = Entry(top)
        kd.grid(row=14, column=7)

        k = 0
        i_limpa_texto = 0

        arquivousuario = open(salvararquivo, 'a')
        graf_setpoint = open("grafico_setpoint.txt", 'w')
        graf_LDR = open("grafico_LDR.txt", 'w')
        graf_r = open("grafico_r.txt", 'w')

        rol = IntVar()

        rol_parar = Radiobutton(top, text="Parar rolagem", variable=rol, value=0)
        rol_parar.grid(row=22, column=1, columnspan = 2)
        rol_parar.configure(background='#F2F2F2', indicatoron=0, width=15)

        rol_iniciar = Radiobutton(top, text="Auto rolagem", variable=rol, value=1)
        rol_iniciar.grid(row=22, column=3, columnspan=2)
        rol_iniciar.configure(background='#F2F2F2', indicatoron=0, width=15)
        rol_iniciar.select()

        limpar_graf = IntVar()

        def limpar_graf_estado():
            limpar_graf.set(1)

        limpar_graf_botao = Button(top, text="Limpar gráfico", command=limpar_graf_estado)
        limpar_graf_botao.grid(row=6, column=5, rowspan = 2)
        limpar_graf_botao.configure(activebackground='#000000', activeforeground='#FFFFFF', width=12, height=3)

        try:
            # LOOP DE LEITURA
            while True:
                var_kp = kp.get()
                var_ki = ki.get()
                var_kd = kd.get()
                k += 1
                if (k > 10):
                    kp.delete(0, 'end')
                    ki.delete(0, 'end')
                    kd.delete(0, 'end')
                    k = 0
                if var_kp:
                    ser.write(str.encode('p' + var_kp)) #str.encode() retorna a versão da str codificada em utf-8
                if var_ki:
                    ser.write(str.encode('i' + var_ki))
                if var_kd:
                    ser.write(str.encode('d' + var_kd))

                serial_bytes = ser.readline()
                serial_texto = serial_bytes.decode('utf-8')
                a = serial_texto.split(':')
                dados = []
                dados_graf = []
                if a:
                    dados = '[%s]' % ', '.join(map(str, a))
                    # map serve para aplicarmos uma função a cada elemento de uma lista,
                    # retornando uma nova lista contendo os elementos resultantes da aplicação da função.
                    # The %s token allows to insert (and potentially format) a string.
                    # Notice that the %s token is replaced by whatever I pass to the string after the % symbol.
                    dados = dados.replace('\n', '').replace('\r', '').replace('[', '').replace(']', '')
                    dados_graf = dados.split()
                    for i in range(len(dados_graf)):
                        dados_graf[i] = dados_graf[i].replace(',', '')
                if dados_graf:
                    graf_setpoint.write(dados_graf[0] + '\n')
                    graf_setpoint.flush()
                    graf_LDR.write(dados_graf[2] + '\n')
                    graf_LDR.flush()
                    graf_r.write(dados_graf[3] + '\n')
                    graf_r.flush()
                # ordem: set_point[0], soma_erro, LDR_valor[2], r[3], kp, ki, kd
                if dados:
                    arquivousuario.write(dados + '\n')
                    arquivousuario.flush()
                    text.insert(END, dados + '\n')
                    if rol.get() == 1:
                        text.see(END)
                    i_limpa_texto += 1
                if i_limpa_texto > 1000:
                    text.delete(1.0, END)

                    graf_setpoint = open('grafico_setpoint.txt', 'r+')
                    graf_setpoint.truncate(0)
                    graf_LDR = open('grafico_LDR.txt', 'r+')
                    graf_LDR.truncate(0)
                    graf_r = open('grafico_r.txt', 'r+')
                    graf_r.truncate(0)

                    i_limpa_texto = 0
                if limpar_graf.get() == 1:
                    graf_setpoint = open('grafico_setpoint.txt', 'r+')
                    graf_setpoint.truncate(0)
                    graf_LDR = open('grafico_LDR.txt', 'r+')
                    graf_LDR.truncate(0)
                    graf_r = open('grafico_r.txt', 'r+')
                    graf_r.truncate(0)

                    limpar_graf.set(0)

                # time.sleep(1)
        except Exception as e:
            messagebox.showinfo("Erro!", "Erro: " + str(e), icon='error')
            pass
        ser.close()
        graf_LDR.close()
        graf_r.close()
        graf_setpoint.close()
        arquivousuario.close()

    t = threading.Thread(target=iniciar)
    t.daemon = True
    t.start()

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
        R.configure(background='#F2F2F2', indicatoron=0, width=12)
        if "Arduino" in ports[i]:
            # print(ports[i])
            R.select()
            selecao = "Porta selecionada:\n" + ports[i]
            label = Label(top)
            label.grid(row=2, column=1)
            label.configure(background='#6689da', foreground='white', borderwidth=3, relief='groove')
            label.config(text=selecao)

def reiniciar():
    if messagebox.askokcancel("Reiniciando...", "Tem certeza?"):
        python = sys.executable
        os.execl(python, python, *sys.argv)
    else:
        return None

def fechando():
    if messagebox.askokcancel("Fechando...", "Tem certeza?"):
        plt.close('all')
        top.destroy()

# fim das funções-----------------------------------------------------------------------------

# Código para os widgets vai aqui.------------------------------------------------------------

# define a janela principal----------------------------------
top = tkinter.Tk()
top.wm_title("Leitor de dados - portas serial - DEQ - UEM")
top.minsize(750, 650)
top.geometry("750x650")
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
label1.configure(background='#6689da', foreground='white')

# exibe as portas disponíveis
ports = list(serial.tools.list_ports.comports())
for i in range(len(ports)):
    ports[i] = str(ports[i])
var = StringVar()  # var armazena a porta que o usuário informa
for i in range(len(connected)):
    R = Radiobutton(top, text=connected[i], variable=var, value=str(connected[i]), command=sel)
    R.grid(row=1, column=2 + i)
    R.configure(indicatoron=0, width=12, activebackground='white', activeforeground='black')
    if "Arduino" or "Serial USB" in ports[i]:
        print(ports[i])
        R.select()
        selecao = "Porta selecionada:\n" + str(var.get())
        label = Label(top)
        label.grid(row=2, column=1)
        label.configure(background='#6689da', foreground='white', borderwidth=3, relief='groove')
        label.config(text=selecao)
# pega o baud rate, varbaud é o baudrate e var2 é uma label============================
var2 = StringVar()
label2 = Label(top, textvariable=var2, bd=0)
var2.set("Selecione a taxa \n de transferência de \n dados (Baudrate):")
label2.grid(row=3, column=1)
label2.configure(background='#6689da', foreground='white')
varbaud = IntVar()
R1 = Radiobutton(top, text="4800", variable=varbaud, value=4800, command=selbaud)
R1.grid(row=3, column=2)
R1.configure(indicatoron=0, width=12)
R2 = Radiobutton(top, text="9600", variable=varbaud, value=9600, command=selbaud)
R2.grid(row=3, column=3)
R2.configure(indicatoron=0, width=12)
R3 = Radiobutton(top, text="38400", variable=varbaud, value=38400, command=selbaud)
R3.grid(row=3, column=4)
R3.configure(indicatoron=0, width=12)
R4 = Radiobutton(top, text="57600", variable=varbaud, value=57600, command=selbaud)
R4.grid(row=3, column=5)
R4.configure(indicatoron=0, width=12)
R5 = Radiobutton(top, text="115200", variable=varbaud, value=115200, command=selbaud)
R5.grid(row=3, column=6)
R5.configure(indicatoron=0, width=12)
R5.select()
R6 = Radiobutton(top, text="230400", variable=varbaud, value=230400, command=selbaud)
R6.grid(row=3, column=7)
R6.configure(indicatoron=0, width=12)

selection = "Baudrate: " + str(varbaud.get())
labelbaud = Label(top)
labelbaud.grid(row=4, column=1)
labelbaud.config(background='#6689da', foreground='white', borderwidth=3, relief='groove', width=14)
labelbaud.config(text=selection)
# =====================================================================================

espaco = Label(top, text=" ")  # apenas coloca um espaço vazio no grid
espaco.grid(row=5, column=1)
espaco.configure(background='#6689da', foreground='white')
# botão que chama o gráfico dos dados
botaograf = tkinter.Button(top, text="Exibir gráfico em tempo real", command=grafico)
botaograf.grid(row=7, column=3, columnspan = 2)
botaograf.configure(activebackground='#000000', activeforeground='#FFFFFF', width = 25)

botaograf_inst = tkinter.Button(top, text="Exibir gráfico", command=graficoinst)
botaograf_inst.grid(row=6, column=3, columnspan = 2)
botaograf_inst.configure(activebackground='#000000', activeforeground='#FFFFFF', width = 25)


inicia = tkinter.Button(top, text="Iniciar leitura", command=handle_leitura)
inicia.grid(row=6, column=1)
inicia.configure(activebackground='#000000', activeforeground='#FFFFFF', width=12)

reinicia = tkinter.Button(top, text="Reiniciar", command=reiniciar, width=12)
reinicia.grid(row=6, column=7)
reinicia.configure(activebackground='#000000', activeforeground='#FFFFFF', width=12)

atporta = tkinter.Button(top, text="Atualizar portas", command=atualizarporta)  # botão atualizar portas
atporta.grid(row=6, column=6)
atporta.configure(activebackground='#000000', activeforeground='#FFFFFF', width=12)

espaco2 = Label(top, text=" ")  # apenas coloca um espaço vazio no grid
espaco2.grid(row=8, column=1)
espaco2.configure(background='#6689da', foreground='white')

label_variaveis = Label(top, text="Set point      soma erro     LDR_valor        r          kp       ki       kd")
label_variaveis.grid(row=9, column=1, columnspan=4)
label_variaveis.configure(background='#6689da', foreground='white')

text = ScrolledText(top, width=50, height=20)
text.grid(row=11, column=1, columnspan=5, rowspan=10)

# chama o mainloop -> abre a janela com os itens anteriores
top.protocol("WM_DELETE_WINDOW", fechando)
top.mainloop()