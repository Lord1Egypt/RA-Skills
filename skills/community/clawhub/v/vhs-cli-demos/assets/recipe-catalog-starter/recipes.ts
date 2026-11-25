// Recipe catalog — a typed list of named capture scenes (DATA).
// See ../../references/recipe-catalog-pattern.md for the pattern this implements.
// Once this base shape feels natural, ../../references/recipe-catalog-advanced.md
// covers mocking an external CLI a view depends on, an authentic cold-boot hero
// GIF, and generating near-identical recipes (e.g. a theme gallery) programmatically.
//
// Keep this file declarative: no VHS syntax, no shell commands. Just "what
// scene is this, what does it need, what happens in it."

export type Action =
  | { kind: 'type'; text: string }
  | { kind: 'key'; key: string; count?: number }
  | { kind: 'sleep'; ms: number }

export type Recipe = {
  /** 'ui-*' for stills, 'demo-*' for motion — lets --list and reviewers tell them apart at a glance. */
  name: string
  /** Surfaces in `--list`. */
  description: string
  /** Named fixture the driver should materialize before recording, or null for no fixture. */
  scenario: string | null
  /** What to run. `{{fixture}}` is replaced with the materialized fixture's path. */
  command: string
  /** Keystrokes/sleeps after launch. */
  actions?: Action[]
  /** Size the capture via font, not pixels. Default ~20. */
  fontSize?: number
  /** RARE: explicit pixel override. Only for a fixed canvas across a whole set — keep it generous. */
  canvas?: { width: number; height: number }
  /** Key into THEME_MAP (themes.ts). Omit to use the default theme. */
  theme?: string
  /** true -> motion GIF (`Output`); false/absent -> still PNG (`Screenshot`). */
  emitGif?: boolean
}

export const RECIPES: Recipe[] = [
  {
    name: 'ui-home',
    description: 'Still: the default landing screen, no fixture needed.',
    scenario: null,
    command: 'myapp',
    actions: [{ kind: 'sleep', ms: 3000 }], // generous settle — a still gets one frame, no second chance
  },
  {
    name: 'demo-workflow',
    description: 'Motion: the core workflow end to end, on a seeded fixture.',
    scenario: 'sample-repo',
    command: 'myapp ui --repo {{fixture}}',
    emitGif: true,
    actions: [
      { kind: 'sleep', ms: 1500 }, // shorter settle than a still — loading frames read as startup
      { kind: 'type', text: 'gd' }, // open diff
      { kind: 'sleep', ms: 2400 }, // hold so the viewer can read it
      { kind: 'key', key: 'Escape' },
      { kind: 'sleep', ms: 600 },
      { kind: 'type', text: 'gb' }, // switch view — show contrast, not completeness
      { kind: 'sleep', ms: 2400 },
      // no trailing quit — end on the UI, not a shell prompt
    ],
  },
]
