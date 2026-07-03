## Description: <br>
RealBrowser by Ceki lets an AI agent drive a real Chrome session, either self-hosted or rented from an opted-in marketplace participant, for authorized QA, accessibility, monitoring, support, and data-collection workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iwedmak](https://clawhub.ai/user/iwedmak) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, QA engineers, accessibility reviewers, and support teams use this skill to run authorized browser workflows on sites they own or are permitted to operate on when a real Chrome session is required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rent and drive live browser sessions, including click and type actions that may affect real accounts or incur charges. <br>
Mitigation: Review before installing, require confirmation before renting, clicking, or typing, and keep marketplace sessions stopped when work is complete. <br>
Risk: One example configuration pre-approves high-impact actions through alwaysAllow. <br>
Mitigation: Remove or narrow alwaysAllow entries so the agent asks before renting, clicking, typing, scrolling, or stopping sessions. <br>
Risk: Marketplace sessions are visible to the opted-in host, so confidential pages, credentials, payment data, or private content could be exposed. <br>
Mitigation: Use Self mode for sensitive workflows and avoid entering secrets or private user data into marketplace sessions. <br>
Risk: Profile export and import can create sensitive local files containing cookies or session state. <br>
Mitigation: Treat exported profiles as sensitive session files, store them only where needed, and delete or protect them after use. <br>
Risk: Real-browser automation can violate site terms, consent expectations, access controls, or local law if used on unauthorized sites. <br>
Mitigation: Use only on sites where the user has explicit authorization, respect Terms of Service and robots.txt, and do not use it for CAPTCHA or third-party-site automation unless explicitly authorized. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iwedmak/realbrowser) <br>
- [Ceki dashboard and API key management](https://ceki.me) <br>
- [Ceki Chrome extension for Self mode](https://browser.ceki.me/install) <br>
- [ceki-sdk on PyPI](https://pypi.org/project/ceki-sdk/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, and Python or TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces browser-operation guidance and command examples; live actions depend on the ceki CLI and user-provided API key.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata, manifest.json, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
