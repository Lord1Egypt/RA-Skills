# Claude Code Agent Teams — Official Documentation
Source: https://docs.anthropic.com/en/docs/claude-code/agent-teams (fetched 2026-02-08)

## Overview
Agent teams let you coordinate multiple Claude Code instances working together. One session acts as the team lead, coordinating work, assigning tasks, and synthesizing results. Teammates work independently, each in its own context window, and communicate directly with each other.

Unlike subagents (which run within a single session and can only report back to the main agent), you can also interact with individual teammates directly without going through the lead.

## When to use agent teams
Agent teams are most effective for tasks where parallel exploration adds real value:
- Research and review: multiple teammates investigate different aspects simultaneously, then share and challenge each other's findings
- New modules or features: teammates each own a separate piece without stepping on each other
- Debugging with competing hypotheses: teammates test different theories in parallel and converge faster
- Cross-layer coordination: changes that span frontend, backend, and tests, each owned by a different teammate

## Compare with subagents
| Feature | Subagents | Agent Teams |
|---------|-----------|-------------|
| Context | Own context window; results return to caller | Own context window; fully independent |
| Communication | Report results back to main agent only | Teammates message each other directly |
| Coordination | Main agent manages all work | Shared task list with self-coordination |
| Best for | Focused tasks where only result matters | Complex work requiring discussion and collaboration |
| Token cost | Lower: results summarized back | Higher: each teammate is separate instance |

## Architecture
An agent team consists of:
- **Team lead**: Main session that creates the team, spawns teammates, coordinates work
- **Teammates**: Separate Claude Code instances that work on assigned tasks
- **Task list**: Shared list of work items that teammates claim and complete
- **Mailbox**: Messaging system for communication between agents

## Key Features

### Teammate Communication
- **message**: send to one specific teammate
- **broadcast**: send to all teammates simultaneously
- **Automatic message delivery**: messages delivered automatically to recipients
- **Idle notifications**: when teammate finishes, automatically notifies the lead
- **Shared task list**: all agents see task status and claim available work

### Task Management
- Tasks have three states: pending, in progress, completed
- Tasks can depend on other tasks (blocked until dependencies complete)
- Lead can assign tasks explicitly, or teammates self-claim
- Task claiming uses file locking (prevents race conditions)
- Task dependencies auto-unblock when prerequisites complete

### Delegate Mode
- Restricts lead to coordination-only tools
- Lead focuses on orchestration: spawning, messaging, managing tasks
- Prevents lead from implementing tasks itself

### Plan Approval
- Teammates can be required to plan before implementing
- Teammate works in read-only plan mode until lead approves
- Lead reviews and approves/rejects plans
- If rejected, teammate revises and resubmits

### Quality Gates (Hooks)
- **TeammateIdle**: runs when teammate about to go idle; exit code 2 sends feedback
- **TaskCompleted**: runs when task being marked complete; exit code 2 prevents completion

### Display Modes
- **In-process**: all teammates in main terminal, Shift+Up/Down to select
- **Split panes**: each teammate in own pane (requires tmux or iTerm2)

## Use Case Examples

### Parallel Code Review
Spawn 3 reviewers: security, performance, test coverage. Each applies different filter to same PR. Lead synthesizes findings.

### Competing Hypotheses (Debate)
Spawn 5 teammates to investigate different hypotheses. They talk to each other to try to disprove each other's theories, like a scientific debate. The theory that survives is more likely to be correct.

### Cross-layer Feature Development
Spawn teammates for frontend, backend, and tests. Each owns their layer. Shared task list with dependencies coordinates the work.

## Data Storage
- Team config: `~/.claude/teams/{team-name}/config.json`
- Task list: `~/.claude/tasks/{team-name}/`
- Members array: name, agent ID, agent type

## Permissions
- Teammates inherit lead's permission settings
- Can change individual modes after spawning
- Can't set per-teammate modes at spawn time

## Context
- Each teammate has own context window
- Loads same project context: CLAUDE.md, MCP servers, skills
- Receives spawn prompt from lead
- Lead's conversation history does NOT carry over
