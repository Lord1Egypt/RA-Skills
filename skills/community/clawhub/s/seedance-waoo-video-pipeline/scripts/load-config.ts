import fs from 'node:fs'
import path from 'node:path'

export type StageConfig = {
  厂商?: string
  接口地址?: string
  模型名?: string
  APIKey?: string
}

export type AmbienceConfig = StageConfig & {
  优先本地环境音素材?: boolean
}

export type AsrConfig = StageConfig & {
  资源ID?: string
  appid?: string
  token?: string
  鉴权方式?: string
  语言?: string
  输出分句?: boolean
}

export type RuntimeConfig = {
  时长秒数?: number
  分辨率?: string
  每日Fast视频额度?: number
  单条主视频优先?: boolean
  ffmpeg?: string
  ffprobe?: string
}

export type PipelineUserConfig = {
  upstream?: {
    seedance?: StageConfig
  }
  downstream?: {
    waoo?: {
      image?: StageConfig
      video?: StageConfig
      tts?: StageConfig
      ambience?: AmbienceConfig
      asr?: AsrConfig
      asrs?: Record<string, AsrConfig>
    }
  }
  runtime?: RuntimeConfig
}

export const DEFAULT_CONFIG_PATH = path.resolve(__dirname, '..', 'config', 'pipeline.config.json')

export function loadConfig(configPath: string = DEFAULT_CONFIG_PATH): PipelineUserConfig {
  if (!fs.existsSync(configPath)) {
    return {}
  }

  const raw = fs.readFileSync(configPath, 'utf8').trim()
  if (!raw) {
    return {}
  }

  return JSON.parse(raw) as PipelineUserConfig
}

export function saveConfig(config: PipelineUserConfig, configPath: string = DEFAULT_CONFIG_PATH) {
  fs.mkdirSync(path.dirname(configPath), { recursive: true })
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf8')
}

if (require.main === module) {
  const configPath = process.argv[2] || DEFAULT_CONFIG_PATH
  const config = loadConfig(configPath)
  console.log(JSON.stringify({ configPath, config }, null, 2))
}
