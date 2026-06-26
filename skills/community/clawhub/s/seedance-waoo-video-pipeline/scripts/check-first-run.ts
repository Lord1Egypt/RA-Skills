import { loadConfig, DEFAULT_CONFIG_PATH, type PipelineUserConfig, type StageConfig } from './load-config'
import { checkFfmpegPrerequisites, getRuntimeConfig } from './_shared'

type MissingItem = {
  阶段: string
  缺少: string[]
}

function missingFields(stage: StageConfig | undefined, requireApiKey: boolean = true): string[] {
  const fields: string[] = []
  if (!stage?.厂商) fields.push('厂商')
  if (!stage?.接口地址) fields.push('接口地址')
  if (!stage?.模型名) fields.push('模型名')
  if (requireApiKey && !stage?.APIKey) fields.push('API Key')
  return fields
}

export function checkFirstRun(config: PipelineUserConfig): MissingItem[] {
  const result: MissingItem[] = []

  const upstream = config.upstream?.seedance
  const image = config.downstream?.waoo?.image
  const video = config.downstream?.waoo?.video
  const tts = config.downstream?.waoo?.tts
  const ambience = config.downstream?.waoo?.ambience

  const upstreamMissing = missingFields(upstream)
  if (upstreamMissing.length) result.push({ 阶段: '上游 Seedance', 缺少: upstreamMissing })

  const videoMissing = missingFields(video)
  if (videoMissing.length) result.push({ 阶段: '下游 waoowaoo 视频', 缺少: videoMissing })

  const ttsMissing = missingFields(tts)
  if (ttsMissing.length) result.push({ 阶段: '下游 waoowaoo 配音', 缺少: ttsMissing })

  if (image && missingFields(image).length) {
    result.push({ 阶段: '下游 waoowaoo 图片', 缺少: missingFields(image) })
  }

  const preferLocal = ambience?.优先本地环境音素材 === true
  if (!preferLocal) {
    const ambienceMissing = missingFields(ambience)
    if (ambienceMissing.length) result.push({ 阶段: '下游 waoowaoo 环境音', 缺少: ambienceMissing })
  }

  try {
    checkFfmpegPrerequisites(getRuntimeConfig(config))
  } catch {
    result.push({ 阶段: '本地媒体工具', 缺少: ['ffmpeg', 'ffprobe'] })
  }

  return result
}

export function buildFirstRunMessage(config: PipelineUserConfig): string {
  const missing = checkFirstRun(config)
  if (!missing.length) {
    return '配置已满足最小运行要求。'
  }

  const lines = ['首次运行还缺这些配置/前置条件：']
  for (const item of missing) {
    lines.push(`- ${item.阶段}：${item.缺少.join(' / ')}`)
  }
  lines.push('请按“厂商 / 接口地址 / 模型名 / API Key”补齐；如需本地混音/拼接，还必须先准备 ffmpeg 与 ffprobe。')
  return lines.join('\n')
}

if (require.main === module) {
  const configPath = process.argv[2] || DEFAULT_CONFIG_PATH
  const config = loadConfig(configPath)
  console.log(buildFirstRunMessage(config))
}
