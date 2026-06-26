# Dev Update: SKILL.md as the Real Interface

**Date:** 2026-03-10 22:10 PST
**Author:** Claude Code (cc-mini)
**Version:** v1.7.4
**Branch:** cc-mini/skill-installer-details

## The Insight

Parker said it plainly: "We're not doing READMEs anymore. This is not for humans."

The human interface is the AI. The AI's interface is the SKILL.md. If the skill doesn't contain everything needed to operate, the AI guesses. And it guesses wrong.

We proved this earlier in the session. Lesa read the toolbox and miscategorized Universal Installer under "Repo Management" because the SKILL.md had no category structure (fixed in v1.7.3). But even after categories, she still couldn't explain what the tools actually do operationally, because the SKILL.md was still a half-README with links and one-liners.

## What We Researched

Parker pointed us to agentcard.sh/agent.txt as a reference. We researched three AI documentation conventions:

1. **llms.txt** (llmstxt.org) ... a directory of links. Points to docs but doesn't contain them. An AI still has to fetch and read multiple files. Good for discovery, not for operation.

2. **agent.txt / AgentCard** (agentcard.sh) ... self-contained operational manual. Everything in one file. An AI reads it and knows how to interact with the service. Closer to what we need, but designed for describing APIs/services, not developer tools.

3. **SKILL.md** (ours) ... YAML frontmatter for machine parsing, then full operational detail. Designed specifically to teach an AI how to use developer tools. Not a pointer to docs. Not a summary. The complete manual.

We took the best from each: the discoverability mindset of llms.txt, the self-contained philosophy of agent.txt, and built SKILL.md as the standard for AI-native developer tool documentation.

## What Changed in v1.7.4

The SKILL.md went from ~140 lines (descriptions + links) to ~475 lines (complete operational manual).

Every one of the 11 tools now has:
- Complete commands with all flags and options
- Step-by-step "what happens when you run it" sequences
- Exact file paths (where it reads, where it writes)
- Safety notes (what it deletes, what it overwrites, what to watch for)
- How it works across different interfaces (CC Hook, OpenClaw Plugin, MCP server)

### Specific additions worth noting:

**Universal Installer** got a full deployment table showing what each of the 6 interfaces does and where it writes. We read the install.js source code and documented that it does `rm -rf` on existing extension directories before copying. That's critical safety information an AI needs before running it.

**Release Pipeline** got all 13 steps documented (step 0: license gate through step 12: branch prune). Every flag, every file it touches, every decision point.

**Identity File Protection** got the exact list of protected files and the definition of "destructive" (replacing >50% of content). Also documented the difference between how the CC Hook and OpenClaw Plugin work.

**MCP section** got complete tool function names for all MCP-enabled tools, so an AI can add them to .mcp.json without guessing.

## The "Teach Your AI" Framing

Parker's directive on the README: the first tool (Universal Installer) says "Teaches your AI to..." explicitly. The rest infer the pattern. You don't need to say "teaches" 11 times. The frame is set once, and a reader (human or AI) carries it forward.

Universal Installer's description changed from a generic "installs tools" to: "Teaches your AI to take anything you build and make it work across every AI interface. You write code in any language. This tool turns it into a CLI, MCP Server, OpenClaw Plugin, Skill, and Claude Code Hook."

## Interface Coverage Table Iterations

We went through several iterations on the table format:

1. **Separate tables per category** ... Parker: "too hard on the eyes"
2. **Single table, bold category divider rows** ... better, but needed numbering
3. **Added numbers 1-11 in a # column** ... Parker liked it
4. **Tried moving categories into the # column, removing numbers** ... Parker: "looks worse, change it back"
5. **Final: numbers + category divider rows, no dashes in empty cells** ... clean and scannable

The lesson: don't overthink table formatting. Numbers give anchoring. Category rows give structure. Empty cells are cleaner than dashes.

## The Standard Going Forward

This is how we think SKILL.md files should be written for any tool in the toolbox:

1. YAML frontmatter with name, version, interface list
2. One-paragraph description of what the tool teaches
3. Complete command reference with all flags
4. Step-by-step operational detail (what happens when you run it)
5. File paths (reads from, writes to)
6. Safety notes (destructive operations, prerequisites)
7. Interface-specific behavior (how it works as CLI vs Hook vs MCP vs Plugin)

The SKILL.md is the source of truth. READMEs exist for humans browsing GitHub. But the AI reads the SKILL.md, and the SKILL.md must be complete.

## Release Notes Standard

We also established that release notes on GitHub should tell the story. Not just "bumped version" or a one-liner from `--notes`. The v1.7.4 release notes explain the thinking, the research, and what changed. This is how releases should read going forward.

Earlier releases (v1.7.1, v1.7.2) shipped with thin notes and we had to go back and manually update them via `gh release edit`. The tool (wip-release) uses the `--notes` flag, which encourages one-liners. For significant releases, we should write RELEASE-NOTES files on the branch and have the tool pick them up.

## Files Changed

- `SKILL.md` ... complete rewrite (140 -> 475 lines)
- `README.md` ... Interface Coverage table: numbered, category dividers, no dashes
- `ai/feedback/2026-03-10--gpt--v1.7.1-readme-review.md` ... GPT rated the README 9.6/10

## wip-release: Auto-Detect Dev Updates as Release Notes

Parker's feedback: "The release notes should be automated. I shouldn't have to keep telling you to do this."

We updated `wip-release` to auto-detect release notes from `ai/dev-updates/`. The priority order:

1. `--notes-file=path` (explicit)
2. `RELEASE-NOTES-v{ver}.md` in repo root
3. `ai/dev-updates/YYYY-MM-DD*` (today's dev update files, most recent first)
4. `--notes="one-liner"` (fallback, but dev updates win if they have more content)

This means: write dev updates as you work (which we already do). When you run `wip-release`, it finds today's dev update and uses it as the full release notes. No more thin one-liners on GitHub releases. No more "this week's sauce, come on, man."

## What's Next

- Consider making the SKILL.md standard a section in the Dev Guide
- Operational guide for agent identities (Parker mentioned needing this)
