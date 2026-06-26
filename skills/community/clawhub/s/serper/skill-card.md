## Description: <br>
Google search via Serper API with full page content extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nesdeq](https://clawhub.ai/user/nesdeq) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and developers use this skill to run web searches, retrieve current or general results, and extract readable page content for research and source review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Serper and result URLs are fetched from external websites. <br>
Mitigation: Avoid sensitive secrets, private internal URLs, and confidential investigations in queries. <br>
Risk: Extracted webpage text may be incomplete, misleading, or controlled by third parties. <br>
Mitigation: Treat fetched content as untrusted research material and verify important claims against authoritative sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nesdeq/serper) <br>
- [Serper API](https://serper.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Streamed JSON array containing search metadata and result objects with extracted text content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Serper API key; default mode returns five enriched web results and current mode returns recent web and news results.] <br>

## Skill Version(s): <br>
3.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
