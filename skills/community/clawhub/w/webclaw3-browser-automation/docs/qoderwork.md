# Using webclaw3 in qoderwork

**English** | [中文](./qoderwork.zh-CN.md)

Everything happens in the qoderwork chat — you say things, it runs the commands.

**0. Two one-time prerequisites** (only you can do these):

- Install the Chrome extension: download and unzip [wc3-chrome-extension-2.0.0.zip](https://github.com/fatmind/webclaw3/blob/main/dist/wc3-chrome-extension-2.0.0.zip), open `chrome://extensions/`, enable **Developer mode** → **Load unpacked** → pick the unzipped folder
- Log into [webclaw3.com](https://webclaw3.com) and grab your Access Key — it meters generation and unlocks the site-knowledge base

**1. Install + check** — say:

```
Install webclaw3 (https://github.com/fatmind/webclaw3) for me, then check the environment
```

qoderwork clones the repo into `~/.qoderwork/skills/webclaw3`, starts the local services, and walks you through the basic configuration (paste the Access Key, confirm the default directory for generated skills, etc.).

**2. Use it** — from here everything is conversation:

- Explore: `show me the trending list at https://example.com` → adjust until it's exactly what you want
- Distill: `distill that into a skill — I want to run it every day` (first time, it helps you grab an Access Key from [webclaw3.com](https://webclaw3.com))
- Run daily: `/skill-name run it` or schedule it
- Repair: paste the error, it fixes the skill locally

The full flow with examples is in the [README](../README.md#quickstart).
