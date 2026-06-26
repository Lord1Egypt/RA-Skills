# Platform Compatibility

Brain/Hands/Session separation is platform-agnostic. Adapt the file structure to your platform's conventions.

| Platform | Skill Manifest | Scripts Directory | Notes |
|----------|---------------|-------------------|-------|
| **WorkBuddy** | `SKILL.md` | `scripts/` | Native support, `read_when` triggers |
| **ClawHub** | `SKILL.md` | `scripts/` | Open marketplace |
| **OpenAI GPTs** | Instructions + Functions | Code Interpreter | Map concepts to GPT architecture |
| **Anthropic Claude** | System Prompt + Tools | External functions | Brain=system prompt, Hands=tools |
| **LangChain** | Chain definition | Runnable lambdas | Patterns map to LCEL |
| **Custom Agents** | Agent config | Tool implementations | Architecture principles universal |
