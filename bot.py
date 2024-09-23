import discord
from discord.ext import commands
import os
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="a!", intents = intents)

#LISTAS
lista = []
lugares = "lugares.txt"

#VARIÁVEIS
i_jogadores = 0
i_invasor = 0
invasor = 0

def contar_linhas(arq):
    with open(arq, 'r', encoding='utf-8') as arquivo:
        return int (sum(1 for linha in arquivo))

#Funções
def pegar_palavra(num):
    with open(lugares, "r", encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()
        palavra = (str (linhas[num]))
    arquivo.close()
    return palavra

@bot.command()
async def add(ctx:commands.Context):
    usuario = ctx.author
    #adicionar jogadores no jogo
    if str (usuario.name) not in lista:
        lista.append(str (usuario.name))
        await ctx.send(f"{usuario.name} adicionado")

@bot.command() #ver jogadores que já estão no jogo
async def jogadores(ctx:commands.Context):
    await ctx.reply(lista)

@bot.command()
async def jogar(ctx:commands.Context):
    if (len(lista) < 3):
        await ctx.send(f"jogadores insuficientes")
    else:
        #variáveis
        total_palavras = contar_linhas(lugares)
        total_jogadores = len(lista)

        #escolhendo aleatoriamente jogadores e palavras
        invasor = (random.sample(range(total_jogadores), k=1))[0]
        i_jogadores, i_invasor = random.sample(range(1,total_palavras), k=2)
        nome_invasor = lista[invasor]

        #mandando mensagens na dm
        for member in bot.guilds[0].members:
            if str(member) == str(nome_invasor):
                palavra = pegar_palavra(i_invasor)
                await member.send(palavra)
            else:
                if str(member) in lista:
                    palavra = pegar_palavra(i_jogadores)
                    await member.send(palavra)

        await ctx.send(f"JOGO INICIADO!")

@bot.command() #limpar lista de jogadores
async def limpar(ctx:commands.Context):
    lista.clear()
    await ctx.send("Jogadores resetados.")

@bot.event
async def on_ready():
    print("ESTOU PRONTO")


bot.run("CHAVE")
