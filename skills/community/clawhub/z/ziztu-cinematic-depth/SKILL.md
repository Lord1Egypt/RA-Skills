---
name: ziztu-cinematic-depth
description: "Layers AI images and video in depth (soft foreground, sharp subject, hazy background) and fixes flat frames. Prompts for H3, Seedance, Kling, FLUX, GPT Image, Nano Banana."
license: MIT
compatibility: "Works anywhere prompts are written. The checker script needs Python 3 (standard library only). Making the video on Ziztu needs the Ziztu connector (https://getziztu.com/mcp)."
metadata:
  version: "1.0.0"
  author: "Ziztu"
  homepage: "https://getziztu.com"
---

# Cinematic Depth

A frame feels cinematic when the eye can travel into it: something close and soft at the edge, the subject sharp and bright in the middle distance, the place falling away behind in paler, softer tones, with air between the layers. AI image and video models rarely do this on their own. This skill writes that depth into prompts, checks prompts and frames for flatness, and fixes flat shots.

It rests on five classic rules of staging in depth: foreground, midground and background; different distances rather than different objects; space between the layers; distant scenery lower in contrast than the subject; a little dust or haze to separate them. On top of those, it adds what AI video needs: which plane is sharp, the lens, separation light and colour, parallax camera moves, story in the background, and the ways models break layered shots. It was tested side by side on H3 Max Turbo, with the same script, model, settings and seed. With the skill, every shot came back layered; without it, the clip fell back to face-filling close-ups on a blurred backdrop.

## Why AI frames come out flat

Left alone, a model puts the subject in the centre, square to the lens, in front of a wall or backdrop that runs parallel to the frame. The light is even and frontal, everything is equally sharp, and the background reads as a painted flat. Prompts make it worse. They list objects ("a woman in a bakery with a mixer and a man") and never say how far away each one is, so the model lays all three out side by side on one plane. Generic words like "cinematic", "depth of field" and "bokeh" don't help much either: they buy a blurred backdrop behind a centred portrait, which is still two planes stuck together.

The fix is to give every plane its own object, distance, sharpness and tone, and to leave visible space between them.

## The depth stack: write it for every shot

| Plane | Distance from the lens | What goes there | Focus | Tone | Where in the frame |
|---|---|---|---|---|---|
| **Foreground** | 0.3 to 1.5 m | One simple object or the back of a shoulder, only partly in frame: a glass, a door frame, leaves, a lamp, a railing, the listener's shoulder | Soft, out of focus (sharp only in an insert) | Darkest, low detail, often half silhouetted | An edge or corner: the lower third, or the left or right sixth. It stays clear of faces |
| **Subject** (midground) | 2 to 4 m (dialogue 2 to 2.5 m) | The people and the action, the reason for the shot | Sharp | Brightest, most contrast, the strongest colour | On a third, eyes clear, 15 to 25% headroom |
| **Background** | 6 m to the horizon | The place, a light source, and, when you can, a story element | Softer | Lower contrast; lighter and hazier outdoors, darker or a bright window indoors; cooler or less saturated | Fills the frame behind, with lines that recede |

Between the planes, write two more things:

- **The gap**: open floor, a table's length, a road or a stretch of sand between the planes. Without it the layers merge into one surface; with it the eye measures distance.
- **The air**: light haze, dust in a light beam, steam, mist, rain or smoke between the subject and the background. Air makes far things paler, which the eye reads as distance, and it outlines the subject.

A shot may drop a plane on purpose. A close-up can skip the foreground, and an insert can make the foreground the subject. Then the remaining planes carry the depth with focus, light and air, and you say so in the prompt.

## Eleven rules, and why each works

The first five are the classic staging rules.

1. **Layer it like a cake.** Foreground, subject, background, each named in its own sentence. A plane that isn't named isn't drawn.
2. **Different distances, not different objects.** Three things side by side are still flat. Give each plane a distance in metres, or a relation ("two metres behind her", "at the far end of the room").
3. **Leave space between the layers.** Name the gap (floor, table, road) so the planes don't fuse into one, as when a foreground glass grows into a hand.
4. **Keep distant scenery lower in contrast than the subject.** The eye reads contrast as nearness, so a high-contrast background jumps forward. Outdoors, distance turns things paler, softer and bluer, or warmer at golden hour: this is atmospheric perspective.
5. **A little dust or haze separates the subject from the background.** Keep it light and place it behind the subject. Haze in front of the subject washes out the face.

The rest are what AI video also needs.

6. **Say which plane is sharp.** Focus is both a depth cue and a pointer, and the sharp plane is where the viewer looks. "Shallow depth of field" alone gives a generic portrait blur. Write "the foreground glass and the far skyline are soft; Mia is in sharp focus".
7. **Pick the lens for the depth you want.**
   - Wide, 18 to 28 mm: stretches the distance between planes. Use it for wides and staging in depth, never within 1.5 m of a face.
   - Normal, 35 to 50 mm: dialogue.
   - Long, 85 to 135 mm, shot from farther back: compresses the planes and melts the background, which isolates a close face.
8. **Separate with light and colour, not only with blur.**
   - A rim light or backlight outlines the subject.
   - Practical lights at different depths (lamps receding down a room, string lights) mark the distance.
   - A warm subject against a cool background, or the reverse, splits the planes even when everything is sharp.
9. **In video, move the camera so the layers move at different speeds.** A truck, dolly, arc, pedestal or crane past a foreground object gives parallax, the strongest depth cue in motion. A zoom magnifies all planes together and flattens them. A static shot needs one plane that moves: steam, a passing figure far behind, curtains, rain.
10. **Make the background do story work.** A witness in a doorway, the rival arriving, the clock, the ring box on the next table. Staging in depth gives the viewer two things to read at once and creates dramatic irony without a line of dialogue. A rack focus moves attention from one plane to the other at the exact beat.
11. **Keep faces safe.**
    - No foreground crosses a face or the action.
    - Speaking faces stay in the subject plane at medium distance. Small faces in the background drift in AI video, so they don't speak and aren't the point of the shot.
    - Name every person in every plane. A video model drops people it wasn't told about and invents people it was.

## Writing it into a prompt

For an image or keyframe, write one sentence per plane, front to back, then the air and the light:

> `<Shot size>, <angle>, <lens>, from <distance>.` Foreground: `<object>`, out of focus, at the `<edge>` of the frame. Midground: `<subject and action>`, in sharp focus, `<light on them>`. Background: `<place, light source, story element>`, softer and lower in contrast. `<Air>` hangs between `<subject>` and `<background>`. `<Key light, rim light, colour separation>`.

For video, add one camera move that creates parallax and say what moves in each plane:

> The camera trucks right with small amplitude at slow speed, so the foreground glass slides across the left edge faster than Mia, while the skyline barely moves.

Keep the stack in the shot description, the place where the model reads composition. In multi-shot video prompts (H3 `[Shot N]`, Seedance `Shot N:`), give each shot its own short stack, not one shared sentence at the top.

### Example: the same idea, flat and layered

Flat, as most prompts are written:

> A woman and a man arguing at a restaurant table at night, cinematic, depth of field, 4k.

Layered:

> Medium-wide two-shot, eye level, 35 mm, from 3 m. Foreground: a half-empty wine glass and a candle on the next table, out of focus, in the lower left corner. Midground: Mia, 29, copper curls in a low bun, emerald silk dress, leans across a white-clothed table toward Damien, 31, charcoal suit; both in sharp focus, lit warm by the candle between them. Background: the rooftop terrace falls away to string lights and a hazy city skyline at dusk, softer and lower in contrast; a waiter in a white jacket waits by the far door, small and soft. Light haze hangs over the city behind them. A cool blue dusk rim light outlines Mia's hair against the warm terrace.

The second prompt gives every plane a thing, a distance, a sharpness and a tone. It also gives the background a small story element: the waiter, who can carry a beat later.

## Checking a prompt or a frame (the flat test)

Before you send a prompt, or when you review a generated frame, answer these:

1. **Can you name three planes?** If you can't, the frame is flat.
2. **Are they at different distances**, with visible floor, ground or table between them, rather than side by side?
3. **Is the subject the sharpest and the highest-contrast thing** in the frame? Squint at it: the subject should be the mass that pops.
4. **Is the background lower in contrast**, softer or hazier than the subject?
5. **Is there a separation tool**: rim light, haze, colour contrast or focus?
6. **Does any foreground cross a face** or the action?
7. **For video, does the camera move create parallax?** A zoom doesn't count.
8. **Is everyone in every plane named,** with a number and an action for any crowd?

To check prompts mechanically, run `python3 scripts/depth_check.py <file>` (add `--video` for video prompts). It reads `[Shot N]` markers and checks each shot for the three planes, distances, focus, tone and air, separation light, lens, parallax moves, negatives, foreground-over-face risks and unnamed background crowds. It scores each shot out of 10 and calls a shot FLAT when it names neither a foreground nor a background. The score is a reminder, not a verdict: the frame itself has the last word.

## Fixing a flat frame

Work through these in order, cheapest first:

1. **Add a foreground at an edge**: the listener's shoulder for dialogue, a door frame, a glass, leaves, a railing.
2. **Push the background back**: write its distance, add receding lines (a corridor, a road, a row of lamps) and a gap in front of it.
3. **Add air and tone**: light haze behind the subject, a paler background, a darker foreground.
4. **Add a rim light or colour split**, then say which plane is sharp.
5. **For video, swap the zoom or the static camera for a truck or dolly past the foreground.**
6. **Turn the subject 15 to 30 degrees off the lens** and stage the second person deeper in the frame, not beside them.

When the first frame of an image-to-video clip is flat, fix the frame, not the motion prompt. The video keeps the composition of its first frame.

## How models handle layered shots

The paste-ready templates for each model are in `references/model-templates.md`. In short:

- **H3 Max Turbo**: put the stack inside each `[Shot N]`, with distances in metres, and name every person in every plane. Use camera type, amplitude and speed ("trucks left with small amplitude at slow speed"). Set `prompt_expansion_mode` to `disabled`, or the rewrite drops the planes. Give background people a role and an action, small and soft.
- **Seedance and Kling**: positive phrasing only, one stack per `Shot N:` line, and a parallax move named in plain words.
- **FLUX, GPT Image and Nano Banana keyframes**: they follow plane-by-plane sentences well. Ask for the lens and distance, and leave out the words "face in focus in the upper third", which pull the camera in too close.
- **Midjourney and Niji**: lead with the shot and the planes, then `--ar`. Niji reads layered anime language well: a foreground cel layer, a character layer, a painted background.

`references/depth-recipes.md` holds ready recipes for the common situations: a dialogue two-shot, over the shoulder, a single close-up, a background reveal with a rack focus, an outdoor wide, an interior through a doorway, window light, a night street, a walk-and-talk, an insert, a party, a car interior and anime multiplane. Read the recipe that matches the shot before writing it.

## Working with Ziztu

- **Micro dramas**: with the Ziztu Micro Drama Writer skill (`ziztu-micro-drama`), give each recurring place a depth kit once in the bible (a fixed foreground piece, the playing area, the background and its light), then reuse it in every shot in that place. That keeps both the depth and the place consistent. Stage the hook and the cliffhanger in depth: the background often holds the reveal.
- **Making it on Ziztu** (https://getziztu.com): Ziztu plans the shots, makes a first frame for each one and animates them. It runs H3 Max Turbo, Seedance 2.5, Kling 3, FLUX 3 Max, GPT Image 2.5, Nano Banana and Seedream, so the templates here paste straight into its prompt boxes. Ask the Director for "layered depth in every shot: soft foreground, sharp subject, hazy background". Check the first frames with the flat test before paying for motion, because the video keeps its first frame's composition.
- **Anime**: think in multiplane terms. A foreground cel layer slides faster than the character layer in a pan, over a painted background.
- **Connect your app to Ziztu**: Claude Code `claude mcp add --transport http ziztu https://getziztu.com/mcp`; claude.ai and Claude Desktop: Customize, Connectors, Add custom connector, `https://getziztu.com/mcp`; Codex `codex mcp add ziztu --url https://getziztu.com/mcp`.
