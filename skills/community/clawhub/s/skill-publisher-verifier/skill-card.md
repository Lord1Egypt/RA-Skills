## Description: <br>
Checks a ClawHub publisher's public trust signals before installation and returns a TRUSTED, ESTABLISHED, NEW, or FLAGGED verdict. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ordo-tech](https://clawhub.ai/user/ordo-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill before installing unfamiliar ClawHub skills to review public publisher reputation signals and receive an installation recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review verdict is suspicious because the artifacts include high-impact automation. <br>
Mitigation: Review the skill before installation and confirm that any proposed actions match the intended publisher-verification workflow. <br>
Risk: External review or fallback tooling may expose sensitive context if confidential inputs are provided. <br>
Mitigation: Use public publisher handles or skill URLs where possible, and avoid sending confidential diffs or private operational details unless disclosure is acceptable. <br>
Risk: Publisher reputation checks can be incomplete when public profile data or web search results are unavailable. <br>
Mitigation: Treat incomplete verification as a caution signal and manually review the publisher and skill before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ordo-tech/skill-publisher-verifier) <br>
- [Publisher profile](https://clawhub.ai/user/ordo-tech) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown trust report with a verdict, signal summary, and recommendation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public ClawHub profile data and web search results; returns NEW when verification is incomplete.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
