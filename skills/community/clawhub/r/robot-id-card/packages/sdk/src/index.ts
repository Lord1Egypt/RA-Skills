/**
 * @robot-id-card/sdk
 *
 * Drop-in middleware for websites to verify bot identity and enforce permission levels.
 * Compatible with Express, Fastify, Next.js, Koa, and vanilla Node.js.
 */

export { RICMiddleware } from './middleware/express.js'
export { RICFastifyPlugin } from './middleware/fastify.js'
export { verifyRICRequest, getRICHeaders } from './verify.js'
export type { RICVerifyResult, RICPermissionRule, RICMiddlewareOptions } from './types.js'
