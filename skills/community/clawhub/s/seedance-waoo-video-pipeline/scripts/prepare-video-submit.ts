import { getStringArg, parseArgs, readJsonFile, writeJsonMaybe } from './_shared'
import { validatePanelOrder } from './guard-panel-order'
import { buildGuardCheckpoint } from './guard-checkpoint'
import type { ResolvedPanelContext } from './get-panel-context'

type PrepareSubmitResult = {
  ok: boolean
  ready: boolean
  panel: ResolvedPanelContext
  guard: ReturnType<typeof validatePanelOrder>
  checkpoint: ReturnType<typeof buildGuardCheckpoint>
  nextCommand: string
}

if (require.main === module) {
  const args = parseArgs(process.argv.slice(2))
  const panelPath = getStringArg(args, 'panel')
  const outputPath = getStringArg(args, 'out') || undefined
  const configPath = getStringArg(args, 'config')
  const duration = getStringArg(args, 'duration', '6')
  const resolution = getStringArg(args, 'resolution', '768P')
  const requireImageApproval = args['require-image-approval'] === true

  if (!panelPath) {
    throw new Error('用法: tsx prepare-video-submit.ts --panel <panel-context.json> [--config <json>] [--duration 6] [--resolution 768P] [--require-image-approval] [--out <json>]')
  }

  const panel = readJsonFile<ResolvedPanelContext>(panelPath)
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
  const checkpoint = buildGuardCheckpoint('panel-guard', guard.errors, guard.warnings)

  const nextCommand = [
    'tsx scripts/submit-official-video.ts',
    configPath ? `--config ${configPath}` : '',
    `--panel ${panelPath}`,
    `--duration ${duration}`,
    `--resolution ${resolution}`,
    requireImageApproval ? '--require-image-approval' : '',
  ].filter(Boolean).join(' ')

  const result: PrepareSubmitResult = {
    ok: guard.ok,
    ready: guard.ok && !guard.needsUserConfirmation,
    panel,
    guard,
    checkpoint,
    nextCommand,
  }

  writeJsonMaybe(result, outputPath)
  if (!result.ok) process.exit(2)
}
