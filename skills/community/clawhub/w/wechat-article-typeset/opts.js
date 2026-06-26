/**
 * 解析主题混搭参数：预设、主题、版式、图片样式、代码主题。
 * 优先级：命令行 --theme/--layout > 预设 > 环境变量 > 默认值。
 */
import { resolvePreset, listPresets } from './presets.js'
import { themes } from './lib/themes/index.js'
import { layoutSets } from './lib/themes/layouts.js'

const DEFAULT_THEME = 'coral-warm'
const DEFAULT_LAYOUT = 'default'
const DEFAULT_IMAGE_STYLE = 'default'
const DEFAULT_CODE_THEME = 'vscode-dark'

function parseArgv(argv) {
  const args = argv || process.argv.slice(2)
  const out = { preset: null, themeId: null, layoutId: null, imageStyleId: null, codeThemeId: null, listPresets: false, listThemes: false, listLayouts: false, positional: [] }
  for (let i = 0; i < args.length; i++) {
    const a = args[i]
    if (a === '--list-presets' || a === '-L') out.listPresets = true
    else if (a === '--list-themes') out.listThemes = true
    else if (a === '--list-layouts') out.listLayouts = true
    else if ((a === '--preset' || a === '-p') && args[i + 1]) { out.preset = args[++i] }
    else if ((a === '--theme' || a === '-t') && args[i + 1]) { out.themeId = args[++i] }
    else if ((a === '--layout' || a === '-l') && args[i + 1]) { out.layoutId = args[++i] }
    else if ((a === '--image-style' || a === '-i') && args[i + 1]) { out.imageStyleId = args[++i] }
    else if ((a === '--code-theme' || a === '-c') && args[i + 1]) { out.codeThemeId = args[++i] }
    else if (!a.startsWith('-')) out.positional.push(a)
  }
  return out
}

/**
 * 解析最终 themeId, layoutId, imageStyleId, codeThemeId。
 * 支持：环境变量 WEWORK_PRESET / WEWORK_THEME_ID / WEWORK_LAYOUT_ID / WEWORK_IMAGE_STYLE_ID / WEWORK_CODE_THEME_ID，以及 parseArgv 返回的 CLI 参数。
 */
export function resolveOptions(argv) {
  const cli = parseArgv(argv)
  if (cli.listPresets) {
    const rows = listPresets()
    console.log('预设（主题混搭）：')
    rows.forEach(({ name, themeId, layoutId }) => console.log(`  ${name}\ttheme=${themeId} layout=${layoutId}`))
    return { exit: true }
  }
  if (cli.listThemes) {
    console.log('主题(themeId)：')
    themes.forEach((t) => console.log(`  ${t.id}\t${t.name}`))
    return { exit: true }
  }
  if (cli.listLayouts) {
    console.log('版式(layoutId)：')
    layoutSets.forEach((l) => console.log(`  ${l.id}\t${l.name}`))
    return { exit: true }
  }

  const presetName = cli.preset || process.env.WEWORK_PRESET
  const fromPreset = presetName ? resolvePreset(presetName) : null

  let themeId = cli.themeId || process.env.WEWORK_THEME_ID || (fromPreset && fromPreset.themeId) || DEFAULT_THEME
  let layoutId = cli.layoutId || process.env.WEWORK_LAYOUT_ID || (fromPreset && fromPreset.layoutId) || DEFAULT_LAYOUT
  let imageStyleId = cli.imageStyleId || process.env.WEWORK_IMAGE_STYLE_ID || (fromPreset && fromPreset.imageStyleId) || DEFAULT_IMAGE_STYLE
  let codeThemeId = cli.codeThemeId || process.env.WEWORK_CODE_THEME_ID || (fromPreset && fromPreset.codeThemeId) || DEFAULT_CODE_THEME

  return {
    exit: false,
    themeId,
    layoutId,
    imageStyleId,
    codeThemeId,
    positional: cli.positional,
  }
}
