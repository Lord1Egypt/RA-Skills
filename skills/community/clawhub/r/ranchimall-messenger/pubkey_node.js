/**
 * Node.js Messenger CLI — Public Key Operations
 *
 * Usage:
 *   node pubkey_node.js --action my-pubkey
 *   node pubkey_node.js --action get     --address <FLO_ID>
 *   node pubkey_node.js --action request --address <FLO_ID> [--message <MSG>]
 *
 * Security: Requires FLO_PRIVATE_KEY environment variable.
 */

'use strict';

const { initCloud, getPrivateKey, setupUser } = require('./node_shared');

// ── Parse CLI arguments ──

function parseArgs() {
    const args   = process.argv.slice(2);
    const parsed = { message: '' };
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--action':  parsed.action  = args[++i]; break;
            case '--address': parsed.address = args[++i]; break;
            case '--message': parsed.message = args[++i]; break;
        }
    }
    return parsed;
}

// ── Actions ──

// Show own public key (derived from private key — no cloud needed)
function showMyPubKey(privateKey) {
    const floID = floCrypto.getFloID(privateKey);
    const pubKey = floCrypto.getPubKeyHex(privateKey);
    console.log(`\n--- My Identity ---`);
    console.log(`FLO ID  : ${floID}`);
    console.log(`Pub Key : ${pubKey}`);
    console.log(`-------------------\n`);
}

// Look up the public key for a FLO address by scanning cloud messages FROM that address
async function getAddressPubKey(targetAddress) {
    console.log(`\n[pubkey] Looking up public key for: ${targetAddress}`);

    const response = await floCloudAPI.requestApplicationData(null, {
        senderID: [targetAddress],
        mostRecent: true
    });

    if (!response || typeof response !== 'object') {
        console.log('[pubkey] No data returned from cloud.');
        return;
    }

    const msgs = Object.values(response);
    if (msgs.length === 0) {
        console.log('[pubkey] No messages found from this address. Public key is unknown.');
        console.log('         Tip: Use --action request to ask them to share their key.');
        return;
    }

    // The pubKey field is included in every message by floCloudAPI
    const pubKey = msgs[0].pubKey || msgs.find(m => m.pubKey)?.pubKey;
    if (pubKey) {
        console.log(`\n  Address : ${targetAddress}`);
        console.log(`  Pub Key : ${pubKey}\n`);
    } else {
        console.log('[pubkey] Messages found but pubKey field was not present in the response.');
    }
}

// Send a PUBLIC_KEY request message to another user
async function requestPubKey(myFloID, targetAddress, message) {
    console.log(`\n[pubkey] Sending PUBLIC_KEY request to: ${targetAddress}`);

    const result = await floCloudAPI.sendApplicationData(
        message || '',
        'REQUEST',
        {
            receiverID: targetAddress,
            comment: 'PUBLIC_KEY',
            application: 'messenger'
        }
    );

    console.log('[pubkey] Request sent successfully!');
    console.log(`         Vector Clock : ${result.vectorClock}`);
    console.log(`         Time         : ${new Date(result.time).toLocaleString()}`);
    console.log('\nThe recipient will see this as a public key request in their messenger.\n');
}

// ── Main ──

async function main() {
    try {
        const args       = parseArgs();
        const privateKey = getPrivateKey();

        // my-pubkey doesn't need cloud
        if (args.action === 'my-pubkey') {
            showMyPubKey(privateKey);
            return;
        }

        // All other actions need cloud
        await initCloud();
        const myFloID = setupUser(privateKey);

        switch (args.action) {
            case 'get': {
                if (!args.address) { console.error('[error] --address is required.'); process.exitCode = 1; break; }
                await getAddressPubKey(args.address);
                break;
            }
            case 'request': {
                if (!args.address) { console.error('[error] --address is required.'); process.exitCode = 1; break; }
                await requestPubKey(myFloID, args.address, args.message);
                break;
            }
            default:
                console.log(`
Messenger Public Key Manager

Usage: node pubkey_node.js --action <action> [options]

Actions:
  my-pubkey                             Show your own FLO ID and public key
  get     --address <FLO_ID>            Look up the public key of any FLO address
  request --address <FLO_ID>            Send a public key request to another user
          [--message <MSG>]             Optional note to include with the request

Prerequisites:
  FLO_PRIVATE_KEY environment variable must be set (not needed for my-pubkey).
`);
        }

    } catch (error) {
        console.error('[error]', error.message || error);
        process.exitCode = 1;
    }

    setTimeout(() => process.exit(process.exitCode || 0), 100);
}

main();
