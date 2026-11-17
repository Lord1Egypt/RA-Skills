## Description:

Finds similar Chinese utility models, including drawings and legal status, and suggests whether to file a utility model or an invention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as engineers working on structural improvements and individual inventors use the skill to find similar patents, review representative drawings and legal status, and get an initial filing-type suggestion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be forwarded or stored insecurely.

Mitigation: Do not paste keys into chat; review credential handling and secure saved keys before using a production key.

Risk: Searches send technical terms to PatentMax and may incur charges.

Mitigation: Approve disclosure of confidential invention details before searching, and set a spending limit.

Risk: Cache filename handling warrants review before production use.

Mitigation: Validate cache filenames and review generated file paths before using a production key.

## Reference(s):

- [PatentMax API reference](artifact/references/api-reference.md)
- [Search workflow](artifact/references/search-workflow.md)
- [Query construction](artifact/references/query-construction.md)
- [Query syntax](artifact/references/query-syntax.md)
- [Usage FAQ](artifact/references/faq.md)
- [Known pitfalls](artifact/references/pitfalls.md)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance, CSV files, Patent drawing image files]

**Output Format:** [Markdown summary and UTF-8 CSV, with patent drawings saved as image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CSV ranks candidate patents by similarity and includes bibliographic details, legal status, structural notes, and drawing filenames.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
