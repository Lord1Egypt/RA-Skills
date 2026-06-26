---
name: alipayplus-integration
description: Alipay+ Payment Integration Assistant. Helps Acquirers and Mobile Service Providers quickly integrate Alipay+ payments, including customer-presented mode payment and merchat-presented mode payment. This skill can help on configuration generation, signature verification testing, asynchronous notification debugging (ACQP only), and reconciliation file processing.
allowed-tools: Read, Write, Bash, WebFetch
---


# Alipay+ Payment Integration Assistant

## ⚠️ CONSTRAINTS - READ FIRST

**Information Sources (Priority Order):**
1. **This SKILL.md** - Core capabilities and flows
2. **./references/api-reference.md** - API endpoint list only
3. **./references/flows.md** - Flow diagrams (if exists)
4. **Official docs via WebFetch** - When details not in above files


**DO NOT:**
- ❌ Invent API parameters not in skill files or official docs
- ❌ Make up field names (e.g., `paymentToken`, `paymentCodeType`)
- ❌ Create fake request/response examples
- ❌ Assume flow details not documented here

**WHEN UNSURE:**
1. Check if info exists in skill files first
2. If not found, use `WebFetch` to get official docs
3. If still unclear, tell user "I need to check official docs" and fetch
4. Never guess - say "I don't have this info in my skill files"

**CAPABILITY BOUNDARIES:**
- ✅ Configuration generation (`generate-config.sh`)
- ✅ Signature testing (`test-signature.sh`)
- ✅ Webhook debugging (`debug-notify.sh`, ACQP only)
- ✅ Reconciliation file processing
- ❌ Detailed API parameters → Fetch from official docs
- ❌ Business logic advice → Refer to official docs

---

## Usage Examples

**This skill is triggered when users say:**
- "How to integrate with Alipay+"
- "How to integrate with A+"
- "Implement Alipay+ products"
- "Implement A+ products"
- "Alipay+"
- "AlipayPlus"
- "Acquirer integrates with Alipay+"
- "Wallet integrates with Alipay+"

**Not for:**
- Alipay
- WechatPay
- Wire transfer

**⚠️ Role Clarification Required:**
Before starting integration, users must clarify their role:
- **Acquirer Service Provider (ACQP)** - Payment service providers integrating with merchants
- **Mobile Payment Service Provider (MPP)** - E-wallet providers integrating with Alipay+

## Clarification Scripts

When user descriptions are ambiguous, use the following to clarify their scenario:

**For ACQP (Acquirer Service Provider):**

1. **ACQP CPM (Customer-presented Mode)**
   - **Scenario**: User presents payment code, merchant scans with barcode scanner
   - **Suitable for**: Convenience stores, shopping malls, restaurants, tourist attractions, etc.

2. **ACQP MPM (Merchant-presented Mode) Order Code**
   - **Scenario**: Merchant generates dynamic QR code, user scans to pay
   - **Suitable for**: Self-service ordering, convenience stores, vending machines, etc.

3. **ACQP MPM (Merchant-presented Mode) Entry Code**
   - **Scenario**: Merchant displays static QR code, user scans and enters amount to pay
   - **Suitable for**: Small individual merchant scenarios

**For MPP (Mobile Payment Provider):**

4. **MPP CPM (Customer-presented Mode)**
   - **Scenario**: User opens wallet payment code page, wallet generates payment code
   - **Suitable for**: Offline stores where merchants support barcode scanner payments

5. **MPP MPM (Merchant-presented Mode) Order Code**
   - **Scenario**: User opens wallet scanner page, scans merchant's dynamic order code to pay
   - **Suitable for**: Offline stores where merchants generate dynamic order codes

6. **MPP MPM (Merchant-presented Mode) Entry Code**
   - **Scenario**: User opens wallet scanner page, scans merchant's static payment code and entry payment amount to pay
   - **Suitable for**: Offline stores where merchants display static payment codes

## Quick Start

```bash
# Generate configuration template
bash "$(dirname "$SKILL_DIR")/scripts/generate-config.sh"

# Signature verification test
bash "$(dirname "$SKILL_DIR")/scripts/test-signature.sh"
```

## Capabilities

### 1. Configuration Generation

> ⚠️ **SAFE TO USE**: This uses `generate-config.sh` script which reads from skill files. No API parameter guessing needed.

Generate configuration templates for Alipay+ integration:

- **ACQP Config**: PartnerId, ClientId, API keys, webhook URLs
- **MPP Config**: PartnerId, ClientId, API keys, MPP endpoints
- **Environment**: Sandbox vs Production settings

### 2. Signature Verification

> ⚠️ **SAFE TO USE**: This uses `test-signature.sh` script. Signature algorithm is documented in skill files.

Help debug signature issues:

- Generate test signatures
- Verify incoming request's signatures
- Common signature errors and fixes

### 3. Webhook Debugging (for ACQP only)

> ⚠️ **SAFE TO USE**: Webhook format is defined in official notification docs. Use `WebFetch` if unsure about payload structure.

Assist with asynchronous notification setup:

- Webhook endpoint requirements
- Signature verification for webhooks
- Retry logic and idempotency

### 4. Reconciliation Files

> ⚠️ **CHECK DOCS FIRST**: Reconciliation file format may change. Verify column definitions with official docs.

Process daily reconciliation files:

- Parse settlement reports
- Match transactions
- Identify discrepancies

## Integration Flows

> ⚠️ **CHECK DOCS FIRST**: The flows in `flows.md` file are high-level summaries. For detailed API parameters, request/response schemas, and error codes, use `WebFetch` to retrieve official docs:
> - ACQP CPM: https://docs.alipayplus.com/alipayplus/alipayplus/integration_user_mode_acq/accept_payment
> - ACQP MPM Order Code: https://docs.alipayplus.com/alipayplus/alipayplus/integration_merchant_mode_acq/accept_payment_order_code
> - ACQP MPM Entry Code: https://docs.alipayplus.com/alipayplus/alipayplus/integration_merchant_mode_acq/accept_payment_entry_code
> - MPP CPM: https://docs.alipayplus.com/alipayplus/alipayplus/integration_user_mode_mpp/accept_payments
> - MPP MPM Order Code: https://docs.alipayplus.com/alipayplus/alipayplus/integration_merchant_mode_mpp/accept_payments#imyfn
> - MPP MPM Entry Code: https://docs.alipayplus.com/alipayplus/alipayplus/integration_merchant_mode_mpp/accept_payments#xSovW


### ACQP (Acquirer) Flow

1. Merchant onboarding
2. Payment initiation (CPM/MPM)
3. Payment notification
4. Settlement

### MPP (Wallet) Flow

1. User authentication
2. Payment code generation/scan
3. Payment execution
4. MPP notifies Alipay+ payment final result



## API References

- [ACQP API Reference](./references/api-reference.md#acqp-api-acquirer-service-provider)
- [MPP API Reference](./references/api-reference.md#mpp-api)
- [Flow Documentation](./references/flows.md)



## Resources

⚠️ **CHECK DOCS FIRST**: Documentation for all Alipay+ payment products is provided via dynamic online links. Before integration, be sure to read the relevant product’s online documentation to obtain the latest API parameters and code samples.


- [ACQP API Overview Documentation](https://docs.alipayplus.com/alipayplus/alipayplus/api_acq_tile/)
- [MPP API Overview Documentation](https://docs.alipayplus.com/alipayplus/alipayplus/api_mpp/)
- [MPP Android Client SDK Quick Start Documentation](https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/android_quick)
- [MPP iOS Client SDK Quick Start Documentation](https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/ios_quick)
- [MPP Server SDK Quick Start Documentation](https://docs.alipayplus.com/alipayplus/alipayplus/sdk_mpp/server_quick)


## Notes
- For business inquiries, please contact the regional BD.
- All links in this document point to Alipay+ online documentation, which is updated dynamically. Before coding, be sure to review the latest version.



