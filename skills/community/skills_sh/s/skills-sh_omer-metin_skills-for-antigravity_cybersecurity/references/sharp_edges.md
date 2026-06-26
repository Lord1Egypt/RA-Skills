# Cybersecurity - Sharp Edges

## Hardcoded Secret

### **Id**
hardcoded-secret
### **Summary**
Credentials, API keys, or secrets committed to source code
### **Severity**
critical
### **Situation**
Secrets in code that get into version history, logs, and attacker hands
### **Why**
  Git history is forever. Removing from latest commit ≠ removed. Bot scanners find
  secrets in seconds. One exposed key = full breach. Secrets end up in CI/CD logs,
  backup systems, and all developer machines that clone the repo.
  
### **Solution**
  # 1. Use environment variables
  const apiKey = process.env.API_KEY
  
  # 2. Use secrets managers
  const { data } = await vault.read('secret/api-key')
  
  # 3. Use .gitignore properly
  .env
  .env.local
  *.pem
  secrets/
  
  # 4. Pre-commit hooks
  # .pre-commit-config.yaml
  - repo: https://github.com/gitleaks/gitleaks
    hooks:
      - id: gitleaks
  
  # 5. If already leaked:
  - Rotate immediately (new credentials)
  - Old ones are compromised
  - History cleanup is not enough
  
  # TOOLS
  - gitleaks: Pre-commit scanning
  - trufflehog: History scanning
  - Doppler/Vault: Secrets management
  
### **Symptoms**
  - API keys in source code
  - .env files committed
  - Credentials in config files
  - Secrets in CI logs
### **Detection Pattern**
sk_live_|AKIA[A-Z0-9]{16}|password\\s*=\\s*["'][^"']{8,}|api[_-]?key\\s*=\\s*["']

## Sql Injection

### **Id**
sql-injection
### **Summary**
Building SQL queries with string concatenation
### **Severity**
critical
### **Situation**
User input directly concatenated into SQL queries
### **Why**
  SQL injection is #1 on OWASP Top 10. Attackers can read, modify, or delete entire
  databases. One vulnerable endpoint = full database access. Automated tools find
  and exploit in minutes.
  
### **Solution**
  # WRONG: Direct string concatenation
  const query = `SELECT * FROM users WHERE id = ${userId}`
  const query = "SELECT * FROM users WHERE name = '" + name + "'"
  
  # RIGHT: Parameterized queries (ALWAYS)
  const { rows } = await pool.query(
    'SELECT * FROM users WHERE id = $1',
    [userId]
  )
  
  # RIGHT: With ORM (Prisma)
  const user = await prisma.user.findUnique({
    where: { id: userId }
  })
  
  # Defense in depth
  if (!isValidUUID(userId)) {
    throw new ValidationError()
  }
  
  # Least privilege database user
  # App DB user should NOT have DROP, GRANT permissions
  
### **Symptoms**
  - String concatenation in SQL
  - Template literals with user input in queries
  - No parameterized queries
  - Raw SQL with user input
### **Detection Pattern**
SELECT.*\$\{|SELECT.*\+\s*\w+|query\s*\(`[^`]*\$\{

## Xss Vulnerability

### **Id**
xss-vulnerability
### **Summary**
Rendering untrusted data without proper encoding
### **Severity**
critical
### **Situation**
User content inserted into HTML without escaping
### **Why**
  XSS is #2 on OWASP Top 10. Attackers can steal sessions, credentials, and execute
  code as users. Persisted XSS affects every user who views the content.
  
### **Solution**
  # WRONG: Direct HTML insertion
  element.innerHTML = userComment
  dangerouslySetInnerHTML={{ __html: userContent }}
  
  # RIGHT: Framework auto-escaping (React, Vue)
  <div>{userContent}</div>  // Safe
  
  # RIGHT: Content Security Policy
  Content-Security-Policy: default-src 'self';
    script-src 'self';
    style-src 'self' 'unsafe-inline'
  
  # RIGHT: Sanitize if HTML required
  import DOMPurify from 'dompurify'
  const clean = DOMPurify.sanitize(dirty)
  
  # RIGHT: HTTPOnly cookies
  Set-Cookie: session=abc; HttpOnly; Secure
  
  # NEVER:
  - innerHTML with user content
  - eval() with user content
  - document.write() with user content
  
### **Symptoms**
  - innerHTML with user data
  - dangerouslySetInnerHTML usage
  - Missing CSP headers
  - User content in script tags
### **Detection Pattern**
innerHTML\s*=|dangerouslySetInnerHTML|v-html|document\.write

## Missing Authentication

### **Id**
missing-authentication
### **Summary**
API endpoints or pages accessible without authentication
### **Severity**
critical
### **Situation**
Protected resources accessible by anyone
### **Why**
  Frontend is not a security boundary. Anyone can call your API directly. Every
  endpoint needs authentication. "Hidden" URLs are not secure.
  
### **Solution**
  # WRONG: Frontend checks but API doesn't
  if (user.isAdmin) { showAdminPanel() }
  
  app.get('/api/admin/users', (req, res) => {
    // No auth check!
    return getAllUsers()
  })
  
  # RIGHT: Auth on every protected endpoint
  app.get('/api/admin/users', authMiddleware, (req, res) => {
    // Now protected
  })
  
  # RIGHT: Default deny
  app.use('/api/*', authMiddleware)  // All protected
  app.get('/api/public/*', publicMiddleware)  // Explicit exceptions
  
  # AUTH CHECKLIST
  □ All admin endpoints protected
  □ All data endpoints protected
  □ File/media endpoints protected
  □ Webhooks verified
  □ No auth bypass routes
  
### **Symptoms**
  - Admin endpoints without auth
  - APIs assuming frontend auth
  - No middleware on routes
  - Inconsistent auth patterns
### **Detection Pattern**
app\.(get|post|put|delete)\s*\([^,]*,\s*\(req

## Missing Authorization

### **Id**
missing-authorization
### **Summary**
User can access another user's resources (IDOR/BOLA)
### **Severity**
critical
### **Situation**
Authentication without ownership/access verification
### **Why**
  Authentication ≠ Authorization. "Who are you?" ≠ "What can you access?"
  BOLA/IDOR is #1 API security risk. Easy to exploit, often overlooked.
  
### **Solution**
  # WRONG: Authenticated but not authorized
  app.get('/api/orders/:id', authMiddleware, (req, res) => {
    const order = await getOrder(req.params.id)
    // Missing: Is req.user allowed to access this order?
    return res.json(order)
  })
  
  # RIGHT: Check ownership on every request
  app.get('/api/orders/:id', auth, async (req, res) => {
    const order = await getOrder(req.params.id)
  
    if (order.userId !== req.user.id) {
      return res.status(403).json({ error: 'Forbidden' })
    }
  
    return res.json(order)
  })
  
  # RIGHT: Scope queries to user
  const order = await prisma.order.findFirst({
    where: {
      id: orderId,
      userId: req.user.id  // Scoped
    }
  })
  
  # Use UUIDs not sequential IDs
  /orders/550e8400-e29b-41d4-a716-446655440000
  
### **Symptoms**
  - No ownership checks
  - Sequential IDs exposed
  - Generic getById functions
  - Missing authorization middleware
### **Detection Pattern**
findUnique\s*\(\s*\{[^}]*id:|getOne\s*\([^,]*\)

## Insecure Password Storage

### **Id**
insecure-password-storage
### **Summary**
Passwords stored in plaintext, weak hashing, or reversible encryption
### **Severity**
critical
### **Situation**
Password storage that doesn't use modern password hashing
### **Why**
  Databases get breached. Assume your password table will be stolen. Proper hashing
  is the last line of defense. Weak hashing = millions of accounts compromised.
  
### **Solution**
  # WRONG
  user.password = req.body.password  // Plaintext
  user.password = md5(password)  // MD5 broken
  user.password = sha256(password)  // No salt, rainbow tables
  
  # RIGHT: Use bcrypt or argon2
  import bcrypt from 'bcrypt'
  
  // Hash password (on signup/change)
  const hash = await bcrypt.hash(password, 12)  // 12 rounds
  
  // Verify password (on login)
  const valid = await bcrypt.compare(password, hash)
  
  # HASHING ALGORITHMS
  ✓ bcrypt (battle-tested)
  ✓ argon2id (modern, recommended)
  ✓ scrypt (high memory)
  ✗ MD5 (broken)
  ✗ SHA1 (broken)
  ✗ SHA256 alone (rainbow tables)
  
### **Symptoms**
  - MD5 or SHA1 for passwords
  - No salt in hashing
  - Plaintext password storage
  - Reversible encryption for passwords
### **Detection Pattern**
md5\(|sha1\(|createHash\(["']md5|createHash\(["']sha1

## Csrf Vulnerability

### **Id**
csrf-vulnerability
### **Summary**
State-changing requests without CSRF protection
### **Severity**
high
### **Situation**
POST/PUT/DELETE requests that don't verify request origin
### **Why**
  Browsers send cookies with every request, including from other sites. User doesn't
  have to click anything. One visit to malicious site = attack.
  
### **Solution**
  # 1. CSRF tokens
  const csrfToken = generateCsrfToken()
  req.session.csrf = csrfToken
  
  <input type="hidden" name="_csrf" value="${csrfToken}" />
  
  if (req.body._csrf !== req.session.csrf) {
    throw new Error('CSRF validation failed')
  }
  
  # 2. SameSite cookies
  Set-Cookie: session=abc; SameSite=Lax; Secure; HttpOnly
  
  # 3. Custom headers for AJAX
  fetch('/api/action', {
    headers: { 'X-CSRF-Token': token }
  })
  
  # 4. Origin header checking
  const origin = req.get('Origin')
  if (!allowedOrigins.includes(origin)) {
    throw new Error('Invalid origin')
  }
  
### **Symptoms**
  - No CSRF tokens in forms
  - Missing SameSite cookie attribute
  - No origin validation
  - State changes via GET
### **Detection Pattern**
method="POST"(?![\\s\\S]*csrf)|Set-Cookie:(?!.*SameSite)

## Broken Session

### **Id**
broken-session
### **Summary**
Sessions that are predictable, never expire, or improperly invalidated
### **Severity**
high
### **Situation**
Weak session management allowing hijacking or persistent access
### **Why**
  Sessions are the keys to the kingdom. Weak sessions = account takeover. Stale
  sessions = persistent access. Poor logout = sessions live forever.
  
### **Solution**
  # Cryptographically random session IDs
  import { randomBytes } from 'crypto'
  const sessionId = randomBytes(32).toString('hex')
  
  # Set appropriate expiration
  const session = createSession({
    expiresIn: '1h',           // Absolute
    inactiveTimeout: '15m'     // Inactivity
  })
  
  # Invalidate on logout (server-side)
  app.post('/logout', (req, res) => {
    await destroySession(req.sessionId)  // Server invalidation
    res.clearCookie('session')
  })
  
  # Rotate session after authentication
  app.post('/login', async (req, res) => {
    const user = await authenticate(req.body)
    await destroySession(req.sessionId)  // Old session
    const newSession = await createSession(user.id)  // New session
    res.cookie('session', newSession.id)
  })
  
### **Symptoms**
  - Predictable session IDs
  - No session expiration
  - Client-only logout
  - No session rotation
### **Detection Pattern**
sessionId.*=.*Date\\.now|sessionId.*=.*timestamp

## Exposed Error Details

### **Id**
exposed-error-details
### **Summary**
Detailed error messages, stack traces, or debug info in production
### **Severity**
high
### **Situation**
Internal system details exposed to users/attackers
### **Why**
  Error details reveal database schema, technology stack, file paths, configuration,
  credentials, and valid usernames. Helps attackers understand and exploit system.
  
### **Solution**
  # Generic errors in production
  app.use((err, req, res, next) => {
    // Log full error internally
    logger.error(err)
  
    // Return generic message
    if (process.env.NODE_ENV === 'production') {
      return res.status(500).json({
        error: 'An error occurred',
        requestId: req.id  // For support
      })
    }
  
    // Details in development only
    return res.status(500).json({
      error: err.message,
      stack: err.stack
    })
  })
  
  # Consistent error responses
  // Don't reveal if user exists
  // BAD: "No user with that email"
  // GOOD: "Invalid email or password"
  
  # Hide headers
  app.disable('x-powered-by')
  
### **Symptoms**
  - Stack traces in responses
  - SQL queries in errors
  - Config details exposed
  - Different errors for existing vs non-existing users
### **Detection Pattern**
res\\.json\\([^)]*stack|res\\.json\\([^)]*err\\.message

## Insecure Direct Object Reference

### **Id**
insecure-direct-object-reference
### **Summary**
Using user-supplied identifiers without validation
### **Severity**
high
### **Situation**
File paths or object references built from user input
### **Why**
  Path traversal allows access to arbitrary server files. User input should never
  be used directly in file paths, template names, or include statements.
  
### **Solution**
  # WRONG: Direct path usage
  app.get('/download', (req, res) => {
    const file = req.query.file
    res.download(`/uploads/${file}`)
  })
  // Attack: GET /download?file=../../../etc/passwd
  
  # RIGHT: Whitelist allowed values
  const allowedFiles = ['report.pdf', 'invoice.pdf']
  if (!allowedFiles.includes(req.query.file)) {
    return res.status(400).json({ error: 'Invalid file' })
  }
  
  # RIGHT: Validate paths
  const requestedPath = path.join('/uploads', req.query.file)
  const resolvedPath = path.resolve(requestedPath)
  
  if (!resolvedPath.startsWith('/uploads/')) {
    return res.status(403).json({ error: 'Access denied' })
  }
  
  # RIGHT: Use indirect references
  // Instead of: /files/secret_report.pdf
  // Use: /files/a1b2c3d4-uuid
  // Map internally to actual file
  
### **Symptoms**
  - User input in file paths
  - Template names from parameters
  - No path validation
  - Direct file access
### **Detection Pattern**
path\\.join\\([^)]*req\\.|res\\.download\\([^)]*req\\.

## Weak Cryptography

### **Id**
weak-cryptography
### **Summary**
Using deprecated algorithms or implementing crypto incorrectly
### **Severity**
high
### **Situation**
DES, MD5, ECB mode, predictable IVs, hardcoded keys
### **Why**
  Crypto is hard. One mistake = no security. Deprecated algorithms are deprecated
  for a reason. Custom crypto is almost always wrong.
  
### **Solution**
  # WRONG
  crypto.createCipher('des', key)  // DES is broken
  crypto.createHash('md5')  // MD5 is broken
  crypto.createCipheriv('aes-256-ecb', key, null)  // ECB patterns visible
  const iv = Buffer.from('0000000000000000')  // Predictable IV
  
  # RIGHT: Use modern algorithms
  const cipher = crypto.createCipheriv(
    'aes-256-gcm',
    key,
    crypto.randomBytes(16)  // Random IV
  )
  
  # RIGHT: Use libraries
  // Node.js: libsodium, tweetnacl
  // Don't implement yourself
  
  # CRYPTO CHECKLIST
  □ AES-256-GCM or ChaCha20-Poly1305
  □ Random IVs for each encryption
  □ Keys from secure key store
  □ HTTPS for transport
  □ No deprecated algorithms
  
### **Symptoms**
  - DES or 3DES usage
  - MD5 or SHA1 for security
  - ECB mode
  - Static/predictable IVs
### **Detection Pattern**
createCipher\(["']des|createHash\(["']md5|aes-.*-ecb

## Unvalidated Redirect

### **Id**
unvalidated-redirect
### **Summary**
Redirecting users based on user-supplied URLs
### **Severity**
medium
### **Situation**
Open redirects that can be abused for phishing
### **Why**
  Open redirects enable phishing (fake login pages), malware distribution, OAuth
  token theft. Users trust your domain but get redirected to malicious sites.
  
### **Solution**
  # WRONG: Open redirect
  app.get('/redirect', (req, res) => {
    res.redirect(req.query.url)
  })
  
  # RIGHT: Whitelist allowed destinations
  const allowedRedirects = ['/dashboard', '/settings', '/logout']
  if (!allowedRedirects.includes(req.query.url)) {
    return res.redirect('/')
  }
  
  # RIGHT: Validate URL is internal
  function isInternalUrl(url) {
    try {
      const parsed = new URL(url, 'https://yoursite.com')
      return parsed.hostname === 'yoursite.com'
    } catch {
      return false
    }
  }
  
  # RIGHT: Use indirect references
  // Instead of: /redirect?url=https://...
  // Use: /redirect?target=dashboard
  // Map 'dashboard' to internal URL
  
### **Symptoms**
  - Full URLs in query parameters
  - No redirect validation
  - External URLs allowed
  - No whitelist
### **Detection Pattern**
res\\.redirect\\(req\\.(query|params|body)