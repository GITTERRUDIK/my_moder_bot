import discord
from discord.ext import commands

# Задайте префикс для команд
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Событие: бот готов к работе
@bot.event
async def on_ready():
    print(f"Бот {bot.user.name} успешно запущен!")

# Команда: очистка сообщений
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"Удалено {amount} сообщений!", delete_after=5)

# Команда: кикнуть пользователя
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"Пользователь {member.mention} был кикнут. Причина: {reason}")

# Команда: забанить пользователя
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Пользователь {member.mention} был забанен. Причина: {reason}")

# Команда: разбанить пользователя
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member_name):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name == member_name:
            await ctx.guild.unban(user)
            await ctx.send(f"Пользователь {user.mention} был разбанен.")
            return
    await ctx.send(f"Пользователь с именем {member_name} не найден в бан-листе.")

# Дополнительная команда: опрос
@bot.command()
async def poll(ctx, *, question):
    message = await ctx.send(f"\ud83c\udf10 Опрос: {question}")
    await message.add_reaction("\u2705")  # Реакция ✅ (галочка)
    await message.add_reaction("\u274c")  # Реакция ❌ (крестик)

# Команда: проверить права пользователя
@bot.command()
async def permissions(ctx, member: discord.Member = None):
    member = member or ctx.author
    perms = member.guild_permissions
    embed = discord.Embed(title=f"Права пользователя {member.display_name}", color=discord.Color.blue())
    for perm, value in perms:
        embed.add_field(name=perm, value="\u2705" if value else "\u274c", inline=True)
    await ctx.send(embed=embed)

# Обработчик ошибок
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("У вас недостаточно прав для выполнения этой команды.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Не хватает аргументов для выполнения команды.")
    else:
        await ctx.send("Произошла ошибка при выполнении команды.")

# Запуск бота
import os
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
