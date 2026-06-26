/**
 * Node.js Messenger CLI — Bitcoin (BTC) Blockchain Operations
 *
 * Usage:
 *   node btc_node.js --action balance --address <BTC_ADDR>
 *   node btc_node.js --action history --address <BTC_ADDR>
 *   node btc_node.js --action tx --txid <TXID>
 *   node btc_node.js --action new-keys
 *   node btc_node.js --action validate --address <BTC_ADDR>
 *   node btc_node.js --action multisig --pubkeys "<PUB1,PUB2,PUB3>" --required <N>
 *   node btc_node.js --action convert --address <ADDR> --from <TYPE> --to <TYPE>
 *
 * Note: This script does NOT require FLO_PRIVATE_KEY — all actions are read-only
 *       or use keys you supply via flags. No funds are moved by this script.
 *       To send BTC, use the raw signed hex via --action broadcast.
 */

'use strict';

// ── Bootstrap ──
(function bootstrap() {
    const fs = require('fs');
    const vm = require('vm');
    const path = require('path');
    global.floGlobals = { blockchain: "FLO", application: "messenger", adminID: "FMRsefPydWznGWneLqi4ABeQAJeFvtS3aQ" };
    Object.defineProperty(global, 'navigator', { value: { userAgent: "node", plugins: [], mimeTypes: [], cookieEnabled: false, language: "en" }, writable: true, configurable: true });
    Object.defineProperty(global, 'screen', { value: { height: 1080, width: 1920 }, writable: true, configurable: true });
    global.history = { length: 0 };
    global.location = "node";
    global.window = global;
    global.require = require;
    // coinjs (inside lib.js) references document for localStorage fallback — stub it
    if (typeof global.document === 'undefined') {
        global.document = {
            createElement: () => ({}),
            getElementById: () => null,
            querySelector: () => null,
            addEventListener: () => {}
        };
        global.localStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };
    }
    if (typeof global.btoa === 'undefined') {
        global.btoa = s => Buffer.from(s, 'binary').toString('base64');
        global.atob = s => Buffer.from(s, 'base64').toString('binary');
    }
    // btcOperator needs fetch (Node 18+ has it natively; fallback for older)
    if (typeof global.fetch === 'undefined') {
        try { global.fetch = require('node-fetch'); } catch (e) { /* Node 18+ has fetch built-in */ }
    }
    function loadScript(fp) { vm.runInThisContext(fs.readFileSync(path.join(__dirname, fp), 'utf8'), { filename: fp }); }
    loadScript('scripts/lib.js');
    loadScript('scripts/btcOperator.js');
})();

// ── Parse CLI arguments ──

function parseArgs() {
    const args = process.argv.slice(2);
    const parsed = { required: 2, bech32: true };
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--action':  parsed.action  = args[++i]; break;
            case '--address': parsed.address = args[++i]; break;
            case '--txid':    parsed.txid    = args[++i]; break;
            case '--pubkeys': parsed.pubkeys = args[++i]; break;
            case '--required':parsed.required= parseInt(args[++i], 10); break;
            case '--from':    parsed.from    = args[++i]; break;
            case '--to':      parsed.to      = args[++i]; break;
            case '--hex':     parsed.hex     = args[++i]; break;
            case '--no-bech32': parsed.bech32 = false; break;
        }
    }
    return parsed;
}

// ── Actions ──

/**
 * Show BTC balance for an address.
 */
async function showBalance(address) {
    if (!address) throw new Error('--address is required for balance.');
    const type = btcOperator.validateAddress(address);
    if (!type) throw new Error(`Invalid Bitcoin address: ${address}`);

    console.log(`\n[btc] Fetching balance for: ${address}  (${type})`);
    const balance = await btcOperator.getBalance(address);

    console.log(`\n  Address : ${address}`);
    console.log(`  Type    : ${type}`);
    console.log(`  Balance : ${balance} BTC  (${btcOperator.util.BTC_to_Sat(balance).toLocaleString()} sat)\n`);
}

/**
 * Show transaction history for a BTC address.
 */
async function showHistory(address) {
    if (!address) throw new Error('--address is required for history.');
    const type = btcOperator.validateAddress(address);
    if (!type) throw new Error(`Invalid Bitcoin address: ${address}`);

    console.log(`\n[btc] Fetching transaction history for: ${address}`);
    const txs = await btcOperator.multiApi('txs', { addr: address });
    const list = Array.isArray(txs) ? txs : (txs.txs || txs.data || []);

    if (!list.length) {
        console.log('[btc] No transactions found.\n');
        return;
    }

    console.log(`\n${'='.repeat(65)}`);
    console.log(`  BTC TRANSACTION HISTORY  (${list.length} shown)`);
    console.log('='.repeat(65));

    for (const raw of list) {
        try {
            const tx = await btcOperator.util.format.tx(raw);
            const date = tx.time ? new Date(tx.time).toLocaleString() : 'pending';
            const isSender = tx.inputs && tx.inputs.some(i => i.prev_out && i.prev_out.addr === address);
            const dir = isSender ? 'SENT' : 'RECV';

            let netBTC = 0;
            if (tx.out) {
                tx.out.filter(o => o.addr === address).forEach(o => netBTC += o.value);
            }

            console.log(`\n  ${dir}  ${date}`);
            console.log(`  TXID   : ${tx.hash}`);
            if (tx.confirmations !== undefined) console.log(`  Conf   : ${tx.confirmations}`);
            if (isSender) {
                const receivers = (tx.out || []).filter(o => o.addr !== address);
                receivers.forEach(o => console.log(`  To     : ${o.addr}  (${btcOperator.util.Sat_to_BTC(o.value)} BTC)`));
            } else {
                console.log(`  Amount : ${btcOperator.util.Sat_to_BTC(netBTC)} BTC`);
            }
            if (tx.fee) console.log(`  Fee    : ${typeof tx.fee === 'number' ? btcOperator.util.Sat_to_BTC(tx.fee) : tx.fee} BTC`);
        } catch (e) {
            const txid = raw.txid || raw.hash || JSON.stringify(raw).slice(0, 60);
            console.log(`\n  TX: ${txid}`);
        }
    }
    console.log(`\n${'='.repeat(65)}\n`);
}

/**
 * Show details of a BTC transaction.
 */
async function showTx(txid) {
    if (!txid) throw new Error('--txid is required.');
    console.log(`\n[btc] Fetching transaction: ${txid}`);
    const tx = await btcOperator.multiApi('tx', { txid });

    console.log(`\n${'='.repeat(65)}`);
    console.log(`  BTC TRANSACTION`);
    console.log('='.repeat(65));
    console.log(`  TXID     : ${tx.hash}`);
    if (tx.time)         console.log(`  Time     : ${new Date(tx.time).toLocaleString()}`);
    if (tx.confirmations !== undefined) console.log(`  Confs    : ${tx.confirmations}`);
    if (tx.block_height) console.log(`  Block    : ${tx.block_height}`);
    if (tx.size)         console.log(`  Size     : ${tx.size} bytes`);
    if (tx.fee)          console.log(`  Fee      : ${typeof tx.fee === 'number' ? btcOperator.util.Sat_to_BTC(tx.fee) : tx.fee} BTC`);
    if (tx.inputs && tx.inputs.length) {
        console.log(`  Inputs   :`);
        tx.inputs.forEach(i => console.log(`    ${i.prev_out && i.prev_out.addr ? i.prev_out.addr : '?'}  →  ${i.prev_out && i.prev_out.value !== undefined ? btcOperator.util.Sat_to_BTC(i.prev_out.value) + ' BTC' : ''}`));
    }
    if (tx.out && tx.out.length) {
        console.log(`  Outputs  :`);
        tx.out.forEach(o => console.log(`    ${o.addr || '?'}  ←  ${o.value !== undefined ? btcOperator.util.Sat_to_BTC(o.value) + ' BTC' : ''}`));
    }
    console.log();
}

/**
 * Generate a brand-new BTC key pair (legacy + segwit + bech32 addresses).
 * WARNING: printed to stdout — store securely, never share.
 */
function generateNewKeys() {
    const keys = btcOperator.newKeys;
    console.log(`\n${'='.repeat(65)}`);
    console.log(`  NEW BITCOIN KEY PAIR`);
    console.log('='.repeat(65));
    console.log(`  WIF Private Key  : ${keys.wif}`);
    console.log(`  Public Key (hex) : ${keys.pubkey}`);
    console.log(`  Legacy Address   : ${keys.address}`);
    console.log(`  Segwit Address   : ${keys.segwitAddress}`);
    console.log(`  Bech32 Address   : ${keys.bech32Address}`);
    console.log(`\n  ⚠  Store your private key (WIF) securely. Never share it.\n`);
}

/**
 * Validate a BTC address and show its type.
 */
function validateAddress(address) {
    if (!address) throw new Error('--address is required for validate.');
    const type = btcOperator.validateAddress(address);
    if (!type) {
        console.log(`\n  ✗ Invalid Bitcoin address: ${address}\n`);
    } else {
        console.log(`\n  ✓ Valid Bitcoin address`);
        console.log(`    Address : ${address}`);
        console.log(`    Type    : ${type}\n`);
    }
}

/**
 * Generate a multisig address from public keys.
 */
function generateMultisig(pubkeysStr, required, bech32) {
    if (!pubkeysStr) throw new Error('--pubkeys "PUB1,PUB2,..." is required.');
    const pubkeys = pubkeysStr.split(',').map(s => s.trim()).filter(Boolean);
    if (pubkeys.length < 2) throw new Error('At least 2 public keys are required.');
    if (required > pubkeys.length) throw new Error(`--required (${required}) cannot exceed number of pubkeys (${pubkeys.length}).`);

    const result = btcOperator.multiSigAddress(pubkeys, required, bech32);

    console.log(`\n${'='.repeat(65)}`);
    console.log(`  MULTISIG ADDRESS  (${required}-of-${pubkeys.length})`);
    console.log('='.repeat(65));
    console.log(`  Address       : ${result.address}`);
    console.log(`  Redeem Script : ${result.redeemScript || result.redeemscript || result.witnessScript || result.witnessscript}`);
    console.log(`  Type          : ${bech32 ? 'bech32 (P2WSH)' : 'legacy (P2SH)'}`);
    console.log(`  Required sigs : ${required} of ${pubkeys.length}\n`);
}

/**
 * Decode a BTC redeem script.
 */
function decodeRedeemScript(hex, bech32) {
    if (!hex) throw new Error('--hex (redeem script hex) is required.');
    const decoded = btcOperator.decodeRedeemScript(hex, bech32);
    if (!decoded) {
        console.log('\n  ✗ Could not decode redeem script.\n');
        return;
    }
    console.log(`\n${'='.repeat(65)}`);
    console.log(`  DECODED REDEEM SCRIPT`);
    console.log('='.repeat(65));
    console.log(`  Address          : ${decoded.address}`);
    console.log(`  Required sigs    : ${decoded.required}`);
    console.log(`  Public Keys      :`);
    decoded.pubKeys.forEach((pk, i) => console.log(`    [${i + 1}] ${pk}`));
    console.log(`  Redeem Script    : ${decoded.redeemScript}\n`);
}

/**
 * Convert an address from one format to another.
 * Supported --from/--to combos: legacy, bech32, segwit, multisig
 */
function convertAddress(address, from, to) {
    if (!address) throw new Error('--address is required for convert.');
    if (!from || !to) throw new Error('--from and --to (address types) are required. Types: legacy, bech32, segwit, multisig');

    const key = `${from}2${to}`;
    const converters = {
        legacy2bech:      () => btcOperator.convert.legacy2bech(address),
        legacy2legacy:    () => btcOperator.convert.legacy2legacy(address),
        bech2legacy:      () => btcOperator.convert.bech2legacy(address),
        bech2bech:        () => btcOperator.convert.bech2bech(address),
        bech2multisig:    () => btcOperator.convert.bech2multisig(address),
        multisig2multisig:() => btcOperator.convert.multisig2multisig(address),
    };

    if (!converters[key])
        throw new Error(`Unsupported conversion: ${from} → ${to}. Supported: ${Object.keys(converters).map(k => k.replace('2', ' → ')).join(', ')}`);

    const result = converters[key]();
    if (!result) throw new Error(`Conversion failed — address may not be a valid ${from} address.`);

    console.log(`\n  Source  (${from.padEnd(8)}) : ${address}`);
    console.log(`  Result  (${to.padEnd(8)}) : ${result}\n`);
}

/**
 * Broadcast a raw signed BTC transaction.
 */
async function broadcastTx(hex) {
    if (!hex) throw new Error('--hex (signed raw transaction hex) is required.');
    console.log('\n[btc] Broadcasting transaction...');
    const txid = await btcOperator.broadcastTx(hex);
    console.log(`\n[btc] Transaction broadcast!`);
    console.log(`  TXID : ${txid}\n`);
}

// ── Main ──

async function main() {
    try {
        const args = parseArgs();

        switch (args.action) {
            case 'balance':    await showBalance(args.address); break;
            case 'history':    await showHistory(args.address); break;
            case 'tx':         await showTx(args.txid); break;
            case 'new-keys':   generateNewKeys(); break;
            case 'validate':   validateAddress(args.address); break;
            case 'multisig':   generateMultisig(args.pubkeys, args.required, args.bech32); break;
            case 'decode-script': decodeRedeemScript(args.hex, args.bech32); break;
            case 'convert':    convertAddress(args.address, args.from, args.to); break;
            case 'broadcast':  await broadcastTx(args.hex); break;

            default:
                console.log(`
Messenger Bitcoin (BTC) Operations (Node.js)

Usage: node btc_node.js --action <action> [options]

Actions:
  balance        --address <BTC_ADDR>              Show BTC balance
  history        --address <BTC_ADDR>              Show transaction history
  tx             --txid <TXID>                     Show transaction details
  new-keys                                         Generate a new BTC key pair
  validate       --address <BTC_ADDR>              Validate and identify address type
  multisig       --pubkeys "PUB1,PUB2,PUB3"        Generate M-of-N multisig address
                 --required <N>                    Number of required signatures
                [--no-bech32]                       Use legacy P2SH instead of bech32
  decode-script  --hex <REDEEM_SCRIPT_HEX>         Decode a multisig redeem script
                [--no-bech32]
  convert        --address <ADDR>                  Convert address format
                 --from <TYPE>                     Source type: legacy, bech32, segwit, multisig
                 --to <TYPE>                       Target type: legacy, bech32, multisig
  broadcast      --hex <SIGNED_TX_HEX>             Broadcast a signed raw transaction

Examples:
  node btc_node.js --action balance --address bc1q...
  node btc_node.js --action history --address 1A1zP1...
  node btc_node.js --action tx --txid 4a5e1e...
  node btc_node.js --action new-keys
  node btc_node.js --action validate --address bc1q...
  node btc_node.js --action multisig --pubkeys "02aa...,03bb...,02cc..." --required 2
  node btc_node.js --action convert --address 1A1zP1... --from legacy --to bech32
  node btc_node.js --action broadcast --hex 0200000001...

Note: No FLO_PRIVATE_KEY needed. This script reads from public Bitcoin blockchain APIs.
`);
        }

    } catch (error) {
        console.error('[error]', error.message || error);
        process.exitCode = 1;
    }

    setTimeout(() => process.exit(process.exitCode || 0), 300);
}

main();
