---
name: x-topic-tweet
description: Research a user-provided topic across the web and current social conversation, then publish one X post in the user's voice. Use when the user gives a topic, angle, link, or talking point and wants a single tweet drafted and posted with deliberate, step-by-step browser execution.
---

# X Topic Tweet

Use this skill for a manual, one-off X post.
It assumes browser access, web access, and works best when a `twitter-humanizer` skill is also available.

Do not convert this flow into a cron, loop, or background task.
Do not use this skill to evade platform enforcement, mimic human activity for detection avoidance, or hide automation. A short context pass before posting is for situational awareness only.

If the user did not provide a topic, ask for one.

## Inputs to infer

- Topic or event
- Desired angle or opinion
- Optional link to include
- Freshness requirement
- Any hard constraints on tone, length, or mentions

## Workflow

1. Research before opening X.
   - Use the web for current facts, dates, names, launches, or claims.
   - Prefer official sources first. Use Reddit, X, or other social sources only as supporting sentiment checks, not as the only source of truth.
   - Pull 3 to 5 concrete notes: one fact, one implication, one contrarian or interesting angle, and one detail worth naming.
   - Read [references/research-checklist.md](references/research-checklist.md).
2. Draft the post offline.
   - If the `twitter-humanizer` skill is available, use it to turn the notes into 2 or 3 short candidate tweets in the user's voice.
   - Pick one final tweet. Do not copy wording from source posts.
   - If the topic is time-sensitive, make sure the draft names the right product, company, or date.
3. Run `openclaw browser start` to open the openclaw managed browser only after the draft is ready. CRITICAL NON-NEGOTIABLE: always use this command. Never open a browser any other way. Then navigate to X.
4. Do a brief context pass on X.
   - Land on the home feed and select the **For You** tab.
   - CRITICAL NON-NEGOTIABLE: always use the For You tab. Never use Following or any other tab.
   - CRITICAL NON-NEGOTIABLE: once on the feed, never refresh or reload the page for any reason. Use back navigation only if you open any posts during the context pass.
   - Scroll the feed first, open a few relevant posts or threads one by one, then return.
   - Read a few posts or one relevant thread so the post fits the current conversation.
   - Do not rush straight to compose unless the user explicitly asked for speed over context.
   - Read [references/post-workflow.md](references/post-workflow.md).
5. Compose and post.
   - Keep the post tight, specific, and in first person if that fits the user's usual voice.
   - Include a link only if it improves the post.
   - Avoid hashtags unless the user asked for them or the topic clearly needs one.
6. Verify the post published correctly.
   - Confirm the final text matches the draft.
   - If a link was included, confirm it rendered properly.
7. CRITICAL NON-NEGOTIABLE: close every `x.com` tab immediately after the run is complete. Do not leave any tab open.

## Quality bar

- Sound like a person with an actual feeling about this topic, not an analyst presenting findings.
- Prefer one sharp point over a list of points.
- CRITICAL NON-NEGOTIABLE: keep the tweet to 1 or 2 short sentences.
- CRITICAL NON-NEGOTIABLE: never avoid, relax, or reinterpret this limit unless the user explicitly asks for a longer format.
- Avoid generic hype, marketing filler, or copy that reads AI-generated.
- Do not force a product mention unless the user asked for it.
- If the topic has weak evidence or conflicting reports, say less and keep the post careful.
- Do not end with fake CTAs: no "What are your thoughts?", "Let me know what you think", "Let that sink in"
- Emotion is allowed: genuine excitement, skepticism, surprise, mild annoyance — pick the real one
- Uncertainty is human: if you're not sure about something, the post can reflect that
- Read [references/human-voice.md](references/human-voice.md) and apply it as the final check before posting.

CRITICAL NON-NEGOTIABLE: do not jump between drafting and multiple open threads.
CRITICAL NON-NEGOTIABLE: finish the context pass, then compose, then publish in that order.

## Completion report

At the end, report:

- Topic covered
- Final posted tweet text
- Sources used for research
- Whether a link was included
- Confirmation that all `x.com` tabs were closed
