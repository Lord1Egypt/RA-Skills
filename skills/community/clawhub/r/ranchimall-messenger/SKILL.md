---
name: messenger_node
description: Use this skill whenever you are asked to send or receive messages, manage contacts, read or send mail, manage groups, look up public keys, check FLO balance, send FLO tokens, view transaction history, perform multisig address generation and multisig transactions using the FLO blockchain messenger, query FLO token (fungible token) balances or send tokens, query Bitcoin blockchain (balance, history, transactions, address generation, multisig), or manage local key-value storage. This is the primary way to interact with the decentralized FLO messenger, blockchain, and standard-operations libraries programmatically.
requires:
  binaries:
    - node
  env:
    - FLO_PRIVATE_KEY
---

# Messenger Node CLI Skill

When the user asks to perform any messenger operation, use your command execution tool to run the appropriate script. All scripts live in the messenger project directory.

## Setup & Dependencies
The `ws` dependency is required. Run `npm install` if needed.

## Network Activity
At runtime, scripts fetch a supernode list from the FLO blockchain and establish wss/https connections to discovered supernodes. Network activity is expected and required for the messenger to function.

## Security & Credentials
- All scripts strictly require the `FLO_PRIVATE_KEY` environment variable (except `contacts_node.js` and `pubkey_node.js --action my-pubkey`).
- **NEVER** ask or allow the user to paste their private key in the chat. If the key is missing, instruct them to set it securely via system environment variables.

## Runtime Transparency
All bundled libraries loaded at runtime via `vm.runInThisContext` are static, local files — no remote code is fetched or executed:

**Messaging scripts** (`send_node.js`, `receive_node.js`, `mail_node.js`, `groups_node.js`, `pubkey_node.js`, `multisig_node.js`) load via `node_shared.js`:

| File loaded | Purpose |
|---|---|
| `scripts/lib.js` | Crypto primitives (AES, Bitcoin, BigInteger) |
| `scripts/floCrypto.js` | FLO key derivation and signing |
| `scripts/floBlockchainAPI.js` | FLO blockchain read/write access |
| `scripts/floCloudAPI.js` | Supernode messaging transport |

**`flo_node.js`** (blockchain transactions) loads only 3 of the above — `floCloudAPI.js` is NOT loaded as no supernode messaging is needed for direct blockchain transactions.

**`contacts_node.js`** loads no FLO libraries at all — pure local JSON file operations.

**New standard-operations Node scripts** (added alongside existing scripts):

| Script | Library used | Purpose |
|---|---|---|
| `token_node.js` | `floTokenAPI.js` | FLO token balance, send, history |
| `btc_node.js` | `btcOperator.js` | Bitcoin balance, history, address tools |
| `idb_node.js` | *(file-backed shim)* | Local key-value store mirroring `compactIDB` |
| `crypto_node.js`| `floCrypto.js` | Pure cryptography, Shamir secret sharing |
| `cloud_node.js` | `floCloudAPI.js` | Supernode Cloud API raw operations |
| `dapp_node.js`  | `floDapps.js` | SubAdmin management, local key encryption |

**`scripts/floDapps.js`** is a browser startup framework (IndexedDB init, login, cloud boot). It has no meaningful Node.js equivalent — its individual sub-operations are covered by the existing messenger scripts and `idb_node.js`.

**`scripts/blockchainAddresses.js` is NOT loaded by any Node script.** It is a browser-only utility used by the web app (`index.html`) to display multi-chain addresses in the UI. No agent-facing script references, requires, or executes it. The private key is used solely for FLO messaging and transaction signing.

Local files written by this skill:
- `contacts.json` — contact address book (`contacts_node.js` only)
- `groups_cache.json` — group membership cache (`groups_node.js` only)
- `multisig_cache.json` — pending multisig pipeline state (`multisig_node.js` only)

## Blockchain Activity & Fees
- Sending messages writes data to the live FLO blockchain requiring a microscopic dust fee (0.0002 FLO per send) — this is a standard blockchain protocol requirement.

---

## Execution Instructions (Strict Adherence Required)

1. **Use your command execution tool** — DO NOT just print the command as text.
2. **Wait for user approval** before executing.
3. **Use the exact formats** shown below.

---

## Script Reference

###  Sending Messages — `send_node.js`
```powershell
node send_node.js --receiver "<RECEIVER_FLO_ID>" --message "<MESSAGE>"
```
Optional: Append `--encrypt "<RECEIVER_PUBLIC_KEY>"` to encrypt the message.

---

###  Receiving Messages — `receive_node.js`
```powershell
node receive_node.js
```
Flags:
- `--limit <N>` — Limit to N most recent messages (default: 50)
- `--sender <FLO_ID>` — Filter by sender address
- `--decrypt` — Auto-decrypt encrypted payloads
- `--watch` — Watch mode: live stream of incoming messages (long-running)

---

###  Contacts — `contacts_node.js`
No FLO_PRIVATE_KEY needed. Contacts stored locally in `contacts.json`.

```powershell
# List all contacts
node contacts_node.js --action list

# Add or update a contact
node contacts_node.js --action add --address "<FLO_ID>" --name "<NAME>"

# Remove a contact
node contacts_node.js --action remove --address "<FLO_ID>"

# Look up a contact by address
node contacts_node.js --action lookup --address "<FLO_ID>"
```

---

###  Public Keys — `pubkey_node.js`
```powershell
# Show your own FLO ID and public key (no cloud needed)
node pubkey_node.js --action my-pubkey

# Look up the public key of any FLO address from the cloud
node pubkey_node.js --action get --address "<FLO_ID>"

# Send a public key request to another user
node pubkey_node.js --action request --address "<FLO_ID>" --message "<OPTIONAL_NOTE>"
```

---

###  Mail — `mail_node.js`
Long-form messages with subject and body. Supports multiple recipients.

```powershell
# Send a mail (multiple --to flags or comma-separated addresses allowed)
node mail_node.js --action send --to "<FLO_ID1>,<FLO_ID2>" --subject "<SUBJECT>" --body "<BODY>"

# List received mails
node mail_node.js --action list --limit 20

# Read the full content of a specific mail
node mail_node.js --action read --ref "<MAIL_REF>"
```

---

###  Groups — `groups_node.js`
Requires `groups_cache.json` to be populated first via `--action fetch`.

```powershell
# Pull group memberships from cloud and cache locally (run this first!)
node groups_node.js --action fetch

# List all cached groups
node groups_node.js --action list

# Send an encrypted message to a group
node groups_node.js --action send --group "<GROUP_ID>" --message "<MESSAGE>"

# Read group messages (decrypted)
node groups_node.js --action read --group "<GROUP_ID>" --limit 30
```

> **Note:** Group IDs are long FLO addresses — use `--action list` to find them after fetching.

---

###  FLO Transactions — `flo_node.js`
Send FLO tokens, check balances, and view transaction history directly on-chain.

> **Warning:** `send` broadcasts a real on-chain transaction. Funds move immediately and cannot be reversed. The `--memo` text is stored publicly on the FLO blockchain.

```powershell
# Check your own FLO balance
node flo_node.js --action balance

# Check balance of any FLO address
node flo_node.js --action balance --address "<FLO_ID>"

# Send FLO tokens (with optional on-chain memo)
node flo_node.js --action send --to "<FLO_ID>" --amount <FLO> --memo "<TEXT>"

# View transaction history (your address)
node flo_node.js --action history --limit 20

# View transaction history for any address
node flo_node.js --action history --address "<FLO_ID>" --limit 20

# Write custom data to the blockchain
node flo_node.js --action write-data --data "<TEXT>" --to "<FLO_ID>"

# Read raw data transactions for an address
node flo_node.js --action read-data --address "<FLO_ID>"

# Send FLO to multiple receivers in a single transaction
node flo_node.js --action send-tx-multiple --privkeys "<WIF1>,<WIF2>" --receivers "<FLO_ID1>:0.1,<FLO_ID2>:0.5"

# Merge UTXOs to consolidate dust
node flo_node.js --action merge-utxos
```

---

### 🔒 Cryptography — `crypto_node.js`
Pure cryptographic operations. Offline, no network required.

```powershell
# Generate random data
node crypto_node.js --action rand-string --length 16
node crypto_node.js --action rand-int --min 1 --max 100

# Address validation
node crypto_node.js --action validate-address --address "<FLO_ID>"
node crypto_node.js --action verify-pubkey --pubkey "<HEX>"

# Identity retrieval
node crypto_node.js --action get-pubkey --privkey "<WIF>"
node crypto_node.js --action get-address --pubkey "<HEX>"

# Encrypt / Decrypt
node crypto_node.js --action encrypt --data "<TEXT>" --pubkey "<HEX>"
node crypto_node.js --action decrypt --data "<HEX>" --privkey "<WIF>"

# Sign / Verify
node crypto_node.js --action sign --data "<TEXT>" --privkey "<WIF>"
node crypto_node.js --action verify-sign --data "<TEXT>" --sig "<HEX>" --pubkey "<HEX>"

# Shamir's Secret Sharing
node crypto_node.js --action shamir-create --secret "<TEXT>" --shares <N> --threshold <M>
node crypto_node.js --action shamir-retrieve --shares "S1,S2,S3"
node crypto_node.js --action shamir-verify --shares "S1,S2" --secret "<TEXT>"
```

---

### ☁️ Supernode Cloud API — `cloud_node.js`
Raw interaction with the FLO Supernode Cloud infrastructure.

```powershell
node cloud_node.js --action send-general --data "<TEXT>" --type "<TYPE>"
node cloud_node.js --action request-general --type "<TYPE>"
node cloud_node.js --action request-object --object "<NAME>"
```

---

### 🛠️ DApp Tools — `dapp_node.js`
Node equivalents for administrative `floDapps` operations.

```powershell
# Add/Remove SubAdmins on the blockchain
node dapp_node.js --action manage-subadmins --add "FLO_ID1" --rm "FLO_ID2"

# Encrypt your private key with a PIN via Shamir shares
node dapp_node.js --action secure-privkey --pin "<PASSWORD>"

# Get next general data
node dapp_node.js --action get-next-general --type "<TYPE>" [--vector "<CLOCK>"]
```

---

###  FLO Multisig — `multisig_node.js`
FLO multisig address generation, collaborative transaction signing, and pending transaction management.

> **Note:** Multisig transactions require M-of-N co-signers. The `create-tx` action partially signs the transaction and distributes it to co-signers via an encrypted cloud pipeline. Co-signers then run `sign-tx` to add their signature. Once M signatures are collected, the transaction is automatically broadcast.

> **Warning:** `create-tx` sends real FLO funds when eventually broadcast. Memos are stored publicly on-chain.

```powershell
# Step 1: Generate a multisig address (no FLO_PRIVATE_KEY needed)
node multisig_node.js --action generate-address --pubkeys "PUB1,PUB2,PUB3" --required 2

# Step 2: Create and sign a multisig tx (initiator)
# Supports single receiver/amount or multiple (comma-separated or multiple --to/--amount flags matching in length)
node multisig_node.js --action create-tx \
  --address "<MULTISIG_FLO_ID>" \
  --redeem-script "<REDEEM_SCRIPT_HEX>" \
  --to "<RECEIVER_FLO_ID1>,<RECEIVER_FLO_ID2>" \
  --amount "1.5,0.5" \
  --memo "payments"

# Step 3 (co-signer): Sign the pending tx
node multisig_node.js --action sign-tx --pipeline "<PIPELINE_ID>"

# View status of a pending tx
node multisig_node.js --action view-tx --pipeline "<PIPELINE_ID>"

# List all locally cached pending multisig transactions
node multisig_node.js --action list-pending

# Manually broadcast a fully-signed tx
node multisig_node.js --action broadcast --pipeline "<PIPELINE_ID>"
```

---

###  FLO Token Operations — `token_node.js`
Query and transfer FLO tokens (fungible tokens on the FLO blockchain).

> **Warning:** `send` broadcasts a real on-chain token transfer. Tokens move immediately and cannot be reversed.

```powershell
# Check your own token balance (default token: rupee)
node token_node.js --action balance

# Check balance for any address / any token
node token_node.js --action balance --address "<FLO_ID>" --token rupee

# Send tokens
node token_node.js --action send --to "<FLO_ID>" --amount <N> --token rupee --message "<NOTE>"

# Token transaction history
node token_node.js --action history
node token_node.js --action history --address "<FLO_ID>" --token rupee

# Details of a specific token transaction
node token_node.js --action tx --txid "<TXID>"

# Bulk transfer to multiple receivers
node token_node.js --action bulk-transfer --receivers "<FLO_ID1>:10,<FLO_ID2>:20"

# Parse token tx data
node token_node.js --action parse-tx --txdata "<JSON>"

# Raw fetch against token API
node token_node.js --action raw-fetch --apicall "api/v1.0/getTx?txid=..."
```

Flags:
- `--address <FLO_ID>` — Target address (defaults to your address derived from FLO_PRIVATE_KEY)
- `--token <TOKEN>` — Token name (default: `rupee`)
- `--message <TEXT>` — Optional note attached to the token transfer

---

###  Bitcoin Operations — `btc_node.js`
Bitcoin blockchain queries and address tools. Uses multiple APIs with automatic failover (Blockcypher, Blockstream, Mempool.space, Blockchain.info).

> **Note:** No `FLO_PRIVATE_KEY` required. All read actions are public. `broadcast` sends a pre-signed raw transaction you provide.

```powershell
# BTC balance for any address
node btc_node.js --action balance --address "<BTC_ADDR>"

# Transaction history
node btc_node.js --action history --address "<BTC_ADDR>"

# Transaction details
node btc_node.js --action tx --txid "<TXID>"

# Generate a new BTC key pair (legacy + segwit + bech32 addresses)
node btc_node.js --action new-keys

# Validate a BTC address and show its type (legacy/bech32/segwit/multisig)
node btc_node.js --action validate --address "<BTC_ADDR>"

# Generate a multisig address
node btc_node.js --action multisig --pubkeys "PUB1,PUB2,PUB3" --required 2
node btc_node.js --action multisig --pubkeys "PUB1,PUB2" --required 2 --no-bech32

# Decode a redeem script
node btc_node.js --action decode-script --hex "<REDEEM_SCRIPT_HEX>"

# Convert an address between formats
node btc_node.js --action convert --address "<ADDR>" --from legacy --to bech32
node btc_node.js --action convert --address "<ADDR>" --from bech32 --to legacy

# Broadcast a pre-signed raw transaction
node btc_node.js --action broadcast --hex "<SIGNED_RAW_TX_HEX>"
```

Address type options for `--from`/`--to`: `legacy`, `bech32`, `segwit`, `multisig`

---

###  Local Key-Value Storage — `idb_node.js`
File-backed key-value store that mirrors the browser `compactIDB` API. Data is persisted to `./idb_data/<db>.json`.

> **Note:** No `FLO_PRIVATE_KEY` required. No network activity. Pure local file operations.

```powershell
# List all local databases
node idb_node.js --action dbs

# List stores in a database
node idb_node.js --action stores --db "<DB_NAME>"

# Initialise a database with stores
node idb_node.js --action init --db "<DB_NAME>" --stores "contacts,settings,messages"

# List all records in a store
node idb_node.js --action list --db "<DB_NAME>" --store "<STORE>"

# Read a single record
node idb_node.js --action read --db "<DB_NAME>" --store "<STORE>" --key "<KEY>"

# Add a new record (fails if key already exists)
node idb_node.js --action add --db "<DB_NAME>" --store "<STORE>" --key "<KEY>" --value '"Alice"'

# Write (upsert) a record (value is JSON or plain string)
node idb_node.js --action write --db "<DB_NAME>" --store "<STORE>" --key "<KEY>" --value '"Alice"'
node idb_node.js --action write --db "<DB_NAME>" --store "<STORE>" --key "cfg" --value '{"theme":"dark"}'

# Remove a record
node idb_node.js --action remove --db "<DB_NAME>" --store "<STORE>" --key "<KEY>"

# Clear all records in a store
node idb_node.js --action clear --db "<DB_NAME>" --store "<STORE>"

# Delete an entire database
node idb_node.js --action delete-db --db "<DB_NAME>"
```

---

## Standard Operations Library Reference (Browser)

> The following libraries are browser/DApp-side. They are documented here so the agent understands their API when working with FLO DApp code or the web app (`index.html`).

---

### 📦 compactIDB — `scripts/compactIDB.js`
Compact browser IndexedDB wrapper. Exposes `window.compactIDB`.

| Method | Description |
|---|---|
| `compactIDB.initDB(dbName, objectStores)` | Create/upgrade a database and its object stores |
| `compactIDB.setDefaultDB(dbName)` | Set the default database for subsequent calls |
| `compactIDB.openDB(dbName?)` | Open a database connection |
| `compactIDB.deleteDB(dbName?)` | Delete an entire database |
| `compactIDB.writeData(store, data, key?, db?)` | Write (put/upsert) a record |
| `compactIDB.addData(store, data, key?, db?)` | Add a new record (fails if key exists) |
| `compactIDB.readData(store, key, db?)` | Read a single record by key |
| `compactIDB.readAllData(store, db?)` | Read all records from a store as `{key: value}` |
| `compactIDB.removeData(store, key, db?)` | Delete a record by key |
| `compactIDB.clearData(store, db?)` | Clear all records in a store |
| `compactIDB.searchData(store, options, db?)` | Cursor-based filtered search with limit/range/reverse |

All methods return Promises.

---

### 🚀 floDapps — `scripts/floDapps.js`
FLO DApp framework for browser apps. Handles startup, credentials, app config, and user data. Exposes `window.floDapps`.

**Startup & Lifecycle**

| Method | Description |
|---|---|
| `floDapps.launchStartUp()` | Full app startup: IndexedDB init + supernode list + app config + credentials + user DB load |
| `floDapps.addStartUpFunction(fn)` | Register an additional async startup function |
| `floDapps.setMidStartup(fn)` | Register a function that runs after startup functions but before credential load |
| `floDapps.setCustomStartupLogger(fn)` | Override default console startup logger |
| `floDapps.setCustomPrivKeyInput(fn)` | Override the default `prompt()` for private key entry |
| `floDapps.setAppObjectStores(obs)` | Register additional IndexedDB object stores for the app |

**Startup Options**

| Property | Default | Description |
|---|---|---|
| `floDapps.startUpOptions.cloud` | `true` | Whether to fetch supernode list and app config from chain |
| `floDapps.startUpOptions.app_config` | `true` | Whether to read subAdmins/trustedIDs/settings from blockchain |

**User Object** (`floDapps.user`)

| Property/Method | Description |
|---|---|
| `user.id` | Logged-in FLO address |
| `user.public` | Public key hex |
| `user.private` | Private key (async if PIN-protected) |
| `user.sign(message)` | Sign a message with the user's private key |
| `user.decrypt(data)` | Decrypt EC-encrypted data |
| `user.encipher(msg)` | AES-encrypt a string with user's private key |
| `user.decipher(data)` | AES-decrypt with user's private key |
| `user.contacts` | Loaded contact map `{floID: name}` |
| `user.pubKeys` | Loaded public key map `{floID: pubKeyHex}` |
| `user.messages` | Loaded inbox messages map `{vectorClock: msgObj}` |
| `user.lock()` / `user.unlock()` | Lock/unlock private key access (require PIN re-entry) |
| `user.clear()` | Clear all user state |

**Data & Messaging**

| Method | Description |
|---|---|
| `floDapps.storeContact(floID, name)` | Save a contact to IndexedDB and memory |
| `floDapps.storePubKey(floID, pubKeyHex)` | Save a public key to IndexedDB and memory |
| `floDapps.sendMessage(floID, message)` | Send an encrypted (if pubKey known) cloud message |
| `floDapps.requestInbox(callback)` | Fetch and decrypt inbox messages via live cloud request |

**App Config (admin only)**

| Method | Description |
|---|---|
| `floDapps.manageAppConfig(adminPrivKey, addList, rmList, settings)` | Add/remove subAdmins and update settings on-chain |
| `floDapps.manageAppTrustedIDs(adminPrivKey, addList, rmList)` | Add/remove trusted IDs on-chain |

**Credential Management**

| Method | Description |
|---|---|
| `floDapps.securePrivKey(pwd)` | Encrypt stored private key with a PIN/password |
| `floDapps.verifyPin(pin?)` | Verify the current PIN or check if one is set |
| `floDapps.clearCredentials()` | Wipe stored credentials from IndexedDB + localStorage |
| `floDapps.deleteUserData(credentials?)` | Delete user IndexedDB; optionally also clear credentials |
| `floDapps.deleteAppData()` | Delete entire app IndexedDB and reset local state |

**Global shortcuts set on `window`:** `myFloID`, `myUserID`, `myPubKey`, `myPrivKey`

---

### 🪙 floTokenAPI — `scripts/floTokenAPI.js`
FLO token (fungible token) operations. Exposes `window.floTokenAPI`.

| Method | Description |
|---|---|
| `floTokenAPI.getBalance(floID, token?)` | Get token balance for a FLO address (default token: `rupee`) |
| `floTokenAPI.sendToken(privKey, amount, receiverID, message?, token?, options?)` | Send tokens on-chain |
| `floTokenAPI.bulkTransferTokens(sender, privKey, token, receivers)` | Send tokens to multiple receivers (`{addr: amount}`) |
| `floTokenAPI.getAllTxs(floID, token?)` | Get all token transactions for a FLO address |
| `floTokenAPI.getTx(txID)` | Get details of a specific token transaction |
| `floTokenAPI.util.parseTxData(txData)` | Parse raw tx data into `{type, sender, receiver, amount, time}` |
| `floTokenAPI.fetch(apicall)` | Raw fetch against the token API server |

**Properties:**
- `floTokenAPI.currency` — Current default token name (get/set)
- `floTokenAPI.URL` — Current API base URL

> **Warning:** `sendToken` and `bulkTransferTokens` broadcast real on-chain token transfers. Token amounts are checked against balance before sending.

---

### ₿ btcOperator — `scripts/btcOperator.js`
Bitcoin blockchain operations — address generation, balance, transactions, multi-sig. Exposes `window.btcOperator`.

**Address & Key Utilities**

| Method/Property | Description |
|---|---|
| `btcOperator.newKeys` | Generate new BTC key pair (legacy + segwit + bech32 addresses) |
| `btcOperator.pubkey(key)` | Get pubkey hex from WIF, hex private key, or pubkey |
| `btcOperator.address(key, prefix?)` | Get legacy BTC address from key |
| `btcOperator.segwitAddress(key)` | Get P2SH-segwit address |
| `btcOperator.bech32Address(key)` | Get native bech32 (bc1q) address |
| `btcOperator.validateAddress(addr)` | Validate BTC address; returns type string or `false` |
| `btcOperator.verifyKey(addr, key)` | Verify a private key matches an address |

**Multisig**

| Method | Description |
|---|---|
| `btcOperator.multiSigAddress(pubKeys, minRequired, bech32?)` | Generate M-of-N multisig address |
| `btcOperator.decodeRedeemScript(redeemScript, bech32?)` | Decode a redeem script into `{address, pubKeys, required}` |

**Address Conversion**

| Method | Description |
|---|---|
| `btcOperator.convert.wif(sourceWif, targetVersion?)` | Convert WIF private key to another chain's format |
| `btcOperator.convert.legacy2legacy(addr, targetVersion?)` | Convert legacy address version |
| `btcOperator.convert.legacy2bech(addr, version?, hrp?)` | Legacy → bech32 |
| `btcOperator.convert.bech2legacy(addr, targetVersion?)` | Bech32 → legacy |
| `btcOperator.convert.bech2bech(addr, version?, hrp?)` | Bech32 → bech32 (different chain) |
| `btcOperator.convert.multisig2multisig(addr, targetVersion?)` | Multisig → multisig (different version) |
| `btcOperator.convert.bech2multisig(addr, targetVersion?)` | Bech32 multisig → legacy multisig |

**Blockchain Queries**

| Method | Description |
|---|---|
| `btcOperator.getBalance(addr)` | Get BTC balance for an address |
| `btcOperator.broadcastTx(rawTxHex)` | Broadcast a signed raw transaction |
| `btcOperator.multiApi(fnName, args?)` | Call any API method with automatic failover across providers |

**Utilities**

| Method | Description |
|---|---|
| `btcOperator.util.Sat_to_BTC(value)` | Convert satoshis to BTC |
| `btcOperator.util.BTC_to_Sat(value)` | Convert BTC to satoshis |
| `btcOperator.util.format.block(block)` | Normalize block data from any API |
| `btcOperator.util.format.tx(tx)` | Normalize transaction data from any API |
| `btcOperator.util.format.utxos(utxos)` | Normalize UTXO list from any API |

**Supported API Providers** (automatic failover): Blockcypher, Blockstream, Mempool.space, Blockchain.info, Coinb.in

---

## Quick Reference Table

| Task | Command |
|---|---|
| Send a message | `node send_node.js --receiver "..." --message "..."` |
| Read messages | `node receive_node.js` |
| List contacts | `node contacts_node.js --action list` |
| Add contact | `node contacts_node.js --action add --address "..." --name "..."` |
| My public key | `node pubkey_node.js --action my-pubkey` |
| Get someone's pubkey | `node pubkey_node.js --action get --address "..."` |
| Send mail | `node mail_node.js --action send --to "..." --subject "..." --body "..."` |
| List mails | `node mail_node.js --action list` |
| Read mail | `node mail_node.js --action read --ref "..."` |
| Sync groups | `node groups_node.js --action fetch` |
| List groups | `node groups_node.js --action list` |
| Send group message | `node groups_node.js --action send --group "..." --message "..."` |
| Read group messages | `node groups_node.js --action read --group "..."` |
| FLO balance | `node flo_node.js --action balance` |
| Send FLO | `node flo_node.js --action send --to "..." --amount <FLO>` |
| FLO tx history | `node flo_node.js --action history` |
| **floCrypto** | |
| Generate new FLO keys (`generateNewID`) | `node flo_node.js --action new-keys` |
| Get FLO Public Key Hex (`getPubKeyHex`) | `node crypto_node.js --action get-pubkey` |
| Get FLO ID from privkey (`getFloID`) | `node crypto_node.js --action get-address` |
| Get FLO Address from pubkey (`getAddress`)| `node crypto_node.js --action get-address` |
| Verify FLO Private Key (`verifyPrivKey`) | `node crypto_node.js --action verify-privkey` |
| Validate FLO Address (`validateAddr`) | `node crypto_node.js --action validate-address` |
| Validate FLO ID (`validateFloID`) | `node crypto_node.js --action validate-address` |
| Verify FLO Public Key (`verifyPubKey`) | `node crypto_node.js --action verify-pubkey` |
| Encrypt Data with FLO pubkey (`encryptData`) | `node crypto_node.js --action encrypt --data "..." --pubkey "..."` |
| Decrypt Data with FLO privkey (`decryptData`) | `node crypto_node.js --action decrypt --data "..." --privkey "..."` |
| Sign Data with FLO privkey (`signData`) | `node crypto_node.js --action sign --data "..." --privkey "..."` |
| Verify FLO Signature (`verifySign`) | `node crypto_node.js --action verify-sign --data "..." --sig "..." --pubkey "..."` |
| Generate Random Integer (`randInt`) | `node crypto_node.js --action rand-int` |
| Generate Random String (`randString`) | `node crypto_node.js --action rand-string` |
| Create Shamir's Shares (`createShamirsSecretShares`) | `node crypto_node.js --action shamir-create --secret "..." --shares <N> --threshold <M>` |
| Retrieve Shamir Secret (`retrieveShamirSecret`) | `node crypto_node.js --action shamir-retrieve` |
| Verify Shamir's Secret (`verifyShamirsSecret`) | `node crypto_node.js --action shamir-verify` |
| **floBlockchainAPI** | |
| Write Data to FLO Blockchain (`writeData`) | `node flo_node.js --action write-data --data "..."` |
| Write Data Multiple to FLO Blockchain (`writeDataMultiple`) | `node flo_node.js --action write-data-multiple --privkeys "..." --data "..."` |
| Send FLO Tx Multiple (`sendTxMultiple`) | `node flo_node.js --action send-tx-multiple --privkeys "..." --receivers "..."` |
| Merge FLO UTXOs (`mergeUTXOs`) | `node flo_node.js --action merge-utxos` |
| Read Data from FLO Blockchain (`readData`) | `node flo_node.js --action read-data --address "..."` |
| Read FLO Txs range (`readTxs`) | `node flo_node.js --action history --limit N` |
| Read All FLO Txs (`readAllTxs`) | `node flo_node.js --action read-all-txs --address "..."` |
| **floCloudAPI** | |
| Send General Data to Supernode (`sendGeneralData`) | `node cloud_node.js --action send-general --data "..."` |
| Request General Data from Supernode (`requestGeneralData`) | `node cloud_node.js --action request-general` |
| Send Application Data to Supernode (`sendApplicationData`) | `node cloud_node.js --action send-app --data "..."` |
| Request Application Data from Supernode (`requestApplicationData`) | `node cloud_node.js --action request-app` |
| Reset Object Data on Supernode (`resetObjectData`) | `node cloud_node.js --action reset-object` |
| Update Object Data on Supernode (`updateObjectData`) | `node cloud_node.js --action update-object` |
| Request Object Data from Supernode (`requestObjectData`) | `node cloud_node.js --action request-object` |
| **floDapps** | |
| Manage SubAdmins on FLO Blockchain (`manageSubAdmins`) | `node dapp_node.js --action manage-subadmins --add "..."` |
| Secure FLO Private Key with PIN (`securePrivKey`) | `node dapp_node.js --action secure-privkey --pin "..."` |
| Get Next General Data from Supernode (`getNextGeneralData`) | `node dapp_node.js --action get-next-general --type "..."` |
| **floTokenAPI** | |
| Bulk Transfer FLO Tokens (`bulkTransferTokens`) | `node token_node.js --action bulk-transfer --receivers "..."` |
| Parse FLO Token Tx Data (`parseTxData`) | `node token_node.js --action parse-tx --txdata "..."` |
| Raw Fetch FLO Token API (`raw API fetch`) | `node token_node.js --action raw-fetch --apicall "..."` |
| **compactIDB** | |
| Add Data to Local IndexedDB (`addData`) | `node idb_node.js --action add --db "..." --store "..." --key "..." --value "..."` |
| **BTC / Token / Core Messenger** | |
| Generate FLO multisig address | `node multisig_node.js --action generate-address --pubkeys "..." --required N` |
| Create FLO multisig TX | `node multisig_node.js --action create-tx --address "..." --redeem-script "..." --to "..." --amount <FLO>` |
| Sign pending FLO multisig TX | `node multisig_node.js --action sign-tx --pipeline "..."` |
| View FLO multisig TX status | `node multisig_node.js --action view-tx --pipeline "..."` |
| List pending FLO multisig TXs | `node multisig_node.js --action list-pending` |
| Broadcast FLO multisig TX | `node multisig_node.js --action broadcast --pipeline "..."` |
| FLO Token balance | `node token_node.js --action balance` |
| FLO Token balance (any address) | `node token_node.js --action balance --address "..." --token rupee` |
| Send FLO token | `node token_node.js --action send --to "..." --amount <N> --token rupee` |
| FLO Token tx history | `node token_node.js --action history` |
| FLO Token tx details | `node token_node.js --action tx --txid "..."` |
| BTC balance | `node btc_node.js --action balance --address "..."` |
| BTC tx history | `node btc_node.js --action history --address "..."` |
| BTC tx details | `node btc_node.js --action tx --txid "..."` |
| New BTC key pair | `node btc_node.js --action new-keys` |
| Validate BTC address | `node btc_node.js --action validate --address "..."` |
| BTC multisig address | `node btc_node.js --action multisig --pubkeys "P1,P2,P3" --required 2` |
| Decode BTC redeem script | `node btc_node.js --action decode-script --hex "..."` |
| Convert BTC address format | `node btc_node.js --action convert --address "..." --from legacy --to bech32` |
| Broadcast BTC tx | `node btc_node.js --action broadcast --hex "..."` |
| List local databases | `node idb_node.js --action dbs` |
| Init local database | `node idb_node.js --action init --db "..." --stores "s1,s2"` |
| List store records | `node idb_node.js --action list --db "..." --store "..."` |
| Read local record | `node idb_node.js --action read --db "..." --store "..." --key "..."` |
| Write local record | `node idb_node.js --action write --db "..." --store "..." --key "..." --value "..."` |
| Remove local record | `node idb_node.js --action remove --db "..." --store "..." --key "..."` |
| Clear store | `node idb_node.js --action clear --db "..." --store "..."` |
