import { getStringArg, hasFlag, parseArgs, readJsonFile, writeJsonMaybe } from './_shared'

type LoosePanel = {
  id?: string
  panelId?: string
  clipId?: string
  panelIndex?: number
  panel_index?: number
  index?: number
  imageUrl?: string
  image?: string
  firstFrame?: string
  first_frame_image?: string
  videoPrompt?: string
  prompt?: string
  video_prompt?: string
  subtitleText?: string
  subtitle?: string
  srtSegment?: string
  srt_segment?: string
  isMainClip?: boolean
  is_main_clip?: boolean
}

type LooseInput = {
  projectId?: string
  episodeId?: string
  panels?: LoosePanel[]
  clips?: LoosePanel[]
  storyboard?: LoosePanel[]
}

export type GuardPanel = {
  panelId: string
  panelIndex: number
  imageUrl: string
  videoPrompt: string
  subtitleText: string
  isMainClip: boolean
}

export type GuardResult = {
  ok: boolean
  identityLocked: boolean
  orderingValid: boolean
  duplicates: string[]
  skippedIndexes: number[]
  needsUserConfirmation: boolean
  target?: GuardPanel
  orderedPanels: GuardPanel[]
  errors: string[]
  warnings: string[]
}

export type GuardOptions = {
  panelId?: string
  panelIndex?: number
  requireImageApproval?: boolean
}

function normalizePanel(panel: LoosePanel): GuardPanel {
  return {
    panelId: String(panel.panelId ?? panel.id ?? panel.clipId ?? ''),
    panelIndex: Number(panel.panelIndex ?? panel.panel_index ?? panel.index ?? -1),
    imageUrl: String(panel.imageUrl ?? panel.image ?? panel.firstFrame ?? panel.first_frame_image ?? ''),
    videoPrompt: String(panel.videoPrompt ?? panel.prompt ?? panel.video_prompt ?? ''),
    subtitleText: String(panel.subtitleText ?? panel.subtitle ?? panel.srtSegment ?? panel.srt_segment ?? ''),
    isMainClip: Boolean(panel.isMainClip ?? panel.is_main_clip ?? false),
  }
}

function resolvePanels(input: LooseInput): GuardPanel[] {
  const list = input.panels ?? input.clips ?? input.storyboard ?? []
  return list.map(normalizePanel)
}

function uniqueSorted(values: number[]): number[] {
  return [...new Set(values)].sort((a, b) => a - b)
}

export function validatePanelOrder(input: LooseInput, options: GuardOptions = {}): GuardResult {
  const panels = resolvePanels(input)
  const errors: string[] = []
  const warnings: string[] = []

  if (!panels.length) {
    errors.push('未找到可校验的 panels/clips/storyboard')
  }

  const duplicateIds = panels
    .map((item) => item.panelId)
    .filter(Boolean)
    .filter((item, index, arr) => arr.indexOf(item) !== index)
  const duplicateIndexes = panels
    .map((item) => item.panelIndex)
    .filter((item) => item >= 0)
    .filter((item, index, arr) => arr.indexOf(item) !== index)
    .map((item) => `panelIndex=${item}`)
  const duplicates = [...new Set([...duplicateIds, ...duplicateIndexes])]
  if (duplicates.length) {
    errors.push(`存在重复 panel 标识: ${duplicates.join(' / ')}`)
  }

  const orderedPanels = [...panels].sort((a, b) => a.panelIndex - b.panelIndex)
  const orderedIndexes = uniqueSorted(orderedPanels.map((item) => item.panelIndex).filter((item) => item >= 0))
  const skippedIndexes: number[] = []
  for (let i = 1; i < orderedIndexes.length; i += 1) {
    const prev = orderedIndexes[i - 1]
    const current = orderedIndexes[i]
    if (current > prev + 1) {
      for (let missing = prev + 1; missing < current; missing += 1) skippedIndexes.push(missing)
    }
  }
  if (skippedIndexes.length) {
    warnings.push(`检测到缺失顺序索引: ${skippedIndexes.join(', ')}`)
  }

  let target: GuardPanel | undefined
  if (options.panelId) {
    target = panels.find((item) => item.panelId === options.panelId)
    if (!target) errors.push(`未找到目标 panelId=${options.panelId}`)
  }
  if (typeof options.panelIndex === 'number' && Number.isFinite(options.panelIndex)) {
    const matched = panels.find((item) => item.panelIndex === options.panelIndex)
    if (!matched) {
      errors.push(`未找到目标 panelIndex=${options.panelIndex}`)
    } else if (target && matched.panelId !== target.panelId) {
      errors.push(`panelId 与 panelIndex 指向不一致: ${target.panelId} vs ${matched.panelId}`)
    } else {
      target = matched
    }
  }

  if (target) {
    if (!target.panelId || target.panelIndex < 0) {
      errors.push('目标 panel 缺少稳定身份字段')
    }
    if (!target.imageUrl) warnings.push('目标 panel 缺少 imageUrl')
    if (!target.videoPrompt) warnings.push('目标 panel 缺少 videoPrompt')
    if (!target.subtitleText) warnings.push('目标 panel 缺少 subtitleText')
  }

  const identityLocked = Boolean(target?.panelId || target?.panelIndex >= 0)
  const orderingValid = duplicates.length === 0
  const needsUserConfirmation = Boolean(options.requireImageApproval) || warnings.length > 0 || !identityLocked
  const ok = errors.length === 0

  return {
    ok,
    identityLocked,
    orderingValid,
    duplicates,
    skippedIndexes,
    needsUserConfirmation,
    target,
    orderedPanels,
    errors,
    warnings,
  }
}

if (require.main === module) {
  const args = parseArgs(process.argv.slice(2))
  const inputPath = getStringArg(args, 'input')
  const outputPath = getStringArg(args, 'out') || undefined
  const targetPanelId = getStringArg(args, 'panel-id')
  const targetPanelIndexRaw = getStringArg(args, 'panel-index')
  const requireImageApproval = hasFlag(args, 'require-image-approval')

  if (!inputPath) {
    throw new Error('用法: tsx guard-panel-order.ts --input <json> [--panel-id <id>] [--panel-index <n>] [--require-image-approval] [--out <json>]')
  }

  const input = readJsonFile<LooseInput>(inputPath)
  const result = validatePanelOrder(input, {
    panelId: targetPanelId || undefined,
    panelIndex: targetPanelIndexRaw ? Number(targetPanelIndexRaw) : undefined,
    requireImageApproval,
  })

  writeJsonMaybe(result, outputPath)
  if (!result.ok) process.exit(2)
}
