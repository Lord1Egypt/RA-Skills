import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'
import {
  ensureDirForFile,
  getRuntimeConfig,
  getStringArg,
  loadSkillConfig,
  parseArgs,
  probeMediaFile,
  resolveFfmpegBinary,
  resolveFfprobeBinary,
  writeJsonMaybe,
} from './_shared'
import { validateMergeOrder } from './guard-merge-order'
import { buildGuardCheckpoint } from './guard-checkpoint'

type MergeResult = {
  mergedVideo: string
  ffmpeg: string
  ffprobe: string
  inputs: string[]
  panelIndexes: number[]
  guard: ReturnType<typeof validateMergeOrder>
  checkpoint: ReturnType<typeof buildGuardCheckpoint>
  probe: ReturnType<typeof probeMediaFile>
}

if (require.main === module) {
  const args = parseArgs(process.argv.slice(2))
  const configPath = getStringArg(args, 'config') || undefined
  const storyboardPath = getStringArg(args, 'storyboard')
  const inputsRaw = getStringArg(args, 'inputs')
  const panelIndexesRaw = getStringArg(args, 'panel-indexes')
  const outputPath = getStringArg(args, 'out')
  const resultJsonPath = getStringArg(args, 'result-json') || undefined
  const allowSelectiveCut = getStringArg(args, 'allow-selective-cut', 'false') === 'true'
  const assumeConfirmed = getStringArg(args, 'assume-confirmed', 'false') === 'true'

  if (!storyboardPath || !inputsRaw || !outputPath) {
    throw new Error('用法: tsx merge-final-videos.ts --config <json> --storyboard <json> --inputs <a.mp4,b.mp4> --panel-indexes <0,1,2> --out <merged.mp4> [--result-json <json>] [--allow-selective-cut true|false] [--assume-confirmed true|false]')
  }

  const config = loadSkillConfig(configPath)
  const runtime = getRuntimeConfig(config)
  const ffmpeg = resolveFfmpegBinary(getStringArg(args, 'ffmpeg'), runtime?.ffmpeg)
  const ffprobe = resolveFfprobeBinary(getStringArg(args, 'ffprobe'), runtime?.ffprobe)
  const storyboard = JSON.parse(fs.readFileSync(path.resolve(storyboardPath), 'utf8'))
  const panelIndexes = panelIndexesRaw.split(',').map((item) => Number(item.trim())).filter((item) => Number.isFinite(item))
  const guard = validateMergeOrder(storyboard, panelIndexes, allowSelectiveCut)
  const checkpoint = buildGuardCheckpoint('merge-guard', guard.errors, guard.warnings)

  if (!guard.ok) {
    throw new Error(`merge guard 校验失败: ${guard.errors.join('；')}`)
  }
  if (guard.needsUserConfirmation && !assumeConfirmed) {
    throw new Error(`merge guard 要求先确认: ${guard.warnings.join('；') || '当前 merge 顺序需要人工确认'}`)
  }

  const inputs = inputsRaw.split(',').map((item) => path.resolve(item.trim())).filter(Boolean)
  if (!inputs.length) {
    throw new Error('缺少 merge 输入视频')
  }
  if (inputs.length !== panelIndexes.length) {
    throw new Error(`merge 输入数量与 panel-indexes 数量不一致: videos=${inputs.length} panelIndexes=${panelIndexes.length}`)
  }

  ensureDirForFile(outputPath)
  const concatListPath = path.resolve(`${outputPath}.concat.txt`)
  const concatContent = inputs.map((item) => `file '${item.replace(/'/g, "'\\''")}'`).join('\n')
  fs.writeFileSync(concatListPath, concatContent, 'utf8')

  execFileSync(ffmpeg, ['-y', '-f', 'concat', '-safe', '0', '-i', concatListPath, '-c', 'copy', path.resolve(outputPath)], { stdio: 'inherit' })

  const probe = probeMediaFile(outputPath, ffprobe)
  const result: MergeResult = {
    mergedVideo: path.resolve(outputPath),
    ffmpeg,
    ffprobe,
    inputs,
    panelIndexes,
    guard,
    checkpoint,
    probe,
  }
  writeJsonMaybe(result, resultJsonPath)
}
