# template-py-discordbot
Template for python discord bot with project structure. Initially made for a friend. 

Discord Moderation Bot (Python)

This project is a Python-based Discord moderation bot with a modular structure that separates commands and events. It uses the discord.py library and the python-dotenv package to manage environment variables securely.

Features
* Slash commands
* Event handling
* Commands and events organized into separate folders

## project Structure

```
discord-bot/
│
├── bot.py          # Main Python file
├── commands/       # Folder for slash commands
│   ├── __init__.py # (Leave this file empty or for imports)
│   └── ping.py     # Example slash command
├── events/         # Folder for event handling
│   ├── __init__.py # (Leave this file empty or for imports)
│   └── on_ready.py # Example event
├── config.py       # Optional configuration file (e.g., token)
├── .env            # Environment file (for sensitive data)
└── README.md       # Project documentation
```

## Prerequisites

- Python 3.8 or higher
- A Discord bot token (you can create one from the [Discord Developer Portal](https://discord.com/developers/applications))
- [Git](https://git-scm.com/)
- [pip](https://pip.pypa.io/en/stable/)

## Setup Guide

### Step 1: Clone the Repository

First, clone the repository to your local machine using Git:

```bash
git clone https://github.com/NoctDevT/discord-moderation-bot-python.git
cd discord-moderation-bot-python
```

### Step 2: Install the Dependencies

Use `pip` to install the necessary dependencies for the project:

```bash
pip install -r requirements.txt
```

Make sure the `requirements.txt` contains the following packages:

```
discord.py
python-dotenv
```

If `requirements.txt` doesn't exist, create it with:

```bash
pip freeze > requirements.txt
```

### Step 3: Set Up the Environment Variables

Create a `.env` file in the root of the project with your Discord bot token. The `.env` file should look like this:

```bash
TOKEN=your-bot-token-here
```

### Step 4: Run the Bot

Run the bot by executing `bot.py`:

```bash
python bot.py
```

If everything is set up correctly, you should see a message in the console indicating that the bot has successfully logged in:

```bash
Logged in as BOT_NAME!
```

## Bot Commands and Events

- **Slash Commands**: Commands are defined in the `commands/` folder. You can add more commands by creating new Python files and following the structure of `ping.py`.
- **Events**: Event handlers are defined in the `events/` folder. You can create new event handlers by adding Python files and defining event listeners.

## Example Commands

- **Ping Command**: Replies with "Pong!" when the `/ping` command is used.
