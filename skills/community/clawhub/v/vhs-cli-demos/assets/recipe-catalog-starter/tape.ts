// recipe -> VHS tape string. A pure transform: all determinism/gotcha-handling
// lives here once, so no individual recipe has to remember it.
// See ../../references/recipe-catalog-pattern.md § "The tape builder".

import type { Recipe } from './recipes'
import { resolveTheme, type VhsTheme } from './themes'

function themeLine(theme: VhsTheme): string {
  if ('name' in theme) return `Set Theme "${theme.name}"`
  return `Set Theme ${JSON.stringify(theme)}`
}

export function buildTape(
  recipe: Recipe,
  opts: { fixturePath?: string; pinnedNow?: string; binPath?: string } = {},
): string {
  const fontSize = recipe.fontSize ?? 20
  const theme = resolveTheme(recipe.theme)
  const command = recipe.command.replace('{{fixture}}', opts.fixturePath ?? '.')

  const lines: string[] = [
    `# Generated from recipe "${recipe.name}" — edit recipes.ts, not this file.`,
    `Set Shell "bash"`,
    `Set FontSize ${fontSize}`,
    `Set Padding 24`,
    themeLine(theme),
    `Set CursorBlink false`,
    `Set TypingSpeed 50ms`,
  ]

  // RARE: only emit explicit dimensions when a recipe asks for them. Omitting
  // Width/Height lets VHS use its roomy defaults, which stay sharp when a
  // README/docs page scales the capture up.
  if (recipe.canvas) {
    lines.push(`Set Width ${recipe.canvas.width}`, `Set Height ${recipe.canvas.height}`)
  }

  lines.push('')
  if (recipe.emitGif) lines.push(`Output ${recipe.name}.gif`)
  lines.push('')

  lines.push('Hide')
  if (opts.binPath) lines.push(`Type "export PATH=${opts.binPath}:$PATH" Enter`) // unquoted $PATH — must expand
  if (opts.pinnedNow) lines.push(`Type "export APP_NOW=${opts.pinnedNow}" Enter`)
  lines.push(opts.fixturePath ? `Type "cd ${opts.fixturePath} && clear" Enter` : `Type "clear" Enter`)
  lines.push('Show', '')

  lines.push(`Type "${command}" Enter`)

  for (const action of recipe.actions ?? []) {
    switch (action.kind) {
      case 'sleep':
        lines.push(`Sleep ${action.ms}ms`)
        break
      case 'type':
        lines.push(`Type "${action.text}"`)
        break
      case 'key':
        lines.push(action.count ? `${action.key} ${action.count}` : action.key)
        break
    }
  }

  // Stills capture at an explicit point; GIFs never get a trailing quit so the
  // recording ends on the UI, not a shell prompt.
  if (!recipe.emitGif) lines.push(`Screenshot ${recipe.name}.png`)

  return lines.join('\n') + '\n'
}
