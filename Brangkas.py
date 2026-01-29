import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Struktur brangkas: kategori → material → jumlah
brangkas = {
    "pertanian": {},
    "pertambangan": {},
    "peternakan": {},
    "perminyakan": {},
    "laut": {},
    "perkayuan": {}
}

@bot.command()
async def deposit(ctx, kategori: str, material: str, jumlah: int):
    kategori = kategori.lower()
    material = material.lower()
    if kategori in brangkas:
        brangkas[kategori][material] = brangkas[kategori].get(material, 0) + jumlah
        await ctx.send(f"✅ Deposit {jumlah} {material} ke {kategori}\nSisa {material}: {brangkas[kategori][material]}")
    else:
        await ctx.send("❌ Kategori tidak ditemukan!")

@bot.command()
async def withdraw(ctx, kategori: str, material: str, jumlah: int):
    kategori = kategori.lower()
    material = material.lower()
    if kategori in brangkas and material in brangkas[kategori]:
        if brangkas[kategori][material] >= jumlah:
            brangkas[kategori][material] -= jumlah
            await ctx.send(f"✅ Withdraw {jumlah} {material} dari {kategori}\nSisa {material}: {brangkas[kategori][material]}")
        else:
            await ctx.send("❌ Stok tidak cukup!")
    else:
        await ctx.send("❌ Material tidak ditemukan!")

@bot.command(name="input")
async def input_new_material(ctx, tipe: str, kategori: str, material: str):
    if tipe.lower() == "new" and kategori.lower() in brangkas:
        material = material.lower()
        if material not in brangkas[kategori.lower()]:
            brangkas[kategori.lower()][material] = 0
            await ctx.send(f"✅ Material baru '{material}' ditambahkan ke kategori {kategori} dengan stok awal 0.")
        else:
            await ctx.send(f"⚠️ Material '{material}' sudah ada di kategori {kategori}.")
    else:
        await ctx.send("❌ Format salah atau kategori tidak ditemukan.\nGunakan: !input new material <kategori> <material>")

@bot.command()
async def brangkas(ctx):
    total_semua = 0
    output = "**📦 SISA BRANGKAS MATERIAL DISNAKER**\n"

    for kategori, materials in brangkas.items():
        for jumlah in materials.values():
            total_semua += jumlah

    output += f"\n**TOTAL SELURUH STOK: {total_semua}**\n"

    for kategori, materials in brangkas.items():
        output += f"\n**{kategori.upper()}**\n"
        if materials:
            for material, jumlah in materials.items():
                output += f"- {material.capitalize():12}: {jumlah}\n"
        else:
            output += "- (kosong)\n"

    await ctx.send(output)

bot.run("MTQ2NjI3ODYyOTEyOTQ1MzYyMQ.GFwE5C.KbiXcfU8xjrABZRHNxuf5kpz2Oob4lZsjkpRcQ")