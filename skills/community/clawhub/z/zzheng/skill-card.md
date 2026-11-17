## Description:

zzheng generates Chinese WeChat public-account legal articles for personal and enterprise audiences by combining current legal hot topics with preset legal knowledge templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mylillo926](https://clawhub.ai/user/mylillo926)

### License/Terms of Use:

MIT-0

## Use Case:

Legal professionals and content creators use this skill to draft daily Chinese WeChat public-account articles for individual readers and enterprise compliance audiences. Generated legal content should be reviewed for accuracy, jurisdictional fit, and publication readiness before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may contact public Chinese news and social services when optional dependencies are installed.

Mitigation: Run it in an environment where that outbound network access is acceptable, and install dependencies in a virtual environment with pinned versions.

Risk: The skill creates or overwrites dated article files and progress JSON in its configured output directory.

Mitigation: Set the output directory deliberately and review generated files before publication.

Risk: Generated legal articles can be incomplete, outdated, or unsuitable for a specific jurisdiction or client matter.

Mitigation: Have a qualified reviewer check legal accuracy, jurisdictional assumptions, and source relevance before publishing.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown-style Chinese article text saved as dated plain text files, with progress state stored as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces separate personal and enterprise articles; may contact public Chinese news and social services and write or overwrite files in the configured output directory.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
