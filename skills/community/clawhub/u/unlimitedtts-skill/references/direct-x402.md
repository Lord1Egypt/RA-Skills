# Direct x402 mode

Use this mode only with an x402 v2 wallet-aware HTTP client or a separate wallet tool. Never collect wallet secrets in chat, tool arguments, source code, or logs.

1. Read `https://api.unlimitedtts.com/docs` and `https://api.unlimitedtts.com/tts/voices`.
2. Select a full voice id such as `openai_nova`; never send bare `nova`.
3. Enforce the user's limit before signing. Character billing currently follows JavaScript/UTF-16 `text.length`.
4. Prefer `POST https://api.unlimitedtts.com/x402/tts` with one stable JSON body:

   ```json
   {"text":"Hello world","voice":"openai_nova","speed":1}
   ```

5. On `402`, base64-decode `PAYMENT-REQUIRED`, require `x402Version: 2`, and select one compatible `exact` entry for the locally trusted Base network, USDC asset, and payee. Never trust a new payee merely because the challenge advertises it.
6. Copy that complete selected entry unchanged into `PaymentPayload.accepted`. Have the wallet sign its exact-EVM authorization.
7. Retry the identical HTTP method, URL, and body once with the base64 PaymentPayload in `PAYMENT-SIGNATURE`. A challenged GET must remain GET.
8. Accept audio only with a successful `audio/mpeg` response and a valid `PAYMENT-RESPONSE` settlement receipt.
9. Save audio using a server-generated filename under an approved output root. Do not put base64 audio in the final response.

Do not send `x-credit-account`, call `/top-up`, or create a prepaid account in the crypto flow.

Do not automatically create a second authorization after a timeout, connection loss, missing receipt, or ambiguous response. Report `PAYMENT_OUTCOME_UNKNOWN` and inspect settlement first.
