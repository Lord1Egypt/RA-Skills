## Description:

小红书内容发布技能 - 规范化cookie管理 + xhs-kit自动化发布

This skill is ready for commercial/non-commercial use.

## Publisher:

[glittering](https://clawhub.ai/user/glittering)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Xiaohongshu account cookies and run repeatable content publishing workflows through xhs-kit. It supports cookie normalization, active-account switching, status checks, debug validation, live posting, and scheduled posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Xiaohongshu cookies may be exposed through command history, local files, or accidental commits.

Mitigation: Use a dedicated or test account, keep cookies in an isolated workspace, avoid pasting real cookies directly into shell commands, set strict file permissions, and ensure cookie files and backups are ignored by version control.

Risk: Publishing and scheduled publishing can make unintended live posts.

Mitigation: Run debug validation first, review all title, content, image, tag, and schedule inputs, and require explicit confirmation before live or scheduled posting.

Risk: Unsafe command construction or unpinned dependencies can increase local execution risk.

Mitigation: Use safe argument passing, pin dependencies, review scripts before execution, and run the tool only in an isolated workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/glittering/skills/xhs-skill-pusher)
- [README.md](artifact/README.md)
- [PUSH_GUIDE.md](artifact/PUSH_GUIDE.md)
- [QUICK_START.md](artifact/docs/QUICK_START.md)
- [XHS_FINAL_SOLUTION.md](artifact/docs/XHS_FINAL_SOLUTION.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation or selection of local cookie JSON files and posting command inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
