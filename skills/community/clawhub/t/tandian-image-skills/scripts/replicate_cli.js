#!/usr/bin/env node
/*
Simple CLI script to call Replicate for gpt-image-2 edit + SeedVR2 upscale,
save the final HD image to disk.

Usage:
  REPLICATE_API_TOKEN=... node scripts/replicate_cli.js --image test/input/1.png --out test/output/1.webp
  REPLICATE_API_TOKEN=... node scripts/replicate_cli.js --image test/input/1.png --templatePreset lucy --out test/output/1.webp --prompt "..."

*/
const fs = require('node:fs/promises')
const path = require('node:path')
const { PRESET_ROLE_TEMPLATES } = require('./role_templates')

const POLL_INTERVAL = 1500
const POLL_TIMEOUT = 90_000
const ALLOWED_ASPECT_RATIOS = ['1:1', '2:3', '3:2']
const DEFAULT_PROMPT = '生成一个探店打卡照片，要求：提取图1中的美女人物角色，她的姿势可以随意自由变化，站姿或者坐姿都可以，放入场景参考图2中，图2里的场景保持不变，不要漏出手指，远景镜头，去除无关水印，iphone 手机拍摄质感。'

function usage() {
  console.log('Usage: REPLICATE_API_TOKEN=... node scripts/replicate_cli.js --image test/input/1.png --out test/output/1.webp [--templatePreset lucy] [--templateUrl https://...] [--aspect 2:3] [--prompt "..."]')
}

function parseArgs() {
  const args = process.argv.slice(2)
  const res = {}
  for (let i = 0; i < args.length; i++) {
    const a = args[i]
    if (a.startsWith('--')) {
      const key = a.slice(2)
      const val = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : 'true'
      res[key] = val
    }
  }
  return res
}

function isRemoteUrl(input) {
  return input.startsWith('http://') || input.startsWith('https://')
}

function getMimeType(filePathOrUrl) {
  const ext = path.extname(filePathOrUrl).toLowerCase()
  if (ext === '.webp') return 'image/webp'
  if (ext === '.jpg' || ext === '.jpeg') return 'image/jpeg'
  return 'image/png'
}

function getPresetTemplateEntries() {
  const entries = Object.entries(PRESET_ROLE_TEMPLATES).filter(([, url]) => typeof url === 'string' && isRemoteUrl(url))
  if (entries.length === 0) {
    throw new Error('No preset role templates configured')
  }
  return entries
}

function pickRandomItem(items) {
  return items[Math.floor(Math.random() * items.length)]
}

function normalizePresetKey(rawKey) {
  const lower = rawKey.toLowerCase().trim()
  return lower.endsWith('.png') || lower.endsWith('.jpg') || lower.endsWith('.jpeg') || lower.endsWith('.webp')
    ? lower.slice(0, lower.lastIndexOf('.'))
    : lower
}

function resolveTemplateSource(args) {
  if (args.templateUrl) {
    if (!isRemoteUrl(args.templateUrl)) {
      throw new Error(`templateUrl must be an http/https URL: ${args.templateUrl}`)
    }
    return { url: args.templateUrl, label: args.templateUrl, source: 'user-url' }
  }

  const presetEntries = getPresetTemplateEntries()
  const requestedPreset = args.templatePreset || args.template
  if (requestedPreset) {
    const key = normalizePresetKey(requestedPreset)
    const selected = PRESET_ROLE_TEMPLATES[key]
    if (!selected) {
      throw new Error(`Template preset not found: ${requestedPreset}. Available presets: ${presetEntries.map(([name]) => name).join(', ')}`)
    }
    return { url: selected, label: `preset:${key}`, source: 'preset' }
  }

  const [randomKey, randomUrl] = pickRandomItem(presetEntries)
  return { url: randomUrl, label: `preset:${randomKey}`, source: 'preset-random' }
}

async function fileOrUrlToDataUrl(input) {
  if (!input) throw new Error('no input')
  try {
    if (isRemoteUrl(input)) {
      const resp = await fetch(input)
      if (!resp.ok) throw new Error(`Failed to fetch template: ${resp.status}`)
      const ab = await resp.arrayBuffer()
      const b64 = Buffer.from(ab).toString('base64')
      const mime = resp.headers.get('content-type') || 'image/png'
      return `data:${mime};base64,${b64}`
    } else {
      const abs = path.resolve(process.cwd(), input)
      const buf = await fs.readFile(abs)
      const mime = getMimeType(abs)
      return `data:${mime};base64,${buf.toString('base64')}`
    }
  } catch (err) {
    throw err
  }
}

async function createPrediction(token, userImage, templateImage, aspectRatio, prompt) {
  const input = {
    aspect_ratio: aspectRatio,
    background: 'auto',
    input_images: [templateImage, userImage],
    moderation: 'auto',
    number_of_images: 1,
    output_compression: 90,
    output_format: 'webp',
    prompt: prompt || DEFAULT_PROMPT,
    quality: 'low',
  }

  const res = await fetch('https://api.replicate.com/v1/models/openai/gpt-image-2/predictions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ input }),
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Replicate create failed: ${res.status} ${text}`)
  }
  return res.json()
}

async function getPrediction(id, token) {
  const res = await fetch(`https://api.replicate.com/v1/predictions/${id}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Replicate get failed: ${res.status} ${text}`)
  }
  return res.json()
}

async function createUpscalePrediction(token, mediaUrl) {
  const res = await fetch('https://api.replicate.com/v1/predictions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({
      version: 'ca98249be9cb623f02a80a7851a2b1a33d5104c251a8f5a1588f251f79bf7c78',
      input: {
        media: mediaUrl,
        fps: 24,
        sp_size: 1,
        cfg_scale: 1,
        sample_steps: 1,
        model_variant: '3b',
        output_format: 'webp',
        output_quality: 90,
        apply_color_fix: true,
      },
    }),
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`SeedVR2 create failed: ${res.status} ${text}`)
  }
  return res.json()
}

async function downloadToFile(url, outPath) {
  const resp = await fetch(url)
  if (!resp.ok) throw new Error(`Failed downloading output: ${resp.status}`)
  const ab = await resp.arrayBuffer()
  await fs.mkdir(path.dirname(outPath), { recursive: true })
  await fs.writeFile(outPath, Buffer.from(ab))
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

async function main() {
  const args = parseArgs()
  if (!args.image || !args.out) {
    usage()
    process.exit(1)
  }
  const token = process.env.REPLICATE_API_TOKEN
  if (!token) {
    console.error('Missing REPLICATE_API_TOKEN in environment')
    process.exit(2)
  }
  const aspect = args.aspect || '2:3'
  if (!ALLOWED_ASPECT_RATIOS.includes(aspect)) {
    console.error('Invalid aspect ratio')
    process.exit(1)
  }

  try {
    const userImage = await fileOrUrlToDataUrl(args.image)
    const selectedTemplate = resolveTemplateSource(args)
    const templateImage = await fileOrUrlToDataUrl(selectedTemplate.url)

    console.log('Using role template:', selectedTemplate.label)

    const pred = await createPrediction(token, userImage, templateImage, aspect, args.prompt || '')
    const start = Date.now()
    let finalUrl = null
    while (true) {
      const status = await getPrediction(pred.id, token)
      if (status.status === 'succeeded') {
        const output = Array.isArray(status.output) ? status.output[0] : status.output
        if (!output) throw new Error('Invalid output from replicate')
        const up = await createUpscalePrediction(token, output)
        const upStart = Date.now()
        while (true) {
          const upStatus = await getPrediction(up.id, token)
          if (upStatus.status === 'succeeded') {
            const hd = Array.isArray(upStatus.output) ? upStatus.output[0] : upStatus.output
            finalUrl = hd
            break
          }
          if (upStatus.status === 'failed') throw new Error(upStatus.error || 'SeedVR2 failed')
          if (Date.now() - upStart > POLL_TIMEOUT) throw new Error('Timeout waiting for SeedVR2')
          await sleep(POLL_INTERVAL)
        }
        break
      }
      if (status.status === 'failed') throw new Error(status.error || 'Replicate failed')
      if (Date.now() - start > POLL_TIMEOUT) throw new Error('Timeout waiting for prediction')
      await sleep(POLL_INTERVAL)
    }

    if (!finalUrl) throw new Error('No final url')
    await downloadToFile(finalUrl, path.resolve(process.cwd(), args.out))
    console.log('Saved output to', args.out)
  } catch (err) {
    console.error('Error:', err?.message || String(err))
    process.exit(3)
  }
}

if (process.argv[1] && process.argv[1].endsWith('replicate_cli.js')) {
  main()
}
