# Form: letter

**Register:** `formal`

A form file supplies slots. Only the voice may fill them. Every quoted phrase in this file is under Tells, and every one of them is a phrase to avoid.

A letter is not a long email. It has no subject line, so the first paragraph carries the BLUF that a subject would have carried, and it is meant to be read once, in order, on paper or as a PDF. That changes what the shape has to do: a reader cannot scan back up a printed page as cheaply as they can scroll.

## Slots

- **Sender block.** Whatever the voice defines. Absent in a letter on headerless stationery.
- **Date.** Its own line, above the recipient block. This is the one slot with a mechanical half: the voice's `date_format` mechanic decides the spelling, and a letter is the form where an ambiguous numeric date does the most damage, because there is no thread above it to date the document by.
- **Recipient block.** Name, title, organization, address. Each on its own line.
- **Salutation.** One line. Formality set by the relationship, from the voice, not from this file.
- **Body.** BLUF in the first paragraph, then the evidence. Paragraphs may run longer here than anywhere else in the register set. A letter is read in one pass with no scrolling, and the airiness that helps on a screen fragments an argument on a page.
- **Closer.** One line, from the voice.
- **Signature block.** Whatever the voice defines.
- **Enclosures.** Named, if any. A letter that mentions an attachment without listing it leaves the reader unable to tell whether something went missing in the post.

## Bands

| Purpose | Band |
|---|---|
| A cover letter | one page, which is roughly 400 words with the blocks |
| A notice or a formal request | one page |
| A letter of reference | one to two pages |
| A complaint or a dispute | as long as the facts require, and every paragraph is a fact |

Paragraph length runs about half again what an email tolerates. Three to six sentences reads normal on a page where three to five reads normal on a screen.

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "I am writing to you today regarding" and every variant that spends a sentence announcing that a letter is a letter.
- "Please find attached", where a plain statement of what is enclosed does the same work.
- "I would like to take this opportunity to."
- "Thank you for your time and consideration" as an automatic closer rather than a chosen one.
- A closing paragraph that summarizes the letter. The reader finished it thirty seconds ago.
- Headers and bullets. A letter that needs them wanted to be a memo, and the right fix is to send a memo.
- Emoji, in any position.

## What the mechanical layer sees here

A one-page letter sits near the reliability floor, so the stylometric numbers are thin and the judgment above carries the load. Two mechanical checks matter more here than anywhere else. The date, for the reason in the Slots section. And the fact check in `verify.py`, because a letter is the form most likely to be a document of record, and a number that changed between draft and sent is the failure that outlives the letter.

The `formal` rung runs the extra-strict cells. In a letter that is the correct setting and not a harsh one: promotional language and significance inflation are what a reader discounts a formal letter for.
