## Description: <br>
Talebook is a third-party agent skill for managing a Talebook/MyBooks personal library, including searching books, viewing statistics, editing metadata, filling book information, uploading ebooks, sending books to email or reading devices, and updating reading states. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poxenstudio](https://clawhub.ai/user/poxenstudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate a trusted Talebook/MyBooks personal library through a Python command wrapper. It is intended for library search, metadata maintenance, ebook upload, book delivery, and reading-list workflows after the user supplies server credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Talebook/MyBooks credentials and signs in to the configured server before tool calls. <br>
Mitigation: Provide credentials only through session-scoped environment variables or a dedicated secret manager, and avoid shared or global configuration files. <br>
Risk: The skill can upload local ebook files and send books to arbitrary email addresses or device endpoints. <br>
Mitigation: Manually confirm file paths, book IDs, destination email addresses, and device addresses before allowing upload or send actions. <br>
Risk: A malicious or untrusted Talebook/MyBooks server could receive credentials and file uploads. <br>
Mitigation: Use the skill only with a trusted local or HTTPS Talebook/MyBooks server. <br>


## Reference(s): <br>
- [ClawHub Talebook Skill Page](https://clawhub.ai/poxenstudio/talebook) <br>
- [MyBooks Homepage](https://www.mybooks.top) <br>
- [Publisher Profile](https://clawhub.ai/user/poxenstudio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus TALEBOOK_HOST, TALEBOOK_USER, and TALEBOOK_PASSWORD environment variables.] <br>

## Skill Version(s): <br>
1.0.7 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
