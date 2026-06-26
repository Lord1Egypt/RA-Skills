# product-positioning

## What this skill is
A deliverable-oriented extraction skill.

It is not just OCR.
It is not just HTML scraping.
It is a workflow for turning visible information into something a human can read and reuse.

## Promise to the user
Given a public page, screenshot set, or image-heavy source, this skill should aim to return:
- the main readable content
- high-value facts from images
- a clean markdown result
- an optional Word deliverable
- explicit uncertainty notes when quality limits remain

## What a mature result looks like
- easy to read without opening raw JSON
- minimal garbage in the main body
- uncertainty separated, not mixed into the core narrative
- Word output suitable for sharing internally

## What this skill should avoid
- raw OCR dump as the default final output
- pretending completeness when the source is blocked
- mixing UI debris with article body text
- making users manually stitch multiple scripts unless they explicitly want control
