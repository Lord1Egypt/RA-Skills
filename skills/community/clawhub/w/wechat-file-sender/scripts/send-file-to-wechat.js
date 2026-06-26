#!/usr/bin/env node
// send-file-to-wechat.js
// Send files via Windows WeChat client
// Usage: node send-file-to-wechat.js "<filePath>" "<contactName>"
//
// SECURITY NOTES:
// - Only use with files and contacts you trust
// - filePath is validated to prevent injection
// - contactName is sanitized to prevent SendKeys injection
// - No network calls, no data exfiltration
// - ExecutionPolicy Bypass is required: PowerShell blocks .ps1 scripts by default

const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

const args = process.argv.slice(2);
if (args.length < 2) {
    console.error('[ERROR] Usage: node send-file-to-wechat.js "<filePath>" "<contactName>"');
    process.exit(1);
}

let filePath = args[0];
let contactName = args[1];

// SECURITY: Validate filePath - must be an absolute path
if (!path.isAbsolute(filePath)) {
    console.error('[ERROR] filePath must be an absolute path');
    process.exit(1);
}

// SECURITY: Validate contactName - no special characters, max 50 chars
if (!/^[\u4e00-\u9fa5a-zA-Z0-9_\s]{1,50}$/.test(contactName)) {
    console.error('[ERROR] contactName contains invalid characters');
    process.exit(1);
}

// SECURITY: Check file exists
if (!fs.existsSync(filePath)) {
    console.error('[ERROR] File does not exist: ' + filePath);
    process.exit(1);
}

// SECURITY: Escape double quotes for shell safety
const safeFilePath = filePath.replace(/"/g, '\\"');
const safeContactName = contactName.replace(/"/g, '\\"');

// Resolve script path relative to this script's directory
const scriptDir = __dirname;
const ps1Path = path.join(scriptDir, 'send-file.ps1');

if (!fs.existsSync(ps1Path)) {
    console.error('[ERROR] send-file.ps1 not found at: ' + ps1Path);
    process.exit(1);
}

try {
    const r = execSync(
        'powershell -ExecutionPolicy Bypass -File "' + ps1Path + '" -filePath "' + safeFilePath + '" -contactName "' + safeContactName + '"',
        { encoding: 'utf8', timeout: 30000, windowsHide: true, stdio: ['pipe', 'pipe', 'pipe'] }
    );
    console.log(r.trim());
    if (r.includes('[ERROR]')) process.exit(1);
} catch(e) {
    const msg = e.stdout ? e.stdout.trim() : e.message;
    console.error('[ERROR] ' + msg);
    process.exit(1);
}
