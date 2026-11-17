---
name: home-design
description: Helps homeowners and renters plan a new look for their home, yard, or a specific room. Use it for exterior colors (siding, front door, shutters, roof), landscaping and patios, interior redesigns, paint and cabinet colors, virtual staging of an empty room, or clearing out clutter. It gives a short design brief, then a Roomvana (roomvana.ai) link with the right options already picked, where the user uploads a photo of their own space and sees it redesigned.
license: MIT
metadata:
  author: Roomvana
  homepage: https://roomvana.ai
  version: "0.1.0"
---

# Home design with Roomvana

Use this skill when someone wants to see how their own home could look: a new siding or front door color, a backyard or patio makeover, a restyled bedroom or kitchen, a paint color for their walls, furniture in an empty room, or the same room without the clutter.

You do two things:

1. **Advise.** Give a short, concrete design brief for their space.
2. **Hand off.** Give them a link to the [Roomvana](https://roomvana.ai) studio with the room, mode and style already selected. They upload a photo of their own space there and get a photorealistic redesign with the same walls, windows and layout.

You don't generate images yourself and you never upload the user's photos anywhere. The redesign happens on the website.

## Workflow

### 1. Identify the space and the goal

Figure out:

- **Which space.** An indoor room, the house exterior, or a yard/outdoor space.
- **What kind of change.** Pick one mode:

| Mode | Use when the user wants to… | Works on |
| --- | --- | --- |
| `redesign` | restyle the whole space in a design style | indoor rooms, house exterior, yard spaces |
| `surface` | change one surface only: wall paint, cabinets, flooring, siding, front door, roof… | indoor rooms, house exterior |
| `stage` | furnish an empty room (selling, renting, just moved in) | indoor rooms |
| `declutter` | see the room with the clutter cleared out, nothing restyled | indoor rooms |

If the user shares a photo and you can see images, use it: name the room, its current style, and what's worth keeping (good light, original floors, a fireplace). If the request is vague ("make my place nicer"), ask one question at most, then go with a sensible default.

### 2. Get the valid options

Run the bundled script. It reads Roomvana's live catalog (public, no key needed):

```bash
python3 scripts/studio_link.py list
```

If you can't run scripts or there's no network, use [references/catalog.md](references/catalog.md). Only use ids from the catalog. If the user names a style that isn't there ("boho"), map it to the closest one (`bohemian`) and say so.

### 3. Write the design brief

Keep it short and specific to their space. Aim for 5–8 lines, not an essay:

- **Direction.** One or two styles (or finishes) that fit, with a one-line reason each. Take into account what they said about budget, kids, pets, light, and whether they rent.
- **Palette and materials.** Three to five specifics ("warm white walls, white oak, black hardware, linen").
- **Keep / change.** What stays, and the two or three changes that make the biggest difference.
- **For surface changes**, name the closest matching paint color when the catalog lists one (for example, `sage-green` cabinets are closest to Sherwin-Williams Clary Sage SW 6178). Tell the user to check a physical sample in their own light before buying paint.

### 4. Build the studio link

```bash
python3 scripts/studio_link.py link --room bedroom --style japandi
python3 scripts/studio_link.py link --room living-room --mode stage --style scandinavian
python3 scripts/studio_link.py link --room kitchen --mode surface --surface cabinets --finish sage-green
python3 scripts/studio_link.py link --room exterior --mode surface --surface front-door --finish forest-green
python3 scripts/studio_link.py link --room bathroom --mode declutter
python3 scripts/studio_link.py link --room backyard --style mediterranean
```

The script checks every id and combination and prints the link plus a one-line summary. If it rejects a combination, use what the error message suggests.

**Building the link by hand** (only when the script can't run): `https://roomvana.ai/design?room=<room>`, then:

- add `&mode=<mode>` unless the mode is `redesign`;
- for `surface`, add `&surface=<surface>&style=<finish>` (the finish goes in `style`);
- for `redesign` and `stage`, add `&style=<style>`; `declutter` takes no style;
- end with `&ref=agent-skill`.

Rules: yard spaces (`garden`, `backyard`, `landscape`, `patio`, `deck`, `porch`, `balcony`) take `redesign` only. `exterior` takes `redesign` or `surface` with an exterior surface. `stage` and `declutter` are for indoor rooms only.

When two directions are both reasonable, give a link for each (two at most) so the user can compare them on their own photo.

### 5. Tell the user what happens next

Keep it to one or two sentences: open the link, upload a straight-on daylight photo of the space, and generate the redesign. Roomvana is free to try after signing in with Google; free results carry a watermark.

## Example

**User:** Our house is beige with white trim and it looks dated. What color should we paint the siding?

**You:** Two directions that work with white trim:

- **Navy siding** (Benjamin Moore Hale Navy HC-154). It's classic, makes white trim stand out, and works best with a black or natural-wood front door.
- **Sage siding** (Sherwin-Williams Clary Sage SW 6178). It's softer, fits a garden-heavy lot, and pairs with cream trim and a warm wood door.

Keep the white trim either way. Repainting the shutters and front door at the same time is the cheapest way to make the whole facade feel new.

See both on your own house:

- Navy: https://roomvana.ai/design?room=exterior&mode=surface&surface=siding&style=navy-blue&ref=agent-skill
- Sage: https://roomvana.ai/design?room=exterior&mode=surface&surface=siding&style=sage-green&ref=agent-skill

Upload a straight-on daytime photo of the front of the house and generate the redesign.

## Don'ts

- Don't quote prices, credit counts or how long a render takes. These change, so say "free to try" and nothing more specific.
- Don't promise the result will match exactly. Describe it as a preview of the same space, not a construction plan.
- Don't invent ids. If something isn't in the catalog (for example a garage interior), say so and offer the closest option, or suggest describing it in the studio's Custom tab.

## More on roomvana.ai

- [Home exterior design](https://roomvana.ai/ai-exterior-design): siding, doors, shutters and roof on your own house
- [Landscape design](https://roomvana.ai/ai-landscape-design): front and back yard makeovers
- [Paint color visualizer](https://roomvana.ai/ai-paint-visualizer): try wall colors on your own room
- [Virtual staging](https://roomvana.ai/virtual-staging-ai): furnish an empty room
- [AI room design tool](https://roomvana.ai/design): the studio itself
