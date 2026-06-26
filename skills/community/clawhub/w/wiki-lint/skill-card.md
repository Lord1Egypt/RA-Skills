## Description: <br>
Lint and health-check a persistent markdown knowledge wiki for contradictions, stale claims, missing cross-links, orphan pages, duplicate pages, inconsistent naming, inconsistent frontmatter, schema drift, weak source attribution, and other maintenance issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teki-ai](https://clawhub.ai/user/teki-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and knowledge-base owners use this skill to review markdown or git-backed wikis for structural drift, stale or contradictory claims, missing links, duplicate pages, and weak attribution before applying targeted cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad wiki cleanup could introduce incorrect or unwanted markdown changes if edits are accepted without review. <br>
Mitigation: Start with a report-only review for broad wikis and review proposed diffs before accepting cleanup edits. <br>
Risk: Reviewing the wrong repository or wiki could surface irrelevant findings or modify unintended markdown files. <br>
Mitigation: Point the skill only at the wiki or repository intended for maintenance. <br>


## Reference(s): <br>
- [Wiki Lint Checklist](references/lint-checklist.md) <br>
- [ClawHub Wiki Lint Release](https://clawhub.ai/teki-ai/wiki-lint) <br>
- [Publisher Profile](https://clawhub.ai/user/teki-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with severity-grouped findings and concrete fix recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or apply targeted markdown edits when the user asks for cleanup.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
