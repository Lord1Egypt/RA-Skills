---
name: quiver
description: Generate SVGs from text prompts and convert raster images (PNG/JPG/WebP) to SVG using QuiverAI's AI models. Use when user asks to create icons, illustrations, logos as SVG, or to vectorize/convert an image to SVG.
argument-hint: "<generate|vectorize|models> [options]"
allowed-tools: Bash(quiver:*), Bash(pwd), Read, Write, Glob
---

# QuiverAI SVG Generation Skill

You have access to the `quiver` CLI tool for AI-powered SVG generation and image vectorization.

## Prerequisites

The `quiver` CLI must be installed globally:

```bash
npm install -g quiver-ai-cli
```

If the user hasn't configured their API key yet, guide them:

```bash
quiver config set api_key <their-key>
```

## Commands

### Text to SVG — `quiver generate`

Generate SVG graphics from a text description.

```bash
quiver generate [options] "<prompt>"
```

**Options:**

| Flag | Description |
|------|-------------|
| `-m, --model <model>` | Model ID (default: arrow-preview) |
| `-o, --output <file.svg>` | Save to file instead of stdout |
| `-s, --stream` | Stream via SSE (shows progress on stderr) |
| `-n, --count <n>` | Number of SVG variants (default: 1) |
| `-t, --temperature <float>` | Creativity level (default: 1) |
| `-i, --instructions <text>` | Additional style guidance |
| `--max-tokens <n>` | Upper bound on output tokens |
| `-r, --reference <url\|file>` | Reference image (repeatable) |

### Image to SVG — `quiver vectorize`

Convert a raster image into a clean SVG vector.

```bash
quiver vectorize [options] <image-path-or-url>
```

**Options:**

| Flag | Description |
|------|-------------|
| `-m, --model <model>` | Model ID (default: arrow-preview) |
| `-o, --output <file.svg>` | Save to file instead of stdout |
| `-s, --stream` | Stream via SSE |
| `-t, --temperature <float>` | Temperature (default: 1) |
| `--auto-crop` | Auto-crop to dominant subject |
| `--target-size <px>` | Resize before processing |
| `--max-tokens <n>` | Upper bound on output tokens |

### List Models — `quiver models`

```bash
quiver models list
quiver models get <model-id>
```

### Configuration — `quiver config`

```bash
quiver config set api_key <key>
quiver config set default_model <model>
quiver config get
quiver config path
```

## Workflow

When the user asks you to create or generate an SVG:

1. Run `pwd` to confirm the working directory.
2. Determine whether this is a **generate** (text-to-SVG) or **vectorize** (image-to-SVG) task.
3. Always use `-o <filename>.svg` to save the output to a file so the user can use it.
4. Pick a sensible filename based on the prompt content (e.g., `rocket-icon.svg`).
5. Run the `quiver` command.
6. Read the generated SVG file to verify it was created successfully.
7. Report the result: file path, file size, and a brief summary.

## Arguments Handling

If the user provides arguments directly after `/quiver`, pass them through:

```bash
quiver $ARGUMENTS
```

## Examples

**User says "create a rocket icon":**

```bash
quiver generate -o rocket-icon.svg "a minimalist rocket icon, clean lines, flat design"
```

**User says "make me 3 variants of a logo":**

```bash
quiver generate -n 3 -o logo.svg "a modern tech startup logo with geometric shapes"
```

This produces `logo-1.svg`, `logo-2.svg`, `logo-3.svg` when n > 1.

**User says "convert this image to SVG" with a file path:**

```bash
quiver vectorize -o vectorized.svg --auto-crop ./photo.png
```

**User says "vectorize this URL":**

```bash
quiver vectorize -o output.svg https://example.com/image.png
```

**User says "list available models":**

```bash
quiver models list
```

## Tips

- Always save output to a file with `-o` so the user has a usable artifact.
- Use `--auto-crop` for vectorize when the source image has whitespace or background.
- For icons and simple graphics, a lower temperature (e.g., `-t 0.7`) gives more consistent results.
- For creative/artistic SVGs, a higher temperature (e.g., `-t 1.2`) adds variety.
- Use `-i` instructions to control style: "flat design", "line art", "monochrome", "gradient", etc.
- When generating multiple variants, mention which files were created.
- If `quiver` is not found, tell the user to install it: `npm install -g quiver-ai-cli`
- If auth fails, tell the user to run: `quiver config set api_key <key>`
