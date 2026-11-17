# Publish: web copy, poster, captions

`node "${CLAUDE_PLUGIN_ROOT}/scripts/video-publish.mjs" <appDir> <render-name>`

`<render-name>` is the name `video-render.mjs` printed (without `.mp4`), for example `launch-light-nomusic`. Do this once per cut you want on the web (light, dark, phone).

## What it makes

In `<appDir>/public/video/`:

- `<name>.mp4`: H.264 with AAC sound, loudness-normalised, plays before it finishes loading, tuned to stay under 10 MB (it tries better quality first and gets smaller step by step). If it cannot get under the limit it says so: make the video shorter.
- `<name>.jpg`: the poster picture. It is taken from just under halfway; pass `--poster-at <seconds>` to pick a frame where the screen is full, then open the picture and check it is not blank.
- `demo.vtt`: the captions (one file shared by all cuts). `--captions-top` puts the captions at the top of the picture: use it when the video already shows text at the bottom. `--vtt <tag>` picks the captions of another cut. The silent cut needs no file because its captions are in the picture. `--lang <code>` is the language the video speaks (default `en`): with `--lang el` the player's captions menu says "Ελληνικά".

File names are plain (`demo-light`, `demo-dark`, `demo-light-phone`), never the product's name. Use `--name` only for another plain name.

It also records the published video in `.shipyard-app.json` (`video.published`) and makes sure signed-out visitors can open `.mp4`, `.webm` and `.vtt` files: the app's `src/proxy.ts` sends signed-out visitors to sign-in for every path except a short list of static file types, so the script adds these three (`--no-patch` skips this). Tell the student this one-line change was made and why; it must be in the pull request.

On an app Shipyard did not make (`--general`, after the upgrade guide), it changes neither file. Shipyard does not guess at another app's sign-in rules, so it prints one check instead: open the mp4's address in a private window while signed out. If that lands on a sign-in page, let `.mp4`, `.webm` and `.vtt` files through the app's sign-in check, in the pull request. It also prints a plain HTML snippet for pages that are not React. `--public-dir <folder>` puts the files in another folder the app serves as they are (for example `static` or `web`).

## Put it on the page

The script prints a snippet. It looks like:

```tsx
<video controls playsInline preload="none" poster="/video/demo-light.jpg" aria-label="Product video" style={{ width: "100%", height: "auto" }}>
  <source src="/video/demo-light.mp4" type="video/mp4" />
  <track kind="captions" src="/video/demo.vtt" srcLang="en" label="English" />
</video>
<p>Narrated with an AI voice.</p>
```

- `preload="none"`: nothing downloads until someone presses play, so the page stays fast.
- Captions are off by default on purpose. Keep it that way.
- Show the dark cut when the page is dark and the light cut when it is light (two `<video>` elements, show the one that matches the app's theme).
- Keep the "Narrated with an AI voice" note next to the video wherever it is shown (home page, store listing, social post).
- If the student wants a home page section, add it following the app's `AGENTS.md`: tokens only, designed states, no filler text. Change the `aria-label` to describe the video.

## Before the student shares it

- Re-watch the final mp4 once, start to end. Check the first and last second, the caption text, and that every claim is true of the app today.
- Store listings and social posts need the AI-voice note too.
- The files in `public/video/` are part of the app. They are committed like code (each under 10 MB). Ask "OK to save this to GitHub?" first. On a live app use a branch and a pull request; never push straight to a branch that publishes automatically.

## YouTube and other sites

Read `references/youtube.md` before the video goes on YouTube or anywhere else.

## Licence note

The video engine uses Remotion. It is free for individuals and companies of up to 3 people; larger companies need a paid licence (remotion.dev/license). The student's videos are their own.
