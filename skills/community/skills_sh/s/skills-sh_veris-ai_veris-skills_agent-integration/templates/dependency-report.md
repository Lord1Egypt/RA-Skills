# Dependency Analysis — Presentation Format

When presenting dependency findings to the user, use this structure. Keep it conversational — explain what you found and what you recommend.

## Agent Summary
- **Name:** {agent_name}
- **Language/Runtime:** {e.g., Python 3.12 / Node.js 20}
- **Architecture:** {single process / multi-process / micro-services / serverless}
- **Entry point:** {command or module path}
- **Port:** {port number}
- **Package manager:** {pip / uv / poetry / npm / pnpm / yarn}

## Dependencies

For each dependency, explain naturally:

### {Dependency Name}
- **What it is:** {DB / cache / queue / API / monitoring / etc.}
- **How the agent uses it:** {specific imports, function calls, config reads — cite files}
- **Recommendation:** {what to do and why}
  - If veris mocks it: "Veris mocks this — your agent's API calls will be transparently intercepted. I'll add it to veris.yaml."
  - If bundling: "I'd install this in the container. It adds ~{X}MB memory / ~{Y}MB to the image. Alternatively, you could point it at an external staging instance."
  - If skipping: "I checked {files} and your agent doesn't import or call this service. It's only present as {reason}. Safe to leave out."
  - If external: "This is too heavy to install locally / not mockable. You'd need to provide a staging URL and credentials."
  - If unsure: "I'm not sure about this one. Here are the options: {A vs B}. What do you think?"

## LLM Provider
- **SDK:** {OpenAI / Anthropic / LangChain / etc.}
- **Note:** Veris automatically intercepts LLM API calls through its proxy. No configuration needed for this.

## Things I Want to Confirm
List any decisions where the user's input matters — bundling vs external, whether something is truly optional, etc.

## Summary Table (optional, for quick reference)

| Dependency | What I Recommend | Notes |
|-----------|-----------------|-------|
| {name} | Veris mock / Install in container / Skip / External / Discuss | {brief reason} |
