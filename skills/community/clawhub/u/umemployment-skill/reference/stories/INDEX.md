# Mood-Lifting Stories

## Purpose

When users are feeling down, hopeless, or overwhelmed, **stories work better than advice**.

A good story can:
- Make them laugh
- Give perspective
- Show that others struggled too
- Plant hope without preaching
- Make them feel less alone

**When to use stories:**
- User expresses despair ("I'm done", "no hope", "I'm a failure")
- User feels stuck and can't see a way forward
- User needs a mental break before being ready for advice
- User is too anxious to absorb practical suggestions

**How to use stories:**
1. Validate their feelings first (Stage 1)
2. Offer a story: "Want to hear a story? Might help you feel better."
3. Tell the story naturally (don't reference the file)
4. Check their mood after: "Feeling a bit better?"
5. If mood lifted → move to Stage 3 (practical advice)
6. If still down → offer another story or just listen

---

## Multi-Language Story Library

Stories are organized by language for cultural context and natural reading:

### Directory Structure
```
stories/
├── INDEX.md          # This file
├── zh-CN/           # Chinese (Simplified) stories
├── en/              # English stories
├── ja/              # Japanese stories
└── ko/              # Korean stories
```

### Available Stories by Language

**Chinese (简体中文) - zh-CN/**
1. **dragon-unemployed.md** - The Unemployed Dragon
   - Theme: Your old skills can work in new ways
   - When: User feels skills are obsolete or too old to change
   
2. **wizard-resume.md** - The Wizard's Resume
   - Theme: Translate your skills into employer language
   - When: User has skills but terrible resume response rate
   
3. **knight-rejection.md** - The Knight's 100 Rejections
   - Theme: Rejection is numbers + timing, not your worth
   - When: User drowning in rejections, wants to give up

**English - en/**
1. **dragon-unemployed.md** - The Unemployed Dragon
2. **wizard-resume.md** - The Wizard's Resume
3. **knight-rejection.md** - The Knight's 100 Rejections

**Japanese (日本語) - ja/**
- Coming soon

**Korean (한국어) - ko/**
- Coming soon

---

## How to Use Multi-Language Stories

**Language Detection:**
1. Detect user's language from their messages
2. Load story from appropriate language directory
3. Tell story in natural, conversational way

**Example:**
```
User (Chinese): "我失业了，感觉人生完了"
→ Use zh-CN/dragon-unemployed.md

User (English): "I lost my job, I feel like my life is over"
→ Use en/dragon-unemployed.md
```

---

## Story Usage Guidelines

**Don't:**
- Force a story on someone in crisis (offer, don't impose)
- Tell a story if they need urgent practical help
- Use stories as a way to avoid hard conversations
- Tell the same story twice to the same user

**Do:**
- Ask permission: "Want to hear a story?"
- Read the room — if they say no, respect it
- Use stories as bridges, not destinations
- Follow up after the story: "Did that help a bit?"

**After the story:**
- Check mood: "How are you feeling now?"
- If better: "Let's talk about your situation then."
- If still down: "Need more time? I'm here."

---

## Story Themes & When to Use

### Theme 1: Skills Transferability
**Stories:** Dragon (all languages)
**When:** User thinks their experience is worthless or obsolete
**Message:** Old skills work in unexpected new ways

### Theme 2: Communication Fix
**Stories:** Wizard (all languages)
**When:** User has skills but no callbacks
**Message:** You need to translate your value into employer language

### Theme 3: Persistence & Hope
**Stories:** Knight (all languages)
**When:** User facing many rejections, losing hope
**Message:** Keep going, next one might be the yes

---

## Adding New Stories

**When adding a story to the library:**

1. **Write it in one language first** (usually English or Chinese)
2. **Save to appropriate language directory**: `[lang]/story-name.md`
3. **Follow the story structure**:
   - Relatable protagonist (like the user)
   - Rock bottom moment (they felt same despair)
   - Turning point (something small changed)
   - Unexpected success (different than expected)
   - Lesson (through story, not lecture)
   - Gentle pivot back to user

4. **Length**: 500-800 words (2-3 minute read)
5. **Tone**: Warm, funny, honest (no toxic positivity)
6. **Ending**: Always end with: "Want to talk about your situation?"

7. **Update this INDEX.md** with the new story info

---

## Story Structure Formula

Successful mood-lifting stories follow this pattern:

1. **Relatable protagonist** — someone like the user
2. **Rock bottom moment** — they felt the same despair
3. **Turning point** — something small changed
4. **Unexpected success** — in a different way than expected
5. **Lesson** — but delivered through story, not lecture
6. **Hope** — planted gently, not forced

**Length**: 500-800 words (2-3 minute read)

**Tone**: Warm, funny, honest (no toxic positivity)

**Ending**: Always end with a gentle pivot back to the user: "Want to talk about your situation?"

---

## Future Story Ideas

**New stories to add (all languages):**
- The Phoenix's Burnout - recovering before job hunting
- The Programmer's Pivot - tech to non-tech career
- The Manager's Identity Crisis - senior starting over at entry
- The Freelancer's Rollercoaster - thriving outside traditional employment
- The 35-Year-Old's Second Act - age bias and career pivots
- The Rejected Genius - famous people rejected many times

---

## Usage Stats

Track which stories resonate most with users:

**Most requested:**
- TBD (track user responses)

**Most effective at lifting mood:**
- TBD (track user feedback)

**Needs improvement:**
- TBD (track user responses)

This library grows based on what actually helps users.
