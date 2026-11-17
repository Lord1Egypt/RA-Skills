## Description:

X2strategy helps agents transform quantitative finance research inputs into structured strategy specifications, executable Backtrader code, backtests, and diagnosis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patrick-lew](https://clawhub.ai/user/patrick-lew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative researchers use X2strategy to turn finance papers, drafts, reports, notes, or search results into structured trading strategy specs and executable Backtrader implementations. It supports parsing, LLM extraction, validation, backtesting, and diagnosis against paper metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make external LLM calls and market-data network requests.

Mitigation: Use restricted API keys with spending limits and install only in environments where those network calls are acceptable.

Risk: The skill stores API keys in project files during setup.

Mitigation: Use a throwaway workspace when possible and avoid storing long-lived secrets in the project .env.

Risk: The skill can run generated trading strategy code directly.

Mitigation: Review generated code before execution and avoid running real tests or untrusted backtests outside a restricted environment.

Risk: Security evidence flags probing of an unrelated secret path in tests.

Mitigation: Review the test suite before running tests and do not execute real or network-enabled tests during routine installation.

## Reference(s):

- [X2strategy ClawHub skill page](https://clawhub.ai/patrick-lew/skills/x2strategy)
- [Architecture](docs/ARCHITECTURE.md)
- [Paper2Spec](references/paper2spec.md)
- [Spec2Code](references/spec2code.md)
- [Skill Internals](references/skill-internals.md)
- [Data Sources](references/data_sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated Python code, JSON strategy specifications, shell commands, and diagnostic reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on external LLM and market-data services, and may propose or run generated trading code after user review.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence; artifact metadata reports 0.6.0 and pyproject.toml reports 0.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
