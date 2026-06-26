/**
 * Express.js middleware for RIC verification
 *
 * @example
 * import { RICMiddleware } from '@robot-id-card/sdk'
 *
 * app.use(RICMiddleware({
 *   permissions: {
 *     '/api/posts':   { minGrade: 'unknown', level: 1 },
 *     '/api/comment': { minGrade: 'healthy', level: 4 },
 *   }
 * }))
 */

import { getRICHeaders, verifyRICRequest, meetsGradeRequirement } from '../verify.js'
import type { RICMiddlewareOptions } from '../types.js'

export function RICMiddleware(options: RICMiddlewareOptions = {}) {
  return async function ricMiddleware(req: any, res: any, next: () => void) {
    const headers = getRICHeaders(req)

    // No RIC headers at all — not a bot, pass through
    const hasRFC9421 = !!(headers.signatureInput && headers.signature)
    const hasLegacy  = !!headers.ricId
    if (!hasRFC9421 && !hasLegacy) return next()

    const result = await verifyRICRequest(headers, {
      registryUrl: options.registryUrl,
      cacheTtl:    options.cacheTtl,
      // RFC 9421: pass request context so registry can reconstruct signature base
      authority: req.hostname || req.headers?.host?.split(':')[0],
      method:    req.method,
      path:      req.path,
    })

    if (!result) return next()

    // Attach RIC info to request for downstream use
    req.ric = result
    options.onBotDetected?.(result, req)

    // Check permission rules for this route
    const rule =
      options.permissions?.[req.path] ||
      options.permissions?.[req.route?.path] ||
      options.defaultRule

    if (rule) {
      if (!result.valid) {
        return res.status(401).json({
          error: 'Invalid RIC certificate',
          code: 'RIC_INVALID',
        })
      }

      if (!meetsGradeRequirement(result.grade, rule.minGrade)) {
        return res.status(403).json({
          error: `Bot grade '${result.grade}' does not meet minimum required grade '${rule.minGrade}'`,
          code: 'RIC_GRADE_INSUFFICIENT',
          your_grade: result.grade,
          required_grade: rule.minGrade,
          upgrade_info: 'https://robotidcard.dev/upgrade',
        })
      }

      if (result.permission_level < rule.level) {
        return res.status(403).json({
          error: `Permission level ${result.permission_level} insufficient for this action (requires ${rule.level})`,
          code: 'RIC_PERMISSION_DENIED',
          your_level: result.permission_level,
          required_level: rule.level,
        })
      }
    }

    next()
  }
}
