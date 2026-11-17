# Documentation: Canonical style and usable technical truth

For **every documentation artifact** (README, quickstart, tutorial, how-to, technical reference, explanation, API/CLI docs), enforce the **current Canonical/Ubuntu documentation style guide** as the sole house *writing style*: https://documentation.ubuntu.com/style-guide/ . This is a Second Read product choice. **Do not use Canonical's writing conventions for emails, PR, marketing, fiction or journalism.** Do not import an unrelated publication's house style into documentation.

Canonical's published guide, not this summary, is the authoritative source. When web access is available and a rule affects the edit, consult the current relevant section. Its conventions include US English, sentence-case headings, descriptive link labels, list clarity and code blocks that users can copy without stray shell prompts. Check the live guide for any exceptions or revisions.

## Organize by reader job, not author convenience

Canonical's Diátaxis-based documentation distinction is useful for classifying what the reader is doing:

- **Tutorial:** a guided learning experience; steps support learning rather than maximal flexibility.
- **How-to:** a focused procedure for a user who already has a goal; include prerequisites and success criteria.
- **Reference:** exact names, defaults, options, allowed values and behavior, organized for lookup.
- **Explanation:** background, concepts, decisions and tradeoffs; does not pretend to be a step-by-step procedure.

A README or first landing page should route readers toward the correct next page quickly. If a single page mixes modes, edit only the part where mode confusion actually blocks understanding.

## Verify product claims separately from style

Search available docs/source first. For commands, flags, outputs, UI labels, API arguments, versions and expected results, use authorized evidence and [PRODUCT-VERIFICATION](PRODUCT-VERIFICATION.md). Source inspection establishes *source corroboration* only; actual execution establishes runtime observation. Label missing tests `unknown` or `not checked` as appropriate. Do not invent a successful command or a UI screen.

## Paired decisions

**Edit, missing precondition:** the first command requires a token never introduced, and the linked setup notes explain where to obtain it. Add the shortest accurate prerequisite and link, preserving tested spelling.

**Edit, heading:** an H2 called “Introducing The Powerful New CLI” explains a single flag; replace with a sentence-case, task-accurate heading, subject to Canonical's current rules.

**Leave, functional command:** a verified `curl` example is terse and correct. Do not replace it with generic conceptual introduction or change parameter names for stylistic consistency.

**Leave, style vs truth:** a repository's actual CLI flag uses an underscore. Retain the flag even if prose naming preferences differ; code is not rewritten as English.

## Sources

- Canonical documentation style: https://documentation.ubuntu.com/style-guide/
- Canonical Diátaxis reference (architecture): https://diataxis.fr/
