## Description:

Verify Rust with Verus, check proof repairs, and run cached Z3 queries with Sail. Use when cargo verus verify is slow, when developing Verus proofs, or when giving coding agents SMT-LIB solver access through the CLI or MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffreykentjr](https://clawhub.ai/user/jeffreykentjr)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use Sail to verify Rust code and Verus proofs, review candidate proof repairs, and submit SMT-LIB queries to Z3 through a CLI or configured MCP server. It provides guidance for interpreting verification scope, verdicts, and evidence freshness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external Sail installer and release binaries were not verified by the supplied scan.

Mitigation: Review the installation instructions and verify the release source before installing Sail.

Risk: Persistent verification caches and automatic background preparation can use disk space and CPU time.

Mitigation: Monitor cache and preparation activity, and set SAIL_BACKGROUND_PREPARE=0 to disable automatic preparation when it is not wanted.

Risk: A cached result can be mistaken for current proof evidence if input freshness, verification scope, or verdict is overlooked.

Mitigation: Check the reported scope, verdict, and currentness; rerun verification after relevant input changes.

## Reference(s):

- [Verus workflows](references/verus.md)
- [SMT requests](references/smt.md)
- [Sail installation guide](https://github.com/Chelis-Lang/sail/blob/main/docs/install.md)
- [Sail compatibility](https://github.com/Chelis-Lang/sail/blob/main/docs/compatibility.md)
- [Sail runtime documentation](https://github.com/Chelis-Lang/sail/blob/main/docs/runtime.md)
- [Standalone verification](https://github.com/Chelis-Lang/sail/blob/main/docs/standalone-verification.md)
- [Background preparation](https://github.com/Chelis-Lang/sail/blob/main/docs/background-preparation.md)
- [Sail MCP documentation](https://github.com/Chelis-Lang/sail/blob/main/docs/mcp.md)
- [Proof repair walkthrough](https://github.com/Chelis-Lang/sail/blob/main/docs/proof-repair-walkthrough.md)
- [Verification freshness](https://github.com/Chelis-Lang/sail/blob/main/docs/freshness.md)
- [CI cache guide](https://github.com/Chelis-Lang/sail/blob/main/docs/ci-cache.md)
- [Workspace hygiene](https://github.com/Chelis-Lang/sail/blob/main/docs/workspace-hygiene.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with shell command examples, JSON request examples, and verification guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes CLI and MCP workflows, proof and query interpretation guidance, and cache management instructions.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
