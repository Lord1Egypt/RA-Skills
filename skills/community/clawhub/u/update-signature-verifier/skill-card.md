## Description: <br>
Helps verify the cryptographic integrity of skill updates by checking whether each version is signed by the same key as the original install, detecting key changes, signature gaps, and unsigned updates that may indicate a compromised or transferred skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit whether skill updates preserve signing-key continuity, identify unsigned versions, and summarize chain-of-custody gaps before trusting an updated skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Version history or signing metadata may be unavailable or incomplete, which can limit confidence in chain-of-custody conclusions. <br>
Mitigation: Treat missing metadata as an explicit uncertainty and avoid claiming signature continuity without per-version signing records. <br>
Risk: The skill may lead an agent to retrieve or parse public update-signature metadata and produce recommendations about pinning versions or challenging a publisher. <br>
Mitigation: Review the target skill, source metadata, and resulting recommendations before acting on version-pinning or publisher-trust decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/andyxinweiminicloud/update-signature-verifier) <br>
- [Publisher Profile](https://clawhub.ai/user/andyxinweiminicloud) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown signature continuity report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include version-by-version signing key comparisons, unsigned version detection, chain-of-custody status, and recommended actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
