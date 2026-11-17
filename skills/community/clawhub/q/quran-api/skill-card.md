## Description:

Search and retrieve Quranic verses, surahs, pages, or juz with full Arabic text and detailed metadata using the alquran.cloud API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m7madash](https://clawhub.ai/user/m7madash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Quranic verses, full surahs, pages, or juz data from alquran.cloud and present Arabic text with related metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup requests are sent to the public alquran.cloud API.

Mitigation: Use the skill only when sharing the requested surah, ayah, page, or juz lookup with that service is acceptable.

Risk: The advertised search command is not implemented.

Mitigation: Use the implemented surah, ayah, page, and juz retrieval commands, or update the script before relying on keyword search.

## Reference(s):

- [Quran Api ClawHub Release](https://clawhub.ai/m7madash/skills/quran-api)
- [alquran.cloud API](https://api.alquran.cloud/v1/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text and Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns Arabic Quran text with surah, ayah, page, juz, revelation, and related metadata when the public API request succeeds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
