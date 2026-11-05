
import os
import asyncio
import logging
from collections import deque

import discord
import yt_dlp
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing from .env")

if not GUILD_ID:
    raise RuntimeError("GUILD_ID is missing from .env")

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()

YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

# Music queues for each Discord server
queues = {}
current_songs = {}


class MusicBot(commands.Bot):
    async def setup_hook(self):
        guild = discord.Object(id=int(GUILD_ID))
        self.tree.copy_global_to(guild=guild)
        synced = await self.tree.sync(guild=guild)
        print(f"Synced {len(synced)} commands to your server.")


bot = MusicBot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")


def get_queue(guild_id):
    if guild_id not in queues:
        queues[guild_id] = deque()
    return queues[guild_id]


def extract_audio(query):
    with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ydl:
        info = ydl.extract_info(query, download=False)

        if "entries" in info:
            info = next(
                (entry for entry in info["entries"] if entry),
                None
            )

        if not info:
            raise RuntimeError("No playable audio found.")

        return {
            "title": info.get("title", "Unknown Song"),
            "url": info["url"],
            "webpage": info.get("webpage_url", query),
        }


async def play_next(guild):
    voice = guild.voice_client
    if not voice or not voice.is_connected():
        return

    queue = get_queue(guild.id)

    if not queue:
        current_songs.pop(guild.id, None)
        return

    song = queue.popleft()

    try:
        # Refresh the stream URL before playback
        song = await asyncio.to_thread(
            extract_audio, song["webpage"]
        )

        source = discord.FFmpegPCMAudio(
            song["url"],
            **FFMPEG_OPTIONS
        )

        current_songs[guild.id] = song

        def after_playing(error):
            if error:
                logging.error("Playback error: %s", error)

            future = asyncio.run_coroutine_threadsafe(
                play_next(guild),
                bot.loop
            )

            try:
                future.result()
            except Exception:
                logging.exception("Queue playback failed")

        voice.play(source, after=after_playing)

    except Exception:
        logging.exception("Could not play song")
        await play_next(guild)


@bot.tree.command(
    name="ping",
    description="Check whether the music bot is online"
)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Music Bot is online!"
    )


@bot.tree.command(
    name="join",
    description="Join your voice channel"
)
@app_commands.guild_only()
async def join(interaction: discord.Interaction):
    member = interaction.user

    if not member.voice or not member.voice.channel:
        await interaction.response.send_message(
            "Join a voice channel first.",
            ephemeral=True
        )
        return

    channel = member.voice.channel
    voice = interaction.guild.voice_client

    try:
        if voice:
            await voice.move_to(channel)
        else:
            await channel.connect()

        await interaction.response.send_message(
            f"Joined {channel.name}!"
        )
    except Exception:
        logging.exception("Voice connection failed")
        await interaction.response.send_message(
            "Could not join the voice channel.",
            ephemeral=True
        )


@bot.tree.command(
    name="play",
    description="Play a song from a YouTube or audio URL"
)
@app_commands.describe(url="YouTube or direct audio URL")
@app_commands.guild_only()
async def play(interaction: discord.Interaction, url: str):
    member = interaction.user

    if not member.voice or not member.voice.channel:
        await interaction.response.send_message(
            "Join a voice channel first.",
            ephemeral=True
        )
        return

    if not url.startswith(("https://", "http://")):
        await interaction.response.send_message(
            "Enter a valid YouTube or audio URL.",
            ephemeral=True
        )
        return

    await interaction.response.defer()

    try:
        voice = interaction.guild.voice_client
        channel = member.voice.channel

        if not voice:
            voice = await channel.connect()
        elif voice.channel != channel:
            await voice.move_to(channel)

        song = await asyncio.to_thread(extract_audio, url)

        queue = get_queue(interaction.guild.id)
        queue.append(song)

        await interaction.followup.send(
            f"Added to queue: **{song['title']}**"
        )

        if not voice.is_playing() and not voice.is_paused():
            await play_next(interaction.guild)

    except Exception:
        logging.exception("Play command failed")
        await interaction.followup.send(
            "Unable to play this URL. Check the terminal for errors."
        )


@bot.tree.command(
    name="pause",
    description="Pause the current song"
)
@app_commands.guild_only()
async def pause(interaction: discord.Interaction):
    voice = interaction.guild.voice_client

    if voice and voice.is_playing():
        voice.pause()
        await interaction.response.send_message("Music paused.")
    else:
        await interaction.response.send_message(
            "Nothing is currently playing.",
            ephemeral=True
        )


@bot.tree.command(
    name="resume",
    description="Resume the paused song"
)
@app_commands.guild_only()
async def resume(interaction: discord.Interaction):
    voice = interaction.guild.voice_client

    if voice and voice.is_paused():
        voice.resume()
        await interaction.response.send_message("Music resumed.")
    else:
        await interaction.response.send_message(
            "Nothing is paused.",
            ephemeral=True
        )


@bot.tree.command(
    name="skip",
    description="Skip the current song"
)
@app_commands.guild_only()
async def skip(interaction: discord.Interaction):
    voice = interaction.guild.voice_client

    if voice and (voice.is_playing() or voice.is_paused()):
        voice.stop()
        await interaction.response.send_message("Song skipped.")
    else:
        await interaction.response.send_message(
            "Nothing to skip.",
            ephemeral=True
        )


@bot.tree.command(
    name="queue",
    description="Show upcoming songs"
)
@app_commands.guild_only()
async def show_queue(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    queue = get_queue(guild_id)

    lines = []

    current = current_songs.get(guild_id)

    if current:
        lines.append(f"Now playing: {current['title']}")

    for index, song in enumerate(list(queue)[:10], start=1):
        lines.append(f"{index}. {song['title']}")

    if not lines:
        lines.append("The music queue is empty.")

    await interaction.response.send_message(
        "\n".join(lines)
    )


@bot.tree.command(
    name="stop",
    description="Stop playback and clear the queue"
)
@app_commands.guild_only()
async def stop(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    get_queue(guild_id).clear()
    current_songs.pop(guild_id, None)

    voice = interaction.guild.voice_client

    if voice:
        voice.stop()

    await interaction.response.send_message(
        "Music stopped and queue cleared."
    )


@bot.tree.command(
    name="leave",
    description="Disconnect from the voice channel"
)
@app_commands.guild_only()
async def leave(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    get_queue(guild_id).clear()
    current_songs.pop(guild_id, None)

    voice = interaction.guild.voice_client

    if voice:
        await voice.disconnect()
        await interaction.response.send_message(
            "Disconnected from voice channel."
        )
    else:
        await interaction.response.send_message(
            "I'm not in a voice channel.",
            ephemeral=True
        )


bot.run(TOKEN)
