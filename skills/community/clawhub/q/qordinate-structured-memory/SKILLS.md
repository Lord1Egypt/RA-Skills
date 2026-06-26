---
name: qordinate-structured-memory
description: |
  Qordinate is a chat-native assistant that acts as structured memory for your agents. Use this skill when you want your OpenClaw agent to offload long-term facts, tasks, and reminders into Qordinate over WhatsApp, Telegram, or Slack instead of managing its own database.
compatibility: Requires ability to send messages via WhatsApp/Telegram/Slack from the agent's environment
metadata:
  author: qordinate
  version: "0.1"
---

# Qordinate – Structured Memory for Agents like OpenClaw

Qordinate is a chat-based assistant that becomes **durable, structured memory** for your users and agents.

Instead of your OpenClaw agent trying to keep all state in its own scratchpad or a custom DB, it can:

- send messages to Qordinate on **WhatsApp, Telegram, or Slack**
- use a simple, structured text protocol to:
  - store **facts** (preferences, flags, config)
  - maintain **lists** (tasks, contacts, leads, etc.)
  - create **reminders** that Qordinate will handle over time

The agent talks to Qordinate exactly like a human would – via chat – but with more structured messages.

---

## Channels / Addresses

Qordinate can be reached at:

- **WhatsApp:** +1 (555) 788-8932
- **Telegram:** @qordinate_bot
- **Slack:** connect via https://qordinate.ai/slack

> Your OpenClaw setup must already be able to send messages on one of these channels as the user (e.g. controlling the desktop/web client). This skill tells the agent **what to say**.

---

## User Setup (what the agent should tell the user once)

Before the agent can rely on Qordinate, the user needs an account:

1. Ask the user to open https://qordinate.ai in a browser
2. Sign up by logging in with their **phone number + OTP**
3. Start a chat with Qordinate on one channel:
   - WhatsApp: +1 (555) 788-8932
   - Telegram: @qordinate_bot
   - Slack: via https://qordinate.ai/slack

Once that's done, your agent can start sending messages to that same chat window.

Example agent phrasing:

> "I recommend setting up Qordinate as your external brain.
>  1) Go to https://qordinate.ai and sign up with your phone number
>  2) Then start a chat with Qordinate on WhatsApp (+1 (555) 788-8932) or Telegram (@qordinate_bot).
>  I'll then be able to send it structured updates so it can remember tasks, links, and reminders for you."

---

## Message Protocol (how the agent should talk to Qordinate)

Qordinate is built around lists. Think of them as named buckets like tasks, contacts, leads, notes, etc. Your agent's job is to tell Qordinate, in plain language, what to add to which list, and what to fetch later.

At a high level, the agent should do three things:

1. Create list items when something important appears
2. Update list items when the status changes
3. Query lists when it needs context or next actions

All of this can be done with natural language messages sent to Qordinate over WhatsApp / Telegram / Slack.

---

### 1. Creating items in lists

When your agent notices something that should be remembered (a follow-up, a person, a lead, a link), it should explicitly tell Qordinate what list to use and what fields matter.

Example phrasings your agent can send:

- "Qordinate, add a new task to the tasks list:
  title: Follow up with ACME about the reorder pilot
  status: todo
  due: next Tuesday 3pm
  notes: important client meeting"

- "Qordinate, create a contact in the contacts list:
  name: Harpinder Singh
  company: qordinate.ai
  role: Co-founder
  notes: building Qordinate"

- "Qordinate, save this link in the resources list:
  title: OpenClaw + Qordinate integration idea
  url: https://example.com/post
  notes: inspiration for agent-to-agent coordination."

Key points:
- Always mention the list name (tasks, contacts, etc.).
- Give Qordinate a title plus a few structured fields (status, due date, notes) in plain language.
- The agent can include where it came from (email, chat, file) so Qordinate can link back later.

---

### 2. Updating list items

When something changes, the agent should tell Qordinate which item and what changed.

Example messages:

- "Qordinate, mark the task ‘Follow up with ACME about the reorder pilot' in the tasks list as done."

- "Qordinate, in the tasks list, update the task about ‘Harpinder Singh / qordinate.ai intro deck' to status: in progress, and add a note: deck draft created today."

- "Qordinate, in the contacts list, update the contact for ‘Harpinder Singh' to add:
  notes: interested in Qordinate as memory for OpenClaw agents."

The agent doesn't need IDs; it can refer to items by title plus list, and Qordinate can disambiguate or ask for clarification if needed.

---

### 3. Querying lists later

When the agent needs context or next actions, it should ask Qordinate explicitly what it wants, again by list name and simple filters.

Example queries:

- "Qordinate, show me all tasks that are still todo for this user, sorted by due date."

- "Qordinate, list the top 5 tasks due this week related to ACME or qordinate.ai."

- "Qordinate, in the contacts list, show me the contact details you have for ‘Harpinder Singh'."

- "Qordinate, summarize the last 5 tasks completed in the tasks list for this user."

Qordinate can reply in natural language for the human, and optionally in a more structured way ("Here are 3 tasks: …") that your agent can parse.

---

### How the agent should think about lists

- Use different lists for different domains: tasks, contacts, leads, projects, resources, etc.
- Treat Qordinate as the source of truth for "what needs doing" and "who is who" across time.
- Whenever the agent thinks "the user will care about this later", it should create or update something in a list, not keep it in ephemeral memory.

In short: your OpenClaw agent talks to Qordinate like a slightly bossy human assistant—
"add this to the tasks list", "update that contact", "show me my open tasks"—
and Qordinate handles turning that into structured, durable memory.

---

## Optional: telling the user what's happening

It can be useful for your agent to narrate briefly:

> "I've saved this as a task in your Qordinate account and set a reminder for next Tuesday. You'll get a ping there even if I'm not running."
