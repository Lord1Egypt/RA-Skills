## Description: <br>
Helps agents operate browser workflows with real UI interactions, reliable text entry, page-state verification, and refresh-based recovery when pages become stuck or stale. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuxinyang111](https://clawhub.ai/user/shuxinyang111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill during browser-based workflows that require reliable form entry, visible-control interaction, front-end state checks, and recovery from blank, stale, or desynchronized pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive text could be pasted into an untrusted website during browser workflows. <br>
Mitigation: Avoid using the skill to paste secrets into untrusted websites and review the target page before text entry. <br>
Risk: Refresh-based recovery can clear fields or discard page state when a page appears stuck or out of sync. <br>
Mitigation: Confirm that refresh or retry is acceptable before recovery steps, then re-check the page's own indicators after re-entry. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shuxinyang111/smooth-browser-use) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Markdown guidance with inline browser-operation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only browser helper; no executable code or credential references were detected in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
