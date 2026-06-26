import type { FastifyPluginAsync } from 'fastify'
import { z } from 'zod'
import { nanoid } from 'nanoid'
import * as ed from '@noble/ed25519'
import { botStore } from '../store/botStore.js'
import { auditStore } from '../store/auditStore.js'
import { BotCapabilitySchema } from '../models/certificate.js'
import { selectCertificateFile, buildCodeAward, buildVisualAward } from './certificate.js'

const RegisterBodySchema = z.object({
  developer: z.object({
    name: z.string().min(1).max(128),
    email: z.string().email(),
    org: z.string().max(128).optional(),
    website: z.string().url().optional(),
  }),
  bot: z.object({
    name: z.string().min(1).max(64),
    version: z.string().regex(/^\d+\.\d+(\.\d+)?$/, 'version must be semver e.g. 1.0.0'),
    purpose: z.string().min(10).max(500),
    capabilities: z.array(BotCapabilitySchema).min(1),
    user_agent: z.string().min(1).max(256),
  }),
  public_key: z.string().startsWith('ed25519:').length(72), // 'ed25519:' (8) + 64 hex chars
})

export const registrationRoutes: FastifyPluginAsync = async (fastify) => {
  /**
   * POST /v1/bots/register
   * Register a new bot and receive its RIC certificate.
   *
   * Uniqueness rules:
   *   1. A public key can only be registered once (each keypair = one bot identity)
   *   2. (email + bot name) combo must be unique — prevents duplicate registrations
   */
  fastify.post('/register', {
    config: { rateLimit: { max: 5, timeWindow: '1 hour' } },
  }, async (request, reply) => {
    const body = RegisterBodySchema.safeParse(request.body)
    if (!body.success) {
      return reply.status(400).send({ error: 'Invalid request', details: body.error.flatten() })
    }

    const { developer, bot, public_key } = body.data

    // ── Uniqueness check 1: public key ────────────────────
    const existingByKey = botStore.findByPublicKey(public_key)
    if (existingByKey) {
      return reply.status(409).send({
        error: 'Public key already registered',
        code: 'DUPLICATE_KEY',
        existing_id: existingByKey,
        hint: 'Each bot must use a unique Ed25519 keypair. Generate a new key with `ric keygen`.',
      })
    }

    // ── Uniqueness check 2: email + bot name ──────────────
    const existingByName = botStore.findByEmailAndBotName(developer.email, bot.name)
    if (existingByName) {
      return reply.status(409).send({
        error: 'A bot with this name is already registered for this developer account',
        code: 'DUPLICATE_BOT',
        existing_id: existingByName,
        hint: 'Use `ric status` to retrieve your existing certificate, or choose a different bot name.',
      })
    }

    // ── Validate public key is valid Ed25519 ──────────────
    const pubKeyHex = public_key.replace('ed25519:', '')
    try {
      if (pubKeyHex.length !== 64 || !/^[0-9a-f]+$/i.test(pubKeyHex)) {
        throw new Error('invalid hex')
      }
      // ed25519 public keys are always 32 bytes = 64 hex chars
      Buffer.from(pubKeyHex, 'hex')
    } catch {
      return reply.status(400).send({
        error: 'Invalid public key format',
        code: 'INVALID_KEY',
        hint: 'Public key must be a valid Ed25519 key in hex format prefixed with "ed25519:"',
      })
    }

    // Embed first 8 hex chars of public key as fingerprint — the bot's identity
    // is permanently woven into its RIC ID: ric_{fp8}_{rand8}
    const fingerprint = pubKeyHex.slice(0, 8)
    const id = `ric_${fingerprint}_${nanoid(8)}`
    const now = new Date().toISOString()

    const certificate = {
      ric_version: '1.0' as const,
      id,
      created_at: now,
      developer: { ...developer, verified: false },
      bot: { ...bot },
      grade: 'unknown' as const,
      grade_updated_at: now,
      public_key,
      // Registry signature placeholder — in v0.3 this will be a real Ed25519 sig from registry key
      signature: `registry_sig_${nanoid(32)}`,
    }

    botStore.insert(certificate)
    auditStore.append({ ric_id: id, event: 'registered', reason: 'New bot registration' })

    fastify.log.info(`New bot registered: ${id} (${bot.name} by ${developer.email})`)

    const { type: certificateType, file: certFile } = selectCertificateFile(bot.capabilities)

    // Build inline award:
    //   visual bots → base64 PNG data URI
    //   code-only   → array of ASCII lines (safe for JSON serialization)
    const award = certificateType === 'visual'
      ? buildVisualAward(certFile)
      : buildCodeAward({
          botName: bot.name,
          ricId: id,
          developer: developer.email,
          grade: 'unknown',
          issuedAt: now,
        })

    return reply.status(201).send({
      certificate,
      certificate_url: `/v1/bots/${id}/certificate`,
      certificate_type: certificateType,
      // visual: string (data:image/png;base64,...)
      // code:   string[] (each line of the ASCII award)
      award,
      message: 'Bot registered successfully. Grade: UNKNOWN — weekly review pending.',
      docs: 'https://github.com/Cosmofang/robot-id-card',
    })
  })

  /**
   * GET /v1/bots/:id
   * Fetch a bot's current certificate and grade
   */
  fastify.get('/:id', async (request, reply) => {
    const { id } = request.params as { id: string }
    const cert = botStore.findById(id)

    if (!cert) {
      return reply.status(404).send({ error: 'Bot not found', id })
    }

    return reply.send(cert)
  })

  /**
   * GET /v1/bots?grade=healthy&page=1&limit=50
   * List registered bots with optional grade filter and pagination
   */
  fastify.get('/', async (request) => {
    const { grade, page = '1', limit = '50' } = request.query as {
      grade?: string
      page?: string
      limit?: string
    }

    let bots = botStore.listSummary()

    if (grade && ['unknown', 'healthy', 'dangerous'].includes(grade)) {
      bots = bots.filter((b) => b.grade === grade)
    }

    const pageNum = Math.max(1, parseInt(page, 10) || 1)
    const limitNum = Math.min(100, Math.max(1, parseInt(limit, 10) || 50))
    const total = bots.length
    const start = (pageNum - 1) * limitNum
    const paged = bots.slice(start, start + limitNum)

    return {
      total,
      page: pageNum,
      limit: limitNum,
      pages: Math.ceil(total / limitNum),
      bots: paged,
    }
  })
}
