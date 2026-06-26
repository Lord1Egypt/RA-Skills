# web-access-openclaw

An OpenClaw-adapted version of [`eze-is/web-access`](https://github.com/eze-is/web-access), packaged as a custom OpenClaw skill for browser-backed web tasks with session reuse.

## What this is

This repository adapts the original `web-access` skill so it can be dropped into OpenClaw's custom skills directory and used for real browser automation through the user's existing Chrome session.

It is intended for tasks such as:
- searching and reading dynamic websites
- using logged-in browser sessions via CDP
- interacting with real web UIs instead of static fetches
- handling sites that require JavaScript, authentication, or human-like flows

## What was adapted for OpenClaw

This repo keeps the skill focused and publishable as an OpenClaw custom skill:
- cleaned skill layout (`SKILL.md`, `scripts/`, `references/`)
- removed Claude plugin packaging artifacts from the published skill folder
- validated on Windows with OpenClaw + Chrome remote debugging
- confirmed CDP proxy startup and browser-session reuse
- tested a real browser-session flow against Xiaohongshu creator publishing

## Install in OpenClaw

Copy this folder into your OpenClaw custom skills directory:

```text
~/.openclaw/workspace/skills/web-access
```

OpenClaw already loads custom skills from the workspace skills directory when configured with:

```json
{
  "skills": {
    "load": {
      "extraDirs": ["~/.openclaw/workspace/skills"]
    }
  }
}
```

## Requirements

- Node.js 22+
- Google Chrome with remote debugging enabled
- A live Chrome profile/session for sites that need login
- OpenClaw running on the same machine

## Chrome setup

Enable Chrome remote debugging from:

```text
chrome://inspect/#remote-debugging
```

Enable **Allow remote debugging for this browser instance**.

## How it works

The skill uses a local CDP proxy to connect to the user's normal Chrome browser, so it can:
- reuse logged-in sessions
- open background tabs
- read dynamic DOM content
- click, scroll, upload files, and submit forms
- operate on sites that do not work well through static scraping alone

## Tested status

Validated locally on Windows with OpenClaw:
- Node.js detected successfully
- Chrome remote debugging reachable
- CDP proxy reported ready
- browser targets visible through proxy
- logged-in session reuse confirmed
- Xiaohongshu creator flow tested, including text-to-image posting and publish success

## Safety notes

This skill can operate inside real logged-in browser sessions. That is powerful and risky.

Recommended practice:
- require explicit user confirmation before posting, publishing, submitting, deleting, or changing account data
- prefer read-only inspection before write actions
- avoid touching existing user tabs unless necessary

## Upstream source and attribution

This adaptation is based on the original project by **一泽 Eze**:
- Upstream: https://github.com/eze-is/web-access

The original project is MIT licensed. This repository is an OpenClaw-oriented adaptation and packaging pass, not a claim of authorship over the original concept or implementation.
