from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, FloodWaitError
from telethon.tl import functions
import time
import os
import asyncio
import random
import logging
import sys
import itertools
import shutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

api_id = 23877053
api_hash = '989c360358b981dae46a910693ab2f4c'

# ANSI color codes
COLORS = {
    'green': '\033[92m',
    'red': '\033[91m',
    'cyan': '\033[96m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'white': '\033[97m',
    'reset': '\033[0m'
}

def print_colored(text, color, end='\n'):
    print(f"{COLORS[color]}{text}{COLORS['reset']}", end=end)

def get_terminal_width():
    """Get the current terminal width, defaulting to 80 if unavailable."""
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80

def print_box(text, style='double', color='cyan'):
    """Prints a styled text box with dynamic width."""
    width = min(get_terminal_width(), 80)  # Cap width at 80 or terminal size
    if style == 'double':
        top = f"╔{'═' * (width - 2)}╗"
        bottom = f"╚{'═' * (width - 2)}╝"
        side = '║'
    elif style == 'single':
        top = f"┌{'─' * (width - 2)}┐"
        bottom = f"└{'─' * (width - 2)}┘"
        side = '│'
    else:
        top = f"█{'█' * (width - 2)}█"
        bottom = f"█{'█' * (width - 2)}█"
        side = '█'
    
    print_colored(top, color)
    lines = [text[i:i + width - 4] for i in range(0, len(text), width - 4)]
    for line in lines:
        print_colored(f"{side} {line:<{width - 4}} {side}", color)
    print_colored(bottom, color)

def print_section_header(title):
    """Prints a section header with a horizontal rule."""
    width = min(get_terminal_width(), 80)
    print_colored(f"{'═' * width}", 'magenta')
    print_colored(f"{title:^{width}}", 'white')
    print_colored(f"{'═' * width}", 'magenta')

def print_banner():
    """Prints a futuristic, multi-layered banner."""
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = r"""
       
            ████████╗ ██████╗     ███████╗                           
           ╚══██╔══╝██╔════╝     ██╔════╝                           
              ██║   ██║  ███╗    ███████╗                           
              ██║   ██║   ██║    ╚════██║                           
              ██║   ╚██████╔╝    ███████║                           
                                           
        
    """
    colors = ['cyan', 'blue', 'magenta', 'cyan', 'blue', 'magenta', 'cyan']
    for i, line in enumerate(banner.split('\n')):
        print_colored(line, colors[i % len(colors)])
    print_box(" TELEGRAM SCRAPER ", style='double', color='white')
    print_colored("          Developed by Muhammad Riyad ", 'green')
    print()

def loading_animation(message, duration=2, style='pulse'):
    """Displays a sophisticated loading animation."""
    width = 30
    if style == 'pulse':
        frames = ['.', '..', '...', '....']
        start_time = time.time()
        print_colored(f"{message} ", 'yellow', end='')
        while time.time() - start_time < duration:
            for frame in frames:
                print_colored(f"\r{message} {frame}", 'yellow', end='')
                sys.stdout.flush()
                time.sleep(0.2)
        print()
    elif style == 'segment':
        print_colored(f"{message}", 'yellow')
        for i in range(width + 1):
            percent = (i / width) * 100
            bar = '█' * (i // 2) + ' ' * ((width - i) // 2)
            print_colored(f"\r[{bar}] {percent:3.0f}%", 'blue', end='')
            sys.stdout.flush()
            time.sleep(duration / width)
        print()

client = TelegramClient('session_name', api_id, api_hash)

async def resolve_group(group_input):
    loading_animation("Resolving group", duration=1, style='pulse')
    if group_input.startswith('https://t.me/'):
        try:
            invite = await client(functions.messages.CheckChatInviteRequest(hash=group_input.split('/')[-1]))
            return invite.chat
        except Exception as e:
            print_colored(f"Error resolving invite link: {e}", 'red')
            raise
    return await client.get_entity(group_input)

async def main():
    print_banner()
    
    print_section_header("Group Or Chennel Configuration")
    group_to_scrape = input(f"{COLORS['blue']}Source group (without @ or invite link): {COLORS['reset']}").strip()
    group_to_add = input(f"{COLORS['blue']}Target group (without @ or invite link): {COLORS['reset']}").strip()
    try:
        max_members = int(input(f"{COLORS['blue']}Number of members to add (default 10): {COLORS['reset']}") or 10)
    except ValueError:
        max_members = 10
        print_colored("Invalid input, defaulting to 10 members", 'yellow')

    if not await client.is_user_authorized():
        print_section_header("Authentication")
        phone_number = input(f"{COLORS['blue']}Phone number: {COLORS['reset']}")
        loading_animation("Requesting OTP", duration=2, style='segment')
        await client.send_code_request(phone_number)
        otp = input(f"{COLORS['blue']}Enter OTP: {COLORS['reset']}")
        try:
            await client.sign_in(phone_number, otp)
        except SessionPasswordNeededError:
            password = input(f"{COLORS['blue']}Enter 2FA password: {COLORS['reset']}")
            await client.sign_in(password=password)
        print_box("Authentication successful", style='single', color='green')
    else:
        print_box("Session active", style='single', color='green')

    try:
        group_to_scrape = await resolve_group(group_to_scrape)
        group_to_add = await resolve_group(group_to_add)
    except Exception as e:
        print_colored(f"Failed to fetch group: {e}", 'red')
        return

    print_section_header("Analyzing Target Group")
    loading_animation("Fetching existing members", duration=2, style='segment')
    existing_members = await client.get_participants(group_to_add)
    existing_ids = {member.id for member in existing_members}
    print_box(f"Found {len(existing_ids)} existing members", style='single', color='cyan')

    print_section_header("Scraping Source Group")
    members = []
    async for member in client.iter_participants(group_to_scrape):
        members.append(member)
        print_colored(f"\rScraped {len(members)} members...", 'blue', end='')
        sys.stdout.flush()
    print()
    print_box(f"Total members scraped: {len(members)}", style='single', color='cyan')

    print_section_header("Adding Members")
    added_count = 0
    for i, member in enumerate(members):
        if added_count >= max_members:
            print_box(f"Reached limit of {max_members} members", style='double', color='white')
            break

        if member.bot or member.username is None:
            print_colored(f"Skipping user {member.id}: Bot or no username", 'red')
            continue
        if member.id in existing_ids:
            print_colored(f"Skipping {member.username}: Already in group", 'cyan')
            continue

        for attempt in range(3):
            try:
                loading_animation(f"Adding {member.username}", duration=1, style='pulse')
                await client(functions.channels.InviteToChannelRequest(group_to_add, [member]))
                added_count += 1
                print_box(f"Added {member.username} ({added_count}/{max_members})", style='single', color='green')
                await asyncio.sleep(15)
                break
            except FloodWaitError as e:
                wait_time = e.seconds + random.uniform(5, 15)
                print_colored(f"Flood wait: Pausing for {wait_time:.1f}s (Attempt {attempt + 1}/3)", 'red')
                await asyncio.sleep(wait_time)
                if attempt == 2:
                    print_colored(f"Max retries for {member.username}, skipping", 'red')
            except Exception as e:
                print_colored(f"Failed to add {member.username}: {e}", 'red')
                await asyncio.sleep(3)
                break

        # Progress bar
        progress = (added_count / max_members) * 100
        bar_width = 30
        filled = int(bar_width * added_count // max_members)
        bar = '█' * filled + '-' * (bar_width - filled)
        print_colored(f"\rProgress: [{bar}] {progress:3.0f}%", 'green')

    print_section_header("Operation Complete")
    print_box(f"Added {added_count} members to {group_to_add.title}", style='double', color='white')

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())