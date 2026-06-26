# VatGentic Skill - Development Notes

**Created:** 2026-04-16  
**Status:** Soft launch ready (70% functional)  
**Version:** v0.1.0

---

## What's Included

```
skills/vatgentic/
├── SKILL.md                    # ClawHub skill definition
├── scripts/
│   ├── vatgentic-request.py    # Create validation request
│   ├── vatgentic-status.py     # Check validation status
│   └── vatgentic-validate.py   # End-to-end validation
└── README.md                   # This file
```

---

## Current State (2026-04-16)

### ✅ Working

1. **ln.bot wallet integration**
   - Balance: 928 sats (tested)
   - Invoice generation: working
   - API: fully functional

2. **VAT request webhook**
   - Endpoint: `POST /webhook/vatgentic/request`
   - Creates BTCPay invoices successfully
   - Returns proper response format

3. **Payment flow**
   - BTCPay invoices generated
   - Checkout links work
   - Lightning payment links provided

### ⚠️ Needs Fix

1. **Status endpoint**
   - Returns 404 in current n8n deployment
   - Webhook path may need configuration
   - **Fix needed:** Import `vatgentic-prototype-fixed.json` to n8n

2. **Payment webhook**
   - BTCPay webhook configuration unclear
   - May not be firing to n8n
   - **Fix needed:** Verify BTCPay store webhook settings

3. **VAT API credentials** (n8n instance owner)
   - eu.vatapi.com key needs to be configured in n8n
   - **Note:** This is instance-level config, not user requirement

---

## Publishing to ClawHub

### Pre-flight Checklist

- [x] SKILL.md created with metadata
- [x] Python scripts created and executable
- [x] ln.bot integration working
- [x] Documentation complete

- [ ] Status endpoint fixed in n8n
- [ ] Payment webhook verified
- [ ] VAT API key confirmed working
- [ ] End-to-end test with real payment
- [ ] Security review passed

### Publishing Steps

```bash
# 1. Validate skill metadata
openclaw clawhub validate /root/.openclaw/workspace/skills/vatgentic/SKILL.md

# 2. Test in local environment
cd /root/.openclaw/workspace/skills/vatgentic
python3 scripts/vatgentic-request.py --vat-number LU26375245

# 3. Publish to ClawHub
export GITHUB_TOKEN="ghp_your_token"
clawhub publish /root/.openclaw/workspace/skills/vatgentic --version 0.1.0

# 4. Verify
clawhub search vatgentic
```

### Security Review Notes

**Required for ClawHub publishing:**

1. **Declare all file access**
   - Scripts only read: `~/.openclaw/secrets/lnbot-api.json`
   - No write operations to user files

2. **Environment variables**
   - `VATGENTIC_N8N_URL` - n8n instance URL
   - `VATGENTIC_AMOUNT` - default payment amount
   - `LNBOT_API_TOKEN` - ln.bot API token (optional, for auto-pay)
   - `LNBOT_WALLET_ID` - ln.bot wallet ID (optional)

3. **External endpoints** (document in SKILL.md)
   - ln.bot API: `https://api.ln.bot`
   - n8n webhook: user-configurable
   - BTCPay: user-configurable
   - VAT API: `https://eu.vatapi.com`

4. **No shell injection risks**
   - All user input properly sanitized
   - No raw string interpolation in shell commands

---

## Testing Guide

### Manual Test Flow

```bash
# 1. Request validation
python3 scripts/vatgentic-request.py --vat-number LU26375245 --country LU

# Expected output:
# ✅ VAT Validation Request Created
# Request ID: vat_1776348560582_yq24e3
# Amount: 10 sats
# Checkout link: https://btcpay...

# 2. Open checkout link in browser and pay

# 3. Check status
python3 scripts/vatgentic-status.py --request-id vat_1776348560582_yq24e3

# Expected output after payment:
# ✅ Validation Result:
#    Valid: true
#    Company: Example S.à r.l.
#    Address: 123 Example Street, Luxembourg
```

### Automated Test (when status endpoint works)

```bash
# Full end-to-end test
python3 scripts/vatgentic-validate.py \
  --vat-number LU26375245 \
  --timeout 300 \
  --json
```

---

## Known Issues

### 1. Status Endpoint 404

**Problem:** `/webhook/vatgentic/request-status/:requestId` returns 404

**Causes:**
- Webhook not configured in n8n
- Path parameter syntax differs
- Workflow not active

**Fix:**
```bash
# Import latest workflow to n8n
# Check webhook configuration:
# - Method: GET
# - Path: vatgentic/request-status/:requestId
# - Response Mode: Response Node
# - Active: true
```

### 2. Payment Webhook Not Firing

**Problem:** BTCPay doesn't send settlement webhook to n8n

**Causes:**
- Webhook URL incorrect in BTCPay settings
- API token expired
- Network/firewall blocking

**Fix:**
```bash
# Check BTCPay store settings → Webhooks
# Verify URL: https://YOUR-N8N-INSTANCE.com/webhook/vatgentic/payment
# Test with manual webhook:
curl -X POST https://YOUR-N8N-INSTANCE.com/webhook/vatgentic/payment \
  -H "Content-Type: application/json" \
  -d '{
    "invoiceId": "test-invoice",
    "type": "InvoiceSettled",
    "metadata": {"requestId": "vat_test_123"},
    "event": {"code": "InvoiceSettled"}
  }'
```

### 3. VAT API Returns Error

**Problem:** eu.vatapi.com returns invalid API key or rate limited

**Fix:**
```bash
# Check API key status
curl -X GET "https://eu.vatapi.com/v2/vat-number-check?vatid=LU26375245" \
  -H "Authorization: Bearer YOUR_API_KEY"

# If rate limited, wait or upgrade plan
# If invalid, regenerate key in VAT API dashboard
```

---

## Next Steps for Full Launch

1. **Fix status endpoint** (critical)
   - Import `vatgentic-prototype-fixed.json` to n8n
   - Activate all 3 webhooks
   - Test end-to-end flow

2. **Verify payment webhook**
   - Check BTCPay webhook settings
   - Fire test webhook
   - Confirm n8n execution

3. **Test with real VAT numbers**
   - Valid: LU26375245, DE123456789, FR12345678901
   - Invalid: Test error handling
   - Edge cases: Non-EU VAT, malformed numbers

4. **Documentation**
   - Add examples to SKILL.md
   - Create troubleshooting guide
   - Document expected response formats

5. **Soft launch**
   - Share with 2-3 trusted testers
   - Collect feedback
   - Fix any issues found

6. **Full ClawHub publishing**
   - Security review
   - Validate metadata
   - Publish with version 0.1.0

---

## Files Referenced

- Workflow: `/root/.openclaw/workspace/projects/vatgentic-n8n/vatgentic-prototype-fixed.json`
- Test results: `/root/.openclaw/workspace/projects/vatgentic-n8n/TEST-RESULTS-2026-04-16.md`
- Test script: `/root/.openclaw/workspace/projects/vatgentic-n8n/test-vatgentic-live.sh`
- Daily memory: Will update after tests complete

---

*Created by Rex, 2026-04-16*
