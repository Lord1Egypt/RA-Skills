import type { FastifyPluginAsync } from 'fastify'
import { getRICHeaders, verifyRICRequest, meetsGradeRequirement } from '../verify.js'
import type { RICMiddlewareOptions } from '../types.js'

export const RICFastifyPlugin: FastifyPluginAsync<RICMiddlewareOptions> = async (
  fastify,
  options
) => {
  fastify.addHook('preHandler', async (request, reply) => {
    const headers = getRICHeaders(request as any)
    if (!headers.ricId) return

    const result = await verifyRICRequest(headers, {
      registryUrl: options.registryUrl,
      cacheTtl: options.cacheTtl,
    })

    if (!result) return
    ;(request as any).ric = result
    options.onBotDetected?.(result, request)

    const rule = options.permissions?.[request.url] || options.defaultRule
    if (!rule) return

    if (!result.valid) {
      return reply.status(401).send({ error: 'Invalid RIC certificate', code: 'RIC_INVALID' })
    }

    if (!meetsGradeRequirement(result.grade, rule.minGrade)) {
      return reply.status(403).send({
        error: `Grade '${result.grade}' insufficient`,
        required: rule.minGrade,
        code: 'RIC_GRADE_INSUFFICIENT',
      })
    }

    if (result.permission_level < rule.level) {
      return reply.status(403).send({
        error: 'Permission denied',
        code: 'RIC_PERMISSION_DENIED',
        your_level: result.permission_level,
        required_level: rule.level,
      })
    }
  })
}
