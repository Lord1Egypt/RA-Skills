## Description:

Guide for SenseAudio voice selection, plan-level voice entitlement checks, and cloned voice usage constraints in TTS calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to troubleshoot SenseAudio voice availability, check plan-level voice entitlements, configure cloned voice usage, and decide fallbacks when a requested voice is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A requested paid or cloned voice may be unavailable if the account tier or platform entitlement is not confirmed.

Mitigation: Confirm the exact voice_id, account tier, and platform voice-list result before using a paid or cloned voice in production.

Risk: Dictionary-based polyphone correction may be misapplied to unsupported voices or models.

Mitigation: Verify clone voice usage and current model compatibility before enabling dictionary behavior; provide a fallback without dictionary when unsupported.

## Reference(s):

- [Voice and Cloning Reference](references/voice.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable behavior; guidance centers on voice IDs, entitlement checks, cloned voice constraints, and fallback selection.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
