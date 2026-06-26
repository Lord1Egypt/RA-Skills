## Description: <br>
Locates and imports character-specific chapters from Chen Yan's novel The Protagonist so an agent can answer questions, analyze characters, trace relationships, find source passages, or draft commentary from relevant background text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junwugit](https://clawhub.ai/user/junwugit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill when a request refers to characters, roles, or relationships in The Protagonist and needs relevant chapters loaded before analysis, Q&A, quotation lookup, or writing. It is designed to narrow retrieval by character, co-occurrence, and novel section instead of loading the full book. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read an alternate chapter directory when ZHUJUE_TXT is set. <br>
Mitigation: Leave ZHUJUE_TXT unset unless you intentionally want the scripts to read a different local chapter corpus. <br>
Risk: Retrieved literary passages may include offensive language or sensitive content from the source novel. <br>
Mitigation: Treat passages as contextual literary source material, preserve context, and quote only what is necessary. <br>
Risk: Broad character matches, especially the protagonist who appears throughout the novel, can pull too much text into the agent context. <br>
Mitigation: Narrow retrieval with co-occurring characters, section filters, or selected chapters before exporting text. <br>


## Reference(s): <br>
- [Character roster](references/characters.md) <br>
- [ClawHub skill page](https://clawhub.ai/junwugit/zhujue-characters) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, chapter lists, and optional plain-text chapter extracts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write selected cleaned chapter text to a local file for the agent to read; text export defaults limit broad matches and should be narrowed before increasing limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
