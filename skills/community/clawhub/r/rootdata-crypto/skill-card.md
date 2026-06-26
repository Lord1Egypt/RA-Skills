## Description: <br>
Query crypto project details, Web3 investor info, funding rounds, trending projects, and personnel job changes from RootData. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rdquanyu](https://clawhub.ai/user/rdquanyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up RootData crypto intelligence for blockchain projects, Web3 investors, recent funding rounds, trending projects, and personnel movements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent creates and stores a RootData API key locally. <br>
Mitigation: Treat ROOTDATA_SKILL_KEY as a credential in logs and screenshots, and revoke it through RootData support if it is exposed. <br>
Risk: Crypto research queries are sent to RootData. <br>
Mitigation: Use the skill only when sharing those queries with RootData is acceptable for the user or organization. <br>
Risk: Funding and personnel results are constrained by RootData endpoint limits. <br>
Mitigation: State the 365-day funding window, 3-investor funding-round limit, and 20-entry personnel limit when answering questions that could be interpreted as exhaustive. <br>
Risk: Artifact metadata reports version 1.0.2 while the release evidence and skill files report version 1.0.3. <br>
Mitigation: Confirm the installed release is v1.0.3 when version-specific behavior matters. <br>


## Reference(s): <br>
- [RootData Crypto on ClawHub](https://clawhub.ai/rdquanyu/rootdata-crypto) <br>
- [RootData Web3 Data Platform](https://www.rootdata.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [Markdown or plain text summaries backed by RootData API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ROOTDATA_SKILL_KEY; funding data covers the past 365 days with up to 3 investors per round, personnel results return up to 20 entries per category, and rate limit is 200 requests per minute per key.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter, README.md, and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
