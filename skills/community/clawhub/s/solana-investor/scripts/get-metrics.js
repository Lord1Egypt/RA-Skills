#!/usr/bin/env node
/**
 * Output metrics summary for last 24 hours
 * Usage: node get-metrics.js
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');

const { getMetricsSummary } = require(path.join(sharedDir, 'metrics'));

function main() {
    const summary = getMetricsSummary();
    console.log(JSON.stringify(summary, null, 2));
}

main();
