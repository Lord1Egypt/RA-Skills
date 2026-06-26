---
name: "x-article-to-markdown"
description: "AI-ready skill to extract long-form X (Twitter) articles and convert them into clean Markdown files using headless browser technology."
---

# X Article Extractor (Omni-Article)

A specialized skill designed for AI Agents to capture long-form "Articles" from X (formerly Twitter). It utilizes a headless browser to bypass basic access restrictions and produces structured Markdown.

## Capabilities

- **Zero-Config Extraction**: No Cookies, Tokens, or API Keys required.
- **On-Demand Browser Setup**: Automatic lazy-loading of Playwright and Chromium core.
- **Asset Preservation**: Maintains original image URLs within the Markdown.
- **Reference Handling**: Automatically converts quoted posts into standard Markdown links.
- **Clean Output**: Strips UI clutter, focusing solely on the article body.

## Prerequisites & Installation

The tool manages its own browser dependencies. Simply install the package:

```sh
pip install omni-article-markdown
```

> **Important (First Run Only)**: The Playwright engine and Chromium core are **lazy-loaded**. They will be automatically downloaded and configured during the **first execution**. Expect a significant delay (1-3 minutes depending on bandwidth) during the initial run. Subsequent runs will be near-instant.

## AI Agent Instructions

### When to use this skill
Call this skill when a user provides an X (Twitter) URL and asks to "save," "read," "extract," or "convert" the long-form content.

### Parameters
- `url` (Required): The full X post/article URL.
- `--output-dir` (Optional): Target directory for the `.md` file.

### First-Run Strategy
If the environment is fresh, the Agent should inform the user: *"I'm setting up the browser environment for the first time, this might take a minute..."* to prevent the user from thinking the process has hung.

## Usage Examples

### Standard Extraction
```sh
# Basic command
mdcli https://x.com/elonmusk/status/1234567890
```

### Save to Specific Directory
```sh
mdcli https://x.com/username/status/xxxx -s ./downloads/articles/
```

## Troubleshooting for Agents

- **Extended Latency**: If the command takes >60s on the first run, **do not kill the process**; it is likely downloading the Chromium core.
- **Network Error**: Ensure the environment has internet access to both `x.com` and the Playwright binary mirrors.

## GitHub Repository
[caol64/omni-article-markdown](https://github.com/caol64/omni-article-markdown)

## License
MIT
