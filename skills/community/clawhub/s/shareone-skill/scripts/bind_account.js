#!/usr/bin/env node

// Account binding script: send verification code to email, then verify to bind
// email to an existing guest API key (upgrading guest → registered user).
//
// Usage:
//   node bind_account.js --send --email user@example.com
//   node bind_account.js --verify --email user@example.com --code 123456

const {
    printShareOneScriptError,
    emitError,
    getBaseUrl,
    requestPublicShareOneJson,
    resolveDirectApiKey,
} = require('./shareone_client');

const args = process.argv.slice(2);
let action = null;
let email = null;
let code = null;
let apiKey = null;
let lang = null;

function usage() {
    console.error('Usage:');
    console.error('  node bind_account.js --send --email <email> [--api-key <key>] [--lang en|zh]');
    console.error('  node bind_account.js --verify --email <email> --code <6-digit-code> [--api-key <key>]');
}

function nextValue(index, flag) {
    const value = args[index + 1];
    if (value === undefined || value.startsWith('--')) {
        emitError(`ERROR:MISSING_VALUE:${flag}`);
    }
    return value;
}

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--send') {
        action = 'send';
    } else if (args[i] === '--verify') {
        action = 'verify';
    } else if (args[i] === '--email') {
        email = nextValue(i, args[i]);
        i += 1;
    } else if (args[i] === '--code') {
        code = nextValue(i, args[i]);
        i += 1;
    } else if (args[i] === '--api-key') {
        apiKey = nextValue(i, args[i]);
        i += 1;
    } else if (args[i] === '--lang') {
        lang = nextValue(i, args[i]);
        i += 1;
    } else {
        emitError(`ERROR:UNKNOWN_ARGUMENT:${args[i]}`);
    }
}

if (!action) {
    emitError('ERROR:NO_ACTION', ['Specify --send or --verify.'].join('\n'));
}

if (!email) {
    emitError('ERROR:MISSING_EMAIL');
}

function resolveApiKey() {
    const key = resolveDirectApiKey(apiKey);
    if (!key) {
        emitError('ERROR:KEY_NOT_FOUND', ['No API Key found. Run ensure_credentials.js first or pass --api-key.'].join('\n'));
    }
    return key;
}

async function sendCode() {
    const key = resolveApiKey();
    const payload = { email, api_key: key };
    if (lang) payload.lang = lang;

    await requestPublicShareOneJson('/api/v1/auth/email/send-code', {
        method: 'POST',
        authRequired: false,
    }, payload);
    console.log('CODE_SENT');
    console.log(`Verification code sent to ${email}`);

}

async function verifyCode() {
    const key = resolveApiKey();

    if (!code) {
        emitError('ERROR:MISSING_CODE', ['--code is required for --verify.'].join('\n'));
    }

    if (!/^\d{6}$/.test(code)) {
        emitError('ERROR:INVALID_CODE_FORMAT', ['Code must be exactly 6 digits.'].join('\n'));
    }

    const result = await requestPublicShareOneJson('/api/v1/auth/email/verify', {
        method: 'POST',
        authRequired: false,
    }, { email, code, api_key: key });
    console.log('BIND_SUCCESS');
    console.log(`Account bound to ${email}. API Key unchanged.`);
    if (result.username) {
        console.log(`USERNAME:${result.username}`);
    }
    console.log(`You can now log in at ${getBaseUrl()} with this email to manage your shares.`);

}

if (action === 'send') {
    sendCode().catch((error) => {
        process.exit(printShareOneScriptError(error));
    });
} else {
    verifyCode().catch((error) => {
        process.exit(printShareOneScriptError(error));
    });
}
