# The worked style: Battle TV painted broadcast

This is the house look this skill was born from, kept whole so a new fighter, overlay or prop matches
what is already on screen. It is one worked style, not a requirement of the wider guide.

Public home: https://chatagent.ca/
Live game this look follows: https://chatagent.ca/games/lattice-arena/
Worked picture: https://deepseekoracle.github.io/battle-tv-unity/ and
https://github.com/DeepSeekOracle/battle-tv-unity

You are building that painted side-view broadcast. The fight numbers are not yours unless the user asks
for them.

**Art methods have one home:** `references/techniques.md` in this folder. Read it before you generate a
frame, import a sprite, parent a prop, write a shader, or place a hit. If this file and that log
disagree, the log is current.

## Who this is for

Several agents load this folder; one of them keeps the live arena brain. This style is the shared
picture language so any of them can add a fighter, overlay or prop that matches the screen.

This folder is the only copy of the method. Do not paste it into the live site repo or the Unity repo -
a second copy will drift. Do not put a local disk path, drive letter, or user folder in this skill.

## Standing stage

- Public repo: https://github.com/DeepSeekOracle/battle-tv-unity. Editor `6000.5.9f1`. Built-in render
  pipeline. Color space Linear. Screen-space overlay canvas. Not URP.
- One fighter, one move, then watch it. Do not generate the roster in one pass.
- Presentation lives in the Unity view (`DuelView` and the art). Fight math stays on the live game. Do
  not retune armor, cooldowns, mana, shared heals, or the roster to fix a picture.
- Do not edit the live site to change this look.
- Publish the WebGL page with `tools/publish-webgl.ps1` only when the user wants a page to watch. Do not
  `git add -A`. Do not shrink art to chase 20 MB. That publish-log line is not a failure.

## How you work

1. Read `references/techniques.md`.
2. Match an existing confirmed method before you invent one.
3. Generate or paint a plate, then measure its real pixels. A model's description of an image is not
   proof. Preview the alpha. The opaque bounds are the asset.
4. Import the whole texture as one sprite. Parent fighters, rings, sparks, and planted props to the
   stage plate. Keep the HUD on the canvas above the plate.
5. Watch the built page. A method goes into the log only after that watch shows the picture you
   intended.
6. When a watch confirms a new method, append one dated line under **Confirmed** in
   `references/techniques.md`. Name the commit or the page you watched. Do not log a method that was
   only tried. If a later watch overturns a line, append a new line that says what replaced it. Leave
   the old line and mark it replaced.

## What a 3D step is allowed to be

The shipped look is painted 2D on the plate. A mesh, baker, or 3D scene joins this style only after a
watched frame matches the painted fighters and you log that method. Do not switch the project to URP to
chase a baker. Do not replace a painted fighter with a marketplace pack.

## Adding to the log

Write the line in plain language a later session can follow without this chat:

`- YYYY-MM-DD — what you did, why it holds, where the file lives. Watched: <url or commit>.`

Rejected tools and failed looks stay in the **Rejected** list in the log so the next session does not
retry them as the production path.
