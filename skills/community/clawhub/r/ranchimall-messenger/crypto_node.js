/**
 * Node.js Messenger CLI — Pure Cryptography Operations
 *
 * Usage:
 *   node crypto_node.js --action <action> [options]
 *
 * Note: This script performs pure, offline cryptography operations.
 *       No cloud connection or FLO_PRIVATE_KEY environment variable is required
 *       unless you are specifically using the decrypt/sign commands.
 */

'use strict';

const fs = require('fs');
const vm = require('vm');
const path = require('path');

// ── Bootstrap ──
(function bootstrap() {
    global.window = global;
    global.require = require;
    global.history = { length: 0 };
    global.location = "node";
    Object.defineProperty(global, 'navigator', { value: { userAgent: "node", plugins: [], mimeTypes: [], cookieEnabled: false, language: "en" }, writable: true, configurable: true });
    Object.defineProperty(global, 'screen', { value: { height: 1080, width: 1920, colorDepth: 24 }, writable: true, configurable: true });
    if (typeof global.btoa === 'undefined') {
        global.btoa = s => Buffer.from(s, 'binary').toString('base64');
        global.atob = s => Buffer.from(s, 'base64').toString('binary');
    }
    const loadScript = fp => vm.runInThisContext(fs.readFileSync(path.join(__dirname, fp), 'utf8'), { filename: fp });
    loadScript('scripts/lib.js');
    loadScript('scripts/floCrypto.js');
})();

// ── Parse CLI arguments ──
function parseArgs() {
    const args = process.argv.slice(2);
    const parsed = { };
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--action':  parsed.action  = args[++i]; break;
            case '--privkey': parsed.privkey = args[++i]; break;
            case '--pubkey':  parsed.pubkey  = args[++i]; break;
            case '--address': parsed.address = args[++i]; break;
            case '--data':    parsed.data    = args[++i]; break;
            case '--sig':     parsed.sig     = args[++i]; break;
            case '--secret':  parsed.secret  = args[++i]; break;
            case '--shares':  parsed.shares  = args[++i]; break;
            case '--threshold': parsed.threshold = parseInt(args[++i], 10); break;
            case '--length':  parsed.length  = parseInt(args[++i], 10); break;
            case '--min':     parsed.min     = parseInt(args[++i], 10); break;
            case '--max':     parsed.max     = parseInt(args[++i], 10); break;
        }
    }
    return parsed;
}

// ── Actions ──

function getPubkey(privkey) {
    if (!privkey) throw new Error('--privkey is required.');
    console.log(`\n  Public Key : ${floCrypto.getPubKeyHex(privkey)}\n`);
}

function getAddress(pubOrPriv) {
    if (!pubOrPriv) throw new Error('Provide --pubkey or --privkey.');
    // Check if it's a pubkey (hex) or WIF
    if (pubOrPriv.length === 66 && (pubOrPriv.startsWith('02') || pubOrPriv.startsWith('03'))) {
        console.log(`\n  Address (from PubKey) : ${floCrypto.getAddress(pubOrPriv)}\n`);
    } else {
        console.log(`\n  Address (from PrivKey): ${floCrypto.getFloID(pubOrPriv)}\n`);
    }
}

function verifyPrivkey(privkey) {
    if (!privkey) throw new Error('--privkey is required.');
    const valid = floCrypto.verifyPrivKey(privkey);
    console.log(`\n  Valid Private Key? : ${valid ? 'Yes ✓' : 'No ✗'}\n`);
}

function validateAddress(address) {
    if (!address) throw new Error('--address is required.');
    // Try both validateAddr and validateFloID for robustness, though usually they are the same or one wraps the other
    const valid = floCrypto.validateAddr(address) || floCrypto.validateFloID(address);
    console.log(`\n  Valid Address? : ${valid ? 'Yes ✓' : 'No ✗'}\n`);
}

function verifyPubkey(pubkey) {
    if (!pubkey) throw new Error('--pubkey is required.');
    const valid = floCrypto.verifyPubKey(pubkey);
    console.log(`\n  Valid Public Key? : ${valid ? 'Yes ✓' : 'No ✗'}\n`);
}

function encrypt(data, pubkey) {
    if (!data || !pubkey) throw new Error('--data and --pubkey are required.');
    const enc = floCrypto.encryptData(data, pubkey);
    console.log(`\n  Encrypted Data :\n  ${typeof enc === 'object' ? JSON.stringify(enc) : enc}\n`);
}

function decrypt(data, privkey) {
    if (!data || !privkey) throw new Error('--data and --privkey are required.');
    const dec = floCrypto.decryptData(data, privkey);
    console.log(`\n  Decrypted Data :\n  ${dec}\n`);
}

function sign(data, privkey) {
    if (!data || !privkey) throw new Error('--data and --privkey are required.');
    const sig = floCrypto.signData(data, privkey);
    console.log(`\n  Signature :\n  ${sig}\n`);
}

function verifySign(data, sig, pubkey) {
    if (!data || !sig || !pubkey) throw new Error('--data, --sig, and --pubkey are required.');
    const valid = floCrypto.verifySign(data, sig, pubkey);
    console.log(`\n  Valid Signature? : ${valid ? 'Yes ✓' : 'No ✗'}\n`);
}

function randInt(min, max) {
    if (isNaN(min) || isNaN(max)) throw new Error('--min and --max are required.');
    console.log(`\n  Random Integer : ${floCrypto.randInt(min, max)}\n`);
}

function randString(length) {
    if (!length) throw new Error('--length is required.');
    console.log(`\n  Random String : ${floCrypto.randString(length, false)}\n`);
}

function shamirCreate(secret, numShares, threshold) {
    if (!secret || !numShares || !threshold) throw new Error('--secret, --shares (N), and --threshold (M) are required.');
    const shares = floCrypto.createShamirsSecretShares(secret, numShares, threshold);
    console.log(`\n  SHAMIR'S SECRET SHARES (${threshold} of ${numShares} required)\n`);
    shares.forEach((s, i) => console.log(`  [Share ${i+1}] : ${s}`));
    console.log('\n');
}

function shamirRetrieve(sharesStr) {
    if (!sharesStr) throw new Error('--shares "S1,S2,..." is required.');
    const shares = sharesStr.split(',').map(s => s.trim()).filter(Boolean);
    const secret = floCrypto.retrieveShamirSecret(shares);
    if (!secret) console.log(`\n  ✗ Failed to retrieve secret. (Not enough shares or invalid)\n`);
    else console.log(`\n  Retrieved Secret : ${secret}\n`);
}

function shamirVerify(sharesStr, secret) {
    if (!sharesStr || !secret) throw new Error('--shares "S1,S2,..." and --secret are required.');
    const shares = sharesStr.split(',').map(s => s.trim()).filter(Boolean);
    const valid = floCrypto.verifyShamirsSecret(shares, secret);
    console.log(`\n  Shares match secret? : ${valid ? 'Yes ✓' : 'No ✗'}\n`);
}

// ── Main ──

async function main() {
    try {
        const args = parseArgs();

        switch (args.action) {
            case 'get-pubkey':       getPubkey(args.privkey); break;
            case 'get-address':      getAddress(args.pubkey || args.privkey); break;
            case 'verify-privkey':   verifyPrivkey(args.privkey); break;
            case 'validate-address': validateAddress(args.address); break;
            case 'verify-pubkey':    verifyPubkey(args.pubkey); break;
            case 'encrypt':          encrypt(args.data, args.pubkey); break;
            case 'decrypt':          decrypt(args.data, args.privkey); break;
            case 'sign':             sign(args.data, args.privkey); break;
            case 'verify-sign':      verifySign(args.data, args.sig, args.pubkey); break;
            case 'rand-int':         randInt(args.min, args.max); break;
            case 'rand-string':      randString(args.length); break;
            case 'shamir-create':    shamirCreate(args.secret, parseInt(args.shares,10), args.threshold); break;
            case 'shamir-retrieve':  shamirRetrieve(args.shares); break;
            case 'shamir-verify':    shamirVerify(args.shares, args.secret); break;
            default:
                console.log(`
Messenger Crypto Node Operations

Usage: node crypto_node.js --action <action> [options]

Actions:
  get-pubkey        --privkey <WIF>
  get-address       --pubkey <HEX> OR --privkey <WIF>
  verify-privkey    --privkey <WIF>
  validate-address  --address <FLO_ID>
  verify-pubkey     --pubkey <HEX>
  encrypt           --data <TEXT> --pubkey <HEX>
  decrypt           --data <HEX> --privkey <WIF>
  sign              --data <TEXT> --privkey <WIF>
  verify-sign       --data <TEXT> --sig <HEX> --pubkey <HEX>
  rand-int          --min <N> --max <M>
  rand-string       --length <N>
  shamir-create     --secret <TEXT> --shares <N> --threshold <M>
  shamir-retrieve   --shares "SHARE1,SHARE2,..."
  shamir-verify     --shares "SHARE1,SHARE2,..." --secret <TEXT>
`);
        }

    } catch (error) {
        console.error('[error]', error.message || error);
        process.exitCode = 1;
    }
}

main();
