# @robot-id-card/sdk

> Website SDK for verifying Robot ID Card bot identities in Express and Fastify apps.

## Install

```bash
npm install @robot-id-card/sdk
```

## Quick Start

### Express

```typescript
import express from 'express'
import { ricMiddleware } from '@robot-id-card/sdk/middleware/express'

const app = express()

// Block unknown/dangerous bots on protected routes
app.use('/api/write', ricMiddleware({ minGrade: 'healthy' }))

// Only allow healthy bots with post_content capability
app.use('/api/posts', ricMiddleware({
  minGrade: 'healthy',
  requiredPermissionLevel: 4,
}))
```

### Fastify

```typescript
import Fastify from 'fastify'
import { ricPlugin } from '@robot-id-card/sdk/middleware/fastify'

const server = Fastify()
await server.register(ricPlugin, { minGrade: 'healthy' })
```

### Manual verification

```typescript
import { getRICHeaders, verifyRICRequest } from '@robot-id-card/sdk'

// In your request handler:
const headers = getRICHeaders(req)
const result = await verifyRICRequest(headers, {
  registryUrl: 'https://registry.robotidcard.dev',
  cacheTtl: 300, // seconds
})

if (!result?.valid) {
  // Bot not verified
}
console.log(result.grade)           // 'healthy' | 'unknown' | 'dangerous'
console.log(result.permission_level) // 0–5
```

## HTTP Headers (set by the bot)

| Header | Description |
|--------|-------------|
| `X-RIC-ID` | Bot's RIC identifier (`ric_...`) |
| `X-RIC-Timestamp` | Unix timestamp in ms (replay protection) |
| `X-RIC-Signature` | Ed25519 signature over `${ric_id}:${timestamp}:${message}` |

## Grade Levels

| Grade | Meaning | Permission Level |
|-------|---------|-----------------|
| `dangerous` | Reported / flagged | 0 — blocked |
| `unknown` | Registered, not yet trusted | 1 — read only |
| `healthy` | 3+ consecutive daily claims | 1–5 based on capabilities |
