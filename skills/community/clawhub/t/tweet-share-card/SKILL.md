---
name: tweet-share-card
description: Turn an X/Twitter post link into a share image. Use when the user sends an X/Twitter URL and wants a polished share card image: detect the tweet URL, capture the tweet content area, place it onto a pink poster-style background, and send the final image back.
---

Create a share image from an X/Twitter post.

## When to use

- User sends an `x.com` / `twitter.com` post URL
- User wants a tweet screenshot, share card, poster, or social-share image
- User wants the final image sent back in chat

## Workflow

1. Extract the tweet URL from the user message.
2. Open the tweet in the dedicated visible Chrome profile/session already used for X login.
3. Capture the **tweet content area only**:
   - keep avatar/name/text/link preview
   - exclude right sidebar
   - exclude reply/action counts when possible
   - do not rewrite or re-typeset tweet text
4. Parse any user-requested color style (examples: `pink`, `blue-purple`, `purple-blue`, `peach`, `mint`).
5. Composite the captured tweet area onto a poster background using that style.
6. Save the final image under `workspace/tmp/`.
7. Send the final image back to the user.

## Rules

- Prefer the user's logged-in **dedicated Chrome profile**, not their default browser profile.
- Do **not** use headless/embed screenshots if they produce blank/incorrect tweet content.
- The tweet content must be a real screenshot, not re-rendered fake text.
- Default background style: clean pink poster style.
- Support color presets when the user asks, including `pink`, `blue-purple`, `purple-blue`, `peach`, and `mint`.
- Default output is a square share card with a peach background unless the user asks for another preset.
- The white content card should adapt to content height instead of using a fixed internal height.
- Preserve the tweet content area without cropping away core text.
- Always inspect the result before sending if the capture path changed.

## Output

Return the final image directly to the user with a short caption only if needed.

## Scripts

- `python3 {Skills Directory}/tweet-share-card/scripts/capture_visible_tweet.py <tweet_url> <output_png>`
- `python3 {Skills Directory}/tweet-share-card/scripts/compose_pink_card.py <tweet_capture_png> <output_png> [pink|blue-purple|purple-blue|peach|mint]`
