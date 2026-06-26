---
name: xhs-comic-creator
description: Generate educational comic-style Xiaohongshu posts using AI-generated comic images. Includes topic research, storyboard creation, image generation, and automated publishing.
metadata:
  requires:
    - GEMINI_API_KEY: API key for image generation (nano-banana-pro)
    - TAVILY_API_KEY: API key for tavily search
    - xiaohongshu_cookies_path: path to Xiaohongshu login cookies JSON (for publishing)
    - node_version: ">=18.0"
    - python_version: ">=3.12"
  dependencies:
    - nano-banana-pro
    - xiaohongshu-mcp
    - playwright-mcp
    - tavily-search
---

# Xiaohongshu Comic Post Skill

This skill generates an educational comic-style Xiaohongshu post from a topic.

The workflow includes:

1. Topic research
2. Knowledge summarization
3. Comic storyboard creation
4. Image generation
5. Xiaohongshu post publishing

For the complete workflow read:

`references/workflow.md`

---

## Output Format

The final result must include:

- Title
- Text content
- 5-6 comic images
- Xiaohongshu post

Images must be generated before publishing.

---

## Image Generation

Requires installing the image generation skill:

```bash
npx clawhub@latest --workdir {your_agent_workspace_dir} install nano-banana-pro
```

**`GEMINI_API_KEY` must be set to enable image generation.**

```bash
export GEMINI_API_KEY="your_gemini_api_key"
```

Call skill `nano-banana-pro` with:
  - prompt
  - image_count

Requires installing the searching skills:

```bash
npx clawhub@latest --workdir {your_agent_workspace_dir} install tavily-search
npx clawhub@latest --workdir {your_agent_workspace_dir} install playwright-mcp
```

**`TAVILY_API_KEY` must be set to use tavily.**

```bash
export TAVILY_API_KEY="your_tavily_api_key"
```

Prompt construction rules are described in:

`references/comic_generation.md`

---

## Xiaohongshu Publishing

Requires installing the Xiaohongshu MCP skill:

```bash
npx clawhub@latest --workdir {your_agent_workspace_dir} install xiaohongshu-mcp
```

Xiaohongshu login cookies must be exported and saved as:

`~/.xiaohongshu/cookies.json`

Call skill `xiaohongshu` with:
  - title
  - content
  - images

Posting procedure is described in:

`references/xhs_posting.md`

---

## Quality Requirements

Posts must:

- be educational
- feel natural and human-written
- avoid spam-like tone
- use friendly storytelling

Images must:

- look like anime tactical comic style
- contain multiple panels
- include speech bubbles when appropriate