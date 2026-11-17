// Explicit live query helper; no built-in destinations or automatic network requests.
'use strict';
if (require.main === module) {
  try { require('../query_trip').main(); } catch (e) { console.error(e.message); process.exitCode = 1; }
}
