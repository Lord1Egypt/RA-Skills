/**
 * Node.js Messenger API - Send messages without a browser
 * 
 * Usage:
 *   node send_node.js
 * 
 * Prerequisites:
 *   npm install ws
 * 
 * The libraries (lib.js, floCrypto.js, floCloudAPI.js, floBlockchainAPI.js)
 * already support Node.js via their IIFE bindings:
 *   - lib.js:              (GLOBAL) => typeof global !== "undefined" ? global : window
 *   - floCrypto.js:        'object' === typeof module ? module.exports : window.floCrypto
 *   - floCloudAPI.js:      'object' === typeof module ? module.exports : window.floCloudAPI
 *   - floBlockchainAPI.js: 'object' === typeof module ? module.exports : window.floBlockchainAPI
 */

'use strict';

// ── 1. Polyfill browser globals that lib.js needs for entropy ──

const { WebSocket } = require('ws');
global.WebSocket = WebSocket;

// floGlobals must exist before loading lib.js (it reads floGlobals.blockchain)
global.floGlobals = {
    blockchain: "FLO",
    application: "messenger",
    adminID: "FMRsefPydWznGWneLqi4ABeQAJeFvtS3aQ"
};

// lib.js SecureRandom uses these for entropy seeding (fake values are fine)
// Node.js 22+ has some of these as read-only getters, so use defineProperty
Object.defineProperty(global, 'navigator', {
    value: { userAgent: "node", plugins: [], mimeTypes: [], cookieEnabled: false, language: "en" },
    writable: true, configurable: true
});
Object.defineProperty(global, 'screen', {
    value: { height: 1080, width: 1920, colorDepth: 24, availHeight: 1080, availWidth: 1920, pixelDepth: 24 },
    writable: true, configurable: true
});
global.history = { length: 0 };
global.location = "node";

// btoa/atob 
if (typeof global.btoa === 'undefined') {
    global.btoa = (str) => Buffer.from(str, 'binary').toString('base64');
    global.atob = (b64) => Buffer.from(b64, 'base64').toString('binary');
}

// ── 2. Load the libraries in dependency order ──
// Using vm.runInThisContext (like browser <script> tags) instead of require()
// because require() wraps code in a module function, preventing libraries
// from finding each other as bare globals (e.g., floCrypto, Crypto, etc.)

const fs = require('fs');
const vm = require('vm');
const path = require('path');

// Set window = global so the IIFE browser-path assignments (window.X = {}) work
global.window = global;

function loadScript(filePath) {
    const fullPath = path.join(__dirname, filePath);
    const code = fs.readFileSync(fullPath, 'utf8');
    vm.runInThisContext(code, { filename: filePath });
}

// Expose require globally so lib.js can use `require('crypto')` for secure random
global.require = require;

loadScript('scripts/lib.js');             // → sets globals: Crypto, BigInteger, Bitcoin, bitjs, coinjs, ripemd160, etc.
loadScript('scripts/floCrypto.js');        // → sets global.floCrypto
loadScript('scripts/floBlockchainAPI.js'); // → sets global.floBlockchainAPI
loadScript('scripts/floCloudAPI.js');      // → sets global.floCloudAPI

// ── 3. Bootstrap: Fetch supernode list from blockchain & init cloud ──

async function initCloud() {
    console.log('[init] Fetching supernode list from FLO blockchain...');

    const SNStorageID = floCloudAPI.SNStorageID; // "FNaN9McoBAEFUjkRmNQRYLmBF8SpS7Tgfk"
    const result = await floBlockchainAPI.readData(SNStorageID, {
        sentOnly: true,
        pattern: "SuperNodeStorage"
    });

    let nodes = {};
    for (let i = result.data.length - 1; i >= 0; i--) {
        let content = JSON.parse(result.data[i])["SuperNodeStorage"];
        if (content.removeNodes)
            for (let sn in content.removeNodes) delete nodes[sn];
        if (content.newNodes)
            for (let sn in content.newNodes) nodes[sn] = content.newNodes[sn];
        if (content.updateNodes)
            for (let sn in content.updateNodes)
                if (sn in nodes) nodes[sn].uri = content.updateNodes[sn];
    }

    const nodeCount = Object.keys(nodes).length;
    console.log(`[init] Found ${nodeCount} supernodes`);

    if (nodeCount === 0) throw new Error('No supernodes found!');

    await floCloudAPI.init(nodes);
    console.log('[init] Cloud initialized successfully');
    return nodes;
}

// ── 4. Parse CLI arguments ──

function parseArgs() {
    const args = process.argv.slice(2);
    const parsed = {};
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--sender': parsed.sender = args[++i]; break;
            case '--receiver': parsed.receiver = args[++i]; break;
            case '--message': parsed.message = args[++i]; break;
            case '--encrypt': parsed.encrypt = args[++i]; break;
        }
    }

    // Security: strictly require the private key from the environment
    if (process.env.FLO_PRIVATE_KEY) {
        parsed.key = process.env.FLO_PRIVATE_KEY;
    }

    return parsed;
}

// ── 5. Readline helper (for interactive mode) ──

function createReadline() {
    const readline = require('readline');
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    function ask(question) {
        return new Promise(resolve => {
            rl.question(question, answer => resolve(answer.trim()));
        });
    }
    return { rl, ask };
}

// ── 6. Send a message ──

async function sendMessage(senderPrivKey, receiverFloID, message, encrypt = false) {
    // Auto-derive FLO ID from private key
    const senderFloID = floCrypto.getFloID(senderPrivKey);
    if (!senderFloID) throw new Error('Invalid private key — could not derive FLO ID');

    floCloudAPI.user(senderFloID, senderPrivKey);
    console.log(`\n[send] Sender: ${senderFloID}`);
    console.log(`[send] Receiver: ${receiverFloID}`);
    console.log(`[send] Message: ${message}`);

    let payload = message;

    if (encrypt && typeof encrypt === 'string') {
        payload = floCrypto.encryptData(message, encrypt);
        console.log('[send] Message encrypted');
    }

    const result = await floCloudAPI.sendApplicationData(payload, 'MESSAGE', {
        receiverID: receiverFloID,
        application: 'messenger'
    });

    console.log('[send] Message sent successfully!', result);
    return result;
}

// ── 7. Main ──

async function main() {
    try {
        await initCloud();

        const args = parseArgs();

        // Strict enforcement: Private key must come from the environment
        if (!args.key) {
            throw new Error('FLO_PRIVATE_KEY environment variable is missing. It must be set for secure execution.');
        }

        // Required fields must be populated
        if (args.key && args.receiver && args.message) {
            await sendMessage(args.key, args.receiver, args.message, args.encrypt);
        }
        // Interactive mode: prompt the user for missing fields (except key)
        else {
            const { rl, ask } = createReadline();
            console.log('\n--- Messenger (Node.js) ---\n');
            console.log('[info] Using securely loaded private key from environment.');

            const receiverID = args.receiver || await ask('Enter receiver FLO ID: ');
            const message = args.message || await ask('Enter message: ');

            await sendMessage(args.key, receiverID, message);
            rl.close();
        }

    } catch (error) {
        console.error('[error]', error);
        process.exitCode = 1;
    }

    setTimeout(() => process.exit(process.exitCode || 0), 100);
}

main();


