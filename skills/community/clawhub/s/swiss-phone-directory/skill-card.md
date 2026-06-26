## Description: <br>
Swiss phone directory lookup via the search.ch API for businesses, people, and reverse phone-number searches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xenofex7](https://clawhub.ai/user/xenofex7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up Swiss business and personal directory entries, addresses, contact details, categories, and reverse phone-number matches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends lookup queries such as names, phone numbers, and locations to search.ch. <br>
Mitigation: Search only for information you are comfortable sending to search.ch and follow the service terms that apply to your use. <br>
Risk: The skill requires a search.ch API key. <br>
Mitigation: Use a dedicated key, keep it out of committed files and shared configuration, and prefer a temporary environment variable or secret manager. <br>
Risk: The documented command path may differ from the packaged artifact path. <br>
Mitigation: Use the installed artifact path, such as searchch.py, when scripts/searchch.py is not present. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xenofex7/swiss-phone-directory) <br>
- [search.ch Telephone API help](https://search.ch/tel/api/help.en.html) <br>
- [search.ch API key request](https://search.ch/tel/api/getkey.en.html) <br>
- [Artifact configuration guide](artifact/configuration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-formatted CLI output or JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SEARCHCH_API_KEY; search parameters include query, location, entry type, result limit, language, verbosity, clickable phone links, and JSON output.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
