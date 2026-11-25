# Patterns and pitfalls

## Default principles

| Principle | What it means | Seen in |
|---|---|---|
| One AI entry point | One floating ✦ button opens a half-sheet chat. It knows the current screen and has a scope chip (this item / this folder / everything). Answers cite sources (timestamps, lines) that open the exact spot. Remove AI tabs and other widgets. | Granola (scope switch), ChatGPT and similar AI chat apps (one composer), Notion AI |
| Home · + · Actions | Bottom bar with 3 items: Home, a large centre +, and a cross-item list (to-dos, actions). Rare things (folders, settings, connections, help) move into a left drawer opened from the avatar. | ChatGPT (drawer), Linear, Todoist |
| One + sheet | Every way to create something (record, upload, paste link, import, connect) lives in one sheet. The top option starts with last-used settings in one tap; the settings are one line you can change. | Otter, Fireflies, Notion |
| Calm live screen | At most 5 controls (for example pause, stop, notes/transcript, mark moment, ask). Live notes are the default view; decisions and to-dos appear as cards. Asking opens as a half-sheet so the content stays visible. | Granola, Otter |
| Summary first | A detail screen opens on the summary, then the person's actions, then key moments. At most 4 sections; hide sections with no content (for example slides). | Granola, Fireflies |
| Useful waiting | A processing screen shows progress in plain words and lets the user do something (read the partial result, name people, set the title). Offer an email or notification when it takes long. | Otter |

## Themes vs layout

Classify every existing theme from its CSS: if it only changes tokens (colour, blur, radius, shadow, font, spacing) it stays a theme. If it hides, moves or adds elements, or changes navigation, that part is a layout and moves behind the layout setting. Two settings, any combination valid: theme x layout. Test the new layout under every theme.

## Step counting

Count taps and screens from app open to the outcome, from the code (routes, buttons, required fields), not from guesses. Typing a value is one step. Report current, proposed, and the saving.

## Pitfalls

- The floating AI button covers a media player, a send box or a bottom sheet's button. Lift it above the player and hide it while a sheet is open.
- Mobile CSS that hides the desktop sidebar also hides the new drawer (same element or class). Give the drawer its own element.
- Dev or test pages (for example a component gallery) still reachable in production. Remove or guard them.
- Two layouts drift: every new feature needs both until the old one is removed. Set a date to remove it.
- End-to-end tests that already fail on main: run them on main too and say so, so they are not blamed on the PR.
- Screenshots taken signed out show the landing page. Use a seeded test account or a dev route behind a flag, and say which.
- Skill reference files missing (for example a review skill's checklists): do the step by hand and say so instead of skipping it silently.
