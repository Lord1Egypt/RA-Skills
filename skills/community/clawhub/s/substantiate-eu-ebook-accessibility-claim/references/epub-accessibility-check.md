# Ebook Accessibility Check reference

Load this reference before the automated evidence step or when interpreting a single-build or comparison result.

## Scope

Ebook Accessibility Check version 0.3.2 runs a pinned local DAISY Ace engine in a network-isolated sandbox and renders EPUB content in a real headless browser.
It applies axe-core WCAG rules plus EPUB Accessibility 1.1 discovery-metadata checks, but does not check structural EPUB validity or scan web pages.

The single-build tool reports evidence grouped by WCAG success criterion.
Each returned rule can include impact, description, affected content-document count, and affected element count.
It also reports schema.org accessibility metadata state for `accessMode`, `accessibilityFeature`, `accessibilityHazard`, and `accessibilitySummary`.

The comparison tool runs the identical pinned evaluation over two proposed builds.
It checks package title, creator, and identifier before producing a remediation diff.
It withholds introduced, resolved, remediation, and ranking claims when those fields do not establish shared publication lineage.

## Single-build check

Use `powmcp-epub-accessibility-check:epub_accessibility_check` for one release EPUB.
Tell the user before the call that it can take up to about 90 seconds.

Provide exactly one source:

- `url`: one direct public HTTP(S) URL to EPUB file bytes.
- `file`: one EPUB attached in the conversation, up to 64 MB.

Do not provide both, and put an attached EPUB in `file`, not `url`.
A URL cannot be a local path, cloud-drive share, archive or viewer page, or authenticated URL requiring login.
Never repeat URL query strings or credentials.

`maxViolations` controls the maximum returned WCAG violations in most-severe-first order.
Its default is 400, its minimum is 1, and its maximum is 1000.
Set it only when the expected report size requires judgment.

## Build comparison

Use `powmcp-epub-accessibility-check:epub_accessibility_compare` whenever exactly two proposed builds are supplied for a before-and-after or cleaner-build question.
Tell the user before the call that it can take up to about 100 seconds.

Provide exactly one source pair:

- `urls`: exactly two distinct direct public HTTP(S) EPUB URLs, baseline first and revised second.
- `files`: exactly two distinct attached EPUB files, baseline first and revised second.

Do not provide both pairs, and put attachments in `files`, not `urls`.
`maxViolations` is the maximum collected per build; its default is 300, its minimum is 1, and its maximum is 600.

## Fields to quote

For `epub_accessibility_check`, quote these returned values without re-deriving, rounding, or embellishing them:

- `pass`
- Ace `engineVersion`
- `ruleProfileDate`
- `violationsState`
- WCAG success criterion, rule, impact, description, affected content-document count, and affected element count
- Counts by impact
- `metadataConformance`
- Truncation

Read `violationsState` with `pass`.
`not-checked` means no content document was evaluated and is unassessable.
`no-violations-found` means only that the pinned DAISY Ace run found no failure it can automate.
Truncation means the returned rule list is incomplete.

For `epub_accessibility_compare`, quote:

- Comparable or not-comparable state
- Per-build hashes and versions
- Per-build pass verdicts and impact counts
- Per-build discovery-metadata state
- Introduced and resolved rule lists when comparable
- Ranking when comparable
- Truncation when returned

The ranking orders automated conformance by pass state and then fewer violation instances.
It is not a ranking of genuine accessibility or EAA compliance.

## Interpretation limits

A pass proves only the result of Ace's automated subset for the evaluated content, engine version, dated rule profile, artifact, and check date.
It does not prove full accessibility, WCAG conformance, EPUB Accessibility 1.1 conformance, or legal compliance with the European Accessibility Act.
Human review is still needed for alt-text quality, reading order, semantics, navigation, hazards, assistive-technology behavior, and the reading experience.
DRM obstruction requires separate confirmation.

Structural EPUB validity is unassessed because these tools answer the accessibility question rather than running EPUBCheck.
Run EPUBCheck separately for structural conformance.
An absent finding is not an endorsement of an unmeasured feature.
A rule identifier names a rule, not a diagnosis.
Open the cited location and apply the message as returned without expanding what the defect means.

## Source and argument failures

For invalid source selection, tell the user the applicable line:
`Accessibility check failed: provide exactly one source: a public EPUB URL or an attached EPUB file`
`Accessibility compare failed: provide exactly one source pair: two public EPUB URLs or two attached EPUB files`

For duplicate attached comparison inputs, repeat this line verbatim: `Accessibility compare failed: the two attached files must be distinct builds`

If an invalid-arguments error names a field, correct that field and call again; an invalid argument is not a missing tool and does not trigger the missing-tool two-path response.

## Non-PowMCP path

Download the release EPUB, install and run the free DAISY Ace checker locally, and retain its report.
The wider procedure remains the same: remediate reported issues, run EPUBCheck separately, inspect package accessibility metadata, complete qualified manual checks, confirm that DRM does not obstruct assistive technology, map the verified description into ONIX codelist 196, and reconcile EPUB and ONIX representations.
The retained local Ace report replaces the single-build PowMCP evidence result.
For a two-build deliverable, it does not supply the comparison tool's package-lineage decision, remediation diff, or ranking; do not recreate those claims from separate local reports.

## Source-of-truth links

- App page: https://powmcp.com/apps/epub-accessibility-check/
- DAISY ONIX accessibility metadata guidance: https://kb.daisy.org/publishing/docs/metadata/onix/
- W3C accessibility metadata crosswalk: https://w3c.github.io/a11y-discov-vocab/crosswalk/
- AccessibilitySummary authoring guidelines: https://github.com/benetech/AccessibilitySummaryEPUBMetadata/blob/master/AccessibilitySummaryAuthoringGuidelines.md
- EDItEUR accessibility metadata application note: https://www.editeur.org/files/ONIX%203/APPNOTE%20Accessibility%20metadata%20in%20ONIX.pdf
- European Accessibility Act ebook checklist: https://publica.la/en/blog/european-accessibility-act-checklist-ebook-store-compliant
