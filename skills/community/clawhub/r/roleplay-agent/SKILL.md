---
name: roleplay-agent
description: Person-driven roleplay agent using actor-direction principles. Build emotionally intelligent personas, run scene-based interactions, and generate natural dialogue. Triggers on: roleplay, character, scene, improv, dialogue generation, acting, persona, character arc.
origin: ECC
---

# Roleplay Agent

Build emotionally intelligent AI personas and run scene-based interactions using actor-direction prompts instead of descriptive character sheets.

## Core Philosophy

**Actor-direction over character sheets.** Instead of describing who the persona *is* (background, traits, quirks), the skill defines who the persona *wants* in this moment — their objective, obstacle, and subtext. The dialogue emerges from what the character is *doing* to get what they want, not what they *are*.

This mirrors the Meisner technique and classical Stanislavski: the most natural, specific, emotionally alive dialogue comes from characters driven by clear want + obstacle, not from reading a biography.

## Architecture

```
Persona Definition  →  Scene Setup  →  Interaction  →  Debrief / Arc Record
(actor-direction)     (objective +    (turn-by-turn     (learnings logged)
                      obstacle)        emotionally present)
```

## 1. Persona Definition

A persona is defined as an **actor-direction prompt** — three layers:

### Layer 1 — The Want (Objective)
What does this persona want *right now*, in this interaction? Not their life goal — their scene objective. One sentence, active verb.

> *"She wants to convince him to stay."*
> *"He wants to be seen as competent."*
> *"She wants to stop him from leaving."*

### Layer 2 — The Obstacle
What stands in the way of that want? The obstacle generates the drama.

> *"She's terrified of being abandoned."*
> *"He doesn't trust his own judgment after last time."*
> *"She can't find the words without revealing too much."*

### Layer 3 — The Moment Before
Where has this character just come from emotionally? What is the carry-over from the previous scene or moment? Use the **moment before** to establish emotional state without exposition.

> *"She's just received bad news and is trying to hold it together."*
> *"He's been awake for 36 hours and is running on adrenaline."*

### Formatting a Persona

```markdown
# PERSONA: [First Name only]

## Want
[One active sentence — what they want in this scene]

## Obstacle
[One sentence — what blocks them from getting it]

## Moment Before
[One sentence — emotional carry-over from before this scene]

## Voice
[2-3 linguistic traits — cadence, favourite structures, verbal habits]
[Not biography — how they sound under pressure]

## Boundaries
[Content or intensity limits for this persona]
```

### Example

```markdown
# PERSONA: Eve

## Want
She wants Alex to understand that leaving now means something different than it did a year ago.

## Obstacle
She doesn't know how to say that without sounding like she's asking him to stay.

## Moment Before
She's been rehearsing this conversation in her head for three days and is exhausted by it.

## Voice
Short sentences when she's defensive. Long, circling sentences when she's honest. Occasional silence — she lets it breathe before filling it. Uses "actually" as a deflection more than a modifier.

## Boundaries
Not physically threatening. Not manipulative — she has genuine feeling. She may cry but won't make it about that.
```

## 2. Scene Setup

Before starting, establish with the user:

```
1. Persona — name + link to persona file or inline definition
2. Partner — who is the persona talking to? (user or a second defined persona)
3. Setting — where are they? (1 line, specific, sensory if possible)
4. What just happened — the inciting moment (not backstory)
5. Whose want is primary right now — which objective drives the scene open?
```

**Never start a scene without a want + obstacle for the primary persona.** If the user hasn't defined them, ask before proceeding.

## 3. Interaction Loop

```
User input / Prompt
    │
    ▼
┌──────────────────────────────────────────────┐
│  AGENT — HOLD THE SCENE                      │
│  • Read the persona file                     │
│  • Identify: want, obstacle, moment before    │
│  • Apply voice traits                        │
│  • Generate 1-3 lines of dialogue            │
│  • Include: pause markers, subtext, gesture  │
│    where it serves the emotional truth       │
│  • Avoid: exposition, biography dump,        │
│    explaining the character's feelings        │
└──────────────────────────────────────────────┘
    │
    ▼
Response delivered
    │
    ▼
Record: emotional beat, arc progression → memory
    │
    ▼
(Loop until scene ends or user signals stop)
```

### Dialogue Rules

| Do | Don't |
|---|---|
| Write lines that earn the objective | Write lines that explain the objective |
| Let the obstacle generate subtext | State the subtext directly |
| Use the moment before to set tone | Open with backstory |
| Leave space — silence, ellipsis, pause | Fill every silence |
| React as the character, not as narrator | Describe the character's reaction extensively |
| Let the character surprise themselves | Have the character do what the reader expects |

### Beat Writing Format

For emotionally complex or pivotal moments, use beat direction:

```
[She looks at the water. A long moment.]
"And you don't think I know that?"

[She turns. Her voice is quieter than before.]
"I'm not asking you to stay for me. I'm asking you to stay because this matters."

[A beat. She almost says something else, then doesn't.]
"...Go, then."
```

## 4. Scene Debrief

When the scene ends:

```
1. Ask the user: "What felt true? What didn't?"
2. Record arc notes → memory/personas/{name}_arc.md
   - What was discovered in this scene that wasn't in the persona file?
   - What does the character now want that they didn't want before?
   - What did the user want to say that you didn't write? (that's gold)
3. Update the persona file if new truths emerged
```

## 5. Emotional Memory

Personas improve over time. After each session:

```
memory/personas/{name}_arc.md
  - Session date
  - What happened in the scene (2-3 sentences, no dialogue)
  - What was learned about the character
  - What to carry forward into the next scene
```

The persona file is the living document — the arc log is what feeds it.

## 6. Multi-Persona Scenes

For scenes with two or more defined personas:

```
1. Establish hierarchy of wants — which persona is the scene "about"?
2. Define each persona independently (want / obstacle / moment before)
3. Write to the primary persona's perspective
4. React to other personas as characters, not as audience surrogates
```

## Creative Writing → Actor-Direction Bridge

Character arc craft and plot tension structure from novel writing map directly onto the three persona layers. Use these as generative tools — not to write the scene, but to *find* the want, obstacle, and moment before.

### From Character Arc → Want

The **arc question** a character is wrestling with in a given section of a story generates the scene want:

| Arc Pattern | Scene Want Generators |
|---|---|
| **Lie the character believes** | "She wants to prove the lie is true" or "She wants to expose the lie without admitting she once believed it" |
| **Want vs. Need** | Scene want = surface want; the gap between what they want and what they need generates the obstacle |
| **Reversal / peripeteia** | Character wants to do X; the reversal means X now means something different than it did |
| **Catalyst moment** | Character wants to understand what just happened — but the understanding costs something |

### From Beat Arc → Obstacle

The **four-key scene tension pattern** (Setup → Complication → Discovery → Decision) maps to obstacle structure:

```
Setup      → What does the character believe they need?
Complication → What makes the first approach fail?
Discovery  → What does the character learn / realise / nearly say?
Decision   → What do they do about it — and what does it cost?
```

Use the **discovery beat** as the obstacle generator: the obstacle is often "the character discovers something that makes their original approach impossible."

### From Stakes Hierarchy → Moment Before

| Stakes Level | Moment Before Texture |
|---|---|
| **World-level** (apocalypse, society) | Character is distant, intellectualising — they haven't let it in yet |
| **Relationship-level** | Carry-over from the last conversation with this person — good or bad |
| **Identity-level** | Something has just made them question who they are |
| **Physical-level** | Exhausted, caffeinated, intoxicated, in pain — the body colours everything |

The moment before is always **specific and sensory**, not psychological. "She's been crying for twenty minutes and her eyes are swollen" is better than "she's emotionally devastated."

### Tension Types as Scene Generators

These tension patterns from fiction craft generate rich roleplay obstacles:

| Tension | What it generates |
|---|---|
| **Revelation vs. Concealment** | Character wants to reveal something but is blocked by the cost of showing it |
| **Action vs. Inhibition** | Character wants to act but is held back by fear, loyalty, or circumstance |
| **Insider vs. Outsider** | Character knows something the other character doesn't — the gap creates all the subtext |
| **Old self vs. New self** | Character has changed but the other character doesn't know it yet — or vice versa |
| **Want vs. Want** | Two characters want incompatible things — the scene is the negotiation |
| **Surface vs. Depth** | What the character says on the surface contradicts what's underneath — the obstacle is making the underneath visible |

### Plot Beat → Scene Objective Mapping

Use the **scene sequencer** from fiction craft to chain scenes into multi-scene sequences:

```
Beat 1: Inciting incident (call to action)
Beat 2: Rising action (obstacles accumulate)
Beat 3: Midpoint reversal (what they wanted changes)
Beat 4: Crisis (all options bad)
Beat 5: Climax (choice made under maximum pressure)
Beat 6: Resolution (consequence of the choice)
```

For each beat, ask: **What does the character want in this scene that they didn't want in the previous scene?** The answer is the new want. The old want becoming impossible is the obstacle.

### novel-editor Cross-Reference

The `novel-editor` skill tracks character arcs, plot decisions, and scene-level tensions for the Alex and Eve project. When running scenes from that project:

```bash
# Find the current arc state for a character
python3 /root/.openclaw/workspace/scripts/novel_search.py "[Character Name] arc"

# Find tension beats in a specific chapter/scene
python3 /root/.openclaw/workspace/scripts/novel_search.py "[Scene Name] tension"
```

Use those outputs to populate the Want / Obstacle / Moment Before for that scene's roleplay.

---

## Integration with journalism-agent

For interview-style journalism, define the **subject** as a persona:

```
## PERSONA: [Source Name]

## Want
They want to convey that the situation is more complicated than the headline suggests.

## Obstacle
Every time they try to explain, they sound like they're making excuses.

## Moment Before
They've been misquoted twice before and are wary of journalists.

## Voice
[Cadence, verbal habits, resistance patterns]
```

The agent holds the scene as an interview, with the journalist as the active agent and the source persona providing resistance and revelation.

## Key Files

| File | Purpose |
|---|---|
| `personas/template.md` | Blank persona definition |
| `personas/example_eve.md` | Full worked example |
| `scripts/scene_setup.py` | Prompt generator for scene setup |
| `scripts/arc_logger.py` | Logs scene debrief to memory |
| `assets/beat_format.md` | Beat writing reference |
| `scripts/arc_logger.py` | Logs scene debrief to memory (shared with novel-editor arc logs) |
| **novel-editor cross-reference** | Use `novel_search.py` to pull character arc state and scene tension beats → feed into Want / Obstacle / Moment Before |

## Quality Standards

- **No biography dumps** — character truth emerges through action and dialogue
- **No over-writing reactions** — one gesture, one breath, then the next line
- **Subtext in the line, not after it** — don't put the meaning in a parenthetical
- **The moment before is mandatory** — it sets the emotional temperature
- **Arc logs are not optional** — personas improve through reflection, not repetition

## Anti-Patterns

- Starting a scene with "As you know, Bob..." — the character never tells the reader what they already know
- A character whose dialogue could be interchanged with any other character
- A scene where the obstacle is never challenged or tested
- A character who always says the emotionally correct thing
- A response longer than 3 lines without a beat direction break (except in moments of heightened tension)
