## Description:

Runs a patched Bitcoin Core node with built-in CPU mining, configurable resource controls, verification, build, update, and mining workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happybigmtn](https://clawhub.ai/user/happybigmtn)

### License/Terms of Use:


## Use Case:

Developers and node operators use this skill to install, verify, build, update, run, and mine with an rBitcoin node derived from Bitcoin Core.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts CPU cryptocurrency mining by default, which can consume local compute resources.

Mitigation: Set START_MINER=0 unless mining is intentional, and cap resource use with MINER_CPU_PERCENT and MINER_MAX_THREADS.

Risk: The default patch-hash acceptance setting can weaken patch-pinning controls.

Mitigation: Set AUTO_ACCEPT_NETWORK_PATCH_HASH=0 and manually review patch-hash changes before accepting them.

Risk: Running the skill can involve Bitcoin network participation and persistent blockchain storage.

Mitigation: Install only on machines where network participation, storage use, and local mining behavior are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/happybigmtn/skills/rbtc)
- [Source repository](https://github.com/happybigmtn/rBTC)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include environment variable settings for CPU mining, node networking, patch verification, build, update, and rollback workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
