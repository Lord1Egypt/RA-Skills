import type { FastifyPluginAsync } from 'fastify'
import { createReadStream, readFileSync, statSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'
import { botStore } from '../store/botStore.js'

const __dirname = dirname(fileURLToPath(import.meta.url))
const ASSETS_DIR = resolve(__dirname, '../../assets')

/**
 * Certificate issuance logic:
 *   - Bot has 'read_images' capability → visual PNG certificate (luxury card style)
 *   - Otherwise                        → code ASCII certificate (terminal text style)
 */
export function selectCertificateFile(capabilities: string[]): {
  file: string
  type: 'visual' | 'code'
} {
  if (capabilities.includes('read_images')) {
    return { file: 'certificate-visual.png', type: 'visual' }
  }
  return { file: 'certificate-code.png', type: 'code' }
}

/**
 * Generate an ASCII award certificate personalized with bot info.
 * Returned as a plain text string to embed directly in JSON responses.
 */
export function buildCodeAward(opts: {
  botName: string
  ricId: string
  developer: string
  grade: string
  issuedAt: string
}): string[] {
  const { botName, ricId, developer, grade, issuedAt } = opts
  const date = issuedAt.slice(0, 10)
  const border = '✦  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ✦'
  const sep   = '       ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─'
  const pad = (label: string, value: string) =>
    `  ${label.padEnd(5)}›  ${value}`

  return [
    border,
    '         R  ·  I  ·  C     C E R T I F I C A T E',
    sep,
    pad('Bot', botName.padEnd(22) + `Grade  ›  ${grade.toUpperCase()}`),
    pad('ID ', ricId),
    pad('Dev', developer),
    sep,
    '         ◈   Certified Robot Identity — Verified Worldwide   ◈',
    `  ✦  ·  ·  LUMIOI  ·  ${date}  ·  ·  ✦`,
    border,
  ]
}

/**
 * Read the visual PNG template and return as base64 data URI.
 */
export function buildVisualAward(file: string): string {
  const buf = readFileSync(resolve(ASSETS_DIR, file))
  return `data:image/png;base64,${buf.toString('base64')}`
}

export const certificateRoutes: FastifyPluginAsync = async (fastify) => {
  /**
   * GET /v1/bots/:id/certificate
   *
   * Returns the appropriate award certificate PNG for this bot.
   * - read_images capability  → luxury visual certificate
   * - text-only bots          → terminal code certificate
   *
   * Query params:
   *   ?format=image   force PNG stream (default)
   *   ?format=json    return certificate metadata as JSON
   */
  fastify.get('/:id/certificate', async (request, reply) => {
    const { id } = request.params as { id: string }
    const { format } = request.query as { format?: string }

    const cert = botStore.findById(id)
    if (!cert) {
      return reply.status(404).send({ error: 'Bot not found', id })
    }

    const { file, type } = selectCertificateFile(cert.bot.capabilities)
    const filePath = resolve(ASSETS_DIR, file)

    // JSON metadata mode
    if (format === 'json') {
      return reply.send({
        ric_id: cert.id,
        bot_name: cert.bot.name,
        developer: cert.developer.email,
        grade: cert.grade,
        certificate_type: type,
        certificate_url: `/v1/bots/${id}/certificate`,
        issued_at: cert.created_at,
        signed_by: 'LUMIOI',
      })
    }

    // PNG stream mode (default)
    try {
      const stat = statSync(filePath)
      reply.header('Content-Type', 'image/png')
      reply.header('Content-Length', stat.size)
      reply.header('Content-Disposition', `inline; filename="${cert.bot.name}-ric-certificate.png"`)
      reply.header('Cache-Control', 'public, max-age=86400')
      return reply.send(createReadStream(filePath))
    } catch {
      return reply.status(500).send({ error: 'Certificate asset not found on server' })
    }
  })
}
