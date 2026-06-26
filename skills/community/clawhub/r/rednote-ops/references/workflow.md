# Workflow

## First-time setup

1. Ask setup questions
2. Save config to `data/xiaohongshu/profile.json`
3. Confirm the saved style in one concise summary
4. Ask whether the user wants a first publish test

## Later usage

When the user says things like:
- 帮我运营小红书
- 发一篇小红书
- 生成一篇 AI 小红书
- 按我的风格做一篇

Do this:
1. Read `data/xiaohongshu/profile.json`
2. If autoLearning is enabled, allow daily reference learning outputs to inform topic/style choice
3. Generate topic/title/page structure/body using that style
4. Choose image mode:
   - stock / cards-lite / mixed
5. If using stock/mixed, generate stock-image search plan first
6. Build image pipeline plan (stock first, cards-lite fallback when needed)
7. Generate cards only when the chosen strategy needs cards or as fallback
8. Publish through the dedicated independent browser flow when publishing is requested

## Image policy

- Prefer relevant watermark-free stock images when configured
- Use lightweight cards as fallback or by preference
- Never remove watermarks

## Publish policy

- Canonical real publish path: independent browser profile
- Do not rely on the user's daily browser as the default automation target
- Before relaunching the independent browser publish flow, clear any stale independent instance that still holds the profile lock

## First publish test

If the user agrees, generate one post with the saved style and prepare/publish it through the independent browser path to verify the full chain works.
