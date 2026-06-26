'use strict';

// Read bytes from a single user-supplied file for multipart upload.
//
// Scope:
//   - Only paths already validated by classifyInput() in run.js (CLI
//     positional argument → resolve → stat → regular file).
//   - Refuses descriptors that are not kind: 'file' (fail closed).
//   - No network I/O here; run.js passes the Buffer to lib/http.js
//     pipelineUpload(), which POSTs to the configured pipeline API.
//   - No environment reads; no reads outside the vetted path.
//
// Documented capability: upload user-named files to the remote pipeline
// service. See config.json permissions.filesystem.read / .network and
// SKILL.md (privacy: files leave the local machine for server-side processing).

const fs = require('fs');

function readClassifiedFileBuffer(classified) {
  if (!classified || classified.kind !== 'file' || typeof classified.path !== 'string') {
    throw new Error('readClassifiedFileBuffer: expected a classifyInput()-vetted file descriptor');
  }
  // One-shot CLI read; server rejects uploads above MARKITDOWN_MAX_INPUT_BYTES (~50 MiB).
  return fs.readFileSync(classified.path);
}

module.exports = {
  readClassifiedFileBuffer
};
