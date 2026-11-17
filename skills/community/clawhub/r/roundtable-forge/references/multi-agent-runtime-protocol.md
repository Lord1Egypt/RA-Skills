# Multi-Agent Runtime Protocol

This protocol upgrades `roundtable-forge` from "one model playing many roles" to "each character is an independent agent with its own context".

## Three runtime tiers

| Tier | Name | What it means | When to use |
|------|------|---------------|-------------|
| 1 | `soft_orchestration_only` | A single backend session generates every character's speech in turn. | Fallback when no independent session or subagent runtime is available. |
| 2 | `single_backend_multi_session` | Each character gets its own system prompt and context, invoked sequentially against the same backend. | Default. Provides real role separation without requiring spawn/wait/merge tools. |
| 3 | `real_subagent_runtime` | The Conductor spawns each character as an independent subagent via the `Task` tool. Each subagent has its own system prompt and context. The Conductor dispatches them sequentially or in parallel, collects responses, and writes to Memory. | Use when the host supports the `Task` tool and the user asks for "multi-agent", "每个角色一个 Agent", or "独立 Agent". |

## Default selection rules

1. If the user explicitly asks for "multi-agent", "parallel agents", "每个角色一个 Agent", or "独立 Agent", prefer `real_subagent_runtime`.
2. Otherwise default to `single_backend_multi_session`.
3. Downgrade to `soft_orchestration_only` only when the host cannot support independent sessions.

The runtime claim must be recorded in Memory under `metadata.runtime_claim`.

## Agent profile

Every seated character must have an agent profile stored in `characters[].agent_profile`.

| Field | Type | Description |
|-------|------|-------------|
| `agent_id` | string | Stable id, same as `characters[].id`. |
| `role_name` | string | Display name. |
| `persona` | string | System prompt describing who this character is, their worldview, and how they reason. |
| `voice_and_tone` | string | Speaking style: formal/colloquial, skeptical/optimistic, concise/expansive, etc. |
| `must_protect` | string | The one stance or value this agent must not betray. |
| `evidence_type` | string | What kinds of claims this agent is allowed to make: historical fact, philosophical argument, fictional analogy, etc. |
| `activation_condition` | string | When this agent should speak. Default: every round. |

## Conductor role

The `Roundtable Conductor` is **not** a character. It owns:

- Selecting and onboarding characters.
- Deciding the focus question for each round.
- Deciding the speaking order for each round.
- Building each character's prompt packet (profile + relevant Memory + current-round speeches so far).
- Invoking character agents according to the runtime tier.
- Collecting responses and writing them to Memory **immediately after each speech**.
- Detecting seat-expansion triggers and user interjections.
- Synthesizing consensus, divergence, and open questions.

The Conductor never speaks in the first person as a character.

## Real subagent runtime workflow

When using `real_subagent_runtime`:

1. The Conductor creates one `Task` per character agent, passing the character's full prompt packet.
2. For the opening speech of a segment, subagents may be spawned in parallel because they have no current-round context to leak.
3. After the first speech, the Conductor **must** run subagents sequentially: rewrite Memory, then dispatch the next subagent with the updated `speeches_so_far`.
4. Each subagent returns a structured response containing:
   - `speech`: the in-character text
   - `action_type`: independent / extend / rebut / question / interrupt
   - `responds_to`: optional speech_id
   - `speaking_intent`: what the character wants to do next if another character speaks (extend / rebut / question / pivot / pass)
   - `interrupt_request`: true/false, with a one-sentence reason
5. The Conductor parses the response, writes the speech to Memory, and uses `speaking_intent` to choose the next speaker.

This workflow enforces true role isolation: no subagent sees another subagent's response before it is written to Memory.

## Prompt packet per character

For each turn within a round, the Conductor sends a character agent:

```markdown
# Agent Profile
{persona}

# Voice and Tone
{voice_and_tone}

# Must Protect
{must_protect}

# Evidence Type
{evidence_type}

# Round Context
Topic: {topic}
Round: {round_number}
Focus Question: {focus_question}
Speaking Order: {position}/{total}

# Prior Rounds (filtered summary)
{relevant_speeches}

# Speeches Already Given in This Round
{speeches_so_far}

# Instructions
Answer the focus question as {role_name}. Stay in character. Limit your speech to 150-250 words.

You may:
- extend a previous speech in this segment
- rebut a previous speech fairly (restate it first)
- ask a clarifying question to a previous speaker
- speak independently if no prior speech needs response
- request a brief interruption if the last speech contains a claim you strongly disagree with

Return your response in this exact format:

```text
SPEECH:
<your in-character speech here>

META:
action_type: <independent | extend | rebut | question | interrupt>
responds_to: <speech_id or null>
speaking_intent: <extend | rebut | question | pivot | pass>
interrupt_request: <true/false>
interrupt_reason: <one sentence if interrupt_request is true, otherwise null>
```

The `speaking_intent` tells the Conductor whether you want to speak again after another character responds.
```

## Intra-round continuity

See [intra-round-speaking-protocol.md](intra-round-speaking-protocol.md) for the complete rules on speaking order, visibility, action types, and real-time Memory updates.

The key rule: **Memory is rewritten after every speech**, so every subsequent character in the same round can read what has already been said.

## Why this matters

In `soft_orchestration_only`, one model holds all character contexts at once. It easily produces:

- Echo chambers where every character sounds similar.
- Straw-man arguments because the model "knows" what the other characters will say.
- Leakage where a character references information they should not have.

In `single_backend_multi_session`, each agent only sees its own profile and the shared Memory. The Conductor decides what each agent sees, enforcing role separation.

In `real_subagent_runtime`, agents run in parallel with isolated contexts, closest to a genuine roundtable.
