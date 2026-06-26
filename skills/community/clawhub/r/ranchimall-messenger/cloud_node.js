/**
 * Node.js Messenger CLI — Cloud API Operations
 *
 * Usage:
 *   node cloud_node.js --action <action> [options]
 *
 * Security: Requires FLO_PRIVATE_KEY environment variable for sending data.
 */

'use strict';

const { initCloud, getPrivateKey, setupUser } = require('./node_shared');

// ── Parse CLI arguments ──
function parseArgs() {
    const args = process.argv.slice(2);
    const parsed = { };
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--action':  parsed.action = args[++i]; break;
            case '--data':    parsed.data   = args[++i]; break;
            case '--type':    parsed.type   = args[++i]; break;
            case '--object':  parsed.object = args[++i]; break;
            case '--receiver':parsed.receiver = args[++i]; break;
            case '--sender':  parsed.sender = args[++i]; break;
            case '--comment': parsed.comment= args[++i]; break;
        }
    }
    return parsed;
}

// ── Actions ──

async function sendGeneral(data, type, comment) {
    if (!data) throw new Error('--data is required.');
    console.log(`\n[cloud] Sending General Data...`);
    const result = await floCloudAPI.sendGeneralData(data, type || 'RAW', { comment });
    console.log(`\n  ✓ Success\n  Vector Clock : ${result.vectorClock}\n`);
}

async function requestGeneral(type, sender) {
    console.log(`\n[cloud] Requesting General Data...`);
    const result = await floCloudAPI.requestGeneralData(type || null, { senderID: sender });
    console.log(`\n  Data:\n`, JSON.stringify(result, null, 2), '\n');
}

async function sendApp(data, type, receiver, comment) {
    if (!data) throw new Error('--data is required.');
    console.log(`\n[cloud] Sending Application Data...`);
    const result = await floCloudAPI.sendApplicationData(data, type || 'RAW', { receiverID: receiver, comment });
    console.log(`\n  ✓ Success\n  Vector Clock : ${result.vectorClock}\n`);
}

async function requestApp(type, sender, receiver) {
    console.log(`\n[cloud] Requesting Application Data...`);
    const result = await floCloudAPI.requestApplicationData(type || null, { senderID: sender, receiverID: receiver });
    console.log(`\n  Data:\n`, JSON.stringify(result, null, 2), '\n');
}

async function requestObject(objectName) {
    if (!objectName) throw new Error('--object is required.');
    console.log(`\n[cloud] Requesting Object: ${objectName}...`);
    const result = await floCloudAPI.requestObjectData(objectName);
    console.log(`\n  Object Data:\n`, JSON.stringify(result, null, 2), '\n');
}

async function updateObject(objectName, data, comment) {
    if (!objectName || !data) throw new Error('--object and --data are required.');
    let parsedData;
    try { parsedData = JSON.parse(data); } catch (e) { parsedData = data; } // Send raw if not JSON
    console.log(`\n[cloud] Updating Object: ${objectName}...`);
    const result = await floCloudAPI.updateObjectData(objectName, parsedData, { comment });
    console.log(`\n  ✓ Success\n  Vector Clock : ${result.vectorClock}\n`);
}

async function resetObject(objectName, data, comment) {
    if (!objectName || !data) throw new Error('--object and --data are required.');
    let parsedData;
    try { parsedData = JSON.parse(data); } catch (e) { parsedData = data; }
    console.log(`\n[cloud] Resetting Object: ${objectName}...`);
    const result = await floCloudAPI.resetObjectData(objectName, parsedData, { comment });
    console.log(`\n  ✓ Success\n  Vector Clock : ${result.vectorClock}\n`);
}

// ── Main ──

async function main() {
    try {
        const args = parseArgs();
        
        // request-general doesn't strictly need a private key if it isn't sending, but initCloud might need setup
        // Actually, we'll try to get private key, but allow read-only if it fails for requests.
        let privateKey;
        try { privateKey = getPrivateKey(); } catch (e) {}

        if (!privateKey && ['send-general', 'send-app', 'update-object', 'reset-object'].includes(args.action)) {
            throw new Error(`FLO_PRIVATE_KEY is required for ${args.action}`);
        }

        await initCloud();
        if (privateKey) setupUser(privateKey);

        switch (args.action) {
            case 'send-general':    await sendGeneral(args.data, args.type, args.comment); break;
            case 'request-general': await requestGeneral(args.type, args.sender); break;
            case 'send-app':        await sendApp(args.data, args.type, args.receiver, args.comment); break;
            case 'request-app':     await requestApp(args.type, args.sender, args.receiver); break;
            case 'request-object':  await requestObject(args.object); break;
            case 'update-object':   await updateObject(args.object, args.data, args.comment); break;
            case 'reset-object':    await resetObject(args.object, args.data, args.comment); break;
            default:
                console.log(`
Messenger Cloud API Node Operations

Usage: node cloud_node.js --action <action> [options]

Actions:
  send-general       --data <TEXT> [--type <TYPE>] [--comment <TEXT>]
  request-general    [--type <TYPE>] [--sender <FLO_ID>]
  send-app           --data <TEXT> [--type <TYPE>] [--receiver <FLO_ID>] [--comment <TEXT>]
  request-app        [--type <TYPE>] [--sender <FLO_ID>] [--receiver <FLO_ID>]
  request-object     --object <NAME>
  update-object      --object <NAME> --data <JSON> [--comment <TEXT>]
  reset-object       --object <NAME> --data <JSON> [--comment <TEXT>]
`);
        }

    } catch (error) {
        console.error('[error]', error.message || error);
        process.exitCode = 1;
    }

    setTimeout(() => process.exit(process.exitCode || 0), 300);
}

main();
