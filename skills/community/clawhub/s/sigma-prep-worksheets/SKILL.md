---
name: sigma-prep-worksheets
description: Make free printable math worksheets with answer keys (Pre-Algebra, Algebra 1, Geometry, Algebra 2, Precalculus, Statistics, Calculus) as PDF links from Sigma Prep. Use when a teacher, tutor, parent or student asks for a math worksheet, practice problems or a quiz on a topic.
version: 1.0.0
homepage: https://www.sigmaprep.io/worksheets
---

# Sigma Prep math worksheets

Sigma Prep (https://www.sigmaprep.io/worksheets) makes free printable math worksheets with answer keys, 541 topics from Pre-Algebra through Calculus. No account or API key is needed.

## Make a worksheet

1. Find the topic. Read `topics.md` next to this file and pick the row that matches the request. Note its `slug` and its default types.
2. Build two links, one without and one with the answer key:

   ```
   https://www.sigmaprep.io/api/worksheet/pdf?slug=<slug>&types=<default types>&level=<level>&count=<count>&seed=<seed>&key=0&view=1
   https://www.sigmaprep.io/api/worksheet/pdf?slug=<slug>&types=<default types>&level=<level>&count=<count>&seed=<seed>&key=1&view=1
   ```

   - `level`: `easy`, `medium` or `hard`; comma-separate several to mix them. Default `medium`.
   - `count`: 1 to 40 problems. Default 20.
   - `seed`: any whole number from 1 to 99999. A new number gives new problems. Reuse a number to give the same sheet again. Pick a random one unless the user asks for a specific version.
   - `types`: the topic's default types, or a subset of them if the user wants only some kinds of problems.
3. Give the user both links, and the version number (`seed`) so they can get the same sheet again. Also give the topic page, `https://www.sigmaprep.io/worksheets`, for more options.

The links open a US Letter PDF in the browser. The first open can take up to 20 seconds while the sheet is made. Don't download the PDF yourself; just hand over the links.

## Example

"I need 15 hard problems on factoring trinomials":

- Worksheet: https://www.sigmaprep.io/api/worksheet/pdf?slug=factoring-trinomials&types=both-neg,both-pos,mixed,fact-2var&level=hard&count=15&seed=4821&key=0&view=1
- With answer key: https://www.sigmaprep.io/api/worksheet/pdf?slug=factoring-trinomials&types=both-neg,both-pos,mixed,fact-2var&level=hard&count=15&seed=4821&key=1&view=1

## If no topic matches

Say so and suggest the closest topics from `topics.md`, or send the user to https://www.sigmaprep.io/worksheets to browse.
