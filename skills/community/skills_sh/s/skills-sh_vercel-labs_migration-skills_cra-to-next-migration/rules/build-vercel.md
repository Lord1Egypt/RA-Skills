---
title: Deploy to Vercel
impact: LOW
impactDescription: Recommended deployment platform
tags: build, deployment, vercel
---

## Deploy to Vercel

Vercel is the recommended platform for deploying Next.js applications.

**Initial deployment:**

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy (first time will prompt for setup)
vercel

# Deploy to production
vercel --prod
```

**Via GitHub integration (recommended):**

1. Push code to GitHub
2. Import project at vercel.com/new
3. Vercel auto-detects Next.js
4. Deploys on every push

**vercel.json configuration (optional):**

```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "regions": ["iad1"],
  "env": {
    "DATABASE_URL": "@database-url"
  },
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "no-store" }
      ]
    }
  ]
}
```

**Environment variables:**
1. Go to Project Settings > Environment Variables
2. Add variables for Production/Preview/Development
3. Redeploy to apply changes

**Preview deployments:**
- Every PR gets a unique preview URL
- Share for review before merging
- Automatic cleanup after merge

**Key features:**
- Edge Functions for API routes
- Automatic HTTPS
- Global CDN
- Analytics integration
- Serverless functions
- Image optimization

**Domain setup:**
1. Go to Project Settings > Domains
2. Add your domain
3. Configure DNS as instructed
