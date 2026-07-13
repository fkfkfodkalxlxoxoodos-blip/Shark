import discord
from discord import app_commands
from discord.ext import commands
import json
import os

TOKEN = ""

ARCHIVO = "equipos.json"

if not os.path.exists(ARCHIVO):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump({}, f)

def cargar_datos():
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_datos(datos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot conectado como {bot.user}")

@bot.tree.command(name="equipo_agregar", description="Agregar un equipo")
@app_commands.describe(nombre="Nombre del equipo")
async def equipo_agregar(interaction: discord.Interaction, nombre: str):

    datos = cargar_datos()

    if nombre in datos:
        await interaction.response.send_message(
            f"❌ El equipo **{nombre}** ya existe.",
            ephemeral=True
        )
        return

    datos[nombre] = 0
    guardar_datos(datos)

    await interaction.response.send_message(
        f"✅ Equipo **{nombre}** agregado con 0 puntos."
    )

@bot.tree.command(name="equipo_eliminar", description="Eliminar un equipo")
@app_commands.describe(nombre="Nombre del equipo")
async def equipo_eliminar(interaction: discord.Interaction, nombre: str):

    datos = cargar_datos()

    if nombre not in datos:
        await interaction.response.send_message(
            "❌ Ese equipo no existe.",
            ephemeral=True
        )
        return

    del datos[nombre]
    guardar_datos(datos)

    await interaction.response.send_message(
        f"🗑️ Equipo **{nombre}** eliminado."
    )

@bot.tree.command(name="agg", description="Agregar puntos a un equipo")
@app_commands.describe(equipo="Nombre del equipo", puntos="Cantidad de puntos")
async def agg(interaction: discord.Interaction, equipo: str, puntos: int):

    datos = cargar_datos()

    if equipo not in datos:
        await interaction.response.send_message(
            "❌ Ese equipo no existe.",
            ephemeral=True
        )
        return

    datos[equipo] += puntos
    guardar_datos(datos)

    await interaction.response.send_message(
        f"✅ Se agregaron **{puntos}** punto(s) a **{equipo}**.\nAhora tiene **{datos[equipo]}** puntos."
    )

@bot.tree.command(name="demote", description="Quitar puntos a un equipo")
@app_commands.describe(equipo="Nombre del equipo", puntos="Cantidad de puntos")
async def demote(interaction: discord.Interaction, equipo: str, puntos: int):

    datos = cargar_datos()

    if equipo not in datos:
        await interaction.response.send_message(
            "❌ Ese equipo no existe.",
            ephemeral=True
        )
        return

    datos[equipo] -= puntos
    guardar_datos(datos)

    await interaction.response.send_message(
        f"➖ Se quitaron **{puntos}** punto(s) a **{equipo}**.\nAhora tiene **{datos[equipo]}** puntos."
    )

@bot.tree.command(name="puntos", description="Ver los puntos de todos los equipos")
async def puntos(interaction: discord.Interaction):

    datos = cargar_datos()

    if not datos:
        await interaction.response.send_message("📭 No hay equipos registrados.")
        return

    mensaje = "📋 **PUNTOS DE LOS EQUIPOS**\n\n"

    for equipo, pts in datos.items():
        mensaje += f"⚽ {equipo}: **{pts}** puntos\n"

    await interaction.response.send_message(mensaje)

@bot.tree.command(name="tabla", description="Mostrar la tabla de posiciones")
async def tabla(interaction: discord.Interaction):

    datos = cargar_datos()

    if not datos:
        await interaction.response.send_message("📭 No hay equipos registrados.")
        return

    ordenados = sorted(datos.items(), key=lambda x: x[1], reverse=True)

    mensaje = "🏆 **TABLA DE POSICIONES** 🏆\n\n"

    posicion = 1

    for equipo, pts in ordenados:

        if posicion == 1:
            emoji = "🥇"
        elif posicion == 2:
            emoji = "🥈"
        elif posicion == 3:
            emoji = "🥉"
        else:
            emoji = f"{posicion}."

        mensaje += f"{emoji} {equipo} — **{pts}** pts\n"

        posicion += 1

    await interaction.response.send_message(mensaje)

bot.run(TOKEN)