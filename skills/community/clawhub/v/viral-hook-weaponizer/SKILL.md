name: Viral Hook Weaponizer
description: Generates high-performing viral hooks for short-form content based on proven psychological patterns.

trigger:
  when:
    - user requests content ideas, captions, hooks, or viral content
    - OR provides a topic and wants engagement
  avoid:
    - long-form writing (blogs, essays)
    - technical explanations

input_schema:
  topic: string
  audience: optional string
  platform: optional string (tiktok, instagram, youtube)

execution:
  - identify emotional drivers (fear, curiosity, status, urgency)
  - select 3 hook archetypes:
      - curiosity gap
      - bold claim
      - relatable pain
  - generate 10 hooks using these archetypes
  - ensure each hook is under 15 words
  - avoid repetition and generic phrasing

output_format:
  HOOKS:
  1.
  2.
  3.
  ...
  10.

constraints:
  - no emojis
  - no explanations
  - hooks must feel native and human
  - each hook must be unique





