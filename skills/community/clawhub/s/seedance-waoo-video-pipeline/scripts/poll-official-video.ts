import { canonicalVendor, getStringArg, getVideoConfig, loadSkillConfig, parseArgs, trimSlash, writeJsonMaybe } from './_shared'

type PollResult = {
  taskId: string
  status: 'queued' | 'processing' | 'success' | 'fail'
  fileId: string
  downloadUrl: string
  isProbe: boolean
  原始响应?: unknown
}

function mapMinimaxStatus(value: string): PollResult['status'] {
  const status = (value || '').toLowerCase()
  if (status === 'success') return 'success'
  if (status === 'fail' || status === 'failed') return 'fail'
  if (status === 'preparing' || status === 'queue' || status === 'queued') return 'queued'
  return 'processing'
}

async function pollMinimaxVideo(baseUrl: string, apiKey: string, taskId: string, isProbe: boolean): Promise<PollResult> {
  const url = `${trimSlash(baseUrl)}/query/video_generation?task_id=${encodeURIComponent(taskId)}`
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${apiKey}` },
  })
  const data = await res.json()
  if (!res.ok || data?.base_resp?.status_code !== 0) {
    throw new Error(`MiniMax 视频查询失败: ${JSON.stringify(data)}`)
  }
  return {
    taskId,
    status: mapMinimaxStatus(String(data?.status || '')),
    fileId: String(data?.file_id || ''),
    downloadUrl: '',
    isProbe,
    原始响应: data,
  }
}

if (require.main === module) {
  const args = parseArgs(process.argv.slice(2))
  const configPath = getStringArg(args, 'config') || undefined
  const taskId = getStringArg(args, 'task-id')
  const outputPath = getStringArg(args, 'out') || undefined
  const isProbe = args['probe'] === true
  if (!taskId) {
    throw new Error('用法: tsx poll-official-video.ts --config <json> --task-id <id> [--probe] [--out <json>]')
  }
  const config = loadSkillConfig(configPath)
  const stage = getVideoConfig(config)
  if (!stage?.厂商 || !stage?.接口地址 || !stage?.模型名 || !stage?.APIKey) {
    throw new Error('视频配置不完整，请先补齐 厂商 / 接口地址 / 模型名 / API Key')
  }
  const vendor = canonicalVendor(stage.厂商)
  const promise = vendor === 'minimax'
    ? pollMinimaxVideo(stage.接口地址, stage.APIKey, taskId, isProbe)
    : Promise.reject(new Error(`暂不支持的官方视频厂商: ${stage.厂商}`))

  promise.then((result) => writeJsonMaybe(result, outputPath)).catch((error) => {
    console.error(error)
    process.exit(1)
  })
}
