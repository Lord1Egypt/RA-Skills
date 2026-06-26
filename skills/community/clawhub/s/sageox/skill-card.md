## Description: <br>
Sageox helps agents query SageOx team knowledge, manage AI coworkers, run distillation and summaries, review coworker activity, catch up after time away, and import or export knowledge across configured repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avi-ox-agola](https://clawhub.ai/user/avi-ox-agola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and team operators use Sageox inside compatible agent environments to search team context, coordinate expert AI coworkers, synthesize recent activity, and manage knowledge import or export workflows across selected repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repo, team, recording, or OpenClaw memory data may be sent to SageOx or Claude during import, distill, summary, or catchup workflows. <br>
Mitigation: Confirm the data scope before those actions, avoid importing sensitive material without authorization, and review selected repositories and state files under ~/.openclaw/memory. <br>
Risk: The skill requires credentials and access to SageOx, GitHub, Claude CLI, selected repositories, and selected OpenClaw memory files. <br>
Mitigation: Use the skill only in trusted workspaces, verify the active authentication context before running commands, and limit repository access to the teams being supported. <br>
Risk: The ox install flow adds a pinned downloaded executable to the user's local PATH. <br>
Mitigation: Review the bundled install script, keep the pinned checksum verification intact, and confirm PATH resolves ox to the expected local install before use. <br>


## Reference(s): <br>
- [SageOx homepage](https://sageox.ai) <br>
- [ClawHub skill page](https://clawhub.ai/avi-ox-agola/sageox) <br>
- [Query - Search Team Knowledge](references/query.md) <br>
- [Coworkers - Expert Agent Management](references/coworkers.md) <br>
- [Distill - Interactive Single-Repo Distillation](references/distill.md) <br>
- [Distill Pipeline - Multi-Repo Automated Distillation](references/distill-pipeline.md) <br>
- [Summary - Cross-Team Activity Summary](references/summary.md) <br>
- [Glance - Real-Time AI Coworker Activity](references/glance.md) <br>
- [Catchup - What Happened While You Were Away](references/catchup.md) <br>
- [Import/Export - Knowledge Bridge](references/import-export.md) <br>
- [Installing and Configuring ox](references/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with shell command snippets and JSON or configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some summaries are formatted for Slack mrkdwn; several workflows call ox, gh, git, jq, and claude from a selected repository.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
