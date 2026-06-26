---
name: image-generation
description: Generate illustration images for articles and documentation with a Codex-first workflow, OpenAI API fallback, and Gemini fallback.
---

# Image Generation Skill

Generate illustration images for blog posts, documentation, and technical articles. The workflow is provider-aware:

1. **Codex built-in path first** — when the current agent is Codex and the built-in `image_gen` tool is available, use it directly. This path does not require `OPENAI_API_KEY`.
2. **OpenAI API fallback** — outside Codex, or when the built-in tool is unavailable, use the local script with `OPENAI_API_KEY` if present.
3. **Gemini fallback** — if OpenAI API generation is unavailable or fails, use the same script with `GEMINI_API_KEY` and the existing Gemini image model.

Load provider-specific references only when needed:

- Codex built-in path: `references/codex-built-in.md`
- OpenAI API fallback: `references/openai-api.md`
- Gemini fallback: `references/gemini-api.md`

## When to Use

- User asks to generate an illustration, diagram, concept image, article visual, or documentation visual
- User is writing an article and needs visual explanations for concepts or workflows
- User explicitly asks for a generated raster image

## Step 1: Determine the Image Requirements

Before generating, clarify only what is necessary:

1. **What to illustrate** — the concept, architecture, flow, or scene
2. **Language** — default to English for both prompt and text in image. Only use another language if the user explicitly requests it
3. **Save location** — see "Output Path" below
4. **Style/color preferences** — if user has specific needs, use them; otherwise use the default style

## Step 2: Select the Provider Path

### Path A: Codex Built-In

Use this path when:

- The current agent is Codex
- The built-in `image_gen` tool is available
- The user did not explicitly request API/CLI execution

Read `references/codex-built-in.md`, generate with the built-in tool, then move/copy the final image into the workspace if it is project-bound.

### Path B: Script Auto Fallback

Use this path when:

- The current agent is not Codex
- The built-in tool is unavailable
- The user explicitly asks for API/CLI execution

Run:

```bash
python <skill-root>/scripts/generate_image.py \
  --prompt "your prompt here" \
  --output "/path/to/save/image.png"
```

The script uses `--provider auto` by default:

1. Try OpenAI API when `OPENAI_API_KEY` is set
2. If OpenAI API fails or is not configured, try Gemini when `GEMINI_API_KEY` is set
3. If neither credential is available, report the missing environment variables

## Step 3: Craft the Prompt

### Default Style Prefix

The script automatically prepends this style prefix unless `--style-prefix` or `--no-style` is used:

> Use a clean, modern color palette with soft tones. Minimalist flat illustration style with clear visual hierarchy. Professional and polished look suitable for technical blog articles. No photorealistic rendering. No excessive gradients or shadows.

For the Codex built-in path, include the same style guidance directly in the prompt unless the user requested a different style.

### Prompt Writing Guidelines

- Be specific about visual elements, relationships, and layout
- For technical concepts: describe the components and how they connect
- For architecture diagrams: list the layers/components and data flow direction
- For flow diagrams: describe the steps and direction of flow
- If text labels are needed in the image, spell them out explicitly and keep text short
- Default language is English; use another language only when requested

### Example Prompts

**Architecture diagram:**

```text
A system architecture diagram showing: User sends query to an API Gateway,
which routes to a Vector Database labeled "Milvus" and a generation service.
The Vector Database returns relevant documents, which are combined with the
original query and sent to the generation service for final response generation.
Arrows show data flow direction. Each component is a rounded rectangle with
an icon and label.
```

**Concept illustration:**

```text
A visual comparison of keyword search vs semantic search. Left side shows
keyword search with exact word matching and highlighted matching words.
Right side shows semantic search with a brain icon understanding meaning
and connecting related concepts with dotted lines. A dividing line separates
the two approaches.
```

## Step 4: Parameters

### Default Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Provider | `auto` in script; Codex built-in when available | Codex built-in first, then OpenAI API, then Gemini |
| OpenAI model | `gpt-image-2` | Used by script fallback |
| Gemini model | `gemini-3.1-flash-image-preview` | Used by script fallback |
| Aspect ratio | `3:2` | Landscape, ideal for article illustrations |
| Image size | `1K` | Good balance of quality and cost |
| Style | Minimal, clean, soft tones | Auto-prepended by script |
| Language | English | Prompt and in-image text |

### Script Options

```text
--provider          auto, openai, gemini
--model             Provider model ID for the selected provider
--openai-model      OpenAI model ID, default gpt-image-2
--gemini-model      Gemini model ID, default gemini-3.1-flash-image-preview
--aspect-ratio      1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 9:16, 16:9, 21:9, etc.
--image-size        512, 1K, 2K, 4K
--openai-quality    low, medium, high, auto
--style-prefix      Custom style prefix
--no-style          Skip default style prefix
```

### When to Change Defaults

| Scenario | Change |
|----------|--------|
| Higher quality final asset | `--image-size 2K` or `--openai-quality high` |
| Social media banner | `--aspect-ratio 16:9` |
| Portrait/vertical image | `--aspect-ratio 3:4` or `--aspect-ratio 9:16` |
| Square image | `--aspect-ratio 1:1` |
| User has their own style | `--style-prefix "your style"` or `--no-style` |
| Non-English content | Write prompt in target language |

## Step 5: Determine Output Path

Follow this priority order:

### Priority 1: Context from Current Conversation

If the user is working on a specific markdown file or article:

1. Check where existing images in that article are stored by looking for image references in the `.md` file
2. Save the new image in the same directory as the existing images
3. Use a descriptive filename that matches the existing naming convention

Example: if the article has `![](images/architecture-overview.png)`, save to the same `images/` directory.

### Priority 2: Project Image Directory

If no specific article context but working within a project:

1. Look for existing image directories: `images/`, `assets/`, `static/`, `img/`, `figures/`
2. Save in the most appropriate existing directory
3. If none exists, create an `images/` directory at the project root or under the relevant content directory

### Priority 3: Fallback

If no clear project context:

1. Save to the current working directory
2. Use a descriptive filename: `concept-name-illustration.png`

## Step 6: Verify the Result

After generating:

1. Read the image file to visually verify it matches the user's request
2. If the result is not satisfactory, refine the prompt and regenerate once with targeted changes
3. If the image will be inserted into a markdown file, suggest the markdown syntax: `![alt text](relative/path/to/image.png)`
4. Report which provider path was used and where the final file was saved
