## Description:

Search and explore Jewish texts (Torah, Tanach, Talmud, Midrash, commentaries) via Sefaria API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeperl](https://clawhub.ai/user/abeperl)

### License/Terms of Use:

MIT

## Use Case:

External users, Torah learners, educators, researchers, and developers use this skill to search Jewish texts, retrieve Hebrew and English passages, find commentaries and cross-references, check learning schedules, and prepare source-backed dvar Torah outlines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Torah searches, references, and themes to Sefaria's public API.

Mitigation: Avoid submitting sensitive or private study topics unless public API disclosure is acceptable.

Risk: Generated dvar Torah outlines and source suggestions may contain textual or religious inaccuracies.

Mitigation: Review cited sources and religious interpretation before teaching, publishing, or relying on the output.

Risk: Sefaria API availability, rate limits, and text coverage can affect results.

Mitigation: Handle API errors and missing translations, and verify important references against primary sources.

## Reference(s):

- [Torah Scholar on ClawHub](https://clawhub.ai/abeperl/skills/torah-scholar)
- [Sefaria](https://www.sefaria.org)
- [Sefaria API Docs](https://developers.sefaria.org)
- [Common Torah References](references/common-refs.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown, plain text, and JSON-formatted API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Hebrew and English source text, commentary summaries, search results, learning calendar data, and structured dvar Torah outlines.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
