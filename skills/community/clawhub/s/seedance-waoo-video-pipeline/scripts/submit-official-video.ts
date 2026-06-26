import { canonicalVendor, getStringArg, getVideoConfig, loadSkillConfig, parseArgs, readJsonFile, resolveImageInput, trimSlash, writeJsonMaybe } from './_shared'
import type { ResolvedPanelContext } from './get-panel-context'
import { validatePanelOrder } from './guard-panel-order'

type SubmitResult = {
  厂商: string
  模型名: string
  taskId: string
  status: 'queued'
  isProbe: boolean
  原始响应?: unknown
  guard?: ReturnType<typeof validatePanelOrder>
}

async function submitMinimaxVideo(baseUrl: string, apiKey: string, model: string, panel: ResolvedPanelContext, duration: number, resolution: string, isProbe: boolean): Promise<SubmitResult> {
  const url = `${trimSlash(baseUrl)}/video_generation`
  const firstFrame = resolveImageInput(panel.imageUrl)
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model,
      prompt: panel.videoPrompt,
      prompt_optimizer: true,
      first_frame_image: firstFrame,
      resolution,
      duration,
    }),
  })
  const data = await res.json()
  if (!res.ok || data?.base_resp?.status_code !== 0 || !data?.task_id) {
    throw new Error(`MiniMax 视频提交失败: ${JSON.stringify(data)}`)
  }
  return {
    厂商: 'MiniMax',
    模型名: model,
    taskId: String(data.task_id),
    status: 'queued',
    isProbe,
    原始响应: data,
  }
}

if (require.main === module) {
  const args = parseArgs(process.argv.slice(2))
  const configPath = getStringArg(args, 'config') || undefined
  const panelPath = getStringArg(args, 'panel')
  const duration = Number(getStringArg(args, 'duration', '6'))
  const resolution = getStringArg(args, 'resolution', '768P')
  const outputPath = getStringArg(args, 'out') || undefined
  const isProbe = args['probe'] === true
  const requireImageApproval = args['require-image-approval'] === true

  if (!panelPath) {
    throw new Error('用法: tsx submit-official-video.ts --config <json> --panel <panel-context.json> [--duration 6] [--resolution 768P] [--probe] [--require-image-approval] [--out <json>]')
  }

  const panel = readJsonFile<ResolvedPanelContext>(panelPath)
  const config = loadSkillConfig(configPath)
  const stage = getVideoConfig(config)
  if (!stage?.厂商 || !stage?.接口地址 || !stage?.模型名 || !stage?.APIKey) {
    throw new Error('视频配置不完整，请先补齐 厂商 / 接口地址 / 模型名 / API Key')
  }

  const guard = validatePanelOrder(
    {
      projectId: panel.projectId,
      episodeId: panel.episodeId,
      panels: [
        {
          panelId: panel.panelId,
          panelIndex: panel.panelIndex,
          imageUrl: panel.imageUrl,
          videoPrompt: panel.videoPrompt,
          subtitleText: panel.subtitleText,
          isMainClip: panel.isMainClip,
        },
      ],
    },
    {
      panelId: panel.panelId,
      panelIndex: panel.panelIndex,
      requireImageApproval,
    },
  )

  if (!guard.ok) {
    throw new Error(`panel guard 校验失败: ${guard.errors.join('；')}`)
  }
  if (guard.needsUserConfirmation) {
    throw new Error(`panel guard 要求先确认: ${guard.warnings.join('；') || '当前目标需要人工确认后再生成'}`)
  }

  const vendor = canonicalVendor(stage.厂商)
  const promise = vendor === 'minimax'
    ? submitMinimaxVideo(stage.接口地址, stage.APIKey, stage.模型名, panel, duration, resolution, isProbe)
    : Promise.reject(new Error(`暂不支持的官方视频厂商: ${stage.厂商}`))

  promise.then((result) => writeJsonMaybe({ ...result, guard }, outputPath)).catch((error) => {
    console.error(error)
    process.exit(1)
  })
}
