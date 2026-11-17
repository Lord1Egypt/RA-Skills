## Description:

Explicitly invoked Uncle Matt local project generator: asks for off-limits paths, scans only allowed project/workspace evidence, diagnoses repeated patterns, and builds one fresh-folder runnable counter-move.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uncmatteth](https://clawhub.ai/user/uncmatteth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users invoke this skill when they want an agent to inspect allowed local project/workspace evidence, identify repeated creative patterns, and build one fresh runnable project in a new folder. The workflow emphasizes explicit scan boundaries, concise progress, local verification, and optional review tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect broad local project or workspace evidence to infer creative patterns.

Mitigation: Set concrete off-limits paths and avoid broad scan permission on machines containing client, private, or sensitive work.

Risk: Optional AutoReview, ClawPatch, or missing-tool installs can introduce external tooling decisions.

Mitigation: Approve optional review tools or installs only after confirming the named tool, source, and current package metadata are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uncmatteth/skills/unclematts-build-me-something-anything)
- [Unattended orchestration reference](references/unattended-orchestration.md)
- [Review closeout reference](references/review-closeout.md)
- [OpenClaw AutoReview helper](https://github.com/openclaw/agent-skills/tree/main/skills/autoreview)
- [ClawPatch package](https://www.npmjs.com/package/clawpatch)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown progress and final handoff with generated project files, code, commands, and configuration as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one local runnable project in a fresh folder and may include context notes, asset plans, verification results, and review closeout details.]

## Skill Version(s):

7.420.70 (source: server release metadata; artifact SKILL.md body says 7.420.69)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
