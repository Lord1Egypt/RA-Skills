# Contributing to The Founder's Playbook

Thanks for considering contributing! This is an Agent Skill based on Anthropic's "The Founder's Playbook: Building an AI-Native Startup," adapted for any AI agent.

## Guidelines

1. **Keep it platform-agnostic** — No references to specific AI products (Claude, ChatGPT, Copilot, Gemini, etc.) in the skill logic. Use "your AI agent" or "agentic tools."
2. **Preserve the stage framework** — The 4 stages (Idea → MVP → Launch → Scale) are the backbone. Additions should fit within this structure.
3. **Exercises should be actionable** — Each exercise must be something a founder can do with an AI agent in one session.
4. **YAML frontmatter** — Ensure valid YAML and the `name` field matches the directory name.

## Pull request process

1. Fork the repo
2. Make your changes
3. Run `node --check tools/*.js` if you add CLI tools
4. Submit a PR with a clear description of what changed and why

## License

By contributing, you agree that your contributions will be licensed under MIT-0.
