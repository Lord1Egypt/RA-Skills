## Description:

Writes and runs tests across unit, integration, and end-to-end layers, performs linting, and auto-fixes failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guifav](https://clawhub.ai/user/guifav)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to add, run, and repair tests for Next.js App Router projects, with attention to Vitest, Playwright, Supabase, Firebase Auth, linting, and TypeScript checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically modify source files while repairing failed tests or lint issues.

Mitigation: Use it in a clean working tree and review diffs before accepting changes.

Risk: The skill may run npm-based tools through npx, which can execute locally resolved or downloaded packages.

Mitigation: Use locked local development dependencies and review command output before trusting results.

Risk: The artifact describes committing broad repository changes after fixes.

Mitigation: Inspect git status and staged diffs before allowing any commit.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guifav/skills/test-sentinel)
- [Publisher Profile](https://clawhub.ai/user/guifav)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, test files, source edits, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify tests and source files, run local test and lint commands, and propose commits when appropriate.]

## Skill Version(s):

0.1.2 (source: server release metadata; artifact claw.json and CHANGELOG report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
