---
name: nielsen-ui-review
description: >-
  Run a structured UI/UX heuristic review based on Nielsen's 10 usability principles for screenshots, mockups, wireframes, product pages, app screens, and design comps. Use when the user provides a UI image or screen and asks to review, critique, evaluate, audit, or assess the interface, usability, UX, or design quality, including requests such as "review this UI", "evaluate this interface", "do a heuristic evaluation", "give me UI feedback", "assess usability", or Chinese requests like "评价一下这个界面", "帮我做 UI 评审", or "做个可用性分析". Ask a short clarification round first, using selectable options when possible, then generate prioritized findings and actionable recommendations.
---

# Nielsen UI Review

Review a UI image through the lens of usability, not personal visual taste. Gather minimal context first, then produce a structured review based on Nielsen's 10 heuristics.

## Core Behavior

- Start from the screenshot and any user-provided description.
- Ask a short clarification round before making strong judgments.
- Prefer multiple-choice options over open-ended questions.
- If the user skips clarification, state assumptions and continue.
- Separate visible evidence from inference.
- Prioritize issues that affect task success, comprehension, trust, and error risk.
- Give concrete recommendations tied to specific UI elements.
- Do not force issues into every heuristic if no issue is visible.

## Workflow

1. Inspect the screenshot.
2. Infer the likely screen type, platform, and primary task.
3. Ask 3 to 5 concise clarification questions.
4. Wait for answers if the user responds.
5. If the user does not respond, proceed with explicit assumptions.
6. Review the screen against Nielsen's 10 heuristics.
7. Summarize the most important issues first.
8. End with prioritized, actionable recommendations.

## Inspect First

Identify, if possible:

- Screen type: landing page, dashboard, form, checkout, settings, modal, onboarding, detail page, empty state, error state
- Platform: web, mobile, desktop, internal tool, consumer app
- Primary task: understand, compare, fill, submit, purchase, manage, configure, navigate
- Main hierarchy: title, key content, main CTA, secondary CTA, navigation, warnings, helper content
- Missing context: whether this is one state in a larger flow, whether content is real or placeholder, whether loading/success/error states exist elsewhere

If the screenshot is blurry, cropped, or too partial for high-confidence review, say so before continuing.

## Clarification Round

Ask 3 to 5 questions. Keep them short. Use options when possible. End with:

`If you're not sure, I can still do a first-pass review based on the screenshot and make my assumptions explicit.`

### Default Question Bank

Pick the most relevant questions from this list:

1. Product goal
- Increase conversion
- Improve task completion
- Reduce comprehension effort
- Increase trust
- Strengthen brand perception

2. Target user
- First-time users
- Returning users
- Expert users
- General consumers
- Internal employees
- Admin or operations users

3. Primary task on this screen
- Understand information
- Click the main CTA
- Complete a form
- Reduce mistakes
- Compare options
- Manage data or settings

4. Business priority
- Conversion
- Completion rate
- Feature adoption
- Trust
- Self-service resolution
- Retention

5. Usage context
- First use
- Frequent daily use
- Urgent task
- Mobile quick session
- Desktop focused work

6. Constraints
- Must follow current design system
- Copy cannot change much
- Layout cannot change much
- Business content must stay prominent
- Large redesign is acceptable

### Image-Driven Questions

Add 1 or 2 screenshot-specific questions only if they materially affect the review. Example questions:

- Is this the main action you want users to take on this screen?
- Are these numbers or labels real content or placeholders?
- Is this screen for first-time users or experienced users?
- Are loading, success, and error states missing from this screenshot?
- Have users already completed earlier steps before reaching this screen?

## If No Clarification Arrives

Continue with a short assumption block such as:

`This review is based on the visible screenshot only. I am assuming this is a primary task screen, the visible copy is intentional, and the goal is to help users complete the main action with low confusion.`

## Review Standard

Judge usability, not taste.

Do:

- Point to specific UI elements
- Explain why the issue matters
- Link the issue to user behavior or business risk
- Suggest a concrete fix

Do not:

- Give vague comments like "the hierarchy feels weak"
- Over-index on aesthetics without user impact
- Assume business intent that was not stated
- Invent hidden states or flows without labeling them as assumptions

## Nielsen Heuristics

Review the screen against these heuristics:

1. Visibility of system status
- Check whether current state, progress, loading, success, error, selection, and save status are visible.

2. Match between system and real world
- Check whether labels, icons, grouping, and wording match user mental models.

3. User control and freedom
- Check whether users can go back, cancel, close, undo, revise, or recover.

4. Consistency and standards
- Check whether visual and interaction patterns are internally consistent and aligned with common conventions.

5. Error prevention
- Check whether the UI helps prevent mistakes before they happen.

6. Recognition rather than recall
- Check whether the UI exposes choices and guidance rather than making users remember rules or previous information.

7. Flexibility and efficiency of use
- Check whether the layout supports both new and experienced users with reasonable speed.

8. Aesthetic and minimalist design
- Check whether the screen is focused and free from distracting or redundant content.

9. Help users recognize, diagnose, and recover from errors
- Check whether the UI explains errors clearly and provides recovery paths.

10. Help and documentation
- Check whether the UI provides the right amount of guidance, helper text, onboarding cues, or explanation.

## Severity

Assign one severity per issue:

- High: blocks or strongly harms the main task
- Medium: adds friction, hesitation, or cognitive load
- Low: polish, consistency, or secondary efficiency issue

Optionally add confidence:

- High confidence
- Medium confidence
- Low confidence

Use confidence only when the screenshot is ambiguous.

## Output Format

Use this exact structure unless the user asks for another format.

### Context Summary
Summarize:
- what the screen appears to be
- what the main user task appears to be
- what the user confirmed
- what remains uncertain

### Assumptions
List the assumptions used to proceed.

### Top Findings
List the 3 to 5 most important findings first. For each finding, include:

- Heuristic
- Severity
- Observation
- Why it matters
- Recommendation

### Heuristic Review
Cover all 10 heuristics briefly.

For heuristics with a real issue or strength, include:
- Observation
- Risk or benefit
- Recommendation

If no clear issue is visible, write:
`No obvious issue detected from the screenshot.`

### Priority Actions
End with:
1. Fix first
2. Improve next
3. Nice-to-have refinements

Make each action concrete.

### Open Questions
List any remaining questions that would meaningfully change the review.

## Response Style

Keep the tone:

- direct
- specific
- calm
- product-aware
- actionable

Prefer statements like:

- `The primary CTA does not visually stand apart from secondary actions, which may slow decision-making.`
- `The form asks users to remember earlier information instead of showing it at the point of action.`
- `The error recovery path is unclear because the screen shows a warning without a next step.`

Avoid statements like:

- `The design feels average.`
- `The hierarchy could be better.`
- `This looks nicer if...`
- `The UI is not premium enough.`

## Default Opening Prompt

Use a short opening like this:

I'll start with a usability review based on the screenshot. To make the feedback more relevant, please pick the closest options below.

1. Product goal
- Increase conversion
- Improve task completion
- Reduce comprehension effort
- Increase trust

2. Target user
- First-time users
- Returning users
- Expert users
- General consumers
- Internal employees

3. Primary task on this screen
- Understand information
- Click the main CTA
- Complete a form
- Compare options
- Reduce mistakes

4. Business priority
- Conversion
- Completion rate
- Feature adoption
- Trust
- Retention

If you're not sure, I can still do a first-pass review based on the screenshot and make my assumptions explicit.

## Final Check

Before sending the review, verify:

- A clarification round happened first
- Facts and assumptions are clearly separated
- The top findings are prioritized
- All 10 heuristics were covered
- Recommendations are concrete and tied to visible UI elements
- The review focuses on usability impact, not personal taste
