# Story Illustration Art Director

An agent skill that reads a chapter or story passage and returns one illustration concept with a composition plan and a ready-to-use image prompt. It works with any image generator.

It picks one strong image instead of summarizing the chapter. Internally it compares three candidate concepts (a story moment, an atmospheric image, a symbolic image), limits the number of figures, plans the composition before writing the prompt, and critiques the result before returning it.

## Install

Copy the `story-illustration-art-director` folder into your agent's skills directory, or install it from ClawHub.

## Use

Give it the text and, optionally, the target generator, format, and character references.

> Here's chapter 12. I need a portrait chapter-header illustration for Flux. Character sheet attached.

## Example output

- **Concept:** Mara alone at the rail after the ship has left her brother behind.
- **Composition:** 2:3 portrait. Mara small in the lower right third, the empty harbor filling the upper left. Cold dawn backlight gives a strong silhouette.
- **Characters:** 1.
- **Image prompt:** Mara Venn stands at the stern rail of a wooden warship at dawn, seen from behind and slightly above. Mara Venn is a tall woman with cropped grey hair and a long naval coat. Mara Venn grips the rail with both hands. The harbor behind the ship is empty and fading into mist. Pale cold backlight, muted blue-grey palette, painterly book illustration with soft edges.
- **Alternatives:** the brother's abandoned coat on the dock; a close-up of the captain's log with one line struck out.

## Character references

Character sheets can be in any format. One simple record per character works:

```
name: Mara Venn
aliases: [Captain Venn]
visual: tall woman, cropped grey hair, burn scar on left jaw, long naval coat
exclude: [helmet, smiling]
```

If a character has no reference, the skill uses only what the text supports and marks the design as unverified.
