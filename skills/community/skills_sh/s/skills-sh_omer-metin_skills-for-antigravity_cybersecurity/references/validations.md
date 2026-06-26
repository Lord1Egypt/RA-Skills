# Cybersecurity - Validations

## Hardcoded Secret

### **Id**
sec-hardcoded-secret
### **Severity**
error
### **Type**
regex
### **Pattern**
AKIA[A-Z0-9]{16}|sk_live_[a-zA-Z0-9]+|sk_test_[a-zA-Z0-9]+|password\s*=\s*["'][^"']{8,}["']|secret\s*=\s*["'][^"']{8,}["']|api[_-]?key\s*=\s*["'][^"']{16,}["']|private[_-]?key\s*=\s*["'][^"']{16,}["']
### **Message**
Hardcoded secret detected. Use environment variables or secrets manager.
### **Fix Action**
Move to process.env.SECRET_NAME or secrets manager
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx
  - *.json
  - *.yaml
  - *.yml

## Potential SQL Injection

### **Id**
sec-sql-injection
### **Severity**
error
### **Type**
regex
### **Pattern**
SELECT.*\${|INSERT.*\${|UPDATE.*\${|DELETE.*\${|query\s*\(`[^`]*\${|execute\s*\(`[^`]*\${
### **Message**
String interpolation in SQL query. Use parameterized queries.
### **Fix Action**
Use parameterized query: query('SELECT * FROM users WHERE id = $1', [id])
### **Applies To**
  - *.ts
  - *.js

## XSS via innerHTML

### **Id**
sec-xss-innerhtml
### **Severity**
error
### **Type**
regex
### **Pattern**
innerHTML\s*=\s*[^"']+(?:req|user|input|data|param)|dangerouslySetInnerHTML\s*=\s*\{\s*\{\s*__html|v-html\s*=
### **Message**
Potential XSS vulnerability. Sanitize user content before rendering.
### **Fix Action**
Use DOMPurify.sanitize() or framework auto-escaping
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx
  - *.vue

## Dangerous eval Usage

### **Id**
sec-eval-usage
### **Severity**
error
### **Type**
regex
### **Pattern**
eval\s*\(|new\s+Function\s*\(|setTimeout\s*\(\s*["']|setInterval\s*\(\s*["']
### **Message**
eval() or dynamic code execution. Avoid or use safer alternatives.
### **Fix Action**
Replace with JSON.parse() for data or explicit logic
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Weak Hash Algorithm

### **Id**
sec-weak-hash
### **Severity**
error
### **Type**
regex
### **Pattern**
createHash\s*\(\s*["']md5["']|createHash\s*\(\s*["']sha1["']|md5\s*\(|sha1\s*\(
### **Message**
MD5/SHA1 is cryptographically broken. Use SHA-256 or bcrypt for passwords.
### **Fix Action**
Use createHash('sha256') or bcrypt for passwords
### **Applies To**
  - *.ts
  - *.js

## Weak Cipher

### **Id**
sec-weak-cipher
### **Severity**
error
### **Type**
regex
### **Pattern**
createCipher\s*\(\s*["']des|createCipher\s*\(\s*["']rc4|aes-.*-ecb
### **Message**
Weak or broken cipher algorithm. Use AES-256-GCM.
### **Fix Action**
Use createCipheriv('aes-256-gcm', key, iv)
### **Applies To**
  - *.ts
  - *.js

## Missing CSRF Protection

### **Id**
sec-no-csrf
### **Severity**
warning
### **Type**
regex
### **Pattern**
method\s*=\s*["']POST["'](?![\s\S]*csrf)|method\s*=\s*["']post["'](?![\s\S]*csrf)
### **Message**
Form without CSRF token. Add CSRF protection.
### **Fix Action**
Add CSRF token: <input type='hidden' name='_csrf' value={csrfToken} />
### **Applies To**
  - *.html
  - *.tsx
  - *.jsx
  - *.vue

## Insecure Cookie

### **Id**
sec-insecure-cookie
### **Severity**
warning
### **Type**
regex
### **Pattern**
Set-Cookie:(?!.*HttpOnly)|Set-Cookie:(?!.*Secure)|res\.cookie\([^)]*\)(?!.*httpOnly)
### **Message**
Cookie without HttpOnly or Secure flag. Add security flags.
### **Fix Action**
Set cookie with { httpOnly: true, secure: true, sameSite: 'lax' }
### **Applies To**
  - *.ts
  - *.js

## Open Redirect

### **Id**
sec-open-redirect
### **Severity**
warning
### **Type**
regex
### **Pattern**
res\.redirect\s*\(\s*req\.(query|params|body)|redirect\s*:\s*req\.(query|params|body)|location\s*=\s*[^"']*req\.
### **Message**
Open redirect vulnerability. Validate redirect URLs.
### **Fix Action**
Whitelist allowed redirect destinations
### **Applies To**
  - *.ts
  - *.js

## Path Traversal

### **Id**
sec-path-traversal
### **Severity**
error
### **Type**
regex
### **Pattern**
path\.join\s*\([^)]*req\.|readFile\s*\([^)]*req\.|res\.download\s*\([^)]*req\.|res\.sendFile\s*\([^)]*req\.
### **Message**
User input in file path. Validate and sanitize path.
### **Fix Action**
Validate path doesn't escape intended directory
### **Applies To**
  - *.ts
  - *.js

## Exposed Stack Trace

### **Id**
sec-exposed-stack
### **Severity**
warning
### **Type**
regex
### **Pattern**
res\.json\s*\([^)]*stack|res\.send\s*\([^)]*stack|res\.json\s*\([^)]*err\.message
### **Message**
Stack trace or error details in response. Hide in production.
### **Fix Action**
Return generic error message in production
### **Applies To**
  - *.ts
  - *.js

## Command Injection

### **Id**
sec-command-injection
### **Severity**
error
### **Type**
regex
### **Pattern**
exec\s*\(`[^`]*\${|exec\s*\([^)]*\+\s*\w+|spawn\s*\([^)]*req\.|execSync\s*\([^)]*req\.
### **Message**
User input in shell command. High risk of command injection.
### **Fix Action**
Use parameterized commands or avoid shell execution
### **Applies To**
  - *.ts
  - *.js

## CORS Wildcard

### **Id**
sec-cors-wildcard
### **Severity**
warning
### **Type**
regex
### **Pattern**
Access-Control-Allow-Origin:\s*\*|origin:\s*['"]\\*['"]|cors\s*\(\s*\)
### **Message**
CORS allows all origins. Restrict to specific domains.
### **Fix Action**
Specify allowed origins: cors({ origin: 'https://yoursite.com' })
### **Applies To**
  - *.ts
  - *.js

## JWT None Algorithm

### **Id**
sec-jwt-none-alg
### **Severity**
error
### **Type**
regex
### **Pattern**
algorithms\s*:\s*\[\s*["']none["']|algorithm\s*:\s*["']none["']
### **Message**
JWT 'none' algorithm allows unsigned tokens. Never allow.
### **Fix Action**
Specify allowed algorithms: algorithms: ['HS256', 'RS256']
### **Applies To**
  - *.ts
  - *.js