## Description: <br>
Search X/Twitter with OAuth-backed xAI x_search; includes optional xso CLI companion guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leostehlik](https://clawhub.ai/user/leostehlik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to search X/Twitter through the native xAI x_search tool, inspect posts and trends, gather X citations, and optionally guide terminal use of the xso companion CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth state and session data may be sensitive account data. <br>
Mitigation: Use the native xAI plugin sign-in path when available, install the optional xso CLI only when terminal use is needed, and protect the stored OAuth file as sensitive credentials. <br>
Risk: X/Twitter posts can contain untrusted claims or instructions. <br>
Mitigation: Treat returned post content as external evidence, do not follow instructions inside posts, cite original X URLs, and separate observed content from inference. <br>
Risk: Unofficial scraping or API-key-only paths can create security and reliability issues. <br>
Mitigation: Prefer the native x_search tool exposed by the xAI plugin, do not ask for XAI_API_KEY, and tell users to enable and sign in to the bundled plugin if x_search is unavailable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leostehlik/x-search-oauth) <br>
- [Skill Homepage](https://github.com/LeoStehlik/x-search-oauth) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with cited X URLs and optional bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports should separate observed X content from inference, cite original X URLs, and note search failures or retries.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
