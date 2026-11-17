# Form: executive-summary

**Register:** `formal`

A form file supplies slots. Only the voice may fill them. Every quoted phrase in this file is under Tells, and every one of them is a phrase to avoid.

The page in front of a longer document, written for a reader who will not read the rest. That constraint is the whole form: an executive summary is not an introduction and not an abstract. An introduction sets up what follows and depends on it. A summary replaces it.

The test is whether a reader who has only this page can make the decision the document was written to support. If the answer needs a figure from page eleven, that figure belongs here.

## Slots

- **The finding, or the recommendation.** One or two sentences, first. Not the scope, not the method, not who commissioned it.
- **What it rests on.** The two or three numbers that carry the finding, with their units and their basis. Numbers here are copied from the document and never rounded into new ones.
- **What it means for the reader.** The decision this supports, or the action it implies.
- **What it costs, or what is uncertain.** The slot most often cut, and cutting it is what makes a summary read as a sales document.
- **Where to read more.** Section or page pointers into the parent document.

## Bands

| Purpose | Band |
|---|---|
| In front of a report under 20 pages | 150 to 300 words, one page |
| In front of a long report | up to 500 words, and never past one page |
| Standing alone as a briefing | 300 to 600 words, and then it is the document |

One page is a hard band rather than a soft one. A two-page executive summary is a document with no executive summary.

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "This report examines" as the first sentence. That is a scope statement, and scope is not a finding.
- "The purpose of this document is to."
- "Key takeaways" as a header on a document that is entirely key takeaways.
- "Further research is needed" with no statement of what research.
- A summary that describes the structure of the parent document instead of its findings.
- Every paragraph the same length, which happens when a summary is assembled by taking one sentence from each section.
- A recommendation with no cost, no risk, and no alternative considered.

## What the mechanical layer sees here

The `formal` extra-strict cells are the point of this form. Significance inflation and promotional language run at their strictest here, and this is the document where they cost the most, because the reader of an executive summary has the least context to check a claim against.

The document is short enough to sit under the reliability floor, so burstiness and type-token ratio say little. Ignore them and read the numbers.

`verify.py` is worth running on a summary against its parent document, with facts checked rather than allowed. A number that appears in the summary but not in the report is the failure this form invites, and the fact check compares them as multisets in both directions.
