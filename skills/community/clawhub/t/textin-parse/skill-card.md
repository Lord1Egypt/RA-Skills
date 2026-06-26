## Description: <br>
Textin Parse helps agents send supported images and documents to Textin's document parsing API for layout detection, OCR, table and formula recognition, and Markdown or structured output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KingJus](https://clawhub.ai/user/KingJus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing users use this skill to configure Textin credentials and parse PDFs, images, Office documents, HTML, and text into Markdown or structured data through Textin's API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents or URLs are sent to Textin for third-party processing. <br>
Mitigation: Use only documents approved for Textin processing and confirm privacy, retention, and data-handling requirements before parsing. <br>
Risk: Textin credentials are requested from the user and stored in plaintext at ~/.openclaw/textin-config.json. <br>
Mitigation: Use a dedicated low-privilege Textin key, avoid pasting production secrets into chat, and restrict or remove the local config file after use. <br>
Risk: Credential display commands can expose secrets in shared terminals, logs, or screenshots. <br>
Mitigation: Do not run config display commands in shared sessions or captured environments, and rotate credentials if they are exposed. <br>


## Reference(s): <br>
- [ClawHub release page for Textin Parse](https://clawhub.ai/KingJus/textin-parse) <br>
- [Textin registration page](https://www.textin.com/register/code/3EJS7P) <br>
- [Textin PDF-to-Markdown API endpoint](https://api.textin.com/ai/service/v1/pdf_to_markdown) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown text, JSON results, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save full API results to a JSON file and can display a truncated Markdown preview in shell output.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, skill.yaml, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
