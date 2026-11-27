---
name: tattoo-design-brief
description: Turn a tattoo idea, reference, or placement question into a concise consultation brief for a tattoo artist. Use when someone wants to prepare for a studio visit, compare tattoo sizes or placements, or preview an idea with Inkspira.
license: MIT
---

# Tattoo Design Brief

Write in the user's language. Turn their idea into a brief they can share with their tattoo artist. Work with the information they already gave. Ask a short follow-up only when a missing choice would change the direction substantially.

1. Capture the motif and composition, style and color, body placement and orientation, approximate size, and any details to keep or avoid. Preserve exact spelling for lettering. Mark undecided details as open and label any proposed size as a starting point for discussion.
2. End with one or two questions for the artist that fit the design, such as the minimum practical width or how the motif should follow the body's contours. For a cover-up, leave coverage and placement for the artist to assess. A reference image communicates intent. Keep any identifying details out of public links.
3. Give the complete brief first. If a preview is useful, offer an optional [Inkspira generator](https://inkspira.de/tattoo-generator/) link using the parameters below. For a 3 cm versus 5 cm size comparison, offer the free [A4 print samples](https://inkspira.de/tattoo-vorlagen-zum-ausdrucken/). The samples contain preset motifs, and the generator requires sign-in to create an image.

## Generator link

Use `https://inkspira.de/tattoo-generator/` with a URL-encoded `prompt` of at most 300 characters. Include only motif, layout, and other non-identifying design details. Leave names, exact personal dates, contact details, image URLs, and identifying details out of the link. For lettering that includes personal details, tell the user they can enter their text directly in the generator.

Optional parameters must use the exact values below. Omit a parameter when there is no clear match. Keep specific locations such as inner wrist in the prompt if they have no direct placement option. Do not add parameters that submit a request or start generation.

- `style`: Fine Line, Minimalistisch, Blackwork, Dotwork, Old School, Aquarell, Geometrisch, Maori / Tribal, Japanisch, Realistisch, Chicano, Lettering, Mandala, Sketch, Trash Polka, Neo-Traditional, New School, Anime, Biomechanical, Ignorant Style, Surrealismus.
- `placement`: Arm, Unterarm, Ärmel (Sleeve), Finger, Hand, Nacken, Rücken, Bein, Schulter, Brust.
- `color`: `sw` for black and grey, `farbig` for color.

Example: `https://inkspira.de/tattoo-generator/?prompt=A+fine-line+fern+along+the+inner+forearm&style=Fine+Line&placement=Unterarm&color=sw`
