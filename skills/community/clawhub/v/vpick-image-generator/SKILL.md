---
name: vpick-image-generator
description: "Multi-model AI image generation on a visual canvas. Supports Midjourney (relaxed/fast/turbo, v7.0, 4-image grid), Grok Imagine (6 images per call, auto I2I), nano-banana-2 (multi-reference), Seedream 5.0 (up to 3K HD). Features: text-to-image, image-to-image, style transfer, multi-reference composition, batch generation, aspect ratio control. Use when the user says 'generate image', 'create an image', 'AI image', 'Midjourney', 'generate artwork', 'character design', 'create illustration', or wants AI image generation."
version: 1.0.1
metadata:
  openclaw:
    emoji: "🎨"
    homepage: https://vpick-doc.10xboost.org/guide/mcp-connection.html
---

# VPick Image Generator

Multi-model AI image generation on a visual canvas — Midjourney, Grok, nano-banana, Seedream — with reference image support, style transfer, and batch generation. Powered by [VPick](https://vpick.10xboost.org).

## Security & Data Handling

- **Authentication**: Your MCP link contains an embedded token — no separate API keys or credentials are needed or sent. Treat your MCP link like a password.
- **Data flow**: All generation requests go through VPick's server (`vpick.10xboost.org` on Google Cloud). VPick routes requests to third-party AI model providers (Midjourney, Grok, Seedream, etc.) on your behalf. Your prompts and uploaded reference images are sent to these providers for processing.
- **Storage**: Generated images are stored in Google Cloud Storage under your VPick account.
- **No local credentials**: This skill does not require any local API keys, environment variables, or secrets.
- **Billing**: Generation costs are charged to your VPick credit balance, not directly to any third-party service.

## Prerequisites

1. **Sign up** at [vpick.10xboost.org](https://vpick.10xboost.org) (Google OAuth — new users get $1 free credit)
2. **Get your MCP link**: Go to **Settings** → copy your MCP Server URL (contains your auth token)
3. **Add to Claude**: Paste the MCP link into Claude settings as a Connector — no install, no API keys needed

## Available Image Models

| Model | Cost | Output | Best For |
|-------|------|--------|----------|
| **nano-banana-2** | $0.16/image | 1 image | Default, fast, multi-reference support |
| **Midjourney Relaxed** | $0.045/grid | 4 images (grid) | Budget artistic generation |
| **Midjourney Fast** | $0.12/grid | 4 images (grid) | Quick artistic generation |
| **Midjourney Turbo** | $0.24/grid | 4 images (grid) | Fastest Midjourney |
| **Grok Imagine** | $0.06/call | 6 images (T2I) or 2 (I2I) | Budget bulk generation |
| **Seedream 5.0 Lite** | $0.0825/image | 1 image (2K) | High resolution, affordable |
| **Seedream 5.0 HD** | $0.0825/image | 1 image (3K) | Ultra high resolution |

**Aspect Ratios**: 1:1, 16:9, 9:16, 3:4, 4:3 (all models)

## Core Workflow

### Step 1: Set Up

Check user's canvas and project:
```
get_canvas          → See current state
list_projects       → Check existing projects
create_project      → Start fresh if needed
```

### Step 2: Create Image Generator Node

```
add_node(type: "image-generator", name: "My Image")
```

### Step 3: Set the Prompt

**Option A — Direct prompt:**
```
update_node(id: "<node_id>", data: { prompt: "a cyberpunk cityscape at sunset, neon lights, rain reflections" })
```

**Option B — Connect a Text node:**
```
add_node(type: "text", name: "Prompt", data: { content: "a cyberpunk cityscape at sunset" })
connect_nodes(sourceId: "<text_node>", targetId: "<image_node>", sourceHandle: "text-out", targetHandle: "prompt-in")
```

### Step 4: Add Reference Images (Optional)

Reference images guide the generation style or subject. Up to 10 reference images supported.

```
upload_image(url: "https://example.com/reference.jpg")
connect_nodes(sourceId: "<upload_node>", targetId: "<image_node>", sourceHandle: "file-out", targetHandle: "image-in")
```

**Use `@NodeLabel` in prompts** to reference connected images:
```
"A portrait in the style of @reference, vibrant colors"
```

The `@reference` is resolved at generation time to the connected image URL.

### Step 5: Generate

```
run_image_generator(
  nodeId: "<image_node>",
  prompt: "a cyberpunk cityscape at sunset, neon lights",
  model: "nano-banana-2",
  aspectRatio: "16:9"
)
```

**Midjourney-specific options:**
```
run_image_generator(
  nodeId: "<image_node>",
  prompt: "a cyberpunk cityscape at sunset",
  model: "midjourney",
  aspectRatio: "16:9",
  mjSpeed: "fast",        // "relaxed", "fast", "turbo"
  mjVersion: "7.0"        // Midjourney version
)
```

**Grok — auto-detects T2I vs I2I:**
- No reference image → Text-to-Image (6 images)
- With reference image → Image-to-Image (2 images)

### Step 6: Browse Results

Models may generate multiple images:
- **Midjourney**: 4-image grid — browse via `currentImageIndex` (0-3)
- **Grok**: 6 images (T2I) or 2 images (I2I)
- **Others**: 1 image

Check results:
```
get_node(id: "<image_node>")   → See generatedImageUrl, status
list_nodes                      → Overview of all nodes
```

### Step 7: Use Generated Images

Generated images can be used as input for:
- **Video generation**: Connect to VideoGenerator's `start-image-in` port
- **More image generation**: Connect as reference for another ImageGenerator
- **Character consistency**: Use as Element reference in MultiShot video

```
connect_nodes(sourceId: "<image_node>", targetId: "<video_node>", sourceHandle: "image-out", targetHandle: "start-image-in")
```

## Common Use Cases

### Character Design (White Background References)
For video production, generate character references on white backgrounds:
```
run_image_generator(
  nodeId: "<node>",
  prompt: "full body portrait of a young woman, casual outfit, white background, isolated figure, front view",
  model: "nano-banana-2",
  aspectRatio: "3:4"
)
```
Generate multiple angles (front, side, 3/4) for use as MultiShot Elements.

### Batch Generation
Create multiple ImageGenerator nodes and generate in parallel:
```
add_node(type: "image-generator", name: "Variant A")
add_node(type: "image-generator", name: "Variant B")
add_node(type: "image-generator", name: "Variant C")
run_image_generator(nodeId: "<A>", prompt: "sunset beach, warm tones", model: "midjourney")
run_image_generator(nodeId: "<B>", prompt: "sunset beach, cool tones", model: "grok-imagine")
run_image_generator(nodeId: "<C>", prompt: "sunset beach, dramatic", model: "nano-banana-2")
```

### Style Transfer with References
```
upload_image(url: "https://example.com/style-reference.jpg")
connect_nodes(sourceId: "<upload>", targetId: "<image_node>", sourceHandle: "file-out", targetHandle: "image-in")
run_image_generator(
  nodeId: "<image_node>",
  prompt: "a portrait in the style of @style-reference, detailed, high quality",
  model: "nano-banana-2"
)
```

## Organize Your Canvas

Keep things tidy:
```
auto_layout(nodeIds: [...], direction: "horizontal", spacing: 200)
create_group(nodeIds: [...], overrides: { label: "Character Designs", color: "#E57373" })
```

## Check Usage & History

```
list_generated_files(limit: 20, model: "midjourney")   → Recent generations filtered by model
get_generation_stats                                     → Cost breakdown by model
```

## Tips

- **nano-banana-2** is the best default — fast, affordable, supports multi-reference
- **Midjourney** excels at artistic/stylized images — use `relaxed` speed to save cost
- **Grok** is the cheapest for bulk generation ($0.06 for 6 images)
- **Seedream** produces the highest resolution (up to 3K)
- **White background** images are essential for video Element references
- **`@NodeLabel` references** are resolved at generation time — make sure labels match exactly
- Use `list_models` tool to check current pricing and available models

## Error Handling

| Error | Solution |
|-------|----------|
| Generation timeout | Auto-retries up to 2 times; check status with `get_node` |
| Insufficient credits | Top up at vpick.10xboost.org |
| Invalid aspect ratio | Use: 1:1, 16:9, 9:16, 3:4, or 4:3 |
| Reference not resolved | Ensure `@NodeLabel` matches the connected node's label exactly |
| Node not found | Use `list_nodes` to get current node IDs |

## Documentation

- VPick App: [vpick.10xboost.org](https://vpick.10xboost.org)
- Available models: Call `list_models` tool for current pricing and capabilities
