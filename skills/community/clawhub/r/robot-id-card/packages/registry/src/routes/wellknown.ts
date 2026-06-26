import type { FastifyPluginAsync } from 'fastify'
import { botStore } from '../store/botStore.js'

/**
 * Well-known HTTP Message Signatures key directory — RFC 9421 / Web Bot Auth standard.
 *
 * Endpoints:
 *   GET /.well-known/http-message-signatures-directory
 *     Returns JWKS for ALL registered bots (healthy + unknown, not dangerous).
 *     Content-Type: application/http-message-signatures-directory+json
 *
 *   GET /.well-known/http-message-signatures-directory?kid=ric_abc_xyz
 *     Returns JWKS for a single bot by its RIC ID.
 *
 *   GET /v1/bots/:id/keys
 *     Per-bot key endpoint — useful as the keyid URL in Signature-Input.
 *
 * Key format: JWK with OKP / Ed25519 (RFC 8037)
 *   {
 *     "kty": "OKP",
 *     "crv": "Ed25519",
 *     "x": "<base64url 32-byte public key>",
 *     "kid": "ric_abc_xyz",
 *     "use": "sig"
 *   }
 */

function hexToBase64url(hex: string): string {
  const bytes = Buffer.from(hex, 'hex')
  return bytes.toString('base64url')
}

function certToJWK(cert: { id: string; public_key: string; bot: { name: string } }) {
  const pubKeyHex = cert.public_key.replace('ed25519:', '')
  return {
    kty: 'OKP',
    crv: 'Ed25519',
    x: hexToBase64url(pubKeyHex),
    kid: cert.id,
    use: 'sig',
  }
}

export const wellknownRoutes: FastifyPluginAsync = async (fastify) => {
  // Registry-level JWKS — all non-dangerous bots
  fastify.get('/.well-known/http-message-signatures-directory', async (request, reply) => {
    const { kid } = request.query as { kid?: string }

    reply.header('Content-Type', 'application/http-message-signatures-directory+json')
    reply.header('Cache-Control', 'public, max-age=300')

    if (kid) {
      const cert = botStore.findById(kid)
      if (!cert || cert.grade === 'dangerous') {
        return reply.status(404).send({ keys: [], error: 'Key not found or bot is dangerous' })
      }
      return reply.send({ keys: [certToJWK(cert)] })
    }

    const all = botStore.listSummary()
    const keys = all
      .filter((b) => b.grade !== 'dangerous')
      .map((b) => {
        const cert = botStore.findById(b.id)
        return cert ? certToJWK(cert) : null
      })
      .filter(Boolean)

    return reply.send({ keys })
  })
}

// Per-bot key endpoint registered under /v1/bots prefix
export const botKeyRoutes: FastifyPluginAsync = async (fastify) => {
  fastify.get('/:id/keys', async (request, reply) => {
    const { id } = request.params as { id: string }
    const cert = botStore.findById(id)

    if (!cert) {
      return reply.status(404).send({ error: 'Bot not found' })
    }
    if (cert.grade === 'dangerous') {
      return reply.status(403).send({ error: 'Bot is flagged as dangerous — key directory unavailable' })
    }

    reply.header('Content-Type', 'application/http-message-signatures-directory+json')
    reply.header('Cache-Control', 'public, max-age=300')
    return reply.send({ keys: [certToJWK(cert)] })
  })
}
