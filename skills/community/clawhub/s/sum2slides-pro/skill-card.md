## Description:

Sum2Slides Pro helps agents convert text summaries, meeting notes, research reports, and project updates into structured PowerPoint presentations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and business teams use this skill to turn plain text or Markdown content into editable PPTX slide decks through a command-line workflow or Python API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated presentation files may overwrite existing output paths.

Mitigation: Review output paths before conversion and write to a dedicated output directory when processing batches.

Risk: Unpinned dependency ranges can change runtime behavior in production environments.

Mitigation: Install in a virtual environment and use pinned or locked dependencies for production deployments.

Risk: Default language behavior may not match non-Chinese user expectations.

Mitigation: Explicitly set language options where available before generating decks.

## Reference(s):

- [Sum2Slides Pro ClawHub Page](https://clawhub.ai/wwumit/skills/sum2slides-pro)
- [Sum2Slides Documentation](https://sum2slides.readthedocs.io/)
- [python-pptx](https://github.com/scanny/python-pptx)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with CLI commands, Python API examples, YAML configuration, and generated PPTX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces editable PowerPoint presentations from local text or Markdown input.]

## Skill Version(s):

1.5.0 (source: release evidence, artifact changelog, and package __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
