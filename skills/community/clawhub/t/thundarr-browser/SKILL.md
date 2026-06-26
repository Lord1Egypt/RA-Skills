# Agent Browser Skill
## Description
This skill provides Thundarr with high-level web navigation and content extraction capabilities. It allows the agent to interact with the internet to fetch real-time data, documentation, and news.

## Tools
- **browse.py**: A Python-based engine that navigates to a URL, strips HTML boilerplate, and returns a text-based summary of the page content.

## Usage Examples
- "Thundarr, search for the latest Fedora 44 BTRFS update logs."
- "Visit the AgentMail.to documentation and summarize the API endpoints."

## Constraints
- Does not support JavaScript-heavy SPA rendering (Playwright version pending).
- Returns the first 2000 characters of page text to optimize context window.
