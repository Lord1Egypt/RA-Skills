# README Patterns: Tool-Type Repositories

Based on analysis of: ripgrep, bat, fzf, GitHub CLI, Caddy, Traefik, Meilisearch

Tool repos are software that end users run directly — CLI utilities, servers, desktop apps, search engines. Their README needs to make someone install and try the tool in under 5 minutes.

---

## Structure Template

```
1. Centered logo (dark/light mode)
2. Navigation menu (links to sections or external pages)
3. Badges (build, version, license, community)
4. Tagline
5. Demo GIF or hero screenshot
6. Features list (with brief explanations)
7. Installation (platform-specific)
8. Usage (real commands + output)
9. Integration with other tools (if applicable)
10. Configuration (brief, link to full docs)
11. Documentation
12. Contributing
13. License
```

---

## What Makes Tool READMEs Work

### 1. Lead with the Sensory Experience
People choose tools based on how they *feel* to use. Show output, not just description.

- **bat**: Multiple screenshots showing syntax highlighting, git diffs, special characters — you *see* what you're getting
- **fzf**: Animated GIF of fuzzy finding in action is the very first thing after the title
- **Meilisearch**: Demo GIF + 5 live example apps (movies, e-commerce, photos)
- **Traefik**: Architecture diagram + Web UI screenshot

If your tool has a visual output, the GIF or screenshot should appear before the features list.

### 2. Comparative Positioning
If your tool replaces something, say so immediately:

```markdown
# ripgrep (rg)
ripgrep is a line-oriented search tool that recursively searches the current directory for
a regex pattern while **respecting gitignore rules** and automatically skipping hidden files.
It is similar to grep, ag, and ack, but with significant performance improvements.
```

Patterns:
- "Like X, but Y" (ripgrep)
- "Replaces X with better Z" (bat = "cat clone with syntax highlighting")
- Explicit comparison tables (ripgrep vs grep vs ag)
- Performance benchmarks (ripgrep benchmarks are central to the README)

### 3. Platform-Specific Installation
Tools are installed, not imported. Cover every common platform:

```markdown
## Installation

**macOS**: `brew install mytool`
**Linux (Debian/Ubuntu)**: `apt install mytool`
**Windows**: `winget install mytool` or `scoop install mytool`
**Cargo/npm/pip**: `cargo install mytool`
**From release**: [GitHub Releases](https://github.com/owner/repo/releases)
**From source**: See [building from source](docs/build.md)
```

Model: **bat** covers Ubuntu, Alpine, Arch, Fedora, Gentoo, FreeBSD, OpenBSD, nix. **fzf** covers Homebrew, 12+ Linux distros, Windows (4 options), from git, binary releases.

If installation is complex, link to external docs rather than embedding 100+ lines.

### 4. Integration Showcase
Top tool READMEs have a dedicated section showing integrations with other tools:

**bat** has: bat + fzf, bat + ripgrep, bat + git log, bat + man, bat + tail, bat + xclip, bat + delta, bat + lessopen

**fzf** has: vim/neovim plugin, bash/zsh/fish integration, tmux integration

Why this matters: it shows the tool fits into existing workflows, and gives users immediate inspiration for how to use it.

Structure each integration as:
```bash
# What this does in one sentence
some-tool --option | mytool --flag
```

### 5. Transparency About Trade-offs
The most trusted tool READMEs are honest about limitations:

ripgrep has a "Why shouldn't I use ripgrep?" section! This builds credibility and helps users make an informed choice.

Consider adding: "This tool is NOT the right choice if..." or "Known limitations:..."

### 6. Navigation Menu
For long READMEs, add a navigation menu near the top:

```markdown
[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Docs](https://docs.example.com)
```

Or use a proper Table of Contents (fzf uses vim-markdown-toc generated TOC).

---

## Section-by-Section Examples

### Hero GIF/Screenshot
```markdown
<p align="center">
  <img src="doc/demo.gif" alt="Demo" width="700">
</p>
```

For dark/light mode:
```markdown
<p align="center">
  <img src="assets/logo-light.svg#gh-light-mode-only" width="400">
  <img src="assets/logo-dark.svg#gh-dark-mode-only" width="400">
</p>
```

### Performance / Comparison Table
When speed or capability is a key differentiator, include a comparison table:

```markdown
| Feature | mytool | competitor1 | competitor2 |
|---|---|---|---|
| Speed | ⚡ 2.5x faster | baseline | 1.2x faster |
| Respects .gitignore | ✅ | ❌ | ✅ |
| Unicode support | ✅ | ✅ | ❌ |
```

### Integration Examples (Tool + Other Tool)
```markdown
## Integration with Other Tools

**With fzf** — fuzzy find and preview:
```bash
rg --files | fzf --preview 'bat --color=always {}'
```

**With git** — show changed files:
```bash
git diff --name-only | xargs bat
```
```

### Getting Help / Support
```markdown
## Getting Help

- 📖 [Documentation](https://docs.example.com)
- 💬 [Discord Community](https://discord.gg/example)
- 🐛 [Bug Reports](https://github.com/owner/repo/issues)
- 🔒 [Security Issues](SECURITY.md) — please don't use public issues
```

---

## Common Mistakes to Avoid

- ❌ Hiding the demo — put visuals near the top, not buried in "Features"
- ❌ Installation wall — don't put a 50-line installation guide before explaining what the tool does
- ❌ Only showing basic usage — show at least one "power user" example
- ❌ Skipping the comparison — if users are switching from another tool, acknowledge it
- ❌ No output shown — always show what the tool actually outputs

---

## Tone & Voice

Tool READMEs tend to be:
- **Direct and efficient** — no fluff, get to the point
- **Technical but accessible** — assume developer audience, avoid jargon for jargon's sake
- **Confident without being arrogant** — state clearly what your tool does better

ripgrep's tone is exemplary: technical, precise, benchmarks included, honest about trade-offs.

---

## Sponsor Section (Optional)

For mature tools with a sponsor/backers program:
```markdown
## Sponsors

Thanks to [Warp](https://warp.dev) for sponsoring this project.

<a href="https://warp.dev"><img src="https://example.com/warp-logo.png" width="200"></a>
```

Place this after the demo/features, before or after installation.
