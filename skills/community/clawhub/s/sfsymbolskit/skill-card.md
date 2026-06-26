## Description: <br>
Helps agents generate, validate, and fix Apple SFSymbol names in Swift, SwiftUI, UIKit, and AppKit by grounding output against the bundled SFSymbolsKit 7.2 catalog of 7,007 symbols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wikipediabrown](https://clawhub.ai/user/wikipediabrown) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to choose real SFSymbol names and typed SFSymbolsKit accessors for Apple platform code, reducing blank-icon bugs caused by guessed systemName strings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent may suggest adding the SFSymbolsKit SwiftPM dependency to a project. <br>
Mitigation: Review the package URL and version before accepting dependency changes. <br>
Risk: Marketplace capability tags list crypto, wallet, and sensitive-credential requirements even though the security summary describes a static lookup helper. <br>
Mitigation: Do not grant wallet, credential, or crypto-related access based only on those tags; rely on the security evidence and local review. <br>
Risk: Symbol guidance can be incorrect if the manifest is skipped or if the target project uses a different SFSymbols version. <br>
Mitigation: Resolve names against symbols.json and check target platform compatibility before shipping UI changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wikipediabrown/sfsymbolskit) <br>
- [Publisher profile](https://clawhub.ai/user/wikipediabrown) <br>
- [SFSymbolsKit documentation](https://sfsymbolskit.com) <br>
- [SFSymbolsKit symbol manifest](https://sfsymbolskit.com/symbols.json) <br>
- [SFSymbolsKit Swift package](https://github.com/WikipediaBrown/SFSymbolsKit.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Swift code snippets and SwiftPM dependency instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Grounded against the bundled symbols.json manifest when followed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
