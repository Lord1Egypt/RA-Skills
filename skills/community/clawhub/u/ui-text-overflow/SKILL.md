---
name: ui-text-overflow
description: Use when checking whether text in a user interface fits its container and stays readable when it changes — uneven text length across sibling components (cards, list rows), truncated text with no way to read the rest, and layouts that break with longer copy, a translation or larger text. Reports line counts and a character budget; it does not rewrite the copy.
triggers:
  use_when:
    - user asks why cards or list rows look uneven because their texts have different lengths
    - user asks how long a title or description can be for a component
    - user asks to check truncation, ellipsis, line clamp or max lines
    - user asks whether a layout survives longer text, translation or larger text size
    - agent has Figma access and user asks to check text overflow or text fit in selected components
  do_not_use_for:
    - column width for reading (see line-length-optimizer)
    - shortening or rewriting copy (a content task — this skill only gives the budget)
    - spacing between blocks (see vertical-spacing)
    - line-height and tracking (see text-typesetting)
metadata:
  author: Monika Zapisek
  project: Design Engineering Playbook
  version: "1.1.0"
  status: draft
---

# UI Text Overflow

## Purpose

Check how text sits in the container it was given: whether sibling components carry comparable amounts of text, whether anything is cut off without a way to read it, and whether the layout holds when the text gets longer or larger. The output is a measurement and a budget that a writer or designer can act on.

## When To Use

- A grid of cards or a list where some items run to one line and others to four.
- Deciding how many characters a title, label or description may have.
- Reviewing truncation: ellipsis, max lines, fixed-height text boxes.
- Before handoff or localisation: does the layout survive longer strings and larger text?
- Not for choosing a comfortable reading width (`line-length-optimizer`), and not for rewriting text to fit.

## Questions

This skill is an audit, not an interview. Work in this order: read what the file or the input already says, report, then ask.

- Ask only when a value can't be read and the answer would change the result. One question at a time.
- Don't ask for anything the request already states or the file shows — say what you took and where it came from.
- If the question can't be answered, state the assumption and carry on. Never stall the report on it.
- Always ask before writing to a file or a Figma node.

Questions this skill may need:

- Which languages the interface ships in, when checking room for translation.
- Whether the full text is available somewhere else (detail view, tooltip, expand), when a text is truncated and the file doesn't show it.

## Inputs

- The components to compare: a set of siblings (cards in a grid, rows in a list), or one component with its text.
- For each text: its content, the width it has, and its line-height.
- If known: target languages, and whether users can change text size on the platform.

## Outputs

- Per text role (title, description, …): lines per sibling, shortest and longest, and which siblings are outliers.
- A character budget per role: a range a writer can aim for.
- A list of truncated texts, each marked as "full text reachable" or "full text not reachable".
- Result of the resilience check: what breaks, and at which condition.

## Workflow

### Rule 1 — Compare siblings by lines, not by characters

Readers see uneven line counts, not character counts. For each text role across the sibling set:

1. Count the lines each sibling's text takes at its current width.
2. Report the minimum, the maximum and the most common value.
3. Flag siblings whose line count differs from the most common value.

A difference in line count is a finding to report, not an error by itself. No typographic source prescribes equal text lengths across cards; what the sources do require is that the content stays available (Rule 3) and the container adapts to it (Rule 4). Say this when reporting, so an uneven grid isn't presented as a rule violation.

### Rule 2 — Give a character budget

Turn the measurement into something a writer can use:

```
characters per line = characters in the text / lines it takes     (averaged over the siblings)
budget              = characters per line × target number of lines
```

- Take the target number of lines from the most common value among the siblings, or from the design if it states one.
- Give the budget as a range, from one line short of the target to the full target — a text that ends mid-line reads better than one that fills the last line to the edge.
- State that the budget is derived from the current text and font. It moves when the font, size or width changes, and it is tighter in languages with longer words.
- Don't shorten or pad the copy. Report which texts are over or under budget and leave the wording to a content pass.

### Rule 3 — Truncation must leave a way to read the rest

Platform requirement (Material Design 3, "Text truncation"): information stays available to the reader even when text is truncated or wrapped.

- Prefer wrapping. Truncate only when the text is not critical for understanding, or when wrapping is impossible in the component.
- An ellipsis is acceptable only if the full text is reachable — a linked detail view, an expand control, a tooltip. An ellipsis with no way to see the rest is an accessibility failure, not a style choice.
- For every truncated text, name where the full text can be read. If you can't find it, mark it "full text not reachable".
- Don't set a line limit tighter than the space the component already has.

### Rule 4 — The container follows the text

Platform requirement (Material Design 3): use flexible containers that change size to fit their content.

- A text box with a fixed height is a risk: longer text is clipped silently. Flag fixed-height text and fixed-height parents of text.
- In a row of siblings, decide deliberately between equal heights (the shorter cards carry empty space) and natural heights (the row is uneven). Report which one the design uses; don't change it unasked.

### Rule 5 — Resilience check

Check the layout under the conditions real use produces. Report the first condition at which content is lost or overlaps.

| Condition | What to apply | Source |
|---|---|---|
| Longer copy | The longest string the component already holds elsewhere in the file, placed in every sibling | — |
| Translation | Real strings in the target languages. English is often shorter than other European languages; German compounds run long | Google Fonts Knowledge, "Language support in fonts" |
| User text spacing | Line height 1.5 × font size, paragraph spacing 2 ×, letter spacing 0.12 ×, word spacing 0.16 × — content and function must survive | WCAG 2.2, SC 1.4.12 |
| Larger text | The platform's larger text setting; the hierarchy between text roles must remain visible | Apple Human Interface Guidelines, "Typography" |

The WCAG values are a robustness test, not recommended settings. Don't write them into the design.

## Figma Node Integration

When running with Figma access, work on the selected components instead of asking for pasted text.

- **Find the siblings.** Instances of the same component under one parent, or the frames the user selected. Match text nodes across siblings by layer name.
- **Read:** `characters`, `width`, `height`, `lineHeight`, `fontSize`, `textAutoResize`, `textTruncation`, `maxLines`.
- **Line count.** The Plugin API doesn't expose line boxes. For a node with `textAutoResize: "HEIGHT"`, estimate lines as `height / line-height in px`, rounded. Resolve a percentage or `AUTO` line-height to px first; say when the value is an estimate.
- **Truncation.** `textTruncation: "ENDING"` (optionally with `maxLines`) or `textAutoResize: "TRUNCATE"` means text can be cut. `"NONE"` with content taller than the box means text is clipped with no ellipsis — report that as the more serious case.
- **Fixed heights.** `textAutoResize: "NONE"` or `"TRUNCATE"` on the text, or a parent Auto Layout frame with a fixed height on the text's axis.
- **Resilience check needs writes.** Applying longer strings or spacing changes edits the layers. Run it on a duplicate of the frame, ask first, and remove the duplicate afterwards.
- **Action back to Figma:** on request only — set `textAutoResize: "HEIGHT"` so the box follows the text, or set `textTruncation` and `maxLines` where truncation is agreed and the full text is reachable. Never edit `characters` to make a text fit.

## Quality Checklist

- [ ] Siblings compared by line count; outliers named.
- [ ] Uneven lengths reported as a measurement, not as a broken rule.
- [ ] Character budget given as a range, with the font, size and width it was derived from.
- [ ] Copy not rewritten, shortened or padded.
- [ ] Every truncated text marked reachable or not reachable.
- [ ] Fixed-height text and clipped text flagged.
- [ ] Resilience check states which conditions were applied and which were skipped.
- [ ] Line counts from Figma labelled as estimates.
- [ ] Figma writes only on explicit request; the resilience check run on a duplicate.

## References

- Google. *Material Design 3*, "Text truncation" (Foundations › Writing and text) — content stays available when text is truncated or wrapped; wrap first; ellipsis only with a way to reveal the text; flexible containers.
- W3C. *Web Content Accessibility Guidelines 2.2*, Success Criterion 1.4.12 Text Spacing — no loss of content or functionality at the listed spacing values.
- Apple. *Human Interface Guidelines*, "Typography" — keep the relative hierarchy of text elements when people adjust text sizes.
- Google Fonts Knowledge, "Language support in fonts" — word length varies across languages; English is often shorter than other European languages.
- Figma Plugin API Docs: `TextNode.textAutoResize`, `TextNode.textTruncation`, `TextNode.maxLines`.
- Related skills: [`line-length-optimizer`](../line-length-optimizer/README.md) (reading width), [`vertical-spacing`](../vertical-spacing/README.md) (space between the blocks), [`microtypography`](../microtypography/README.md) (line endings inside the text).
