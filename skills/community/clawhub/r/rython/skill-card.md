## Description:

Compile Python to native Rust with the rython toolchain (rythonc/rypip): single files, packages, no_std embedded targets, PyO3 bindings, userspace drivers, and Linux kernel modules — output verified byte-identical to CPython.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rexlunae](https://clawhub.ai/user/rexlunae)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Rython to convert Python files or packages into Rust source, crates, binaries, PyO3 bindings, no_std targets, userspace drivers, or kernel-module projects while keeping Python as the source of truth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kernel-module workflows can load or unload kernel code and affect the host system.

Mitigation: Require explicit approval before running make load, make unload, insmod, or rmmod, and perform kernel-module experiments in an isolated VM or disposable test system.

Risk: Installation workflows can place binaries in ~/.cargo/bin and change the developer environment.

Mitigation: Require explicit approval before installing toolchain outputs or generated binaries into user-level executable paths.

Risk: Rython has documented conversion boundaries, so unsupported Python constructs can fail conversion or require refactoring.

Mitigation: Keep Python as the source of truth, use strict warning settings for correctness-sensitive work, verify output against CPython, and regenerate instead of editing generated Rust by hand.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rexlunae/skills/rython)
- [Publisher profile](https://clawhub.ai/user/rexlunae)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with inline bash commands and code-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent guidance may include conversion flags, build steps, compatibility notes, and verification steps.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
