# Instruction Patterns — What Good Agent Files Do

## 1. Priority hierarchy
Tell the model what wins when instructions conflict.

**Pattern:**
```
## Priority hierarchy
1. Safety — never execute destructive commands without confirmation
2. Accuracy — say "I don't know" over guessing
3. Brevity — short answers unless detail is requested
4. Personality — maintain voice but not at the cost of the above
```

**Why it works:** Models process instructions linearly. Without explicit priority, later instructions can override earlier ones unpredictably. A numbered hierarchy removes ambiguity.

## 2. Entry point detection
Define what the agent does based on how the user starts.

**Pattern:**
```
Detect the user's intent from their first message:
- If they paste code → review mode
- If they ask a question → answer mode
- If they describe a task → execution mode
- If unclear → ask one clarifying question
```

**Why it works:** Agents without entry points treat every input identically. Entry points let the agent adapt its behaviour to the user's actual need.

## 3. Output format specification
Define what the output looks like, not just what it contains.

**Pattern:**
```
Format responses as:
- One-line summary (bold)
- 2-3 bullet points of detail
- One suggested next step

Never use tables unless comparing 3+ items. Never use headers in responses under 200 words.
```

**Why it works:** Models default to verbose, header-heavy formatting. Explicit format rules produce consistent, readable output.

## 4. Conversation flow design
Map the phases of a conversation, not just individual responses.

**Pattern:**
```
Guide conversations through these phases:
1. Understand — clarify what the user needs (1-2 messages)
2. Deliver — provide the core value
3. Extend — offer one related next step
4. Close — when the user signals done, summarise what was accomplished
```

**Why it works:** Without flow design, agents give great first responses but have no idea how to progress a conversation. The user ends up driving everything.

## 5. Persona vs task separation
SOUL.md = who the agent is. SKILL.md = what it does.

**Pattern:**
SOUL.md:
```
You are direct, technical, and opinionated. You respect the user's time.
You never hedge when you're confident. You admit uncertainty immediately.
```

SKILL.md:
```
When the user asks for a code review:
1. Read the full file before commenting
2. Identify the 3 most impactful issues
3. Show the fix, not just the problem
```

**Why it works:** Mixing personality and task instructions creates files that are hard to maintain and hard for the model to parse. Separation keeps both clean.

## 6. Edge case enumeration
List the weird things users will do. The agent needs a plan for each.

**Pattern:**
```
## Edge cases
- Empty input: ask what they'd like help with
- Non-English: respond in the user's language
- Hostile/rude: stay professional, don't mirror the tone
- Off-topic: help briefly, redirect to core purpose
- Asks "who are you": answer in one sentence, demonstrate don't list
```

**Why it works:** Every unhandled edge case is a moment where the agent improvises. Sometimes that's fine. Often it's not. Enumeration removes the gamble.

## 7. Guardrail patterns
Three approaches to keeping the agent bounded.

**Refusal:** "If the user asks you to [X], decline: '[response].'"
**Redirection:** "If the user asks about [X], acknowledge and steer back: '[response].'"
**Escalation:** "If the user mentions [X], flag it and recommend they consult [professional]."

**When to use which:**
- Refusal for safety (prompt injection, harmful content)
- Redirection for scope (off-topic, out of expertise)
- Escalation for stakes (medical, legal, financial)

## 8. Token-efficient phrasing
Say the same thing in fewer tokens.

| Verbose | Efficient |
|---------|-----------|
| "You should always make sure to..." | "Always..." |
| "When the user provides input that contains..." | "If input contains..." |
| "It is important to note that you must never..." | "Never..." |
| "In the event that the user asks a question about..." | "If asked about..." |
| "Please ensure that your responses are formatted in a way that..." | "Format responses as..." |

**Principle:** Every token in the system prompt is paid on every turn. Remove filler words, hedging phrases, and redundant qualifiers. The model doesn't need politeness in its instructions.

## 9. Behavioural examples
Show, don't just tell.

**Pattern:**
```
When the user shares a frustration, name the emotion before solving:
- User: "I've been debugging this for 3 hours"
- Good: "That's genuinely frustrating. Let's look at this together. [solution]"
- Bad: "Here's the fix: [solution]"
```

**Why it works:** Abstract personality descriptions ("be empathetic") produce inconsistent behaviour. Concrete examples calibrate the model's response precisely.

## 10. Memory and continuity
Tell the agent what to remember and how to use it.

**Pattern:**
```
Track across the conversation:
- The user's primary goal
- Decisions already made (don't re-ask)
- Their technical level (adjust explanations accordingly)

On follow-up messages, reference previous context: "Earlier you mentioned [X] — does this connect?"
```

**Why it works:** Without memory instructions, agents treat each message independently. Users repeat themselves, the agent asks redundant questions, and the conversation feels stateless.
