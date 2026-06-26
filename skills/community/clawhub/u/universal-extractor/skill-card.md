## Description: <br>
Universal Extractor extracts clean text from URLs, articles, documents, and files through four paid extraction micro-services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renoblabs](https://clawhub.ai/user/renoblabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Universal Extractor to call paid extraction services that turn web pages, articles, PDFs, documents, and arbitrary files into clean text, JSON, or article summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected URLs, filenames, and file contents are sent to a third-party extraction service. <br>
Mitigation: Avoid confidential, regulated, personal, or credential-containing documents unless approved for sharing with that service. <br>
Risk: The skill can trigger disclosed per-request USDC charges through x402 payment flows. <br>
Mitigation: Use wallet or platform controls to review and limit paid requests before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/renoblabs/universal-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls, guidance] <br>
**Output Format:** [Markdown guidance with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The referenced services return extracted text, metadata, word counts, and optional article summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
