---
name: skill-file-security
description: Battle-tested security checks for AI coding assistants — 29 categories covering OWASP Top 10, CWE Top 25, and ASVS Level 3
triggers:
  - "install security skill"
  - "add security checks to my AI"
  - "run security audit on my project"
  - "scan my code for vulnerabilities"
  - "configure security skill"
  - "fix security issues in my codebase"
  - "check my project for OWASP violations"
  - "security scan with skill-file-security"
---

# skill-file-security

> Skill by [ara.so](https://ara.so) — Security Skills collection.

**skill-file-security** installs 29 battle-tested security instruction files into your project that teach AI coding assistants to identify and fix vulnerabilities across OWASP Top 10, CWE Top 25, ASVS Level 3, and more — without leaving your IDE.

## What This Does

skill-file-security is a CLI tool that:
- Installs security knowledge files to `.skills/security/` in your project
- Auto-configures all major AI coding assistants (Claude, Cursor, Copilot, Windsurf, Cline, etc.)
- Creates `memory-security.md` to track your security score over time
- Hardens `.gitignore` with 6 security-focused entries
- Provides 6 slash commands: `/security-scan`, `/security-audit`, `/security-fix`, `/security-status`, `/security-history`, `/security-incident`

The AI assistant reads these instruction files and applies 29 security categories to YOUR specific stack (Next.js, Django, Laravel, Express, Docker, Supabase, Firebase, etc.).

## Installation

### Interactive Mode (Recommended)
```bash
npx @netxeo/security-skill
```

This launches a smart 5-question setup that:
1. Auto-detects your stack (Next.js, Supabase, Docker, etc.)
2. Asks about auth, database, API, deployment, and custom rules
3. Installs only the security rules you need

### Fast Mode (Silent Install)
```bash
# Install everywhere (all AI assistants)
npx @netxeo/security-skill --yes

# Install for specific assistants
npx @netxeo/security-skill --claude
npx @netxeo/security-skill --cursor
npx @netxeo/security-skill --copilot
npx @netxeo/security-skill --windsurf
npx @netxeo/security-skill --cline
```

### Install as a Dev Dependency
```bash
npm install --save-dev @netxeo/security-skill

# Then run via package.json script
npx security-skill
```

## What Gets Installed

```
your-project/
├── .skills/
│   └── security/
│       ├── skill.md                      # Main security orchestrator
│       ├── 01-secrets-and-files.md
│       ├── 02-network-and-cors.md
│       ├── 03-http-headers.md
│       ├── 04-auth-and-sessions.md
│       ├── 05-cryptography.md
│       ├── 06-jwt-security.md
│       ├── 07-database-security.md
│       ├── 08-deployment-ci-cd.md
│       ├── 09-docker-security.md
│       ├── 10-protocols-graphql-websocket.md
│       ├── 11-advanced-attacks.md
│       ├── 12-all-injections.md
│       ├── 13-race-conditions.md
│       ├── 14-file-upload.md
│       ├── 15-dns-email.md
│       ├── 16-supply-chain.md
│       ├── 17-mobile-security.md
│       ├── 18-compliance-gdpr.md
│       ├── 19-monitoring-honeytokens.md
│       ├── 20-serverless-edge.md
│       ├── 21-source-code-analysis.md
│       ├── 22-ai-llm-security.md
│       ├── 23-bot-ddos.md
│       ├── 24-browser-apis.md
│       └── 25-modern-security.md
├── memory-security.md                     # Score tracker
├── CLAUDE.md                              # Claude / Antigravity config
├── .cursorrules                           # Cursor config
├── .cursor/rules/security.mdc             # Cursor new format
├── .github/copilot-instructions.md        # GitHub Copilot config
├── .windsurfrules                         # Windsurf config
├── .clinerules                            # Cline config
├── AGENTS.md                              # OpenAI Codex CLI config
├── GEMINI.md                              # Gemini Code Assist config
└── .gitignore                             # Updated with security entries
```

## Key Commands

After installation, use these slash commands in your AI coding assistant:

### `/security-scan`
Quick 30-second scan focusing on critical issues only.

```javascript
// Example output:
// 🔴 CRITICAL #1 — Hardcoded Supabase service role key in .env.local
// 🔴 CRITICAL #2 — RLS disabled on 3 tables (users, orders, messages)
// 🟠 HIGH #3 — Missing rate limiting on /api/auth/login
// ⏱️ Scan completed in 28s
```

### `/security-audit`
Full audit that generates a security score (/100) and detailed report file.

```javascript
// Example output:
// ╔══════════════════════════════════════════════════╗
// ║      🔐  SECURITY AUDIT — myproject              ║
// ║         Stack: Next.js · Supabase · Vercel        ║
// ╠══════════════════════════════════════════════════╣
// ║  SECURITY SCORE  :  61 / 100  🟠                  ║
// ╠══════════════════════════════════════════════════╣
// ║  🔴  Secrets & Files          12/20  ← FIX NOW   ║
// ║  🟢  Auth & Sessions          16/20              ║
// ║  🔴  Database (Supabase RLS)   8/20  ← FIX NOW   ║
// ║  🟡  HTTP Headers             12/20              ║
// ...
// 📄 Full report → security-report.md
```

### `/security-fix`
Applies fixes with your approval. Always shows diffs before modifying code.

```javascript
// Example interaction:
// You: /security-fix rls
// AI: I'll enable RLS on 3 tables. Here's what will change:
//
// --- a/supabase/migrations/add_rls.sql
// +++ b/supabase/migrations/add_rls.sql
// @@ -0,0 +1,12 @@
// +ALTER TABLE users ENABLE ROW LEVEL SECURITY;
// +ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
// +ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
//
// Apply these changes? (y/n)
```

### `/security-status`
Shows your score history from `memory-security.md`.

```javascript
// Example output:
// | Date       | Score  | Critical | High | Notes              |
// |------------|--------|----------|------|--------------------|
// | 2025-05-01 | 61/100 | 2        | 3    | First audit        |
// | 2025-05-03 | 84/100 | 0        | 1    | Fixed RLS + secret |
// | 2025-05-10 | 97/100 | 0        | 0    | 🟢 Excellent       |
```

### `/security-history`
Shows before→after comparison to prove value.

### `/security-incident`
Full incident response playbook for when something goes wrong.

## Real-World Usage Examples

### Example 1: Next.js + Supabase Project

```bash
# Install security skill
npx @netxeo/security-skill

# In your AI assistant:
# You: /security-scan
```

**AI Response:**
```
🔴 CRITICAL #1 — Supabase service role key exposed in frontend
   File: .env.local:3
   Found: NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY=eyJhbG...
   Risk:  Full database access exposed to browser
   Fix:   Move to server-only env var (no NEXT_PUBLIC_ prefix)

🔴 CRITICAL #2 — RLS disabled on users table
   File: supabase/migrations/001_create_users.sql
   Risk:  Any authenticated user can read all user data
   Fix:   /security-fix rls

🟠 HIGH #3 — Missing rate limiting on auth endpoints
   File: app/api/auth/login/route.ts
   Risk:  Brute force attacks on login
   Fix:   Add @upstash/ratelimit middleware
```

**Apply a fix:**
```javascript
// You: /security-fix rls

// AI shows diff and asks for approval:
// --- a/supabase/migrations/002_enable_rls.sql
// +++ b/supabase/migrations/002_enable_rls.sql
// +ALTER TABLE users ENABLE ROW LEVEL SECURITY;
// +
// +CREATE POLICY "Users can read own data"
// +  ON users FOR SELECT
// +  TO authenticated
// +  USING (auth.uid() = id);
// +
// +CREATE POLICY "Users can update own data"
// +  ON users FOR UPDATE
// +  TO authenticated
// +  USING (auth.uid() = id);

// You: yes
// AI: ✅ Applied RLS policy. Run migration with: supabase db push
```

### Example 2: Express API with PostgreSQL

```javascript
// You: /security-audit

// AI detects SQL injection vulnerability
// 🔴 CRITICAL — SQL Injection in user search endpoint
//    File: routes/users.js:23
//    Code: db.query(`SELECT * FROM users WHERE name = '${req.query.name}'`)
//    Fix:  Use parameterized queries

// You: /security-fix sql-injection routes/users.js:23

// AI shows the fix:
// --- a/routes/users.js
// +++ b/routes/users.js
// @@ -20,7 +20,7 @@
//  router.get('/search', async (req, res) => {
// -  const results = await db.query(`SELECT * FROM users WHERE name = '${req.query.name}'`);
// +  const results = await db.query('SELECT * FROM users WHERE name = $1', [req.query.name]);
//    res.json(results.rows);
//  });

// You: yes
// AI: ✅ Fixed. SQL injection prevented using parameterized query.
```

### Example 3: Docker + CI/CD Security

```dockerfile
# You: /security-scan

# AI finds Docker security issues:
# 🔴 CRITICAL — Running as root in production container
#    File: Dockerfile:15
#    Code: USER root
#    Fix:  Create non-root user

# 🟠 HIGH — Secrets in environment variables
#    File: .github/workflows/deploy.yml:34
#    Code: DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
#    Fix:  Use secret management service (AWS Secrets Manager, Vault)

# You: /security-fix dockerfile

# AI rewrites Dockerfile:
# --- a/Dockerfile
# +++ b/Dockerfile
# @@ -12,5 +12,8 @@
#  COPY . .
#  RUN npm run build
#  
# -USER root
# +RUN addgroup -S appgroup && adduser -S appuser -G appgroup
# +RUN chown -R appuser:appgroup /app
# +USER appuser
# +
#  CMD ["npm", "start"]
```

## Configuration

### Environment Variables

No environment variables required. skill-file-security works entirely through instruction files.

### Custom Rules

Add custom security rules by creating `.skills/security/26-custom.md`:

```markdown
---
name: custom-security-rules
category: Custom
priority: high
---

# Custom Security Rules

## Rule 1: No console.log in production
- Check all `console.log()` calls
- Verify `NODE_ENV === 'production'` removes them
- Suggest using structured logging (winston, pino)

## Rule 2: API keys must be rotated every 90 days
- Check `memory-security.md` for last rotation date
- Alert if > 90 days since rotation
```

### Stack-Specific Configuration

skill-file-security auto-detects your stack from:
- `package.json` (Next.js, Express, React, Vue)
- `requirements.txt` / `Pipfile` (Django, Flask)
- `composer.json` (Laravel, Symfony)
- `Gemfile` (Rails)
- `pom.xml` / `build.gradle` (Spring Boot)
- `Dockerfile` (Docker)
- `supabase/` directory (Supabase)
- `firebase.json` (Firebase)

No manual configuration needed.

## Coverage

### OWASP Top 10 (2025)
- A01: Broken Access Control
- A02: Cryptographic Failures
- A03: Injection
- A04: Insecure Design
- A05: Security Misconfiguration
- A06: Vulnerable Components
- A07: Auth & Session Management Failures
- A08: Software & Data Integrity Failures
- A09: Logging & Monitoring Failures
- A10: SSRF

### CWE Top 25
All 25 covered, including:
- CWE-79 (XSS)
- CWE-89 (SQL Injection)
- CWE-22 (Path Traversal)
- CWE-352 (CSRF)
- CWE-434 (Unrestricted File Upload)
- CWE-862 (Missing Authorization)
- CWE-798 (Hard-coded Credentials)
- CWE-918 (SSRF)
- And 17 more...

### ASVS Level 3
- Session Management (V3)
- Access Control (V4)
- Cryptography (V6)
- Error Handling (V7)
- Data Protection (V8)
- Communications (V9)
- Business Logic (V11)
- Files & Resources (V12)
- API & Web Services (V13)
- Configuration (V14)

## Troubleshooting

### AI doesn't respond to /security-scan

**Cause:** AI assistant config file not properly loaded.

**Fix:**
```bash
# Reinstall for specific AI
npx @netxeo/security-skill --claude
# or
npx @netxeo/security-skill --cursor

# Restart your AI assistant after installation
```

### Security score not updating in memory-security.md

**Cause:** AI hasn't written to memory file yet.

**Fix:**
```javascript
// You: Update my security score after this audit
// AI will append new row to memory-security.md
```

### False positives in security scan

**Cause:** Context-specific code patterns that are actually safe.

**Fix:**
```javascript
// You: /security-scan --ignore-false-positives

// Or add exception comment in code:
const html = userInput; // security-skill-ignore: sanitized by DOMPurify on line 12
```

### Skill files not found

**Cause:** Installation didn't complete or files were deleted.

**Fix:**
```bash
# Reinstall
npx @netxeo/security-skill --yes

# Verify installation
ls -la .skills/security/
# Should show 25+ .md files
```

### Conflicts with existing .cursorrules or CLAUDE.md

**Cause:** You already have custom AI instructions.

**Fix:**
```bash
# Backup existing files
cp .cursorrules .cursorrules.backup
cp CLAUDE.md CLAUDE.md.backup

# Reinstall (will merge with existing)
npx @netxeo/security-skill --cursor

# Manually merge if needed
```

## Advanced Patterns

### CI/CD Integration

Add security checks to GitHub Actions:

```yaml
# .github/workflows/security.yml
name: Security Audit

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npx @netxeo/security-skill --yes
      - run: |
          # Use AI CLI to run audit
          # (requires AI with CLI support like aider or continue.dev)
          echo "/security-audit" | npx continue
```

### Pre-commit Hook

```bash
# .husky/pre-commit
#!/bin/sh
npx @netxeo/security-skill --yes
echo "/security-scan" | npx aider --yes-always
```

### Custom Security Categories

Extend with your own categories:

```bash
# Create custom category
cat > .skills/security/26-internal-compliance.md << 'EOF'
---
name: internal-compliance
category: Custom
priority: high
---

# Internal Compliance Rules

## PCI DSS Requirements
- Credit card numbers must be masked in logs
- Payment forms must use tokenization
- No credit card data in URLs or GET requests

## SOC 2 Requirements
- All database queries must be logged
- User actions must be auditable
- Access controls must be reviewed quarterly
EOF

# AI will now check these rules during scans
```

## Integration with Other Tools

skill-file-security complements (doesn't replace):
- **ESLint/Prettier**: Code style and basic checks
- **SonarQube**: Static analysis for code quality
- **Snyk/Dependabot**: Dependency vulnerability scanning
- **OWASP ZAP**: Dynamic application security testing

skill-file-security focuses on **semantic security analysis** that understands business logic and context — things static analyzers miss.

## Learn More

- **Official Website**: https://skill-file-security-website.vercel.app
- **NPM Package**: https://www.npmjs.com/package/@netxeo/security-skill
- **GitHub**: https://github.com/Netxeo/skill-file-security

---

**Made by developers who got tired of pushing secrets to production.** 🔐
