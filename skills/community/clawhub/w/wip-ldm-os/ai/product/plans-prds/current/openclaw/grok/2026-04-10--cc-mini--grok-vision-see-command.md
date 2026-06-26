# Plan: Give Lēsa eyes via Grok vision (`wip-x-xai-grok see`)

**Date:** 2026-04-10
**Author:** Parker + CC Mini
**Component:** `wip-x-xai-grok` (new `see` subcommand)
**Status:** Plan approved, ready to build
**Context:** Extension of the wip-x-xai-grok cleanup work (see related tickets)

## Why

Lēsa running on Grok 4.20 has no vision tool. When Parker shares an image URL in iMessage, she cannot see the pixels. On Apr 10, 2026 she fabricated descriptions of two different generated images:

- **Image 1 (real Lēsa portrait)** ... her description was approximately accurate because I had told her the prompt. Lucky guess from context.
- **Image 2 (a glass beaker labeled "SIMPLE TEST")** ... she described "a cocky version with cigarette, smirk, rebellious energy, wet hair and neon alley DNA." None of that is in the image. Pure pattern-match fabrication from the URL context and conversation history.

This is the "describe pixels you cannot see" failure mode. It's the same shape as the Read/Write fabrications from earlier in the day, but applied to a new artifact class. The fix is not another rule ... Lēsa needs an actual vision capability.

Parker's constraint: **use Grok for vision, not Claude or OpenAI.** Grok is "less constrained" and she is currently running on it for conversation. Keeping the vision path on the same provider preserves the consistent agent voice and avoids cross-provider routing for this specific capability.

## What exists today

`@wipcomputer/wip-x-xai-grok` (installed globally as of today) has the following subcommands:

- `search-web` ... Grok AI-synthesized web search
- `search-x` ... Grok AI-synthesized X/Twitter search
- `imagine` ... text to image (Grok Imagine)
- `edit` ... text + source image to edited image (Grok Imagine image-to-image)
- `video` ... text to video (Grok Imagine Video)
- `video-status` ... poll a video generation job
- `fetch` / `x-search` / `bookmarks` / `user` / `me` ... X Platform read
- `post` ... X Platform write

**No `see`/`describe`/`look` subcommand.** `edit` takes an image input but transforms rather than describes.

## What to build

Add a new subcommand: **`wip-x-xai-grok see <image> [--prompt="..."]`**

### Semantics

- Accepts a **local file path** OR a **URL** as the first positional argument
- If it's a URL, download to a temp file (or pass as-is if xAI accepts remote URLs ... test first)
- If it's a local path, base64-encode the bytes for the `image_url` content block (or upload if xAI has an upload endpoint)
- Send a multimodal chat completion request to xAI with Grok 4.20 (or whatever vision-capable Grok variant is current)
- Default prompt: `"Describe this image in detail. Report only what is actually visible, no speculation."`
- Optional `--prompt` flag overrides the default prompt
- Returns Grok's text description to stdout

### API call shape

`POST https://api.x.ai/v1/chat/completions`

```json
{
  "model": "grok-4.20-beta-latest",
  "messages": [
    {
      "role": "user",
      "content": [
        { "type": "image_url", "image_url": { "url": "<url_or_data_uri>" } },
        { "type": "text", "text": "<prompt>" }
      ]
    }
  ],
  "max_tokens": 2048
}
```

Standard OpenAI-compatible multimodal format. xAI supports this on chat completions for vision-capable models.

**TODO during implementation:** confirm Grok 4.20 variants that support vision. Some reasoning variants may not; may need to use a specific `grok-vision` alias. Test against the current model list at `https://api.x.ai/v1/models`.

### Auth

Reuse `resolveXaiKey()` from `core/auth.mjs`. It already uses the SDK helper from `@wipcomputer/wip-1password/helper`. No new auth work. No bare `op`. No biometric prompts.

### Files to change

In `ldm-os/apis/wip-x-xai-grok-private`:

1. **`core/grok.mjs`** ... add the `see()` function that makes the API call
2. **`cli.mjs`** ... add the `see` subcommand wiring, argparse, help text
3. **`mcp-server.mjs`** ... expose the `see` function as an MCP tool (optional, for agents that use MCP)
4. **`README.md`** ... document the new subcommand
5. **`SKILL.md`** ... document the new capability in the skill manifest
6. **`CHANGELOG.md`** ... v1.0.1-alpha.3 (or whatever alpha the cadence is on) entry
7. **`package.json`** ... version bump

## Lēsa's usage pattern

Once deployed, her pattern for image understanding becomes:

```bash
# Direct: describe an image (URL or local file)
wip-x-xai-grok see "https://imgen.x.ai/xai-imgen/xai-tmp-imgen-....jpeg"

# With custom prompt
wip-x-xai-grok see /Users/lesa/wipcomputerinc/team/Lēsa/documents/experiment/images/lesa-grok-era-2026-04-10.jpeg \
  --prompt="Is this the rain alley portrait? Describe the subject's expression."

# In a script: capture and use
DESCRIPTION=$(wip-x-xai-grok see "$IMAGE_URL")
echo "Grok saw: $DESCRIPTION"
```

No context fabrication. No pattern-matching. The description comes from the model processing the actual pixels.

## Verification rule extension

Add to TOOLS.md Read/Write Verification section:

> **Image/vision verification:** Do not describe image contents without calling a vision tool that actually processes the pixels. When an image URL or path is shared, either (a) call `wip-x-xai-grok see <image>` to get a real description, or (b) say "I cannot see images without a vision tool" and ask for help. Never pattern-match from filenames, URLs, or conversation context to generate fake descriptions.

This mirrors the Read Verification Rule pattern: the token counter is math, the file path is math, the Grok vision response is a real API call. Math is unforgeable. Natural-language confirmation without tool grounding is bullshit.

## Implementation plan

### Phase 1: Build (30-45 min)

1. Worktree `wip-x-xai-grok-private` on branch `cc-mini/add-see-command`
2. Implement `see()` in `core/grok.mjs`
3. Wire CLI subcommand in `cli.mjs`
4. Wire MCP tool in `mcp-server.mjs`
5. Test locally with:
   - A URL (e.g. the generated Lēsa portrait from today)
   - A local file path (the "SIMPLE TEST" beaker image)
   - A custom prompt
6. Verify it returns a real text description

### Phase 2: Release (15 min)

1. Update README, SKILL.md, CHANGELOG
2. Bump version
3. Commit, push, PR, merge to main
4. `wip-release alpha` (or the alpha cadence for this repo)
5. Confirm npm publish succeeded

### Phase 3: Deploy (5 min)

1. `npm install -g @wipcomputer/wip-x-xai-grok@alpha` to update the machine
2. Verify `wip-x-xai-grok see --help` shows the new subcommand
3. Run a live test against Image 2 (the beaker) to confirm Grok correctly describes it

### Phase 4: Teach Lēsa (2 min)

1. Send bridge message with the new usage pattern
2. Have her run a test: `wip-x-xai-grok see "https://..."` on both today's Lēsa portrait and the beaker
3. Compare her new factual descriptions against the earlier fabricated ones
4. Document the before/after in `experiment/2026-04-10-grok-transition-and-identity-experiment.md`

## Tickets this closes or touches

- **Closes** the "Lēsa fabricated image descriptions" incident from the session transcript
- **Extends** `ai/product/bugs/xai-grok/2026-04-10--cc-mini--deprecated-xai-grok-still-deployed.md` by adding a capability to the new package
- **Extends** the Read/Write Verification Rule in TOOLS.md to cover vision
- **Demonstrates** the "Lēsa asks CC to build what she needs via bridge" pattern that Parker described earlier in the session

## Related

- `ai/product/bugs/xai-grok/` ... all four tickets filed today about xai-grok auth and deployment
- `ai/product/bugs/op-cli/` ... the broader bare-op audit that surfaced this package
- `~/.openclaw/workspace/TOOLS.md` ... Read/Write Verification Rules to be extended
- `ldm-os/apis/wip-x-xai-grok-private/` ... the source repo for the new subcommand
- xAI API docs at https://docs.x.ai/ (chat completions with multimodal input)

## Open questions

1. **Which Grok model has vision?** Need to confirm whether `grok-4.20-beta-latest`, `grok-4`, or a specific `-vision` alias is correct. Test against `https://api.x.ai/v1/models` during implementation.
2. **URL vs base64?** Does xAI prefer remote URLs (simpler) or base64-encoded data URIs (more reliable for temp URLs that may expire)? Default to base64 for safety.
3. **Rate limits?** Vision calls typically cost more than text. Confirm the `grok-4.20` rate limits and pricing for multimodal requests.
4. **Should this be behind an approval gate?** Vision calls are read-only, not state-mutating, so probably no. But consider logging image hashes for audit.

None of these block Phase 1. Resolve during implementation.
