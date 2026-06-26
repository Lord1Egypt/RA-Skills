/**
 * Node.js Messenger CLI — Group Operations
 *
 * Usage:
 *   node groups_node.js --action fetch                           Sync group memberships from cloud
 *   node groups_node.js --action list                            List cached groups
 *   node groups_node.js --action send  --group <ID> --message <MSG>   Send a message to a group
 *   node groups_node.js --action read  --group <ID> [--limit <N>]     Read group messages
 *
 * How it works:
 *  - 'fetch' pulls CREATE_GROUP messages addressed to you from the cloud,
 *    decrypts the group info (including the AES eKey), and saves to groups_cache.json
 *  - 'send' encrypts your message with the cached group eKey and sends it to the group ID
 *  - 'read' fetches GROUP_MSG messages from the group ID and decrypts them with the cached eKey
 *
 * Security: Requires FLO_PRIVATE_KEY environment variable.
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { initCloud, getPrivateKey, setupUser, decryptCloudMessage } = require('./node_shared');

const GROUPS_CACHE_FILE = path.join(__dirname, 'groups_cache.json');

// ── Cache helpers ──

function loadGroupsCache() {
    try {
        if (fs.existsSync(GROUPS_CACHE_FILE))
            return JSON.parse(fs.readFileSync(GROUPS_CACHE_FILE, 'utf8'));
    } catch (e) {
        console.error('[groups] Could not read groups_cache.json:', e.message);
    }
    return {};
}

function saveGroupsCache(cache) {
    fs.writeFileSync(GROUPS_CACHE_FILE, JSON.stringify(cache, null, 2), 'utf8');
}

// ── Parse CLI arguments ──

function parseArgs() {
    const args = process.argv.slice(2);
    const parsed = { limit: 30 };
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--action': parsed.action = args[++i]; break;
            case '--group': parsed.group = args[++i]; break;
            case '--message': parsed.message = args[++i]; break;
            case '--limit': parsed.limit = parseInt(args[++i], 10); break;
        }
    }
    return parsed;
}

// ── Actions ──

/**
 * Fetch group invitations (CREATE_GROUP messages) from the cloud.
 * Decrypts the group info payload and saves to groups_cache.json.
 */
async function fetchGroups(myFloID, privateKey) {
    console.log(`\n[groups] Fetching group memberships for: ${myFloID}`);

    const response = await floCloudAPI.requestApplicationData('CREATE_GROUP', {
        receiverID: myFloID
    });

    if (!response || typeof response !== 'object') {
        console.log('[groups] No response from cloud.');
        return;
    }

    const msgs = Object.values(response).filter(m => m && m.message);
    console.log(`[groups] Found ${msgs.length} CREATE_GROUP message(s).`);

    const cache = loadGroupsCache();
    let added = 0, skipped = 0;

    for (const msg of msgs) {
        // The CREATE_GROUP payload is RSA-encrypted for the recipient
        const decrypted = decryptCloudMessage(msg.message, privateKey);
        if (!decrypted) { skipped++; continue; }

        let groupInfo;
        try {
            groupInfo = typeof decrypted === 'string' ? JSON.parse(decrypted) : decrypted;
        } catch (e) {
            console.warn('[groups] Could not parse group info:', e.message);
            skipped++;
            continue;
        }

        if (!groupInfo.groupID) { skipped++; continue; }

        // Verify group signature
        const h = ["groupID", "created", "admin"].map(x => groupInfo[x]).join('|');
        const valid = floCrypto.verifySign(h, groupInfo.hash, groupInfo.pubKey) &&
            floCrypto.getFloID(groupInfo.pubKey) === groupInfo.groupID;

        if (!valid) {
            console.warn(`[groups] Skipping group ${groupInfo.groupID} — signature verification failed.`);
            skipped++;
            continue;
        }

        // Store with the plain eKey (already decrypted from RSA envelope)
        cache[groupInfo.groupID] = {
            groupID: groupInfo.groupID,
            name: groupInfo.name || groupInfo.groupID,
            description: groupInfo.description || '',
            admin: groupInfo.admin,
            members: groupInfo.members || [],
            eKey: groupInfo.eKey,             // plain AES key for group encryption
            created: groupInfo.created,
            fetchedAt: Date.now()
        };

        console.log(`[groups] ✓ Group: "${groupInfo.name}" (${groupInfo.groupID})`);
        added++;
    }

    saveGroupsCache(cache);

    const total = Object.keys(cache).length;
    console.log(`\n[groups] Sync complete: ${added} new group(s). Total cached: ${total}. Skipped: ${skipped}.\n`);
}

/**
 * List all cached groups.
 */
function listGroups() {
    const cache = loadGroupsCache();
    const groups = Object.values(cache);

    if (groups.length === 0) {
        console.log('\nNo groups cached. Run --action fetch first.\n');
        return;
    }

    console.log(`\n${'='.repeat(65)}`);
    console.log(`  GROUPS  (${groups.length})`);
    console.log('='.repeat(65));

    groups.forEach(g => {
        const date = new Date(g.created || 0).toLocaleDateString();
        const sync = new Date(g.fetchedAt || 0).toLocaleString();
        const isAdmin = g.admin === (global._myFloID || '');
        console.log(`\n  Name    : ${g.name}${isAdmin ? ' [ADMIN]' : ''}`);
        console.log(`  ID      : ${g.groupID}`);
        console.log(`  Admin   : ${g.admin}`);
        console.log(`  Members : ${g.members.length}`);
        if (g.description) console.log(`  Desc    : ${g.description}`);
        console.log(`  Created : ${date}   (synced: ${sync})`);
    });

    console.log(`\n${'='.repeat(65)}\n`);
}

/**
 * Send an AES-encrypted message to a group.
 *
 * Data flow (no file contents sent to network):
 *   1. Read  — extract only the group name and eKey from local cache
 *   2. Drop  — cache object is not referenced again after step 1
 *   3. Encrypt — user-supplied message is encrypted using the eKey
 *   4. Send  — ONLY the encrypted user message is transmitted; no cache data leaves the host
 */
async function sendGroupMessage(groupID, message) {
    // ── Phase 1: Read local cache, extract only what is needed ──
    const cache = loadGroupsCache();
    const groupName = cache[groupID] && cache[groupID].name;
    const eKey = cache[groupID] && cache[groupID].eKey;
    // cache is no longer referenced after this point

    // ── Phase 2: Validate (no network calls yet) ──
    if (!cache[groupID]) {
        throw new Error(`Group "${groupID}" not found in cache. Run --action fetch first.`);
    }
    if (!eKey) {
        throw new Error(`Group "${groupID}" has no encryption key cached. Re-run --action fetch.`);
    }
    if (!message) {
        throw new Error('--message is required.');
    }

    console.log(`\n[groups] Sending to group: ${groupName} (${groupID})`);
    console.log(`[groups] Message: ${message}`);

    // ── Phase 3: Encrypt the user-supplied message using the group eKey ──
    // Only `message` (typed by the user) is encrypted. The eKey itself is never sent.
    const encryptedMessage = Crypto.AES.encrypt(message, eKey);

    // ── Phase 4: Transmit — only the encrypted user message goes to the network ──
    const result = await floCloudAPI.sendApplicationData(encryptedMessage, 'GROUP_MSG', {
        receiverID: groupID,
        application: 'messenger'
    });

    console.log(`[groups] ✓ Message sent! Vector Clock: ${result.vectorClock}`);
    console.log(`         Time: ${new Date(result.time).toLocaleString()}\n`);
}

/**
 * Read and decrypt messages from a group.
 */
async function readGroupMessages(groupID, limit) {
    const cache = loadGroupsCache();
    const group = cache[groupID];
    if (!group) {
        throw new Error(`Group "${groupID}" not found in cache. Run --action fetch first.`);
    }
    if (!group.eKey) {
        throw new Error(`Group "${groupID}" has no encryption key cached.`);
    }

    console.log(`\n[groups] Fetching messages for group: ${group.name} (${groupID})`);

    const response = await floCloudAPI.requestApplicationData(null, {
        receiverID: groupID
    });

    if (!response || typeof response !== 'object') {
        console.log('[groups] No messages found.');
        return;
    }

    let msgs = Object.values(response).filter(m => m && m.message && m.type === 'GROUP_MSG');
    msgs.sort((a, b) => (a.log_time || a.time || 0) - (b.log_time || b.time || 0));
    if (limit > 0) msgs = msgs.slice(-limit);

    if (msgs.length === 0) {
        console.log('[groups] No GROUP_MSG messages found.\n');
        return;
    }

    console.log(`\n${'='.repeat(65)}`);
    console.log(`  ${group.name.toUpperCase()}  (${msgs.length} message${msgs.length !== 1 ? 's' : ''})`);
    console.log('='.repeat(65));

    for (const msg of msgs) {
        const date = new Date(msg.log_time || msg.time || Date.now()).toLocaleString();
        const sender = msg.senderID || 'Unknown';

        // Decrypt with group eKey
        let text = msg.message;
        try {
            text = Crypto.AES.decrypt(msg.message, group.eKey);
            if (!text) text = '[decryption failed]';
        } catch (e) {
            text = '[decryption error: ' + e.message + ']';
        }

        console.log(`\n   ${sender}`);
        console.log(`   ${date}`);
        console.log(`   ${text}`);
    }

    console.log(`\n${'='.repeat(65)}\n`);
}

// ── Main ──

async function main() {
    try {
        const args = parseArgs();
        const privateKey = getPrivateKey();

        if (args.action === 'list') {
            // list doesn't need cloud
            listGroups();
            return;
        }

        await initCloud();
        const myFloID = setupUser(privateKey);
        global._myFloID = myFloID;  // used for admin badge in list

        switch (args.action) {
            case 'fetch':
                await fetchGroups(myFloID, privateKey);
                break;
            case 'send':
                if (!args.group) { console.error('[error] --group is required.'); process.exitCode = 1; break; }
                if (!args.message) { console.error('[error] --message is required.'); process.exitCode = 1; break; }
                await sendGroupMessage(args.group, args.message);
                break;
            case 'read':
                if (!args.group) { console.error('[error] --group is required.'); process.exitCode = 1; break; }
                await readGroupMessages(args.group, args.limit);
                break;
            default:
                console.log(`
Messenger Group Manager (Node.js)

Usage: node groups_node.js --action <action> [options]

Actions:
  fetch                                 Sync group memberships from FLO cloud → groups_cache.json
  list                                  List all cached groups (run fetch first)
  send  --group <GROUP_ID>              Send an encrypted message to a group
        --message <MSG>
  read  --group <GROUP_ID>              Read messages from a group (decrypted)
        [--limit <N>]                   (default: 30 most recent)

Group IDs can be found with --action list.

Prerequisites:
  FLO_PRIVATE_KEY environment variable must be set.
  Run --action fetch at least once to populate the local groups cache.
`);
        }

    } catch (error) {
        console.error('[error]', error.message || error);
        process.exitCode = 1;
    }

    setTimeout(() => process.exit(process.exitCode || 0), 100);
}

main();
