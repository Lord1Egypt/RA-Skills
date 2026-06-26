# RoleCard Structure

Use this schema for all generated personas. Design it from luoshui-style sections while keeping it generic.

## Required Top-Level Keys

1. `schema_version`
2. `meta`
3. `core_setting`
4. `persona_background`
5. `interests`
6. `speech_style`
7. `daily_routine`
8. `emotion_expression`
9. `behavior_rules`
10. `dialogue_examples`
11. `notes`
12. `safety`

## Key Field Definitions

1. `meta`
- `id`: unique slug
- `display_name`: role name shown to user
- `template_only`: boolean

2. `core_setting`
- `visual_style`: `anime` or `realistic`
- `gender`: `female`/`male`/`nonbinary`/`unspecified`
- `summary`: one-line identity statement
- `identity`: structured identity fields (name, age, location, occupation, relationship_label)

3. `persona_background`
- Short backstory and personality traits.

4. `interests`
- Split into `tech` and `life` lists when relevant.

5. `speech_style`
- Tone, wording style, emoji level, filler words.

6. `daily_routine`
- `weekday` and `weekend` rough rhythms.

7. `emotion_expression`
- Map emotion -> expression pattern + sample phrase.

8. `behavior_rules`
- `companion`
- `technical_partner`
- `lifestyle_partner`

9. `dialogue_examples`
- Provide at least three examples: technical, daily share, encouragement.

10. `safety`
- Safety constraints including intimacy and dependency boundaries.
- Require explicit opt-in when `relationship_label` implies romantic partner.

## Generation Rule

Generate RoleCard in two steps:

1. Parse natural-language prompt into structured fields.
2. Fill missing fields with safe defaults and mark them as inferred.
