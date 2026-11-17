## Description:

rd-ip-accelerator helps R&D and IP teams run patent litigation intelligence, competitor monitoring, freedom-to-operate analysis, solution exploration, novelty search, and technical disclosure workflows from company or invention inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, R&D teams, and IP practitioners use this skill to coordinate patent-risk awareness, competitive IP monitoring, FTO review, invention exploration, novelty searching, and technical disclosure drafting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive company, product, or invention details may be sent to configured external PatSnap/Zhihuiya services during patent and IP workflows.

Mitigation: Use explicit prompts, confirm account and API handling before sharing sensitive inputs, and avoid entering trade secrets unless the data path is acceptable.

Risk: The skill may automatically create persistent HTML, PDF, Excel, or Word report files from R&D inputs.

Mitigation: Review generated files for sensitive content and delete session artifacts that should not be retained.

Risk: Automated IP reports and recommendations may be incomplete or unsuitable for legal decisions.

Mitigation: Have qualified IP or legal reviewers validate outputs before relying on them for filing, FTO, litigation, or licensing decisions.

## Reference(s):

- [PatSnap open platform](https://open.zhihuiya.com/)
- [Zhihuiya API base URL](https://connect.zhihuiya.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with generated HTML reports, downloadable report files, and Word disclosure documents when configured services are available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent session report files and depends on configured PatSnap/Zhihuiya services for live patent and workflow data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
