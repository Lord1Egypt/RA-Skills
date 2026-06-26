## Description: <br>
Helps BSA officers, AML investigators, and FIU staff draft confidential FinCEN SAR Part V narrative packets with 5 W's + H coverage, keyword tagging, quality checks, and BSA-officer review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
BSA officers, AML investigators, transaction-monitoring analysts, and FIU staff at U.S. financial institutions use this skill to turn case files into draft FinCEN SAR Part V narratives. It structures the draft around the required facts, highlights missing information, and keeps the final filing decision with a qualified BSA officer. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: Confidential SAR material or unnecessary customer identifiers could be exposed in a chat or draft. <br>
Mitigation: Use only for authorized BSA/AML work; avoid full SSNs, full account numbers, filing credentials, and unnecessary customer identifiers; keep narrative identifiers to last-4 or the institution's approved minimum. <br>
Risk: A draft narrative could be mistaken for a filing decision or a completed SAR submission. <br>
Mitigation: Keep every output labeled as a draft, require qualified BSA-officer review, and do not use the skill to submit SARs, contact outside parties, or decide whether the filing threshold is met. <br>
Risk: Outdated FinCEN keywords, deadlines, or incomplete case facts could produce a misleading draft. <br>
Mitigation: Verify current FinCEN advisory keywords and filing deadlines, resolve missing 5 W's + H facts before drafting, and review the final packet against institution policy before filing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/sar-narrative-drafter) <br>
- [README.md](artifact/README.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown draft narrative packet] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a draft label, FinCEN keyword list, Part V narrative, 5 W's + H coverage matrix, weak-language audit, FFIEC quality self-check, document-retention block, unresolved-information list, and BSA-officer review block.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
