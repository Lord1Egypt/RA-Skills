## Description: <br>
Creates and manages stock and crypto portfolios with real-time price and profit/loss tracking through AISA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users can ask an agent to create, update, list, rename, delete, and review stock or crypto portfolios from the command line. The skill is intended for portfolio tracking workflows that need live price lookup and local profit/loss summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify or delete locally stored financial portfolio records. <br>
Mitigation: Back up the portfolio file before use and only allow delete, remove, rename, or update commands when the user explicitly requested that exact change. <br>
Risk: Ticker symbols are sent to a third-party pricing provider and the skill requires an AISA API key. <br>
Mitigation: Use the skill only with ticker symbols the user intends to share, keep AISA_API_KEY scoped to trusted sessions, and rotate the key if exposure is suspected. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with inline shell commands and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and stores portfolio state in a local JSON file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
