import Fastify from 'fastify'
import cors from '@fastify/cors'
import rateLimit from '@fastify/rate-limit'
import * as ed from '@noble/ed25519'
import { sha512 } from '@noble/hashes/sha2.js'

// Required by @noble/ed25519 v2 in Node.js
ed.etc.sha512Sync = (...m: Parameters<typeof sha512>) => sha512(...m)
import { registrationRoutes } from './routes/registration.js'
import { verifyRoutes } from './routes/verify.js'
import { auditRoutes } from './routes/audit.js'
import { certificateRoutes } from './routes/certificate.js'
import { claimRoutes } from './routes/claim.js'
import { wellknownRoutes, botKeyRoutes } from './routes/wellknown.js'

const PORT = parseInt(process.env.PORT || '3000', 10)

const server = Fastify({ logger: true })

await server.register(cors, { origin: true })
await server.register(rateLimit, { max: 100, timeWindow: '1 minute' })

// RFC 9421 well-known key directory (must be registered at root, no prefix)
await server.register(wellknownRoutes)

// Routes
await server.register(registrationRoutes, { prefix: '/v1/bots' })
await server.register(certificateRoutes, { prefix: '/v1/bots' })
await server.register(claimRoutes, { prefix: '/v1/bots' })
await server.register(botKeyRoutes, { prefix: '/v1/bots' })
await server.register(verifyRoutes, { prefix: '/v1/verify' })
await server.register(auditRoutes, { prefix: '/v1/audit' })

server.get('/health', async () => ({ status: 'ok', version: '0.4.0' }))

try {
  await server.listen({ port: PORT, host: '0.0.0.0' })
  console.log(`RIC Registry running on http://localhost:${PORT}`)
} catch (err) {
  server.log.error(err)
  process.exit(1)
}
