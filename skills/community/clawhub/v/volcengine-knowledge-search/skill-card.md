## Description: <br>
Searches and fetches public Volcengine official documentation, returning cleaned markdown that agents can use to answer product, pricing, deployment, troubleshooting, and terms questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and support agents use this skill to locate and summarize authoritative Volcengine documentation or fetch the full text of a specific Volcengine documentation page. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and documentation URLs are sent to Volcengine's public documentation service. <br>
Mitigation: Avoid sending confidential, customer-sensitive, or internal-only details in search queries or document URLs. <br>
Risk: Long documentation results can be saved temporarily on disk for the agent to read. <br>
Mitigation: Review temporary output handling in the execution environment and remove saved result files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/volc-sdk-team/skills/volcengine-knowledge-search) <br>
- [Volcengine documentation](https://www.volcengine.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with source links and optional shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are summarized; fetched documents are paginated and long results may be written to temporary files for follow-up reading.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
