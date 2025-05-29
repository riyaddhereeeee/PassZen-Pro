import secrets
import string
import shutil
import sys
import time
from colorama import Fore, Style, init
import os

init(autoreset=True)

SPINNER = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
SPINNER_COLOR = Fore.CYAN

def animate_loading(duration=1.5):
    start_time = time.time()
    i = 0
    while time.time() - start_time < duration:
        sys.stdout.write(f'\r{SPINNER_COLOR}{SPINNER[i % len(SPINNER)]} Generating...')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write('\r' + ' ' * 30 + '\r')

def generate_advanced_password(length, upper=True, lower=True, digits=True, symbols=True, custom="", avoid_ambiguous=True):
    base_chars = ""
    if lower:
        base_chars += string.ascii_lowercase
    if upper:
        base_chars += string.ascii_uppercase
    if digits:
        base_chars += string.digits
    if symbols:
        base_chars += "!@#$%^&*()-_=+[]{}<>?/|"
    base_chars += custom

    if avoid_ambiguous:
        base_chars = base_chars.translate(str.maketrans('', '', 'Il1O0'))

    if not base_chars:
        return None

    password = []

    if upper: password.append(secrets.choice(string.ascii_uppercase))
    if lower: password.append(secrets.choice(string.ascii_lowercase))
    if digits: password.append(secrets.choice(string.digits))
    if symbols: password.append(secrets.choice("!@#$%^&*()-_=+[]{}<>?/|"))
    if custom: password.append(secrets.choice(custom))

    while len(password) < length:
        password.append(secrets.choice(base_chars))

    secrets.SystemRandom().shuffle(password)
    return ''.join(password)

def banner():
    term_width = shutil.get_terminal_size().columns
    title = "Pass Zen Pro"
    version = "v1.0.0"
    developer = "Developed by @ Riyad"
    benefits = "Secure | Fast | Customizable"
    min_width = 20
    max_width = 60
    
    banner_width = min(max(term_width - 2, min_width), max_width)
    
    title_padding = (banner_width - len(title)) // 2
    version_padding = (banner_width - len(version)) // 2
    developer_padding = (banner_width - len(developer)) // 2
    benefits_padding = (banner_width - len(benefits)) // 2
    
    border_char = "-"
    border = border_char * banner_width
    top_border = f"{Fore.CYAN}{Style.BRIGHT}{border}"
    bottom_border = f"{Fore.CYAN}{Style.BRIGHT}{border}"
    
    title_line = f"{Fore.CYAN}{Style.BRIGHT}|{' ' * title_padding}{title}{' ' * (banner_width - len(title) - title_padding)}|"
    version_line = f"{Fore.CYAN}{Style.BRIGHT}|{' ' * version_padding}{version}{' ' * (banner_width - len(version) - version_padding)}|"
    developer_line = f"{Fore.CYAN}{Style.BRIGHT}|{' ' * developer_padding}{developer}{' ' * (banner_width - len(developer) - developer_padding)}|"
    benefits_line = f"{Fore.CYAN}{Style.BRIGHT}|{' ' * benefits_padding}{benefits}{' ' * (banner_width - len(benefits) - benefits_padding)}|"
    
    print("\n")
    print(top_border)
    print(title_line)
    print(version_line)
    print(developer_line)
    print(benefits_line)
    print(bottom_border)
    print("\n")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    banner()
    
    # Language selection with gaps between question and options, and between "2 English" and "Enter 1 or 2:"
    print(Fore.MAGENTA + "Which language would you like to use?")
    print("\n" * 2)  # Adds two blank lines for spacing
    print(Fore.MAGENTA + "1 Bangla")
    print(Fore.MAGENTA + "2 English")  # No gap between "1 Bangla" and "2 English"
    print("\n" * 2)  # Adds two blank lines for spacing
    print(Fore.MAGENTA + "Enter 1 or 2: ")
    language = input().strip()
    if language not in ['1', '2']:
        print(Fore.RED + "Invalid choice. Defaulting to English.")
        language = '2'
    
    # Clear screen after language selection
    clear_screen()
    banner()

    try:
        if language == '1':
            # Bangla prompts
            length_prompt = "পাসওয়ার্ডের দৈর্ঘ্য কত হবে (৮-৫০)? [১২]: "
            count_prompt = "কয়টি পাসওয়ার্ড তৈরি করতে চান? [১-১০]: "
            upper_prompt = "বড় হাতের অক্ষর অন্তর্ভুক্ত করবেন? (Y/N): "
            lower_prompt = "ছোট হাতের অক্ষর অন্তর্ভুক্ত করবেন? (Y/N): "
            digits_prompt = "সংখ্যা অন্তর্ভুক্ত করবেন? (Y/N): "
            symbols_prompt = "চিহ্ন (সিম্বল) অন্তর্ভুক্ত করবেন? (Y/N): "
            custom_prompt = "অতিরিক্ত কাস্টম অক্ষর (ঐচ্ছিক): "
            ambiguous_prompt = "বিভ্রান্তিকর অক্ষর (0/O, l/1) এড়াতে চান? (Y/N): "
            error_no_chars = "আপনাকে অন্তত একটি অক্ষরের ধরন নির্বাচন করতে হবে।"
            error_general = "ত্রুটি: {}"
            thank_you_message = "ধন্যবাদ! আপনার পাসওয়ার্ড খুবই শক্তিশালী এবং নিরাপদ এখন কোন অপেশাদার হ্যাকার আপনার একাউন্ট হ্যাক করতে পারবে না"
        else:
            # English prompts
            length_prompt = "How long should the password be (8–50)? [12]: "
            count_prompt = "How many passwords would you like to generate? [1–10]: "
            upper_prompt = "Include uppercase letters? (Y/N): "
            lower_prompt = "Include lowercase letters? (Y/N): "
            digits_prompt = "Include numbers? (Y/N): "
            symbols_prompt = "Include symbols? (Y/N): "
            custom_prompt = "Add any custom characters (optional): "
            ambiguous_prompt = "Avoid ambiguous characters (0/O, l/1)? (Y/N): "
            error_no_chars = "You must select at least one character type."
            error_general = "Error: {}"
            thank_you_message = "Thank you! Your password is very strong and secure Now Noob Hacker's can't hack Your account."

        # Collect input with automatic clearing
        clear_screen()
        banner()
        length = int(input(Fore.MAGENTA + length_prompt) or "12")
        length = min(max(length, 8), 50)

        clear_screen()
        banner()
        count = int(input(Fore.MAGENTA + count_prompt) or "1")
        count = min(max(count, 1), 10)

        clear_screen()
        banner()
        upper = input(Fore.MAGENTA + upper_prompt).strip().lower() != 'n'

        clear_screen()
        banner()
        lower = input(Fore.MAGENTA + lower_prompt).strip().lower() != 'n'

        clear_screen()
        banner()
        digits = input(Fore.MAGENTA + digits_prompt).strip().lower() != 'n'

        clear_screen()
        banner()
        symbols = input(Fore.MAGENTA + symbols_prompt).strip().lower() != 'n'

        clear_screen()
        banner()
        custom = input(Fore.MAGENTA + custom_prompt)

        clear_screen()
        banner()
        avoid_ambiguous = input(Fore.MAGENTA + ambiguous_prompt).strip().lower() != 'n'

        # Clear the screen after all inputs
        clear_screen()
        banner()

        if not any([upper, lower, digits, symbols, custom]):
            print(Fore.RED + error_no_chars)
            return

        animate_loading()

        for _ in range(count):
            pw = generate_advanced_password(length, upper, lower, digits, symbols, custom, avoid_ambiguous)
            if not pw:
                print(Fore.RED + "Error generating password.")
                return
            print(Fore.GREEN + pw)

        # Add gap before thank you message
        print("\n" * 2)  # Adds two blank lines for spacing

        # Display thank you message
        print(Fore.CYAN + thank_you_message)

    except KeyboardInterrupt:
        # Clear screen on interrupt
        clear_screen()
        print("\n" + Fore.RED + "Canceled.")
    except Exception as e:
        print(Fore.RED + error_general.format(e))

if __name__ == "__main__":
    main()