/**
 * node_shared.js — Shared bootstrap for all messenger Node.js CLI scripts
 *
 * Handles:
 *  - Browser global polyfills (WebSocket, navigator, screen, btoa/atob)
 *  - Library loading via vm.runInThisContext (lib.js, floCrypto, floBlockchainAPI, floCloudAPI)
 *  - Supernode discovery & cloud initialization
 *  - Identity setup via FLO_PRIVATE_KEY env variable
 *  - Cloud message decryption helper
 */

'use strict';

// ── 1. Polyfill browser globals that lib.js needs ──

const { WebSocket } = require('ws');
global.WebSocket = WebSocket;

global.floGlobals = {
    blockchain: "FLO",
    application: "messenger",
    adminID: "FMRsefPydWznGWneLqi4ABeQAJeFvtS3aQ"
};

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

if (typeof global.btoa === 'undefined') {
    global.btoa = (str) => Buffer.from(str, 'binary').toString('base64');
    global.atob = (b64) => Buffer.from(b64, 'base64').toString('binary');
}

// ── 2. Load the FLO libraries in dependency order ──

const fs   = require('fs');
const vm   = require('vm');
const path = require('path');

global.window  = global;
global.require = require;  // expose so lib.js can require('crypto')

function loadScript(filePath) {
    const fullPath = path.join(__dirname, filePath);
    const code = fs.readFileSync(fullPath, 'utf8');
    vm.runInThisContext(code, { filename: filePath });
}

loadScript('scripts/lib.js');              // → Crypto, BigInteger, Bitcoin, bitjs, …
loadScript('scripts/floCrypto.js');         // → global.floCrypto
loadScript('scripts/floBlockchainAPI.js');  // → global.floBlockchainAPI
loadScript('scripts/floCloudAPI.js');       // → global.floCloudAPI

// ── 3. Supernode discovery & cloud init ──

async function initCloud() {
    console.log('[init] Fetching supernode list from FLO blockchain...');

    const SNStorageID = floCloudAPI.SNStorageID;
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

// ── 4. Credential helpers ──

function getPrivateKey() {
    const key = process.env.FLO_PRIVATE_KEY;
    if (!key) throw new Error('FLO_PRIVATE_KEY environment variable is missing. Set it securely before running.');
    return key;
}

function setupUser(privateKey) {
    const floID = floCrypto.getFloID(privateKey);
    if (!floID) throw new Error('Invalid private key — could not derive FLO ID');
    floCloudAPI.user(floID, privateKey);
    return floID;
}

// ── 5. Cloud message decryption helper ──
// Messages sent with encrypt=true arrive as { secret: "..." } objects.
// This function transparently decrypts them using the recipient's private key.

function decryptCloudMessage(message, privateKey) {
    if (!message) return message;

    // Already an encrypted object { secret: "..." }
    if (typeof message === 'object' && message !== null && 'secret' in message) {
        try { return floCrypto.decryptData(message, privateKey); } catch (e) { return null; }
    }

    // String — try to decode first, then decrypt if it resolves to an encrypted object
    if (typeof message === 'string') {
        let decoded = message;
        try { decoded = floCloudAPI.util.decodeMessage(message); } catch (e) { /* leave as-is */ }
        if (typeof decoded === 'object' && decoded !== null && 'secret' in decoded) {
            try { return floCrypto.decryptData(decoded, privateKey); } catch (e) { return null; }
        }
        return decoded;
    }

    return message;
}

module.exports = { initCloud, getPrivateKey, setupUser, decryptCloudMessage };
