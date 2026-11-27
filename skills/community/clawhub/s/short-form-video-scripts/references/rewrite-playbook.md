# Rewrite playbook: improving an existing script or video

The aim is a better version of the user's own idea, in their voice, with their facts. Diagnose before touching anything.

## 1. Intake

Ask for, or look for, in this order:
1. the script or transcript (pasted text; on YouTube it is under "Show transcript"). A video URL alone shows only the title and description
2. the goal and the platform
3. the retention graph or analytics, if the video is already live: where viewers drop off is the best diagnostic. Ask for a screenshot or the timestamps of the biggest drops
4. how it performed compared with their usual videos

## 2. Diagnose

Run `python scripts/script_tools.py check script.json` after converting the text into scenes (split at natural visual changes). Then score each area from 1 to 5 and note evidence from the text:

| Area | Questions |
|---|---|
| Hook | Does it promise something specific in the first 3 seconds? Does it start with a greeting or setup? |
| Promise and payoff | Does the video deliver what the hook promised, and when? |
| Pacing | Long scenes, long sentences, dead air, places with no change for more than 5 seconds? |
| Redundancy | Repeated points, filler, intro and outro padding? |
| Specificity | Real numbers, names, examples, or only general advice? |
| Structure | Does it follow a clear shape (see the structures reference)? |
| CTA | One clear, specific action, placed after the payoff? |
| Language | Spoken and natural, or written and stiff? |
| Visual plan | Does each scene have something to see? On-screen text for muted viewing? |

If the retention graph shows a drop at a given second, link it to the scene at that time and treat that scene as the first suspect.

## 3. Rewrite

- Keep every fact, number and claim the user supplied. Do not add claims. Flag any claim that looks unsupported or risky and ask the user to confirm it.
- Keep their voice: vocabulary, language mix, humour level.
- Move the strongest result or promise to the front; cut setup.
- Write 3 alternative hooks of different types and recommend one.
- Cut filler and repeated points; shorten sentences.
- Add pattern interrupts and a re-hook where the diagnosis showed attention would sag.
- Fix the CTA: one action, after the payoff.
- If asked, produce length variants (for example the 60-second script cut to 30 seconds, keeping the hook, the payoff and the CTA).

## 4. Deliver a changelog

Give the new script plus a table:

| Change | Before | After | Why |
|---|---|---|---|

Keep it to the changes that matter (6 to 10 rows). End with what to test: the hook variant, the length, or the CTA, with the metric that decides it and how many posts to compare.

## 5. Other creators' videos

If the user shares someone else's transcript as a model, extract the structure (hook type, beats, timing, CTA) and write a new script with different words, examples and angle. Do not reproduce or lightly reword their script.
