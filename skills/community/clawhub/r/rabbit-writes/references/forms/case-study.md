# Form: case-study

**Register:** `blog`

A form file supplies slots. Only the voice may fill them. Every quoted phrase in this file is under Tells, and every one of them is a phrase to avoid.

An account of one situation, told in enough detail that a reader can judge whether it resembles theirs. The value is entirely in the specifics, which is why the genre fails so reliably: a case study written to be reusable across customers has had removed from it the only thing that made it worth reading.

It sits at `blog` rather than `formal` because it is published, narrative, and read voluntarily. What it borrows from the formal forms is the evidence discipline, and the Tells below are where that lives.

## Slots

- **Title.** The outcome or the situation, with a number in it where there is one.
- **Who and what.** The organization, the scale, the constraints, the starting state. A reader deciding whether this applies to them decides here.
- **The problem, as it was experienced.** Symptoms before diagnosis. What people noticed, in what order.
- **What was tried.** Including what did not work. A case study with no failed attempt is a case study with the failed attempts edited out, and readers assume that whether or not it is true.
- **What was done.** At the level of mechanism, so a reader could attempt it.
- **The result.** Measured, against a stated baseline, over a stated period.
- **What did not change, and what it cost.** The slot that makes the rest believable.
- **Where this does not transfer.** The conditions that made it work here.

## Bands

| Purpose | Band |
|---|---|
| A short account, one change | 600 to 1,200 words |
| A full case study | 1,200 to 3,000 words |
| A customer story with a quotation and a logo | still 600 to 1,200 words, and the quotation is not evidence |

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "The challenge", "The solution", "The results" as three headers with nothing under them but the same claim three times.
- "Seamless integration" and "unprecedented efficiency gains."
- "Increased productivity by 40%" with no baseline, no period, and no definition of productivity.
- "The team was thrilled with the outcome."
- A named customer quotation used in place of a measurement.
- A problem statement generic enough to belong to any customer in the segment.
- An implementation section that skips the part where something broke.
- A percentage where the absolute number would be small enough to be unimpressive.

## What the mechanical layer sees here

`blog` relaxes almost nothing, so a scan here is close to the engine's strictest reading of prose. That is the right setting for this form: the failure mode is inflation, and the rules that catch inflation all run.

The one thing the mechanical layer cannot see is the thing that decides whether the document works. A number with no baseline passes every regex in the engine. Run the portability test on the problem statement and on the result: if either would be just as true of a different customer, the specifics were removed on the way to publication and there is nothing left to check.

Length clears the reliability floor, so burstiness and paragraph spread mean something. Uniform sections are the tell of a template filled in rather than an account written.
