---
name: reelsfarm-product-photos
description: Make AI product photos and infographics with ReelsFarm: import a product image, place the product in a new scene or a person's hands, or fill a product or infographic template. Needs a ReelsFarm account.
metadata:
  openclaw:
    emoji: "📦"
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

# ReelsFarm product photos

Make AI product photos and infographics with ReelsFarm. Place the user's real product in a new scene, put it in a person's hands, or fill a product or infographic template.

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

## 1. Get the product photo into ReelsFarm

The CLI doesn't upload local files. Import a product image from a public URL, or use one already in the account:

```bash
reelsfarm assets import --category products --url https://example.com/product.jpg --name "Cold brew bottle" --agent
reelsfarm assets list --category products --agent
reelsfarm media-collections gallery --kinds AVATAR,PRODUCT_PLACEMENT --image-category product --agent
```

Use the ReelsFarm URL the import returns. Product imports accept product images only. Never use them for a photo of a person.

## 2. Place the product in a scene

`product-scenes generate` puts the product into a source image, such as an avatar or a template's reference photo:

```bash
reelsfarm product-scenes generate --source-image-url <scene or avatar URL> --product-image-url <product URL> --prompt "She holds the bottle at eye level, label facing the camera" --agent
```

To adjust a result, run it again with `--conversation-id` and `--parent-generation-id` from the previous result.

## 3. Use a template

```bash
reelsfarm image-generations templates --category product --agent
reelsfarm image-generations templates --category infographics --agent
```

Each template has a `referenceUrl`, a `categoryLine`, and a prompt brief with `[PLACEHOLDER]` fields. Replace the placeholders with the user's details, delete lines you can't fill, and start the prompt with the `categoryLine`.

- A template with `requiresProduct: true` uses `reelsfarm product-scenes generate` with `--source-image-url` set to the `referenceUrl` and `--product-image-url` set to the product photo.
- Other templates use `reelsfarm avatars generate` with `--reference-url` set to the `referenceUrl` and the template's model, aspect ratio, and quality.

Keep the product accurate. Don't change its label, shape, or claims, and don't add claims the user didn't give you.
