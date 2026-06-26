/**
 * POST /v1/bots/:id/claim
 *
 * Daily identity claim — bot proves ownership of its RIC ID by signing
 * a challenge with its Ed25519 private key.
 *
 * Rules:
 *   - Max 2 claims per calendar day (UTC)
 *   - One bot is permanently bound to one ID (enforced at registration)
 *   - 3 consecutive daily claims → grade upgraded unknown → healthy
 *   - Bot with 3+ violation reports in 24 h → auto-downgraded to dangerous
 *
 * Request body:
 *   { "signature": "ed25519:<hex>", "date": "YYYY-MM-DD" }
 *
 * The bot must sign exactly: "<ric_id>:<date>"  (UTF-8, no newline)
 * using its registered Ed25519 private key.
 */

import type { FastifyPluginAsync } from 'fastify'
import { z } from 'zod'
import * as ed from '@noble/ed25519'
import { botStore } from '../store/botStore.js'
import { auditStore } from '../store/auditStore.js'
import { selectCertificateFile, buildCodeAward, buildVisualAward } from './certificate.js'

const ClaimBodySchema = z.object({
  signature: z.string().startsWith('ed25519:'),
  date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, 'date must be YYYY-MM-DD'),
})

export const claimRoutes: FastifyPluginAsync = async (fastify) => {
  fastify.post('/:id/claim', {
    config: { rateLimit: { max: 20, timeWindow: '1 hour' } },
  }, async (request, reply) => {
    const { id } = request.params as { id: string }

    const body = ClaimBodySchema.safeParse(request.body)
    if (!body.success) {
      return reply.status(400).send({ error: 'Invalid request', details: body.error.flatten() })
    }

    const { signature, date } = body.data

    // ── Load bot ──────────────────────────────────────────
    const cert = botStore.findById(id)
    if (!cert) {
      return reply.status(404).send({ error: 'Bot not found', id })
    }

    // ── Blocked bots cannot claim ─────────────────────────
    if (cert.grade === 'dangerous') {
      return reply.status(403).send({
        error: 'Forbidden',
        code: 'BOT_DANGEROUS',
        message: 'Dangerous bots cannot claim their identity. Contact LUMIOI to appeal.',
      })
    }

    // ── Verify date is today (allow ±1 day for timezone drift) ───────────
    const today = new Date().toISOString().slice(0, 10)
    const yesterday = new Date(Date.now() - 86_400_000).toISOString().slice(0, 10)
    if (date !== today && date !== yesterday) {
      return reply.status(400).send({
        error: 'Invalid date',
        code: 'DATE_MISMATCH',
        message: `Claim date must be today (${today}) or yesterday (${yesterday}).`,
      })
    }

    // ── Verify Ed25519 signature ──────────────────────────
    const message = `${id}:${date}`
    const msgBytes = new TextEncoder().encode(message)
    const sigHex = signature.replace('ed25519:', '')
    const pubHex = cert.public_key.replace('ed25519:', '')

    try {
      const valid = await ed.verify(sigHex, msgBytes, pubHex)
      if (!valid) {
        return reply.status(401).send({
          error: 'Signature verification failed',
          code: 'INVALID_SIGNATURE',
          hint: `Sign the string "${id}:${date}" with your Ed25519 private key.`,
        })
      }
    } catch {
      return reply.status(400).send({
        error: 'Malformed signature',
        code: 'BAD_SIGNATURE_FORMAT',
      })
    }

    // ── Record claim (enforces daily limit + streak logic) ────────────
    const result = botStore.recordClaim(id)

    if (!result.ok) {
      if (result.error === 'DAILY_LIMIT_REACHED') {
        return reply.status(429).send({
          error: 'Daily claim limit reached',
          code: 'DAILY_LIMIT_REACHED',
          message: 'You have already claimed your identity 2 times today. Try again tomorrow.',
          today_count: result.today_count,
        })
      }
      return reply.status(500).send({ error: 'Claim failed' })
    }

    // ── Audit log ─────────────────────────────────────────
    auditStore.append({
      ric_id: id,
      event: 'identity_claimed',
      reason: `Daily claim #${result.today_count} — streak: ${result.consecutive_days} day(s)`,
    })

    if (result.grade_upgraded) {
      auditStore.append({
        ric_id: id,
        event: 'grade_changed',
        reason: `Auto-upgraded to HEALTHY after ${result.consecutive_days} consecutive daily claims`,
      })
    }

    // ── Build award for response ──────────────────────────
    const updatedCert = botStore.findById(id)!
    const { type: certType, file: certFile } = selectCertificateFile(cert.bot.capabilities)
    const award = certType === 'visual'
      ? buildVisualAward(certFile)
      : buildCodeAward({
          botName: cert.bot.name,
          ricId: id,
          developer: cert.developer.email,
          grade: updatedCert.grade,
          issuedAt: new Date().toISOString(),
        })

    fastify.log.info(`Identity claimed: ${id} (streak: ${result.consecutive_days})`)

    return reply.status(200).send({
      success: true,
      ric_id: id,
      grade: updatedCert.grade,
      grade_upgraded: result.grade_upgraded ?? false,
      consecutive_days: result.consecutive_days,
      today_count: result.today_count,
      remaining_today: 2 - (result.today_count ?? 0),
      certificate_type: certType,
      award,
      message: result.grade_upgraded
        ? `🎉 Grade upgraded to HEALTHY after ${result.consecutive_days} consecutive days!`
        : `✓ Identity claimed. Streak: ${result.consecutive_days} day(s). ${2 - (result.today_count ?? 0)} claim(s) remaining today.`,
    })
  })
}
