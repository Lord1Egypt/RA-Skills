# Contributing

Keep `use-skills` small, readable, and focused on skill selection.

## Contribution Guidelines

- Keep examples realistic.
- Keep the working set small.
- Keep `README.md`, `REFERENCE.md`, and `SKILL.md` aligned.
- Update examples when behavior changes.
- Preserve the three modes: `All related`, `Recommended`, and `Restricted`.
- Preserve mode choice behavior: when `$use-skills` is invoked and no reusable prior mode exists, ask the user to choose with a numbered `1`, `2`, `3` menu before any exploration or skill selection.
- Preserve mode menu formatting: standalone fenced `text` block, one required empty line between option blocks, bare skill names, and the reply instruction after the options.
- Prefer clear wording over dense rule language.

## Good Contributions

- clearer examples
- better mode-selection guidance
- simpler wording
- documentation fixes
- sharper match criteria
- stronger hard-gate wording for ambiguous mode requests
- clearer mode menus that mention likely skill candidates without using tools first

## Changes To Avoid

- long catalogs of unrelated advice
- making the skill run for every request
- adding skills that do not improve the output
- expanding the working set so far that responses become noisy
- repeatedly asking for mode selection when the prior choice still fits
- inferring a mode from vague words like `best`, `most relevant`, or `strongest`
- asking a bare mode question that does not explain what each choice will use

## Review Checklist

- The change improves output quality.
- The docs still match `SKILL.md`.
- The wording stays concise.
- The examples match the current behavior.
- The mode menu remains clear enough to choose by replying with `1`, `2`, or `3`.
