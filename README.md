# AI Coding Agent

A Python-based AI agent powered by Google's Gemini models. This agent is designed to assist with coding tasks by autonomously planning and executing file operations and Python scripts within a specific working directory.

## Features

* **Natural Language Interface:** Accepts user prompts via command-line arguments.
* **Tool Usage:** The agent can perform the following actions within a sandboxed working directory:
    * **List Files:** View file names, sizes, and types (`get_files_info`).
    * **Read Files:** Retrieve the content of files (`get_file_content`).
    * **Write Files:** Create or overwrite files with generated code (`write_file`).
    * **Execute Code:** Run Python scripts and capture their output (`run_python_file`).
* **Safety:** Includes path validation to ensure operations are restricted to the allowed working directory (default: `./calculator`).
* **Gemini Integration:** Utilizes the `google-genai` SDK for function calling and content generation.

## Prerequisites

* Python 3.13 or higher.
* A Google Gemini API Key.

## Installation

1.  **Navigate to the project directory:**
    ```bash
    cd AI-Agent
    ```

2.  **Install dependencies:**
    You can install the requirements defined in `pyproject.toml`:
    ```bash
    pip install .
    ```
    *Alternatively, manually install the required packages:*
    ```bash
    pip install google-genai python-dotenv
    ```

3.  **Environment Setup:**
    Create a `.env` file in the `Agent` directory and add your API key:
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

## Usage

Run the agent from the terminal by passing your prompt as an argument.

**Basic Example:**
```bash
python main.py "Create a python script that calculates the factorial of a number and run it"
```

Verbose Mode: Use the --verbose flag to see detailed logs of tool calls, token usage, and execution results.

```bash
python main.py "List all files in the current directory" --verbose
```
## ⚙️ Configuration

The agent is configured to operate within a specific **working directory** to enforce security and prevent unintentional modification of system files.

### Working Directory

| Setting | Value | Location |
| :--- | :--- | :--- |
| **Default Working Directory** | `./calculator` | `functions/call_function.py` |

The working directory acts as a sandbox, ensuring all file operations are contained within this project's scope.

---

## 🏗️ Architecture

The agent's architecture is modular, separating the main interaction loop from the tool implementations (functions) available to the Large Language Model (LLM).

### Core Components

* **`main.py`**
    * This is the **entry point** of the application.
    * It handles the initialization of the GenAI client and manages the **main interaction loop** with the user/system.

* **`functions/` Directory**
    * This directory contains all the **tool implementations** (functions) that the LLM can call to interact with the environment.

### Available Tools (LLM Functions)

| File Name | Description |
| :--- | :--- |
| `get_files_info.py` | Lists the contents and structure of the directories within the working directory. |
| `get_file_content.py` | Reads and returns the textual content of a specified file. |
| `write_file.py` | Writes or updates content to a specified file within the working directory. |

run_python_file.py: Executes Python files in a subprocess.

call_function.py: Dispatches model requests to the appropriate function.
