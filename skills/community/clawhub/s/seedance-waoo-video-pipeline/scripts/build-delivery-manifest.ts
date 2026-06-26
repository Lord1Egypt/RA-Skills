import { getRuntimeConfig, getStringArg, loadSkillConfig, parseArgs, probeMediaFile, resolveFfprobeBinary, writeJsonMaybe } from './_shared'

type DeliveryManifest = {
  rawVideo: string
  subtitledVideo: string
  subtitleTtsVideo: string
  finalVideo: string
  status: 'partial' | 'final'
  formal: boolean
  notes: string[]
  probes?: {
    rawVideo?: ReturnType<typeof probeMediaFile>
    subtitledVideo?: ReturnType<typeof probeMediaFile>
    subtitleTtsVideo?: ReturnType<typeof probeMediaFile>
    finalVideo?: ReturnType<typeof probeMediaFile>
  }
}

if (require.main === module) {
  const args = parseArgs(process.argv.slice(2))
  const configPath = getStringArg(args, 'config') || undefined
  const config = loadSkillConfig(configPath)
  const runtime = getRuntimeConfig(config)
  const rawVideo = getStringArg(args, 'raw')
  const subtitledVideo = getStringArg(args, 'subtitled')
  const subtitleTtsVideo = getStringArg(args, 'tts-video')
  const finalVideo = getStringArg(args, 'final')
  const outputPath = getStringArg(args, 'out') || undefined
  const note = getStringArg(args, 'note')
  const status = (getStringArg(args, 'status', 'partial') as 'partial' | 'final')
  const formal = getStringArg(args, 'formal', 'true') !== 'false'
  const includeProbe = getStringArg(args, 'with-probe', 'true') !== 'false'
  const ffprobe = resolveFfprobeBinary(getStringArg(args, 'ffprobe'), runtime?.ffprobe)

  const manifest: DeliveryManifest = {
    rawVideo,
    subtitledVideo,
    subtitleTtsVideo,
    finalVideo,
    status,
    formal,
    notes: note ? [note] : [],
  }

  if (includeProbe) {
    const probes: DeliveryManifest['probes'] = {}
    if (rawVideo) probes.rawVideo = probeMediaFile(rawVideo, ffprobe)
    if (subtitledVideo) probes.subtitledVideo = probeMediaFile(subtitledVideo, ffprobe)
    if (subtitleTtsVideo) probes.subtitleTtsVideo = probeMediaFile(subtitleTtsVideo, ffprobe)
    if (finalVideo) probes.finalVideo = probeMediaFile(finalVideo, ffprobe)
    manifest.probes = probes
  }

  writeJsonMaybe(manifest, outputPath)
}
