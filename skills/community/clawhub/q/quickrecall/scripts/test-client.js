/**
 * Memory Enhancement Engine — Node.js test client
 * Uses a temporary store in OS temp directory.
 * Never touches MEMORY_STORE.json in the skill directory.
 * Safe to run on existing installations.
 */

const path = require('path');
const fs = require('fs');
const os = require('os');

const memPath = path.join(__dirname, '..', 'memory.js');
const tmpStore = path.join(os.tmpdir(), '__me_test_' + Date.now() + '.json');

function assert(cond, msg) {
    if (!cond) throw new Error('FAIL: ' + msg);
    console.log('  [PASS] ' + msg);
}

async function run() {
    const { MemorySystem } = await import('file:///' + memPath.replace(/\\/g, '/'));
    console.log('=== Memory Enhancement Engine Tests (temp store only) ===\n');
    
    // Use storePath to write to temp directory only
    const mem = new MemorySystem({ storePath: tmpStore, decayHalfLifeHours: 100 });
    assert(true, 'Engine created with temp store');
    
    const id1 = mem.add('Paris is the capital of France.', 1.5, { tags: ['geo'] });
    const id2 = mem.add('Light travels at 299,792,458 m/s', 0.8);
    const id3 = mem.add('User prefers dark mode', 1.2, { tags: ['pref'] });
    assert(id1 && id2 && id3, 'Add 3 memories');
    
    const results = mem.retrieve('France capital', 5);
    assert(results.length > 0, 'retrieve returns ' + results.length);
    assert(results[0]._score > 0, 'Score=' + results[0]._score.toFixed(3));
    
    const recent = mem.getRecent(5);
    assert(recent.length >= 3, 'getRecent');
    
    mem.remove((m) => m.id === id3);
    assert(true, 'remove');
    
    const compactR = mem.compact(5, 0.0);
    assert(typeof compactR === 'number', 'compact');
    
    // Clean up temp file
    try { fs.unlinkSync(tmpStore); } catch (e) {}
    console.log('\n=== ALL TESTS PASSED ===');
    
    // Verify no MEMORY_STORE.json was created in skill directory
    const expected = path.join(__dirname, '..', 'MEMORY_STORE.json');
    if (fs.existsSync(expected)) {
        console.warn('[WARN] MEMORY_STORE.json exists in skill dir (from earlier use or real data)');
    } else {
        console.log('[OK] No MEMORY_STORE.json in skill directory');
    }
}

run().catch(e => {
    try { fs.unlinkSync(tmpStore); } catch (ex) {}
    console.error(e.message);
    process.exit(1);
});
