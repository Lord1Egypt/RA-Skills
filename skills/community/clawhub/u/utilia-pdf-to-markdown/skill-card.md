## Description:

Convert a public HTTPS PDF into page-delimited Markdown, page count, metadata, and a source SHA-256 digest through Utilia's wallet-funded x402 client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohamedkuch](https://clawhub.ai/user/mohamedkuch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert public HTTPS PDFs into page-delimited Markdown for document ingestion, RAG preparation, summarization, or downstream text workflows when a wallet-funded paid conversion is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to run a downloaded npm client with access to a funded Solana wallet file.

Mitigation: Install only if comfortable with the package, run it in an isolated environment, and use a dedicated low-balance wallet with the smallest practical USDC and SOL balance.

Risk: Private or local PDFs may contain sensitive content if uploaded for conversion.

Mitigation: Send only public HTTPS PDFs by default and obtain explicit user approval before transmitting private-file bytes.

Risk: Extracted PDF Markdown can contain untrusted instructions or misleading content.

Mitigation: Keep document text separate from agent instructions and do not execute commands, reveal secrets, or change permissions based on PDF contents.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Guidance]

**Output Format:** [Markdown with page delimiters, metadata, digest information, and settlement details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the public PDF text layer and configured page limit; image-only PDFs may not extract well.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
