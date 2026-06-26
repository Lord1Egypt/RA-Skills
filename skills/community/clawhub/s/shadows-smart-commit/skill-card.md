## Description: <br>
Intelligent git commit assistant that analyzes diffs, enforces conventional commits, checks for common secret patterns, and generates commit messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NakedoShadow](https://clawhub.ai/user/NakedoShadow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering agents use this skill to inspect local Git changes, stage explicit files, scan staged diffs for common secret patterns, and create conventional commits with a proposed message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can stage files and create local Git commits. <br>
Mitigation: Review the staged files, generated commit message, and exact Git commands before allowing a commit. <br>
Risk: Secret-like values may appear in terminal output during grep-based staged-diff checks. <br>
Mitigation: Run the workflow in a trusted terminal and stop if the scan reports sensitive files or secret matches. <br>
Risk: The fixed co-author trailer may not match every repository's authorship policy. <br>
Mitigation: Confirm or edit the commit message and trailer before committing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NakedoShadow/shadows-smart-commit) <br>
- [Publisher profile](https://clawhub.ai/user/NakedoShadow) <br>
- [Metadata homepage](https://clawhub.ai/NakedoShadow) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes changed-file summary, security scan result, proposed commit message, explicit files to stage, and post-commit status.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
