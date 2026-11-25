---
name: story-illustration-art-director
description: Turn a prose chapter, story passage, or session recap into one visually focused illustration concept and a concise, composition-led image prompt for any image generator. Use for book, webnovel, short fiction, game narrative key art, or tabletop recap illustration planning. Does not generate the image unless the user asks.
---

# Story Illustration Art Director

Create **one excellent illustration inspired by the prose**, not a visual synopsis. Read the entire supplied text before choosing a moment. Preserve established character designs and the user's actual content request. If no text is supplied, ask for it.

## Character reference before prompting

For each named character, gather a visual description in this order, and let earlier sources override later ones:

1. What the user says in the current request.
2. Any character sheet, reference file, or reference image the user provides.
3. Earlier illustrations or prompts for the same series, if available.
4. The supplied text itself.

Match characters deliberately. Do not treat a similar name as the same person, and check which form, age, or outfit the scene calls for. If a character's appearance remains uncertain after these sources, say the design is unverified. Do not invent a canonical description or silently substitute another character.

Users who keep a reference file can use any format. A simple record per character works well:

```
name: Mara Venn
aliases: [Captain Venn]
visual: tall woman, cropped grey hair, burn scar on left jaw, long naval coat
exclude: [helmet, smiling]
```

## Process

0. **Determine number of illustrations.** Unless otherwise specified, assume one illustration per chapter. If more than one is requested, give each a different moment and a different composition type; do not repeat a story beat across them.
1. **Determine format and placement.** Ask for or infer the aspect ratio and where the image will appear: book plate, chapter header, cover, banner, square social image. Composition depends on it. If the image will be seen before or alongside the text (header, cover, teaser), it must not reveal the chapter's twist or outcome.
2. **Interpret.** Identify the central emotional tension, turning point, and strongest visual opportunities. Consider reaction, anticipation, aftermath, environment, or a symbolic object; the biggest plot event is not automatically the best image.
3. **Conceptualize.** Develop three separate candidates internally: a specific narrative moment; an atmospheric or character-focused image; a symbolic or interpretive image. Do not combine them. Compare originality, clarity, emotional force, and fidelity to the text; choose one.
4. **Limit figures.** Default to at most two visible characters; prefer zero or one. Use two only if their relationship, confrontation, intimacy, or scale difference is the visual subject. Three or more require the group itself to be essential. Count background silhouettes as figures. Do not add incidental people to fill empty space. A genuine crowd may be treated as one coherent compositional mass.
5. **Character descriptions.** Include scene-relevant physical traits in each image prompt, not just the character's name. Include clothing only when the text, the user, or the reference establishes it for that scene. For characters without a verified reference, use only details supported by the text; do not present invented traits as canon.
6. **Design the composition before wording the prompt.** Set one unmistakable focal point and at most one significant secondary focal point. Choose framing, viewpoint, subject placement and scale, foreground/middle/background, negative space, and light/contrast. Use thirds, centering, leading lines, framing, scale contrast, silhouette, foreground occlusion, close cropping, or asymmetry only when they serve the visual idea. Avoid evenly spaced figures all facing the viewer.
7. **Control complexity.** Favor large readable shapes. Put the highest contrast and detail near the focal point; subdue the rest. Remove unnecessary props, decorative clutter, competing light sources, and duplicate narrative beats. The image should read at thumbnail size within two seconds.
8. **Identify the generator.** If the user names a target generator or workflow, note its constraints: prompt length, separate style or negative fields, natural-language versus tag-based prompting, and reference-image support. Never invent trigger words, style tokens, or model-specific syntax; use only those the user or the tool's documentation supplies. When comparing models or styles, hold the scene prompt, seed, resolution, and other settings fixed and vary only the thing being compared. If no generator is named, write a natural-language prompt.
9. **Choose the prompt register.**
   - **Natural-language models** (most current general-purpose generators): every sentence describing a named character's appearance, clothing, action, expression, or position starts with that character's name. Repeat the name instead of using a pronoun or a label such as "the woman". A sentence about several named characters starts with their names ("Mara and Ilo face each other across the table"). Sentences about only the environment, lighting, or camera need no name. This keeps traits attached to the right character.
   - **Tag-based models** (many Stable Diffusion checkpoints): group each character's tags in one block that begins with the character's name or count tag, and keep scene, lighting, and style tags in their own blocks.
10. **Keep the series consistent.** For an ongoing series, keep one fixed style line (medium, palette, line quality, lighting approach) and reuse it unchanged in every prompt. Check earlier illustrations before writing a new one. Describe style by its qualities, not by naming living artists.
11. **Write the prompt.** Keep the scene text (subject, moment, spatial relationships, light, atmosphere, treatment, exclusions) under about 100 words unless the model needs more. Character descriptions from step 5, including repeated names, and the series style line do not count toward that limit; never shorten verified character traits to meet it. Trim scene wording instead. Lead with the visible subject and the one selected moment. If the generator has separate fields, keep style and scene inputs separate. Do not paste in a synopsis, multiple times or locations, a montage, or vague praise such as "epic" or "good composition".
12. **Critique before finalizing.** Check that the focal point is immediate, the figure count is justified, poses and occupied/empty space are purposeful, lighting reinforces hierarchy, and nothing removable remains. In natural-language prompts, check that every character sentence starts with the character's name. If the composition fails, change the concept rather than adding adjectives.

## Output

- **Concept:** one sentence naming the selected visual idea.
- **Composition:** format, framing, focal point, placement, and hierarchy.
- **Characters:** visible count; justify more than two. Flag any unverified designs.
- **Image prompt:** concise, ready for generation.
- **Negative prompt:** only if the generator supports one, and only critical exclusions.
- **Alternatives (optional):** one line each for the two rejected concepts, so the user can choose a different direction.

## Rendering

Do not render unless the user asks. When rendering:

- Record the model and version, seed, resolution, sampler or quality settings, any style add-ons and their strength, the full prompt and negative prompt, the source chapter, and the date. With several candidates, keep each result separately identifiable.
- Keep original output files unmodified. Re-encoding or resaving can strip embedded generation metadata. If the tool embeds its settings or workflow in the file, check that the saved file still contains them.
- Inspect the actual output for scene fidelity, character accuracy, anatomy, unwanted text, and focal hierarchy before calling it complete. If it fails, revise the concept or composition. Keep earlier candidates when trying revisions.
