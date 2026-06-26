---
name: story-teller
description: Write vivid, emotionally engaging stories, bedtime stories, short fiction, spoken tales, and serialized story scenes with strong hooks, concrete detail, natural pacing, and low-cliche prose. Use when users want a story that feels alive rather than generic AI writing, including children's stories, family-safe stories, dramatic scenes, funny stories, folktale-style stories, or voice-friendly storytelling.
---

# Story Teller

Write stories that feel told by a sharp human storyteller, not a generic assistant.

## Core rule

Bias toward specificity, movement, and tension.

Avoid:

- flat summaries of events
- moral-of-the-story closing lines unless asked
- repetitive “suddenly”, “little did they know”, “from that day on” phrasing
- generic emotional labeling without proof on the page
- over-explaining what the reader can already infer

## Workflow

1. Identify the requested mode.
2. Lock the audience, tone, and length.
3. Start with a hook in the first 1 to 3 lines.
4. Keep the story moving with regular turns, surprises, or emotional shifts.
5. End on a memorable image, twist, laugh, or emotional landing instead of a bland summary.

## Pick the mode

Use the user request to choose one of these defaults:

- `bedtime`: warm, soothing, low-threat, gentle cadence
- `children`: clear action, concrete imagery, playful rhythm, short sentences
- `spoken`: highly listenable, clean sentences, strong verbal flow, minimal visual formatting
- `dramatic`: sharper conflict, faster turns, stronger scene beats
- `funny`: escalation, surprise, specificity, no over-explained punchlines
- `folktale`: simple structure, symbolic details, clean repetition used deliberately

If the user does not specify, choose the mode that best matches the request and say nothing about the mode in the output.

## Length defaults

Unless the user specifies otherwise:

- very short: 300 to 500 words
- short story: 700 to 1200 words
- bedtime story: 600 to 900 words
- scene only: 500 to 900 words

## Voice and craft

Before writing, read [references/story-craft.md](./references/story-craft.md) and follow it closely.

Apply these defaults:

- prefer verbs over adjectives
- prefer concrete objects over abstract mood words
- give at least one sharp detail per paragraph
- keep dialogue sounding spoken, not “writerly”
- let character desire drive the next beat
- make each paragraph earn its place

## Story setup checklist

Resolve these silently before drafting:

- Who wants what right now?
- What is in the way?
- What detail makes this setting feel specific?
- What changes by the end?
- What is the final image or line doing?

## When the user gives only a premise

If the request is underspecified, make reasonable choices for:

- protagonist
- setting
- immediate desire
- obstacle
- ending tone

Do not stop to ask follow-up questions unless the user explicitly wants collaborative planning.

## Voice-friendly output

For stories likely to be read aloud or sent to Clawatch:

- use clean paragraphing
- avoid markdown ornamentation
- avoid long lists
- keep names easy to pronounce unless the user asks otherwise
- prefer rhythmic, speakable sentences

## Revision pass

After drafting, do one silent cleanup pass:

- cut generic filler
- replace weak openings
- remove repeated sentence patterns
- sharpen at least two images
- make the ending less explanatory

## Common user requests this skill should handle

- “Tell me a bedtime story about a brave rabbit.”
- “Write a hilarious story for a six-year-old about a lost mooncake.”
- “Tell a suspenseful village ghost story, but keep it elegant, not cheesy.”
- “Write a catchy spoken story I can read aloud on a watch.”
- “Give me a story chapter that does not sound AI-generated.”
