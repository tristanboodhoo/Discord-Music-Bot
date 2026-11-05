# Discord Music Bot — Python Project

## Project Overview

I developed a Discord music bot using Python, discord.py, FFmpeg, and yt-dlp. The bot connects to Discord voice channels, plays audio from supported URLs, and manages music queues through slash commands.

This project demonstrates Python programming, API integration, software configuration, audio processing, and technical troubleshooting.

## Technologies Used

- Python 3.13
- discord.py
- Discord API
- FFmpeg
- yt-dlp
- Visual Studio Code
- Windows 11

## Features

The bot supports nine Discord slash commands:

| Command | Description |
|---|---|
| `/ping` | Check whether the bot is online |
| `/join` | Join a voice channel |
| `/play` | Play audio from a YouTube or supported audio URL |
| `/pause` | Pause the current song |
| `/resume` | Resume paused music |
| `/skip` | Skip the current song |
| `/queue` | Display the current song and upcoming tracks |
| `/stop` | Stop playback and clear the queue |
| `/leave` | Disconnect from the voice channel |

## Project Setup and Configuration

### Step 1 — Install Python

Installed Python 3.13 and verified the installation using:

`py -3.13 --version`

### Step 2 — Install FFmpeg

Installed FFmpeg and configured the Windows PATH environment variable.

Verified the installation using:

`ffmpeg -version`

FFmpeg handles audio processing for Discord voice playback.

### Step 3 — Install Python Dependencies

Installed the required Python libraries using:

`py -3.13 -m pip install -U "discord.py[voice]" python-dotenv yt-dlp`

### Step 4 — Create the Discord Application

1. Opened the Discord Developer Portal.
2. Created a Discord application and bot.
3. Configured the required permissions.
4. Enabled the bot and application command installation scopes.
5. Invited the bot to my Discord server.

### Step 5 — Develop the Python Bot

Created `bot.py` using Visual Studio Code.

Implemented nine slash commands, voice channel connectivity, music playback, and queue management.

Used yt-dlp to extract audio information and FFmpeg to process audio for playback.

### Step 6 — Configure Environment Variables

Created a `.env` file containing the Discord bot token and server ID.

Example configuration:

`DISCORD_TOKEN=YOUR_BOT_TOKEN`

`GUILD_ID=YOUR_SERVER_ID`

Configured `.gitignore` to prevent sensitive credentials from being uploaded to GitHub.

### Step 7 — Start the Bot

Started the application using:

`py -3.13 bot.py`

Verified that the bot successfully connected to Discord and synchronized all nine slash commands.

### Step 8 — Test the Bot

Tested the bot inside my Discord server.

- Confirmed the bot appeared online.
- Verified that the slash commands were registered.
- Successfully used `/play` to add a song.
- Used `/queue` to display the currently playing song.
- Confirmed successful Discord voice channel connectivity.
- Verified FFmpeg execution through terminal logs.

## Project Screenshots

### 1. Project Structure

Visual Studio Code showing the Discord Music Bot project files and Python source code.

![Project Structure](screenshots/01-project-structure.png)

### 2. Python Source Code

The `/play` command implementation, including voice channel validation and URL checking.

![Python Source Code](screenshots/02-python%20code.png)

### 3. Bot Running Successfully

Terminal showing the bot connected to Discord and all nine slash commands synchronized.

![Bot Online](screenshots/03-bot-online.png)

### 4. Discord Slash Commands

Discord displaying the bot's available slash commands.

![Slash Commands](screenshots/04-slashcommands.png)

### 5. Music Playback Command

Discord showing a successful `/play` command response and a song added to the queue.

![Music Playback](screenshots/05-music-playback.png)

### 6. Music Queue

Discord showing the currently playing song using the `/queue` command.

![Music Queue](screenshots/06-music-queue.png)

## Troubleshooting

During development, I encountered and resolved several technical issues:

- Python version compatibility problems with Discord voice dependencies.
- Missing Python libraries and dependency installation errors.
- FFmpeg installation and Windows PATH configuration.
- Discord bot authentication and connection issues.
- Slash command synchronization problems.

## Skills Demonstrated

- Python programming
- Discord API integration
- Software installation and configuration
- Dependency management
- FFmpeg audio processing
- Troubleshooting and debugging
- Environment variable management
- Technical documentation

## Project Summary

Successfully developed and tested a Python Discord music bot with nine slash commands, audio playback functionality, voice channel integration, and music queue management.

This project provided hands-on experience with Python development, API integration, application configuration, and technical troubleshooting.
  
