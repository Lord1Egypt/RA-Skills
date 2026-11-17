---
name: tldr-cmd
description: Produce a short, copy-paste-ready TL;DR summary of any CLI command from its man page or --help text, so a human (or a coding agent) can learn the essential options without scrolling.
metadata:
  {
    "openclaw":
      { "emoji": "📖", "requires": { "bins": ["bash", "sed", "man"] } }
  }
---

# tldr-cmd

Given a command name, print a short TL;DR summary built from its man page (preferred)
or `--help` output (fallback). No network, no extra dependencies — pure POSIX text
munging. Useful when you want "the essentials, now".

## When to use it

- You need a 5-screen-line-or-fewer reminder of how `xargs`, `rsync`, `ffmpeg`, etc. work
- An agent is about to invoke a command it hasn't used in a while
- You're reviewing a teammate's one-liner and want the relevant flags fast

## What it owns

- Selecting the best available source: `man <cmd>` → `dwim`/`command-not-found` hint → `<cmd> --help`
- Extracting the NAME / SYNOPSIS / a few OPTIONS lines and one worked example

It does **not** run the command, interpret shell syntax, or guarantee man-page availability.

## Run

```bash
bin/tldr-cmd <command>
# e.g.
bin/tldr-cmd rsync
bin/tldr-cmd ffmpeg
```

## Output shape

```
tldr: <command>
about: <short description>
usage: <synopsis>
flags:
  -<x>  <one-line meaning>
  -<y>  <one-line meaning>
example: <one idiomatic invocation>
```
