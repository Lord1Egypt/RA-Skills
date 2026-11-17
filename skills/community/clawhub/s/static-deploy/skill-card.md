## Description:

Helps agents validate local static-site build outputs, choose a deployment target, publish to CloudStudio Sandbox, EdgeOne Pages, Netlify, Vercel, or GitHub Pages, and verify the deployed URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to publish local static site artifacts that include index.html, compare deployment targets, run preflight checks for entry files and sensitive filenames, and verify the resulting URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing the wrong local directory can expose private or unfinished files.

Mitigation: Review the exact directory and deployment target before execution, and run the preflight check before publishing.

Risk: The sensitive-file check is a filename heuristic and not a complete secret scan.

Mitigation: Use a dedicated secret scan and manually inspect build artifacts before public deployment.

Risk: The documented unpinned npx deployment command can fetch changing tooling.

Mitigation: Prefer pinned deployment tooling or an approved CLI version.

Risk: Local learning history can persist deployment notes, URLs, or preferences.

Mitigation: Avoid recording sensitive details, and clear learned_patterns.json when local telemetry should not persist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/static-deploy)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and deployment target recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON output when the bundled deployment checker is run with --json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
