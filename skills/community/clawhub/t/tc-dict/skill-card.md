## Description:

Query Traditional Chinese dictionary entries from Taiwan Ministry of Education data, with support for word lookup, dictionary downloads, and update checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kai-tw](https://clawhub.ai/user/kai-tw)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to look up Traditional Chinese word definitions, pronunciations, examples, and related dictionary details from public MOE data. They can also download dictionary data and check for updates when local data needs to be refreshed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual or scheduled updates download ZIP archives from MOE and write extracted dictionary data to a local user directory.

Mitigation: Use a deliberate update schedule, monitor automated runs, and keep the storage path under user control.

Risk: Python dependencies are specified as minimum versions rather than pinned exact versions.

Mitigation: Install from a locked environment or pin dependency versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kai-tw/skills/tc-dict)
- [Dictionary data sources](references/DICTIONARY_SOURCES.md)
- [Dictionary data schema](references/SCHEMA.md)
- [MOE dictionary download page](https://language.moe.gov.tw/001/Upload/Files/site_content/M0001/respub/dict_concised_download.html)
- [MOE dictionary site](https://language.moe.gov.tw/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lookup results may include the matched word, pronunciation, definition, examples, and alternative fuzzy or prefix matches.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
