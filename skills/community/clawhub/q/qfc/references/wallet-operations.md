# QFC Wallet Operations Guide

## Creating a Wallet

```typescript
const wallet = new QFCWallet('testnet');
const { address, mnemonic, privateKey } = wallet.createWallet();
```

**Returns:**
- `address`: `string` — The 0x-prefixed Ethereum-style address
- `mnemonic`: `string` — 12-word BIP39 recovery phrase
- `privateKey`: `string` — 0x-prefixed 32-byte private key

**Security**: Never display the mnemonic or private key to the user. Store securely.

## Importing a Wallet

```typescript
const wallet = new QFCWallet('testnet');
const address = wallet.importWallet('0x...');
```

**Returns:** `string` — The derived address

## Checking Balance

```typescript
const { qfc, wei } = await wallet.getBalance('0x...');
```

**Returns:**
- `qfc`: `string` — Human-readable balance (e.g., "100.5")
- `wei`: `string` — Raw balance in wei

**Errors:**
- `NETWORK_ERROR` — RPC unreachable

## Sending QFC

```typescript
const { txHash, explorerUrl } = await wallet.sendQFC('0xRecipient', '10.0');
```

**Returns:**
- `txHash`: `string` — Transaction hash
- `explorerUrl`: `string` — Link to explorer for the transaction

**Errors:**
- `INSUFFICIENT_FUNDS` — Not enough QFC for amount + gas
- `INVALID_ADDRESS` — Recipient address format invalid
- `NONCE_TOO_LOW` — Previous tx pending; wait and retry

## Signing a Message

```typescript
const signature = await wallet.signMessage('Hello QFC');
```

**Returns:** `string` — The 0x-prefixed signature (65 bytes)

## Wallet Persistence

Wallets are encrypted with scrypt KDF and stored in `~/.openclaw/qfc-wallets/`. The keystore format is compatible with MetaMask and Geth.

### Save Wallet to Disk

```typescript
await wallet.save('mypassword', 'my-wallet');
```

Encrypts the current wallet and writes it to `~/.openclaw/qfc-wallets/keystore/<address>.json` with 0600 permissions.

### Load a Saved Wallet

```typescript
const wallet = await QFCWallet.load('0xAddress', 'mypassword', 'testnet');
```

Decrypts the keystore file and returns a ready-to-use `QFCWallet` instance.

### List Saved Wallets

```typescript
const wallets = QFCWallet.listSaved();
// [{ address, name, network, createdAt }]
```

No password needed — returns metadata only.

### Remove a Saved Wallet

```typescript
const keystore = new QFCKeystore();
keystore.removeWallet('0xAddress');
```

Deletes the keystore file and metadata entry.

### Export Keystore JSON

```typescript
const keystore = new QFCKeystore();
const json = keystore.getKeystoreJson('0xAddress');
```

Returns the encrypted JSON string for import into MetaMask or other tools.

## Security Policy

Before any transaction, run the security check:

```typescript
const policy = new SecurityPolicy();
const check = policy.preTransactionCheck({
  to: '0xRecipient',
  amount: 150,
});

if (!check.approved && check.requiresConfirmation) {
  // Ask user for confirmation, showing check.warnings
}
```

### Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `dailyLimit` | 1000 QFC | Max daily spending |
| `autoApproveBelow` | 10 QFC | Auto-approve small amounts to known addresses |
| `requireConfirmAlways` | false | Always require confirmation |

### Rules Applied

1. Transactions >100 QFC require confirmation
2. New recipient addresses require confirmation for amounts >10 QFC
3. Contract calls always require confirmation
4. Invalid address format blocks the transaction
5. Daily spending limit triggers confirmation when exceeded
