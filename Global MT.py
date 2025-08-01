import os
import sys
import platform
import time
import socket
import psutil
import json

# --- Configuration ---
MISC_FOLDER = "Misc"
CONFIG_FILE = os.path.join(MISC_FOLDER, "Config.json")
DEFAULT_COLOR_NAME = "blue"
DEFAULT_USERNAME = "GMT_User"
DEFAULT_LANGUAGE = "en" # Default language: English

# ANSI escape codes for colors
class Colors:
    RESET = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

# Map color names to their ANSI codes
COLOR_MAP = {
    "reset": Colors.RESET,
    "black": Colors.BLACK,
    "red": Colors.RED,
    "green": Colors.GREEN,
    "yellow": Colors.YELLOW,
    "blue": Colors.BLUE,
    "magenta": Colors.MAGENTA,
    "cyan": Colors.CYAN,
    "white": Colors.WHITE,
    "bright_black": Colors.BRIGHT_BLACK,
    "bright_red": Colors.BRIGHT_RED,
    "bright_green": Colors.BRIGHT_GREEN,
    "bright_yellow": Colors.BRIGHT_YELLOW,
    "bright_blue": Colors.BRIGHT_BLUE,
    "bright_magenta": Colors.BRIGHT_MAGENTA,
    "bright_cyan": Colors.BRIGHT_CYAN,
    "bright_white": Colors.BRIGHT_WHITE,
}

# --- Language Data ---
LANGUAGES = {
    "en": { # English
        "commands_available": "Available Commands:",
        "help_cmd": "Show this help message.",
        "echo_cmd": "Repeat your input.",
        "color_cmd": "Change the text color.",
        "color_usage": "Usage: color [color_name]",
        "color_available": "Available colors:",
        "setusername_cmd": "Set your username.",
        "setusername_usage": "Usage: setusername [new_username]",
        "ipinfo_cmd": "Display concise network information for your computer (IPs, MACs).",
        "langset_cmd": "Change the display language.",
        "langset_usage": "Usage: langset [language_code]",
        "langset_available": "Available languages: en (English), es (Español), ja (日本語), zh (中文)",
        "reload_cmd": "Reloads GMT, maintaining the current configuration and displaying the banner.",
        "exit_cmd": "Exit the GMT tool.",
        "clear_cmd": "Clear the console screen.",
        "type_command": "\nType a command and press Enter.",
        "unknown_command": "Unknown command: '{command}'. Type 'help' for available commands.",
        "exiting_gmt": "Exiting GMT. Goodbye!",
        "error_occurred": "An error occurred: {error}",
        "warning_screenshare_start": "WARNING: If you are screen sharing, displaying this information can reveal details about your network to others, which could be used to harm your system.",
        "prompt_screenshare": "Are you currently screen sharing? (yes/no):",
        "screenshare_yes_warning": "It is strongly recommended to stop screen sharing before proceeding. Proceeding anyway...",
        "screenshare_no_proceed": "Proceeding with IP information display.",
        "invalid_input_proceed": "Invalid input. Proceeding with IP information display anyway.",
        "network_info_title": "--- Network Information ---",
        "hostname": "Hostname: {hostname}",
        "interface": "Interface: {interface}",
        "ipv4": "  IPv4: {ipv4}",
        "mac": "  MAC:  {mac}",
        "no_active_interfaces": "No active network interfaces with IPv4 or MAC found (excluding localhost).",
        "error_retrieving_network": "Error retrieving network information: {error}",
        "network_info_end": "---------------------------\n",
        "reloading_gmt": "Reloading GMT...",
        "gmt_reloaded": "GMT Reloaded!",
        "color_set_to": "Color set to {color_name}.",
        "invalid_color": "Invalid color: '{color_name}'.",
        "reset_color_info": "The 'reset' color is for internal use and cannot be directly set.",
        "username_set_to": "Username set to: {username}",
        "username_empty": "Username cannot be empty.",
        "current_username": "Current username: {username}",
        "invalid_language": "Invalid language code: '{lang_code}'.",
        "language_set_to": "Language set to {lang_name}.",
        "warning_config_save": "Warning: Could not save configuration: {error}",
        "warning_config_load_corrupted": "Warning: Corrupted configuration file. Resetting to defaults.",
        "warning_config_load_error": "Warning: Error loading configuration: {error}. Using defaults.",
        "warning_invalid_saved_color": "Warning: Saved color '{color}' is invalid. Using default '{default_color}'.",
    },
    "es": { # Spanish
        "commands_available": "Comandos Disponibles:",
        "help_cmd": "Mostrar este mensaje de ayuda.",
        "echo_cmd": "Repetir tu entrada.",
        "color_cmd": "Cambiar el color del texto.",
        "color_usage": "Uso: color [nombre_del_color]",
        "color_available": "Colores disponibles:",
        "setusername_cmd": "Establecer tu nombre de usuario.",
        "setusername_usage": "Uso: setusername [nuevo_nombre_de_usuario]",
        "ipinfo_cmd": "Mostrar información concisa de red de tu computadora (IPs, MACs).",
        "langset_cmd": "Cambiar el idioma de visualización.",
        "langset_usage": "Uso: langset [código_de_idioma]",
        "langset_available": "Idiomas disponibles: en (English), es (Español), ja (日本語), zh (中文)",
        "reload_cmd": "Recarga GMT, manteniendo la configuración actual y mostrando el banner.",
        "exit_cmd": "Salir de la herramienta GMT.",
        "clear_cmd": "Limpiar la pantalla de la consola.",
        "type_command": "\nEscribe un comando y presiona Enter.",
        "unknown_command": "Comando desconocido: '{command}'. Escribe 'help' para ver los comandos disponibles.",
        "exiting_gmt": "Saliendo de GMT. ¡Adiós!",
        "error_occurred": "Ocurrió un error: {error}",
        "warning_screenshare_start": "ADVERTENCIA: Si estás compartiendo la pantalla, mostrar esta información puede revelar detalles de tu red a otros, lo que podría usarse para dañar tu sistema.",
        "prompt_screenshare": "¿Estás compartiendo la pantalla actualmente? (sí/no):",
        "screenshare_yes_warning": "Se recomienda encarecidamente dejar de compartir la pantalla antes de continuar. Procediendo de todos modos...",
        "screenshare_no_proceed": "Procediendo con la visualización de la información de IP.",
        "invalid_input_proceed": "Entrada inválida. Procediendo con la visualización de la información de IP de todos modos.",
        "network_info_title": "--- Información de Red ---",
        "hostname": "Nombre de Host: {hostname}",
        "interface": "Interfaz: {interface}",
        "ipv4": "  IPv4: {ipv4}",
        "mac": "  MAC:  {mac}",
        "no_active_interfaces": "No se encontraron interfaces de red activas con IPv4 o MAC (excluyendo localhost).",
        "error_retrieving_network": "Error al recuperar la información de red: {error}",
        "network_info_end": "---------------------------\n",
        "reloading_gmt": "Recargando GMT...",
        "gmt_reloaded": "¡GMT Recargado!",
        "color_set_to": "Color establecido a {color_name}.",
        "invalid_color": "Color inválido: '{color_name}'.",
        "reset_color_info": "El color 'reset' es para uso interno y no se puede establecer directamente.",
        "username_set_to": "Nombre de usuario establecido a: {username}",
        "username_empty": "El nombre de usuario no puede estar vacío.",
        "current_username": "Nombre de usuario actual: {username}",
        "invalid_language": "Código de idioma inválido: '{lang_code}'.",
        "language_set_to": "Idioma establecido a {lang_name}.",
        "warning_config_save": "Advertencia: No se pudo guardar la configuración: {error}",
        "warning_config_load_corrupted": "Advertencia: Archivo de configuración corrupto. Restaurando a valores predeterminados.",
        "warning_config_load_error": "Advertencia: Error al cargar la configuración: {error}. Usando valores predeterminados.",
        "warning_invalid_saved_color": "Advertencia: El color guardado '{color}' no es válido. Usando el predeterminado '{default_color}'.",
    },
    "ja": { # Japanese
        "commands_available": "利用可能なコマンド:",
        "help_cmd": "このヘルプメッセージを表示します。",
        "echo_cmd": "入力内容を繰り返します。",
        "color_cmd": "テキストの色を変更します。",
        "color_usage": "使用法: color [色の名前]",
        "color_available": "利用可能な色:",
        "setusername_cmd": "ユーザー名を設定します。",
        "setusername_usage": "使用法: setusername [新しいユーザー名]",
        "ipinfo_cmd": "コンピュータのネットワーク情報（IP、MACなど）を簡潔に表示します。",
        "langset_cmd": "表示言語を変更します。",
        "langset_usage": "使用法: langset [言語コード]",
        "langset_available": "利用可能な言語: en (English), es (Español), ja (日本語), zh (中文)",
        "reload_cmd": "GMTをリロードし、現在の設定を維持してバナーを表示します。",
        "exit_cmd": "GMTツールを終了します。",
        "clear_cmd": "コンソール画面をクリアします。",
        "type_command": "\nコマンドを入力してEnterを押してください。",
        "unknown_command": "不明なコマンド: '{command}'。利用可能なコマンドについては'help'と入力してください。",
        "exiting_gmt": "GMTを終了します。さようなら！",
        "error_occurred": "エラーが発生しました: {error}",
        "warning_screenshare_start": "警告: 画面共有を行っている場合、この情報を表示すると、ネットワークの詳細が他者に漏洩し、システムに危害が加えられる可能性があります。",
        "prompt_screenshare": "現在画面を共有していますか？（はい/いいえ）:",
        "screenshare_yes_warning": "続行する前に画面共有を停止することを強くお勧めします。それでも続行します...",
        "screenshare_no_proceed": "IP情報の表示に進みます。",
        "invalid_input_proceed": "無効な入力です。IP情報の表示に進みます。",
        "network_info_title": "--- ネットワーク情報 ---",
        "hostname": "ホスト名: {hostname}",
        "interface": "インターフェース: {interface}",
        "ipv4": "  IPv4: {ipv4}",
        "mac": "  MAC:  {mac}",
        "no_active_interfaces": "IPv4またはMACを持つアクティブなネットワークインターフェースが見つかりません（localhostを除く）。",
        "error_retrieving_network": "ネットワーク情報の取得中にエラーが発生しました: {error}",
        "network_info_end": "---------------------------\n",
        "reloading_gmt": "GMTをリロード中...",
        "gmt_reloaded": "GMTがリロードされました！",
        "color_set_to": "色を{color_name}に設定しました。",
        "invalid_color": "無効な色: '{color_name}'。",
        "reset_color_info": "'reset'色は内部使用のため、直接設定することはできません。",
        "username_set_to": "ユーザー名が{username}に設定されました。",
        "username_empty": "ユーザー名を空にすることはできません。",
        "current_username": "現在のユーザー名: {username}",
        "invalid_language": "無効な言語コード: '{lang_code}'。",
        "language_set_to": "言語を{lang_name}に設定しました。",
        "warning_config_save": "警告: 設定を保存できませんでした: {error}",
        "warning_config_load_corrupted": "警告: 設定ファイルが破損しています。デフォルトにリセットします。",
        "warning_config_load_error": "警告: 設定の読み込み中にエラーが発生しました: {error}。デフォルトを使用します。",
        "warning_invalid_saved_color": "警告: 保存された色 '{color}' は無効です。デフォルトの '{default_color}' を使用します。",
    },
    "zh": { # Chinese (Simplified)
        "commands_available": "可用命令:",
        "help_cmd": "显示此帮助信息。",
        "echo_cmd": "重复您的输入。",
        "color_cmd": "更改文本颜色。",
        "color_usage": "用法: color [颜色名称]",
        "color_available": "可用颜色:",
        "setusername_cmd": "设置您的用户名。",
        "setusername_usage": "用法: setusername [新用户名]",
        "ipinfo_cmd": "显示您电脑的简洁网络信息（IPs, MACs）。",
        "langset_cmd": "更改显示语言。",
        "langset_usage": "用法: langset [语言代码]",
        "langset_available": "可用语言: en (English), es (Español), ja (日本語), zh (中文)",
        "reload_cmd": "重新加载GMT，保持当前配置并显示横幅。",
        "exit_cmd": "退出GMT工具。",
        "clear_cmd": "清空控制台屏幕。",
        "type_command": "\n输入命令并按Enter。",
        "unknown_command": "未知命令: '{command}'。输入 'help' 查看可用命令。",
        "exiting_gmt": "正在退出GMT。再见！",
        "error_occurred": "发生错误: {error}",
        "warning_screenshare_start": "警告: 如果您正在进行屏幕共享，显示此信息可能会向他人泄露您的网络详细信息，这可能被用于危害您的系统。",
        "prompt_screenshare": "您当前正在进行屏幕共享吗？(是/否):",
        "screenshare_yes_warning": "强烈建议在继续之前停止屏幕共享。仍然继续...",
        "screenshare_no_proceed": "继续显示IP信息。",
        "invalid_input_proceed": "无效输入。仍然继续显示IP信息。",
        "network_info_title": "--- 网络信息 ---",
        "hostname": "主机名: {hostname}",
        "interface": "接口: {interface}",
        "ipv4": "  IPv4: {ipv4}",
        "mac": "  MAC:  {mac}",
        "no_active_interfaces": "未找到具有IPv4或MAC的活动网络接口（不包括localhost）。",
        "error_retrieving_network": "检索网络信息时出错: {error}",
        "network_info_end": "---------------------------\n",
        "reloading_gmt": "正在重新加载GMT...",
        "gmt_reloaded": "GMT已重新加载！",
        "color_set_to": "颜色设置为{color_name}。",
        "invalid_color": "无效颜色: '{color_name}'。",
        "reset_color_info": "'reset'颜色用于内部用途，无法直接设置。",
        "username_set_to": "用户名设置为: {username}",
        "username_empty": "用户名不能为空。",
        "current_username": "当前用户名: {username}",
        "invalid_language": "无效的语言代码: '{lang_code}'。",
        "language_set_to": "语言设置为{lang_name}。",
        "warning_config_save": "警告: 无法保存配置: {error}",
        "warning_config_load_corrupted": "警告: 配置文件损坏。重置为默认值。",
        "warning_config_load_error": "警告: 加载配置时出错: {error}。使用默认值。",
        "warning_invalid_saved_color": "警告: 保存的颜色 '{color}' 无效。使用默认 '{default_color}'。",
    }
}
# Map language codes to display names (for the langset_available message)
LANGUAGE_NAMES = {
    "en": "English",
    "es": "Español",
    "ja": "日本語",
    "zh": "中文",
}


# Global variables for current configuration
current_color_code = Colors.BLUE
current_color_name = DEFAULT_COLOR_NAME
current_username = DEFAULT_USERNAME
current_lang_code = DEFAULT_LANGUAGE

# --- Translation Function ---
def get_translation(key):
    """Retrieves the translated string for a given key from the current language dictionary."""
    return LANGUAGES[current_lang_code].get(key, f"MISSING_TRANSLATION_FOR_{key}")


def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def set_terminal_color(color_code):
    """Sets the terminal text color using ANSI escape codes and updates current_color_code."""
    global current_color_code
    sys.stdout.write(color_code)
    sys.stdout.flush()
    current_color_code = color_code

def save_config():
    """Saves the current configuration (color, username, language) to a JSON file."""
    try:
        os.makedirs(MISC_FOLDER, exist_ok=True)
        config_data = {
            "last_color": current_color_name,
            "username": current_username,
            "last_language": current_lang_code
        }
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4)
    except Exception as e:
        # Use get_translation here too, but be careful if it fails to load
        print(f"{Colors.RED}{get_translation('warning_config_save').format(error=e)}{Colors.RESET}")

def load_config():
    """Loads the last saved configuration from a JSON file."""
    global current_color_code, current_color_name, current_username, current_lang_code
    
    # Initialize translation function to default English first, in case loading fails
    # This ensures error messages have some language even if the config is bad
    _temp_translate = LANGUAGES[DEFAULT_LANGUAGE].get 

    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)

                # Load color
                saved_color_name = config.get("last_color", DEFAULT_COLOR_NAME)
                if saved_color_name.lower() in COLOR_MAP:
                    current_color_name = saved_color_name.lower()
                    current_color_code = COLOR_MAP[current_color_name]
                else:
                    print(f"{Colors.YELLOW}{_temp_translate('warning_invalid_saved_color').format(color=saved_color_name, default_color=DEFAULT_COLOR_NAME)}{Colors.RESET}")
                    current_color_name = DEFAULT_COLOR_NAME
                    current_color_code = COLOR_MAP[DEFAULT_COLOR_NAME]
                    save_config()

                # Load username
                current_username = config.get("username", DEFAULT_USERNAME)

                # Load language
                saved_lang_code = config.get("last_language", DEFAULT_LANGUAGE)
                if saved_lang_code.lower() in LANGUAGES:
                    current_lang_code = saved_lang_code.lower()
                else:
                    print(f"{Colors.YELLOW}{_temp_translate('warning_invalid_language').format(lang_code=saved_lang_code)}{Colors.RESET}")
                    current_lang_code = DEFAULT_LANGUAGE
                    save_config()

        else:
            # If config file doesn't exist, use defaults and save them
            current_color_name = DEFAULT_COLOR_NAME
            current_color_code = COLOR_MAP[DEFAULT_COLOR_NAME]
            current_username = DEFAULT_USERNAME
            current_lang_code = DEFAULT_LANGUAGE
            save_config()

    except json.JSONDecodeError:
        print(f"{Colors.RED}{_temp_translate('warning_config_load_corrupted')}{Colors.RESET}")
        current_color_name = DEFAULT_COLOR_NAME
        current_color_code = COLOR_MAP[DEFAULT_COLOR_NAME]
        current_username = DEFAULT_USERNAME
        current_lang_code = DEFAULT_LANGUAGE
        save_config()
    except Exception as e:
        print(f"{Colors.RED}{_temp_translate('warning_config_load_error').format(error=e)}{Colors.RESET}")
        current_color_name = DEFAULT_COLOR_NAME
        current_color_code = COLOR_MAP[DEFAULT_COLOR_NAME]
        current_username = DEFAULT_USERNAME
        current_lang_code = DEFAULT_LANGUAGE
        save_config()
    finally:
        # Crucially, set the global _ function *after* loading is complete
        # to ensure it reflects the newly loaded or defaulted language.
        pass # The get_translation function already uses current_lang_code dynamically

def display_banner():
    """Displays the GMT ASCII art banner."""
    clear_screen()
    set_terminal_color(current_color_code)
    print(r"""
 ██████╗ ██╗       ██████╗ ██████╗  █████╗ ██╗         ███╗   ███╗████████╗
██╔════╝ ██║      ██╔═══██╗██╔══██╗██╔══██╗██║         ████╗ ████║╚══██╔══╝
██║ ███╗██║      ██║   ██║██████╔╝███████║██║         ██╔████╔██║  ██║
██║   ██║██║      ██║   ██║██╔══██╗██╔══██║██║         ██║╚██╔╝██║  ██║
╚██████╔╝███████╗╚██████╔╝██████╔╝██║  ██║███████╗    ██║ ╚═╝ ██║  ██║
 ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝

 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                              Version - 1.0.0
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""")

def help_command():
    """Displays available commands in the current language."""
    # Now using get_translation function instead of direct _()
    print(f"\n{get_translation('commands_available')}")
    print(f"  help        - {get_translation('help_cmd')}")
    print(f"  echo        - {get_translation('echo_cmd')}")
    print(f"  color       - {get_translation('color_cmd')} {get_translation('color_usage')}")
    print(f"                {get_translation('color_available')} " + ", ".join([name for name in COLOR_MAP.keys() if name != "reset"]))
    print(f"  setusername - {get_translation('setusername_cmd')} {get_translation('setusername_usage')}")
    print(f"  ipinfo      - {get_translation('ipinfo_cmd')}")
    print(f"  langset     - {get_translation('langset_cmd')} {get_translation('langset_usage')}")
    print(f"                {get_translation('langset_available')}")
    print(f"  reload      - {get_translation('reload_cmd')}")
    print(f"  exit        - {get_translation('exit_cmd')}")
    print(f"  clear       - {get_translation('clear_cmd')}")
    print(get_translation('type_command'))

def echo_command(args):
    """Echoes the provided arguments."""
    print(" ".join(args))

def set_color_command(color_name_input):
    """Sets the terminal text color."""
    global current_color_name
    
    selected_color_code = COLOR_MAP.get(color_name_input.lower())
    if selected_color_code and color_name_input.lower() != "reset":
        set_terminal_color(selected_color_code)
        current_color_name = color_name_input.lower()
        save_config() # Save the new color
        print(get_translation('color_set_to').format(color_name=current_color_name))
    elif color_name_input.lower() == "reset":
        print(get_translation('reset_color_info'))
    else:
        print(get_translation('invalid_color').format(color_name=color_name_input))
        print(get_translation('color_available') + " " + ", ".join([name for name in COLOR_MAP.keys() if name != "reset"]))

def set_username_command(args):
    """Sets the username."""
    global current_username
    if args:
        new_username = " ".join(args).strip()
        if new_username:
            current_username = new_username
            save_config() # Save the new username
            print(get_translation('username_set_to').format(username=current_username))
        else:
            print(get_translation('username_empty'))
    else:
        print(get_translation('setusername_usage'))
        print(get_translation('current_username').format(username=current_username))

def set_language_command(args):
    """Sets the display language."""
    global current_lang_code
    if args:
        lang_code = args[0].lower()
        if lang_code in LANGUAGES:
            current_lang_code = lang_code
            save_config() # Save the new language
            print(get_translation('language_set_to').format(lang_name=LANGUAGE_NAMES.get(lang_code, lang_code.upper())))
            # After changing language, it's good practice to re-display the help
            help_command()
        else:
            print(get_translation('invalid_language').format(lang_code=lang_code))
            print(get_translation('langset_available'))
    else:
        print(get_translation('langset_usage'))
        print(get_translation('langset_available'))
        print(f"Current language: {LANGUAGE_NAMES.get(current_lang_code, current_lang_code.upper())}")


def ipinfo_command():
    """Displays concise network information for the local machine with a screen sharing warning."""
    print(f"\n{Colors.BRIGHT_YELLOW}{get_translation('warning_screenshare_start')}{Colors.RESET}")
    sys.stdout.write(Colors.WHITE)
    sys.stdout.flush()
    response = input(f"{get_translation('prompt_screenshare')} ").strip().lower()
    set_terminal_color(current_color_code)

    if response in ['yes', 'si', 'はい', '是']:
        print(f"{Colors.BRIGHT_RED}{get_translation('screenshare_yes_warning')}{Colors.RESET}")
        time.sleep(2)
    elif response in ['no', 'いいえ', '否']: # 'no' is the same in English and Spanish
        print(get_translation('screenshare_no_proceed'))
    else:
        print(f"{Colors.BRIGHT_YELLOW}{get_translation('invalid_input_proceed')}{Colors.RESET}")
        time.sleep(1)

    set_terminal_color(current_color_code)

    print(get_translation('network_info_title'))
    try:
        hostname = socket.gethostname()
        print(get_translation('hostname').format(hostname=hostname))

        addresses = psutil.net_if_addrs()
        found_interface = False
        for interface_name, interface_addresses in addresses.items():
            ipv4_address = "N/A"
            mac_address = "N/A"
            for addr in interface_addresses:
                if addr.family == socket.AF_INET and not addr.address.startswith('127.'):
                    ipv4_address = addr.address
                elif addr.family == psutil.AF_LINK:
                    mac_address = addr.address

            if ipv4_address != "N/A" or mac_address != "N/A":
                print(get_translation('interface').format(interface=interface_name))
                print(get_translation('ipv4').format(ipv4=ipv4_address))
                print(get_translation('mac').format(mac=mac_address))
                found_interface = True
        
        if not found_interface:
            print(get_translation('no_active_interfaces'))

    except Exception as e:
        print(get_translation('error_retrieving_network').format(error=e))
    print(get_translation('network_info_end'))


def reload_gmt():
    """Reloads GMT, maintaining the current configuration and redisplaying the banner."""
    print(get_translation('reloading_gmt'))
    time.sleep(0.5)
    display_banner()
    print(get_translation('gmt_reloaded'))


def gmt_shell():
    """The main loop for the GMT shell."""
    # --- Load configuration on startup ---
    load_config()
    set_terminal_color(current_color_code)
    display_banner()

    while True:
        try:
            command_line = input(f"{current_color_code}{current_username}: $> {Colors.RESET}").strip()
            
            set_terminal_color(current_color_code) 

            if not command_line:
                continue

            parts = command_line.split()
            command = parts[0].lower()
            args = parts[1:]

            if command == "help":
                help_command()
            elif command == "echo":
                echo_command(args)
            elif command == "color":
                if args:
                    set_color_command(args[0])
                else:
                    print(get_translation('color_usage'))
                    print(get_translation('color_available') + " " + ", ".join([name for name in COLOR_MAP.keys() if name != "reset"]))
            elif command == "setusername":
                set_username_command(args)
            elif command == "langset":
                set_language_command(args)
            elif command == "ipinfo":
                ipinfo_command()
            elif command == "reload":
                reload_gmt()
            elif command == "clear":
                set_terminal_color(current_color_code)
                clear_screen()
                display_banner()
            elif command == "exit":
                set_terminal_color(Colors.RESET)
                print(get_translation('exiting_gmt'))
                break
            else:
                # Use get_translation here, which caused the original error
                print(get_translation('unknown_command').format(command=command))
        except KeyboardInterrupt:
            set_terminal_color(Colors.RESET)
            print(f"\n{get_translation('exiting_gmt')}")
            break
        except Exception as e:
            set_terminal_color(Colors.RESET)
            # Use get_translation here too
            print(get_translation('error_occurred').format(error=e))

if __name__ == "__main__":
    gmt_shell()
