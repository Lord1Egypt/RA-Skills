import { ensureAsrReady, getStringArg, loadSkillConfig, parseArgs, StructuredConfigError, writeJsonMaybe } from './_shared'

if (require.main === module) {
  const args = parseArgs(process.argv.slice(2))
  const configPath = getStringArg(args, 'config') || undefined
  const outputPath = getStringArg(args, 'out') || undefined

  try {
    const config = loadSkillConfig(configPath)
    ensureAsrReady(config)
    writeJsonMaybe({
      ok: true,
      type: 'configuration-guidance',
      feature: 'asr',
      message: 'ASR 配置检查通过，可以继续执行自动语音识别。',
      missing: [],
      choices: [],
    }, outputPath)
  } catch (error) {
    if (error instanceof StructuredConfigError) {
      writeJsonMaybe({ ok: false, ...error.hint }, outputPath)
      process.exit(2)
    }
    console.error(error)
    process.exit(1)
  }
}
