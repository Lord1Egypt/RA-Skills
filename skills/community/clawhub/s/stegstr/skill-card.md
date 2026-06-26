## Description: <br>
Decode and embed Stegstr payloads in PNG images for steganographic Nostr workflows, including extracting hidden data, encoding payloads into cover images, and using the Stegstr CLI from scripts or agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brunkstr](https://clawhub.ai/user/brunkstr) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, automation authors, and external users use this skill to decode Stegstr data from PNG images, embed text, JSON, binary, or Nostr bundle payloads into PNG cover images, and run headless Stegstr CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation builds an unpinned Rust project from GitHub and its dependencies. <br>
Mitigation: Install only from a trusted Stegstr release or a reviewed commit, and review dependency changes before using it in sensitive environments. <br>
Risk: Nostr private keys can be exposed through prompts, shell history, shared logs, or process-visible command lines. <br>
Mitigation: Avoid placing real private keys in prompts or command arguments; prefer safer secret-handling workflows and scrub logs before sharing. <br>
Risk: Decoded payloads may contain sensitive or untrusted content. <br>
Mitigation: Review decoded text, JSON, or base64 payloads before sharing, executing, importing, or using them in another workflow. <br>
Risk: Stegstr payloads are documented for PNG images only, and lossy formats can corrupt hidden data. <br>
Mitigation: Use lossless PNG inputs and outputs for embedding, decoding, and sharing Stegstr images. <br>


## Reference(s): <br>
- [Stegstr homepage](https://stegstr.com) <br>
- [For agents](https://www.stegstr.com/wiki/for-agents.html) <br>
- [Stegstr repository](https://github.com/brunkstr/Stegstr) <br>
- [CLI documentation](https://www.stegstr.com/wiki/cli.html) <br>
- [Bundle schema](https://raw.githubusercontent.com/brunkstr/Stegstr/main/schema/bundle.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI command examples and JSON payload notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide commands that read and write local PNG, JSON, text, or binary payload files; decoded payloads may print as text, JSON, or base64.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
