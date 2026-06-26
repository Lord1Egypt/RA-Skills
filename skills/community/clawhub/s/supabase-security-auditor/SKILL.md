---
name: supabase-security-auditor
description: Audit Supabase projects for security — check Row Level Security policies, auth configuration, API exposure, storage rules, and edge function security.
metadata:
  tags: ["supabase", "security", "postgres", "auth", "rls"]
---

# Supabase Security Auditor

Audit Supabase projects for security vulnerabilities including Row Level Security (RLS) policies, authentication configuration, API key exposure, storage bucket rules, and edge function security. Use before launching, after configuration changes, or during security reviews.

## Usage

```
"Audit my Supabase project for security"
"Check RLS policies on all tables"
"Review auth configuration for vulnerabilities"
"Are my Supabase storage buckets secure?"
```

## How It Works

### 1. Project Discovery

```bash
# Find Supabase config
cat supabase/config.toml 2>/dev/null
ls supabase/migrations/ 2>/dev/null | tail -10
# Find API usage
grep -rn "createClient\|supabase\." src/ lib/ app/ | head -20
# Check for exposed keys
grep -rn "SUPABASE_\|supabase\.\(url\|key\|anon\)" .env* src/ | head -10
```

### 2. Row Level Security (RLS)

**Critical checks:**
- Tables without RLS enabled (exposed to anon/authenticated)
- RLS policies that are too permissive (`using (true)`)
- Missing policies for INSERT/UPDATE/DELETE (only SELECT covered)
- Policies using `auth.uid()` correctly for ownership
- Service role bypass patterns
- Policies on junction/join tables

**Common vulnerabilities:**
```sql
-- BAD: Anyone can read all users
create policy "public read" on users for select using (true);

-- GOOD: Users can only read own profile
create policy "own profile" on users for select 
  using (auth.uid() = id);

-- BAD: No RLS means API exposes everything
-- (table has no policies at all)
```

### 3. Auth Configuration

- Email confirmations enabled/disabled
- Password strength requirements
- OAuth providers properly configured
- JWT expiry times appropriate
- Custom claims validation
- Magic link vs password vs OAuth strategy
- Rate limiting on auth endpoints

### 4. API Key Security

- `anon` key: only used client-side, limited by RLS
- `service_role` key: NEVER exposed to client
- Check for service_role key in frontend code
- Environment variable usage vs hardcoded keys
- Key rotation policy

### 5. Storage Security

- Public vs private bucket configuration
- File upload size limits
- Allowed MIME types
- Storage policies matching RLS patterns
- Signed URL expiry times

### 6. Edge Functions

- CORS configuration
- Input validation
- Error handling (no stack traces in responses)
- Rate limiting
- Secret management (env vars vs hardcoded)

### 7. Database Security

- Functions with `SECURITY DEFINER` (runs as owner, not caller)
- Triggers that bypass RLS
- Views that expose sensitive data
- Proper role permissions (anon vs authenticated vs service_role)

## Output

```
## Supabase Security Audit

**Project:** my-app | **Tables:** 12 | **RLS Enabled:** 8/12

### 🔴 Critical (3)
1. **4 tables without RLS** — orders, payments, audit_log, api_keys
   These are fully accessible via the anon API key!
   → Enable RLS: `alter table orders enable row level security;`

2. **service_role key in frontend** — src/lib/supabase.ts:3
   `createClient(url, 'eyJhbGciOiJIUz...')` — this key bypasses ALL RLS
   → Use NEXT_PUBLIC_SUPABASE_ANON_KEY only in client code

3. **Public storage bucket** — 'avatars' bucket is public
   Anyone can list and download all uploaded files
   → Set bucket to private, use signed URLs for access

### 🟡 Warnings (4)
4. profiles table: SELECT policy uses `using (true)` — all profiles public
5. No email confirmation required — anyone can create accounts
6. JWT expiry: 3600s default — consider shorter for sensitive apps
7. No file type restriction on uploads — allows executables

### ✅ Secure
- Auth using PKCE flow (no implicit grant)
- Password minimum length enforced
- Edge functions use env vars for secrets
- Database functions use SECURITY INVOKER

### 📋 RLS Policy Coverage
| Table | SELECT | INSERT | UPDATE | DELETE | Status |
|-------|--------|--------|--------|--------|--------|
| users | ✅ | ✅ | ✅ | ❌ | 🟡 |
| posts | ✅ | ✅ | ✅ | ✅ | ✅ |
| orders | ❌ | ❌ | ❌ | ❌ | 🔴 NO RLS |
| payments | ❌ | ❌ | ❌ | ❌ | 🔴 NO RLS |
```
