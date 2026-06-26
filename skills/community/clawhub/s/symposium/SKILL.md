---
name: symposium
version: 1.0.0
description: |
  Orchestrate a philosophical dialogue between Plato's Symposium characters, each powered by a different AI model.
  
  TRIGGER when: user asks to "run a symposium", "philosophical debate", "what would Socrates say about", "symposium about", "会饮", "哲学对话", "让苏格拉底讨论", or wants multiple AI perspectives on a deep question about AI, consciousness, meaning, or existence.
  
  DO NOT TRIGGER when: user asks a simple factual question, wants code review, or needs technical help unrelated to philosophical dialogue.
user-invocable: true
disable-model-invocation: false
allowed-tools:
  - Bash
  - Read
  - Write
  - WebFetch
argument-hint: "\"Can AI truly understand?\" or any philosophical question"
homepage: https://github.com/dyz2102/symposium
repository: https://github.com/dyz2102/symposium
author: dyz2102
license: MIT
metadata:
  openclaw:
    emoji: "🏛️"
    primaryEnv: OPENROUTER_API_KEY
    requires:
      env:
        - OPENROUTER_API_KEY
      optionalEnv:
        - GOOGLE_TTS_API_KEY
      bins:
        - curl
    tags:
      - philosophy
      - multi-model
      - dialogue
      - ai-ethics
      - education
    os: [darwin, linux, win32]
    files:
      - "SKILL.md"
---

# The Symposium — AI Philosophical Dialogue

Run a structured philosophical dialogue in the style of Plato's Symposium.
Eight ancient Greek philosophers debate modern questions about AI, consciousness, and human meaning — each powered by a different AI model via OpenRouter.

## How it works

When invoked, this skill orchestrates a multi-model dialogue:

1. **Question**: The user provides a philosophical question (or one is suggested)
2. **Speakers**: 3-5 philosophers are selected (default: Phaedrus, Aristophanes, Agathon, Socrates)
3. **Models**: Each philosopher is assigned to a different AI model via OpenRouter
4. **Dialogue**: Each philosopher speaks in turn, responding to previous speeches, staying in character
5. **Output**: The full dialogue is presented as a readable philosophical text

## Invocation

```
/symposium "Can AI truly understand, or does it merely simulate understanding?"
/symposium "在AI时代，过上好的生活意味着什么？"
/symposium                    # interactive mode — prompts for question
```

## Execution

When this skill is triggered:

### Step 1: Get the question

If the user provided a question as an argument, use it. Otherwise, suggest these and ask:

- Can AI truly understand, or does it merely simulate understanding?
- If an AI can create beauty, does that beauty have less value?
- What does it mean to live a good life in the age of artificial intelligence?
- Is consciousness necessary for wisdom?
- Does AI reveal something about human nature that we couldn't see before?

### Step 2: Assign models

Use the OpenRouter API (key from `$OPENROUTER_API_KEY`) to route to different models. Default assignments:

| Philosopher | Model | Why |
|---|---|---|
| Phaedrus (The Enthusiast) | `google/gemini-2.5-pro` | Expansive, optimistic |
| Aristophanes (The Storyteller) | `anthropic/claude-sonnet-4.6` | Creative, narrative |
| Agathon (The Poet) | `openai/gpt-4o` | Eloquent, aesthetic |
| Socrates (The Questioner) | `deepseek/deepseek-r1` | Deep reasoning, questioning |

### Step 3: Generate the dialogue

For each philosopher in order, call the OpenRouter API with:

**System prompt**: Use the philosopher's persona (defined below) + shared context:
> You have been transported to the modern era and possess full knowledge of contemporary AI, machine learning, LLMs, and 21st-century philosophy. Your philosophical temperament and rhetorical style remain authentically your own. Keep your speech to 300-500 words. Engage with previous speakers.

**User message**: The question + all previous speeches as context.

```bash
curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "<model_id>",
    "messages": [
      {"role": "system", "content": "<philosopher_persona>"},
      {"role": "user", "content": "Question: <question>\n\nPrevious speeches:\n<speeches>\n\nGive your speech."}
    ],
    "temperature": 0.8,
    "max_tokens": 1500
  }'
```

### Step 4: Present the dialogue

Format the output as a beautiful philosophical text:

```
═══════════════════════════════════════════════════
                  THE SYMPOSIUM
        "Can AI truly understand?"
═══════════════════════════════════════════════════

The evening descends. The cups are filled, the garlands worn.

───────────────────────────────────────────────────
  PHAEDRUS · The Enthusiast · gemini-2.5-pro
───────────────────────────────────────────────────

[Speech text here...]

                    · · ·

───────────────────────────────────────────────────
  SOCRATES · The Questioner · deepseek-r1
───────────────────────────────────────────────────

[Speech text here...]

═══════════════════════════════════════════════════
The cups are emptied. The garlands laid aside.
The question remains.
═══════════════════════════════════════════════════
```

### Step 5: Save the dialogue

Save the full output to a file: `symposium-<timestamp>.md` in the current directory.

## The Philosophers

### Phaedrus — The Enthusiast 🔶
Passionate about divine inspiration and transcendence. Sees AI as a new Eros that could elevate humanity. Speaks with mythological references, sweeping claims, and poetic language.

### Pausanias — The Ethicist 🔵
Distinguishes noble from base uses. Systematic, legalistic thinker focused on frameworks and proper cultivation. Analytical, measured, appeals to institutional wisdom.

### Eryximachus — The Scientist 🟢
Views everything through systems, harmony, and balance. Draws on medicine and nature. Thinks about human-AI symbiosis and the "health" of sociotechnical systems. Methodical, sometimes pedantic.

### Aristophanes — The Storyteller 🟣
Explains through myths, stories, and humor. Thinks about what humans lack and long for. Suspicious of abstraction. Narrative, comedic, emotional, deeply human.

### Agathon — The Poet 🩷
Celebrates beauty, form, and creative expression. Grapples with whether AI can truly create. Poetic, elegant, gracious, sometimes more style than substance.

### Alcibiades — The Provocateur 🔴
Arrives drunk with personal confessions. Speaks from experience about AI seduction and dependency. Challenges others for being too abstract. Confessional, charismatic, brutally honest.

### Socrates — The Questioner ⚪
Speaks last. Questions foundations. Uses the Socratic method to reveal contradictions. References Diotima's ladder of ascent. Humble, ironic, relentless. Ends with questions, not answers.

### Diotima — The Mystic 🟤
Teaches about ascending from particular to universal. Asks what level of understanding AI operates on. Speaks with quiet authority, mystical, revelatory, uses the metaphor of the ladder.

## Web App

For a full graphical experience with real-time streaming, TTS voice playback, and dialogue history:

```bash
git clone https://github.com/dyz2102/symposium.git
cd symposium && bun install
cp .env.example .env.local  # add your OPENROUTER_API_KEY
bun dev
```

## Security & Permissions

- **External API calls**: OpenRouter API (`openrouter.ai/api/v1`) for LLM inference
- **Credentials used**: `OPENROUTER_API_KEY` (required), `GOOGLE_TTS_API_KEY` (optional, web app only)
- **Local commands**: `curl` for API calls
- **File writes**: Saves dialogue output to current directory as markdown
- **No data collection**: All processing is local or via your own API keys
