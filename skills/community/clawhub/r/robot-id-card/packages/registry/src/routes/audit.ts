import type { FastifyPluginAsync } from 'fastify'
import { z } from 'zod'
import { GradeSchema } from '../models/certificate.js'
import { botStore } from '../store/botStore.js'
import { auditStore } from '../store/auditStore.js'

const ReportSchema = z.object({
  ric_id: z.string().startsWith('ric_'),
  reporter_domain: z.string().min(1),
  reason: z.enum([
    'spam',
    'scraping_violation',
    'rate_limit_abuse',
    'tos_violation',
    'impersonation',
    'malicious_content',
    'other',
  ]),
  evidence_url: z.string().url().optional(),
  description: z.string().max(1000),
})

const GradeUpdateSchema = z.object({
  ric_id: z.string().startsWith('ric_'),
  grade: GradeSchema,
  reason: z.string().min(1).max(500),
  admin_key: z.string(),
})

const ADMIN_KEY = process.env.RIC_ADMIN_KEY || 'dev-admin-key-change-me'

export const auditRoutes: FastifyPluginAsync = async (fastify) => {
  /**
   * POST /v1/audit/report
   * Website reports bad bot behavior
   */
  fastify.post('/report', async (request, reply) => {
    const body = ReportSchema.safeParse(request.body)
    if (!body.success) {
      return reply.status(400).send({ error: 'Invalid report', details: body.error.flatten() })
    }

    const { ric_id, reporter_domain, reason, description } = body.data

    // Verify the bot exists before accepting a report
    const cert = botStore.findById(ric_id)
    if (!cert) {
      return reply.status(404).send({ error: 'Bot not found', ric_id })
    }

    const entry = auditStore.append({
      ric_id,
      event: 'violation_report',
      reason,
      reporter: reporter_domain,
      description,
    })

    fastify.log.warn(`Violation report for ${ric_id}: ${reason} from ${reporter_domain}`)

    // Auto-flag as dangerous if 3+ reports in 24h
    const recentCount = botStore.countRecentReports(ric_id)
    if (recentCount >= 3 && cert.grade !== 'dangerous') {
      const oldGrade = cert.grade
      botStore.updateGrade(ric_id, 'dangerous')
      auditStore.append({
        ric_id,
        event: 'grade_changed',
        old_grade: oldGrade,
        new_grade: 'dangerous',
        reason: `Auto-flagged: ${recentCount} violation reports in 24h`,
      })
      fastify.log.warn(`Bot ${ric_id} auto-flagged as DANGEROUS`)
    }

    return reply.status(202).send({ message: 'Report submitted for review', report_id: entry.id })
  })

  /**
   * GET /v1/audit/:ric_id
   * Public audit log for a specific bot
   */
  fastify.get('/:ric_id', async (request, reply) => {
    const { ric_id } = request.params as { ric_id: string }
    const events = auditStore.findByRicId(ric_id)
    return reply.send({ ric_id, total: events.length, events })
  })

  /**
   * POST /v1/audit/grade
   * Manually update a bot's grade after weekly review (requires admin key)
   */
  fastify.post('/grade', async (request, reply) => {
    const body = GradeUpdateSchema.safeParse(request.body)
    if (!body.success) {
      return reply.status(400).send({ error: 'Invalid request', details: body.error.flatten() })
    }

    const { ric_id, grade, reason, admin_key } = body.data

    if (admin_key !== ADMIN_KEY) {
      return reply.status(403).send({ error: 'Forbidden' })
    }

    const cert = botStore.findById(ric_id)
    if (!cert) {
      return reply.status(404).send({ error: 'Bot not found', ric_id })
    }

    const oldGrade = cert.grade
    botStore.updateGrade(ric_id, grade)
    auditStore.append({
      ric_id,
      event: 'grade_changed',
      old_grade: oldGrade,
      new_grade: grade,
      reason,
    })

    return reply.send({ message: `Grade updated to ${grade}`, ric_id, old_grade: oldGrade })
  })
}
