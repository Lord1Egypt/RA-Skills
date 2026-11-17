---
name: unlimitedtts
description: Create text-to-speech narration and MP3 audio with UnlimitedTTS using x402 USDC payments. Use for text-to-speech, narration, read-aloud, voice generation, MP3 creation, UnlimitedTTS, or wallet-paid/x402 speech requests.
---

# UnlimitedTTS

Create paid speech without handling wallet secrets. Prefer the UnlimitedTTS MCP tools. Use direct HTTP only when those tools are unavailable and a conforming x402 wallet-aware HTTP client is already present.

## MCP workflow

1. Call `tts_list_voices` when the voice is missing, ambiguous, or rejected. Use the full provider-prefixed id such as `openai_nova`.
2. Call `tts_quote` with the exact text, voice, speed, and any user-stated `maxUsdc`.
3. Check the exact amount, expiry, policy result, and user budget before signing.
4. When an external wallet tool is required, ask it to sign only `selectedRequirement` from this quote. Never request or expose a seed phrase, private key, or secret.
5. Call `tts_synthesize` once with the unchanged text, voice, speed, quote token, and returned `paymentSignature`.
6. Require `payment.settled: true`. Return or send the MP3 attachment/resource, not base64.

Treat `tts_synthesize` as irreversible and not replay-safe. Never retry `PAYMENT_OUTCOME_UNKNOWN`; inspect the wallet or settlement receipt and ask the user before any new quote or authorization.

Character limits vary by voice. If the text exceeds the character limit, split it into multiple chunks and call `tts_synthesize` for each chunk. Each chunk is a separate paid request. Get approval for the aggregate plan before proceeding.

## Direct HTTP mode

Read [direct-x402.md](references/direct-x402.md) only when MCP tools are unavailable and the agent already has both HTTP and x402 signing capability.

Read [errors.md](references/errors.md) when a tool or API call fails.

