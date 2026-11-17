## Description:

Use when generating, validating, or fixing Apple SFSymbol names in Swift, SwiftUI, UIKit, or AppKit. Grounds symbol usage against the real catalog (SFSymbolsKit, SFSymbols 7.2, 7,007 symbols) so you emit typed, compile-checked accessors instead of hallucinated stringly-typed `systemName:` values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wikipediabrown](https://clawhub.ai/user/wikipediabrown)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to resolve, validate, and emit real Apple SF Symbol identifiers as typed SFSymbolsKit accessors for SwiftUI, UIKit, and AppKit code. It helps agents avoid guessed string-based symbol names that compile but render blank icons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may add a third-party SFSymbolsKit Swift package dependency to a project.

Mitigation: Before allowing project changes, confirm the dependency is wanted, review the repository, and pin a reviewed exact version or commit for production or CI use.

Risk: Incorrect SF Symbol names can compile while rendering blank icons.

Mitigation: Validate symbol names against the bundled SFSymbols 7.2 catalog or an available SFSymbolsKit MCP server before emitting accessors.

## Reference(s):

- [SFSymbolsKit documentation](https://sfsymbolskit.com)
- [SFSymbolsKit symbol catalog](https://sfsymbolskit.com/symbols.json)
- [SFSymbolsKit package repository](https://github.com/WikipediaBrown/SFSymbolsKit)
- [ClawHub skill page](https://clawhub.ai/wikipediabrown/skills/sfsymbolskit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with Swift code and package configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be grounded against the bundled symbols.json manifest or an available SFSymbolsKit MCP server.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
