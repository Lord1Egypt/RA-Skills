## Description:

Turns an advisor's written product answers and public Xiaohongshu note questions into separate short spoken wealth FAQ clips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Wealth advisors use this skill to turn supplied product answers and public Xiaohongshu FAQ questions into individually reviewable talking clips for their own posting. It does not post the clips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package uses a broad shared Beatra device authorization with credit-spending capabilities.

Mitigation: Review account permissions and credit balance; approve each paid stage and its live price before submission.

Risk: The bundled client silently installs verified updates by default, changing code without separate approval.

Mitigation: Disable automatic updates with `python3 scripts/mcp_client.py update --auto off` if you need to review releases first.

Risk: Generated wealth-product claims or cloned likenesses could be misleading or unauthorized.

Mitigation: Use only advisor-supplied product facts, confirm face and voice rights, and review each clip before posting.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/beatra-ai/skills/xiaohongshu-wealth-faq-talking)
- [Wealth FAQ talking workflow](artifact/references/workflow.md)
- [Xiaohongshu wealth FAQ note lookup](artifact/references/note-lookup.md)
- [Automatic updates and safety](artifact/references/automatic-updates-and-safety.md)

## Skill Output:

**Output Type(s):** [Text, Video clips]

**Output Format:** [Markdown slot plan and separate short video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically three clips, each 2–15 seconds; no automatic posting.]

## Skill Version(s):

0.1.9 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
