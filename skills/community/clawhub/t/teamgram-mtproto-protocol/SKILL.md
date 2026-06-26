---
name: teamgram-mtproto-protocol
description: Documents the MTProto protocol handling layer in Teamgram Server, including handshake, AES-IGE decryption, QuickAck, auth_key caching, and message forwarding to session service. Reference-only knowledge skill for developers working on Telegram-compatible backends.
compatibility: This is a documentation/knowledge skill only. No executable code is included. It describes Teamgram Server internals for developer reference.
metadata:
  author: zhihang9978
  version: "1.0.1"
  source: https://github.com/teamgram/teamgram-server
  homepage: https://github.com/teamgram/teamgram-server
  openclaw:
    requires:
      env: []
      bins: []
    securityNotes: |
      This skill is DOCUMENTATION ONLY - it contains no executable code, no network calls, and no credential handling.
      It describes how Teamgram Server (an open-source project) processes MTProto protocol messages.
      All code snippets are read-only references from the public teamgram-server repository.
      No auth_keys, secrets, or credentials are collected, stored, or transmitted by this skill.
---

# MTProto Protocol Layer in Teamgram Server

## Skill Type

**This is a reference/knowledge skill.** It contains no executable code. It documents the MTProto protocol handling internals of [Teamgram Server](https://github.com/teamgram/teamgram-server) (open-source, Apache-2.0 licensed) for developers who need to understand, debug, or extend the protocol layer.

## Overview

KHF client and Teamgram Server communicate via Telegram's MTProto binary protocol. The Teamgram gateway layer (gnetway) performs 3 key operations:

1. **Handshake / auth_key generation** (unauthenticated phase: auth_key_id=0 -> handshake)
2. **Authenticated message decryption** (AES-IGE)
3. **Forward decrypted payload (TLMessage2.Object) to session service via gRPC**

## Runtime Environment (for Teamgram Server operators)

If you are **deploying Teamgram Server** (not just reading this skill), the MTProto layer requires:

| Component | Purpose | Configuration |
|---|---|---|
| gnetway service | TCP/WS gateway, listens on ports 10443/5222/11443 | `app/interface/gnetway/etc/gnetway.yaml` |
| session service | Manages auth sessions, routes RPCs | `app/interface/session/etc/session.yaml` |
| MySQL | Stores auth_key records (`auth_keys`, `auth_key_infos` tables) | Configured in service YAML files |
| Redis | Caches auth_key for fast lookup | Configured in service YAML files |
| etcd | Service discovery between gnetway and session | `etcd.hosts` in YAML config |

**No credentials are required to read or install this skill.** The above table is for reference only when operating the actual Teamgram Server.

## Core Data Structure

The decrypted data structure is `mtproto.TLMessage2`, whose Object field contains the specific TL RPC call (e.g., `auth.sendCode`, `messages.sendMessage`, etc.).

## QuickAck Mechanism

gnetway implements QuickAck token computation. ACKs must be encoded through the codec to avoid obfuscated CTR counter desync (otherwise Android clients will fail at `decryptServerResponse`).

Reference function (from `app/interface/gnetway/internal/server/gnet/server_gnet.go:298-305` in [teamgram-server](https://github.com/teamgram/teamgram-server)):

```go
func computeQuickAckToken(authKey []byte, encryptedData []byte) uint32 {
    h := sha256.New()
    h.Write(authKey[88 : 88+32])
    h.Write(encryptedData)
    var sum [32]byte
    h.Sum(sum[:0])
    return binary.LittleEndian.Uint32(sum[:4]) | 0x80000000
}
```

## Encrypted Message Processing Flow

1. Decrypt via `authKey.AesIgeDecrypt`
2. Extract from decrypted payload header: `salt`, `sessionId`, `msgId`
3. Forward `payload[16:]` to session service via `SessionDispatcher.SendData` (gRPC)

## auth_key Caching and QueryAuthKey

When `connContext` lacks an authKey, gnetway asynchronously calls the session service's `QueryAuthKey` RPC, then proceeds with `onEncryptedMessage` after receiving the key.

**Key management note:** auth_keys are generated during the DH handshake, stored in MySQL (`auth_keys` table), and cached in Redis. They are never exposed outside the server process. The gnetway service holds keys only in memory during active connections.

## KHF Client Protocol Constants (must match server)

Extracted from KHF client source code:
- `TLRPC.LAYER = 222`
- `BuildVars.APP_ID = 4`
- `BuildVars.APP_HASH = "014b35b6184100b085b0d0572f9b5103"`

These are public application identifiers, not secrets. They must match between client and server for TL schema compatibility.

## Important Notes

- QuickAck must be encoded through codec, otherwise obfuscated CTR counter will desync
- Messages with auth_key_id=0 go through handshake flow; non-zero go through decryption flow
- After AES-IGE decryption, the first 16 bytes of payload are salt+sessionId, followed by TLMessage2 data

## Source Code References

All code referenced in this skill is from the open-source Teamgram Server project:
- Repository: https://github.com/teamgram/teamgram-server
- License: Apache-2.0
- Gateway code: `app/interface/gnetway/`
- Session code: `app/interface/session/`
- MTProto codec: `mtproto/` package
