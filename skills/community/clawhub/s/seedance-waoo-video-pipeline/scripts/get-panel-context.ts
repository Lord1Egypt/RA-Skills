import { getStringArg, hasFlag, parseArgs, readJsonFile, writeJsonMaybe } from './_shared'

export type ResolvedPanelContext = {
  projectId?: string
  episodeId?: string
  panelId: string
  panelIndex: number
  imageUrl: string
  videoPrompt: string
  subtitleText: string
  existingVideoUrl?: string
  isMainClip: boolean
}

type LoosePanel = Record<string, any>

type LooseInput = {
  projectId?: string
  episodeId?: string
  panelId?: string
  panelIndex?: number
  imageUrl?: string
  videoPrompt?: string
  subtitleText?: string
  existingVideoUrl?: string
  isMainClip?: boolean
  panels?: LoosePanel[]
  clips?: LoosePanel[]
  storyboard?: LoosePanel[]
}

function normalizePanel(root: LooseInput, panel: LoosePanel): ResolvedPanelContext {
  const panelId = String(panel.panelId ?? panel.id ?? panel.clipId ?? '')
  if (!panelId) throw new Error('panel 缺少 id/panelId')
  const panelIndex = Number(panel.panelIndex ?? panel.panel_index ?? panel.index ?? 0)
  const imageUrl = String(panel.imageUrl ?? panel.image ?? panel.firstFrame ?? panel.first_frame_image ?? '')
  const videoPrompt = String(panel.videoPrompt ?? panel.prompt ?? panel.video_prompt ?? '')
  const subtitleText = String(panel.subtitleText ?? panel.subtitle ?? panel.srtSegment ?? panel.srt_segment ?? '')
  const existingVideoUrl = String(panel.existingVideoUrl ?? panel.videoUrl ?? panel.video_url ?? '') || undefined
  return {
    projectId: root.projectId,
    episodeId: root.episodeId,
    panelId,
    panelIndex,
    imageUrl,
    videoPrompt,
    subtitleText,
    existingVideoUrl,
    isMainClip: Boolean(panel.isMainClip ?? panel.is_main_clip ?? false),
  }
}

function resolvePanels(input: LooseInput): ResolvedPanelContext[] {
  if (input.panelId || input.imageUrl || input.videoPrompt || input.subtitleText) {
    return [normalizePanel(input, input)]
  }
  const list = input.panels ?? input.clips ?? input.storyboard ?? []
  return list.map((item) => normalizePanel(input, item))
}

function pickPanel(panels: ResolvedPanelContext[], args: Record<string, string | boolean>): ResolvedPanelContext {
  const panelId = getStringArg(args, 'panel-id')
  const panelIndexRaw = getStringArg(args, 'panel-index')
  const preferMain = hasFlag(args, 'main')

  if (panelId) {
    const found = panels.find((item) => item.panelId === panelId)
    if (!found) throw new Error(`未找到 panel-id=${panelId}`)
    return found
  }

  if (panelIndexRaw) {
    const panelIndex = Number(panelIndexRaw)
    const found = panels.find((item) => item.panelIndex === panelIndex)
    if (!found) throw new Error(`未找到 panel-index=${panelIndex}`)
    return found
  }

  if (preferMain) {
    const found = panels.find((item) => item.isMainClip)
    if (found) return found
  }

  const mainClip = panels.find((item) => item.isMainClip)
  return mainClip ?? panels[0]
}

if (require.main === module) {
  const args = parseArgs(process.argv.slice(2))
  const inputPath = getStringArg(args, 'input')
  const outputPath = getStringArg(args, 'out') || undefined
  if (!inputPath) {
    throw new Error('用法: tsx get-panel-context.ts --input <json> [--panel-id <id>|--panel-index <n>|--main] [--out <json>]')
  }
  const input = readJsonFile<LooseInput>(inputPath)
  const panels = resolvePanels(input)
  if (!panels.length) {
    throw new Error('输入中没有可解析的 panels/clips/storyboard')
  }
  const picked = pickPanel(panels, args)
  writeJsonMaybe(picked, outputPath)
}
