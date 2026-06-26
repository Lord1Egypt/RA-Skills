## Description: <br>
Shuzhi Open wraps the Shuzhi open platform APIs for blockchain anchoring, automated evidence collection, custody certificate generation, and electronic signing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex098929](https://clawhub.ai/user/alex098929) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and authorized operators use this skill to configure Shuzhi platform credentials and run API workflows for blockchain data anchoring, e-commerce or public-account evidence capture, custody certificate PDFs, and electronic contract signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive identity, phone, contract, and signer data. <br>
Mitigation: Use it only in a trusted workspace with authorized users, prefer interactive collection paths, and avoid placing ID numbers or phone numbers directly in command-line arguments. <br>
Risk: Generated evidence, certificate, preview, signing, and download links may expose legally significant or private files. <br>
Mitigation: Treat generated links as sensitive, share them only with intended recipients, and avoid logging or pasting them into untrusted systems. <br>
Risk: Blockchain anchoring, certificate generation, and signing workflows can upload or preserve data externally. <br>
Mitigation: Confirm the exact data, files, templates, signer identities, and product identifiers before executing upload, certificate, or signing workflows. <br>


## Reference(s): <br>
- [Blockchain API service documentation](references/chain-api.md) <br>
- [Automated evidence API documentation](references/evidence-api.md) <br>
- [Custody certificate API documentation](references/certificate-api.md) <br>
- [Electronic signature API documentation](references/sign-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to run Node.js scripts that call external Shuzhi APIs after user confirmation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
