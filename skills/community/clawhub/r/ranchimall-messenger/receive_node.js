/**
 * Node.js Messenger API - Receive messages without a browser
 * 
 * Usage:
 *   node receive_node.js [--sender <FLO_ID>] [--limit <number>] [--decrypt]
 * 
 * Prerequisites:
 *   npm install ws
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

// ── 2. Load the libraries in dependency order ──

const fs = require('fs');
const vm = require('vm');
const path = require('path');

global.window = global;

function loadScript(filePath) {
    const fullPath = path.join(__dirname, filePath);
    const code = fs.readFileSync(fullPath, 'utf8');
    vm.runInThisContext(code, { filename: filePath });
}

global.require = require;

loadScript('scripts/lib.js');             
loadScript('scripts/floCrypto.js');        
loadScript('scripts/floBlockchainAPI.js'); 
loadScript('scripts/floCloudAPI.js');      

// ── 3. Bootstrap: Fetch supernode list from blockchain & init cloud ──

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

// ── 4. Parse CLI arguments ──

function parseArgs() {
    const args = process.argv.slice(2);
    const parsed = { limit: 50, decrypt: false, watch: false };
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--sender': parsed.sender = args[++i]; break;
            case '--limit': parsed.limit = parseInt(args[++i], 10); break;
            case '--decrypt': parsed.decrypt = true; break;
            case '--watch': parsed.watch = true; break;
        }
    }

    if (process.env.FLO_PRIVATE_KEY) {
        parsed.key = process.env.FLO_PRIVATE_KEY;
    }

    return parsed;
}

// ── 5. Receive messages ──

async function receiveMessages(receiverPrivKey, options = {}) {
    const receiverFloID = floCrypto.getFloID(receiverPrivKey);
    if (!receiverFloID) throw new Error('Invalid private key — could not derive FLO ID');

    console.log(`\n[receive] Fetching messages for: ${receiverFloID}`);
    if (options.sender) console.log(`[receive] Filtering by sender: ${options.sender}`);
    if (options.limit && !options.watch) console.log(`[receive] Limiting to latest ${options.limit} messages.`);
    if (options.watch) console.log(`[receive] Watch mode enabled. Listening for live messages...`);
    
    let requestOptions = {
        receiverID: receiverFloID
    };
    if (options.sender) requestOptions.senderID = options.sender;

    const printMessage = (msg) => {
        let text = undefined;
        try {
            text = msg.message;
            if (typeof text === 'string') {
                try {
                    text = floCloudAPI.util.decodeMessage(text);
                } catch (e) { }
            }

            if (options.decrypt) {
                try {
                    const decrypted = floCrypto.decryptData(text, receiverPrivKey);
                    if (decrypted) text = `[Decrypted] ${decrypted}`;
                } catch (e) {
                    // not cleanly decryptable
                }
            } else if (typeof text === 'string' && text.startsWith('U2FsdGVkX1')) {
                 text = `[Encrypted payload - use --decrypt to view]`;
            } else if (typeof text === 'string' && text.startsWith('{"')) {
                 try {
                     let j = JSON.parse(text);
                     if (j && j.iv && j.ciphertext) { text = `[Encrypted AES payload - use --decrypt to view]`; }
                 } catch(err) {}
            }
        } catch (e) {
            text = msg.message; 
        }

        const timestamp = msg.log_time || msg.time || Date.now();
        const date = new Date(timestamp).toLocaleString();
        const sender = msg.senderID || 'Unknown';
        
        console.log(`\n🔔 [New Message]`);
        console.log(`From: ${sender}`);
        console.log(`Date: ${date}`);
        console.log(`Message: ${text}`);
    };

    if (options.watch) {
        let firstLoad = true;
        
        requestOptions.callback = (data, error) => {
            if (error) {
                console.error(`\n[Watch Error] ${error}`);
                return;
            }
            if (data) {
                let msgsArray = Object.values(data).filter(m => m && m.message);
                msgsArray.sort((a, b) => (a.log_time || a.time || 0) - (b.log_time || b.time || 0));

                if (firstLoad) {
                    console.log(`\n[watch] Initial stream connected. Found ${msgsArray.length} existing messages.`);
                    firstLoad = false;
                } else {
                    for (const msg of msgsArray) {
                        printMessage(msg);
                    }
                }
            }
        };

        await floCloudAPI.requestApplicationData('MESSAGE', requestOptions);
        console.log(`[watch] Node is now listening in the background (Press Ctrl+C to stop)...`);
        
    } else {
        const messagesResponse = await floCloudAPI.requestApplicationData('MESSAGE', requestOptions);
        
        let msgsArray = [];
        if (typeof messagesResponse === 'object' && messagesResponse !== null) {
            if (Array.isArray(messagesResponse)) {
                msgsArray = messagesResponse;
            } else if (messagesResponse[Object.keys(messagesResponse)[0]]?.message) {
                 msgsArray = Object.values(messagesResponse);
            } else {
                 msgsArray = Object.values(messagesResponse).filter(m => m && m.message);
            }
        }
        
        // Sort array descending by log_time / time
        msgsArray.sort((a, b) => {
            let tA = a.log_time || a.time || 0;
            let tB = b.log_time || b.time || 0;
            return tB - tA; // Newest first
        });
        
        if (options.limit && options.limit > 0) {
            msgsArray = msgsArray.slice(0, options.limit);
        }

        msgsArray.reverse();

        console.log(`\n--- Messages (${msgsArray.length} found) ---`);

        for (const msg of msgsArray) {
            printMessage(msg);
        }
        
        console.log('\n---------------------------\n');
    }
}

// ── 6. Main ──

async function main() {
    try {
        await initCloud();

        const args = parseArgs();

        if (!args.key) {
            throw new Error('FLO_PRIVATE_KEY environment variable is missing. It must be set for secure execution.');
        }

        await receiveMessages(args.key, { sender: args.sender, limit: args.limit, decrypt: args.decrypt, watch: args.watch });

    } catch (error) {
        console.error('[error]', error);
        process.exitCode = 1;
    }

    // Explicitly unref or only exit if not watching
    if (!process.argv.includes('--watch')) {
        setTimeout(() => process.exit(process.exitCode || 0), 100);
    }
}

main();
