## Description:

Searches official Renesas product pages and datasheets to recommend semiconductor parts and report verified parameters for embedded system design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangp-gh](https://clawhub.ai/user/wangp-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and hardware engineers use this skill to find Renesas semiconductor candidates, download official datasheets, and compare verified table-sourced parameters for embedded product design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes web requests to Renesas-related pages and downloads datasheet PDFs into the workspace.

Mitigation: Confirm downloaded URLs are official renesas.com links and verify saved PDFs before relying on extracted specifications.

Risk: Part pages, datasheet links, and example output paths may become stale.

Mitigation: Confirm each product page is reachable before use and save datasheets under embedded_dev/renesas/datasheet as the current skill behavior specifies.

Risk: Incorrect semiconductor recommendations can result if numerical parameters are inferred from summaries or stale references.

Mitigation: Use only official datasheet tables for numerical values, cite page and table numbers, and mark missing values as not verified.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/wangp-gh/skills/renesas-search)
- [Server-Resolved GitHub Provenance](https://github.com/wangp-gh/renesas-search)
- [Renesas Products](https://www.renesas.com/en/products)
- [Renesas Product Families Reference](references/product_families.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Markdown recommendations with tables, source citations, local datasheet paths, and inline shell commands when downloads are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save official Renesas datasheet PDFs under embedded_dev/renesas/datasheet in the current workspace.]

## Skill Version(s):

3.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
