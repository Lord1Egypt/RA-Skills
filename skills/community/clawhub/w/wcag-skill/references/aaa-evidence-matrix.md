# WCAG 2.2 AAA evidence matrix

Use this template only when the target is WCAG 2.2 AAA. AAA inherits every
applicable A and AA criterion. Create a row for every applicable A/AA criterion
from the [W3C Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/) and for
every AAA criterion below. “Not applicable” must include a concise rationale.

## Required record format

| SC | Applicable? | Route, state, or asset | Evidence and validation method | Result | Residual risk |
|---|---|---|---|---|---|
| 1.4.6 | Yes | `/checkout`, all breakpoints | Measured all normal-text pairs at ≥7:1; visual review | Pass | None recorded |

Use `Pass`, `Fail`, `Not applicable`, or `Needs human review`. Do not convert a
tool warning into a pass without explaining the decision.

## AAA success criteria

| SC | Criterion | Applicability prompt and required evidence |
|---|---|---|
| 1.2.6 | Sign Language (Prerecorded) | If prerecorded synchronized media exists, document sign-language interpretation or the applicable exception. |
| 1.2.7 | Extended Audio Description (Prerecorded) | If prerecorded video has pauses insufficient for description, document extended audio description. |
| 1.2.8 | Media Alternative (Prerecorded) | If prerecorded synchronized media exists, document a complete media alternative. |
| 1.2.9 | Audio-only (Live) | If live audio-only exists, document its equivalent alternative. |
| 1.4.6 | Contrast (Enhanced) | Measure every normal-text pair at ≥7:1 and large-text pair at ≥4.5:1, including hover, focus, disabled, error, and overlay states. |
| 1.4.7 | Low or No Background Audio | If prerecorded audio has speech, document the audio-control or background-audio exception. |
| 1.4.8 | Visual Presentation | Check user-adjustable presentation requirements, including foreground/background choice, width, line spacing, and resize behaviour where applicable. |
| 1.4.9 | Images of Text (No Exception) | Inventory images of text; replace with real text unless the specified exceptions apply. |
| 2.1.3 | Keyboard (No Exception) | Keyboard-test every function and state; document any functionality that cannot be operated without a keyboard. |
| 2.2.3 | No Timing | Document that time limits are absent or provide the applicable exception. |
| 2.2.4 | Interruptions | Document that interruptions can be postponed or suppressed unless essential. |
| 2.2.5 | Re-authenticating | Re-authenticate a representative session and show that user data is preserved. |
| 2.2.6 | Timeouts | For inactivity timeouts that can lose data, document warning and preservation for more than 20 hours or the applicable exception. |
| 2.3.2 | Three Flashes | Inspect all motion/video/ads; document that no content flashes more than three times in any one-second period. |
| 2.3.3 | Animation from Interactions | Check interaction-triggered motion can be disabled unless essential. |
| 2.4.8 | Location | For a multi-page set, identify the user’s current location through breadcrumbs, navigation, or another mechanism. |
| 2.4.9 | Link Purpose (Link Only) | Review every link in isolation; its accessible name must identify purpose except for the criterion’s exceptions. |
| 2.4.10 | Section Headings | Review long/complex content for descriptive section headings where headings organise content. |
| 2.4.12 | Focus Not Obscured (Enhanced, AAA) | Tab through breakpoints, overlays, sticky regions, error states, and menus; no part of a focused component may be hidden by author-created content. |
| 2.4.13 | Focus Appearance (AAA) | When a focus indicator is visible, verify that its area is at least the area of a two-CSS-pixel-thick perimeter of the unfocused component or sub-component, and that the same pixels have at least 3:1 contrast between focused and unfocused states. Exceptions: the user agent determines the indicator and the author cannot adjust it, or neither the indicator nor its background color is modified by the author. |
| 2.5.5 | Target Size (Enhanced) | Measure pointer targets at ≥44×44 CSS px or document the specific exception. |
| 2.5.6 | Concurrent Input Mechanisms | Confirm no author-created restriction disables a supported input mechanism. |
| 3.1.3 | Unusual Words | Identify idioms, jargon, and specialised terms; provide a mechanism for definition when needed. |
| 3.1.4 | Abbreviations | Identify abbreviations whose expanded form is needed for understanding; provide a mechanism for expansion. |
| 3.1.5 | Reading Level | If primary content exceeds lower-secondary reading level, provide supplemental content or an alternative version at that level. |
| 3.1.6 | Pronunciation | Where pronunciation is necessary to understand a word’s meaning, provide a mechanism for it. |
| 3.2.5 | Change on Request | Confirm context changes occur only at user request or document the criterion exception. |
| 3.3.5 | Help | Where context-sensitive help is available, provide it. |
| 3.3.6 | Error Prevention (All) | For every page that requires users to submit information, verify at least one: submissions are reversible; entered data is checked for input errors (required information omitted or values outside the required format or allowed values) with an opportunity to correct them; or users can review, confirm, and correct information before finalizing. Record which alternative is met and its evidence. |
| 3.3.9 | Accessible Authentication (Enhanced) | Test each authentication step; do not require a cognitive-function test unless an allowed alternative or mechanism is available. Do not rely on object recognition or personal content as the enhanced-level exception. |

## Inherited WCAG 2.2 requirements to call out

AAA also requires all applicable A and AA criteria. The AAA table above already
includes 2.4.12 Focus Not Obscured (Enhanced), 2.4.13 Focus Appearance, and
3.3.9 Accessible Authentication (Enhanced) — do not duplicate rows for those.
Explicitly verify the remaining WCAG 2.2 additions that are A/AA level: 2.4.11
Focus Not Obscured (Minimum), 2.5.7 Dragging Movements, 2.5.8 Target Size
(Minimum), 3.2.6 Consistent Help, 3.3.7 Redundant Entry, and 3.3.8 Accessible
Authentication (Minimum). Consult the W3C Quick Reference for the full
inherited set.

The following focus-related A/AA criteria are separate from the AAA focus
criteria above. Record each applicable criterion in the inherited A/AA
evidence rows:

| SC | Criterion and level | Required focus evidence |
|---|---|---|
| 1.4.11 | Non-text Contrast (AA) | Check visual information needed to identify UI components and states (except inactive components or appearances determined by the user agent and not modified by the author), and parts of graphics required to understand content (except an essential presentation), against adjacent colors at ≥3:1. This is distinct from SC 2.4.13's focused/unfocused same-pixel comparison. |
| 2.4.7 | Focus Visible (AA) | Verify every keyboard-operable user interface has at least one mode of operation in which its keyboard focus indicator is visible; the indicator must remain visible while focus is shown. |
| 2.4.11 | Focus Not Obscured (Minimum, AA) | Verify that when a component receives keyboard focus, it is not entirely hidden by author-created content. Content opened by the user may obscure focus if the user can reveal the focused component without advancing focus. Do not apply SC 2.4.12's stronger “no part hidden” requirement as the AA threshold. |

## Dynamic-state evidence for WCAG 4.1.2

WCAG 4.1.2 is an inherited Level A criterion. Record its evidence for each
interactive component and relevant state, including components whose states
change after interaction.

| Component / route / state | Name and role evidence | Initial value/state | Interaction and resulting value/state | Keyboard result | AT review |
|---|---|---|---|---|---|
| Example: `/settings`, theme toggle | Playwright role/name assertion | `aria-pressed=false`, light theme | Click: `aria-pressed=true`, dark theme | Space and Enter verified | Browser/AT, version, date, result |

Do not mark a changing state as verified from a static scan or automated
accessibility audit alone. Use `DYNAMIC TEST REQUIRED` until an interaction test
checks both the exposed state and the corresponding application state. For
custom widgets, live announcements, or state whose meaning depends on context,
record a manual assistive-technology review as well. See
[`dynamic-state-test-protocol.md`](dynamic-state-test-protocol.md).
