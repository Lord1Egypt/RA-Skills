---
name: srift-quick-share
description: Deliver any file from this machine as a download link (https://srift.app/d/<token>) in one command, human to human or agent to human. Decentralized SRIFT transfer: streamed from the sender, stored on no server, end-to-end encrypted with --encrypt. No account, no API key.
version: 4.4.0
metadata:
  openclaw:
    emoji: "📦"
    homepage: https://srift.app
    requires:
      bins: [srift]
    install:
      - kind: node
        package: srift-transfer
        bins: [srift]
---

# SRIFT quick share

Turn any file or folder on this machine into a download link that a human or another agent can
open in a browser, `curl -fLOJ`, `wget --content-disposition`, or `srift get <url>`. The bytes
stream from this machine through the srift.app relay on demand (pass-through, `Cache-Control:
no-store`); nothing is stored on any server, so the link works while this process runs.

## Requirements

- The SRIFT CLI (`srift`), installed with `npm i -g srift-transfer` (or `pip install srift`).
- Outbound HTTPS/WSS on port 443. No account, no token.

## Use

```bash
srift quick-share ./report.pdf                 # prints https://srift.app/d/<token>
srift quick-share ./report.pdf --encrypt       # end-to-end encrypted; key stays in the #k= fragment
srift quick-share a.pdf b.csv dir/             # one bundle link (.tar.gz); --separate for one link each
srift quick-share ./dump.sql --once            # single download
srift quick-share ./build.zip --ttl 15m        # expires (30s, 15m, 2h, 1d)
srift quick-share ./x.bin --max-downloads 5
srift quick-share ./x.bin --wait               # block until downloaded (exit 3 on --wait-timeout)
```

1. Run the command and hand the printed URL to the recipient.
2. Keep this machine (or this process) running until the download finished; `--wait` blocks until then, `--keep-alive` serves until the TTL ends.
3. Use `--encrypt` for anything sensitive: the relay then sees only ciphertext and the browser decrypts locally.

## Sandboxes and datacenters

If a background daemon cannot start (no local servers, loopback blocked, port taken), `srift
quick-share` serves the link from its own process over outbound 443 only. Run it in the
background or with `--wait`. `HTTPS_PROXY`, `NO_PROXY` and `NODE_EXTRA_CA_CERTS` are honoured.
`srift doctor` diagnoses connectivity.

## Receiving

`srift get "<url>"` downloads (resumable, proxy-aware, decrypts `#k=` links). Any browser works too.

Full agent manual: https://srift.app/AGENTS.md · Contract: https://srift.app/openapi.json
