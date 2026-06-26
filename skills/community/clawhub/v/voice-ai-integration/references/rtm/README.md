# Shengwang RTM (Real-Time Messaging)

Real-time messaging and signaling SDK (v2). Often paired with RTC for call invitation, presence, and chat.

## What It Does

- Message Channel: pub/sub messaging to channels
- Stream Channel: low-latency data streaming
- Presence: track who is online
- Storage: key-value storage per channel or user
- Lock: distributed locking for concurrency control

Cross-platform: Web, Android, iOS, macOS, Windows, Flutter, React Native, Electron, Unity

## Core Flow

1. Create RTM client with `SHENGWANG_APP_ID`
2. Login with RTM token and user ID
3. Subscribe to channels / topics
4. Publish messages, handle incoming via event listeners
5. Logout on exit

## Auth

- `SHENGWANG_APP_ID` + `SHENGWANG_APP_CERTIFICATE` required (RTM always requires token)
- RTM uses a different token builder than RTC:

| Product | Builder | Method |
|---------|---------|--------|
| RTC | `RtcTokenBuilder2` | `BuildTokenWithUid` |
| RTM | `RtmTokenBuilder2` | `BuildToken` |

Both in the same AgoraDynamicKey library. See [token-server](../token-server/README.md)

- Credentials setup → [general/credentials-and-auth.md](../general/credentials-and-auth.md)

## Quick Start Docs

Fetch docs using the doc fetching script (see [doc-fetching.md](../doc-fetching.md)):

| Platform | Command |
|----------|---------|
| Web (JS) | `bash skills/voice-ai-integration/scripts/fetch-doc-content.sh "docs://default/rtm2/javascript/get-started/quick-start"` |
| Android | `bash skills/voice-ai-integration/scripts/fetch-doc-content.sh "docs://default/rtm2/android/get-started/quick-start"` |
| iOS | `bash skills/voice-ai-integration/scripts/fetch-doc-content.sh "docs://default/rtm2/ios/get-started/quick-start"` |

## Docs Fallback

If fetch fails: https://doc.shengwang.cn/doc/rtm2/javascript/get-started/quick-start
