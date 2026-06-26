---
name: x-comment-feed-posts
description: Find posts in the user's X feed and leave comments on them one by one. Use when the user wants to comment on N posts from the feed, usually about indie tech launches, new tech, or AI, while keeping comments short, first-person, thread-specific, and manually executed.
---

# X Comment Feed Posts

Use this skill for manual commenting from the feed.
It assumes browser access, and it works best when a `twitter-humanizer` skill is also available.

Default topic focus:

- Indie tech launches
- New tech products or releases
- AI launches, model updates, tooling, or practical AI workflows

If the user provides a different topic set, use that instead.
If the user does not provide `N`, ask for it.

Do not use this skill to evade platform enforcement, fake human browsing patterns, or mass-engage indiscriminately.
By default, use the home feed to discover posts. Do not use the X search bar unless the user explicitly tells you to.
CRITICAL NON-NEGOTIABLE: never find posts by searching when sourcing comments for this skill.
CRITICAL NON-NEGOTIABLE: always use the For You tab on the home feed. Never switch to Following or any other tab.
CRITICAL NON-NEGOTIABLE: once on the X feed, never refresh or reload the page for any reason for the entire run. Return between posts using back navigation only.
CRITICAL NON-NEGOTIABLE: close the x.com tab immediately after the run is complete. Never leave it open.
CRITICAL: do not open post URLs directly. Always click the post card from the feed to open it.
CRITICAL: before selecting the first candidate, perform an initial scroll pass and inspect multiple screenfuls of feed content.
CRITICAL: avoid consecutive comments on near-identical posts from the same narrow topic cluster when other relevant topics are available.

## Comment standard

- One post at a time
- Use first person
- CRITICAL NON-NEGOTIABLE: keep every comment to 1 or 2 short sentences.
- CRITICAL NON-NEGOTIABLE: never avoid, relax, or reinterpret this limit unless the user explicitly asks for longer comments.
- Stay on the thread topic only
- Sound like a person who read the post and had a real reaction — not a summarizer with a polished observation
- Real emotion is allowed: surprise, mild annoyance, genuine excitement, skepticism, confusion
- If you disagree with something, say so directly — do not try to be balanced
- If you are unsure, say so — "not sure about this" is a valid comment
- No forced product mentions
- No fake engagement CTAs like "What do you think?"
- Fresh posts are preferred; target posts that look recent, ideally within the last hour when timestamps are visible
- Read [references/human-voice.md](references/human-voice.md) before drafting any comment

## Workflow

1. Run `openclaw browser start` to open the openclaw managed browser. CRITICAL NON-NEGOTIABLE: always use this command. Never open a browser any other way. Then navigate to X, go to the home feed, and select the **For You** tab.
2. Scroll and inspect candidates one by one.
   - Content quality matters more than popularity.
   - Prefer posts that say something specific enough to answer.
   - Do not stop at the first few visible posts; keep scrolling before deciding on each next candidate.
   - Read [references/feed-workflow.md](references/feed-workflow.md).
3. For each chosen post:
   - Open the post by clicking it in the feed (never by typing/pasting a URL)
   - Read the post and enough surrounding context to understand the thread
   - Like the post before doing anything else
   - Decide on one comment before typing
   - If the `twitter-humanizer` skill is available, use it to refine the comment without making it longer
   - Read [references/comment-rules.md](references/comment-rules.md).
   - Post the comment
   - Return to the feed using back navigation
   - Scroll more, then find the next candidate
   - Do not jump between multiple open posts; complete one full post cycle before opening another
4. Repeat until `N` comments are posted or the feed stops yielding good candidates.
5. CRITICAL NON-NEGOTIABLE: close every `x.com` tab immediately after the run is complete. Do not leave any tab open.

## If the feed is weak

- Keep scrolling instead of lowering the quality bar immediately
- If you truly cannot find enough fresh posts on the requested topic, say so in the completion report
- Only widen the freshness window or topic scope if the user explicitly allows it or the run would otherwise fail

## Completion report

At the end, report:

- Requested `N`
- Actual number of comments posted
- Which topics or posts were chosen
- The final text used for each comment
- Whether search was avoided
- Confirmation that all `x.com` tabs were closed
