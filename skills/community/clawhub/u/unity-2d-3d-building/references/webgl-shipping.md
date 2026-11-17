# Shipping a Unity WebGL build on a real page

Starts at the build output. The page it lands on usually has its own chrome - a header bar, a player
widget, a hub - and that chrome is the part a naive deploy destroys.

## Order of work

1. **Decide the compression mode before the first deploy** - it changes the emitted file names (rule 1).
2. After each build: delete the DoNotShip folder, sync `Build/*` to the site, and leave the site's own
   `index.html` alone (rules 2-3).
3. Commit only the build's paths. A shared repo usually carries unrelated dirty files and a blanket
   `git add -A` sweeps them into the push.
4. Poll the live document for a changed marker, then compare the served wasm's byte size against the
   local build (rule 7).
5. Load the live URL in a browser and click into gameplay: the menu rendering proves the loader, the
   first gameplay frame proves the scene, scripts and wasm all came up.

## Rules

- **A static host serves `.gz` payloads as `application/gzip` with no `Content-Encoding`, and you cannot
  patch the host's handler - so ship the decompression-fallback build.** A stock gzip WebGL build
  answers exactly that way on GitHub Pages and the loader stalls at the progress bar forever. Build with
  `PlayerSettings.WebGL.decompressionFallback = true` (a project setting, not a script argument - set it
  with a tiny eval file and log the value back to confirm it took). Unity then emits `*.unityweb`
  payloads plus a loader that inflates them in JS; the live wasm should read
  `Content-Type: application/vnd.unity`. Delete the superseded `.gz` files rather than shipping both.
- **Delete `<Game>_BurstDebugInformation_DoNotShip/` before publishing.** It is written into the build
  output directory and its name is the instruction. It also bloats the repo.
- **A rebuild changes only `Build/*`; sync that and leave the site's page alone.** Asset names
  (`*.unityweb`, `loader.js`) and the loader reference are stable across builds, so the page's chrome
  and any injected widget survive untouched. Re-copying Unity's template over the page only to re-apply
  the chrome destroys both. If a helper script does the widget injection, remember native tools need a
  native path: an MSYS-style `/d/...` argument can make such a script report "no index.html" and do
  nothing while its caller reports success.
- **Unity's template centres the canvas with `top: 50%` AND `transform: translate(-50%, -50%)` -
  override both or neither.** Replacing `top` with a fixed offset to clear a site header leaves the
  `-50%` lift in force, so the container is pulled up by half its own height and the visitor sees only
  the bottom strip of the game. Move them together - `top: calc(50% + 20px) !important; transform:
  translate(-50%, -50%) !important` for a 40 px header - and note the template's own rule is
  id+class, so a plain ID selector needs `!important` to win.
- **A fixed-size canvas cannot fit a short window; clamp it without touching the aspect.**
  `#unity-canvas { max-width: 100vw; max-height: calc(100vh - 100px); width: auto; height: auto }` - for
  a replaced element a clamped height with `width: auto` follows the intrinsic ratio, so it neither
  clips nor squashes. A fixed-size canvas that is merely re-centred still clips its own top on a short
  window.
- **A host-injected widget with an inline position needs `!important` to move.** A bar written as
  `style="position:fixed;top:10px;z-index:9999"` stays behind a fixed site header no matter what a
  stylesheet says without `!important`, and raising its z-index instead just puts it on top of the
  header. Offset it (`#the-bar { top: 46px !important; }`), or park it inside the header's own 40 px
  strip (`top: 4px` with a higher z-index) if offsetting it below the header covers the top of the game.
- **Escape can never be an in-game key on a web build.** In a browser Escape leaves fullscreen and drops
  canvas focus, so any menu bound to it quits the game instead of opening the menu. Bind TAB with a
  non-browser backstop (`KeyCode.Tab || KeyCode.M`) - a browser may still take Tab for focus navigation
  - and update the on-screen control line in the same edit, or the HUD keeps naming a key that ejects
  the player.
- **Prove the compiled code shipped, not just the page.** Poll the served document for a changed marker
  string (CDN lag has been one to three minutes, with different edges disagreeing in between - never
  conclude a deploy failed from one early read), then compare the served `.wasm`/`.wasm.unityweb` byte
  size against the local build. An HTML change proves the page; only a size change in the wasm proves
  the new code is live rather than an older bundle being re-served. A cache-buster on the document is
  not a substitute for polling the bare URL a visitor actually gets.
- **Verify the layout numerically, and never from a screenshot alone.** Assert the container top equals
  `innerHeight/2 + headerHeight/2 - containerHeight/2` within a pixel, that `canvas.top >=
  headerHeight`, that `canvas.bottom <= innerHeight`, and that the width/height ratio is unchanged. The
  formula holds at any viewport, which matters because a test browser window is usually far shorter than
  the visitor's - a clip seen there is usually the harness, not the page. Read `innerWidth`/`innerHeight`
  back in every probe: `Emulation.setDeviceMetricsOverride` does not always take effect before the
  page's own scripts run.
- **Gate a continuous sound on state and motion, never on one near-zero number.** An idling engine sits
  above any near-zero rpm threshold, so an "idle bed" keyed off rpm plays on page load, the title
  screen and the pre-race grid - exactly the noise a player reports as "still on when you load the
  game". Make it audible only while the session is running AND something is moving or the input is
  held, and keep menus and loading screens silent.
- **Trimming volume cannot fix a noise-derived clip's character.** A low pitch with a permanent volume
  floor on a broadband-noise loop reads as static; cutting the level does not change the character, only
  removing or replacing it does. Diagnose a suspect clip with an FFT (flat broadband energy with no
  peaks is the mistake). Route every sound through one shared scale so levels are a single landing point
  later instead of per-clip edits.
- **Run the build call on its own.** A Unity WebGL build runs minutes; a single call that builds, sleeps
  and then polls for the deploy exceeds the tool's ceiling and comes back with nothing, which looks like
  a failed build. Build in one call; copy, commit and push in the next.
