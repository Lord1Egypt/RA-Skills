---
name: alipayplus-integration
description: Alipay+ Payment Integration Assistant. Provides structured integration guidance for Acquiring Service Providers (ACQP) and Mobile Payment Service Providers (MPP) across User-presented Mode (UPM), Merchant-presented Mode (MPM), Online Cashier Payment, and Online Auto Debit scenarios. Always fetches the latest official documentation from Alipay+ online docs before providing API parameters, flow details, or code examples, ensuring all guidance is accurate and up-to-date.
---


# Alipay+ Payment Integration Assistant

## Document Access Guidelines

To access Alipay+ online documentation, fetch content directly using curl:

```bash
# Example: Get ACQP onboarding process documentation
curl -sL "https://docs.alipayplus.com/alipayplus/alipayplus/onboarding_acq/onboarding_process.md"
```

### Recursive Access

Documentation pages contain links that need to be recursively accessed to retrieve complete content. Access flow:

1. First, access the main documentation URL
2. Parse the links within the document (product introductions, Quick Start, API documentation, etc.)
3. Recursively access these links to retrieve detailed content

## ⚠️ CONSTRAINTS - READ FIRST

**Information Sources (Priority Order):**
1. **This SKILL.md** - Core capabilities and flows
2. **Official docs via curl** - All Alipay+ documentation (MANDATORY)

**MANDATORY ONLINE DOCUMENTATION STRATEGY:**
All Alipay+ integration documentation MUST be fetched via curl. The online document at `https://docs.alipayplus.com/alipayplus/llms.txt` serves as the documentation index. For detailed content, use curl to fetch specific documentation pages. NEVER rely on cached or internal knowledge for API parameters.

**Role-Based Document Fetching:**
- Before starting, you MUST ask the user whether they are **ACQP** or **MPP**.
- **If ACQP**: Fetch only the `## ACQP` section from the online document.
- **If MPP**: Fetch only the `## MPP` section from the online document.

**Document Fetch Commands:**

For ACQP:
```bash
curl -sL "https://docs.alipayplus.com/alipayplus/llms.txt" | awk '/^## ACQP/{found=1} /^## MPP/{found=0} found'
```

For MPP:
```bash
curl -sL "https://docs.alipayplus.com/alipayplus/llms.txt" | awk '/^## MPP/{found=1} found'
```

**DO NOT:**
- ❌ Invent API parameters not in the fetched online docs
- ❌ Make up field names not in online doc
- ❌ Create fake request/response examples
- ❌ Assume flow details not documented in the fetched docs
- ❌ Use any locally cached API documentation without fetching first

**WHEN UNSURE:**
1. Fetch the latest online docs using curl
2. Search within the fetched content for the relevant topic
3. If still unclear, fetch the specific documentation page using curl
4. Never guess - say "I don't have this info in the fetched docs"

**CAPABILITY BOUNDARIES:**
- ❌ Detailed API parameters → Fetch from online docs first
- ❌ Business logic advice → Refer to online docs

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
- Domestic Payments
- Wire transfer

**⚠️ Role Clarification Required:**
Before starting integration, users MUST clarify their role:
- **Acquirer Service Provider (ACQP)** - Payment service providers integrating with merchants
- **Mobile Payment Service Provider (MPP)** - E-wallet providers integrating with Alipay+

After confirming the role, immediately fetch the corresponding section from the online documentation using the curl commands in the Constraints section above.

## Clarification Scripts

When user descriptions are ambiguous, use the following to clarify their scenario:

**For ACQP (Acquirer Service Provider):**

1. **ACQP UPM (User-presented Mode) Payment**
   - **Scenario**: User presents payment code, merchant scans with barcode scanner
   - **Suitable for**: Convenience stores, shopping malls, restaurants, tourist attractions, etc.

2. **ACQP MPM (Merchant-presented Mode) Payment Order Code**
   - **Scenario**: Merchant generates dynamic QR code, user scans to pay
   - **Suitable for**: Self-service ordering, convenience stores, vending machines, etc.

3. **ACQP MPM (Merchant-presented Mode) Payment Entry Code**
   - **Scenario**: Merchant displays static QR code, user scans and enters amount to pay
   - **Suitable for**: Small individual merchant scenarios

4. **ACQP Online Cashier Payment**
   - **Scenario**: Merchant redirects a User to the payment page of a MPP to confirm the Transaction details and Authorise the Payment. 
   - **Suitable for**: Online merchants, such as e-commerce merchants

5. **ACQP Online Auto Debit**
   - **Scenario**: User enters into an Auto Debit agreement to bind a User Account with a Merchant’s service and enjoy automatic payment for subsequent Transactions. 
   - **Suitable for**: Online merchants, such as online subscription services

**For MPP (Mobile Payment Provider):**

6. **MPP UPM (User-presented Mode) Payment**
   - **Scenario**: User opens wallet payment code page, wallet generates payment code
   - **Suitable for**: The e-wallet that need to support offline stores where barcode scanner payments are supported

7. **MPP MPM (Merchant-presented Mode) Payment Order Code**
   - **Scenario**: User opens wallet scanner page, scans merchant's dynamic order code to pay
   - **Suitable for**: The e-wallet that need to support offline stores where merchants generate dynamic order codes

8. **MPP MPM (Merchant-presented Mode) Payment Entry Code**
   - **Scenario**: User opens wallet scanner page, scans merchant's static payment code and enters payment amount to pay
   - **Suitable for**: The e-wallet that need to support offline stores where merchants display static payment codes

9. **MPP Online Cashier Payment**
   - **Scenario**: Customers to select MPP's wallet as a payment method and make payments globally for online purchases.
   - **Suitable for**: The e-wallet that need to support online merchants, such as e-commerce merchants

10. **MPP Online Auto Debit**
   - **Scenario**: Enable MPP's customers to make recurring payments conveniently by authorizing a trusted merchant to collect payments automatically.
   - **Suitable for**: The e-wallet that need to support online merchants, such as online subscription services

## Quick Start

```bash
# Step 1: Fetch role-specific online documentation
# ACQP:
curl -sL "https://docs.alipayplus.com/alipayplus/llms.txt" | awk '/^## ACQP/{found=1} /^## MPP/{found=0} found'

# MPP:
curl -sL "https://docs.alipayplus.com/alipayplus/llms.txt" | awk '/^## MPP/{found=1} found'
```

**Step 2: Read role-specific getting started documentation**

- **ACQP**: Read [ACQP - Get started with Alipay+ integration](https://docs.alipayplus.com/alipayplus/alipayplus/get_started_acq/get_started_integration_acq.md)
- **MPP**: Read [MPP - Get started with Alipay+ integration](https://docs.alipayplus.com/alipayplus/alipayplus/get_started_mpp/get_started_integration.md)

```bash
# Step 3: Fetch Alipay+ Developer Center user guide based on role
# ACQP:
curl -sL "https://docs.alipayplus.com/alipayplus/llms.txt" | awk '/^### Alipay\+ Developer Center User Guide for ACQPs/{found=1} /^## [^#]/{found=0} /^### [^#]/{if(found){found=0}} found'

# MPP:
curl -sL "https://docs.alipayplus.com/alipayplus/llms.txt" | awk '/^### Alipay\+ Developer Center User Guide$/{found=1; next} /^## [A-Z]/{found=0} /^### [^#]/{found=0} found'
```

**Step 4: Develop and Test in Alipay+ Developer Center**

Develop and test your integration using the Alipay+ Developer Center tools and resources. Refer to the fetched user guide for detailed instructions.

> **Before writing code, make sure to read the corresponding product's online documentation via curl. The documentation contains the latest API parameters, code examples, and important notes.**


## API References

After confirming the role, it is recommended to ask user to confirm the product user wants to implement: Online Auto Debit, Online Cashier Payment, Merchant-presented Mode Payment, User-presented Mode Payment. Then based on user's confirmation, fetch the API list from main doc based on the role and product.


## Production Acceptance Testing / User Acceptance Testing (UAT) Checklist

> **This section is for ACQP only.** Comprehensive UAT helps the integration with Alipay+ go live smoothly and efficiently.
> Reference doc: https://docs.alipayplus.com/alipayplus/alipayplus/get_started_acq/uat_checklist.md

## Notes
- For business inquiries, please contact the regional BD.
- All Alipay+ documentation is updated dynamically at `https://docs.alipayplus.com/alipayplus/llms.txt`. Before providing any integration guidance, ALWAYS fetch the latest version using the role-specific curl commands defined in the Constraints section.
- Do not rely on cached or internal knowledge for API parameters, flow details, or code examples. Always fetch fresh docs first.
