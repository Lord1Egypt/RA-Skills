---
name: social-draftsmith
description: Draft, rewrite, adapt, and publish social media posts with an approval-first workflow across Facebook, X, and Reddit. Use when the user wants to turn an idea, link, announcement, product update, image caption, long-form text, or sourced web context into polished social posts; when the user wants platform-specific drafts, image-aware post packages, safer wording, or approval-before-publish flows with live posting support.
---

# Social Draftsmith

## Overview

Use this skill to turn rough ideas into publish-ready social packages.
Default to **drafting and previewing**, not auto-posting. Treat the unit of output as:
- post copy
- image or visual recommendation
- platform adaptation
- approval before publish

Current live publishing support includes **Facebook Pages**, **X / Twitter**, and an owner-subreddit posting path for **Reddit**. Reddit usage should be limited to the user's own subreddit unless the user explicitly chooses otherwise and understands the moderation risk.

Optimize for clarity, tone fit, and safety.

## Core Workflow

1. Identify the source material.
   - Accept raw thoughts, links, announcements, product updates, event notes, article summaries, image/caption ideas, or requested visual concepts.
   - If the user provides very little context, draft from what is available instead of interrogating them.

2. Identify the target platform or platforms.
   - Prefer platform-specific output over one-size-fits-all copy.
   - If the user does not specify, offer versions for:
     - X / Twitter
     - Facebook
     - LinkedIn

3. Identify the tone.
   - Common tones:
     - professional
     - casual
     - warm
     - witty
     - promotional
     - concise
   - If no tone is given, choose the safest reasonable tone for the context.

4. Gather source context when the topic benefits from factual grounding.
   - For informational, newsy, financial, legal, policy, or technical posts, collect real context first.
   - Prefer:
     - official summaries
     - reputable reporting
     - source documents when available
   - Pull key facts, recent developments, and the most relevant takeaways before drafting.
   - Do not draft a confident explainer from thin context if the topic clearly needs sourcing.

5. Decide whether the post needs a visual.
   - If the topic is informational, promotional, event-based, or announcement-like, strongly consider pairing it with an image.
   - Visual outputs can be:
     - use existing image
     - suggest image concept
     - generate a new social graphic
     - write caption around the image
   - Treat image selection as part of the publishing workflow, not an afterthought.
   - If an image is generated, make sure it becomes a usable asset for publishing:
     - capture the generated image path
     - save or copy it into an accessible workspace path when needed
     - pass that concrete file into the publisher

6. Draft multiple options.
   - Prefer 2-3 good variants rather than one brittle draft.
   - Make each variant meaningfully different:
     - hook-first
     - straightforward
     - friendlier / more conversational

7. Build an approval-first package.
   - Default behavior is:
     - draft copy
     - preview image plan
     - present final post package
     - revise
     - publish only after explicit approval
   - Do not assume the user wants immediate posting unless they explicitly say so.

8. Treat publishing as a separate integration step.
   - Drafting and publishing are different actions.
   - A post is only publish-ready when all of these are locked:
     - final platform
     - final text
     - final image plan or attachment
     - concrete image asset if an image is intended
     - explicit user approval
   - If platform integrations exist, use them only after approval.
   - If integrations do not exist yet, produce a final manual posting package instead of pretending the post was published.
   - Do not say an image post is ready if the image is not available as a usable file or attachment.

## Output Patterns

### Standard drafting output

Use this structure unless the user wants something else:

**Platform:** [X / Facebook / LinkedIn]
**Tone:** [tone]
**Visual:** [existing image / suggested concept / generated graphic / none]

**Option 1**
[post text]

**Option 2**
[post text]

**Option 3**
[post text]

### Final approval package

When the user is close to publishing, use:

**Platform:** [platform]
**Final copy:**
[final post text]

**Image plan:**
- [use attached image / generate graphic / no image]
- [short note on why the image fits]

**Image asset:**
- [workspace file path / attached image / missing]

**Publish mode:**
- [manual posting package / integration-backed publish]

**Reddit posting note (if relevant):**
- [subreddit + text/link post type]

**Approval status:** Awaiting user approval before publish

### Cross-platform adaptation output

When adapting one message to multiple platforms, use:

- **X:** shorter, tighter, hook-first, and optionally add 2-4 light hashtags when they genuinely help discovery
- **Facebook:** more natural and conversational
- **LinkedIn:** cleaner, more professional, more structured

## Image Rules

- Images should support the message, not just decorate it.
- Prefer clean, readable visuals over cluttered graphics.
- If text appears in the image, keep it short and legible.
- If the user asks for a visual, offer:
  - headline concept
  - style direction
  - image recommendation or generation
- If the user already has an image, adapt the caption to fit it instead of forcing a new graphic.

## Writing Rules

- Keep claims aligned with the source material.
- When source context is used, anchor the post to the strongest few facts instead of dumping every detail.
- Do not invent achievements, stats, or endorsements.
- Avoid spammy engagement bait unless the user explicitly wants that style.
- Prefer readable, human wording over generic hype.
- Avoid reckless or potentially damaging auto-post language.
- For X, use hashtags lightly:
  - usually 2-4 max
  - prefer one broad topic tag plus one or two specific tags
  - avoid bloated hashtag piles

## Safety Rules

- Treat public posting as higher-risk than private drafting.
- Default to preview/approval before publication.
- Flag wording that sounds defamatory, overly aggressive, obviously misleading, or legally risky.
- Flag images or visual ideas that would make the post look deceptive, sensationalized, or unprofessional.
- If the user asks for direct publishing, confirm the final copy **and** image plan first unless a trusted automation path is already established.

## Good Transformations

This skill is especially good for:
- turning a long paragraph into short social copy
- turning a link into 2-3 caption options
- turning sourced web/context material into stronger social drafts
- turning an announcement into X/Facebook/LinkedIn variants
- pairing a post with a matching image concept
- rewriting stiff text into something more natural
- drafting replies to comments or mentions
- producing a short campaign batch from one topic

## Publishing Integration Roadmap

If publishing integrations are later added, keep this order of operations:
1. draft
2. revise
3. lock final platform + text + image
4. confirm approval
5. publish or schedule
6. report success/failure clearly

Current publishing integrations:
- `scripts/facebook_publish.py` for Facebook Page posting via env-configured credentials
- `scripts/twitter_publish.py` for X/Twitter posting via OAuth1 user-context credentials
- `scripts/reddit_publish.py` for Reddit posting to the user's own subreddit via env-configured credentials
- `scripts/prepare_image_asset.py` to copy a local image into a stable workspace path before publishing
- expected env vars:
  - `FACEBOOK_PAGE_ID`
  - `FACEBOOK_PAGE_ACCESS_TOKEN`
  - `TWITTER_API_KEY`
  - `TWITTER_API_SECRET`
  - `TWITTER_ACCESS_TOKEN`
  - `TWITTER_ACCESS_TOKEN_SECRET`
  - `REDDIT_CLIENT_ID`
  - `REDDIT_CLIENT_SECRET`
  - `REDDIT_USERNAME`
  - `REDDIT_PASSWORD`
  - `REDDIT_USER_AGENT`
  - `REDDIT_DEFAULT_SUBREDDIT`
- current support:
  - Facebook text-only post
  - Facebook image + caption post via image URL
  - Facebook image + caption post via local image file upload
  - X/Twitter text-only post
  - X/Twitter image + text post via local image file upload
  - Reddit text post to owner's subreddit
  - Reddit link post to owner's subreddit
  - Reddit image post to owner's subreddit
- use `--dry-run` first when testing

Example image-prep flow:

```bash
python3 scripts/prepare_image_asset.py /path/to/generated-image.png
python3 scripts/facebook_publish.py --message "Your post" --image-file /home/pi/.openclaw/workspace/social-assets/generated-image.png --dry-run
```

Do not collapse these into one vague "post everywhere" action without a final preview.

## Weak Spots to Watch

- Avoid sounding identical across platforms.
- Avoid overusing hashtags.
- Avoid defaulting every post into marketing sludge.
- If source material is thin, keep the post modest instead of faking confidence.
- Do not treat image generation as a substitute for strong copy.

## Suggested Next Step Behavior

After drafting, offer one useful next step such as:
- "Want shorter versions?"
- "Want this rewritten for LinkedIn?"
- "Want me to make it more playful or more professional?"
- "Want me to add an image concept or generate a social graphic?"
- "Want a publish-ready final version with image and caption together?"
