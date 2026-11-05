# Discord Music Bot — Python Project

## Project Overview

I developed a Discord music bot using Python, discord.py, FFmpeg, and yt-dlp. The bot can connect to Discord voice channels, play music from supported URLs, and manage music queues using slash commands.

## Step 1 — Install Python

Installed Python 3.13 to run the Discord bot.

Verified the installation using:

`py -3.13 --version`

## Step 2 — Install FFmpeg

Installed FFmpeg and configured the Windows PATH environment variable.

Verified the installation using:

`ffmpeg -version`

FFmpeg is used to process audio for playback in Discord voice channels.

## Step 3 — Install Python Libraries

Installed the required Python dependencies using:

`py -3.13 -m pip install -U "discord.py[voice]" python-dotenv yt-dlp`

These libraries provide Discord API integration, voice support, environment variable management, and audio extraction.

## Step 4 — Create a Discord Application

1. Opened the Discord Developer Portal.
2. Created a new Discord application.
3. Configured the bot and its permissions.
4. Enabled the required application command scopes.
5. Invited the bot to my Discord server.

## Step 5 — Develop the Python Bot

Created `bot.py` using Visual Studio Code.

Implemented nine Discord slash commands:

- `/ping` — Check whether the bot is online.
- `/join` — Join a voice channel.
- `/play` — Play audio from a YouTube or supported audio URL.
- `/pause` — Pause the current song.
- `/resume` — Resume paused playback.
- `/skip` — Skip the current song.
- `/queue` — Display the currently playing song and upcoming tracks.
- `/stop` — Stop playback and clear the music queue.
- `/leave` — Disconnect the bot from the voice channel.

## Step 6 — Configure Environment Variables

Created a `.env` file to store the Discord bot token and server ID.

Configured `.gitignore` to prevent sensitive credentials from being uploaded to GitHub.

## Step 7 — Run the Discord Bot

Started the bot using:

`py -3.13 bot.py`

Verified that the bot successfully connected to Discord and synchronized all nine slash commands.

## Step 8 — Test the Bot

Tested the bot inside my Discord server.

- Confirmed the bot appeared online.
- Verified that slash commands were available.
- Successfully used `/play` to add a song.
- Used `/queue` to display the current song.
- Confirmed Discord voice channel connectivity.
- Verified FFmpeg audio processing through terminal logs.

## Troubleshooting

During development, I encountered and resolved several technical issues:

- Python version compatibility problems with Discord voice dependencies.
- Missing Python libraries.
- FFmpeg installation and PATH configuration.
- Discord bot authentication and connection issues.
- Slash command synchronization problems.

## Technologies Used

- Python 3.13
- discord.py
- Discord API
- FFmpeg
- yt-dlp
- Visual Studio Code
- Windows 11

## Project Summary

This project provided hands-on experience with Python programming, API integration, audio processing, dependency management, environment variables, and software troubleshooting.

The completed bot supports nine Discord slash commands and music playback functionality within Discord voice channels.
