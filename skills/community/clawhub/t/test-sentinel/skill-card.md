## Description: <br>
Writes and runs tests (unit, integration, E2E), performs linting, and auto-fixes failures <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guifav](https://clawhub.ai/user/guifav) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to plan, write, run, and fix unit, integration, and end-to-end tests for Next.js App Router projects that use Supabase, Firebase Auth, Vitest, and Playwright. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can broadly read and modify project files while writing tests and auto-fixing failures. <br>
Mitigation: Use it on a clean branch and review diffs before accepting changes. <br>
Risk: The artifact includes an automatic commit workflow using git add -A and git commit, which can stage unintended files. <br>
Mitigation: Confirm staged files before any commit and avoid automatic commits unless the exact file set has been reviewed. <br>
Risk: Generated or modified tests can encode brittle assumptions or mask code defects. <br>
Mitigation: Review test plans, mocks, and source fixes, then rerun focused and full test, lint, and type-check commands. <br>


## Reference(s): <br>
- [Test Sentinel on ClawHub](https://clawhub.ai/guifav/test-sentinel) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with code blocks and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify project files and propose or run local Node test, lint, format, and type-check commands.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata; artifact CHANGELOG.md and claw.json report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
