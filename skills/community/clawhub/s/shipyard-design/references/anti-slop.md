# Avoiding the "made by AI" look

Apps built quickly often share the same tells: purple gradients, emoji everywhere, invented testimonials, tip boxes. Two layers stop this: a script that checks the code, and judgement rules that only a person (or you, looking at screenshots) can apply.

## What the script checks

`npm run check:design` in the app, and `verify.mjs <app> --only design`. It runs in the pull request checks too. Each finding says `file:line rule` and how to fix it.

| Rule | Catches | Fix |
|---|---|---|
| `hard-coded-colour` | A hex code, `rgb(` or `hsl(` value, or a Tailwind palette class like `bg-blue-500` in a component | Use a colour variable such as `var(--accent)` or an existing class |
| `gradient` | Gradient backgrounds | Use a flat colour. A real exception needs `design-check: allow-gradient` |
| `em-dash` | A long dash in text people read | Use a comma, colon or full stop |
| `emoji-in-ui` | Emoji in screens | Use words or the app's icons |
| `placeholder-text` | "Lorem ipsum", "Your tagline here", "Feature 1", "TODO" | Write the real text |
| `fake-proof` | "10,000+ users", five stars, "Trusted by", "#1 rated", "as seen on" | Remove, or use true numbers with `design-check: real-data` |
| `ai-badge` | "Powered by AI", "AI-powered", sparkle marks | Remove. Show what it does, not how it is made |
| `native-alert` | `alert(`, `confirm(`, `prompt(` | Use the app's own dialog (`ConfirmModal`) |
| `small-input-text` | Inputs smaller than 16px (phones zoom in) | Make them 16px or larger |
| `tip-box` | Text starting "Tip:" or "Pro tip:" | Put the guidance in the screen itself |

Colours are allowed only in `src/app/globals.css` and in `opengraph-image` files. The generated files `src/lib/theme.ts` and `src/lib/fonts.ts` are skipped.

Escape comments, for deliberate exceptions only:
- `design-check: allow-<rule>` on the line or the line before it, for any rule (`allow-colour` also works for colours).
- `design-check: real-data` for true numbers or names that look like proof.
- `design-check: allow-file <rule>` near the top, for a whole file (used for the Google sign-in button, which needs Google's own colours).

Say why in plain words next to the comment.

## What only judgement can check

Look at the screenshots and fix these yourself:
- One clear main heading per page. Headings step down in size and weight.
- A clear hierarchy: the main action is the most noticeable thing; quiet things are quiet.
- Empty, loading and error states are designed, not blank or raw.
- No explanatory sentences inside menus and buttons. Labels are short.
- No subtitle that repeats the title in other words.
- Legal links (privacy, terms) live in the account menu, not a footer on app screens.
- One accent colour. No rainbow of buttons.
- Real numbers and real names only. If there is no data yet, say so honestly.
- Touch targets at least 48px high, enough space around text, nothing cut off at 375px wide.
- Light and dark both look deliberate, not just inverted.
