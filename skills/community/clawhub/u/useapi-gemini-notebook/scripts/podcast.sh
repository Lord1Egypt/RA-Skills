#!/usr/bin/env bash
# One command: links (and optional local files) -> a Gemini Notebook (NotebookLM) Audio Overview saved as .m4a.
# Usage: podcast.sh "<title>" URL|FILE [URL|FILE ...] [-- key=value ...]
# Example: podcast.sh "Apollo 11" https://en.wikipedia.org/wiki/Apollo_11 ./notes.pdf -- format=brief length=short
# Same as: studio.sh audio "<title>" ...
exec bash "$(dirname "$0")/studio.sh" audio "$@"
