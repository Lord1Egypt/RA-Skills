## Description: <br>
Syncs package.json project metadata such as name, version, description, license, author, and repository into marked README, SPEC, and similar Markdown sections, with i18n and dry-run support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoqw7](https://clawhub.ai/user/guoqw7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to keep repeated project metadata in README, SPEC, and similar Markdown documentation aligned with package.json after releases or metadata changes. It can report stale values in dry-run mode or update marked sections after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scan Markdown files and propose updates across a project, which could change documentation in more places than expected. <br>
Mitigation: Use dry-run or review mode first, inspect the proposed diff, and approve writes only for intended files and fields. <br>
Risk: Incorrect package.json or i18n metadata can be propagated into README, SPEC, or similar documentation. <br>
Mitigation: Confirm package.json and package.nls values before syncing, especially before release documentation updates. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/guoqw7/sync-metadata) <br>
- [Project Homepage](https://github.com/guoqw7/claude-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown file updates and text change summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run checks and user-confirmed writes to marked Markdown sections.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
