import path from 'node:path'
import { canonicalVendor, ensureTtsReady, fetchBinaryToFile, getStringArg, getTtsConfig, loadSkillConfig, parseArgs, StructuredConfigError, trimSlash, writeJsonMaybe } from './_shared'

type TtsResult = {
  厂商: string
  模型名: string
  输出文件: string
  字节数?: number
  使用音色?: string
  原始响应?: unknown
}

type MinimaxVoiceOptions = {
  voiceId: string
  speed: number
  pitch: number
  volume: number
}

function resolveMinimaxVoiceOptions(args: Record<string, string | boolean>): MinimaxVoiceOptions {
  return {
    voiceId: getStringArg(args, 'voice-id', 'male-qn-qingse'),
    speed: Number(getStringArg(args, 'speed', '1')),
    pitch: Number(getStringArg(args, 'pitch', '0')),
    volume: Number(getStringArg(args, 'volume', '1')),
  }
}

async function generateMinimaxTts(baseUrl: string, apiKey: string, model: string, text: string, outputPath: string, voice: MinimaxVoiceOptions): Promise<TtsResult> {
  const url = `${trimSlash(baseUrl)}/t2a_v2`
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model,
      text,
      stream: false,
      voice_setting: { voice_id: voice.voiceId, speed: voice.speed, vol: voice.volume, pitch: voice.pitch },
      audio_setting: { sample_rate: 32000, bitrate: 128000, format: 'mp3', channel: 1 },
      output_format: 'url',
      subtitle_enable: true,
    }),
  })
  const data = await res.json()
  if (!res.ok || data?.base_resp?.status_code !== 0 || !data?.data?.audio) {
    throw new Error(`MiniMax TTS 失败: ${JSON.stringify(data)}`)
  }
  const saved = await fetchBinaryToFile(data.data.audio, outputPath)
  return {
    厂商: 'MiniMax',
    模型名: model,
    输出文件: saved.outputPath,
    字节数: saved.bytes,
    使用音色: voice.voiceId,
    原始响应: { subtitle_file: data?.data?.subtitle_file ?? null },
  }
}

async function generateOpenAiCompatibleTts(baseUrl: string, apiKey: string, model: string, text: string, outputPath: string, voiceName: string): Promise<TtsResult> {
  const url = `${trimSlash(baseUrl)}/audio/speech`
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ model, input: text, voice: voiceName || 'alloy' }),
  })

  if (!res.ok) {
    throw new Error(`OpenAI-compatible TTS 失败: ${res.status} ${await res.text()}`)
  }

  const contentType = res.headers.get('content-type') || ''
  if (contentType.includes('application/json')) {
    const data = await res.json()
    if (data?.audio_url) {
      const saved = await fetchBinaryToFile(data.audio_url, outputPath)
      return {
        厂商: 'OpenAI-compatible',
        模型名: model,
        输出文件: saved.outputPath,
        字节数: saved.bytes,
        使用音色: voiceName || 'alloy',
        原始响应: data,
      }
    }
    throw new Error(`OpenAI-compatible TTS 返回 JSON 但未提供可下载音频: ${JSON.stringify(data)}`)
  }

  const buffer = Buffer.from(await res.arrayBuffer())
  const fs = await import('node:fs')
  fs.mkdirSync(path.dirname(path.resolve(outputPath)), { recursive: true })
  fs.writeFileSync(outputPath, buffer)
  return {
    厂商: 'OpenAI-compatible',
    模型名: model,
    输出文件: path.resolve(outputPath),
    字节数: buffer.length,
    使用音色: voiceName || 'alloy',
  }
}

if (require.main === module) {
  const args = parseArgs(process.argv.slice(2))
  const configPath = getStringArg(args, 'config') || undefined
  const text = getStringArg(args, 'text')
  const outputPath = getStringArg(args, 'out')
  const resultJsonPath = getStringArg(args, 'result-json') || undefined

  try {
    if (!text || !outputPath) {
      throw new Error('用法: tsx generate-tts.ts --config <json> --text <文本> --out <mp3路径> [--result-json <json>] [--voice-id <音色>] [--speed 1] [--pitch 0] [--volume 1]')
    }

    const config = loadSkillConfig(configPath)
    ensureTtsReady(config)
    const stage = getTtsConfig(config)
    if (!stage) {
      throw new Error('TTS 配置不存在')
    }

    const vendor = canonicalVendor(stage.厂商)
    const minimaxVoice = resolveMinimaxVoiceOptions(args)
    const openAiVoice = getStringArg(args, 'voice-id', 'alloy')
    const promise = vendor === 'minimax'
      ? generateMinimaxTts(stage.接口地址, stage.APIKey, stage.模型名, text, outputPath, minimaxVoice)
      : vendor === 'openai' || vendor === 'openai-compatible'
        ? generateOpenAiCompatibleTts(stage.接口地址, stage.APIKey, stage.模型名, text, outputPath, openAiVoice)
        : Promise.reject(new Error(`暂不支持的 TTS 厂商: ${stage.厂商}`))

    promise.then((result) => writeJsonMaybe(result, resultJsonPath)).catch((error) => {
      if (error instanceof StructuredConfigError) {
        writeJsonMaybe({ ok: false, ...error.hint }, resultJsonPath)
        process.exit(2)
        return
      }
      console.error(error)
      process.exit(1)
    })
  } catch (error) {
    if (error instanceof StructuredConfigError) {
      writeJsonMaybe({ ok: false, ...error.hint }, resultJsonPath)
      process.exit(2)
    }
    console.error(error)
    process.exit(1)
  }
}
