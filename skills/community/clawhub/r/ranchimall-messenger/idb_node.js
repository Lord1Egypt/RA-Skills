/**
 * Node.js Messenger CLI — Local Key-Value Storage (IDB-compatible)
 *
 * Because IndexedDB is a browser API unavailable in Node.js, this script provides
 * the same logical operations (read, write, remove, list, clear) backed by a local
 * JSON file — mirroring the compactIDB interface used in the browser.
 *
 * Usage:
 *   node idb_node.js --action list   --db <DB> --store <STORE>
 *   node idb_node.js --action read   --db <DB> --store <STORE> --key <KEY>
 *   node idb_node.js --action write  --db <DB> --store <STORE> --key <KEY> --value <JSON>
 *   node idb_node.js --action remove --db <DB> --store <STORE> --key <KEY>
 *   node idb_node.js --action clear  --db <DB> --store <STORE>
 *   node idb_node.js --action dbs                              (list all local databases)
 *   node idb_node.js --action stores --db <DB>                (list stores in a database)
 *   node idb_node.js --action delete-db --db <DB>             (delete an entire database file)
 *
 * Storage: Each <db> maps to a JSON file at  ./idb_data/<db>.json
 *          Structure: { "<store>": { "<key>": <value>, ... }, ... }
 *
 * Note: No FLO_PRIVATE_KEY required. No network activity.
 */

'use strict';

const fs   = require('fs');
const path = require('path');

// ── Storage backend ──

const DATA_DIR = path.join(__dirname, 'idb_data');

function dbFile(db) {
    return path.join(DATA_DIR, `${db}.json`);
}

function ensureDataDir() {
    if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
}

function loadDB(db) {
    const file = dbFile(db);
    if (!fs.existsSync(file)) return {};
    try { return JSON.parse(fs.readFileSync(file, 'utf8')); }
    catch (e) { throw new Error(`Corrupted database file: ${file}`); }
}

function saveDB(db, data) {
    ensureDataDir();
    fs.writeFileSync(dbFile(db), JSON.stringify(data, null, 2), 'utf8');
}

function getStore(data, store) {
    if (!(store in data)) throw new Error(`Store '${store}' not found in database. Did you initialise it?`);
    return data[store];
}

// ── Actions ──

/**
 * List all keys (and values) in a store.
 */
function listStore(db, store) {
    if (!db)    throw new Error('--db is required.');
    if (!store) throw new Error('--store is required.');
    const data = loadDB(db);
    const storeData = getStore(data, store);
    const keys = Object.keys(storeData);

    console.log(`\n${'='.repeat(65)}`);
    console.log(`  DB: ${db}  /  STORE: ${store}  (${keys.length} record${keys.length !== 1 ? 's' : ''})`);
    console.log('='.repeat(65));

    if (keys.length === 0) {
        console.log('  (empty)\n');
        return;
    }
    for (const key of keys) {
        const val = storeData[key];
        const display = typeof val === 'object' ? JSON.stringify(val) : String(val);
        console.log(`  ${key.padEnd(30)}  ${display.length > 80 ? display.slice(0, 80) + '...' : display}`);
    }
    console.log();
}

/**
 * Read a single record by key.
 */
function readRecord(db, store, key) {
    if (!db)    throw new Error('--db is required.');
    if (!store) throw new Error('--store is required.');
    if (!key)   throw new Error('--key is required.');
    const data = loadDB(db);
    const storeData = getStore(data, store);

    if (!(key in storeData)) {
        console.log(`\n  [idb] Key '${key}' not found in ${db}/${store}\n`);
        return;
    }
    const val = storeData[key];
    console.log(`\n  Key   : ${key}`);
    console.log(`  Value : ${typeof val === 'object' ? JSON.stringify(val, null, 2) : val}\n`);
}

/**
 * Add (insert) a record.
 */
function addRecord(db, store, key, valueStr) {
    if (!db)       throw new Error('--db is required.');
    if (!store)    throw new Error('--store is required.');
    if (valueStr === undefined || valueStr === null) throw new Error('--value is required.');

    let value;
    try { value = JSON.parse(valueStr); } catch { value = valueStr; }

    const data = loadDB(db);
    if (!(store in data)) data[store] = {};
    
    // Auto-generate key if not provided
    if (!key) key = Date.now().toString();

    if (data[store][key] !== undefined) {
        throw new Error(`Key '${key}' already exists in store '${store}'. Use 'write' to overwrite.`);
    }

    data[store][key] = value;
    saveDB(db, data);
    console.log(`\n  [idb] Added to [${db} > ${store} > ${key}]\n`);
}

/**
 * Write (upsert) a record.
 */
function writeRecord(db, store, key, valueStr) {
    if (!db)       throw new Error('--db is required.');
    if (!store)    throw new Error('--store is required.');
    if (!key)      throw new Error('--key is required.');
    if (valueStr === undefined || valueStr === null) throw new Error('--value is required.');

    // Try to parse JSON; fall back to raw string
    let value;
    try { value = JSON.parse(valueStr); } catch { value = valueStr; }

    const data = loadDB(db);
    if (!(store in data)) data[store] = {};
    data[store][key] = value;
    saveDB(db, data);
    console.log(`\n  [idb] Written: ${db}/${store}/${key}\n`);
}

/**
 * Remove a record by key.
 */
function removeRecord(db, store, key) {
    if (!db)    throw new Error('--db is required.');
    if (!store) throw new Error('--store is required.');
    if (!key)   throw new Error('--key is required.');
    const data = loadDB(db);
    const storeData = getStore(data, store);
    if (!(key in storeData)) {
        console.log(`\n  [idb] Key '${key}' not found — nothing removed.\n`);
        return;
    }
    delete storeData[key];
    saveDB(db, data);
    console.log(`\n  [idb] Removed: ${db}/${store}/${key}\n`);
}

/**
 * Clear all records in a store.
 */
function clearStore(db, store) {
    if (!db)    throw new Error('--db is required.');
    if (!store) throw new Error('--store is required.');
    const data = loadDB(db);
    getStore(data, store); // validate store exists
    const count = Object.keys(data[store]).length;
    data[store] = {};
    saveDB(db, data);
    console.log(`\n  [idb] Cleared ${count} record${count !== 1 ? 's' : ''} from ${db}/${store}\n`);
}

/**
 * List all local database files.
 */
function listDatabases() {
    ensureDataDir();
    const files = fs.readdirSync(DATA_DIR).filter(f => f.endsWith('.json'));
    console.log(`\n${'='.repeat(65)}`);
    console.log(`  LOCAL DATABASES  (${files.length})`);
    console.log('='.repeat(65));
    if (files.length === 0) {
        console.log('  (none yet)\n');
        return;
    }
    for (const f of files) {
        const db = f.replace('.json', '');
        let stores = [];
        try {
            const data = JSON.parse(fs.readFileSync(path.join(DATA_DIR, f), 'utf8'));
            stores = Object.keys(data);
        } catch {}
        console.log(`  ${db.padEnd(30)}  stores: [${stores.join(', ')}]`);
    }
    console.log();
}

/**
 * List stores in a database.
 */
function listStores(db) {
    if (!db) throw new Error('--db is required.');
    const data = loadDB(db);
    const stores = Object.keys(data);
    console.log(`\n  DB: ${db}`);
    console.log(`  Stores (${stores.length}): ${stores.length ? stores.join(', ') : '(none)'}\n`);
}

/**
 * Delete an entire database file.
 */
function deleteDatabase(db) {
    if (!db) throw new Error('--db is required.');
    const file = dbFile(db);
    if (!fs.existsSync(file)) {
        console.log(`\n  [idb] Database '${db}' does not exist.\n`);
        return;
    }
    fs.unlinkSync(file);
    console.log(`\n  [idb] Deleted database: ${db}\n`);
}

/**
 * Initialise a database with one or more stores (creates the file/stores if missing).
 */
function initDatabase(db, storesStr) {
    if (!db)       throw new Error('--db is required.');
    if (!storesStr) throw new Error('--stores "store1,store2,..." is required.');
    const storeNames = storesStr.split(',').map(s => s.trim()).filter(Boolean);
    const data = loadDB(db);
    let added = 0;
    for (const s of storeNames) {
        if (!(s in data)) { data[s] = {}; added++; }
    }
    saveDB(db, data);
    console.log(`\n  [idb] Database '${db}' ready. Added ${added} new store${added !== 1 ? 's' : ''}. Stores: [${Object.keys(data).join(', ')}]\n`);
}

// ── Parse CLI arguments ──

function parseArgs() {
    const args = process.argv.slice(2);
    const parsed = {};
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--action': parsed.action = args[++i]; break;
            case '--db':     parsed.db     = args[++i]; break;
            case '--store':  parsed.store  = args[++i]; break;
            case '--stores': parsed.stores = args[++i]; break;
            case '--key':    parsed.key    = args[++i]; break;
            case '--value':  parsed.value  = args[++i]; break;
        }
    }
    return parsed;
}

// ── Main ──

function main() {
    try {
        const args = parseArgs();

        switch (args.action) {
            case 'list':      listStore(args.db, args.store); break;
            case 'read':      readRecord(args.db, args.store, args.key); break;
            case 'add':       addRecord(args.db, args.store, args.key, args.value); break;
            case 'write':     writeRecord(args.db, args.store, args.key, args.value); break;
            case 'remove':    removeRecord(args.db, args.store, args.key); break;
            case 'clear':     clearStore(args.db, args.store); break;
            case 'dbs':       listDatabases(); break;
            case 'stores':    listStores(args.db); break;
            case 'delete-db': deleteDatabase(args.db); break;
            case 'init':      initDatabase(args.db, args.stores); break;

            default:
                console.log(`
Messenger Local Storage (Node.js IDB-compatible)

Usage: node idb_node.js --action <action> [options]

Actions:
  dbs                                        List all local databases
  stores     --db <DB>                       List stores in a database
  init       --db <DB> --stores "s1,s2,..."  Create database / add stores
  list       --db <DB> --store <STORE>       List all records in a store
  read       --db <DB> --store <STORE> --key <KEY>
  add        --db <DB> --store <STORE> --value <JSON|TEXT> [--key <KEY>]
  write      --db <DB> --store <STORE> --key <KEY> --value <JSON|TEXT>
  remove     --db <DB> --store <STORE> --key <KEY>     Delete a record by key
  clear      --db <DB> --store <STORE>       Clear all records in a store
  delete-db  --db <DB>                       Delete an entire database file

Storage:
  Records are persisted to  ./idb_data/<db>.json
  This mirrors the browser compactIDB API used by the FLO DApp platform.

Examples:
  node idb_node.js --action dbs
  node idb_node.js --action init --db myApp --stores "contacts,settings,messages"
  node idb_node.js --action list --db myApp --store contacts
  node idb_node.js --action write --db myApp --store contacts --key "FBhHiN..." --value '"Alice"'
  node idb_node.js --action read  --db myApp --store contacts --key "FBhHiN..."
  node idb_node.js --action remove --db myApp --store contacts --key "FBhHiN..."
  node idb_node.js --action clear --db myApp --store messages
  node idb_node.js --action delete-db --db myApp

Note: No FLO_PRIVATE_KEY required. No network activity.
`);
        }

    } catch (error) {
        console.error('[error]', error.message || error);
        process.exitCode = 1;
    }
}

main();
