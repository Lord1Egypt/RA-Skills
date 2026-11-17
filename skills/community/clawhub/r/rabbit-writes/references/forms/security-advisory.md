# Form: security-advisory

**Register:** `docs`

A form file supplies slots. Only the voice may fill them. Every quoted phrase in this file is under Tells, and every one of them is a phrase to avoid.

A published notice that a specific product version has a specific flaw, telling affected readers what to do. Its reader is triaging under time pressure with a list of other advisories open, and every constraint on the form comes from that: they need to know whether they are affected before they need to know anything else.

This form describes the writing, never the disclosure. Timing, coordination, embargoes, and whether to publish at all are decisions the reader's own policy and any coordinating body govern, and nothing here overrides them.

## Slots

- **Identifier and title.** Whatever identifiers apply, then one line naming the flaw class and the affected component.
- **Affected versions.** Exact ranges, and the unaffected ones stated too. A reader on a version the advisory does not mention has to guess, and they will guess wrong in whichever direction is cheaper.
- **Severity.** With the scoring vector, not the number alone. A number with no vector cannot be re-scored against the reader's own deployment, which is the only scoring that matters to them.
- **Impact.** What an attacker gains. Concrete, and bounded by what is actually reachable.
- **Preconditions.** What an attacker needs: network position, authentication, a non-default configuration. This is the section that turns a critical score into a low one for most readers, and leaving it out wastes their afternoon.
- **Remediation.** The fixed version, first. Then the upgrade path.
- **Workarounds.** For readers who cannot upgrade today, with the cost of each stated.
- **Detection.** How a reader checks whether they are affected, and whether they were exploited. Two different questions, and both belong here.
- **Timeline and credit.** Report date, fix date, publication date. Credit as the reporter asked for it.
- **References.** Advisories, commits, and any standard cited.

## Bands

| Purpose | Band |
|---|---|
| A single flaw with a clean fix | 200 to 500 words |
| A flaw needing configuration guidance | 500 to 1,200 words |
| A multi-component advisory | one section per component, and consider splitting it |

Shorter is better in this form, in a way that is not true of the others here. Every sentence a triaging reader has to read before finding their version is a cost.

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "All users are strongly encouraged to update immediately" as a substitute for stating the preconditions.
- "A critical vulnerability" where the scoring vector shows it needs local access and a non-default setting.
- "There is no evidence of exploitation in the wild" stated as reassurance rather than as a fact with a date on it.
- "We take the security of our users seriously."
- Marketing language anywhere. An advisory is read by people whose job is to distrust it.
- A remediation section that names a fixed version without naming the vulnerable ones.
- Exploitation detail beyond what a defender needs to detect and remediate.
- A severity rating with no vector.

## What the mechanical layer sees here

`docs` relaxations apply, and the vocabulary partial mode is what makes them right: security writing is dense with terms the general tiers would flag, and the exemption list drops the ones that carry real meaning while still catching the ones that never do.

Skipped here: uniform paragraph length, excessive bullets, bullet-NP lists, and list-label periods. An affected-versions list and a workaround list are those shapes on purpose.

What runs at full strength is the `safety` band, every P0 fingerprint, and the placeholder check. An advisory published with an unfilled template field is a credibility problem in the one genre that cannot afford one.

Significance inflation relaxes to one hit in this register, and one is the right budget here. An advisory that reaches for emphasis twice is an advisory the reader starts discounting, and the next one from the same source gets read slower.
