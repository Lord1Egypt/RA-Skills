## Description: <br>
Generate concise, safety-aware repository orientation briefs with @builtbyecho/repo-agent-brief/agent-brief before coding-agent work, reviews, handoffs, PR analysis, unfamiliar repo edits, diff-aware branch handoffs, or when an agent needs stack/commands/context/risk signals before changing files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[builtbyecho](https://clawhub.ai/user/builtbyecho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to produce a first-pass repository brief before editing, reviewing, delegating, or handing off work in unfamiliar or changed repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated briefs can include code or configuration snippets from private repositories. <br>
Mitigation: Review generated brief files before sharing them outside the workspace, and use no-snippet or machine-readable workflows when sensitive content should be minimized. <br>
Risk: The skill is not a full secret scanner and may only flag obvious risky patterns. <br>
Mitigation: Use a dedicated scanner such as Gitleaks or TruffleHog for full secret-audit workflows, and inspect high-risk findings before proceeding. <br>
Risk: Running the skill invokes an npm-hosted CLI against the current repository. <br>
Mitigation: Review the command being run, execute it from the intended repository root, and inspect generated files before using them in agent handoffs or CI. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown briefs, JSON reports, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write AGENT_BRIEF.md, AGENT_HANDOFF.md, agent-brief.json, or bundled .agent-brief files depending on the selected command.] <br>

## Skill Version(s): <br>
0.4.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
