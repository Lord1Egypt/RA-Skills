# tweet-share-card

Turn an X/Twitter post link into a polished share image.

## What it does

- Detects an `x.com` / `twitter.com` post link
- Reads the tweet content
- Generates a square share card image
- Uses **peach** as the default background style
- Supports alternate presets like `blue-purple`, `purple-blue`, `pink`, and `mint`
- Can include tweet metrics such as replies, likes, and views

## Example prompts

- `https://x.com/... 生成推文分享卡片`
- `https://x.com/... 制作推文分享卡片，蓝紫渐变`
- `https://x.com/... make a tweet share card with mint background`

## Default behavior

- Default color: **peach**
- Square poster output
- White inner content card adapts to content height
- Preserves the main tweet content without arbitrary cropping of core text

## Status

This skill is already usable and focuses on a practical workflow:

1. detect tweet link
2. render a shareable card
3. send image back to the user

Future improvements can refine more layout templates and richer media handling.
