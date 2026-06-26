## Description: <br>
Semia audits agent skills inside OpenClaw and helps agents run Semia scan workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archidoge0](https://clawhub.ai/user/archidoge0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use Semia to audit agent skills and run Semia scan workflows from an OpenClaw-compatible environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill set is mostly coherent developer guidance, but one review helper defaults to running nested Codex with full local access and sandbox bypass, so it should be reviewed before installation. <br>
Mitigation: Install only if you are comfortable with these skills performing high-impact developer and maintainer workflows. Before using `autoreview`, prefer `--no-yolo` or set `AUTOREVIEW_YOLO=0` unless you intentionally want the nested review process to have full local access. Use the moderation and PR-maintainer skills only with explicit targets, confirmation, and authenticated accounts you intend to use. <br>


## Reference(s): <br>
- [Semia on ClawHub](https://clawhub.ai/archidoge0/semia) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on the semia command-line tool when installed through the declared uv tool package.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
