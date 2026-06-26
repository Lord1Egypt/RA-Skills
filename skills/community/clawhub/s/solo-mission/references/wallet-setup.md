# SOLO Mission Platform — Wallet Setup (On-Chain Missions)

On-chain missions require a Sponsor wallet — an Ethereum EOA that signs `createTask()`,
`cancelTask()`, `emergencyRefund()`, and `claimRefund()` on EscrowVault. All four
functions must be called from the **same address**.

---

## Skip this if you already have a funding tool

If your environment provides a signing/funding tool (e.g. a managed wallet service,
an existing KMS-backed key, a hardware wallet CLI, or a platform that handles
transaction signing for you), use it directly. You only need two things from it:

- `WALLET_ADDRESS` — the Ethereum address that will act as Sponsor
- A way to call `cast send` or submit signed transactions on Base Sepolia

Set `WALLET_ADDRESS` and proceed to `references/onchain.md`. No new wallet needed.

---

## Creating a new wallet (owner action — not the agent)

> ⚠️ **Wallet creation must be performed by the owner on a local trusted machine,
> not by the agent and not on a remote server.**

### Prerequisites

- Foundry installed: `curl -L https://foundry.paradigm.xyz | bash && foundryup`
- Verify: `cast --version`

### Generate the keypair

Run on your **local machine**:

```bash
cast wallet new
# Output:
#   Address:     0xYourWalletAddress
#   Private key: 0xYourPrivateKey
```

### Critical security warnings

> 🔴 **NEVER share your private key with the agent or paste it into any AI chat.**
>
> 🔴 **LLM SIDE-CHANNEL RISK: If you paste your private key into any AI chat interface
> (including this one), the key may be logged or stored. Treat it as a secret that
> must never enter an AI conversation.**
>
> 🔴 **NEVER store the private key in plaintext on disk or in a `.env` file on a server.**
>
> ✅ After copying the key, clear your terminal history:
> ```bash
> history -c && > ~/.bash_history   # bash
> fc -p && > ~/.zsh_history          # zsh
> ```

---

## Securing the private key

Encrypt the key so it never exists as plaintext on the server. Decrypt into memory
only at runtime and unset immediately after use.

### Option A — OpenSSL (works everywhere, no cloud required)

On your **local machine**:

```bash
openssl enc -aes-256-cbc -pbkdf2 \
  -in <(echo -n "YOUR_PRIVATE_KEY_HEX") \
  -out wallet.enc
```

Transfer to server:

```bash
scp wallet.enc user@your-server:/path/to/wallet.enc
chmod 600 /path/to/wallet.enc
```

At runtime (decrypt into memory only):

```bash
PRIVATE_KEY=$(openssl enc -d -aes-256-cbc -pbkdf2 -in wallet.enc)
# ... use PRIVATE_KEY in cast send calls ...
unset PRIVATE_KEY
```

Store the passphrase in a password manager. **Never store it on the same server as `wallet.enc`.**

### Option B — Cloud KMS (passphrase-free, recommended for automated agents)

The cloud VM authenticates automatically via its IAM role — no passphrase needed at runtime.

| Environment | KMS option |
|---|---|
| GCP Compute Engine | GCP KMS |
| AWS EC2 | AWS KMS |
| Azure VM | Azure Key Vault |
| Other | Use OpenSSL above |

At runtime:

```bash
# GCP example
PRIVATE_KEY=$(gcloud kms decrypt \
  --ciphertext-file=wallet.enc \
  --plaintext-file=- \
  --key=my-key --keyring=my-keyring --location=global)
# ... use PRIVATE_KEY ...
unset PRIVATE_KEY
```

---

## Fund the wallet

The Sponsor wallet needs ETH for gas and USDC for the mission budget before calling
`create_mission`.

| Asset | Purpose | Source |
|---|---|---|
| Base Sepolia ETH | Gas for every on-chain call | [Base Sepolia faucet](https://docs.base.org/docs/tools/network-faucets) |
| Test USDC | Mission budget (`amount_raw`) | [Circle USDC faucet](https://faucet.circle.com) — select Base Sepolia |

Check USDC balance before creating a mission:

```bash
cast call 0x036CbD53842c5426634e7929541eC2318f3dCF7e \
  "balanceOf(address)(uint256)" $WALLET_ADDRESS \
  --rpc-url https://sepolia.base.org
# Divide result by 1e6 for USDC amount — must be ≥ funding_params.amount_raw
```

---

## Set environment variables

```bash
export WALLET_ADDRESS=0xYourWalletAddress
export PRIVATE_KEY=0xYourPrivateKey   # from decryption step above — unset after use
```

These are the values referenced throughout `references/onchain.md`.
