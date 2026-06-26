# Cybersecurity

## Patterns


---
  #### **Name**
Defense in Depth
  #### **Description**
Multiple security controls so failure of one doesn't compromise system
  #### **When**
Designing any security architecture
  #### **Example**
    Layer 1: WAF blocks common attacks
    Layer 2: Input validation at API boundary
    Layer 3: Parameterized queries prevent SQL injection
    Layer 4: Least privilege database user
    Layer 5: Encrypted data at rest
    Layer 6: Audit logging detects breaches
    
    Each layer catches what others miss.
    

---
  #### **Name**
Least Privilege
  #### **Description**
Grant minimum access required for a task, nothing more
  #### **When**
Designing permissions, roles, or access controls
  #### **Example**
    // BAD: One admin role for everything
    user.role = 'admin'
    
    // GOOD: Granular permissions
    user.permissions = ['orders:read', 'orders:create']
    
    // GOOD: Scoped to resources
    user.access = {
      team: 'sales',
      actions: ['read', 'write'],
      resources: ['orders', 'customers']
    }
    
    // Database: App user can't DROP or GRANT
    GRANT SELECT, INSERT, UPDATE ON app.* TO 'app_user'@'%';
    

---
  #### **Name**
Input Validation Boundary
  #### **Description**
All external input validated at system boundary before processing
  #### **When**
Handling any user input, API requests, or external data
  #### **Example**
    import { z } from 'zod'
    
    const CreateUserSchema = z.object({
      email: z.string().email().max(255),
      password: z.string().min(12).max(128),
      name: z.string().min(1).max(100)
    })
    
    app.post('/users', (req, res) => {
      // Validate at boundary
      const result = CreateUserSchema.safeParse(req.body)
      if (!result.success) {
        return res.status(400).json({ error: result.error })
      }
    
      // Now safe to use result.data
      createUser(result.data)
    })
    

---
  #### **Name**
Secure by Default
  #### **Description**
Systems are secure out of the box, insecurity requires explicit opt-in
  #### **When**
Designing APIs, defaults, or configurations
  #### **Example**
    // WRONG: Security is opt-in
    app.get('/data', (req, res) => { ... })
    app.get('/admin', requireAuth, (req, res) => { ... })
    
    // RIGHT: Security is default
    app.use(requireAuth)  // All routes protected
    app.get('/public/*', allowPublic)  // Explicit exceptions
    
    // Cookie defaults
    res.cookie('session', token, {
      httpOnly: true,   // Default: can't access from JS
      secure: true,     // Default: HTTPS only
      sameSite: 'lax'   // Default: CSRF protection
    })
    

---
  #### **Name**
Secrets Management
  #### **Description**
Secrets stored securely, never in code, with rotation capability
  #### **When**
Handling API keys, passwords, tokens, or any credentials
  #### **Example**
    // WRONG: Secrets in code
    const API_KEY = 'sk_live_abc123'
    
    // RIGHT: Environment variables (development)
    const apiKey = process.env.API_KEY
    
    // RIGHT: Secrets manager (production)
    const { SecretManagerServiceClient } = require('@google-cloud/secret-manager')
    const client = new SecretManagerServiceClient()
    
    async function getSecret(name) {
      const [version] = await client.accessSecretVersion({
        name: `projects/my-project/secrets/${name}/versions/latest`
      })
      return version.payload.data.toString()
    }
    
    // Pre-commit: gitleaks
    # .pre-commit-config.yaml
    - repo: https://github.com/gitleaks/gitleaks
      hooks:
        - id: gitleaks
    

---
  #### **Name**
Session Security
  #### **Description**
Sessions cryptographically random, properly expiring, server-validated
  #### **When**
Implementing authentication or session management
  #### **Example**
    import { randomBytes } from 'crypto'
    
    // Cryptographically random session ID
    const sessionId = randomBytes(32).toString('hex')
    
    // Session with proper expiration
    const session = {
      id: sessionId,
      userId: user.id,
      createdAt: Date.now(),
      expiresAt: Date.now() + (1000 * 60 * 60),  // 1 hour
      lastActive: Date.now()
    }
    
    // Rotate session after authentication
    app.post('/login', async (req, res) => {
      const user = await authenticate(req.body)
      await destroySession(req.sessionId)  // Old session
      const newSession = await createSession(user.id)  // New session
      res.cookie('session', newSession.id, { httpOnly: true, secure: true })
    })
    
    // Server-side invalidation on logout
    app.post('/logout', async (req, res) => {
      await destroySession(req.sessionId)
      res.clearCookie('session')
    })
    

## Anti-Patterns


---
  #### **Name**
Security Through Obscurity
  #### **Description**
Relying on hidden URLs, obfuscated code, or secret algorithms
  #### **Why**
Obscurity provides no real security. Attackers will find hidden endpoints.
  #### **Instead**
Implement proper authentication and authorization. Assume attackers know your code.

---
  #### **Name**
Client-Side Security
  #### **Description**
Relying on JavaScript validation or hiding elements for security
  #### **Why**
Attackers bypass the client entirely. All client-side code can be modified.
  #### **Instead**
All security checks on the server. Client is for UX, server is for security.

---
  #### **Name**
Rolling Your Own Crypto
  #### **Description**
Implementing custom encryption, hashing, or security algorithms
  #### **Why**
Crypto is extremely hard. Custom implementations have fatal flaws.
  #### **Instead**
Use proven libraries (bcrypt, libsodium). Use standard algorithms (AES-256-GCM).

---
  #### **Name**
Blanket Trust
  #### **Description**
Trusting internal services, previous validation, or "safe" data sources
  #### **Why**
Internal networks get compromised. Assumptions fail. Trust boundaries shift.
  #### **Instead**
Validate at every boundary. Zero trust architecture. Defense in depth.

---
  #### **Name**
Logging Sensitive Data
  #### **Description**
Writing passwords, tokens, PII to logs for debugging
  #### **Why**
Logs are stored, shared, and often accessible. Data exposure through logs.
  #### **Instead**
Redact sensitive fields. Use structured logging. Review log output.

---
  #### **Name**
Error Detail Exposure
  #### **Description**
Returning stack traces, SQL queries, or internal details in errors
  #### **Why**
Reveals system internals to attackers. Aids exploitation.
  #### **Instead**
Generic errors in production. Log details internally. Use request IDs for support.