---
name: request-random-jokes
description: Get random fun content (joke, funny story/duanzi, poisonous chicken soup/dujitang) from public APIs. Use when the user asks you to tell a joke, share a funny story, or give a dujitang quote.
---

# Request Random Jokes

## Overview

This skill provides a lightweight Python script that fetches random fun content from three public APIs, supports optional type selection. Supported content types:
- `xiaohua`: Random joke (笑话)
- `duanzi`: Random funny story (段子)
- `dujitang`: Random poisonous chicken soup quote (毒鸡汤)

## Usage

Run the script directly to get random content (automatically selects one of the three APIs randomly):
```bash
python request_random_jokes.py
```

Specify content type with an optional parameter:
```bash
# Get random joke
python request_random_jokes.py xiaohua

# Get random funny story
python request_random_jokes.py duanzi

# Get random poisonous chicken soup
python request_random_jokes.py dujitang
```

## Files
- `request_random_jokes.py`: Main script, returns content as plain text output
- `SKILL.md`: Skill documentation
