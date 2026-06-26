import { getStringArg, parseArgs, readJsonFile, writeJsonMaybe } from './_shared'
import { validatePanelOrder, type GuardResult } from './guard-panel-order'

type LooseInput = {
  projectId?: string
  episodeId?: string
  panels?: any[]
  clips?: any[]
  storyboard?: any[]
}

export type MergeGuardResult = GuardResult & {
  selectedPanelIndexes: number[]
  allowSelectiveCut: boolean
}

export function validateMergeOrder(input: LooseInput, selectedPanelIndexes: number[] = [], allowSelectiveCut = false): MergeGuardResult {
  const base = validatePanelOrder(input)
  const errors = [...base.errors]
  const warnings = [...base.warnings]

  if (selectedPanelIndexes.length > 1) {
    const sorted = [...selectedPanelIndexes].sort((a, b) => a - b)
    for (let i = 1; i < sorted.length; i += 1) {
      if (sorted[i] === sorted[i - 1]) {
        errors.push(`merge 输入存在重复 panelIndex=${sorted[i]}`)
      }
      if (!allowSelectiveCut && sorted[i] > sorted[i - 1] + 1) {
        warnings.push(`merge 顺序存在跳帧: ${sorted[i - 1]} -> ${sorted[i]}`)
      }
    }
  }

  return {
    ...base,
    ok: errors.length === 0,
    warnings,
    errors,
    needsUserConfirmation: base.needsUserConfirmation || warnings.length > 0,
    selectedPanelIndexes,
    allowSelectiveCut,
  }
}

if (require.main === module) {
  const args = parseArgs(process.argv.slice(2))
  const inputPath = getStringArg(args, 'input')
  const outputPath = getStringArg(args, 'out') || undefined
  const panelIndexesRaw = getStringArg(args, 'panel-indexes')
  const allowSelectiveCut = getStringArg(args, 'allow-selective-cut', 'false') === 'true'

  if (!inputPath) {
    throw new Error('用法: tsx guard-merge-order.ts --input <json> [--panel-indexes 0,1,2] [--allow-selective-cut true|false] [--out <json>]')
  }

  const input = readJsonFile<LooseInput>(inputPath)
  const selectedPanelIndexes = panelIndexesRaw
    ? panelIndexesRaw.split(',').map((item) => Number(item.trim())).filter((item) => Number.isFinite(item))
    : []
  const result = validateMergeOrder(input, selectedPanelIndexes, allowSelectiveCut)

  writeJsonMaybe(result, outputPath)
  if (!result.ok) process.exit(2)
}
