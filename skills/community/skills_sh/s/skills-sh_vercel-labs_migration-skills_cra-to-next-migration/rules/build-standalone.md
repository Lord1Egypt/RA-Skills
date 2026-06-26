---
title: Configure Standalone Output
impact: MEDIUM
impactDescription: Optimized for containers
tags: build, standalone, docker
---

## Configure Standalone Output

Use standalone output for smaller, self-contained deployments (Docker, custom servers).

**Standard Next.js deployment:**

```
node_modules/     # All dependencies
.next/            # Build output
public/           # Static files
package.json
```

**Standalone output (optimized):**

```js
// next.config.js
module.exports = {
  output: 'standalone',
}
```

```
.next/standalone/
├── server.js           # Minimal server
├── node_modules/       # Only production deps
├── .next/
│   └── static/        # Copy this to serve static files
└── public/            # Copy this for public files
```

**Running standalone:**

```bash
# Build
npm run build

# Copy static files
cp -r .next/static .next/standalone/.next/
cp -r public .next/standalone/

# Run
cd .next/standalone
node server.js
```

**Docker with standalone:**

```dockerfile
# Dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD ["node", "server.js"]
```

**Benefits:**
- Smaller image size (~100MB vs ~500MB+)
- Only production dependencies
- Self-contained server
- No need for `npm install` at runtime
