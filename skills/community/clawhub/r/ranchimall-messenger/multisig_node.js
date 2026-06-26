/**
 * Node.js Messenger CLI — FLO Multisig Operations
 *
 * Usage:
 *   node multisig_node.js --action generate-address --pubkeys "PUB1,PUB2,PUB3" --required 2
 *   node multisig_node.js --action create-tx --address <MULTISIG_FLO_ID> --redeem-script <HEX> --to <FLO_ID> --amount <FLO> [--memo <TEXT>]
 *   node multisig_node.js --action list-pending
 *   node multisig_node.js --action sign-tx    --pipeline <PIPELINE_ID>
 *   node multisig_node.js --action view-tx    --pipeline <PIPELINE_ID>
 *   node multisig_node.js --action broadcast  --pipeline <PIPELINE_ID>
 *
 * Security: Requires FLO_PRIVATE_KEY environment variable.
 *
 * How it works:
 *   - 'generate-address' derives a FLO multisig address from N public keys, requiring M signatures.
 *     Outputs the address and redeemScript. Optionally records to FLO blockchain floData.
 *   - 'create-tx' builds and signs a multisig FLO transaction from the given address, then
 *     distributes the partially-signed tx_hex to co-signers via an encrypted cloud pipeline.
 *   - 'list-pending' shows all open pipeline conversations with pending multisig transactions.
 *   - 'sign-tx' fetches the latest tx_hex from the pipeline, adds your signature, and
 *     either re-distributes it (not fully signed) or broadcasts it to the FLO network.
 *   - 'view-tx' shows the current status of a pipeline's transaction without signing.
 *   - 'broadcast' manually broadcasts the tx if it appears fully signed.
 *
 * Pipeline cache is stored in multisig_cache.json alongside this script.
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { initCloud, getPrivateKey, setupUser, decryptCloudMessage } = require('./node_shared');

const CACHE_FILE = path.join(__dirname, 'multisig_cache.json');

// ── Cache helpers ──

function loadCache() {
    try {
        if (fs.existsSync(CACHE_FILE))
            return JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));
    } catch (e) {
        console.error('[multisig] Could not read multisig_cache.json:', e.message);
    }
    return { pipelines: {} };
}

function saveCache(cache) {
    fs.writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2), 'utf8');
}

// ── Parse CLI arguments ──

function parseArgs() {
    const args = process.argv.slice(2);
    const parsed = { to: [], amount: [], memo: '' };
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--action': parsed.action = args[++i]; break;
            case '--pubkeys': parsed.pubkeys = args[++i]; break; // comma-separated
            case '--required': parsed.required = parseInt(args[++i], 10); break;
            case '--address': parsed.address = args[++i]; break;
            case '--redeem-script': parsed.redeemScript = args[++i]; break;
            case '--to': {
                const val = args[++i];
                if (val && val.includes(',')) {
                    parsed.to.push(...val.split(',').map(v => v.trim()));
                } else if (val) {
                    parsed.to.push(val);
                }
                break;
            }
            case '--amount': {
                const val = args[++i];
                if (val && val.includes(',')) {
                    parsed.amount.push(...val.split(',').map(v => parseFloat(v.trim())));
                } else if (val) {
                    parsed.amount.push(parseFloat(val));
                }
                break;
            }
            case '--memo': parsed.memo = args[++i]; break;
            case '--pipeline': parsed.pipeline = args[++i]; break;
        }
    }
    return parsed;
}

// ── Simple AES via Crypto (loaded from lib.js) ──

function aesEncrypt(text, key) { return Crypto.AES.encrypt(text, key); }
function aesDecrypt(text, key) { return Crypto.AES.decrypt(text, key); }

// ── Actions ──

/**
 * Generate a FLO multisig address from N public keys, requiring M signatures.
 */
function generateAddress(pubkeys, required) {
    if (!pubkeys || !pubkeys.length)
        throw new Error('--pubkeys is required. Provide comma-separated public keys.');
    if (!required || isNaN(required) || required < 1 || required > pubkeys.length)
        throw new Error(`--required must be between 1 and ${pubkeys.length}.`);

    console.log(`\n[multisig] Generating ${required}-of-${pubkeys.length} multisig address...`);

    const result = floCrypto.getMultisigAddress(pubkeys, required);
    if (!result)
        throw new Error('Failed to generate multisig address. Check that all public keys are valid.');

    console.log('\n' + '='.repeat(65));
    console.log('  FLO MULTISIG ADDRESS GENERATED');
    console.log('='.repeat(65));
    console.log(`\n  Address      : ${result.address}`);
    console.log(`  Redeem Script: ${result.redeemScript}`);
    console.log(`  Required sigs: ${required} of ${pubkeys.length}`);
    console.log('\n  ⚠  Save the Redeem Script — you need it to spend funds from this address.');
    console.log('='.repeat(65) + '\n');

    return result;
}

/**
 * Create a partially-signed multisig FLO transaction and distribute it to co-signers via cloud pipeline.
 */
async function createTransaction(myFloID, privateKey, address, redeemScript, receivers, amounts, memo) {
    if (!address) throw new Error('--address (multisig FLO address) is required.');
    if (!redeemScript) throw new Error('--redeem-script is required.');
    if (!receivers.length) throw new Error('At least one --to recipient is required.');

    // Normalize receivers and amounts to arrays
    const receiverArr = Array.isArray(receivers) ? receivers : [receivers];
    const amountArr = Array.isArray(amounts) ? amounts : [amounts];

    if (!amountArr.length) throw new Error('At least one --amount is required.');
    if (receiverArr.length !== amountArr.length) {
        throw new Error('The number of recipients (--to) and amounts (--amount) must match.');
    }

    let totalAmount = 0;
    for (const amt of amountArr) {
        if (isNaN(amt) || amt <= 0) {
            throw new Error('Each --amount must be a positive number.');
        }
        totalAmount += amt;
    }

    // Validate the multisig address
    const decode = floCrypto.decodeRedeemScript(redeemScript);
    if (!decode)
        throw new Error('Invalid --redeem-script: could not decode.');
    if (decode.address !== address)
        throw new Error(`Redeem script address mismatch. Expected: ${address}, Got: ${decode.address}`);

    const pubkeys = decode.pubkeys;
    const required = decode.required;
    const co_owners = pubkeys.map(p => floCrypto.getFloID(p));

    console.log(`\n[multisig] Creating ${required}-of-${pubkeys.length} multisig transaction...`);
    console.log(`  From   : ${address}`);
    console.log(`  To     : ${receiverArr.join(', ')}`);
    console.log(`  Amount : ${amountArr.join(', ')} FLO (Total: ${totalAmount} FLO)`);
    if (memo) console.log(`  Memo   : ${memo}`);

    // Create the unsigned tx
    const txHex = await floBlockchainAPI.createMultisigTx(redeemScript, receiverArr, amountArr, memo);
    console.log('[multisig] Transaction created.');

    // Sign with our key
    const signedHex = floBlockchainAPI.signTx(txHex, privateKey);
    console.log(`[multisig] Signed by: ${myFloID}`);

    // Check if already fully signed (single signer multisig 1-of-1)
    if (floBlockchainAPI.checkSigned(signedHex)) {
        console.log('[multisig] Transaction is already fully signed! Broadcasting...');
        const txid = await floBlockchainAPI.broadcastTx(signedHex);
        console.log(`\n[multisig] ✓ Broadcast!`);
        console.log(`  TXID     : ${txid}`);
        console.log(`  Explorer : https://blockbook.ranchimall.net/tx/${txid}`);
        return;
    }

    // Need more signatures — create a cloud pipeline
    console.log(`\n[multisig] ${required - 1} more signature(s) required. Distributing to co-signers via cloud pipeline...`);

    // Generate a temporary pipeline ID (random FLO-format address)
    const pipelineID = floCrypto.tmpID;
    const eKey = floCrypto.randString(32, false);

    const cache = loadCache();

    // Send tx to each co-signer (except ourselves)
    const otherOwners = co_owners.filter(o => o !== myFloID);
    const encryptedHex = aesEncrypt(signedHex, eKey);

    let sent = 0, failed = 0;
    for (const owner of otherOwners) {
        try {
            // Send pipeline invitation
            const pipeInfo = JSON.stringify({ id: pipelineID, model: 'flo_multisig', members: co_owners, eKey });
            await floCloudAPI.sendApplicationData(pipeInfo, 'CREATE_PIPELINE', {
                receiverID: owner,
                application: 'messenger'
            });
            // Send the tx_hex via the pipeline
            await floCloudAPI.sendApplicationData(encryptedHex, 'TRANSACTION', {
                receiverID: pipelineID,
                application: 'messenger'
            });
            console.log(`[multisig] ✓ Sent to co-signer: ${owner}`);
            sent++;
        } catch (e) {
            console.log(`[multisig] ✗ Failed to reach: ${owner} — ${e}`);
            failed++;
        }
    }

    // Save to local cache
    cache.pipelines[pipelineID] = {
        pipelineID,
        address,
        redeemScript,
        required,
        co_owners,
        eKey,
        txHex: signedHex,
        status: 'pending',
        createdAt: new Date().toISOString(),
        memo
    };
    saveCache(cache);

    console.log('\n' + '='.repeat(65));
    console.log('  MULTISIG TX CREATED');
    console.log('='.repeat(65));
    console.log(`  Pipeline ID  : ${pipelineID}`);
    console.log(`  Co-signers   : ${sent} notified, ${failed} failed`);
    console.log(`  Required sigs: ${required} of ${co_owners.length}`);
    console.log(`\n  Use the pipeline ID to check status:`);
    console.log(`  node multisig_node.js --action view-tx --pipeline ${pipelineID}`);
    console.log(`  node multisig_node.js --action sign-tx --pipeline ${pipelineID}`);
    console.log('='.repeat(65) + '\n');
}

/**
 * List all pending multisig pipelines (from local cache).
 */
function listPending() {
    const cache = loadCache();
    const pipelines = Object.values(cache.pipelines).filter(p => p.status === 'pending');

    if (pipelines.length === 0) {
        console.log('\n[multisig] No pending multisig transactions in local cache.\n');
        console.log('  Tip: If you received a pipeline invitation from a co-signer,');
        console.log('  use: node multisig_node.js --action sign-tx --pipeline <PIPELINE_ID>\n');
        return;
    }

    console.log('\n' + '='.repeat(65));
    console.log(`  PENDING MULTISIG TRANSACTIONS (${pipelines.length})`);
    console.log('='.repeat(65));

    for (const p of pipelines) {
        const date = new Date(p.createdAt).toLocaleString();
        console.log(`\n  Pipeline : ${p.pipelineID}`);
        console.log(`  Address  : ${p.address}`);
        console.log(`  Required : ${p.required} of ${p.co_owners.length} signatures`);
        console.log(`  Created  : ${date}`);
        if (p.memo) console.log(`  Memo     : ${p.memo}`);
    }

    console.log('\n' + '='.repeat(65) + '\n');
}

/**
 * Fetch pipeline invitations from the cloud and sync them with our local cache.
 */
async function syncRequests(myFloID, privateKey) {
    console.log(`\n[multisig] Syncing multisig requests/pipelines from cloud for: ${myFloID}`);

    const response = await floCloudAPI.requestApplicationData('CREATE_PIPELINE', {
        receiverID: myFloID,
        application: 'messenger'
    });

    if (!response || typeof response !== 'object') {
        console.log('[multisig] No responses or invitations found on the cloud.');
        return;
    }

    const msgs = Object.values(response).filter(m => m && m.message && m.type === 'CREATE_PIPELINE');

    if (msgs.length === 0) {
        console.log('[multisig] No pipeline invitations found on the cloud.\n');
        return;
    }

    const cache = loadCache();
    let imported = 0;

    for (const msg of msgs) {
        let decrypted = decryptCloudMessage(msg.message, privateKey);
        if (!decrypted) continue;

        try {
            const info = JSON.parse(decrypted);
            if (info && info.id && info.eKey && (info.model === 'flo_multisig' || info.model === 'btc_multisig')) {
                const pipelineID = info.id;
                
                // If not already in cache, import it
                if (!cache.pipelines[pipelineID]) {
                    cache.pipelines[pipelineID] = {
                        pipelineID,
                        address: info.address || '?',
                        redeemScript: info.redeemScript || '?',
                        required: info.required || 0,
                        co_owners: info.members || [],
                        eKey: info.eKey,
                        txHex: null,
                        status: 'pending',
                        createdAt: msg.log_time ? new Date(msg.log_time).toISOString() : new Date().toISOString(),
                        memo: `Imported from ${msg.senderID || 'co-signer'} invite`
                    };
                    imported++;
                }
            }
        } catch (e) {
            // failed to parse or import
        }
    }

    if (imported > 0) {
        saveCache(cache);
        console.log(`\n[multisig] Success! Imported ${imported} new pending multisig pipeline(s) to cache.`);
    } else {
        console.log('\n[multisig] No new pipelines found. Local cache is already up-to-date.');
    }

    // List all pending
    listPending();
}

/**
 * View the current transaction status from a pipeline (without signing).
 */
async function viewTransaction(myFloID, pipeline) {
    if (!pipeline) throw new Error('--pipeline is required.');

    const cache = loadCache();
    const cached = cache.pipelines[pipeline];

    console.log(`\n[multisig] Fetching pipeline: ${pipeline}`);

    // Try to fetch from cloud
    let txHex = cached ? cached.txHex : null;
    let eKey = cached ? cached.eKey : null;

    if (eKey) {
        const response = await floCloudAPI.requestApplicationData('TRANSACTION', {
            receiverID: pipeline,
            application: 'messenger'
        });

        if (response && typeof response === 'object') {
            const msgs = Object.values(response).filter(m => m && m.message && m.type === 'TRANSACTION');
            if (msgs.length > 0) {
                // Get the latest TRANSACTION message
                msgs.sort((a, b) => (a.vectorClock || 0) - (b.vectorClock || 0));
                const latest = msgs[msgs.length - 1];
                let rawMsg = latest.message;
                try { rawMsg = floCloudAPI.util.decodeMessage(rawMsg); } catch (e) { }
                try { txHex = aesDecrypt(rawMsg, eKey); } catch (e) { }
            }
        }
    }

    if (!txHex) {
        console.log('[multisig] No transaction found for this pipeline.\n');
        return;
    }

    const isSigned = floBlockchainAPI.checkSigned(txHex);
    const sigStatus = floBlockchainAPI.checkSigned(txHex, false);

    console.log('\n' + '='.repeat(65));
    console.log(`  MULTISIG TX STATUS`);
    console.log('='.repeat(65));
    console.log(`\n  Pipeline : ${pipeline}`);
    console.log(`  Fully Signed: ${isSigned ? '✓ YES — ready to broadcast' : '✗ NO — needs more signatures'}`);
    if (cached) {
        console.log(`  Address  : ${cached.address}`);
        console.log(`  Required : ${cached.required} of ${cached.co_owners.length}`);
    }
    console.log(`\n  TX Hex (latest):`);
    console.log(`  ${txHex.substring(0, 80)}...`);
    console.log('\n  To sign: node multisig_node.js --action sign-tx --pipeline ' + pipeline);
    if (isSigned)
        console.log('  To broadcast: node multisig_node.js --action broadcast --pipeline ' + pipeline);
    console.log('='.repeat(65) + '\n');
}

/**
 * Sign the latest transaction in a pipeline and re-distribute or broadcast.
 */
async function signTransaction(myFloID, privateKey, pipeline) {
    if (!pipeline) throw new Error('--pipeline is required.');

    const cache = loadCache();
    const cached = cache.pipelines[pipeline];

    console.log(`\n[multisig] Fetching transaction from pipeline: ${pipeline}`);

    let txHex = null;
    let eKey = cached ? cached.eKey : null;
    let co_owners = cached ? cached.co_owners : [];

    // Fetch latest tx from cloud
    const response = await floCloudAPI.requestApplicationData('TRANSACTION', {
        receiverID: pipeline,
        application: 'messenger'
    });

    if (response && typeof response === 'object') {
        const msgs = Object.values(response).filter(m => m && m.message && m.type === 'TRANSACTION');
        if (msgs.length > 0) {
            msgs.sort((a, b) => (a.vectorClock || 0) - (b.vectorClock || 0));
            const latest = msgs[msgs.length - 1];
            let rawMsg = latest.message;
            try { rawMsg = floCloudAPI.util.decodeMessage(rawMsg); } catch (e) { }
            if (eKey) {
                try { txHex = aesDecrypt(rawMsg, eKey); } catch (e) { }
            } else {
                txHex = rawMsg;
            }
        }
    }

    if (!txHex) {
        console.log('[multisig] No transaction found for this pipeline.');
        console.log('  If you are a co-signer, ask the initiator for the Pipeline ID and eKey.');
        return;
    }

    console.log('[multisig] Transaction found. Signing...');
    const signedHex = floBlockchainAPI.signTx(txHex, privateKey);
    console.log(`[multisig] Signed by: ${myFloID}`);

    const isSigned = floBlockchainAPI.checkSigned(signedHex);

    if (isSigned) {
        console.log('[multisig] Transaction is FULLY SIGNED! Broadcasting to FLO network...');
        const txid = await floBlockchainAPI.broadcastTx(signedHex);

        // Notify pipeline members of broadcast
        if (eKey && co_owners.length) {
            const encodedTxid = aesEncrypt(txid, eKey);
            await floCloudAPI.sendApplicationData(encodedTxid, 'BROADCAST', {
                receiverID: pipeline,
                application: 'messenger'
            }).catch(e => console.warn('[multisig] Could not notify co-signers of broadcast:', e));
        }

        // Update cache
        if (cached) {
            cached.status = 'broadcast';
            cached.txid = txid;
            saveCache(cache);
        }

        console.log('\n' + '='.repeat(65));
        console.log('  ✓ TRANSACTION BROADCAST!');
        console.log('='.repeat(65));
        console.log(`  TXID     : ${txid}`);
        console.log(`  Explorer : https://blockbook.ranchimall.net/tx/${txid}`);
        console.log('='.repeat(65) + '\n');
    } else {
        // Still needs more signatures — send updated tx back into the pipeline
        console.log('[multisig] More signatures still needed. Re-distributing updated tx_hex...');
        const encryptedHex = eKey ? aesEncrypt(signedHex, eKey) : signedHex;

        await floCloudAPI.sendApplicationData(encryptedHex, 'TRANSACTION', {
            receiverID: pipeline,
            application: 'messenger'
        });

        // Update local cache
        if (cached) {
            cached.txHex = signedHex;
            saveCache(cache);
        }

        console.log(`[multisig] Updated tx_hex sent to pipeline: ${pipeline}`);
        console.log('  Co-signers should run: node multisig_node.js --action sign-tx --pipeline ' + pipeline + '\n');
    }
}

/**
 * Manually broadcast a fully-signed transaction from a pipeline.
 */
async function broadcastTransaction(myFloID, pipeline) {
    if (!pipeline) throw new Error('--pipeline is required.');

    const cache = loadCache();
    const cached = cache.pipelines[pipeline];

    console.log(`\n[multisig] Fetching transaction from pipeline: ${pipeline}`);

    let txHex = null;
    const eKey = cached ? cached.eKey : null;

    const response = await floCloudAPI.requestApplicationData('TRANSACTION', {
        receiverID: pipeline,
        application: 'messenger'
    });

    if (response && typeof response === 'object') {
        const msgs = Object.values(response).filter(m => m && m.message && m.type === 'TRANSACTION');
        if (msgs.length > 0) {
            msgs.sort((a, b) => (a.vectorClock || 0) - (b.vectorClock || 0));
            const latest = msgs[msgs.length - 1];
            let rawMsg = latest.message;
            try { rawMsg = floCloudAPI.util.decodeMessage(rawMsg); } catch (e) { }
            if (eKey) {
                try { txHex = aesDecrypt(rawMsg, eKey); } catch (e) { }
            } else {
                txHex = rawMsg;
            }
        }
    }

    if (!txHex) throw new Error('No transaction found for this pipeline.');

    if (!floBlockchainAPI.checkSigned(txHex))
        throw new Error('Transaction is not fully signed yet. More signatures are needed.');

    console.log('[multisig] Transaction is fully signed. Broadcasting...');
    const txid = await floBlockchainAPI.broadcastTx(txHex);

    if (cached) {
        cached.status = 'broadcast';
        cached.txid = txid;
        saveCache(cache);
    }

    console.log('\n' + '='.repeat(65));
    console.log('  ✓ TRANSACTION BROADCAST!');
    console.log('='.repeat(65));
    console.log(`  TXID     : ${txid}`);
    console.log(`  Explorer : https://blockbook.ranchimall.net/tx/${txid}`);
    console.log('='.repeat(65) + '\n');
}

// ── Main ──

async function main() {
    try {
        const args = parseArgs();

        // 'generate-address' and 'list-pending' don't need cloud or private key
        if (args.action === 'generate-address') {
            const pubkeys = args.pubkeys ? args.pubkeys.split(',').map(p => p.trim()) : [];
            generateAddress(pubkeys, args.required);
            return;
        }

        if (args.action === 'list-pending') {
            listPending();
            return;
        }

        // No action given — show help
        if (!args.action) {
            args.action = '__help__';
        }

        // All other actions need cloud and private key
        const privateKey = getPrivateKey();
        await initCloud();
        const myFloID = setupUser(privateKey);

        switch (args.action) {
            case 'create-tx': {
                const receivers = args.to;
                await createTransaction(myFloID, privateKey, args.address, args.redeemScript, receivers, args.amount, args.memo);
                break;
            }
            case 'sync-requests': {
                await syncRequests(myFloID, privateKey);
                break;
            }
            case 'view-tx': {
                await viewTransaction(myFloID, args.pipeline);
                break;
            }
            case 'sign-tx': {
                await signTransaction(myFloID, privateKey, args.pipeline);
                break;
            }
            case 'broadcast': {
                await broadcastTransaction(myFloID, args.pipeline);
                break;
            }
            default:
                console.log(`
Messenger FLO Multisig (Node.js)

Usage: node multisig_node.js --action <action> [options]

Actions:
  generate-address                     Generate a FLO multisig address
    --pubkeys "PUB1,PUB2,PUB3"         Comma-separated public keys (hex)
    --required <N>                     Number of required signatures (e.g. 2)

  sync-requests                        Fetch pending co-signing invites from cloud to cache

  create-tx                            Create and partially sign a multisig transaction
    --address <MULTISIG_FLO_ID>        The FLO multisig address to spend from
    --redeem-script <HEX>              The redeem script of the multisig address
    --to <FLO_ID>                      Recipient address (repeat for multiple)
    --amount <FLO>                     Amount to send in FLO
    [--memo <TEXT>]                    Optional on-chain memo (public)

  list-pending                         List pending multisig TXs from local cache

  view-tx                              View the current state of a pipeline's TX
    --pipeline <PIPELINE_ID>           Pipeline ID from create-tx

  sign-tx                              Sign and broadcast (or forward) a pending TX
    --pipeline <PIPELINE_ID>           Pipeline ID from create-tx

  broadcast                            Manually broadcast a fully-signed TX
    --pipeline <PIPELINE_ID>           Pipeline ID

Security:
  FLO_PRIVATE_KEY environment variable must be set (except for generate-address and list-pending).

Notes:
  - Multisig transactions require M-of-N co-signers. The 'create-tx' action creates
    the transaction, signs it with your key, and sends it to co-signers via cloud pipeline.
  - Co-signers use 'sign-tx' to add their signatures. Once M signatures are collected,
    the transaction is automatically broadcast to the FLO network.
  - Pipeline state is cached in multisig_cache.json.
  - All on-chain memos are stored publicly on the FLO blockchain.
`);
        }

    } catch (error) {
        console.error('[error]', error.message || error);
        process.exitCode = 1;
    }

    setTimeout(() => process.exit(process.exitCode || 0), 300);
}

main();
