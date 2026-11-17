## Description:

Generates YouMind-style illustrated PowerPoint presentations from a user's outline by turning the content into a visual story with recurring character artwork, concise slide copy, image prompts, and PPTX assembly guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoliu166](https://clawhub.ai/user/xiaoliu166)

### License/Terms of Use:

MIT-0

## Use Case:

External users, designers, product teams, and developers use this skill to transform outlines for launches, retrospectives, personal narratives, team updates, and brand stories into illustrated PPTX presentation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create local presentation and image files in the working directory.

Mitigation: Run it in a project or temporary directory that does not contain unrelated slide assets.

Risk: The workflow may install unpinned npm or pip packages when required tooling is missing.

Mitigation: Prefer preinstalled or pinned dependencies and review package installation commands before execution.

Risk: The cleanup workflow can remove local slide image files matching a narrow pattern.

Mitigation: Use a clean workspace and review cleanup commands before running them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaoliu166/skills/youmind-ppt)
- [IP Role Presets](references/ip-presets.md)
- [YouMind Style Prompt Templates](references/prompt-templates.md)
- [Visual Logic Mapping Guide](references/visual-logic.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown workflow instructions with tables, image prompts, code or shell commands, and PPTX file-generation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local presentation files and intermediate image assets when supporting tools are available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
