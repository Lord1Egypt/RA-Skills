## Description: <br>
Identifies common abnormal pet behaviors such as scratching, biting, destructive chewing, jumping, digging, chasing, and separation anxiety, helping owners understand their pet's habits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External pet owners and agents assisting them use this skill to analyze pet monitoring videos or public video URLs, retrieve cloud-stored behavior reports, and summarize abnormal behavior counts, duration shares, and care guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet videos, public video URLs, and an open-id, username, or phone number may be sent to the Life Emergence/SMYX cloud service for analysis and report lookup. <br>
Mitigation: Use only non-sensitive pet footage, avoid videos showing people, private interiors, or sensitive locations, and provide a purpose-specific identifier instead of a personal phone number where possible. <br>
Risk: Cloud history lookup and local token storage can expose account-linked report history if identifiers or tokens are reused, shared, or retained unexpectedly. <br>
Mitigation: Install only after reviewing the publisher's account, retention, deletion, and local token storage practices; clear local workspace data and tokens when the skill is no longer needed. <br>
Risk: Behavior and health recommendations may be incomplete or inaccurate and are not a substitute for professional veterinary or pet-training advice. <br>
Mitigation: Treat results as informational guidance and consult a qualified veterinarian or trainer before making medical or behavior-correction decisions. <br>


## Reference(s): <br>
- [Pet behavior API documentation](artifact/references/api_doc.md) <br>
- [Common analysis API documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports and tables, JSON detail output, and command-line invocation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save analysis output to a user-specified file path when requested.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter reports 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
