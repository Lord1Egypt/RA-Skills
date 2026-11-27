---
name: social-media-content
description: Create platform-native social media content (Instagram captions and carousels, LinkedIn posts, X posts and threads, Facebook, Threads, TikTok and YouTube Shorts captions, Pinterest, Bluesky) from an idea, topic, product or long piece, in the brand's voice. Covers hooks, post structure, CTAs, hashtags, alt text, visual briefs, repurposing one idea into many formats, reply drafts, length-limit checks and a ready-to-schedule content pack. Use this skill whenever the user wants posts, captions, carousel copy, a thread, a week of content, repurposing a video or article into social posts, or says "write a post", "make a caption", "create content", "for social media", even if no platform is named.
---

# Social media content

Writes posts that fit each platform's format, limits and audience, in the brand's own voice, then checks them mechanically and hands over a pack that can go straight into a calendar or scheduler. Replies follow the user's language preference; posts are written in the language the audience reads.

## Principles

- Start from the audience and the one thing a post should make them do or feel. One post, one idea, one action.
- Specific beats general: a number, a name, an example, a before and after. Never invent facts, results, testimonials, quotes or statistics. If a number is needed and not provided, use a placeholder like `[X%]` and flag it.
- Native, not copy-pasted: each platform gets its own structure (see `references/platform-playbook.md`), not the same text with different hashtags.
- Use the brand voice. If a `brand-voice` guide or profile exists, follow it; if not, ask for 3 sample posts or state the assumed tone and offer to build the guide.
- Rules of thumb here (hooks, lengths, hashtag counts, best formats) are practitioner heuristics, not platform rules or guaranteed results. Say so when it matters, and let the user's analytics decide.

## Workflow

1. **Intake.** Goal (awareness, leads, sales, community), audience, platforms, language mix, offer or topic, source material (video, article, product page, notes), voice guide or samples, links and CTA, claims to avoid, restrictions (legal, regulated topics), how many posts. Ask only for what is missing; proceed with stated assumptions otherwise.
2. **Angle.** For each idea write the point, the proof (fact, story or demo from the user's material), and the action. Pick a content type from `references/content-formats.md` (educate, story, proof, opinion, behind the scenes, offer, community).
3. **Draft per platform.** Hook first, then value, then one CTA. Give 2 to 3 hook options for important posts and recommend one. Draft carousel slide-by-slide; threads with a standalone first post. Keep line breaks short on mobile.
4. **Details.** Hashtags or keywords (few, relevant), alt text for every image, a visual brief (what the image or slides show, using `thumbnail-design` for covers if available), and a first-comment or reply plan where useful.
5. **Check.** Put the posts in a pack JSON (format at the top of `scripts/content_tools.py`) and run `python scripts/content_tools.py check pack.json`. Fix FAILs; read WARNs. If a voice profile exists, also run the `brand-voice` checker on each draft.
6. **Review for rights and claims.** No unlicensed music, images or quotes; ads, sponsorships and affiliate links disclosed as the platform and local rules require; no misleading claims; no personal data. See `references/compliance.md`.
7. **Deliver.** Show the posts grouped by idea or by platform with the recommendation, the open questions (placeholders to fill), and the files: `pack.json` and `posts.csv` (`content_tools.py csv`). If the session offers a docs or sheets type, put long packs there. Offer the next step: schedule with `social-media-calendar`, adapt a video with `short-form-video-scripts`, or measure with `analytics` (when those skills exist).

## Commands

```bash
python scripts/content_tools.py limits [--platform instagram]
python scripts/content_tools.py check PACK.json [--json report.json]
python scripts/content_tools.py csv PACK.json --out posts.csv
python scripts/content_tools.py thread TEXT.txt --platform x [--limit 280]
python scripts/content_tools.py text "caption" --platform instagram
```

Standard library only. Limits come from a vendor help page that is undated and from general knowledge; the tool says which. Confirm in the platform composer before a big campaign.

## Repurposing

One strong source (a video, article, case study, podcast) becomes 5 to 10 pieces: a short hook post, a carousel of the key steps, a thread, a LinkedIn story, a quote graphic, a Reel or Short script, a poll, an FAQ reply set. Keep one core message and change the angle and format. Map it in the table from `references/content-formats.md`. Do not just cut and paste.

## Rules

- Never fabricate engagement, testimonials, reviews or screenshots. Never write fake "customer" stories as real.
- Do not copy another creator's post; use a trend or format, not their words.
- Do not give individualized medical, legal or financial advice; keep general, cite sources, add a clear disclaimer where the topic needs it.
- Disclose paid partnerships and affiliate links.
- Do not post or schedule anything yourself unless the user asks and a connected tool exists; deliver drafts for approval.
- Avoid engagement bait that platforms discourage (tag-for-reward, fake urgency, misleading "link in bio" teasers).

## References

- `references/platform-playbook.md`: per-platform formats, structure, lengths, hooks, CTAs, what to avoid.
- `references/content-formats.md`: content types, hook patterns, carousel/thread/LinkedIn/caption templates, repurposing matrix, reply drafting.
- `references/compliance.md`: disclosure, rights, claims, sensitive topics, AI-content disclosure, community guidelines.
