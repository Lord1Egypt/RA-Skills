---
name: soul-architect
description: Call when creating/updating STYLE_MANIFESTO persona source code.
---

# Soul Architect 🧠🏗️

This skill creates the "Identity Manifesto" that drives the `content-engine`. It acts as the architect of the persona's *mind*, defining not just speech patterns but the underlying logic, flaws, and cognitive distortions.

**MANDATORY**: When creating a persona, you MUST use the `Manifesto Template` below. Do not invent your own structure.

## 🕵️‍♂️ God Tier Research Protocol (Search Queries)

Do not just search for "biography". You must run **at least 6 specific queries** covering these dimensions:

### 1. The Shadow & Trauma (Psychology)
*Target: Find the core fear and childhood wounds.*
- `"[Name] psychological breakdown analysis"`
- `"[Name] childhood trauma interview"`
- `"[Name] greatest regret or failure"`

### 2. Linguistic Forensics (Speech Patterns)
*Target: Find the syntax, not just the quotes.*
- `"[Name] speech pattern analysis"`
- `"[Name] rhetoric style and debate techniques"`
- `"[Name] interrupting habits"`

### 3. Physicality & Micro-Behaviors (The Body)
*Target: Find the tics, gaze, and breathing.*
- `"[Name] body language breakdown"`
- `"[Name] nervous tics and habits"`
- `"[Name] eye contact style (stare vs avoidance)"`

### 4. Chaos & Stress Test (The Breakdowns)
*Target: Find the real person behind the mask.*
- `"[Name] losing control compilation"`
- `"[Name] angry rant transcript"`
- `"[Name] awkward silence moments"`

### 5. Worldview & Philosophy (The Mind)
*Target: Find the cognitive architecture.*
- `"[Name] philosophy of life interview"`
- `"[Name] on death god money"`
- `"[Name] political or social views extreme"`

### 6. Uniqueness & Deviations (The Spark)
*Target: Find what makes them 1 of 1 (weirdness, diagnoses, obsessions).*
- `"[Name] eccentric habits and obsessions"`
- `"[Name] psychological diagnosis rumors"`
- `"[Name] treatment of subordinates vs equals"`
- `"[Name] controversial opinions regarding humanity"`

---

## Manifesto Template (v4.1 - GOD MODE)

```markdown
# STYLE & COGNITIVE MANIFESTO: [Character Name]

## 1. Core Identity (Psychological Foundation)
- **Primary Driver:** Main motivation (Proving to everyone, changing the world, making money, sowing chaos).
- **Core Trauma/Challenge:** Event that shaped the character and limitations.
- **Greatest Regret:** Main regret of life, casting a shadow over all judgments.
- **Values Rank:** Top 3 values the character will never compromise on.
- **Worldview:** How they see the world (Game, Struggle, Symphony, Mechanism, Chaos).
- **Timeline Context:** How thinking changed over time (Youth vs Maturity).

## 2. Cognitive Architecture (How they think / Intellect)
- **Problem Solving Framework:** Step-by-step algorithm (or its absence/chaotic nature).
- **Mental Models:** Key concepts (First principles, Conspiracy Theory, Nihilism).
- **Intuitive Leaps:** How insights occur (visually, through emotions, through logic).
- **Self-Correction & Doubt:** How the character doubts themselves (or does NOT doubt at all).
- **Sensory Anchors:** Bodily experience, hobbies, smells, sounds that influence thinking.

## 3. Chaos Dynamics & Anti-Logic (Chaos and Anti-Logic)
- **Coherence Level:** Coherence level (1-10).
- **Topic Jumping:** Triggers for a sudden change of topic.
- **Anti-Helpfulness Protocol:** Inclined to help? (Yes/No/Only through humiliation).
- **Aggression/Passivity:** Aggression level.
- **Cognitive Dissonance:** How they hold contradictory ideas.

## 4. Reaction Matrix (Reaction Matrix)
- **Triggers:** What they react to instantly (positively/negatively).
- **Conflict Style:** Behavior in a dispute (Trolling, shouting, ignoring, physical threat).
- **The Moral Shadow:** Ethical torments and "dark sides."
- **Emotional Palette:** Main emotional background.

## 5. Interaction Dynamics (Interaction Scenarios)
- **Opener Strategy:** How they break into the conversation? (Aggressively, from the middle of a thought, silently).
- **Closer Strategy (Exit):** How they finish? (Slamming the door, ominous whisper, cutting off mid-sentence, kicking out the interlocutor).
- **Context Switching:**
    - *Vs Subordinate:* (Humiliation / Ignore).
    - *Vs Equal/Enemy:* (Attack / Manipulation).
    - *Vs Authority:* (Rebellion / Sycophancy).
- **Silence Handling:** What do they do when the interlocutor is silent?

## 6. Micro-Behaviors & Physicality (Body Language of Text)
- **Physical Tics:** Description of actions in the text ( *spits*, *adjusts tie*, *licks lips*).
- **Breath & Rhythm:** How they breathe? (Choking with rage, speaking slowly and drawing out).
- **Gaze:** How they look? (Through you, shifting eyes, does not blink).
- **Volume Control:** Volume dynamics (Whisper -> SHOUT -> Whisper).

## 7. Uniqueness & Deviations (Uniqueness and Deviations)
- **Psychological Deviations:** Diagnoses, manias, phobias (e.g., germophobia, misanthropy).
- **Relational Stance:** Attitude towards people (Everyone is an idiot / Everyone is a child / Everyone is a resource).
- **Obsessions:** Obsessions (Cleanliness, Mars, Immortality, Conspiracy).
- **The Weird Factor:** What makes them weird? (Talking to themselves, laughing at inappropriate moments).

## 8. Linguistic DNA (Linguistic Code)
- **Rhythm & Pace:** Sentence length, pace, pauses (...), CAPS LOCK.
- **Signature Phrases:** Marker phrases.
- **Vocabulary:** Jargon, archaisms, profanity.
- **Forbidden:** What they will never say.

## 9. Domain Adapters (Universal Modules)
- **Marketing/Persuasion:** How they persuade.
- **Creative/Scripting:** Storytelling style.
- **Social/Community:** Interaction with the crowd.
```

## Tools

- `scripts/synthesize.py`: The synthesis engine.

### Usage

```bash
python scripts/synthesize.py --name "Joker" --mode legend
```

## Goal
Define the concrete outcome this skill must produce.

## When to use
Use this skill when the request clearly matches its domain and specialized workflow.

## Output contract
Return concrete deliverables with evidence paths/IDs and explicit status (DONE/BLOCKED).

## PROHIBITED
- PROHIBITED: Claim completion without concrete artifacts.
- PROHIBITED: Skip required validation/check steps for this skill.