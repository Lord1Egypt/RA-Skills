# QuickTicket

Turn an idea or project into small, scoped tickets in the right order. QuickTicket checks relevant prior art, saves the plan and gives you a clear next step.

## Install and use

[Download the skill ZIP](https://github.com/RedRookAI/openclaw-skills/releases/download/quickticket-v0.1.0/quickticket-0.1.0.zip), or give your OpenClaw this message:

> Install QuickTicket from https://github.com/RedRookAI/openclaw-skills/tree/main/skills/quickticket into my workspace's skills/quickticket folder, including all bundled files. Preserve my existing instructions, tickets and model settings.

Or copy this whole folder into your workspace as `skills/quickticket`. Start a new chat if the skill does not appear.

Then say:

> Quickticket this project.

Describe the idea or refer to a project already in the conversation. You can also say "Use QuickTicket on this." Where your agent supports it, `$quickticket` is an optional shortcut.

Use it to plan a new project, turn a feature request into work, or reconcile an existing backlog after requirements change. It follows your project's ticket conventions; otherwise it saves Markdown tickets and an index under `tickets/<initiative>/`.

QuickTicket creates the plan. To start work, ask your implementing agent to work through it. Installation does not edit AGENTS.md, SOUL.md or model settings. If you customized an existing QuickTicket folder, review updates before replacing it.

## Use as a prompt

Paste [QUICK-TICKET.md](QUICK-TICKET.md) into a chat, followed by your idea, project context or requested changes.

[Examples](EXAMPLES.md) show a single repair and a project split into several tickets.

## References

- Related planning tools: [Spec Kit](https://github.com/github/spec-kit), [Task Master](https://github.com/eyaltoledano/claude-task-master), [OpenSpec](https://github.com/Fission-AI/OpenSpec).
- Scope and decomposition: [Story splitting](https://agilealliance.org/glossary/story-splitting/), [Spec Kit's feature decomposition](https://github.github.io/spec-kit/concepts/spec-of-specs.html).
- Requirements and coverage: [Can LLMs Generate User Stories and Assess Their Quality?](https://arxiv.org/abs/2507.15157), [Automated Alignment between Elicitation Interviews and Requirements](https://arxiv.org/abs/2510.08622), [ReqElicitGym](https://arxiv.org/abs/2602.18306).
- Acceptance and recovery: [SWE-Gate](https://arxiv.org/abs/2609.04167), [Runtime-Structured Task Decomposition](https://arxiv.org/abs/2605.15425).
- Non-engineer use: [Feasibility of AI-Assisted Programming](https://arxiv.org/abs/2512.05666), [Non-programmers Assessing AI-Generated Code](https://arxiv.org/abs/2508.06484), [Novice engagement with vibe coding](https://arxiv.org/abs/2512.02750).
- External instructions and persistence: [SkillJect](https://arxiv.org/abs/2602.14211), [Bad Memory](https://arxiv.org/abs/2607.14611), [Prompt-injection guidance](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks).
- Delivery example: [Development previews and publishing](https://docs.replit.com/build/publish-your-app).
- Skill format and setup: [Agent Skills](https://agentskills.io/specification), [OpenClaw skills](https://docs.openclaw.ai/tools/skills).

Version 0.1.0. [MIT-0 license](LICENSE).
