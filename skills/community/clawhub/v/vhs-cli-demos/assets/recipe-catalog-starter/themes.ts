// Maps your app's theme/preset names to VHS terminal palettes.
//
// See recipe-catalog-pattern.md § "Theme-palette mapping": if the app has
// themes, the *terminal's* palette must match the app's, or every theme
// renders on the same background and a "theme showcase" is N near-identical
// images.

export type VhsTheme =
  | { name: string } // a named VHS built-in, e.g. "Catppuccin Mocha"
  | {
      // a custom palette — background/foreground + ANSI slots derived from
      // the app's own accent colors
      background: string
      foreground: string
      black?: string
      red?: string
      green?: string
      yellow?: string
      blue?: string
      magenta?: string
      cyan?: string
      white?: string
    }

const DEFAULT_THEME: VhsTheme = { name: 'Catppuccin Mocha' }

// Fill in as your app grows themes, e.g.:
// export const THEME_MAP: Record<string, VhsTheme> = {
//   'my-app-dark': { name: 'Catppuccin Mocha' },
//   'my-app-light': { name: 'Catppuccin Latte' },
//   'my-app-solarized': {
//     background: '#002b36', foreground: '#839496',
//     red: '#dc322f', green: '#859900', yellow: '#b58900', blue: '#268bd2',
//   },
// }
export const THEME_MAP: Record<string, VhsTheme> = {}

export function resolveTheme(preset: string | undefined): VhsTheme {
  if (!preset) return DEFAULT_THEME
  return THEME_MAP[preset] ?? DEFAULT_THEME
}
