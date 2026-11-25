# Advanced recipe-catalog techniques (from a production catalog)

`recipe-catalog-pattern.md` covers the base shape. Once a catalog grows past a
few dozen recipes, a handful of harder problems show up repeatedly:
capturing app views that depend on an external CLI (`gh`, `glab`), telling an
authentic "cold boot" story instead of always hiding startup, and generating
near-identical recipes (a theme gallery) without copy-pasting each one by hand.

The techniques below are drawn from
[coco](https://github.com/gfargo/coco)'s `bin/screenshot/recipes.ts` — a
catalog with 150+ recipes — with short verbatim excerpts. Reach for these once
the base pattern's four pieces feel natural; they're refinements, not
prerequisites.

## Mocking an external CLI dependency

Some views only render once real data comes back from a CLI the app shells
out to (`gh`, `glab`, `docker`, …). Don't hit the real network in a
capture — it's slow, non-deterministic, and needs credentials in CI. Instead,
ship a small mock binary and prepend it to `PATH` for just that recipe:

```ts
{
  name: 'ui-pull-request',
  description: "Pull-request view (g p) — the current branch's PR with checks, reviews, and actions (mock gh)",
  scenario: 'feature-pr-ready',
  command: 'ui',
  githubRemote: 'git@github.com:gfargo/coco.git',
  ghMock: true,
  dimensions: { cols: 150, rows: 38 },
  actions: [
    { kind: 'sleep', ms: 2000 },
    { kind: 'type', text: 'gp' },
    { kind: 'sleep', ms: 2000 },
  ],
},
```

Two recipe fields do the work: `githubRemote` adds an `origin` remote to the
scenario's throwaway repo so the app's own forge-detection logic (parsing
`github.com/<owner>/<repo>` out of the remote URL) finds a GitHub repo to
query; `ghMock` tells the tape builder to prepend a deterministic mock `gh`
script to `PATH` before launch, so the PR/issues/triage views render canned
data instead of shelling out to the real `gh` CLI (and needing a token). The
same shape repeats for GitLab (`gitlabRemote` / `glabMock` → a mock `glab`).

Generalize this beyond git forges: **if a view's content comes from any CLI
the app shells out to, ship a mock of that CLI and prepend it to `PATH` for
the recipe**, rather than depending on real network/auth in a capture.

## `recordFromBoot`: an authentic cold-start story

The rest of this skill's advice is "settle before recording, hide the loading
state" (see Determinism in the main skill body) — correct for almost every
capture, where loading states are boring noise. But a "get started" hero GIF
is the one place a loading→ready transition is the *point*: it proves the tool
actually boots and works, not just that it looks good mid-session.

```ts
{
  name: 'demo-boot-workstation',
  description:
    'Cold boot: `coco ui` comes to life on a real repo — loading commits → the full three-pane workstation paints in, then a live cursor walks the rich graph history (install/get-started hero)',
  scenario: 'rich-history-graph',
  command: 'ui --view history',
  emitGif: true,
  recordFromBoot: true,
  dimensions: { cols: 150, rows: 38 },
  actions: [
    // The recording opens mid-boot (loading → painted) via recordFromBoot;
    // by the time the first action fires the workstation is live.
    { kind: 'sleep', ms: 1100 },
    { kind: 'key', key: 'Down' },
    { kind: 'sleep', ms: 700 },
    // ...
  ],
},
```

`recordFromBoot: true` flips the tape builder from its default (hide the
launch, start recording only once the view has settled) to recording through
the boot sequence itself — the tape builder still needs *some* hidden delay
before the visible recording starts (so the very first on-camera frame isn't
a blank terminal), it's just much shorter than a normal settle. Keep this
opt-in per recipe (coco's builder exposes it as two named constants,
`BOOT_HIDDEN_MS` / `BOOT_VISIBLE_SETTLE_MS`, tuned once and reused) — most
recipes should keep hiding the boot; reach for `recordFromBoot` only for the
one or two hero GIFs whose whole point is "watch it start up."

## `visibleCommand`: decouple what's typed on camera from what actually runs

A recipe's `command` often needs flags a viewer doesn't need to see —
`--repo /tmp/fixture-abc123`, a pinned model flag, `--dry-run`. For a
full-screen TUI this is moot (VHS's `Hide`/`Show` already keeps the launch
line off camera, and the app takes over the alternate screen). But for a
**non-TUI command whose output goes to stdout** — `commit`, `changelog`,
`review` — the typed command *is* the shot, so a viewer watching the recording
type `coco commit --repo /tmp/fixture --dry-run` reads as noise.

```ts
{
  name: 'demo-commit-flow',
  description: 'coco commit: AI drafts a Conventional Commit message from staged code changes',
  scenario: 'partial-stage',
  command: 'commit --dry-run',
  emitGif: true,
  dimensions: { cols: 100, rows: 28 },
  visibleCommand: 'coco commit',
  env: {
    COCO_SERVICE_PROVIDER: 'openai',
    COCO_SERVICE_MODEL: 'gpt-4o-mini',
  },
  actions: [
    // dist/ build: near-instant startup. LLM call ~2-4s.
    { kind: 'sleep', ms: 5000 },
  ],
},
```

When `visibleCommand` is set, that's the literal string `Type`d on camera,
while `command` (with the real flags the recipe actually needs) is what
launches behind the scenes. Reach for this whenever the on-camera command and
the fixture-aware command you need to run diverge.

## Per-recipe `env`: pin a fast, cheap model for deterministic AI timing

If any captured command calls out to an LLM, the response time (and thus how
long to `Sleep` before capturing) depends on which model answers. Pin a fast,
cheap model per recipe via `env` (exported inside the tape's hidden setup)
rather than depending on whatever the ambient environment defaults to —
`demo-commit-flow` above does exactly this (`COCO_SERVICE_PROVIDER: 'openai'`,
`COCO_SERVICE_MODEL: 'gpt-4o-mini'`) so the sleep duration in the recipe stays
a reliable estimate instead of drifting with whatever model happens to be
configured on the machine that regenerates the catalog.

> A recipe that calls a hosted LLM sends the fixture's content (here, the staged
> diff) to that provider. Run it only against a fixture repo that holds no real
> code or secrets, tell the person which provider will receive the data before
> the first run, and use a throwaway key. For CI or repeat runs, prefer a mock
> provider.

## Generating recipes programmatically

Once a catalog needs the same scene repeated across many near-identical
variants — a theme gallery is the canonical case — don't hand-write each one.
Keep the variant list as data and `.map()` it into recipes:

```ts
const NEW_THEME_GALLERY_PRESETS = [
  'catppuccin-frappe', 'rose-pine-moon', 'kanagawa-dragon', /* … */
] as const

export const RECIPES: ScreenshotRecipe[] = [
  // ...hand-written recipes...

  ...NEW_THEME_GALLERY_PRESETS.map((preset): ScreenshotRecipe => ({
    name: `ui-history-theme-${preset}`,
    description: `History view rendered with the ${preset} theme preset`,
    scenario: 'feature-pr-ready',
    command: `ui --view history --theme ${preset}`,
    dimensions: { cols: 140, rows: 32 },
    theme: preset,
  })),
]
```

This keeps the *reviewable* part of the catalog (the preset list) separate
from the *mechanical* part (turning each preset into a full recipe) — adding a
new theme to the gallery is a one-line addition to the list, not a
copy-pasted recipe block.

## "Tour" recipes: a deliberate exception to "one story per demo"

The main skill's motion-GIF guidance says **one story per demo, stop** — the
right default for nearly every recipe. A production catalog can still carry a
small, explicitly-labeled set of longer **tour** recipes that break this rule
on purpose: complete-task journeys (ship a change end-to-end; review a PR;
track down a regression via bisect) rather than a single feature in isolation.
Keep these few, name them distinctly (coco prefixes them `demo-tour-*`), and
don't let the exception creep into ordinary feature recipes — a tour recipe
should read as a deliberate choice, not a demo that grew because trimming it
felt like work.

## Character-based sizing for explicit dimensions

The main skill's sizing advice is to omit `Set Width`/`Set Height` and size
via `FontSize` alone (see the main `SKILL.md` and the sizing section in
`tape-reference.md`) — that's still the right default. When a recipe
genuinely needs explicit, reproducible dimensions across a themed set (so
every capture in a gallery is pixel-identical), express the size as **terminal
columns/rows** rather than raw pixels — `dimensions: { cols: 150, rows: 38 }`
— and let the tape builder compute `Set Width`/`Set Height` from that plus the
recipe's `FontSize`. Columns/rows are what you actually reason about when
picking a size ("wide enough for the three-pane layout without dropping to
single-pane"), and they stay meaningful if `FontSize` later changes; a bare
pixel guess doesn't.

## Addressing several recipes in one invocation

The driver in `recipe-catalog-pattern.md`'s base pattern takes `--recipe
<name>` (one) or no args (all). At catalog scale it's also worth accepting
**several names in one call**, so a themed subset (e.g. a homepage hero
carousel) can be regenerated together without re-running the whole catalog:
`npm run screenshot:sync hero-commit hero-split hero-ui hero-changelog
hero-workspace`. Cheap to add to the argument-parsing in the driver, and it's
the difference between "regenerate everything" and "regenerate everything"
being the only two speeds available.
