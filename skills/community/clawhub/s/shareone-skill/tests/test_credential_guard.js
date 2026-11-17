#!/usr/bin/env node

/**
 * Tests for credential overwrite protection.
 *
 * Tests that saveLocalApiKey refuses to overwrite a different existing key
 * unless force: true is passed, and that create_guest_key.js --no-save works.
 *
 * Run:
 *   node tests/test_credential_guard.js
 */

const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const CRED_PATH = path.join(__dirname, '..', '.shareone_credentials');
const CREATE_GUEST = path.join(__dirname, '..', 'scripts', 'create_guest_key.js');

let passed = 0;
let failed = 0;
let skipped = 0;
const savedCred = fs.existsSync(CRED_PATH) ? fs.readFileSync(CRED_PATH, 'utf8') : null;

function cleanup() {
    // Restore original credentials or remove test file
    if (savedCred !== null) {
        fs.writeFileSync(CRED_PATH, savedCred, { mode: 0o600 });
    } else if (fs.existsSync(CRED_PATH)) {
        fs.unlinkSync(CRED_PATH);
    }
}

function test(name, fn) {
    try {
        fn();
        passed++;
        console.log(`  ✓ ${name}`);
    } catch (error) {
        failed++;
        console.log(`  ✗ ${name}`);
        console.log(`    ${error.message}`);
    }
}

function skip(name, reason) {
    skipped++;
    console.log(`  - ${name} (skipped: ${reason})`);
}

function assert(condition, message) {
    if (!condition) throw new Error(`Assertion failed: ${message}`);
}

// --- Unit tests for saveLocalApiKey guard ---

console.log('\n== saveLocalApiKey overwrite guard ==');

const { saveLocalApiKey, readLocalApiKey } = require(path.join(__dirname, '..', 'scripts', 'shareone_client'));

test('saves key when no existing key', () => {
    if (fs.existsSync(CRED_PATH)) fs.unlinkSync(CRED_PATH);
    saveLocalApiKey('test-key-A');
    const saved = readLocalApiKey();
    assert(saved === 'test-key-A', `expected test-key-A, got ${saved}`);
});

test('saves same key again without error', () => {
    saveLocalApiKey('test-key-A');
    const saved = readLocalApiKey();
    assert(saved === 'test-key-A', `expected test-key-A, got ${saved}`);
});

test('rejects different key without force', () => {
    let threw = false;
    let errorCode = null;
    try {
        saveLocalApiKey('test-key-B');
    } catch (e) {
        threw = true;
        errorCode = e.code;
    }
    assert(threw, 'should have thrown');
    assert(errorCode === 'EXISTING_KEY_CONFLICT', `expected EXISTING_KEY_CONFLICT, got ${errorCode}`);
    // Original key should be preserved
    const saved = readLocalApiKey();
    assert(saved === 'test-key-A', `expected original key test-key-A preserved, got ${saved}`);
});

test('allows different key with force: true', () => {
    saveLocalApiKey('test-key-B', { force: true });
    const saved = readLocalApiKey();
    assert(saved === 'test-key-B', `expected test-key-B, got ${saved}`);
});

test('error includes existingKeyHint', () => {
    // Reset to a known key
    saveLocalApiKey('sk-abcdefghijklmnop', { force: true });
    let hint = null;
    try {
        saveLocalApiKey('sk-different-key-xyz');
    } catch (e) {
        hint = e.existingKeyHint;
    }
    assert(hint !== null, 'should have thrown with hint');
    assert(hint.includes('sk-a'), `hint should start with first 4 chars, got ${hint}`);
    assert(hint.includes('mnop'), `hint should end with last 4 chars, got ${hint}`);
});

// --- create_guest_key.js --no-save test ---

console.log('\n== create_guest_key.js --no-save ==');

test('--no-save creates key but does not save to local credentials', () => {
    // Set a known key
    saveLocalApiKey('owner-key-do-not-overwrite', { force: true });

    let output;
    try {
        output = execFileSync('node', [CREATE_GUEST, '--no-save'], {
            encoding: 'utf8',
            timeout: 15000,
        });
    } catch (error) {
        const out = (error.stdout || '') + (error.stderr || '');
        if (out.includes('RATE_LIMIT')) {
            skip('--no-save preserves existing key', 'rate limited');
            return;
        }
        throw new Error(`create_guest_key --no-save failed: ${out}`);
    }

    assert(output.includes('GUEST_KEY_CREATED:'), `expected GUEST_KEY_CREATED token, got: ${output}`);
    assert(output.includes('NOTE:NOT_SAVED'), `expected NOTE:NOT_SAVED, got: ${output}`);

    // Verify original key is preserved
    const saved = readLocalApiKey();
    assert(saved === 'owner-key-do-not-overwrite', `expected original key preserved, got ${saved}`);
});

// --- create_guest_key.js without --no-save (conflict guard) ---

console.log('\n== create_guest_key.js conflict guard ==');

test('without --no-save, existing key is preserved and NOTE:EXISTING_KEY_KEPT emitted', () => {
    // Set a known key
    saveLocalApiKey('owner-key-precious', { force: true });

    let output;
    try {
        output = execFileSync('node', [CREATE_GUEST], {
            encoding: 'utf8',
            timeout: 15000,
        });
    } catch (error) {
        const out = (error.stdout || '') + (error.stderr || '');
        if (out.includes('RATE_LIMIT')) {
            skip('conflict guard test', 'rate limited');
            return;
        }
        throw new Error(`create_guest_key failed: ${out}`);
    }

    assert(output.includes('GUEST_KEY_CREATED:'), `expected GUEST_KEY_CREATED, got: ${output}`);
    assert(output.includes('NOTE:EXISTING_KEY_KEPT'), `expected NOTE:EXISTING_KEY_KEPT, got: ${output}`);

    // Verify original key is preserved
    const saved = readLocalApiKey();
    assert(saved === 'owner-key-precious', `expected original key preserved, got ${saved}`);
});

// --- Cleanup ---

cleanup();

console.log(`\n== Summary: ${passed} passed, ${failed} failed, ${skipped} skipped ==\n`);
process.exit(failed > 0 ? 1 : 0);
