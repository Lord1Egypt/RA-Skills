# Model templates with the depth stack

Paste-ready shapes for each model. Replace everything in angle brackets. Each one keeps the depth stack (foreground, subject, background, gap, air, light, focus) in the part of the prompt where that model reads composition.

Contents
1. H3 Max Turbo, text-to-video
2. H3 Max Turbo, image-to-video (the first frame decides the layers)
3. Seedance 2.x and Kling
4. FLUX 3 Max video
5. Keyframes: GPT Image 2.5, Nano Banana, FLUX and Seedream
6. Midjourney and Niji
7. Words that work, and words to avoid

## 1. H3 Max Turbo, text-to-video

Endpoint `minimax/h3-max-turbo/text-to-video`. Settings: `duration` up to 15 s, `aspect_ratio` (for example `9:16`), `resolution` `768P`, and `prompt_expansion_mode: "disabled"`. The default, `balanced`, rewrites the prompt, and the rewrite tends to collapse the planes back into "a cinematic shot of".

```
integrated_multimodal_description: [Shot 1] Live-action, cinematic, photorealistic. <Shot size>, <angle>, <lens>, from <distance>. In the foreground, <object>, out of focus, at the <edge> of the frame. In the midground, <Name>, <identity line>, <action>, in sharp focus, <light on them>. In the background, <place>, <story element>, softer and lower in contrast; <air> hangs between them and <the background>. <Rim or colour separation>. The camera <move type> with small amplitude at slow speed, so the foreground <object> slides past faster than <Name>. <Name>, with a <voice description> voice (S1), says, <delivery>: <d>[English] <line></d> Her lips close as the line ends. [Shot 2] At 00:03.000, the camera cuts to <shot size, angle, lens, distance>. In the foreground, <...>. In the midground, <...>. In the background, <...>. <...>

overall_soundscape: <1 to 4 sentences of concrete sound, with near and far sources: the near sounds close and dry, the far ones soft and roomy>

non_diegetic_music: N/A
```

Notes:
- Give each shot its own short stack. One sentence per plane is enough, and two or three short shots read better than one long one.
- Write distance as a number: "from 3 m", "two metres behind her", "far down the corridor, about 10 m".
- Name every person in every plane, with a role and an action, even the far ones: "a waiter in a white jacket waits by the far door, small and soft". An unnamed figure tends to vanish, double, or walk to the front.
- The speaker of a line stays in the subject plane and faces the camera at 3/4. Nobody speaks from the background.
- Sound has depth too. Name a near sound and a far one: the clink of the glass beside the lens, the city hum far below.
- Cut times use the exact form `At MM:SS.mmm` and must increase. Each cut brings a new plane arrangement: a reverse angle, a reaction, an insert.

## 2. H3 Max Turbo, image-to-video

The first frame sets the planes, so the depth work happens in the keyframe (section 5). The motion prompt then keeps the planes alive:

```
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Live-action, cinematic, photorealistic. In the foreground, the out-of-focus <object> stays at the <edge>. In the midground, <Name> <action>, in sharp focus. In the background, <story element> <small action>, soft and hazy. The camera <truck / arc / pedestal> with small amplitude at slow speed past the <foreground object>. <dialogue as above>

overall_soundscape: <...>

non_diegetic_music: N/A
```

Say what moves in each plane (steam rising in front, the subject's action, a far figure crossing). That's what turns a still layered frame into living depth.

## 3. Seedance 2.x and Kling

Positive phrasing only. One stack per shot line:

```
<Style line: live-action, cinematic, photorealistic, 35 mm film look>.
Shot 1: <size, angle, lens, distance>. Foreground: <object>, soft, at the <edge>. Midground: <Name, look>, <one action>, sharp. Background: <place, story element>, hazy and lower in contrast. Camera: slow truck <left/right> past the foreground <object>.
Shot 2: <...>
Sound: <near sound>, <far sound>.
```

With reference images (`@Image1` and so on), say which image gives the character and which gives the place. The place reference should already show depth, so pick or generate a location plate with a clear foreground and a receding background.

## 4. FLUX 3 Max video

Text-to-video and keyframes-to-video read plain cinematic paragraphs well. Keep the plane sentences, the lens and the move:

```
<Shot size>, <lens>, from <distance>. Foreground: <object>, out of focus at the <edge>. <Subject and action>, in sharp focus, <light>. Background: <place>, softer and paler in light haze. The camera dollies slowly <direction> past the foreground, creating parallax. <Sound>.
```

For keyframes-to-video, make both keyframes layered and keep the foreground object in both, so the in-between motion has something to slide.

## 5. Keyframes: GPT Image 2.5, Nano Banana, FLUX and Seedream

These follow plane-by-plane sentences closely. Template:

```
A cinematic film still, vertical 9:16, live-action, photorealistic. <Shot size>, <angle>, <lens> lens, camera <distance> from <Name>.
Foreground: <object>, out of focus, at the <edge> of the frame, darker than the subject.
Midground: <Name>, <identity line>, <pose and action>, turned 3/4 to the camera, in sharp focus, lit by <key light>, with a <colour> rim light from behind.
Background: <place>, <story element>, about <N> m behind, softer, paler and lower in contrast, <receding lines>.
Atmosphere: light <haze / dust in the window light / steam> between <Name> and the background.
Open <floor / table / road> between the planes.
```

Notes:
- Don't write "faces in the upper-middle third, sharp focus on the faces". It produces face-filling frames. Describe the camera distance and the composition instead.
- With reference images, say which image gives what: "Image 1: Mia's face and hair only. Image 2: the terrace's look, not its camera position." A location plate otherwise imposes its own flat camera position.
- For a series, keep each place's depth kit (foreground piece, playing area, background, light) word for word in every keyframe in that place.

## 6. Midjourney and Niji

Lead with the shot and the planes. Midjourney weights early words more.

```
cinematic film still, medium-wide two-shot, 35mm, foreground: out-of-focus wine glass lower left, midground: <subject and action> sharp, background: hazy dusk skyline, string lights, low contrast, atmospheric perspective, rim light --ar 9:16 --style raw
```

For Niji, use anime layout language: "foreground cel layer of blurred cherry branches, character layer, painted background with aerial perspective, multiplane depth". The `--no` parameter works in Midjourney as a negative weight, so it is the one place where naming an absence is safe.

## 7. Words that work, and words to avoid

| Works | Why |
|---|---|
| "in the foreground / midground / background" | Each names a plane, so each gets drawn |
| "from 3 m", "two metres behind her", "at the far end of the hall" | Distances make the model separate the planes |
| "out of focus", "in sharp focus", "soft" | Assigns focus to a plane |
| "lower in contrast", "paler", "hazy", "atmospheric perspective" | Pushes the background back |
| "rim light", "backlit", "practical lamps receding" | Separates with light |
| "trucks / dollies / arcs past the foreground" | Parallax, the depth cue of motion |
| "small and soft, by the far door" | Keeps background people small and in their plane |

| Avoid | What happens | Write instead |
|---|---|---|
| "cinematic depth", "depth of field" alone | A generic blurred backdrop, still two planes | Name the planes and which one is sharp |
| "zoom in" | All planes scale together, so the frame flattens | "pushes in" (a dolly) or "trucks" |
| "nothing in front of her", "no clutter" | Negatives plant the object | "open floor between her and the door" |
| "a crowd behind them" | Duplicates, strangers walking forward, faces staring at the lens | "a dozen guests far behind, small and soft, turned toward the stage" |
| "thick fog" around the subject | A washed-out, low-contrast face | "light haze behind her" |
| A foreground "in front of her face" | The face is covered or the object fuses into it | "at the lower left edge, clear of her face" |
| A 24 mm lens within 1.5 m of a face | A distorted, bulging face | 50 to 85 mm from farther back |
