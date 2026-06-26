import { canonicalVendor, fetchBinaryToFile, getStringArg, getVideoConfig, loadSkillConfig, parseArgs, trimSlash, writeJsonMaybe } from './_shared'

type DownloadResult = {
  taskId: string
  fileId: string
  status: 'success'
  downloadUrl: string
  outputFile: string
  bytes: number
  isProbe: boolean
  原始响应?: unknown
}

async function downloadMinimaxVideo(baseUrl: string, apiKey: string, taskId: string, fileId: string, outputPath: string, isProbe: boolean): Promise<DownloadResult> {
  if (!fileId) throw new Error('缺少 fileId')
  const url = `${trimSlash(baseUrl)}/files/retrieve?file_id=${encodeURIComponent(fileId)}`
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${apiKey}` },
  })
  const data = await res.json()
  const downloadUrl = String(data?.file?.download_url || data?.download_url || '')
  if (!res.ok || data?.base_resp?.status_code !== 0 || !downloadUrl) {
    throw new Error(`MiniMax 文件获取失败: ${JSON.stringify(data)}`)
  }
  const saved = await fetchBinaryToFile(downloadUrl, outputPath)
  return {
    taskId,
    fileId,
    status: 'success',
    downloadUrl,
    outputFile: saved.outputPath,
    bytes: saved.bytes,
    isProbe,
    原始响应: data,
  }
}

if (require.main === module) {
  const args = parseArgs(process.argv.slice(2))
  const configPath = getStringArg(args, 'config') || undefined
  const taskId = getStringArg(args, 'task-id')
  const fileId = getStringArg(args, 'file-id')
  const outputPath = getStringArg(args, 'out')
  const resultJsonPath = getStringArg(args, 'result-json') || undefined
  const isProbe = args['probe'] === true
  if (!taskId || !fileId || !outputPath) {
    throw new Error('用法: tsx download-official-video.ts --config <json> --task-id <id> --file-id <fileId> --out <mp4路径> [--result-json <json>] [--probe]')
  }
  const config = loadSkillConfig(configPath)
  const stage = getVideoConfig(config)
  if (!stage?.厂商 || !stage?.接口地址 || !stage?.模型名 || !stage?.APIKey) {
    throw new Error('视频配置不完整，请先补齐 厂商 / 接口地址 / 模型名 / API Key')
  }
  const vendor = canonicalVendor(stage.厂商)
  const promise = vendor === 'minimax'
    ? downloadMinimaxVideo(stage.接口地址, stage.APIKey, taskId, fileId, outputPath, isProbe)
    : Promise.reject(new Error(`暂不支持的官方视频厂商: ${stage.厂商}`))

  promise.then((result) => writeJsonMaybe(result, resultJsonPath)).catch((error) => {
    console.error(error)
    process.exit(1)
  })
}
