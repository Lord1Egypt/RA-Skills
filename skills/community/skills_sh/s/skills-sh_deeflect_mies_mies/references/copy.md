# Copy

Load when: writing or fixing interface copy — labels, buttons, headings, empty/error/loading/success states, onboarding, microcopy, notifications — or auditing a surface's words for warmth, clarity, and AI tells.

Words are interface. The same restraint applies: ask "why is this here?" of every word, and if it can't answer, cut it. What survives should read warm and clear — like a calm person who knows the user is mid-task and respects their time.

## Voice

- **Warm, not cute.** Plain, human sentences. Warmth comes from respect and good defaults, not exclamation points, mascots, or jokes the user didn't ask for.
- **Clear over clever.** The user should understand without rereading. If a label needs a tooltip to make sense, fix the label.
- **Nothing excessive.** One idea per element. No throat-clearing, no preamble, no restating the obvious.
- **Don't overexplain.** Trust the user. Explain a consequence or a non-obvious step; never narrate what the UI already shows.
- **Speak to the user's state.** Match the moment — neutral for routine actions, calmer and more concrete under stress (errors, destructive actions, money, legal, first-run).
- **Carry one voice.** If the foundation locked a copy voice (`design-system.md` → Copy Voice), write to it. If none exists and the work is more than a small fix, lock it first.

## The pass

1. Read the voice and the user's state for this surface.
2. Draft the tightest version that still answers the user's real question ("what is this / what happens if I act / what went wrong / what do I do now").
3. Cut words that don't change meaning (see Subtract).
4. Run the anti-AI pass.
5. Read it in place, at real width, in the actual state — not in a doc. Copy that reads fine in prose can be too long for a button or too cold for an empty state.

## By surface

- **Buttons and actions** — name the outcome, not the mechanism: `Save changes`, `Send invite`, `Delete project`. Verb + object. No `Submit`, `OK`, `Click here`. Match the verb in a confirm dialog to the verb on the button that opened it.
- **Labels** — the noun for the thing, in the user's words. No colons, no "Please enter your". Let placeholder show format, not repeat the label.
- **Headings** — say what the section is or does. No decorative section numbers, no manifesto headlines about the product's values (see Show, don't claim).
- **Empty states** — say what goes here and how to add the first one, in one line plus one action. This is a warmth moment, not a dead end. Don't apologize for emptiness.
- **Errors** — what happened, in the user's terms, and what they can do next. Name the specific failure, never `Something went wrong` / `Oops!`. No blame, no error codes as the whole message. If it's recoverable, the recovery is the point.
- **Loading** — usually nothing, or the noun of what's loading. Skip "Please wait". Reserve reassurance ("This can take a minute") for genuinely long waits.
- **Success / confirmation** — confirm the specific thing that happened (`Invite sent to maya@…`), then get out of the way. No celebration for routine actions.
- **Destructive confirms** — state exactly what will be lost and whether it's reversible. Plain and concrete; this is not the place for brand voice.
- **Onboarding / first-run** — one job at a time, shown not told. Cut "Welcome! We're so excited." Get the user to their first real action fast.
- **Tooltips / help / placeholders** — only when they remove genuine doubt. A tooltip restating the label is noise. Placeholders are hints, never labels and never the only label.
- **Notifications / system messages** — who did what, why it reached the user, what to do. No fake urgency.

## Subtract

Most interface copy is too long. Cut, in order:

- Throat-clearing and preamble: `In order to`, `Please note that`, `It looks like`, `We noticed that`, `Just`, `simply`.
- Restating what the UI shows or what the user just did.
- Politeness padding that delays the point: `Please`, `Kindly`, `Feel free to`. Keep "Please" only where a real ask warrants it.
- Hedges that dodge commitment: `may`, `might`, `could potentially`, `generally`. Say what happens.
- Adverbs and intensifiers doing no work: `easily`, `quickly`, `effortlessly`, `seamlessly`, `simply`.
- Triple constructions and parallel lists padded to three when two are true.

Subtraction should increase clarity. If cutting a word loses information the user needs to decide or recover, keep it — but rewrite, don't pad.

## Anti-AI pass

Generic, AI-default copy reads competent and says nothing. Scan for these (the UI-relevant subset; the full catalog lives in the `/virality` skill — `reference/ai-detection-social.md` for the short-form profile, `reference/ai-vocabulary.md` for replacements, `reference/ai-detection-patterns.md` for the exhaustive list).

Highest-signal tells in interface copy:

- **Marketing-AI vocabulary**: `seamless`, `effortless`, `powerful`, `robust`, `unlock`, `supercharge`, `elevate`, `streamline`, `leverage`, `delve`, `cutting-edge`, `next-level`, `game-changing`. Replace with the plain word or cut.
- **Fake warmth**: exclamation spam, `Oops!`, `Awesome!`, `Woohoo!`, `Let's get started!`, emoji standing in for tone. Warmth is in the help you give, not the punctuation.
- **Generic optimism / vagueness**: `Get the most out of`, `Take your X to the next level`, `Everything you need`, `The future of`. Say the specific thing instead.
- **Overexplaining**: `It is important to note`, `As you may know`, `In order to` — delete and state the thing.
- **Negative parallelism**: `It's not just X, it's Y`. Pick the true one.
- **Triple-parallel**: every benefit list arriving as exactly three. Vary or cut.
- **Em-dashes in short-form**: rare in good UI copy anyway; prefer a comma, period, or line break.
- **Uniform, balanced blandness**: every string the same medium length and equally hedged. Let one be short and blunt.

If the copy could belong to any product in the category, it's still on rails. Ground it in this product's actual nouns, this user's actual task, this surface's actual state.

## Show, don't claim

Don't write copy that announces the product's qualities — `Beautifully simple`, `Powerful yet intuitive`, `Designed with care`. The design demonstrates those; the words pointing at them undercut both. Cut value-announcing headlines and let the interface carry the impression.

## Calibrate against real copy

Like visual craft, copy improves against real references — but pull them late, for calibration, not as a template to fill in. Read how a serious tool in this category writes its empty states, errors, and primary actions; match the bar, not the wording. Don't anchor on one product's voice up front, or you'll clone it.

## Consistency

- One term per concept across the whole surface. Don't alternate `delete` / `remove` / `trash` for the same action.
- Consistent capitalization on labels and buttons (pick sentence case unless the system already uses title case).
- Consistent tense and person. Usually present tense, second person (`you`), imperative for actions.
- The same action should read the same everywhere it appears.
