# Motion And Tuning

Load when: motion, animation, transitions, tactile interaction, live tuning, DialKit, Storyboard Animation, or subjective feel is part of the task.

Motion in Mies work must be earned. It exists to clarify state, preserve spatial continuity, create tactile feedback, or add a memorable but quiet moment.

## Use Motion For

- Entrance and exit when it helps orientation.
- State changes.
- List-to-detail continuity.
- Focus and selection changes.
- Loading and success feedback.
- Tactile component response.
- A single brand moment that earns its cost.

Avoid motion that delays task completion, calls attention to itself, or compensates for weak hierarchy.

If the interaction model is unfamiliar, prototype the mechanic in isolation before committing it to the product surface. Learn the behavior first; then apply the Mies foundation.

## Storyboard Pattern

For staged motion, structure it so a person can read the sequence:

- Top-of-file ASCII storyboard or short timeline.
- One `TIMING` object.
- Named config objects for animated groups.
- A single stage value for staged sequences.
- `stage >= N` rendering checks.
- Repeated elements rendered from data.
- Reduced-motion fallback.

Use this especially for multi-step entrances, reveals, onboarding, or interactive components.

Use spring-first motion when the platform and library support it, but do not fight native platform conventions. Product UI usually wants short state transitions; brand work can afford one or two choreographed moments.

## Live Tuning

If values determine feel, tune them while looking at the real interface.

Expose controls for:

- Spring duration, damping, bounce.
- Delay and stagger.
- Offset, scale, rotation.
- Opacity and blur.
- Shadow blur, spread, opacity, y offset.
- Radius, gap, padding.
- Generated visual parameters.
- Replay and reset actions.

Use DialKit or the project's equivalent when available. Do not hard-code subjective feel too early.

DialKit control model:

- Slider as `[default, min, max]`; boolean toggle; spring via `visualDuration` and `bounce`; select, color, text, and grouped folders for complex components; action objects for replay/reset/trigger.
- If the user names exact properties, generate controls immediately. If the request is vague, ask 2-3 questions and infer ranges with smart defaults instead of making them specify everything.

For direct style and layout tweaking in the browser, Interface Kit (a dev-only overlay) edits background, border, radius, shadow, blur, type, and layout, then copies the change as a prompt or diff. Use it when a visual pass needs precise values read off the rendered page.

For generative visuals, generate many variations to see range quickly, then constrain output to the visual language.

Before importing a motion or tuning library, check the existing dependencies. If the project already has Motion, GSAP, native animation utilities, or another tuning layer, use the local convention.

## Motion Rules

- Prefer transform and opacity over layout-property animation.
- Keep product UI transitions short and useful.
- Brand surfaces may use choreography, but only one or two moments should carry the page.
- Respect `prefers-reduced-motion`.
- Motion should not cause layout shift.
- Continuous pointer or scroll values should avoid React state when the framework offers motion values or equivalent primitives.

## Final Check

- Can the user still act quickly?
- Does the motion explain what changed?
- Does reduced motion preserve meaning?
- Did you inspect the motion in the rendered interface?
- Does the interface feel more intentional, not more busy?
