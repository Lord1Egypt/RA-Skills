---
name: vibe-security-skill
description: Agent skill that audits vibe-coded apps for common security vulnerabilities introduced by AI coding assistants
triggers:
  - "audit my code for security issues"
  - "check this app for vulnerabilities"
  - "review my Supabase RLS policies"
  - "is this payment flow secure"
  - "scan for hardcoded secrets"
  - "check for common security mistakes"
  - "validate my auth implementation"
  - "run vibe security audit"
---

# Vibe Security Skill

> Skill by [ara.so](https://ara.so) — Security Skills collection.

This skill provides expertise in using the Vibe Security tool to audit vibe-coded applications for common security vulnerabilities that AI coding assistants frequently introduce. It helps identify hardcoded secrets, missing RLS policies, insecure auth patterns, payment vulnerabilities, and other security anti-patterns.

## What Vibe Security Does

Vibe Security is an agent skill that scans codebases for security vulnerability patterns common in AI-generated code. It uses technology-specific reference files to audit only relevant parts of your stack (Supabase, Stripe, React Native, etc.), catching issues like:

- Hardcoded API keys and secrets
- Disabled or missing Row-Level Security (RLS) policies
- Insecure authentication patterns
- Client-submitted payment amounts
- Missing rate limiting
- Tokens stored in localStorage
- Exposed secrets in mobile bundles
- AI API keys without usage caps

## Installation

### For Claude Code

```bash
npx skills add https://github.com/raroque/vibe-security-skill --skill vibe-security
```

### For OpenAI Codex

```bash
npx skills add https://github.com/raroque/vibe-security-skill --skill vibe-security
```

Select "Codex" when prompted.

### Manual Installation

```bash
# Project-level
git clone https://github.com/raroque/vibe-security-skill.git
cp -r vibe-security-skill/vibe-security/ .claude/skills/vibe-security/

# Global installation
cp -r vibe-security-skill/vibe-security/ ~/.claude/skills/vibe-security/
```

## Usage

### Triggering Security Audits

**Claude Code:**
```
/vibe-security
```

Or use natural language:
- "check my code for security issues"
- "is this safe?"
- "audit this Supabase setup"

**Codex:**
```
$vibe-security
```

### Automatic Activation

The skill automatically activates when working with:
- Authentication flows
- Payment processing
- Database queries
- API key configuration
- User data handling
- Environment variables

## Key Security Checks

### 1. Secrets & Environment Variables

**Bad Pattern:**
```typescript
// ❌ Hardcoded secret
const supabase = createClient(
  'https://xxx.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
)

// ❌ Exposed in client bundle
const OPENAI_API_KEY = 'sk-proj-...'
```

**Good Pattern:**
```typescript
// ✅ Environment variable
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

// ✅ Server-side only
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY // Not NEXT_PUBLIC_
})
```

### 2. Supabase Row-Level Security

**Bad Pattern:**
```sql
-- ❌ RLS disabled
CREATE TABLE user_data (
  id uuid,
  user_id uuid,
  sensitive_data text
);
-- No ALTER TABLE ... ENABLE ROW LEVEL SECURITY

-- ❌ Allows everything
CREATE POLICY "allow_all" ON user_data
  FOR ALL USING (true);
```

**Good Pattern:**
```sql
-- ✅ RLS enabled with proper policies
CREATE TABLE user_data (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id uuid REFERENCES auth.users NOT NULL,
  sensitive_data text
);

ALTER TABLE user_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY "users_select_own" ON user_data
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "users_insert_own" ON user_data
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "users_update_own" ON user_data
  FOR UPDATE USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);
```

### 3. Authentication & Authorization

**Bad Pattern:**
```typescript
// ❌ Decoding without verification
import jwt from 'jsonwebtoken'
const decoded = jwt.decode(token) // No signature check!
const userId = decoded.sub

// ❌ Middleware-only auth
// middleware.ts
export function middleware(req: NextRequest) {
  const token = req.cookies.get('token')
  if (!token) return NextResponse.redirect('/login')
}

// app/api/sensitive/route.ts - NOT protected!
export async function GET() {
  return NextResponse.json(await db.getAllUserData())
}
```

**Good Pattern:**
```typescript
// ✅ Verify JWT signature
import jwt from 'jsonwebtoken'
const decoded = jwt.verify(token, process.env.JWT_SECRET!) as JwtPayload
const userId = decoded.sub

// ✅ Auth in every API route
// lib/auth.ts
export async function requireAuth(req: Request) {
  const token = req.headers.get('authorization')?.replace('Bearer ', '')
  if (!token) throw new Error('Unauthorized')
  
  const decoded = jwt.verify(token, process.env.JWT_SECRET!)
  return decoded
}

// app/api/sensitive/route.ts
export async function GET(req: Request) {
  const user = await requireAuth(req)
  return NextResponse.json(await db.getUserData(user.sub))
}
```

### 4. Payment Security

**Bad Pattern:**
```typescript
// ❌ Client submits price
export async function POST(req: Request) {
  const { amount, productId } = await req.json()
  
  const session = await stripe.checkout.sessions.create({
    line_items: [{
      price_data: {
        currency: 'usd',
        product: productId,
        unit_amount: amount // ❌ Trusting client!
      },
      quantity: 1
    }],
    mode: 'payment'
  })
}
```

**Good Pattern:**
```typescript
// ✅ Server determines price
const PRICES = {
  'basic': 999,
  'pro': 2999,
  'enterprise': 9999
} as const

export async function POST(req: Request) {
  const { plan } = await req.json()
  
  if (!PRICES[plan]) throw new Error('Invalid plan')
  
  const session = await stripe.checkout.sessions.create({
    line_items: [{
      price_data: {
        currency: 'usd',
        product: plan,
        unit_amount: PRICES[plan] // ✅ Server-controlled
      },
      quantity: 1
    }],
    mode: 'payment'
  })
}

// ✅ Verify webhook signatures
export async function POST(req: Request) {
  const body = await req.text()
  const sig = req.headers.get('stripe-signature')!
  
  const event = stripe.webhooks.constructEvent(
    body,
    sig,
    process.env.STRIPE_WEBHOOK_SECRET!
  )
  
  // Process event...
}
```

### 5. Rate Limiting

**Bad Pattern:**
```typescript
// ❌ No rate limiting on expensive endpoints
export async function POST(req: Request) {
  const { prompt } = await req.json()
  
  const completion = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [{ role: 'user', content: prompt }]
  })
  
  return NextResponse.json(completion)
}
```

**Good Pattern:**
```typescript
// ✅ Server-side rate limiting
import { Ratelimit } from '@upstash/ratelimit'
import { Redis } from '@upstash/redis'

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '1 h'),
  analytics: true
})

export async function POST(req: Request) {
  const user = await requireAuth(req)
  
  const { success } = await ratelimit.limit(user.sub)
  if (!success) {
    return NextResponse.json(
      { error: 'Rate limit exceeded' },
      { status: 429 }
    )
  }
  
  const { prompt } = await req.json()
  
  const completion = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [{ role: 'user', content: prompt }],
    max_tokens: 1000 // ✅ Cap token usage
  })
  
  return NextResponse.json(completion)
}
```

### 6. Mobile Security (React Native / Expo)

**Bad Pattern:**
```typescript
// ❌ API key in JS bundle
const OPENAI_API_KEY = 'sk-proj-...'

// ❌ Token in AsyncStorage
import AsyncStorage from '@react-native-async-storage/async-storage'
await AsyncStorage.setItem('auth_token', token)
```

**Good Pattern:**
```typescript
// ✅ Use backend proxy for AI calls
const response = await fetch('https://api.myapp.com/ai/chat', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${userToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ prompt })
})

// ✅ Use secure storage for tokens
import * as SecureStore from 'expo-secure-store'

await SecureStore.setItemAsync('auth_token', token)
const token = await SecureStore.getItemAsync('auth_token')
```

### 7. SQL Injection & Data Access

**Bad Pattern:**
```typescript
// ❌ SQL injection vulnerability
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url)
  const userId = searchParams.get('userId')
  
  const result = await db.$queryRawUnsafe(
    `SELECT * FROM users WHERE id = ${userId}`
  )
}

// ❌ Prisma operator injection
const users = await prisma.user.findMany({
  where: req.query // ❌ Direct user input
})
```

**Good Pattern:**
```typescript
// ✅ Parameterized queries
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url)
  const userId = searchParams.get('userId')
  
  const result = await db.$queryRaw`
    SELECT * FROM users WHERE id = ${userId}
  `
}

// ✅ Validate and sanitize input
const userIdSchema = z.string().uuid()
const userId = userIdSchema.parse(searchParams.get('userId'))

const user = await prisma.user.findUnique({
  where: { id: userId }
})
```

## Configuration

Vibe Security uses reference files organized by technology. The skill automatically detects your stack and applies relevant checks.

### Supported Technologies

- **Databases:** Supabase, Firebase, Convex, Prisma
- **Payments:** Stripe
- **Mobile:** React Native, Expo
- **AI:** OpenAI, Anthropic, other LLM providers
- **Frameworks:** Next.js, Vite, Express

### Customizing Rules

You can extend the skill by adding custom security rules in your project's `.claude/skills/vibe-security/rules/` directory.

## Common Issues & Troubleshooting

### "Skill not activating automatically"

Make sure you're working with code that involves:
- Authentication/authorization
- Database queries
- Payment processing
- Environment variables
- API integrations

Or explicitly trigger with `/vibe-security` (Claude) or `$vibe-security` (Codex).

### "False positives on legitimate patterns"

The skill prioritizes security over convenience. If you have a legitimate use case for a flagged pattern:

1. Document why it's safe with comments
2. Ensure compensating controls exist
3. Consider if there's a more secure alternative

### "Not catching vulnerabilities"

The skill focuses on common AI-generated security mistakes. For comprehensive security:

- Run additional tools (Snyk, npm audit, etc.)
- Conduct manual security reviews
- Follow OWASP guidelines
- Implement defense in depth

## Best Practices

### Environment Variables

```bash
# .env.local (never commit)
DATABASE_URL="postgresql://..."
STRIPE_SECRET_KEY="sk_test_..."
OPENAI_API_KEY="sk-proj-..."

# Public vars (safe in client bundle)
NEXT_PUBLIC_SUPABASE_URL="https://xxx.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJ..."
```

### Security Headers

```typescript
// next.config.js
const securityHeaders = [
  {
    key: 'X-DNS-Prefetch-Control',
    value: 'on'
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=63072000; includeSubDomains; preload'
  },
  {
    key: 'X-Frame-Options',
    value: 'SAMEORIGIN'
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff'
  },
  {
    key: 'Referrer-Policy',
    value: 'origin-when-cross-origin'
  }
]

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders
      }
    ]
  }
}
```

### Input Validation

```typescript
import { z } from 'zod'

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().min(13).max(120)
})

export async function POST(req: Request) {
  const body = await req.json()
  const validated = createUserSchema.parse(body)
  
  // Safe to use validated data
  await db.user.create({ data: validated })
}
```

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Supabase Security Best Practices](https://supabase.com/docs/guides/auth)
- [Stripe Security Guide](https://stripe.com/docs/security/guide)
- [Next.js Security Headers](https://nextjs.org/docs/advanced-features/security-headers)

---

Created by [Chris Raroque](https://twitter.com/raroque) and the team at [Aloa](https://aloa.co).
