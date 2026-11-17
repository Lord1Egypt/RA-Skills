---
name: reelsfarm-tiktok-slideshows
description: Create TikTok and Instagram photo slideshows with ReelsFarm: write slide text, pick a look (classic, tweet, iMessage, notebook, magazine), recreate a public TikTok slideshow for your product, find photos, and render slides or an MP4. Needs a ReelsFarm account.
metadata:
  openclaw:
    emoji: "🎞️"
    homepage: https://reelsfarm.com/docs/mcp
    primaryEnv: REELSFARM_API_KEY
    requires:
      bins:
        - reelsfarm
      env:
        - REELSFARM_API_KEY
    envVars:
      - name: REELSFARM_API_KEY
        required: true
        description: ReelsFarm MCP API key (starts with rfmcp_), created in the MCP tab of the ReelsFarm account.
    install:
      - kind: node
        package: "@reelsfarm/mcp-client"
        bins:
          - reelsfarm
---

# ReelsFarm TikTok slideshows

Make photo slideshows for TikTok and Instagram with ReelsFarm: short text over photos, or designed slides that look like a tweet, an iMessage chat, a notebook page, or a magazine. Work in stages and show the user each stage: text, photos, draft, final render.

## Setup

1. Install the CLI: `npm install -g @reelsfarm/mcp-client`. It provides the `reelsfarm` command.
2. Create an MCP API key in the MCP tab of the ReelsFarm account and set it as `REELSFARM_API_KEY`. The key is shown only once.
3. Check the connection: `reelsfarm agent status` and `reelsfarm account status --agent`.

ReelsFarm is a paid service (https://reelsfarm.com). Creating media spends credits from the user's plan or trial. Without one, commands that create or publish return a link to choose a plan. Credential, connection-mode, and permanent-delete settings stay in the ReelsFarm dashboard and are not in the CLI.

## Running actions

- Always add `--agent`. It prints one JSON object with `ok`, `data` or `error`, and a `nextStep` hint.
- Preview first with `--dry-run`. Nothing runs on the server. Tell the user what will be made and what it costs; `reelsfarm account pricing --agent` lists credit prices.
- After the user approves, run the same command with `--yes --wait`. `--yes` confirms only the action the server prepared. It never changes the account's connection mode. `--wait` waits for the job to finish.
- If a response has `requiresConfirmation: true`, ask the user, then run its `nextStep` (`reelsfarm confirm <id> --tool <tool> --agent`). If that returns an operation id, follow it with `reelsfarm operations wait --id <operationId> --agent`.
- Give each action one `--idempotency-key` and reuse it only to retry that same action after a timeout. Never start a second copy while the first may still be running.

## Results

Say an image, video, or slideshow exists only when the response shows `executionState: "COMPLETED"`, `assetCreated: true`, and a ReelsFarm asset id and URL. `PREPARED` or `NOT_STARTED` means nothing ran. `ENQUEUED` or `PROCESSING` means it is not finished. When the user asked for ReelsFarm, don't swap in another image or video generator.

## 1. Know the product

Slideshows that mention a product use a saved product context.

```bash
reelsfarm product-contexts list --agent
reelsfarm product-contexts suggest --url https://example.com/product --agent
reelsfarm product-contexts create --name "Cold brew kit" --description "..." --image-url <ReelsFarm image URL> --agent
```

## 2. Write the slides

```bash
reelsfarm slideshows generate-text --prompt "Texts with my mom about my coffee spending" --design imessage --slide-count 4 --agent
reelsfarm slideshows generate-text --prompt "5 cold brew mistakes" --type EDUCATIONAL --slide-count 6 --effort high --agent
```

- `--design` picks the Look: `auto`, `classic`, `tweet`, `imessage`, `notebook`, or `magazine`. An iMessage slideshow needs no photos.
- `--format` follows a proven format: `help-me-choose`, `numbered-product-last`, `rated-picks`, or `problem-math-steps`.
- `--type` is `EDUCATIONAL`, `PROMOTIONAL`, `STORYTELLING`, `LIFESTYLE`, or `REVIEW`.
- `--effort` is `light`, `low`, `medium`, `high`, or `extra_high`. Higher effort is slower and reads more of the slide photos (pass them with `--max --visual-context-json`, each with its `aspectRatio`).

To change the text, send the current slides with an instruction:

```bash
reelsfarm slideshows revise-text --instruction "Make slide 2 shorter" --slides-json '<current slides>' --agent
```

## 3. Recreate a slideshow that worked

Turn a public TikTok photo slideshow into a new one for the user's product. It keeps the structure and writes new text and photos.

```bash
reelsfarm slideshows recreate --tiktok-url https://www.tiktok.com/@user/photo/123 --product-context-id <id> --instructions "Keep it to 5 slides" --agent
```

## 4. Find photos

```bash
reelsfarm slideshows search-photos "cozy coffee morning" --agent
reelsfarm slideshows search-photos "latte art" --source pexels --agent
reelsfarm slideshows save-photos --photos-json '[{"url":"<photo url from search>"}]' --agent
```

Sources are `pinterest` (default), `tumblr`, and `pexels`. Save the photos you use; slides need the ReelsFarm URLs that `save-photos` returns. The user's own images are in `reelsfarm media-collections gallery --agent`.

## 5. Save, render, export

```bash
reelsfarm slideshows create --title "Cold brew mistakes" --slides-json '<slides>' --agent
reelsfarm slideshows finalize --slideshow-id <id> --agent
reelsfarm slideshows export-video --slideshow-id <id> --agent
```

`finalize` renders the final slide images. `export-video` makes an MP4 and only runs when the user asks for a video. Finalize only after the user approves every slide. To post the result, use the `reelsfarm-social-scheduler` skill.

Don't change slide order on your own, and don't use photos that didn't come from ReelsFarm, a ReelsFarm photo search, or the user.
