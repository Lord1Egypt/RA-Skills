## Description: <br>
Searches Web of Science through institutional access, filters academic literature by quality criteria, and imports selected papers into Zotero. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanfanliu964-web](https://clawhub.ai/user/fanfanliu964-web) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, librarians, and academic users use this skill to collect Web of Science results matching topic, journal, citation, impact-factor, and date criteria, then create a Zotero collection with enriched metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Zotero API key that can write to the user's library. <br>
Mitigation: Use a dedicated Zotero key with the minimum permissions needed, avoid notes access unless required, and prefer safer secret-passing if modifying the script. <br>
Risk: The workflow relies on an authenticated institutional Web of Science browser session. <br>
Mitigation: Proceed only in the user's local browser session and review browser actions before importing results. <br>
Risk: Incorrect extraction or collection selection could write unwanted records to Zotero. <br>
Mitigation: Run with --dry-run first, then review the target collection name and extracted paper list before import. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fanfanliu964-web/wos-zotero-hunter) <br>
- [Zotero API key settings](https://www.zotero.org/settings/keys) <br>
- [Crossref Works API](https://api.crossref.org/works) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON paper lists and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run summaries and Zotero import status for selected papers.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
