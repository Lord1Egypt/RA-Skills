# SberBusiness API (sber-business) v1.1.0

OpenClaw AgentSkill for official **SberBusiness API** integration: real-time account balances, instant transaction notifications (faster than paid SMS), official MCP payment drafting with signUrl, bank-stamped PDF statement downloads, and local-only Zero-Knowledge Vault onboarding.

---

## 🔒 Security Architecture (Zero-Knowledge Vault)

1. **Hardware-Bound AES-256-GCM Encryption:**
   - All banking secrets (`client_id`, `client_secret`, access/refresh tokens, private RSA keys, and mTLS certificates) are encrypted at rest in a binary `.vault` file.
   - Master key is derived via HKDF (SHA-256) from the host's `/etc/machine-id` and a protected master key file (`0400` permissions).
   - Even if disk images or backups are stolen, credentials cannot be decrypted on another machine.
   - Plaintext `.env` files are completely disabled and disallowed.
2. **Ephemeral RAM-Only TLS & Clean CA Validation:**
   - Client certificates and private keys are materialized strictly in RAM (`/dev/shm`), set to `0600`, and securely wiped with null bytes (`\x00`) immediately after each HTTPS request.
   - All download and API requests validate server certificates against the official Ministry of Digital Development / Sber trust bundle (`--cacert trust_bundle.pem`).
3. **Local-Only Credential Ingestion & Process Safety:**
   - Credentials and certificates are never passed through chat transcripts or sent to LLM providers.
   - Certificates are decrypted using `openssl` with `-passin stdin` (passwords never appear in `/proc` process arguments).
   - Users run `python3 scripts/sber_vault.py setup` with masked console input (`getpass`).
4. **Anti-Leak Red Line:**
   - AI agents are strictly instructed never to expose raw secrets, tokens, or private keys in chat messages.

---

## 🛡️ Privacy & Compliance (Banking Secrecy)

- **Mandatory HTTPS:** All external webhook endpoints must use TLS (`https://`). Plain HTTP transmissions are rejected by the poller daemon.
- **Privacy Masking Option:** Set `"maskPrivacy": true` in `config.json` to mask sensitive account numbers (`40702...0000`) and tax IDs (`7707****93`) in broadcast messages.
- **Private Channels:** Users are instructed to deliver balance and transaction alerts exclusively to authenticated, restricted company channels.

---

## ⚡ Instant Multi-Channel Alerts (Faster than SMS)

The included daemon polls the bank's incremental statement endpoint (`/v2/statement/increment`) every 60 seconds and broadcasts incoming/outgoing transaction alerts in seconds:
- **0 ₽ Cost:** completely replaces paid SMS notification packages.
- **Rich Context:** displays full counterparty legal name, INN, bank BIC, clean payment purpose, and real-time closing balance with proper HTML escaping.
- **Supported Channels:**
  - **Telegram** (direct chat, group, or channel)
  - **MAX Messenger** (direct or corporate group)
  - **Discord** (incoming webhook)
  - **Slack / Mattermost** (incoming webhook)
  - **Custom Webhook** (strict HTTPS POST JSON payload for 1C/CRM integration)

---

## 🛠️ Included Capabilities

1. **Instant Balance Query:**
   ```bash
   python3 scripts/sber_api.py summary
   ```
2. **Counterparty Directory Search (MCP):**
   ```bash
   python3 scripts/sber_payments.py search "<inn_or_name>"
   ```
3. **Payment Draft with One-Click Signature Link:**
   ```bash
   python3 scripts/sber_payments.py create \
     --payee "ООО Компания" \
     --inn "7707083893" \
     --kpp "770701001" \
     --account "40702810938000000000" \
     --bic "044525225" \
     --corr "30101810400000000225" \
     --amount 15000.00 \
     --purpose "Оплата по счёту №10. В том числе НДС 22% - 2704.92 руб."
   ```
   Returns `externalId` and a direct web bank link (`signUrl`) for instant SMS/Token signing.
4. **Official PDF Downloads with Bank Stamp:**
   ```bash
   python3 scripts/sber_download.py --date 2026-09-19 --number 61
   ```
   Downloads PDF payment orders with the official blue stamp **«ПАО СБЕРБАНК ИСПОЛНЕНО»**.
5. **Client Secret Rotation (40-day lifecycle):**
   ```bash
   python3 scripts/sber_rotate_secret.py --profile default
   python3 scripts/sber_rotate_secret.py --profile default --dry-run
   python3 scripts/sber_rotate_secret.py --profile default --json
   ```
   Sber fixes the Client Secret lifetime at **exactly 40 days** — it cannot be extended from the cabinet. The bank's own guidance is to rotate it programmatically on day 38. This script calls the official endpoint, atomically rewrites the new secret into the Vault, and re-reads it from disk to confirm.

   ⚠️ **Regenerating the secret in the cabinet invalidates existing refresh tokens.** After a manual regeneration you must obtain a fresh token pair from the portal (`401 UNAUTHORIZED` on the access key, `400 invalid_grant / Unknown refresh_token` on the refresh call). Rotation **through the API** does not have this drawback — verified end-to-end: refresh keeps working afterwards.

---

## 📖 Documentation

- **Human Walkthrough:** see `references/HUMAN_GUIDE.md` for a step-by-step portal guide with links.
- **Notification Channels:** see `references/NOTIFICATION_CHANNELS.md` for configuring Telegram, MAX, Discord, Slack, and Webhooks.

---

## License

MIT-0
