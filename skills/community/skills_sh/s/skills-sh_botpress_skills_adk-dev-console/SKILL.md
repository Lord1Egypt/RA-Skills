---
name: adk-dev-console
description: Explains the ADK Dev Console — what each tab shows, how to read Agent Steps, traces, multi-agent dashboard, agent switching, console modes, and other UI features visible at localhost:3001 during adk dev
license: MIT
---

# ADK Dev Console

The Dev Console is a local app served at port `3001` (by default, but can be customized) during `adk dev`. It gives developers real-time visibility into their agent's behavior — conversations, execution traces, data, integrations, and configuration.

The Dev Console is a **singleton shared dashboard**: one UI server per user, with multiple `adk dev` agents registering and deregistering dynamically. Developers can switch between running agents in the sidebar, toggle between dev and prod targets, and connect to deployed Cloud bots — all from the same browser tab.

## When to Use This Skill

Activate when users ask about:

- **UI concepts** — "What are Agent Steps?", "What does the Observe tab show?", "What is a turn?", "What is the component registry?", "What is the Agent Map?"
- **Agent(0) UI** — "What are the Tasks under Agent(0)?", "Where did the todo list come from?", "Why is Agent(0) showing task progress?"
- **Dev Console navigation** — "What tabs are available?", "Where do I find traces?", "How do I test RAG?"
- **Reading execution data** — "What do the steps mean?", "Why is my step red?", "What's the cost shown?"
- **Component registry** — "Where do I find custom components?", "How do I install a component?", "What components are available?"
- **Multi-agent dashboard** — "How do I switch between agents?", "How do I run multiple agents?", "What does the agent selector show?", "How do I see which agents are running?"
- **Console modes and targets** — "What's the difference between dev and prod?", "How do I connect to a Cloud bot?", "What is Cloud Dev Console?"
- **Agent management CLI** — "How do I list running agents?", "How do I stop an agent?", "What does `adk ps` show?", "How do I open the dashboard?"
- **Specific pages** — "How do I use the evals page?", "Where do I configure integrations?", "How do I search knowledge?"
- **Comparing UI vs CLI** — "Should I use the Dev Console or CLI for debugging?"
- Mentions of `localhost:3001`, "dev console", "Dev Console", "component registry", "agent selector", "agent picker", "agent map", "Cloud Dev Console", or specific tab names (Chat, Build, Components, Data, Test, Observe, Config)

## Available Documentation

| File                                  | Contents                                                                                                                                                    |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `references/agent-steps.md`           | Agent Steps visualization — turns, iterations, tools, messages, state mutations, cost tracking, status indicators                                           |
| `references/pages.md`                 | Every page/tab in the Dev Console — what it shows, key features, layout                                                                                     |
| `references/component-registry.md`    | Component Registry — installed vs registry tabs, component lifecycle, runtime registry internals, UI features                                               |
| `references/multi-agent-dashboard.md` | Multi-agent architecture, agent selector, console modes (local/cloud), dev/prod targets, CLI commands (`adk ps`, `adk kill`, `adk dashboard`, `adk status`) |

## How to Answer

Match depth to the question:

- **"What is X?"** (e.g., "What are Agent Steps?") → One sentence definition + what the user sees. Don't dump the full data model.
- **"Where do I find X?"** → Name the tab group and page, give the URL path.
- **"How do I read X?"** → Explain the visual hierarchy and what each element means.
- **"What does this mean?"** (pointing at something in the UI) → Identify the component, explain its meaning.

## Quick Reference

### Tab Groups

| Group          | Pages                                            | Purpose                                                                                          |
| -------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| **Chat**       | Chat                                             | Test the agent via webchat + see Agent Steps                                                     |
| **Build**      | Agent Map                                        | Interactive agent architecture graph (experimental, feature-flagged behind `enable_agent_forge`) |
| **Components** | Webchat Components, Actions, Workflows, Triggers | Browse component registry, test bot primitives                                                   |
| **Test**       | RAG Search, Evals                                | Test knowledge search and run automated evals                                                    |
| **Data**       | Knowledge, Tables, Files                         | Manage knowledge bases, tables, and files                                                        |
| **Observe**    | Conversations, Traces, Logs                      | View conversation history, execution traces, runtime logs                                        |
| **Config**     | Settings, Integrations                           | Agent config, secrets, LLM settings, integration management                                      |

### Agent(0) Task Dock

When Agent(0) uses its todo tool, the panel shows a compact **Tasks** dock with completed/total count, the active task, and an expandable task list. Status icons map to pending, in progress, completed, and cancelled; priorities are shown as low/medium/high chips.

### Multi-Agent Sidebar

The sidebar header shows the currently selected agent with a status indicator and mode pill (dev/prod/cloud). Clicking it opens the **Agent Selector** dropdown:

- **Active agents** — all running local agents with status dot, name, project path, and a close button
- **Cloud Dev Console** — switch to a deployed Botpress Cloud bot (workspace + bot picker)
- **Recent projects** — previously opened projects not currently running
- **Footer actions** — Create new project, Open existing, Switch environment (dev↔prod), About

### Agent Steps (Chat Page)

The right panel of the Chat page shows **Agent Steps** — a real-time visualization of what the agent did to process each message.

**Hierarchy:** Turn → Iterations → Tools / Messages / State Mutations

- **Turn** = one conversation exchange (user message → agent processing → response)
- **Iteration** = one loop of the autonomous agent (think → decide → act)
- **Tool** = a tool call within an iteration (violet card)
- **Message** = a bot message sent (blue card)
- **State Mutation** = a state change (teal card, shows before/after)

**Status indicators:** ✓ green = ok, ✗ red = error, ⟳ blue spinning = running

**AI metrics per iteration:** model name, input/output tokens, cost (USD)

### Key URLs

| Path             | Page                                                      |
| ---------------- | --------------------------------------------------------- |
| `/chat`          | Chat + Agent Steps                                        |
| `/agent-map`     | Agent Map — interactive architecture graph (experimental) |
| `/components`    | Component registry + installed components                 |
| `/actions`       | Actions browser                                           |
| `/workflows`     | Workflows + run history                                   |
| `/search`        | RAG search testing                                        |
| `/evals`         | Eval definitions + runs                                   |
| `/knowledge`     | Knowledge base management                                 |
| `/tables`        | Table data management                                     |
| `/traces`        | Full trace viewer                                         |
| `/conversations` | Conversation history                                      |
| `/logs`          | Runtime logs                                              |
| `/settings`      | Agent configuration                                       |
| `/integrations`  | Integration management                                    |

### Multi-Agent CLI Commands

| Command         | Purpose                                                                          |
| --------------- | -------------------------------------------------------------------------------- |
| `adk ps`        | List running agents and processes with PIDs, ports, uptime (supports `--watch`)  |
| `adk dashboard` | Open the DevConsole in standalone mode (no agent required)                       |
| `adk kill`      | Stop agents or the entire DevConsole (`--all`, `--current`, `--pid`, or by name) |
| `adk status`    | Show project health and status info                                              |
