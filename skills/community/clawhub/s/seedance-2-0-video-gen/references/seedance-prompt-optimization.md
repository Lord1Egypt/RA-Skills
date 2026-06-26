# Seedance 2.0 Prompt Optimization

Use this reference when the user asks for better prompt quality, stronger control, or more reliable motion planning with `SEEDANCE_2_0`.

This file improves prompt design only. It does not change the runtime API surface of this skill.

## Core principle

A good Seedance prompt is not just "beautiful language". It is a compact production spec:

- what the shot starts with
- what changes over time
- what the camera does
- what visual payoff lands at the end
- what must stay consistent

Prefer controllable, time-aware prompts over poetic but vague prompts.

## Recommended output format

When the user's request is complex, organize the prompt plan in this structure before converting it into the final API `prompt` string:

1. `Mode`
2. `Asset mapping`
3. `Timeline beats`
4. `Final prompt`
5. `Negative constraints`
6. `Generation settings`

## Mode selection

Pick the mode before writing the final prompt.

| Mode | When to use | Input shape in this skill |
|------|-------------|---------------------------|
| Text-only | No reference media; all control comes from language | `prompt` |
| Single-image | One image defines identity/composition; motion is moderate | `image` + `prompt` |
| Multi-image | Multiple images define ordered waypoints or transitions | `images` + `prompt` |
| First/last-frame | The user cares about the opening frame and ending frame most | `first_frame` + `last_frame` + `prompt` |
| Migration alias | The user comes from a provider that uses start image + end image | `image` + `last_image` + `prompt` |

## Asset mapping

Before generating, state what each asset controls.

Examples:

- `image`: identity anchor, composition anchor, palette anchor
- `images[0]`: first visual waypoint
- `images[1]`: transition or midpoint waypoint
- `images[2]`: final reveal or destination
- `first_frame`: opening composition and identity lock
- `last_frame`: ending composition, pose, or scene state

Do not treat every image as "just inspiration". Say exactly what each asset should preserve or influence.

## Timeline beats

Use one major beat per time segment.

### 5 seconds

- `0-2s`: establish shot and first motion
- `2-4s`: primary action or transformation
- `4-5s`: payoff / reveal / clean exit frame

### 10 seconds

- `0-3s`: setup
- `3-7s`: main motion development
- `7-10s`: climax and ending frame

### 15 seconds

- `0-4s`: establish world and subject
- `4-9s`: build action
- `9-13s`: transition or escalation
- `13-15s`: payoff and stable ending frame

If the user asks for a longer video idea, split it into multiple segments conceptually and optimize this single prompt for one segment only.

## Prompt skeletons

### Text-only

```text
9:16 vertical, 5s, cinematic realism.
0-2s: [subject and opening action].
2-4s: [main action and camera move].
4-5s: [reveal / final frame].
Consistent lighting, coherent motion, physically plausible movement, clear final payoff.
```

### Single-image

```text
Animate the subject from the reference image while preserving identity, outfit, composition, and color palette.
9:16 vertical, 5s.
0-2s: subtle opening motion.
2-4s: main movement.
4-5s: clean end pose.
No identity drift, no extra limbs, no sudden scene change.
```

### Multi-image

```text
Use the reference images as ordered waypoints of one coherent shot.
9:16 vertical, 5s.
0-2s: begin from the first image composition.
2-4s: transition naturally through the middle waypoint.
4-5s: land on the final visual state from the last image.
Preserve the same subject, lighting logic, and scene continuity.
```

### First-frame / last-frame

```text
Start from the first frame exactly, transition naturally through one clear action arc, and arrive at the last frame with matching subject identity and scene continuity.
9:16 vertical, 5s.
0-2s: opening state from first frame.
2-4s: transformation or movement bridge.
4-5s: stable arrival at last frame.
No hard cut, no identity drift, no abrupt environment rewrite.
```

## Shot design checklist

Always try to cover these dimensions:

- subject identity
- environment
- shot size
- angle
- camera movement
- lighting quality
- material / texture behavior
- action timing
- final payoff
- continuity constraints

## Negative constraints

Add negative constraints when the user wants clean, controllable output.

Common reusable constraints:

- `no watermark`
- `no logo`
- `no subtitles`
- `no on-screen text`
- `no extra fingers`
- `no extra limbs`
- `no identity drift`
- `no sudden camera jump`
- `no scene change unrelated to the prompt`

Only include constraints that help the user's actual goal.

## Scenario recipes

### Product ad

- Preserve product shape and brand-safe geometry.
- Use a clean studio or premium contextual background.
- Make one hero move the center of the prompt: spin, push-in, reveal, exploded view, or reassembly.
- End on a frame that could serve as a cover image.

### Character short

- Lock identity early.
- Keep one clear action arc only.
- Avoid overloading the prompt with multiple costume, location, and motion changes.
- If using first/last frames, make the bridge action simple and believable.

### Before/after transformation

- Best with `first_frame` + `last_frame` or ordered `images`.
- Explicitly state what remains the same and what changes.
- Write the transformation as a continuous process, not a hard cut.

### Storyboard clip

- Treat each image as a waypoint, not a separate scene.
- Maintain one camera logic across all images.
- Keep the transition language continuous: pan, dolly, arc, push, rise, turn.

## Anti-patterns

Avoid these:

- vague beauty words with no visual instructions
- too many simultaneous actions in one 5-second clip
- switching subject, location, and camera style all at once
- saying "make it cinematic" without specifying what that means
- describing every millisecond instead of a few controllable beats

## Practical conversion rule

When the user gives a rough brief, convert it like this:

`rough idea -> mode -> asset mapping -> 2 to 4 timeline beats -> final prompt -> optional negative constraints`

If the prompt becomes too long, remove decorative adjectives first. Keep:

- subject
- action
- camera
- lighting
- payoff
- continuity constraints
