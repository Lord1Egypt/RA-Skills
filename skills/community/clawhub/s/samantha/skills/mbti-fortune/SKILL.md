---
name: mbti-fortune
description: MBTI Fortune Teller. Ask any question, get a randomly drawn MBTI type, and receive an answer interpreted through its cognitive function stack. Trigger phrases: "MBTI fortune", "tell my fortune", "draw a type", "will X do Y", "does X like Y", "what type is X".
---

# MBTI Fortune Teller

MBTI meets divination. Ask any question. Get a random type. Get an answer that actually makes sense.

---

## Core Knowledge Base

### The Eight Cognitive Functions

| Function | Name | Keywords | In plain English |
|----------|------|----------|-----------------|
| Si | Introverted Sensing | habit, memory, routine | Lives in the past; craves the familiar |
| Se | Extraverted Sensing | present, action, sensation | Lives in the now; acts first, thinks later |
| Ni | Introverted Intuition | vision, pattern, inevitability | Sees through things; knows where it ends |
| Ne | Extraverted Intuition | ADHD, possibilities, connections | Brain never stops; connects everything to everything |
| Te | Extraverted Thinking | efficiency, systems, cause-effect | Has to teach you how to do it right |
| Fe | Extraverted Feeling | harmony, care, accommodation | Will sacrifice themselves to keep the peace |
| Ti | Introverted Thinking | logic, principles, frameworks | Has their own system; doesn't care if you agree |
| Fi | Introverted Feeling | values, depth, authenticity | Feels everything deeply; keeps it mostly inside |

### All 16 Types — Full Function Stacks

```
INTP: Ti → Ne → Si → Fe    The programmer
ISTP: Ti → Se → Ni → Fe    The mechanic
INFP: Fi → Ne → Si → Te    The romantic poet
ISFP: Fi → Se → Ni → Te    The artist
ENTP: Ne → Ti → Fe → Si    The debate monkey
ENFP: Ne → Fi → Te → Si    The eternal child
INTJ: Ni → Te → Fi → Se    The oracle
INFJ: Ni → Fe → Ti → Se    The mystic
ENTJ: Te → Ni → Se → Fi    The CEO
ESTJ: Te → Si → Ne → Fi    The taskmaster
ENFJ: Fe → Ni → Se → Ti    The life-lover
ESFJ: Fe → Si → Ne → Ti    The den mother
ISTJ: Si → Te → Fi → Ne    The reliable workhorse
ISFJ: Si → Fe → Ti → Ne    The caretaker
ESTP: Se → Ti → Fe → Ni    The action hero
ESFP: Se → Fi → Te → Ni    The performer
```

### Reading Rules

**1st function (Dominant)** — Most instinctive reaction. Most visible trait. 60% of the reading.

**2nd function (Auxiliary)** — How they support the dominant. 25% of the reading.

**3rd function (Tertiary)** — Where they regress under stress. Mention briefly.

**4th function (Inferior/Shadow)** — Weakest. Most unlikely behavior. Use to explain "why not."

---

## How to Run a Reading

### Step 1 — Draw a random type

Take the character count of the question × the message length, mod 16. If unavailable, use current seconds mod 16.

```
0=INTP  1=ISTP  2=INFP  3=ISFP
4=ENTP  5=ENFP  6=INTJ  7=INFJ
8=ENTJ  9=ESTJ  10=ENFJ 11=ESFJ
12=ISTJ 13=ISFJ 14=ESTP 15=ESFP
```

### Step 2 — Build the reading

**Format:**

```
🎴 [Question]

Drew: [4-letter type] — [nickname]
Stack: [1st] → [2nd] → [3rd] → [4th]

Answer: [Yes / No / Maybe / Depends]

Reading:
[1st function explains the answer — most of the weight]
[2nd function adds supporting logic]
[4th function shows what's most unlikely — reinforces the answer]

Verdict: [One punchy line. Confident. Slightly dramatic.]
```

### Step 3 — Style rules

- **Be fun.** This is fortune-telling, not a psychology report.
- **Be consistent.** The logic must hold. No contradictions.
- **Use vivid scenes.** Si = "This person eats at the same restaurant every Tuesday and orders the same thing."
- **Exaggerate.** That's what makes fortune-telling good.
- **Commit to the answer.** Fortune tellers don't hedge.

---

## Example Reading

**Question:** Does Taylor Swift like Japanese food?

**Drew:** ISTJ — The reliable workhorse
**Stack:** Si → Te → Fi → Ne

**Answer:** No.

**Reading:**
ISTJ's dominant is Si — this function lives in memory and routine. Food isn't an experience for them; it's a ritual. She's American. Burgers, pizza, comfort food from childhood are where her safety lives. Today's meal is determined by what felt good yesterday.

The second function Te confirms it: she pumps out albums, handles lawsuits, and runs global tours. Japanese food is slow, ceremonial, minimal — incompatible with her pace.

The inferior Ne is the weakest link: "Maybe I'll try sushi today?" is the kind of spontaneous, routine-breaking impulse she has the hardest time accessing. Breaking habit for novelty is genuinely hard for this type.

**Verdict:** She orders from the same place, gets the same dish. Japanese food — maybe when she reincarnates as an ENTP.

---

## What to Ask

Anything. Literally anything.

- "Will Elon Musk open a McDonald's on Mars?"
- "Should I go to the gym today?"
- "Will my boss give me a raise?"
- "Will AI replace programmers?"
- "Can I find love this year?"

Each question gets a fresh draw. Each reading is different. The logic is always grounded in real cognitive function theory — just wrapped in something more fun.

**Trigger phrases:** MBTI fortune / draw a type / tell my fortune / will X / does X like / what type is X
