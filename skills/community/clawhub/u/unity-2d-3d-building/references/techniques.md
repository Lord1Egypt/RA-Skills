# Techniques

This is the art log for Battle TV Unity. The skill file points here. Append under **Confirmed** when a watched build proves a method. Numbers below are the look as shipped. If `Assets/Fight/DuelView.cs` or `Assets/Fight/SideDuel.cs` differs, the file is current. Log the change. Do not keep a second secret copy of every float.

Public home: https://chatagent.ca/
Live game: https://chatagent.ca/games/lattice-arena/
Worked picture: https://deepseekoracle.github.io/battle-tv-unity/
Repo: https://github.com/DeepSeekOracle/battle-tv-unity

## The picture

Painted broadcast fighters on a side-view lane. High-resolution cutouts, feet on the sand, facing right. Effects are glowing plates and shaders in the same painted world. They are not stickers, not ovals drawn in code, and not a pixel-sheet language.

Quality bar: the Line Bulwark ground ring (commit `04dfff5`). If a new effect looks flatter or cheaper than that ring, it is not done.

## Characters

- Build one fighter at a time. Finish the move you are on before you start the next body.
- The body is a painted cutout facing right. Feet sit on the sand line. The idle pivot is at the feet. A punch pivot shifts so the fist is the leading edge of the sprite.
- The personal kite stays on the forearm. Do not strip it, hide it, or swap the body to a toss frame to make a planted wall. The wall is a second sprite.
- Frames are already individual PNGs. Do not run them through a sprite-sheet extractor.
- Before you place a hit or a prop, measure the opaque pixels. Fill empty alpha with a flat color and look. A vision model will describe a torn texture as a complete object. The pixels decide.
- Unity's sprite origin is the bottom-left of the texture. The sprite rect must cover the whole texture. `SpriteMeshType.FullRect` is `0`. `Tight` is `1`. A torn picture with mesh type `0` is a bad rect or a torn source file. It is not a tight mesh. Setting the mesh type and leaving a cropped `spriteSheet` rect still draws the fragment.
- When you crop a prop out of a character frame, search the prop's own region. Vale's armor is the same cyan as her kite, so a full-frame cyan search grabs her body. The toss kite lived on the right of `vale-toss/f07.png` (`x > 340`).

## Stage template

Screen-space overlay canvas. The stage is one plate image that covers the view. No black letterbox around the plate.

Fighters, ground rings, sparks, and planted props are children of the plate. Sibling order is the only sort:

1. ring back
2. bodies
3. planted prop
4. ring front
5. spark

A prop parented to the canvas, using coordinates that were computed for the plate, lands in the wrong place.

The HUD stays on the canvas above the plate. Name board stays. No nameplates, house names, side sponsor plates, or a sky-blue lift cable. No `shadowBlur` on the page chrome.

Video Player is the intro film and the resting loop. Fight frames are sprites.

## Overlays and shaders

Additive UI shader: `Blend SrcAlpha One`, unpremultiplied RGB, target `3.0`. Do not call `pow()` in a shader that runs on this WebGL build. `pow` can return NaN. Use `x * x`.

A shader is stripped from the player unless a material asset references it. Ship the `.mat` with the `.shader`. `Shader.Find` on an unreferenced shader will not save it.

Ground ring, the quality bar:

- Two Images on the plate (back and front), not one disc in front of the feet.
- A flat ellipse in the shader. Spin the ring inside the shader. Do not rotate the RectTransform. Rotating the rect makes the ellipse tumble.
- Centre the ring on the feet.
- Shader name `BattleTv/GroundRing`. Materials `GroundRingBack` and `GroundRingFront`. Soft white plate `glow-white.png`.

Hit flash:

- Small, on the defender's near chest, short life. Not a full-body disc.
- Additive, same shader rules as the ring.
- As shipped, the spark sits about `0.28 * SpanX` from the defender's centre toward the attacker, and about `0.60 * SpanY` up from the feet. `SpanX` and `SpanY` are `sizeDelta * localScale`. `rect.width` is wrong before layout and will pull the lunge by zero.

Floaters:

- Damage, crit (with `!`), block, ward, DOWN, and one FINISH. Live floater colors. A runtime pool, not a baked texture.
- Ward and block are the floater words. They do not replace the move name on the fighter. Writing them into the callout snaps the body to the wrong clip.

## Contact

Sim X is the fight. The view may pull the attacker on the contact frame so the fist meets the chest. That pull is a picture. It does not change `Hit()`.

- Keep the torsos apart. A negative bury (shipped `-18`) lets the fist enter the chest.
- Lunge only on the contact frame of Punch or Shield Bash, and only while the spark is on the defender. Do not lunge every swing.
- Hold the extended punch frame while the spark is up. As shipped, punch and bash wait until the clip time passes about `0.58` of the clip, then the view forces that frame.
- Start the punch or bash clip when the attack cooldown rises and the callout is Punch or Shield Bash. A skill can leave the swing flag high and skip the clip, which shows a spark on a body that is still idle.
- Short hit-stop while the spark is on: about `0.05` for a hit or crit, `0.12` for DOWN, `0.04` for ward or block. During hit-stop the clip does not advance and the sim does not step.

## Planted wall

Confirmed in `37429c6` and watched on the published page.

- Crop the whole kite from a frame that already shows it. The old door file was a torn slice (`188×262` with a sheet rect of `152×165` at the origin), so the scene drew a fragment even after the mesh type was corrected. The replacement is the whole kite, sheet rect covering that whole file, pivot near the bottom point `(0.5, 0.02)`.
- Seat it on the sand. As shipped, height is about `0.24` of the lane band and the anchored Y is the feet minus `0.14` of that sprite height. Hide the planted image while the plant clip is playing, or the toss pose and the wall draw together.
- She keeps the kite on her arm the whole time.
- While the wall is up, opposite sides of it do not cross and do not attack through it. She steps back off her own wall. The other fighter stops at it. That denial does not rename the move and does not float a block.
- `RaiseWall` is the test path (callout "Shield Wall"). The AI plants Aegis Wall. Do not call `RaiseWall` from the AI. Do not change the `Hit()` return values the EditMode tests expect.

## Rejected

Do not use these as the production path. They were tried or offered and they do not match this look:

- PIL ovals and code-drawn circles in front of the feet
- A photo bracelet around the body (`344f45f`)
- An opaque 8-frame sticker ellipse (`ff4620e`)
- Torn sprite crops and a sheet rect that covers only part of the texture
- Treating `spriteMeshType: 0` as Tight. `0` is FullRect
- Random marketplace packs in place of the painted fighters
- `shadowBlur` on the page
- AutoSprite, sprite-sheet extractors, URP 3D-to-sprite bakers, Sprite Baking Studio, MeshAnimator, Frame-Aide, Sprite Dicing, ezgif
- A 16K Poly Haven HDRI dumped into this 2D canvas build, or used as a floor while the shield work is unfinished

## Confirmed

- 2026-10-15 — Ground ring is two plate Images, a flat ellipse spun in `BattleTv/GroundRing`, centred on the feet. This is the quality bar. Watched in `04dfff5`. Replaced the PIL oval, the photo bracelet, and the sticker ellipse.
- 2026-10-15 — A hit is a small additive spark on the defender's near chest, the punch frame held out, a short recoil and hit-stop, and a floater that does not rename the move. Measure span with `sizeDelta`. Watched in `5692f85`.
- 2026-10-15 — A planted wall is a second whole kite, full texture rect, cut from the toss frame, child of the plate, seated on the sand. The arm kite stays. She does not swing through her own wall. A torn source PNG is still torn after you fix the mesh type. Watched after `37429c6`.
