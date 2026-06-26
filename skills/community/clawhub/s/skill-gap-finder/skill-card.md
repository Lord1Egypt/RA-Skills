## Description: <br>
Scans existing skill bundles to identify duplicate responsibilities, coverage gaps, conflicts, and priority areas for new skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and skill publishers use this skill to audit a local skills directory, understand distribution and overlap, and prepare reviewable publishing recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the folder path supplied by the user, which can expose private notes, secrets, or unrelated project files in generated reports. <br>
Mitigation: Run it only against the specific skills directory intended for review, avoid broad home or repository roots, and redact sensitive material before sharing reports. <br>
Risk: Generated gap and publishing recommendations may be incomplete or misleading when the input directory is partial or stale. <br>
Mitigation: Treat the report as a review draft, confirm the scanned inputs, and inspect the pending confirmations before acting on recommendations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/skill-gap-finder) <br>
- [Publisher Profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Specification](artifact/resources/spec.json) <br>
- [Artifact Output Template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown report by default, with optional JSON output from the support script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are structured around distribution, duplicate responsibilities, gaps, conflicts, priority additions, publishing advice, and pending confirmations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
