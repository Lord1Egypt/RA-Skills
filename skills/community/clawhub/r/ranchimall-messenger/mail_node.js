/**
 * Node.js Messenger CLI — Mail Operations
 *
 * Usage:
 *   node mail_node.js --action send --to <FLO_ID> [--to <FLO_ID>] --subject <S> --body <B>
 *   node mail_node.js --action list  [--limit <N>]
 *   node mail_node.js --action read  --ref <MAIL_REF>
 *
 * Security: Requires FLO_PRIVATE_KEY environment variable.
 *
 * Note: Mail is fetched directly from the FLO Cloud — no local cache needed.
 *       Messages are stored on supernodes and fetched on each run.
 */

'use strict';

const crypto = require('crypto');
const { initCloud, getPrivateKey, setupUser, decryptCloudMessage } = require('./node_shared');

// ── Parse CLI arguments ──

function parseArgs() {
    const args   = process.argv.slice(2);
    const parsed = { to: [], limit: 20 };
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--action':  parsed.action  = args[++i]; break;
            case '--to': {
                const val = args[++i];
                if (val && val.includes(',')) {
                    parsed.to.push(...val.split(',').map(v => v.trim()));
                } else if (val) {
                    parsed.to.push(val);
                }
                break;
            }
            case '--subject': parsed.subject = args[++i]; break;
            case '--body':    parsed.body    = args[++i]; break;
            case '--ref':     parsed.ref     = args[++i]; break;
            case '--limit':   parsed.limit   = parseInt(args[++i], 10); break;
        }
    }
    return parsed;
}

// ── Helpers ──

function randString(len = 8) {
    return crypto.randomBytes(len).toString('hex').slice(0, len);
}

function formatMail(mail, index) {
    const date = new Date(mail.time || mail.log_time || Date.now()).toLocaleString();
    const from = mail.senderID || mail.from || 'Unknown';
    let content = mail.message || '';

    // Parse the JSON mail payload
    try {
        const parsed = JSON.parse(content);
        return {
            ref: parsed.ref || mail.vectorClock,
            subject: parsed.subject || '(no subject)',
            body: parsed.content || '(no content)',
            from,
            date
        };
    } catch (e) {
        return {
            ref: mail.vectorClock || '?',
            subject: '(could not parse)',
            body: content,
            from,
            date
        };
    }
}

// ── Actions ──

// Send a mail to one or more recipients
async function sendMail(myFloID, recipients, subject, body) {
    if (recipients.length === 0) {
        throw new Error('At least one --to recipient is required.');
    }
    if (!subject) throw new Error('--subject is required.');
    if (!body)    throw new Error('--body is required.');

    const mail = {
        subject,
        content: body,
        ref: Date.now() + randString(8),
        prev: null
    };

    const mailStr = JSON.stringify(mail);
    console.log(`\n[mail] Sending to ${recipients.length} recipient(s)...`);
    console.log(`[mail] Subject : ${subject}`);

    const promises = recipients.map(r =>
        floCloudAPI.sendApplicationData(mailStr, 'MAIL', {
            receiverID: r,
            application: 'messenger'
        })
    );

    const results = await Promise.allSettled(promises);
    let sent = 0, failed = 0;

    results.forEach((r, i) => {
        if (r.status === 'fulfilled') {
            console.log(`[mail] ✓ Sent to ${recipients[i]}`);
            sent++;
        } else {
            console.log(`[mail] ✗ Failed for ${recipients[i]}: ${r.reason}`);
            failed++;
        }
    });

    console.log(`\n[mail] Done: ${sent} sent, ${failed} failed. Mail ref: ${mail.ref}\n`);
}

// List received mails
async function listMails(myFloID, privateKey, limit) {
    console.log(`\n[mail] Fetching mails for: ${myFloID}`);

    const response = await floCloudAPI.requestApplicationData('MAIL', {
        receiverID: myFloID
    });

    if (!response || typeof response !== 'object') {
        console.log('[mail] No response from cloud.');
        return;
    }

    let mails = Object.values(response).filter(m => m && m.message);

    // Sort newest first
    mails.sort((a, b) => (b.log_time || b.time || 0) - (a.log_time || a.time || 0));
    if (limit > 0) mails = mails.slice(0, limit);
    mails.reverse(); // oldest first for display

    if (mails.length === 0) {
        console.log('[mail] No mails found.\n');
        return;
    }

    console.log(`\n${'='.repeat(60)}`);
    console.log(`  INBOX  (${mails.length} mail${mails.length !== 1 ? 's' : ''})`);
    console.log('='.repeat(60));

    for (const raw of mails) {
        // Decrypt if needed
        let msgText = raw.message;
        const decrypted = decryptCloudMessage(msgText, privateKey);
        if (decrypted) msgText = decrypted;

        let content = msgText;
        let subject = '(no subject)', ref = raw.vectorClock;
        try {
            const parsed = JSON.parse(content);
            subject = parsed.subject || subject;
            ref     = parsed.ref     || ref;
        } catch (e) {}

        const date = new Date(raw.log_time || raw.time || Date.now()).toLocaleString();

        console.log(`\n  From    : ${raw.senderID || 'Unknown'}`);
        console.log(`  Date    : ${date}`);
        console.log(`  Subject : ${subject}`);
        console.log(`  Ref     : ${ref}`);
    }
    console.log(`\n${'='.repeat(60)}\n`);
    console.log('  Tip: Use --action read --ref <REF> to read the full content of a mail.\n');
}

// Read the full content of a specific mail by ref
async function readMail(myFloID, privateKey, ref) {
    console.log(`\n[mail] Fetching mails to search for ref: ${ref}`);

    const response = await floCloudAPI.requestApplicationData('MAIL', {
        receiverID: myFloID
    });

    if (!response || typeof response !== 'object') {
        console.log('[mail] No response from cloud.');
        return;
    }

    const mails = Object.values(response).filter(m => m && m.message);
    let found = null;

    for (const raw of mails) {
        let msgText = raw.message;
        const decrypted = decryptCloudMessage(msgText, privateKey);
        if (decrypted) msgText = decrypted;

        try {
            const parsed = JSON.parse(msgText);
            if (parsed.ref === ref || raw.vectorClock === ref) {
                found = { raw, parsed };
                break;
            }
        } catch (e) {
            if (raw.vectorClock === ref) {
                found = { raw, parsed: { subject: '(parse error)', content: msgText } };
                break;
            }
        }
    }

    if (!found) {
        console.log(`[mail] Mail with ref "${ref}" not found.\n`);
        return;
    }

    const date = new Date(found.raw.log_time || found.raw.time || Date.now()).toLocaleString();

    console.log(`\n${'='.repeat(60)}`);
    console.log(`  From    : ${found.raw.senderID || 'Unknown'}`);
    console.log(`  Date    : ${date}`);
    console.log(`  Subject : ${found.parsed.subject || '(no subject)'}`);
    console.log(`  Ref     : ${found.parsed.ref || found.raw.vectorClock}`);
    console.log('─'.repeat(60));
    console.log(`\n  ${(found.parsed.content || '(empty)').replace(/\n/g, '\n  ')}\n`);
    console.log('='.repeat(60) + '\n');
}

// ── Main ──

async function main() {
    try {
        const args       = parseArgs();
        const privateKey = getPrivateKey();

        await initCloud();
        const myFloID = setupUser(privateKey);

        switch (args.action) {
            case 'send':
                await sendMail(myFloID, args.to, args.subject, args.body);
                break;
            case 'list':
                await listMails(myFloID, privateKey, args.limit);
                break;
            case 'read':
                if (!args.ref) { console.error('[error] --ref is required.'); process.exitCode = 1; break; }
                await readMail(myFloID, privateKey, args.ref);
                break;
            default:
                console.log(`
Messenger Mail (Node.js)

Usage: node mail_node.js --action <action> [options]

Actions:
  send  --to <FLO_ID> [--to <FLO_ID> ...] --subject <S> --body <B>
                                        Send a mail to one or more recipients
  list  [--limit <N>]                   List received mails (default: 20 most recent)
  read  --ref <MAIL_REF>                Read the full content of a specific mail

Prerequisites:
  FLO_PRIVATE_KEY environment variable must be set.
`);
        }

    } catch (error) {
        console.error('[error]', error.message || error);
        process.exitCode = 1;
    }

    setTimeout(() => process.exit(process.exitCode || 0), 100);
}

main();
