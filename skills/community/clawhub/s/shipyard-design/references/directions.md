# Drafting 3 directions

The student wants to see options for THEIR app, not a catalogue. You write three look files, the script renders real screenshots of their app in each, and they pick one.

## Before you write

Read `SPEC.md` (or ask one question if there is none): who uses the app, what they do most, what mood fits. A recipe app for families, a budget tool for freelancers and a meditation timer need three different answers.

Also write the app's real home words in `src/lib/home-content.ts` before running the script: the screenshots show those words, and `design-directions.mjs` warns while the template's stand-in text is still there.

## Make them truly different

Two directions may share at most 4 of these 7 things: menu style (`layout.nav`), homepage pattern (`layout.home`), card style, button style, density, text size (`type.scale`), font. The script refuses otherwise and says "make them more different". Aim for at most 3 shared. Also vary the accent colour family and the page tone (warm paper, cool grey, near-black). Never two blues. Never default to a purple or blue-purple gradient look.

Give each a direction in feeling, e.g. A "calm and quiet", B "bold and friendly", C "sharp and efficient", then let that decide everything:

| Choice | Pick from | Leans toward |
|---|---|---|
| nav | `bottom-nav`, `sidebar`, `top-nav` | phone-first apps: bottom. Tools with many screens: sidebar. Content, shops, sites: top. |
| home | `focus`, `split`, `editorial`, `cards`, `list` | one clear promise: focus. Product with a visual: split. Reading: editorial. Several actions: cards. App-like daily use: list. |
| cards | `flat`, `bordered`, `elevated`, `tinted` | calm: flat. Precise: bordered. Friendly: elevated. Playful: tinted. |
| buttons | `solid`, `pill`, `outline`, `sharp` | pill friendly, sharp technical, outline quiet. |
| density | `compact`, `regular`, `airy` | data-heavy: compact. Relaxed: airy. |
| type.scale | `compact`, `comfortable`, `large` | headings carry the mood. |
| header | `plain`, `bar`, `centered` | |
| maxWidth | `narrow`, `medium`, `wide` | only changes top-nav and sidebar pages |

`editorial` home with `sidebar` nav is a warning (odd pair). Fonts and the file format are in `tokens.md`. Use real, readable colours; the script repairs small contrast problems with `--fix`, but start from good ones. Give each direction its own `id` (`direction-a` and so on), a short feeling-based `name` and a one-line `description`, no brand names.

## Then

1. Save as `<appDir>/.shipyard/design/direction-a.tokens.json`, `-b`, `-c`.
2. Run `design-directions.mjs <appDir>`. If it complains about similarity, change nav, home or cards on one of them rather than only colours.
3. Tell the student the page is open, what each direction is in one plain line, and your pick with the reason in user terms.
4. They paste `Shipyard: use direction B for <App>`. Apply it (see SKILL.md).
5. If they like one but want a tweak ("same but warmer"), edit that file and apply again.
