# Interface sounds (optional, off by default)

Only add sounds if the student asks. They ship OFF; the user turns them on in Settings.

## Rules

- Default off. Store the choice in `localStorage` (`ui-sounds` = `"on"` / `"off"`), and in the user profile if the app has one.
- A single switch in Settings > Appearance: "Interface sounds", with a volume slider only if they ask.
- Never play on page load, on scroll, or for anything the user did not just do. Never for errors that already show a message, unless asked.
- Good moments: a task completed, a message sent, recording started/stopped, a timer finished.
- Tiny files: short (under 300 ms), under 20 KB each, `.mp3` or `.webm`, in `public/sounds/`. Preload once after the user turns sounds on, not before.
- Quiet by default (volume 0.3 to 0.5). Use one sound family so they feel related.
- Respect the system: skip sounds when the tab is hidden. If the user has reduced motion on, still allow sounds (that setting is about motion), but keep them subtle.
- Sounds are never the only signal: always show something on screen too.
- Use sounds you are allowed to ship: make them (e.g. a short synthesized tone with the Web Audio API) or use a CC0 pack, and note the source in DESIGN.md.

## Minimal helper

```ts
// src/lib/sounds.ts
const cache = new Map<string, HTMLAudioElement>();
export const soundsOn = () => { try { return localStorage.getItem("ui-sounds") === "on"; } catch { return false; } };
export function play(name: "done" | "send" | "start" | "stop", volume = 0.4) {
  if (!soundsOn() || document.hidden) return;
  let a = cache.get(name);
  if (!a) { a = new Audio(`/sounds/${name}.mp3`); cache.set(name, a); }
  a.volume = volume; a.currentTime = 0; void a.play().catch(() => {});
}
```
