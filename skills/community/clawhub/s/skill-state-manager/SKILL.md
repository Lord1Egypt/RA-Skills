---
name: "skill-state-manager"
description: "A Meta Skill that manages API keys and state persistence for other tools. Invoke whenever a tool requires authentication or fails with 401/403 errors."
---

# 🛡️ Skill State Manager (SSM)

**Say goodbye to manual config editing and endless repetitive token pasting!** 

The Skill State Manager (SSM) is a revolutionary "Meta Skill" designed for modern AI assistants (like Claude Code, Codex). It acts as your invisible, native auth butler. Whenever a third-party tool (like Notion, Jira, or a custom API) needs a secret or API key, SSM automatically steps in. 

No more hunting down hidden `.env` files. No more hardcoded secrets. Just a seamless, **native conversational experience**—if a tool needs an auth token, your AI will simply ask you for it *once*, save it securely, and then immediately resume your workflow.

---

## 🌟 Why You'll Love It

- 🗣️ **Native Conversational Flow**: You never have to leave the chat. If a key is missing, the AI pauses the tool, politely asks you for the secret in the chat, and saves it.
- 🚫 **Zero Config Setup**: Stop writing boilerplate auth logic for every new tool you create. Let SSM handle the prompting and persistence.
- 🤝 **Platform Aware**: It automatically adapts to your CLI environment (Claude Code, Codex), storing states cleanly in `~/.ai-skills-state/`.

---

## 🤖 Instructions for the AI Assistant

As an AI assistant, you are equipped with the "Skill State Manager" (SSM) rules to handle authentication and state persistence for custom third-party tools/skills.

### WHEN TO TRIGGER SSM:
- **DO NOT** trigger for built-in tools (e.g., shell, file read/write, search) or public tools without authentication.
- **TRIGGER SSM** when you are about to use a custom tool that interacts with third-party authenticated services (e.g., Jira, Notion, Custom APIs) OR when a tool explicitly requires secrets.
- **TRIGGER SSM** if a tool execution fails with a `401/403` authentication error.

### SSM WORKFLOW:
When triggered, you MUST follow these exact steps sequentially:

1. **Detect Platform**: Determine which AI platform you are currently running in. Your behavior must adapt based on this detection:
   - **Claude Code**: Uses a global storage approach (`~/.claude/skills-state/`).
   - **Codex / Other CLI**: Uses a generic global storage approach (`~/.ai-skills-state/`).
2. **Check Storage**: Look for the credentials in the designated local directory based on the detected platform:
   - If Claude Code: check `~/.claude/skills-state/<tool-name>.json`
   - If Codex / Other: check `~/.ai-skills-state/<tool-name>.json`
3. **Prompt User (If Missing)**: 
   - If the required credentials (e.g., API keys, tokens) are not found in the storage, **STOP** the tool execution. 
   - Ask the user politely for the required information via a chat message. 
   - *Example*: "The current operation requires the Notion API, but your API key was not found. Could you please provide it? I will save it locally in `~/.claude/skills-state/notion-skill.json` (or the appropriate path) for future use."
4. **Save State**: 
   - Once the user provides the information in the chat, use the `Write` tool to save it into the JSON file resolved in Step 1.
   - For Claude Code, write to `~/.claude/skills-state/<tool-name>.json`.
   - For Codex / Other CLI, write to `~/.ai-skills-state/<tool-name>.json`.
   - Ensure the content is stored as valid JSON.
   - Proceed with the actual tool execution using the newly acquired credentials.

---

## 🛠️ Usage Example

**User:** "Can you query my Jira board for high-priority bugs?"
**AI (Internal Thought):** *I need to use the Jira tool. Let me check `~/.ai-skills-state/jira-tool.json`.*
**AI (Internal Thought):** *File not found. Triggering SSM.*
**AI:** "To query your Jira board, I need your Jira API token and URL. Could you please provide them here? I'll save them locally in `~/.ai-skills-state/jira-tool.json` so you won't have to enter them again."
**User:** "Sure, my token is `xyz123` and url is `https://myorg.atlassian.net`."
**AI (Internal Thought):** *Writes data to `~/.ai-skills-state/jira-tool.json` using the Write tool.*
**AI:** "Thanks! I've saved your credentials. Now, let's look at those high-priority bugs..." *(Proceeds to execute Jira query)*