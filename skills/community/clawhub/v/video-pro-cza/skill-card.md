## Description:

Professional AI video-generation skill for creating short videos from text with batch generation, templates, and commercial licensing features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cza999](https://clawhub.ai/user/cza999)

### License/Terms of Use:

Commercial software - license required

## Use Case:

Content creators, marketers, educators, and businesses use this skill to generate single or batch short videos from scripts, apply templates, select voices, and manage licensed premium features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs mutable external code from the openclaw-video repository at install time.

Mitigation: Install and run it only in a sandbox or separate account after reviewing and pinning the external repository revision.

Risk: Scripts and generated content may be sent to OpenAI or the vendor API and are also written to local logs.

Mitigation: Do not use sensitive, confidential, or regulated scripts; review log retention and delete generated logs when no longer needed.

Risk: License keys are stored and printed in local files during activation.

Mitigation: Treat license keys as locally exposed secrets, restrict file permissions, and rotate keys if they are shared or checked into another system.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cza999/skills/video-pro-cza)
- [Video Pro Template System](artifact/templates/README.md)
- [Video Pro Documentation](https://docs.video-pro.cza999.com)
- [Video Pro Template Documentation](https://docs.video-pro.cza999.com/templates)
- [OpenClaw Video Dependency](https://github.com/ZhenRobotics/openclaw-video.git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, JSON, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent to install external video-generation tooling, set API and license environment variables, run generation scripts, and locate generated MP4 files and reports.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
