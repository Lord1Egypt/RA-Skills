## Description:

Runs an end-to-end vnstock workflow for free-tier-safe Vietnam stock valuation, ranking, and API operations with strict rate-limit control; used when users request Vietnamese stock analysis under free-tier constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teahann](https://clawhub.ai/user/teahann)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to screen, value, rank, and summarize Vietnamese equities with vnstock while observing free-tier request limits. It supports both end-to-end valuation runs and targeted vnstock API calls for market data, company data, financial ratios, trading data, and fund listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dynamic vnstock invocation helper can execute broad local Python class and method calls when supplied untrusted module, class, method, or argument values.

Mitigation: Run the skill only in an isolated environment and allow only reviewed, trusted invocation arguments.

Risk: API keys passed with command-line flags can be exposed through process listings, logs, shell history, or generated output files.

Mitigation: Prefer environment-based or skill-local key loading, avoid inline --api-key values, restrict file permissions, and redact generated artifacts before sharing.

Risk: The skill depends on external vnstock packages and live data providers while server-resolved import provenance is unavailable for this release.

Mitigation: Pin and review vnstock dependencies before installation, install in a disposable environment, and confirm package sources before execution.

Risk: Market, financial, and ranking outputs can be incomplete, stale, or source-dependent, which can make investment conclusions misleading.

Mitigation: Require the documented coverage, missing-field, confidence, and risk sections, and treat generated rankings as screening inputs rather than final investment advice.

## Reference(s):

- [VNStock Capability Reference](artifact/references/capabilities.md)
- [Free-Tier Playbook](artifact/references/free_tier_playbook.md)
- [VNStock Method Matrix](artifact/references/method_matrix.md)
- [Invocation Recipes](artifact/references/invocation_recipes.md)
- [VNStock Documentation README](artifact/references/vnstock/README.md)
- [VNStock Overview](artifact/references/vnstock/01-overview.md)
- [VNStock Installation](artifact/references/vnstock/02-installation.md)
- [VNStock Official Website](https://vnstocks.com)
- [VNStock Plans and Rate Limits](https://vnstocks.com/insiders-program)

## Skill Output:

**Output Type(s):** [text, markdown, json, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON handoff bundles, CSV/JSON data artifacts, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis outputs should include what was run, coverage, top results, key risks, confidence, and gaps.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
