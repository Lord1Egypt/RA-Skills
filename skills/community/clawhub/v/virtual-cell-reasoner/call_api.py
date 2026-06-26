#!/usr/bin/env python3
"""Simple client for the AAIB /chat API."""
import argparse
import requests

SERVER_URL = "https://noninstructive-famously-leigh.ngrok-free.dev"


def do_chat(url, message, max_new_tokens=512, temperature=0.7):
    resp = requests.post(
        f"{url}/chat",
        json={"message": message, "max_new_tokens": max_new_tokens, "temperature": temperature},
    )
    resp.raise_for_status()
    return resp.json()["response"]


def main():
    parser = argparse.ArgumentParser(description="Query the AAIB /chat API")
    parser.add_argument("prompt", nargs="?", help="User prompt (omit for interactive mode)")
    parser.add_argument("--url", default=SERVER_URL, help="Server base URL")
    parser.add_argument("--max-tokens", type=int, default=2048)
    parser.add_argument("--temperature", type=float, default=0.7)
    args = parser.parse_args()

    if args.prompt:
        print(do_chat(args.url, args.prompt, args.max_tokens, args.temperature))
    else:
        print("Interactive mode (Ctrl+C to quit)")
        while True:
            try:
                user_input = input("\nYou: ").strip()
            except (KeyboardInterrupt, EOFError):
                break
            if not user_input:
                continue
            print("Model:", do_chat(args.url, user_input, args.max_tokens, args.temperature))


if __name__ == "__main__":
    main()
