# Hooks: the first two seconds

The hook decides whether anyone sees the rest. In a paid campaign it also has to be true: a hook is
checked like any other line (references/claims.md), so a hook about your own use is confirmed and
a hook with a brand claim points to its talking point.

## One angle per video

A video that carries one idea reads like a person talking; one that lists every talking point reads
like an ad. Pick one angle per video (one or two talking points), and spread the others over the
campaign's other videos so every required point is covered somewhere. `script.py` warns at more
than two.

## Hook types

| Type | Shape | From the example brief |
|---|---|---|
| Show it first | the thing on screen before any word about it | "This launch could be your lock screen" while holding the phone with the photo up to the camera |
| Watch me | you doing the thing, live | "Watch me find today's space photo" while opening the app |
| Question | the talking point as a question the viewer answers in their head | "A new space photo every single day?" |
| Problem | the small annoyance the product fixes | "My lock screen has been the same photo for two years" (only if true, confirmed) |
| Result first | the outcome, then how | "Two taps and this is your wallpaper" |
| Contrarian | a mild disagreement with what people assume | "You don't need a wallpaper app with ads in it" (only when the brief's talking points back it) |

A result or problem hook about yourself is an experience claim: it needs the creator's
confirmation, like any experience line. No hook promises an outcome the brief doesn't state, and no
hook uses "the best", "guaranteed" or "number one".

## The first frame

- **Something moves in frame one.** A hand, the phone coming up, the footage already playing. A
  still face waiting to talk loses people.
- **Show before you explain.** If the hook is about a photo, the photo is on screen as you say it.
- **Three things agree:** what you say, the hook text on screen, and what the picture shows. A hook
  text that says one thing while you say another splits attention.
- **The "Ad" label is small and in the corner**, so the hook text has the middle of the frame.
- **Under 12 words**, said in about two seconds.

## An action for every hook

Each hook in `script.json` gets an `action`: what you physically do while saying it. It goes into
the shot list, so the hook take isn't just your face. Word it without naming a layout ("point at the launch on
screen", not "point up at the top half"): the same hook can open a split screen and a face plus
screen recording, where the top half is something else.

```json
{"id": "h1", "text": "This launch could be your lock screen", "claim": "none",
 "action": "hold the phone up to the camera with the launch photo on screen"}
```

## Good and bad, from the example brief

| Bad | Why | Better |
|---|---|---|
| "This launch is now my lock screen" (not confirmed) | an experience claim nobody confirmed | "This launch could be your lock screen", or confirm it if it is true |
| "Hey guys, so today I want to talk about an app" | nothing happens for three seconds | "Watch me find today's space photo" |
| "The best space app ever" | an absolute claim, and on the brief's never-say list | "A new space photo every single day?" |
| "This is an ad for <brand>" as the hook, with a 10-second window | spends the hook on the disclosure | the hook first, then "<brand> is paying me to show you this" inside the window |

## When the window is 3 or 4 seconds: a hook that discloses

A brief that wants the ad said in the first 3 seconds leaves no room for a line after the hook. Open
with a hook that discloses and still makes a promise; `script.py` counts it as the disclosure:

- "Ad, but this could be your lock screen"
- "Sponsored by <brand>: watch this"
- "<brand> paid me to find you today's space photo"
- "#ad: two taps and this is your wallpaper"

Not when the brief says not to say it in the hook (`"not_in_hook": true`).

## Testing hooks

One edit can go to TikTok, Reels and Shorts with the same hook. Different hooks per platform are an
optional test: give each account its own opening in `openings`. The ledger keeps each post's hook
next to its views (`ledger.py --report` lists them). Different platforms reach different people, so
read it with care before you reuse a hook.
