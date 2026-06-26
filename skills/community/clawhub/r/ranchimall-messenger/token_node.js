/**
 * Node.js Messenger CLI — FLO Token Operations
 *
 * Usage:
 *   node token_node.js --action balance [--address <FLO_ID>] [--token <TOKEN>]
 *   node token_node.js --action send --to <FLO_ID> --amount <N> [--token <TOKEN>] [--message <TEXT>]
 *   node token_node.js --action history [--address <FLO_ID>] [--token <TOKEN>]
 *   node token_node.js --action tx --txid <TXID>
 *
 * Security: Requires FLO_PRIVATE_KEY environment variable for 'send'.
 *
 * Note: 'balance', 'history', and 'tx' work without a private key when --address/--txid is given.
 *       Default token is 'rupee' (floGlobals.currency).
 *       'send' broadcasts a real on-chain token transfer — tokens move immediately.
 */

'use strict';

const { getPrivateKey } = require('./node_shared');

// ── Bootstrap: load FLO libraries (same pattern as flo_node.js) ──
(function bootstrap() {
    const fs = require('fs');
    const vm = require('vm');
    const path = require('path');
    const { WebSocket } = require('ws');
    global.WebSocket = WebSocket;
    global.floGlobals = {
        blockchain: "FLO",
        application: "messenger",
        adminID: "FMRsefPydWznGWneLqi4ABeQAJeFvtS3aQ",
        currency: "rupee",
        tokenURL: "https://ranchimallflo.ranchimall.net/"
    };
    Object.defineProperty(global, 'navigator', { value: { userAgent: "node", plugins: [], mimeTypes: [], cookieEnabled: false, language: "en" }, writable: true, configurable: true });
    Object.defineProperty(global, 'screen', { value: { height: 1080, width: 1920 }, writable: true, configurable: true });
    global.history = { length: 0 };
    global.location = "node";
    global.window = global;
    global.require = require;
    if (typeof global.btoa === 'undefined') {
        global.btoa = s => Buffer.from(s, 'binary').toString('base64');
        global.atob = s => Buffer.from(s, 'base64').toString('binary');
    }
    function loadScript(fp) { vm.runInThisContext(fs.readFileSync(path.join(__dirname, fp), 'utf8'), { filename: fp }); }
    loadScript('scripts/lib.js');
    loadScript('scripts/floCrypto.js');
    loadScript('scripts/floBlockchainAPI.js');
    loadScript('scripts/floTokenAPI.js');
})();

// ── Parse CLI arguments ──

function parseArgs() {
    const args = process.argv.slice(2);
    const parsed = { token: 'rupee', message: '' };
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--action':  parsed.action  = args[++i]; break;
            case '--to':      parsed.to      = args[++i]; break;
            case '--address': parsed.address = args[++i]; break;
            case '--amount':  parsed.amount  = parseFloat(args[++i]); break;
            case '--token':   parsed.token   = args[++i]; break;
            case '--message': parsed.message = args[++i]; break;
            case '--txid':    parsed.txid    = args[++i]; break;
            case '--receivers': parsed.receivers = args[++i]; break;
            case '--txdata':  parsed.txdata  = args[++i]; break;
            case '--apicall': parsed.apicall = args[++i]; break;
        }
    }
    return parsed;
}

// ── Actions ──

/**
 * Show token balance for an address.
 */
async function showBalance(address, token) {
    console.log(`\n[token] Fetching ${token} balance for: ${address}`);
    const balance = await floTokenAPI.getBalance(address, token);
    console.log(`\n  Address : ${address}`);
    console.log(`  Token   : ${token}`);
    console.log(`  Balance : ${balance}\n`);
}

/**
 * Send tokens from your address to a receiver.
 */
async function sendToken(privateKey, receiverAddr, amount, token, message) {
    if (!receiverAddr) throw new Error('--to (receiver address) is required.');
    if (!amount || isNaN(amount) || amount <= 0) throw new Error('--amount must be a positive number.');

    if (!floCrypto.validateAddr(receiverAddr))
        throw new Error(`Invalid receiver address: ${receiverAddr}`);

    const senderAddr = floCrypto.getFloID(privateKey);
    console.log(`\n[token] Preparing token transfer...`);
    console.log(`  From    : ${senderAddr}`);
    console.log(`  To      : ${receiverAddr}`);
    console.log(`  Amount  : ${amount} ${token}`);
    if (message) console.log(`  Message : ${message}`);

    const balance = await floTokenAPI.getBalance(senderAddr, token);
    console.log(`\n[token] Current ${token} balance: ${balance}`);

    if (amount > balance)
        throw new Error(`Insufficient ${token} balance. Have ${balance}, need ${amount}.`);

    console.log('[token] Broadcasting token transfer...');
    const txid = await floTokenAPI.sendToken(privateKey, amount, receiverAddr, message, token);

    console.log(`\n[token] Token transfer broadcast!`);
    console.log(`  TXID     : ${txid}`);
    console.log(`  Explorer : https://ranchimallflo.ranchimall.net/transaction/${txid}\n`);
}

/**
 * Show token transaction history for an address.
 */
async function showHistory(address, token) {
    console.log(`\n[token] Fetching ${token} transaction history for: ${address}`);
    const result = await floTokenAPI.getAllTxs(address, token);

    const txs = result.transactions || result.data || result || [];
    const list = Array.isArray(txs) ? txs : Object.values(txs);

    if (list.length === 0) {
        console.log('[token] No token transactions found.\n');
        return;
    }

    console.log(`\n${'='.repeat(65)}`);
    console.log(`  TOKEN HISTORY  (${token}, address: ${address})`);
    console.log('='.repeat(65));

    for (const tx of list) {
        try {
            const parsed = floTokenAPI.util.parseTxData(tx);
            const date = parsed.time ? new Date(parsed.time).toLocaleString() : 'unknown';
            const dir = parsed.sender === address ? 'SENT' : 'RECV';
            console.log(`\n  ${dir}  ${date}`);
            console.log(`  TXID     : ${tx.txid || tx.transactionDetails?.txid || '?'}`);
            if (parsed.transferType) console.log(`  Type     : ${parsed.transferType}`);
            if (parsed.tokenAmount) console.log(`  Amount   : ${parsed.tokenAmount} ${parsed.tokenIdentification || token}`);
            if (parsed.sender)   console.log(`  From     : ${parsed.sender}`);
            if (parsed.receiver) console.log(`  To       : ${parsed.receiver}`);
        } catch (e) {
            console.log(`  TX: ${JSON.stringify(tx).slice(0, 120)}...`);
        }
    }
    console.log(`\n${'='.repeat(65)}\n`);
}

/**
 * Show details of a specific token transaction.
 */
async function showTx(txid) {
    if (!txid) throw new Error('--txid is required.');
    console.log(`\n[token] Fetching transaction: ${txid}`);
    const tx = await floTokenAPI.getTx(txid);
    const parsed = floTokenAPI.util.parseTxData(tx);

    console.log(`\n${'='.repeat(65)}`);
    console.log(`  TOKEN TRANSACTION`);
    console.log('='.repeat(65));
    console.log(`  TXID   : ${txid}`);
    if (parsed.time)                 console.log(`  Time   : ${new Date(parsed.time).toLocaleString()}`);
    if (parsed.tokenAmount)          console.log(`  Amount : ${parsed.tokenAmount} ${parsed.tokenIdentification || ''}`);
    if (parsed.sender)               console.log(`  From   : ${parsed.sender}`);
    if (parsed.receiver)             console.log(`  To     : ${parsed.receiver}`);
    if (parsed.transferType)         console.log(`  Type   : ${parsed.transferType}`);
    if (parsed.message)              console.log(`  Note   : ${parsed.message}`);
    console.log(`\n  Full: https://ranchimallflo.ranchimall.net/transaction/${txid}\n`);
}

async function bulkTransfer(privateKey, receiversStr, token) {
    if (!receiversStr) throw new Error('--receivers "addr1:0.1,addr2:0.2" is required.');
    const receiversObj = {};
    receiversStr.split(',').forEach(s => {
        const [addr, amount] = s.split(':');
        receiversObj[addr.trim()] = parseFloat(amount.trim());
    });
    const sender = floCrypto.getFloID(privateKey);
    console.log(`\n[token] Bulk transferring ${token}...`);
    const txid = await floTokenAPI.bulkTransferTokens(sender, privateKey, token, receiversObj);
    console.log(`\n  ✓ Broadcasted!\n  TXID : ${txid}\n`);
}

function parseTx(txdata) {
    if (!txdata) throw new Error('--txdata is required.');
    let data;
    try { data = JSON.parse(txdata); } catch (e) { data = txdata; }
    console.log(`\n[token] Parsing TX Data...`);
    const parsed = floTokenAPI.util.parseTxData(data);
    console.log(`\n  Parsed Data:\n`, JSON.stringify(parsed, null, 2), '\n');
}

async function rawFetch(apicall) {
    if (!apicall) throw new Error('--apicall is required (e.g. "api/v1.0/getTx?txid=...").');
    console.log(`\n[token] Raw Fetch: ${apicall}...`);
    // Some versions of floTokenAPI expose fetch wrapper natively
    const result = await floTokenAPI.fetch ? await floTokenAPI.fetch(apicall) : await fetch(floGlobals.tokenURL + apicall).then(r => r.json());
    console.log(`\n  Response:\n`, JSON.stringify(result, null, 2), '\n');
}


// ── Main ──

async function main() {
    try {
        const args = parseArgs();

        switch (args.action) {
            case 'balance': {
                let address = args.address;
                if (!address) {
                    const pk = getPrivateKey();
                    address = floCrypto.getFloID(pk);
                }
                await showBalance(address, args.token);
                break;
            }

            case 'send': {
                const pk = getPrivateKey();
                await sendToken(pk, args.to, args.amount, args.token, args.message);
                break;
            }

            case 'history': {
                let address = args.address;
                if (!address) {
                    const pk = getPrivateKey();
                    address = floCrypto.getFloID(pk);
                }
                await showHistory(address, args.token);
                break;
            }

            case 'tx': {
                await showTx(args.txid);
                break;
            }

            case 'bulk-transfer': {
                const pk = getPrivateKey();
                await bulkTransfer(pk, args.receivers, args.token);
                break;
            }

            case 'parse-tx': {
                parseTx(args.txdata);
                break;
            }

            case 'raw-fetch': {
                await rawFetch(args.apicall);
                break;
            }

            default:
                console.log(`
Messenger FLO Token Operations (Node.js)

Usage: node token_node.js --action <action> [options]

Actions:
  balance         [--address <FLO_ID>]         Show token balance (defaults to your address)
                  [--token <TOKEN>]             Token name (default: rupee)

  send             --to <FLO_ID>               Send tokens to an address
                   --amount <N>                 Amount to send
                  [--token <TOKEN>]             Token name (default: rupee)
                  [--message <TEXT>]            Optional note attached to the transfer

  history         [--address <FLO_ID>]         Token transaction history (defaults to your address)
                  [--token <TOKEN>]             Token name (default: rupee)

  tx               --txid <TXID>               Show details of a specific token transaction

  bulk-transfer    --receivers "R1:0.1,R2:0.2" [--token <TOKEN>]
  parse-tx         --txdata <JSON|HEX>
  raw-fetch        --apicall <API_PATH>

Examples:
  node token_node.js --action balance
  node token_node.js --action send --to FBhHiN... --amount 50 --token rupee --message "payment"
  node token_node.js --action bulk-transfer --receivers "addr1:10,addr2:20"
  node token_node.js --action raw-fetch --apicall "api/v1.0/getTx?txid=..."

Prerequisites:
  FLO_PRIVATE_KEY environment variable must be set (for send/bulk-transfer).
`);
        }

    } catch (error) {
        console.error('[error]', error.message || error);
        process.exitCode = 1;
    }

    setTimeout(() => process.exit(process.exitCode || 0), 300);
}

main();
