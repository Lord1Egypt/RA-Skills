## Description:

Stock Invest Master guides agents through stock analysis for A-share, Hong Kong, and U.S. equities using a Dao-method and investing-master framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mickshu](https://clawhub.ai/user/mickshu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to prepare educational stock research, valuation checks, financial-statement reviews, risk assessments, and portfolio review notes. Outputs should be treated as informational research support, not personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start an unauthenticated report server that may expose saved investment reports beyond the local machine.

Mitigation: Review before installing; keep the report server disabled unless needed, bind it to 127.0.0.1, and avoid sensitive files or symlinks in ~/.stock-invest-master.

Risk: Stock research output could be mistaken for personalized financial advice.

Mitigation: Treat outputs as informational research support and require user review before making investment decisions.

## Reference(s):

- [Stock Invest Master ClawHub listing](https://clawhub.ai/mickshu/skills/stock-invest-master)
- [A-share browser data retrieval](references/a-stock-data-browser-fetch.md)
- [A-share data retrieval guide](references/a-stock-data-retrieval.md)
- [Buffett investing framework](references/buffett-framework.md)
- [Dalio investing framework](references/dalio-framework.md)
- [Dao analysis method](references/dao-analysis-method.md)
- [Data source notes](references/data-source-notes.md)
- [Duan Yongping investing framework](references/duan-framework.md)
- [Fisher investing framework](references/fisher-framework.md)
- [Graham investing framework](references/graham-framework.md)
- [Lynch investing framework](references/lynch-framework.md)
- [Marks investing framework](references/marks-framework.md)
- [Munger investing framework](references/munger-framework.md)
- [News judgment framework](references/news-judgment-framework.md)
- [Simons quantitative framework](references/simons-framework.md)
- [Soros investing framework](references/soros-framework.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with optional HTML overview cards and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are saved under ~/.stock-invest-master when the workflow archives output.]

## Skill Version(s):

3.9.2 (source: server release metadata; artifact frontmatter says 3.9.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
