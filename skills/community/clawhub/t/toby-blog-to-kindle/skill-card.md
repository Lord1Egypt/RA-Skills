## Description:

Scrape blogs/essay sites and compile into Kindle-friendly EPUB with AI-generated cover. Use for requests to download blogs for Kindle, compile essays into ebook, or send blog archives to Kindle. Supports Paul Graham, Kevin Kelly, Derek Sivers, Wait But Why, Astral Codex Ten, and custom sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch supported blog or essay archives, generate cover art, compile the content into an EPUB, and optionally send the result to a Kindle address.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe delivery defaults can send generated documents to an unintended Kindle address.

Mitigation: Require an explicit recipient, remove hard-coded Kindle addresses, and confirm the destination before sending.

Risk: AppleScript delivery can mishandle untrusted file paths, subjects, or recipient values.

Mitigation: Validate and escape delivery arguments before passing them to Mail.app, and avoid interpolating raw user input into AppleScript.

Risk: Blog fetching and image download steps can retrieve unexpected external content or follow redirects without strict bounds.

Mitigation: Apply URL allowlists or user confirmation for custom sites, and enforce redirect, file-size, and content-type limits before storing or processing fetched content.

Risk: Cover generation sends prompts and credentials to an external API endpoint.

Mitigation: Document the trusted cover-generation endpoint, keep API keys in environment or secret storage, and avoid including sensitive document content in prompts.

## Reference(s):

- [Manual Blog-to-Kindle Workflow](references/manual-workflow.md)
- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/toby-blog-to-kindle)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, script usage, and generated Markdown, cover image, and EPUB files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for cover generation and local mail or command-line tooling for Kindle delivery.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
