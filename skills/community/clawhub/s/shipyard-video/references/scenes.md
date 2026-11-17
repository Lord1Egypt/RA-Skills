# Build the scenes

Read `<appDir>/video/README.md` first (sections 3 and 4 especially). This page is the short route. Every path and command here (`src/`, `scripts/`, `capture/record.mjs`) is inside `<appDir>/video`, the video engine that `video-setup.mjs` copied into the app; none of it is in the Shipyard plugin folder, so run commands from there.

## Start from the example

```
cd "<appDir>/video"
cp -r src/acme src/<tag>
```

Rename `AcmeDemo` in `src/<tag>/Demo.tsx` (for example `RecipeBoxDemo`) and edit its `SCENES` map: one entry per script line id, each a small React component. Scene components receive `sc` (the scene's timing). Read `src/acme/scenes.tsx` and `src/acme/kit.tsx` first and copy their patterns.

## Give it the app's real look

- Colours: write `src/<tag>/theme.ts` with an `apply<Product>Theme(theme)` that does `Object.assign(C, {...})` using the app's real values from `globals.css` (light and dark). Use the same keys as `C` in `src/theme.ts`. Call it at the top of the Demo instead of `applyTheme`. One composition then renders both light and dark.
- Fonts: load the app's own fonts with `@remotion/google-fonts/<FontName>` (already installed) in the product folder, like `src/theme.ts` does for Inter.
- Logo and named colours live in the product folder (`src/<tag>/kit.tsx`), not in the engine's files. Copy the logo SVG from `public/icon.svg`.
- Do not copy another company's logo, colours or copy. Only the student's own brand.

## Rebuild the UI as code

- Show ONE fragment at a time, large (a card, a list, one form). Never a whole screen.
- Use fixed sizes for cards and rows so cursor targets are plain arithmetic. A flexible column that shrinks its rows makes rings and cursors drift.
- Put the `Cursor` inside the element it clicks (relative path), so you do not have to measure the layout.
- Build lists row by row on spoken words. After a click, push the camera in (scale about 1.2).
- Time motion to speech: `const {at, wi} = useTiming(sc)`; `at('word', n, fallbackFrame)` gives the frame where the spoken word starts; `wi(n, fallback)` the nth word. Clamp late animations to the scene length (`Math.min(t, sc.length - 22)`) so a fast cut does not chop them.
- Held scenes need motion (`Drift`), otherwise the render warns about dead air.
- Calm, premium, readable: big serif headline bursts of 2 to 4 words with one italic word, springy scale-ins, blur dissolves between scenes, almost no hard cuts, each beat 1 to 2.5 seconds.
- Only invented data on screen: the one fake scenario from the script.

## Register the product (two places, nothing else changes)

1. `video/src/products.json`: `"<Product>": {"scripts": ["<tag>"], "music": null, "vertical": true}`. The key (for example `RecipeBox`) becomes the composition name `<Product>-<tag>`. Keep the `Acme` entry; it is the working example.
2. `video/src/products.ts`: `import {RecipeBoxDemo} from './<tag>/Demo';` and add `RecipeBox: RecipeBoxDemo` to `DEMOS`.

Another cut of the same product (a shorter script, another voice): add the script id to `scripts`, then `video-voice.mjs <appDir> --tag <other-tag> --script <script-id>`.

Then `cd "<appDir>/video" && npx tsc --noEmit` and fix every error before looking at pictures.

## Phone (9:16) cut

Branch on `format === 'vertical'` in the Demo like `src/acme/Demo.tsx` does, and write camera keys per scene in `src/<tag>/vertical.ts` (see `src/acme/vertical.ts`). Keep UI at zoom 0.85 to 1.15 so it is readable on a phone. List scenes whose spoken words are already the on-screen headline in `NO_CAPTIONS`.

## Showing the real app instead

When the video must look exactly like the app, read `references/footage.md`: practice pages on made-up data, recorded and played inside these same scenes. Never record a signed-in live app: sign-in and waiting on real servers cost days.

## Safety

Invented company, people and numbers only. No screenshots of real accounts. The student's own brand only.
