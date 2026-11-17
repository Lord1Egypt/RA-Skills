# Estimative language

Standardized terms for marking judgments. Read before attaching a probability term or a confidence marking to anything.

## Two separate axes

**Probability** is how likely the judgment is to be correct.
**Confidence** is how good the basis for judging is.

They move independently. "Unlikely, confidence High" is coherent: strong corroborated evidence supporting a call that something will not happen. "Likely, confidence Low" is also coherent, and is the more important one to be able to say, because it warns the reader that the call rests on thin ground.

Marking only one axis is the common failure. A bare "probably" tells the reader nothing about whether it rests on a measurement or a hunch.

## Probability ladder

Above an even chance:

- almost certainly
- very likely
- likely

At the midpoint:

- roughly even chance

Below an even chance:

- unlikely
- very unlikely
- almost certainly not

Use these terms and no others. Do not blend them ("fairly likely"), do not stack them ("very almost certain"), and do not attach a percentage unless a real measurement produced it.

## Confidence levels

- **High.** Strong, high-quality, corroborated information. Still not certainty.
- **Moderate.** Credible information, but limited, or corroboration is incomplete.
- **Low.** Fragmented or questionable information, notable source concerns, or known gaps.

Always give a one-line basis alongside the level. "confidence High" says less than "confidence High - reproduced on three runs with identical output". The basis is what lets the reader disagree with the marking itself.

## Banned phrasings

These read as different probabilities to different readers, which defeats the point of standardizing:

- "serious possibility"
- "fair chance"
- "may or may not"
- "it is possible that"
- "cannot be ruled out"

Each carries no information because almost nothing can be ruled out. Replace it with a ladder term, or drop the claim.

## Fact, assumption, judgment

- **Fact.** Verifiable now against a reliable source. An exit code you observed. A line in a file you read. A version string a command printed. Facts take no probability term.
- **Assumption.** Something taken as true in order to proceed, not verified. Assumptions get stated, because an unstated one is invisible when it turns out wrong.
- **Judgment.** An assertion that cannot be verified at the time it is offered, including every claim about what will happen. Judgments take a probability term and a confidence marking.

The test that catches the common error: a statement delivered assertively is still a judgment if it could not be proven at the moment it was made. Conviction in the delivery is not evidence. A forecast stated flatly reads as a fact to a busy reader, which is how speculation ends up quoted back later as established.

## Worked markings

- `BLUF: The flake is a timeout, not a race. Very likely, confidence Moderate - reproduced 4 of 5 runs under load, no reordering in the trace.`
- `BLUF: Migrating now breaks the mobile client. Almost certainly, confidence High - the client pins the v1 schema at three call sites, all read paths.`
- `BLUF: Bumping the pin fixes it. Roughly even chance, confidence Low - the upstream changelog does not mention this path and there is no local repro yet.`
