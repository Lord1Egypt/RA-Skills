## Description:

Conducts focused or parallel technical research and weekly technology radar scans, using Dify knowledge and web sources to produce structured reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahsh](https://clawhub.ai/user/mahsh)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud phone developers and engineers use the skill to investigate technologies, compare implementation options, and track relevant technical changes. It produces structured research reports with recommendations tailored to cloud phone work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may start research for topics outside the intended scope.

Mitigation: Review the requested topic and scope before starting a research run.

Risk: External searches may disclose query terms in confidential research context.

Mitigation: Keep confidential details out of web queries and use local knowledge sources for sensitive topics.

Risk: The security scan could not assess two referenced memory paths because they were missing.

Mitigation: Confirm the referenced paths exist and inspect their contents before relying on them.

## Reference(s):

- [Research guide](references/research_guide.md)
- [WebRTC blog](https://webrtc.org/blog/)
- [Chromium blog](https://blog.chromium.org/)
- [Android Developers blog](https://android-developers.googleblog.com/)
- [FFmpeg release tags](https://api.github.com/repos/FFmpeg/FFmpeg/tags?per_page=10)
- [Google Cloud blog](https://cloud.google.com/blog/)

## Skill Output:

**Output Type(s):** [Markdown, Research guidance, Files]

**Output Format:** [Structured Markdown reports with comparison tables, recommendations, risks, and source URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are archived locally under memory/research/ with an updated index; Dify knowledge base updates are left to the user.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
