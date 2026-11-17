#!/usr/bin/env node
'use strict';
const { readJson, object } = require('./scripts/lib/safety');
const { callTuniu } = require('./scripts/lib/tuniu');
function main(args = process.argv.slice(2)) {
  if (args.length !== 2 || args[0] !== '--input') throw new Error('Usage: node query_trip.js --input QUERY.json');
  const query = readJson(args[1]);
  object(query, ['server', 'tool', 'params'], 'query');
  const result = callTuniu(query.server, query.tool, query.params);
  console.log(JSON.stringify(result, null, 2));
  return result;
}
if (require.main === module) {
  try { main(); } catch (e) { console.error(e.message); process.exitCode = 1; }
}
module.exports = { main };
