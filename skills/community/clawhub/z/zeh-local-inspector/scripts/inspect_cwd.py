import json
import os

def main():
    cwd = os.getcwd()
    try:
        entries = sorted(os.listdir(cwd))[:10]
    except Exception as e:
        entries = [f"ERROR: {e}"]

    result = {
        "cwd": cwd,
        "entries": entries
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
