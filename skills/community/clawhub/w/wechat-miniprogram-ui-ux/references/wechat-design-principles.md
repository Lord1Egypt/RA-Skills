# WeChat Mini Program Design Principles

This file distills the official WeChat Mini Program design guidance into execution rules for coding work.

## Core Principles

### Friendly and polite

- Reduce irrelevant decoration that distracts from the task.
- Guide the user with clear, calm copy instead of forcing exploration.
- Explain sensitive actions and permissions in plain language.

### Clear and focused

- Every page needs a single obvious purpose.
- The first screen should answer:
  - What page is this?
  - What can I do here?
  - What should I do next?
- Keep unrelated actions out of the main decision path.

### Efficient and graceful

- Keep steps short.
- Prefer direct manipulation over hidden workflows.
- Use immediate feedback for taps, submissions, loading, success, and failure.
- Reduce waiting anxiety with loading indicators or skeletons when needed.

### Stable and consistent

- Preserve consistent navigation, button semantics, spacing, and tone.
- Keep destructive actions visually distinct.
- Keep similar content blocks styled the same across pages.
- Do not surprise the user with inconsistent role behavior.

## Mini Program-Specific Constraints

- The WeChat container adds navigation affordances and a top-right capsule area. Do not depend on custom controls fighting that region.
- Mini programs are mobile-first. Layouts should feel native on handheld screens before anything else.
- `rpx` is the default responsive sizing unit for layout work.
- Fixed bottom actions must account for safe-area insets.
- Long pages still need clear sectioning because users often enter from deep links or shared paths.

## Required State Design

Every production page should consider:

- Initial loading
- Loaded content
- Empty state
- Request failure
- Permission/login required
- Disabled or unavailable action state

Blank pages are not acceptable.

## Layout Heuristics

- Prefer a single-column reading flow.
- Use generous vertical spacing to separate sections.
- Group related metadata into small chips, rows, or cards.
- Keep the title and primary CTA visible without forcing interpretation.
- Use contrast and scale before using decorative effects.

## Forms

- Use explicit labels, not placeholders alone.
- Break long forms into logical sections.
- Validate close to the field whenever possible.
- Tell the user how to recover from invalid input.
- Disable submit only with visible reason, or allow submit and return specific validation errors.

## Lists and Detail Pages

### Lists

- Prioritize scanability over ornament.
- Filters and sort controls should be obvious and not overwhelm the first screen.
- Cards should expose the decision-making fields first.

### Detail pages

- Start with identity: title, image, owner, status, summary.
- Show the main action early.
- Defer secondary detail until after the action context is clear.
- If actions are role-specific, explain who can do what.

## Motion and Feedback

- Use short transitions to clarify state changes.
- Do not rely on hover behavior.
- Use toasts for lightweight feedback and visible inline states for blocking issues.
- For risky actions, confirm first and provide an obvious exit.

## Review Checklist

- Is the page purpose obvious in the first viewport?
- Is there one dominant action instead of several competing ones?
- Can a first-time user recover from failure or empty data?
- Are loading, empty, and error states visible and intentional?
- Does the layout respect mobile reading and tap behavior?
- Are destructive actions clearly separated from primary confirm actions?
- Does the page feel like a mini program instead of a transplanted web page?
