/**
 * Node.js Messenger CLI — DApp Node Operations
 *
 * Usage:
 *   node dapp_node.js --action manage-subadmins --add "FLO_ID" --rm "FLO_ID"
 *   node dapp_node.js --action secure-privkey --pin "1234"
 *
 * Security: Requires FLO_PRIVATE_KEY environment variable.
 */

'use strict';

const fs = require('fs');
const { getPrivateKey } = require('./node_shared');

(function bootstrap() {
    const vm = require('vm');
    const path = require('path');
    const { WebSocket } = require('ws');
    global.WebSocket = WebSocket;
    global.floGlobals = { blockchain: "FLO", application: "messenger", adminID: "FMRsefPydWznGWneLqi4ABeQAJeFvtS3aQ" };
    global.window = global;
    global.require = require;
    Object.defineProperty(global, 'navigator', { value: { userAgent: "node", plugins: [], mimeTypes: [], cookieEnabled: false, language: "en" }, writable: true, configurable: true });
    Object.defineProperty(global, 'screen', { value: { height: 1080, width: 1920, colorDepth: 24 }, writable: true, configurable: true });
    if (typeof global.btoa === 'undefined') {
        global.btoa = s => Buffer.from(s, 'binary').toString('base64');
        global.atob = s => Buffer.from(s, 'base64').toString('binary');
    }
    const loadScript = fp => vm.runInThisContext(fs.readFileSync(path.join(__dirname, fp), 'utf8'), { filename: fp });
    loadScript('scripts/lib.js');
    loadScript('scripts/floCrypto.js');
    loadScript('scripts/floBlockchainAPI.js');
    loadScript('scripts/floCloudAPI.js');
    loadScript('scripts/floDapps.js');
})();

// ── Parse CLI arguments ──
function parseArgs() {
    const args = process.argv.slice(2);
    const parsed = { };
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--action': parsed.action = args[++i]; break;
            case '--add':    parsed.add    = args[++i]; break;
            case '--rm':     parsed.rm     = args[++i]; break;
            case '--pin':    parsed.pin    = args[++i]; break;
            case '--settings': parsed.settings = args[++i]; break;
            case '--type':   parsed.type   = args[++i]; break;
            case '--vector': parsed.vector = args[++i]; break;
        }
    }
    return parsed;
}

// ── Actions ──

async function manageSubAdmins(privateKey, addList, rmList, settingsStr) {
    console.log(`\n[dapp] Managing App Config (SubAdmins)...`);
    const adminID = floCrypto.getFloID(privateKey);
    
    const floData = {
        type: "appConfig",
        application: floGlobals.application
    };
    
    if (addList) floData.addSubAdmin = addList.split(',').map(s => s.trim());
    if (rmList) floData.removeSubAdmin = rmList.split(',').map(s => s.trim());
    if (settingsStr) {
        try { floData.settings = JSON.parse(settingsStr); }
        catch (e) { console.error('Invalid settings JSON'); return; }
    }

    console.log(`  Writing Config:`, JSON.stringify(floData));
    const txid = await floBlockchainAPI.writeData(adminID, JSON.stringify(floData), privateKey);
    console.log(`\n  ✓ Broadcasted!\n  TXID : ${txid}\n`);
}

function securePrivKey(privateKey, pwd) {
    if (!pwd) throw new Error('--pin (password/PIN) is required.');
    console.log(`\n[dapp] Securing Private Key with PIN: ${pwd}`);

    let encryptedKey = Crypto.AES.encrypt(privateKey, pwd);
    let shares = floCrypto.createShamirsSecretShares(encryptedKey, 2, 2);

    console.log(`\n  ✓ Key Secured using Shamir & AES`);
    console.log(`\n  Your Secure Login Shares (Keep these safe, or save them in your custom vault!):`);
    console.log(`  Share 1 : ${shares[0]}`);
    console.log(`  Share 2 : ${shares[1]}\n`);
    console.log(`  To restore your key later, you will need BOTH shares AND your PIN.\n`);
}

async function getNextGeneral(type, vectorClock) {
    if (!type) throw new Error('--type is required.');
    console.log(`\n[dapp] Fetching next general data for type: ${type}`);
    const result = await floDapps.getNextGeneralData(type, vectorClock || '0');
    console.log(`\n  Result:\n`, JSON.stringify(result, null, 2), '\n');
}

// ── Main ──

async function main() {
    try {
        const args = parseArgs();
        const privateKey = getPrivateKey();

        switch (args.action) {
            case 'manage-subadmins': await manageSubAdmins(privateKey, args.add, args.rm, args.settings); break;
            case 'secure-privkey':   securePrivKey(privateKey, args.pin); break;
            case 'get-next-general': await getNextGeneral(args.type, args.vector); break;
            default:
                console.log(`
Messenger DApp Node Operations

Usage: node dapp_node.js --action <action> [options]

Actions:
  manage-subadmins   [--add "FLO_ID1,FLO_ID2"] [--rm "FLO_ID3"] [--settings '{"key":"val"}']
  secure-privkey     --pin <PASSWORD>
  get-next-general   --type <TYPE> [--vector <CLOCK_ID>]

Prerequisites:
  FLO_PRIVATE_KEY environment variable must be set.
`);
        }

    } catch (error) {
        console.error('[error]', error.message || error);
        process.exitCode = 1;
    }

    setTimeout(() => process.exit(process.exitCode || 0), 300);
}

main();
