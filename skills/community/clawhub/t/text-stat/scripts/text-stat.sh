#!/usr/bin/env bash
# text-stat.sh — quick text statistics

tmpfile=$(mktemp)
trap 'rm -f "$tmpfile"' EXIT

# Read from file or stdin
if [ -n "$1" ] && [ "$1" != "/dev/stdin" ]; then
  cat "$1" > "$tmpfile"
else
  cat > "$tmpfile"
fi

lines=$(wc -l < "$tmpfile")
words=$(wc -w < "$tmpfile")
chars=$(wc -m < "$tmpfile")

# Reading time at 200 wpm
minutes=$(( words / 200 ))
seconds=$(( (words % 200) * 60 / 200 ))

printf "Lines:       %d\n" "$lines"
printf "Words:       %d\n" "$words"
printf "Characters:  %d\n" "$chars"
printf "Reading time (200 wpm): %dm %02ds\n" "$minutes" "$seconds"
