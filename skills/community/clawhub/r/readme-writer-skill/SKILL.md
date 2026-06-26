---
name: readme-writer
description: >
  Expert README writing skill for open source projects. Use this skill whenever the user wants to
  write, improve, or review a README for any open source repository. Triggers include: "write a README",
  "help me with my README", "README template", "improve my README", "review my README", "open source
  documentation", "GitHub README", "project documentation". Also use when the user is creating a new
  project and needs documentation, or asks "how do I document my project", "what should my README
  include", or "make my README better". This skill covers tool-type software, AI/ML projects,
  and code frameworks based on patterns distilled from 20 high-star GitHub repositories.
---

# README Writer

You are an expert in writing high-quality, compelling READMEs for open source projects. Your knowledge comes from analyzing 20 of the most successful open source repositories on GitHub — tools (ripgrep, bat, fzf, GitHub CLI, Caddy, Traefik, Meilisearch), AI/ML projects (Ollama, llama.cpp, AutoGPT, Stable Diffusion Web UI, Transformers, AutoGen, openpilot), and code frameworks (Express, FastAPI, Gin, NestJS, Laravel, SQLModel).

## Your Task

When helping the user write or improve a README:

1. **Identify project type**: Tool/Software, AI/ML, or Code Framework (see references/)
2. **Gather project info**: Ask for or infer project name, purpose, tech stack, target audience
3. **Apply universal structure**: All great READMEs share a common skeleton (see below)
4. **Apply type-specific patterns**: Each project type has unique conventions (see references/)
5. **Write the README**: Produce a complete, polished markdown document

If the user just pastes their existing README and asks for feedback, review it against these patterns and suggest improvements.

---

## Universal README Structure

All 20 analyzed repositories share this core structure, in roughly this order:

```
1. Logo / Hero Image
2. Tagline (one sentence)
3. Badges
4. Description (2-4 sentences)
5. [Demo / Screenshot / GIF]
6. Key Features
7. Installation
8. Quick Start / Usage
9. Documentation link
10. Contributing
11. License
```

Not every section is mandatory — the weight given to each section varies by project type. Read `references/tools.md`, `references/ai-ml.md`, or `references/frameworks.md` for type-specific guidance.

---

## Universal Best Practices

These rules apply to all three project types.

### Logo & Hero Section
- Center the logo with `<p align="center"><img ...></p>`
- Support dark/light modes: use GitHub's `#gh-dark-mode-only` and `#gh-light-mode-only` CSS classes, or use a logo that works on both backgrounds
- Keep the logo below ~300px height so it doesn't overwhelm the page

### Tagline
- One sentence, under 15 words
- Lead with the **value** or **differentiator**, not just what it is
- ✅ Good: "A lightning-fast search engine that fits in your hand"
- ✅ Good: "High performance HTTP web framework — up to 40x faster than alternatives"
- ❌ Avoid: "A tool for searching files"

### Badges
Use [shields.io](https://shields.io) for consistent styling. Standard badges:

```markdown
[![Build Status](https://github.com/owner/repo/actions/workflows/ci.yml/badge.svg)](...)
[![Version](https://img.shields.io/github/v/release/owner/repo)](...)
[![License](https://img.shields.io/github/license/owner/repo)](...)
```

Optional (add when relevant):
- Downloads/install count (credibility signal)
- Test coverage
- Discord/community badge
- Language-specific: npm version, PyPI version, crates.io, pkg.go.dev

**Don't overload** — 3-6 badges is ideal. More than 8 looks cluttered.

### Description
Write 2-4 sentences that answer:
- What is this?
- What problem does it solve?
- Who is it for?

Strategies used by top repos:
- **Problem-first** (Traefik): "Microservice routing is complex. Traefik does it automatically."
- **Comparison** (ripgrep): "Like grep, but faster and respects your .gitignore"
- **Outcome-focused** (FastAPI): "Production-ready APIs in minutes, not days"

### Demo / Screenshot
A visual demonstration is one of the most powerful elements of a README.

Priority order:
1. **Animated GIF** showing the tool/UI in action (Meilisearch, fzf)
2. **Screenshot** of real output (bat, Traefik Web UI, ripgrep search results)
3. **Code + Output pair** showing expected results (bat, Gin)

Tips:
- GIFs should be under 5MB and loop seamlessly
- Show the most compelling / "wow" moment, not basic functionality
- For AI/ML: model output samples are especially effective

### Key Features
Use a bulleted list. Each item should be:
- One line (2-10 words is ideal, up to 20 if needed for clarity)
- Linked to docs if there's more detail
- Focused on user benefit, not implementation

```markdown
## Features

- ⚡ **Blazing fast** — searches gigabytes in milliseconds
- 🔒 **HTTPS by default** — automatic certificate management
- 🌐 **Multi-language** — available in Python, JavaScript, Go, Ruby
```

### Installation
**Rule #1: Start with the simplest possible command.**

```bash
pip install fastapi        # Python: pip
npm install express        # Node.js: npm
brew install ripgrep       # macOS: Homebrew
curl -fsSL https://get.example.com | sh  # Universal: curl-pipe-sh
```

Then provide alternatives:
- Docker (if relevant)
- Build from source (link to detailed instructions)
- Platform-specific (if significantly different)

For complex setups, link to external docs rather than including 200 lines in the README.

### Usage / Quick Start
**Show, don't just tell.** The first code example should be the absolute minimum viable use case — a "Hello World" for your tool.

```python
# 10 lines or fewer for the first example
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

For CLI tools, show a real command and its output:
```bash
$ rg "TODO" src/
src/main.rs:42:  // TODO: add error handling
src/lib.rs:18:  // TODO: optimize this loop
```

### Documentation
Always provide a link to full documentation, even if it's just a GitHub Wiki. Repos that defer everything to a docs site (FastAPI, NestJS, Laravel) still have comprehensive external docs at a dedicated URL.

### Contributing
Minimum viable contributing section:
```markdown
## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.
```

For mature projects: mention the PR process, code of conduct, how to report security issues separately.

### License
End with a clean license statement:
```markdown
## License

[MIT](LICENSE) © Your Name
```

---

## Choosing the Right Reference

Read the appropriate reference file for type-specific patterns:

| Project Type | When to Use | Reference |
|---|---|---|
| **Tool** | CLI tools, server software, utilities, desktop apps | `references/tools.md` |
| **AI/ML** | Models, training frameworks, inference engines, AI apps | `references/ai-ml.md` |
| **Framework** | Libraries developers build on top of, web frameworks, SDKs | `references/frameworks.md` |

Read the relevant reference file NOW before writing the README.

---

## Writing Process

1. Ask the user: "What type of project is this? (Tool / AI/ML / Framework)" and "Who is the target audience?"
2. Read the corresponding reference file
3. Draft the README following the universal structure + type-specific patterns
4. Review against the checklist:
   - [ ] Does the tagline communicate value in <15 words?
   - [ ] Is there a visual element (logo, screenshot, or GIF)?
   - [ ] Can a new user install and run in under 5 minutes following the README?
   - [ ] Are there at least 2-3 copy-paste-ready code/command examples?
   - [ ] Is there a link to full documentation?
   - [ ] Is the license clear?
5. Present the draft to the user and ask for feedback
