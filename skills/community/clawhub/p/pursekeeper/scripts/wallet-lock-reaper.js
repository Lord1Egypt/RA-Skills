'use strict';
const fs = require('node:fs');

// Same-host, cooperative wallet clients only. The old compare/unlink sequence
// was not atomic: waiter C could validate dead holder H, waiter B could remove
// H and publish B's *live* record, and C could then delete B's new record.
// Serialise the WHOLE stale-holder recheck + unlink with an O_EXCL local file.
//
// The gate is deliberately never stolen using time, PID or mtime. A waiter
// cannot know whether a slow/paused reaper is alive. A crash can leave a gate
// that needs manual inspection and deletion; this refuses a payment rather
// than permitting a second active wallet writer. Waits happen in the caller,
// NEVER under the gate. No keys, payment or network operations happen here.
//
// This is a cooperative local lock on one filesystem, not a cross-host lock.
// A human removing an in-use gate defeats the protocol and is unsupported.
function reapDeadHolder(file, expectedHolderRecord, holderIsStillDead) {
  const gate = file + '.reaper';
  let fd;
  try {
    fd = fs.openSync(gate, 'wx', 0o600);
  } catch (err) {
    if (err.code === 'EEXIST') return { state: 'busy', gate };
    throw err;
  }

  try {
    let current;
    try {
      current = fs.readFileSync(file, 'utf8');
    } catch (err) {
      if (err.code === 'ENOENT') return { state: 'changed', gate };
      throw err;  // Never assume that an unreadable lock is safe to remove.
    }
    if (current !== expectedHolderRecord || !holderIsStillDead())
      return { state: 'changed', gate };

    // Under the exclusive gate, only this reaper may reclaim a dead holder.
    // The original holder was independently checked as gone using ESRCH.
    try {
      fs.unlinkSync(file);
      return { state: 'removed', gate };
    } catch (err) {
      if (err.code === 'ENOENT') return { state: 'changed', gate };
      throw err;
    }
  } finally {
    // The gate exists for filesystem recheck/unlink ONLY. Never sleep or
    // make paid calls between its creation and release.
    try {
      fs.closeSync(fd);
    } finally {
      fs.unlinkSync(gate);
    }
  }
}

module.exports = { reapDeadHolder };
