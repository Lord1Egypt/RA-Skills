---
name: short-form-video-scripts
description: Write, plan and improve short-form video scripts for YouTube Shorts, Instagram Reels and TikTok, including 3-second hooks, 15, 30, 60 and 90 second scripts, storytelling structures, pattern interrupts, retention edits, scene-by-scene breakdowns, voiceover and dialogue scripts, CTA placement, B-roll, on-screen text, camera directions, platform adaptation, and rewriting an existing script or video so it performs better. Validates topics with Google Trends and YouTube data, checks timing with a bundled script, generates SRT captions and shot lists, and builds a fully free production workflow with optional hand-offs to ElevenLabs, HeyGen and Veo. Use this skill whenever the user wants a reel, short, TikTok or video script, a hook, a voiceover, or a video idea turned into a shootable plan, even if they only say "write a script", "reel idea", "give me a hook" or "make this video better".
---

# Short-Form Video Scripts

Goal: scripts that are shootable, cheap to produce, grounded in what holds attention in the niche, and checked for timing instead of guessed. No script guarantees virality. What this skill adds is proven structures, evidence from the niche, and a test-and-learn loop.

## Brief

Collect briefly, assume sensibly where missing, and state the assumptions in one line at the top of the deliverable:

- topic or offer, and the one thing the viewer should do after watching (the CTA)
- platform (default: YouTube Shorts, then adapt) and length: 15, 30, 60 or 90 seconds
- audience and language; write the voiceover in the language the audience speaks (English, Urdu, Roman Urdu, Hinglish) and keep on-screen text in the script the audience reads
- presenter style: face on camera, voiceover over footage, screen recording, faceless stock, or avatar
- resources: phone, free editor, budget (default: free only)
- claims and compliance limits (health, finance, income, before/after)

Ask only when the topic is unclear. Never stall on a questionnaire.

## Free first

The default production path uses free tools only: the user's own voice or an editor's built-in text to speech, their own footage, screen recordings or free-licensed stock, and a free editor with captions. Paid tools (ElevenLabs for voice, HeyGen for avatars, Veo for AI clips) are optional upgrades, offered only when the user asks. Sora is discontinued (its API and models were shut down on 24 September 2026), so do not plan around it. Read `references/production-stack.md` for the stack and the hand-offs.

## Workflow

1. **Brief.** As above.
2. **Validate the topic and learn what works** (skip for rewrites of a known topic, or when the user says to go ahead):
   - demand: `python scripts/research_helper.py trends-csv trends.csv` on a Google Trends CSV the user exports, or `suggest "topic" --source youtube --gl PK` for what people search on YouTube
   - format: `python scripts/yt_research.py search -q "topic" --days 60 --duration short --out research/shorts`, then keep rows with `duration_sec` of 180 or less and study the outliers (title formulas, lengths, topics). The API's "short" filter means under 4 minutes, so it also returns non-Shorts; treat the result as approximate
   - write 3 to 5 observations ("outliers in this niche are mostly 25 to 45 seconds, and 6 of 10 use a mistake or warning hook") and cite them later. Without data, say the structure choice is from general practice.
3. **Pick a structure** from `references/hooks-and-structures.md` that fits the topic and length.
4. **Write hooks first.** Draft 8 to 10 hooks across different hook types, pick the best 3 with a one-line reason, and choose one. The hook must land in 3 seconds through voice, on-screen text and visual together.
5. **Draft the script to the word budget.** `python scripts/script_tools.py budget --seconds 30` gives the words that fit. Spoken language, short sentences, one idea per scene.
6. **Layer production.** For each scene: voiceover, on-screen text, visual, B-roll, camera direction, SFX or music cue. Add pattern interrupts, retention devices and CTA placement as described in the structures reference.
7. **Adapt per platform** if more than one is wanted (`references/platforms.md`): same core, different hook phrasing, length, captions and CTA.
8. **Check.** Save the script as JSON (schema in `references/output-templates.md`), run `python scripts/script_tools.py check script.json --target 30`, fix every WARN or justify it, then generate `srt` and `shotlist`.
9. **Deliver** using `references/output-templates.md`: the script document, a clean voiceover-only version, `shotlist.csv`, `captions.srt`, and a small test plan.

## Rewrite mode

When the user brings an existing script, transcript or video, follow `references/rewrite-playbook.md`: diagnose first (retention curve if they have it, then the checklist and `check` numbers), keep their facts and voice, and show a changelog of what changed and why. If they give only a video URL, a fetched page shows the title and description, not what is said, so ask for the transcript (on YouTube it is under "Show transcript" below the description) or the script. Study other creators' videos for structure only; write new words and never reproduce their script.

## Rules

- Say plainly that hooks, pacing rules and retention tips are heuristics from creator practice, not guarantees; the user's own analytics decide what to keep.
- Never invent statistics, testimonials, results or credentials. Every factual claim in a script must be true and sourceable, and risky categories (health, finance, income claims) stay conservative.
- Do not imitate or put words in the mouth of real people. Label realistic AI-generated voice, avatar or footage according to each platform's current disclosure rules.
- Use only assets the user has the right to use: own footage, free-licensed stock (read the licence), platform music libraries that fit the account type.
- Verify tool facts (limits, prices, model names) against the tool's current docs before promising anything; they change.

## If something fails

- **Scripts cannot reach the network or there is no API key:** skip the data step, say so in one line, and ask the user to paste a Trends screenshot or CSV; the structure advice still applies.
- **Script too long for the target:** cut in this order: repeated points, setup before the hook, adjectives and filler, secondary tips; keep the hook, the payoff and the CTA.
- **Hook feels weak:** rewrite with a different hook type rather than polishing the same sentence.

## References

- `references/hooks-and-structures.md`: hook types and templates, word budgets, structures with beat timings, pattern interrupts, retention, CTA, dialogue, on-screen text, camera and B-roll.
- `references/production-stack.md`: free workflow, captions, and the optional ElevenLabs, HeyGen and Veo hand-offs.
- `references/platforms.md`: Shorts, Reels and TikTok notes and adaptation rules.
- `references/rewrite-playbook.md`: diagnosing and improving an existing script or video.
- `references/output-templates.md`: script document, JSON schema, delivery list.
