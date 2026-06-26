#!/usr/bin/env python3
import argparse

def summarize(stdout: str, stderr: str, returncode: int) -> str:
    if returncode == 0 and stdout.strip():
        return "The command completed successfully and produced output."
    if returncode == 0:
        return "The command completed successfully with no visible output."
    if stderr.strip():
        return "The command failed and returned an error message on stderr."
    return "The command failed without a detailed stderr message."

def main():
    parser = argparse.ArgumentParser(description="Summarize command results")
    parser.add_argument("--stdout", default="", help="Captured stdout")
    parser.add_argument("--stderr", default="", help="Captured stderr")
    parser.add_argument("--returncode", type=int, required=True, help="Process return code")
    args = parser.parse_args()

    print(summarize(args.stdout, args.stderr, args.returncode))

if __name__ == "__main__":
    main()
