import os
import sys
import argparse
from functions.call_functions import available_functions, call_function
from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Couldn't read the API KEY")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    client = genai.Client(api_key=api_key)
    for _ in range(20):
        try:
            final_response = generate_content(client, messages)
            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print("Maximum iterations (20) reached")
    sys.exit(1)


def generate_content(
    client,
    messages,
):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if response.usage_metadata is None:
        raise RuntimeError("Could't get Api response")
    if response.candidates is not None:
        for candidate in response.candidates:
            if candidate.content is not None:
                messages.append(candidate.content)
    if response.function_calls is not None:
        function_results = []
        for function_call in response.function_calls:
            function_call_result: types.Content = call_function(function_call)
            if (
                function_call_result.parts is None
                or len(function_call_result.parts) == 0
            ):
                raise Exception(f"Error when calling {function_call}")
            first_item = function_call_result.parts[0]
            if first_item.function_response is None:
                raise Exception("Function response is empty")
            if first_item.function_response.response is None:
                raise Exception("Response in function response is empty")
            function_results.append(first_item)
        function_calls_results = types.Content(role="user", parts=function_results)
        messages.append(function_calls_results)
    if not response.function_calls:
        return response.text


if __name__ == "__main__":
    main()
