#!/usr/bin/env node
/**
 * Refresh local note scan state
 * Version: 2.0.0 - NEW in v2
 */

const { rebuildIndex } = require('./lib/common');

const args = process.argv.slice(2);
const input = args.length > 0 ? JSON.parse(args[0]) : {};

const result = rebuildIndex();
console.log(JSON.stringify(result, null, 2));

