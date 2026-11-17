## Description:

SuperClaw is a bundle of 14 agent workflow skills for disciplined AI coding across TDD, debugging, code review, planning, brainstorming, verification, subagent dispatch, and related development workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gvuckovich](https://clawhub.ai/user/gvuckovich)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill bundle to structure software work with repeatable workflows for planning, TDD, debugging, review, verification, worktree isolation, subagent coordination, and skill authoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow skills can lead an agent to make persistent repository changes, including file edits, commits, worktree changes, and skill edits.

Mitigation: Install only from a trusted publisher, work in an isolated branch or worktree, and review file changes, commits, and skill edits before accepting them.

Risk: The optional browser companion can be exposed beyond localhost if configured with a non-loopback bind host.

Mitigation: Keep the companion on localhost or place it behind an authenticated tunnel, and avoid exposing it on a public interface.

Risk: Brainstorming companion session files may contain project or design details that should not be published.

Mitigation: Keep `.superpowers/brainstorm` out of releases and source control unless the contents have been intentionally reviewed for publication.

Risk: The bundle is third-party content with a low trust-tier quality signal in server metadata.

Mitigation: Pin the installer version and review the skill behavior against local repository policy before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gvuckovich/skills/superclaw-skills)
- [SuperClaw README](artifact/README.md)
- [Codex Tool Mapping](artifact/using-superpowers/references/codex-tools.md)
- [Gemini CLI Tool Mapping](artifact/using-superpowers/references/gemini-tools.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to create or edit files, run verification commands, use git worktrees, and dispatch subagents when available.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
