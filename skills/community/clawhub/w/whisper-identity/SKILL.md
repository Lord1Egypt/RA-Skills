---
name: whisper-identity
description: Give this agent a real, routable IPv6 (/128) identity on the Whisper network, with safe egress and externally-verifiable identity (DNSSEC + RDAP). Keyless verification needs no account.
version: 1.0.0
license: MIT
homepage: https://whisper.online
metadata:
  tags: [identity, networking, egress, ipv6, dns, security, agent]
---

# Whisper Identity

Give this agent a real, routable IPv6 `/128` address that is both its name and
its credential. Its traffic egresses from that address, and anyone can verify the
identity with stock `dig` and RDAP, with Whisper never in the trust path. The
address is a live `/128` out of `2a04:2a01::/32`, announced by `AS219419`.

## When to use this skill
- The user wants to give an agent a real, attributable network identity or a
  stable egress IP, or to prove which agent made a request.
- The user wants to check whether an IP or host is a genuine Whisper agent. This
  half is keyless: nothing installed, no account.

## Verify any identity (keyless, no account, nothing to install)
```bash
# Is this IPv6 a real Whisper agent? Public RDAP + reverse DNS.
curl -s https://rdap.whisper.online/ip/<ipv6-address> | jq
dig -x <ipv6-address> +short
```

## Give THIS agent an identity (needs a Whisper API key)
```bash
curl get.whisper.online | sh                 # install the whisper CLI
whisper login                                # or: export WHISPER_API_KEY=whisper_live_...
whisper agent create --name <agent-name>     # mint the agent's /128 identity
whisper connect <agent-name>                 # local SOCKS5/HTTP egress bound to the /128
whisper run -- curl https://whisper.online/egress-ip   # confirm traffic leaves from the /128
```
Then confirm from the outside:
```bash
dig -x <the-/128> +short          # -> the agent's fully-qualified name
curl -s https://rdap.whisper.online/ip/<the-/128> | jq   # -> the public record
```

## Notes
- Two-tier by design: verification is keyless; claiming a `/128` and egress need a
  Whisper API key supplied as `WHISPER_API_KEY` (never hard-code it).
- Identity is anchored with DNSSEC + DANE + reverse DNS + a public RDAP record.
- Full docs: https://whisper.online/docs
