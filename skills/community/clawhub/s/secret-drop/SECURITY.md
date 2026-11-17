# Security policy

## What Secret Drop protects

Secret Drop is designed to keep the **plaintext secret value** out of:

- messenger chat history;
- OpenClaw model context and persisted transcripts;
- tool stdout and stderr;
- shell command arguments;
- repository files.

The one-time URL is still a bearer capability. It normally appears in the messenger message and the agent's tool request. Use one-view drops, short expiration, consume them promptly, and assume anyone who obtains an unconsumed link can redeem it.

Outbound `share` creates a Password Pusher link from a local dotenv or file source. The CLI never prints the payload; only the resulting URL is returned.

## Provider trust models

- **SnapPwd:** client-side encryption. The decryption key is in the URL fragment and is not sent to the provider server. Decryption runs in-process via Python `cryptography`.
- **Password Pusher:** TLS in transit and server-side encryption at rest. The provider can access plaintext during creation/retrieval. Self-host it when that trust is unacceptable.

## Storage trust models

- `openclaw-env` and `dotenv` write plaintext to a mode-0600 file.
- `file` writes plaintext to a mode-0600 file and refuses overwrite unless `--replace` is explicit.
- `openclaw-store --store-kind secret` writes a protected OpenClaw store entry. OpenClaw's current shared store is file-permission protected, not encrypted at rest.
- An external secret manager may provide stronger isolation than any local destination.

## Network protections

Native HTTP adapters:

- require HTTPS;
- reject URL userinfo;
- reject loopback, private, link-local, multicast, reserved, and unspecified DNS results;
- revalidate redirects;
- cap response bodies;
- never include response bodies in errors.

`--allow-private-host` intentionally disables private-address rejection for a trusted self-hosted provider. It does not make that provider trustworthy. DNS preflight is defense in depth and is not a substitute for host firewall or egress policy.

## Limitations

- Python cannot guarantee erasure of immutable strings, allocator copies, swap, filesystem journals, or SSD history.
- The link itself remains in chat unless the operator deletes it after successful consumption.
- OpenClaw must restart before values newly written to its global `.env` become active in the running Gateway process.
- Password-protected provider links may require additional provider-specific support; do not put passphrases in URL query parameters.

## Reporting vulnerabilities

Do not open a public issue containing a real secret, live link, hostname, token, or transcript. Use GitHub's private security advisory flow for this repository.
