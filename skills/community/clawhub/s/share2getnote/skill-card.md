## Description: <br>
Parse ChatGPT or Gemini shared conversation links and save Q&A pairs as notes to GetNote (biji.com). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silentforce](https://clawhub.ai/user/silentforce) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to import public ChatGPT or Gemini shared conversations into GetNote as individual markdown notes after reviewing extracted titles and content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install Playwright browser automation dependencies locally when parsing a shared conversation link. <br>
Mitigation: Install only in environments where local browser automation dependencies are acceptable, and review setup prompts or dependency changes before running the parser. <br>
Risk: Shared conversation content may include private or sensitive information that would be saved into the user's GetNote account. <br>
Mitigation: Review extracted note titles and markdown content before confirming the save step, especially for private conversations. <br>
Risk: Parsing depends on ChatGPT and Gemini share-page structure, which can change and cause incomplete or failed extraction. <br>
Mitigation: Check the extracted note count and content before saving, and fall back to manual extraction if the parser reports missing conversation data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/silentforce/share2getnote) <br>
- [GetNote Skill](https://clawhub.ai/iswalle/getnote) <br>
- [uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON note objects containing title and markdown content fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided ChatGPT or Gemini share URL and user confirmation before saving notes to GetNote.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; SKILL.md frontmatter still lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
