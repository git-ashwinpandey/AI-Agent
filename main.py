import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
MAX_ITERATIONS = 20
def main():
    arg_len = len(sys.argv)
    is_verbose = arg_len >= 3 and sys.argv[2] == '--verbose'

    if arg_len == 1:
        print("No prompt entered")
        sys.exit(1)
        
    user_prompt = sys.argv[1]
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """

    # Include all function declarations
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    # Initialize messages with the user prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    # Print verbose info before the loop
    if is_verbose:
        print(f"User prompt: {user_prompt}")
    
    MAX_ITERATIONS = 20
    
    for i in range(MAX_ITERATIONS):
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001', 
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
            )
        except Exception as e:
            print(f"Error during API call: {e}")
            break

        # 1. Check model's candidates and add to messages (response/tool_call)
        if not response.candidates:
            print("Error: Model returned no candidates.")
            break
        
        # Candidate's content is the model's 'response' (which might contain tool calls)
        model_content = response.candidates[0].content
        messages.append(model_content)

        # Print verbose token info for the current turn (model response)
        if is_verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        # 2. Handle function calls
        # Check for function calls FIRST. This prevents the SDK from checking .text
        # on a function call response, which causes the "Warning: non-text parts" error.
        if response.function_calls:
            function_calls = response.function_calls
            function_responses = []
            
            for call in function_calls:
                # Execute the function call
                function_call_result = call_function(call, verbose=is_verbose)
                
                # Validation and collecting the tool's response part
                if (
                    function_call_result.parts
                    and function_call_result.parts[0].function_response
                    and function_call_result.parts[0].function_response.response
                ):
                    tool_response_part = function_call_result.parts[0]
                    function_responses.append(tool_response_part)
                    
                    # Print result if verbose is set
                    if is_verbose:
                        response_dict = tool_response_part.function_response.response
                        # Extract and print the string result from the dictionary value
                        key = "result" if "result" in response_dict else "error"
                        print(f"-> {response_dict[key]}")
                else:
                    raise RuntimeError(f"Unexpected function call response structure: {function_call_result}")
            
            # Append tool responses to messages
            tool_content = types.Content(role="tool", parts=function_responses)
            messages.append(tool_content)
        
        # 3. Check for final text response (termination condition)
        # Only check .text if there were no function calls
        elif response.text:
            print("Final response:")
            print(response.text)
            break

        # 4. Check max iterations
        if i == MAX_ITERATIONS - 1:
            print("Warning: Max iterations reached. Breaking loop.")
            break

if __name__ == "__main__":
    main()