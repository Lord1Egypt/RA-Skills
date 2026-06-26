#!/usr/bin/env python3
import sys
import subprocess
import argparse

def run_osascript(script):
    try:
        process = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(f"Error: {stderr.strip()}")
            sys.exit(1)
        return stdout.strip()
    except Exception as e:
        print(f"Exception: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Spotify macOS Control Script")
    parser.add_argument("action", choices=[
        "playpause", "next", "previous", "pause", "play",
        "get-info", "set-volume", "get-volume", "set-position",
        "set-shuffle", "set-repeat"
    ], help="Action to perform")
    parser.add_argument("value", nargs="?", help="Value for the action (e.g., volume level, position, on/off)")

    args = parser.parse_args()

    if args.action == "playpause":
        script = 'tell application "Spotify" to playpause'
    elif args.action == "next":
        script = 'tell application "Spotify" to next track'
    elif args.action == "previous":
        script = 'tell application "Spotify" to previous track'
    elif args.action == "pause":
        script = 'tell application "Spotify" to pause'
    elif args.action == "play":
        script = 'tell application "Spotify" to play'
    elif args.action == "get-info":
        script = """
        tell application "Spotify"
            set trackName to name of current track
            set trackArtist to artist of current track
            set trackAlbum to album of current track
            set trackUrl to spotify url of current track
            set pState to player state as string
            return "Spotify (" & pState & "): " & trackName & " - " & trackArtist & " [" & trackAlbum & "] URL: " & trackUrl
        end tell
        """
    elif args.action == "set-volume":
        vol = args.value if args.value else "50"
        script = f'tell application "Spotify" to set sound volume to {vol}'
    elif args.action == "get-volume":
        script = 'tell application "Spotify" to get sound volume'
    elif args.action == "set-position":
        pos = args.value if args.value else "0"
        script = f'tell application "Spotify" to set player position to {pos}'
    elif args.action == "set-shuffle":
        mode = "true" if args.value in ["on", "true", "yes"] else "false"
        script = f'tell application "Spotify" to set shuffling to {mode}'
    elif args.action == "set-repeat":
        mode = "true" if args.value in ["on", "true", "yes"] else "false"
        script = f'tell application "Spotify" to set repeating to {mode}'
    else:
        print(f"Unsupported action: {args.action}")
        sys.exit(1)

    result = run_osascript(script)
    if result:
        print(result)
    else:
        print(f"Action '{args.action}' executed successfully.")

if __name__ == "__main__":
    main()
