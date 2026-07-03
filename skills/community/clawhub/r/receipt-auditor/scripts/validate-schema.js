#!/usr/bin/env node
/**
 * validate-schema.js — Validates a receipt-auditor output against the schema.
 *
 * Usage:
 *   node validate-schema.js < path/to/output.json
 *   node validate-schema.js --file output.json
 */

const fs = require('fs');
const path = require('path');

const SCHEMA_PATH = path.join(__dirname, '..', 'schemas', 'output.schema.json');

function loadSchema() {
    return JSON.parse(fs.readFileSync(SCHEMA_PATH, 'utf8'));
}

function validate(data) {
    const errors = [];

    // Required top-level
    if (!data.mode) errors.push('"mode" is required');
    if (!data.timestamp) errors.push('"timestamp" is required');

    if (data.mode === 'report') {
        if (!data.report) {
            errors.push('"report" is required for mode=report');
        } else {
            if (!Array.isArray(data.report.entries)) errors.push('"report.entries" must be an array');
            if (typeof data.report.total !== 'number') errors.push('"report.total" must be a number');
            if (data.report.entries) {
                data.report.entries.forEach((e, i) => {
                    ['date', 'category', 'amount', 'description'].forEach(f => {
                        if (!(f in e)) errors.push(`report.entries[${i}].${f} is required`);
                    });
                });
            }
        }
    }

    if (data.mode === 'aa-split') {
        if (!data.aaResult) {
            errors.push('"aaResult" is required for mode=aa-split');
        } else {
            if (!Array.isArray(data.aaResult.people)) errors.push('"aaResult.people" must be an array');
            if (typeof data.aaResult.totalVerified !== 'number') errors.push('"aaResult.totalVerified" must be a number');
            if (data.aaResult.people) {
                data.aaResult.people.forEach((p, i) => {
                    ['name', 'personalItemsTotal', 'sharedShare', 'totalPayable'].forEach(f => {
                        if (!(f in p)) errors.push(`aaResult.people[${i}].${f} is required`);
                    });
                });
            }
        }
    }

    if (data.mode === 'audit') {
        if (!data.auditResult) {
            errors.push('"auditResult" is required for mode=audit');
        } else {
            if (!Array.isArray(data.auditResult.entries)) errors.push('"auditResult.entries" must be an array');
            if (!Array.isArray(data.auditResult.anomalies)) errors.push('"auditResult.anomalies" must be an array');
            if (typeof data.auditResult.total !== 'number') errors.push('"auditResult.total" must be a number');
        }
    }

    return {
        valid: errors.length === 0,
        errors,
        fields: Object.keys(data)
    };
}

function main() {
    const args = process.argv.slice(2);
    let raw;

    if (args.includes('--file')) {
        const idx = args.indexOf('--file');
        const filePath = args[idx + 1];
        raw = fs.readFileSync(filePath, 'utf8');
    } else {
        raw = fs.readFileSync('/dev/stdin', 'utf8');
    }

    let data;
    try {
        data = JSON.parse(raw);
    } catch (e) {
        console.error('❌ Invalid JSON:', e.message);
        process.exit(1);
    }

    const result = validate(data);
    if (result.valid) {
        console.log(`✅ Output is valid. Mode: ${data.mode}, Fields: ${result.fields.join(', ')}`);
        process.exit(0);
    } else {
        console.log('❌ Output validation failed:');
        result.errors.forEach(e => console.log(`   • ${e}`));
        process.exit(1);
    }
}

if (require.main === module) main();

module.exports = { validate, loadSchema };
