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

Configuration
The agent operates within a specific "working directory" to prevent modification of system files.

Default Working Directory: ./calculator

This is currently configured in functions/call_function.py.

Architecture
main.py: The entry point. Initializes the GenAI client and manages the interaction loop.

functions/: Contains the tool implementations available to the LLM.

get_files_info.py: Lists directory contents.

get_file_content.py: Reads file text.

write_file.py: Writes content to the filesystem.

run_python_file.py: Executes Python files in a subprocess.

call_function.py: Dispatches model requests to the appropriate function.
