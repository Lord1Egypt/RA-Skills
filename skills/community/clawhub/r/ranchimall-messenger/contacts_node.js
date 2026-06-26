/**
 * Node.js Messenger CLI — Contact Management
 *
 * Stores contacts in contacts.json in the messenger project directory.
 * No FLO cloud connection is required.
 *
 * Usage:
 *   node contacts_node.js --action list
 *   node contacts_node.js --action add    --address <FLO_ID> --name <NAME>
 *   node contacts_node.js --action remove --address <FLO_ID>
 *   node contacts_node.js --action lookup --address <FLO_ID>
 */

'use strict';

const fs   = require('fs');
const path = require('path');

const CONTACTS_FILE = path.join(__dirname, 'contacts.json');

// ── Helpers ──

function loadContacts() {
    try {
        if (fs.existsSync(CONTACTS_FILE))
            return JSON.parse(fs.readFileSync(CONTACTS_FILE, 'utf8'));
    } catch (e) {
        console.error('[error] Could not read contacts.json:', e.message);
    }
    return {};
}

function saveContacts(contacts) {
    fs.writeFileSync(CONTACTS_FILE, JSON.stringify(contacts, null, 2), 'utf8');
}

function parseArgs() {
    const args   = process.argv.slice(2);
    const parsed = {};
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--action':  parsed.action  = args[++i]; break;
            case '--address': parsed.address = args[++i]; break;
            case '--name':    parsed.name    = args[++i]; break;
        }
    }
    return parsed;
}

// ── Main ──

function main() {
    const args     = parseArgs();
    const contacts = loadContacts();

    switch (args.action) {
        case 'list': {
            const entries = Object.entries(contacts);
            if (entries.length === 0) {
                console.log('\nNo contacts saved. Use --action add to add one.\n');
            } else {
                console.log(`\n--- Contacts (${entries.length}) ---`);
                entries
                    .sort((a, b) => a[1].localeCompare(b[1]))
                    .forEach(([address, name]) => {
                        console.log(`  ${name.padEnd(28)} ${address}`);
                    });
                console.log('----------------------------------------------\n');
            }
            break;
        }

        case 'add': {
            if (!args.address || !args.name) {
                console.error('[error] --address and --name are required.');
                process.exitCode = 1;
                break;
            }
            const existed = args.address in contacts;
            contacts[args.address] = args.name;
            saveContacts(contacts);
            console.log(`[contacts] ${existed ? 'Updated' : 'Added'}: "${args.name}" → ${args.address}`);
            break;
        }

        case 'remove': {
            if (!args.address) {
                console.error('[error] --address is required.');
                process.exitCode = 1;
                break;
            }
            if (!(args.address in contacts)) {
                console.log(`[contacts] Not found: ${args.address}`);
            } else {
                const name = contacts[args.address];
                delete contacts[args.address];
                saveContacts(contacts);
                console.log(`[contacts] Removed: "${name}" (${args.address})`);
            }
            break;
        }

        case 'lookup': {
            if (!args.address) {
                console.error('[error] --address is required.');
                process.exitCode = 1;
                break;
            }
            if (contacts[args.address]) {
                console.log(`\n  ${args.address}  →  ${contacts[args.address]}\n`);
            } else {
                console.log(`[contacts] No contact found for: ${args.address}`);
            }
            break;
        }

        default:
            console.log(`
Messenger Contact Manager

Usage: node contacts_node.js --action <action> [options]

Actions:
  list                                    List all saved contacts
  add  --address <FLO_ID> --name <NAME>   Add or update a contact
  remove --address <FLO_ID>               Remove a contact
  lookup --address <FLO_ID>               Look up a contact by address

Contacts are stored locally in: contacts.json
`);
    }
}

main();
