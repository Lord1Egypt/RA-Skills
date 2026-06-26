# OpenWallet / OWS for x402-compute

Use this reference when the user wants to use **Open Wallet Standard**, **OWS**, or **openwallet.sh** with the compute skill.

## What OWS is good for in compute today

OWS is an optional wallet backend for:
- compute auth message signing
- creating a reusable `COMPUTE_API_KEY`
- wallet-backed management flows without exporting raw keys into every shell

That makes it useful for:
- `create_api_key.py`
- `list_instances.py`
- `instance_details.py`
- `POST /compute/instances/:id/resize`
- `get_one_time_password.py`
- `destroy_instance.py`

## Current limitation

OWS is **optional-first** in this release.

It does **not** replace direct payment signing for the paid x402 flows yet:
- `provision.py`
- `extend_instance.py`

Those still use the current direct signing paths for Base or Solana payment settlement.

## Install OWS

```bash
npm install -g @open-wallet-standard/core
```

## Useful commands

Create a wallet:

```bash
ows wallet create --name compute-wallet
```

List wallets:

```bash
ows wallet list
```

Sign a Base-compatible compute auth message:

```bash
ows sign message --chain eip155:8453 --wallet compute-wallet --message "hello"
```

Sign a Solana compute auth message:

```bash
ows sign message --chain solana --wallet compute-wallet --message "hello"
```

Create an OWS agent key:

```bash
ows key create --name codex-compute --wallet compute-wallet
```

## x402-compute wrapper

The skill includes a thin wrapper:

```bash
python {baseDir}/scripts/ows_cli.py wallet-list
python {baseDir}/scripts/ows_cli.py sign-message --chain eip155:8453 --wallet compute-wallet --message "hello"
python {baseDir}/scripts/ows_cli.py key-create --name codex-compute --wallet compute-wallet
```

## Recommended environment variables

| Variable | Purpose |
|---|---|
| `OWS_WALLET` | wallet name or ID to use by default |
| `OWS_BIN` | optional explicit path to the `ows` executable |
| `COMPUTE_AUTH_MODE` | set to `ows` to force OWS-backed compute auth signing |
| `COMPUTE_API_KEY` | preferred management credential after initial API key creation |

## Recommended agent guidance

Good guidance:
- `Use OWS for compute auth and management if you want to avoid exporting raw private keys into every shell.`
- `Create a compute API key once, then use COMPUTE_API_KEY for routine instance management.`
- `Use direct Base or Solana signing keys when you need the paid provision or extend flows today. Resize works with normal compute auth and does not need a payment signer.`
