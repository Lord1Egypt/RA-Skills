---
name: tls-configuration-auditor
description: Audit TLS/SSL configuration of servers and applications. Check protocol versions, cipher suites, certificate chain validity, HSTS headers, and compliance with security standards (PCI-DSS, NIST, Mozilla recommendations).
---

# TLS Configuration Auditor

Audit TLS/SSL configuration for security weaknesses. Check protocol versions (TLS 1.2/1.3 only), cipher suite strength, certificate chain validity, HSTS deployment, key sizes, and compliance with Mozilla, NIST, and PCI-DSS guidelines.

Use when: "check TLS config", "SSL audit", "is our TLS secure", "cipher suite review", "certificate check", "security headers audit", "PCI compliance scan", or before security assessments.

## Commands

### 1. `audit` — Full TLS Audit

#### Step 1: Certificate Chain

```bash
# Get certificate details
echo | openssl s_client -connect $HOST:443 -servername $HOST 2>/dev/null | openssl x509 -noout \
  -subject -issuer -dates -fingerprint -ext subjectAltName 2>&1

# Check full chain
echo | openssl s_client -connect $HOST:443 -servername $HOST -showcerts 2>/dev/null | \
  awk '/BEGIN CERT/,/END CERT/{print}' | \
  openssl x509 -noout -subject -issuer -dates 2>&1

# Days until expiry
echo | openssl s_client -connect $HOST:443 -servername $HOST 2>/dev/null | \
  openssl x509 -noout -enddate 2>&1 | \
  python3 -c "
import sys, datetime
line = sys.stdin.read().strip()
date_str = line.split('=')[1]
expiry = datetime.datetime.strptime(date_str, '%b %d %H:%M:%S %Y %Z')
days = (expiry - datetime.datetime.utcnow()).days
status = '🔴 CRITICAL' if days < 7 else '🟡 WARNING' if days < 30 else '🟢 OK'
print(f'{status}: Certificate expires in {days} days ({expiry.date()})')
"
```

#### Step 2: Protocol Versions

```bash
# Test each TLS version
for proto in ssl3 tls1 tls1_1 tls1_2 tls1_3; do
  result=$(echo | openssl s_client -connect $HOST:443 -$proto 2>&1)
  if echo "$result" | grep -q "CONNECTED"; then
    echo "$proto: ENABLED"
  else
    echo "$proto: DISABLED"
  fi
done
```

**Expected results:**
- SSLv3: DISABLED (POODLE vulnerability)
- TLS 1.0: DISABLED (deprecated, PCI non-compliant since 2018)
- TLS 1.1: DISABLED (deprecated)
- TLS 1.2: ENABLED (minimum acceptable)
- TLS 1.3: ENABLED (preferred)

#### Step 3: Cipher Suites

```bash
# List supported ciphers
nmap --script ssl-enum-ciphers -p 443 $HOST 2>/dev/null || \
  openssl s_client -connect $HOST:443 -cipher 'ALL' 2>&1 | grep "Cipher is"

# Check for weak ciphers
for cipher in RC4 DES 3DES NULL EXPORT ANON MD5; do
  result=$(echo | openssl s_client -connect $HOST:443 -cipher "$cipher" 2>&1)
  if echo "$result" | grep -q "CONNECTED"; then
    echo "🔴 WEAK CIPHER SUPPORTED: $cipher"
  fi
done
```

**Flag as weak:**
- RC4 (biased output, practical attacks)
- DES/3DES (SWEET32, small block size)
- NULL ciphers (no encryption)
- EXPORT ciphers (FREAK/Logjam, 40/56-bit keys)
- Anonymous DH (no authentication, MITM)
- MD5 for MAC (collision attacks)

#### Step 4: Security Headers

```bash
curl -sI "https://$HOST" | grep -iE "^(strict-transport|x-frame|x-content|content-security|referrer|permissions|x-xss)" 2>&1
```

Check for:
- `Strict-Transport-Security` (HSTS) — should be present, max-age ≥ 31536000
- `includeSubDomains` — recommended
- `preload` — recommended for public sites
- HSTS preload list membership

#### Step 5: Key Strength

```bash
echo | openssl s_client -connect $HOST:443 2>/dev/null | openssl x509 -noout -text | \
  grep -E "Public-Key:|Signature Algorithm:" 2>&1
```

- RSA: minimum 2048-bit (4096 preferred)
- ECDSA: minimum 256-bit (P-256 or P-384)
- Signature: SHA-256 or better (SHA-1 is deprecated)

#### Step 6: Generate Report

```markdown
# TLS Configuration Audit — $HOST

## Overall Grade: A / B / C / D / F

## Certificate
- Subject: *.example.com
- Issuer: Let's Encrypt R3
- Valid: 2026-01-15 to 2026-04-15
- Expiry: 🟢 47 days remaining
- Key: ECDSA P-256 ✅
- Signature: SHA-256 ✅
- Chain: Complete ✅

## Protocol Support
| Protocol | Status | Compliance |
|----------|--------|------------|
| TLS 1.3 | ✅ Enabled | Required (modern) |
| TLS 1.2 | ✅ Enabled | Required (intermediate) |
| TLS 1.1 | ✅ Disabled | PCI-DSS compliant |
| TLS 1.0 | ✅ Disabled | PCI-DSS compliant |
| SSLv3 | ✅ Disabled | POODLE-safe |

## Cipher Suites
- Strong ciphers only: ✅
- Forward secrecy (ECDHE/DHE): ✅
- No weak ciphers: ✅

## Security Headers
- HSTS: ✅ max-age=31536000; includeSubDomains; preload
- X-Frame-Options: ⚠️ Missing
- CSP: ❌ Not configured

## Recommendations
1. Add Content-Security-Policy header
2. Add X-Frame-Options: DENY
3. Consider ECDSA certificate for better performance
```

### 2. `compare` — Compare Against Mozilla Presets

Check configuration against Mozilla's three recommended profiles:
- **Modern:** TLS 1.3 only, strongest ciphers
- **Intermediate:** TLS 1.2+, broad compatibility
- **Old:** TLS 1.0+, maximum compatibility (not recommended)

### 3. `monitor` — Set Up Certificate Expiry Alerts

Generate a monitoring script or CI job that checks certificate expiry daily and alerts at 30/14/7/1 day thresholds.
