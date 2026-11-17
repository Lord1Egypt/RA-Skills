// Local installation check only; this does not contact Tuniu.
'use strict';
if (require.main === module) {
  try { require('./lib/tuniu').resolveTuniu(); console.log('Pinned local Tuniu CLI is available.'); }
  catch (e) { console.error(e.message); process.exitCode = 1; }
}
