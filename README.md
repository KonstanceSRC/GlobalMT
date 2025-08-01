# Global Multi-Tool (GMT)

![GMT Screenshot](assets/standard.gif)

GMT (Global Multi-Tool) is a versatile and user-friendly command-line utility designed to offer quick access to essential system information and personalized console interactions. Built with Python, GMT allows you to customize your terminal experience, get a concise overview of your network, and more, all through a simple, interactive command-line interface.

## 🚀 Getting Started

To get started with GMT, follow these simple steps:

1.  **Download:** Clone this repository or download the `main.py` and `install_gmt.bat` files to your local machine.
2.  **Install Dependencies:**
    * Navigate to the directory where you saved the files using your command prompt or terminal.
    * Run the installer script:
        ```bash
        install_gmt.bat
        ```
        This script will automatically install any necessary Python packages (like `psutil`) for the tool to function correctly.
3.  **Run GMT:**
    * Once dependencies are installed, you can start the GMT tool:
        ```bash
        python main.py
        ```

## ✨ Features & Commands

GMT provides a suite of commands to enhance your command-line experience:

* **`help`**
    * **Description:** Displays a list of all available commands and their basic usage.
    * **Usage:** `help`

* **`echo [text]`**
    * **Description:** Repeats any text you type after the command. Useful for testing or simple messages.
    * **Usage:** `echo Hello World!`

* **`color [color_name]`**
    * **Description:** Changes the text color of the GMT interface. Your chosen color will persist across sessions!
    * **Usage:** `color red`
    * **Available Colors:** `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white` (and their `bright_` variants like `bright_red`).

* **`setusername [new_username]`**
    * **Description:** Sets a personalized username that will appear in your command prompt (`YourUsername: $>`). This username will be saved and loaded for future sessions.
    * **Usage:** `setusername MyAwesomeUser`

* **`langset [language_code]`**
    * **Description:** Changes the display language of the GMT tool's messages. Your chosen language will persist across sessions.
    * **Usage:** `langset es`
    * **Available Languages:**
        * `en` (English)
        * `es` (Español)
        * `ja` (日本語)
        * `zh` (中文 - Simplified)

* **`ipinfo`**
    * **Description:** Displays concise network information about your local computer, including hostname, IPv4 addresses, and MAC addresses for active interfaces.
    * **Important Warning:** Before displaying, this command will ask if you are screen sharing, as this information can be sensitive if publicly visible.
    * **Usage:** `ipinfo`

* **`reload`**
    * **Description:** Clears the console screen and reloads the GMT banner and prompt, maintaining your current color and username settings.
    * **Usage:** `reload`

* **`clear`**
    * **Description:** Clears all text from the console screen, leaving only the GMT banner and prompt.
    * **Usage:** `clear`

* **`exit`**
    * **Description:** Closes the GMT application.
    * **Usage:** `exit`

## 💡 Why is GMT Useful?

* **Personalization:** Tailor your command-line environment with custom colors and usernames.
* **Quick Network Overview:** Instantly retrieve local IP and MAC addresses without navigating through system settings.
* **Multilingual Support:** Makes the tool accessible and user-friendly for individuals who prefer different languages.
* **Session Persistence:** Your preferred color, username, and language are saved, so you don't have to reconfigure them every time you launch GMT.
* **Educational:** Provides a simple framework for learning basic Python scripting, command-line interface design, and handling system interactions.
* **Extensible:** The modular design allows for easy addition of new commands and features in the future.

## 🤝 Contributing

This project is a simple multi-tool and open for exploration and learning. If you have ideas for new commands or improvements, feel free to fork the repository and experiment!

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
