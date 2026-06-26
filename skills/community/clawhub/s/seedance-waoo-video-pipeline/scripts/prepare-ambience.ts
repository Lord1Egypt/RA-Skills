import fs from 'node:fs'
import path from 'node:path'
import { ensureAmbienceReady, getStringArg, loadSkillConfig, parseArgs, StructuredConfigError, writeJsonMaybe } from './_shared'

type AmbienceResult = {
  mode: 'local' | 'none' | 'ai-pending'
  ambienceAudio: string
  found: boolean
  notes: string[]
}

function firstExisting(paths: string[]): string {
  for (const item of paths) {
    const full = path.resolve(item)
    if (fs.existsSync(full)) return full
  }
  return ''
}

if (require.main === module) {
  try {
    const args = parseArgs(process.argv.slice(2))
    const preferred = getStringArg(args, 'preferred')
    const fallbackDir = getStringArg(args, 'dir')
    const outputPath = getStringArg(args, 'out') || undefined
    const mode = getStringArg(args, 'mode', 'local').trim().toLowerCase()

    if (mode === 'ai') {
      const configPath = getStringArg(args, 'config') || undefined
      const config = loadSkillConfig(configPath)
      ensureAmbienceReady(config, false)
      const result: AmbienceResult = {
        mode: 'ai-pending',
        ambienceAudio: '',
        found: false,
        notes: ['AI 环境音配置检查通过；当前脚本仅负责检查与本地素材选择，AI 生成由后续步骤执行。'],
      }
      writeJsonMaybe(result, outputPath)
      process.exit(0)
    }

    const candidates = [preferred]
    if (fallbackDir) {
      candidates.push(
        path.join(fallbackDir, 'snow-ambience.mp3'),
        path.join(fallbackDir, 'wind-snow.mp3'),
        path.join(fallbackDir, 'snowstorm.mp3'),
      )
    }
    const found = firstExisting(candidates.filter(Boolean))
    const result: AmbienceResult = found
      ? { mode: 'local', ambienceAudio: found, found: true, notes: ['使用本地环境音'] }
      : { mode: 'none', ambienceAudio: '', found: false, notes: ['未找到本地环境音，需走后续 AI fallback'] }

    writeJsonMaybe(result, outputPath)
  } catch (error) {
    if (error instanceof StructuredConfigError) {
      const args = parseArgs(process.argv.slice(2))
      const outputPath = getStringArg(args, 'out') || undefined
      writeJsonMaybe({ ok: false, ...error.hint }, outputPath)
      process.exit(2)
    }
    console.error(error)
    process.exit(1)
  }
}
