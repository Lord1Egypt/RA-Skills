## Description: <br>
PullThatUpJamie gives agents access to the Jamie podcast intelligence API for semantic podcast search, timestamped research sessions, people and organization discovery, on-demand RSS ingestion, and shareable clip generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unclejim21](https://clawhub.ai/user/unclejim21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to search a hosted podcast corpus, retrieve timestamped clips, build research sessions, generate shareable audio or video clips, and ingest new podcasts through the Jamie API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid Jamie endpoints can use optional NWC or L402 credentials that spend Lightning credits. <br>
Mitigation: Use the free tier first, provide payment credentials only when spending is intended, and keep wallet balances limited. <br>
Risk: Smart Search sends query text to the external Jamie service for triage. <br>
Mitigation: Avoid sensitive or confidential queries when using Smart Search. <br>
Risk: Clip generation and podcast ingestion can create public or shareable outputs or submit new content for processing. <br>
Mitigation: Confirm operator intent before creating public clips, sharing session links, or ingesting new podcasts. <br>


## Reference(s): <br>
- [PullThatUpJamie ClawHub Skill Page](https://clawhub.ai/unclejim21/pullthatupjamie) <br>
- [PullThatUpJamie Homepage](https://pullthatupjamie.ai) <br>
- [Jamie API Service](https://www.pullthatupjamie.ai) <br>
- [RRA - Retrieve, Research, Analyze](references/podcast-rra.md) <br>
- [Create Module - Audio Clip Generation](references/create.md) <br>
- [L402 Protocol Documentation](https://docs.lightning.engineering/the-lightning-network/l402) <br>
- [lnget L402 Client](https://github.com/lightninglabs/lnget) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with API request examples, JSON response handling, and Jamie session or clip URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include HTTP requests to the external Jamie API; free-tier use does not require credentials, while paid requests use optional L402 credentials.] <br>

## Skill Version(s): <br>
1.6.0 (source: frontmatter, CHANGELOG, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
