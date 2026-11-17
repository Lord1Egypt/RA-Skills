## Description:

Reverse engineers Android APKs and other software without source code using REA (rea-agents) in a locked-down Docker container: APK package overview, class search, decompiled Java/Kotlin classes and methods via JADX, reference tracing, decoded resources and strings via Apktool, adb device inspection, plus JavaScript/Electron, .NET, Go, Rust, WASM, SQLite and network-capture analysis, and native decompilation with Ghidra when enabled. Runs as a Streamable HTTP MCP server or as one-off CLI commands. Use when the user wants to understand how an app or feature works from its APK or binary, inspect what an APK contains, or find where behavior lives in decompiled code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to inspect APKs and other binaries they are authorized to analyze, locate code and resources related to a behavior, and summarize what static analysis can establish. It can also guide connected-device inspection and opt-in native decompilation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked the skill suspicious because it uses mutable Docker image references; the scan evidence is partial, with five path-like references unresolved.

Mitigation: Review whether the image source is trusted and verify and pin the image to a reviewed SHA-256 digest. Treat the scan as incomplete because some references could not be assessed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/psyb0t/skills/reverse-engineer-anything)
- [Setup and MCP server configuration](references/setup.md)
- [docker-reverse-engineer-anything repository](https://github.com/psyb0t/docker-reverse-engineer-anything)
- [REA (rea-agents) repository](https://github.com/morluto/rea)

## Skill Output:

**Output Type(s):** [Analysis, Code, JSON, Guidance]

**Output Format:** [JSON analysis results and Markdown explanations, including decompiled code excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static analysis does not prove runtime behavior; obfuscated names may remain unresolved.]

## Skill Version(s):

0.1.2 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
