#!/usr/bin/env node
/**
 * Apply verified models to OpenClaw configuration and restart service.
 * OpenClaw-specific version of apply_updates.py
 */

const fs = require('fs');
const path = require('path');

const HOME = process.env.HOME || process.env.USERPROFILE;
const CLAUDE_SETTINGS = path.join(HOME, '.claude', 'settings.json');
const OPENCLAW_CONFIG = path.join(HOME, '.openclaw', 'openclaw.json');
const VERIFIED_MODELS_FILE = '/tmp/verified_models.txt';

function log(message, type = 'info') {
    const prefix = type === 'error' ? '❌' : type === 'success' ? '✅' : 'ℹ️';
    console.log(`${prefix} ${message}`);
}

function validateJSON(filepath) {
    try {
        fs.readFileSync(filepath, 'utf8');
        JSON.parse(fs.readFileSync(filepath));
        return { valid: true };
    } catch (e) {
        return { valid: false, error: e.message };
    }
}

function updateOpenClawConfig(verifiedModels) {
    if (!fs.existsSync(OPENCLAW_CONFIG)) {
        log(`${OPENCLAW_CONFIG} not found, skipping`, 'warn');
        return;
    }

    const config = JSON.parse(fs.readFileSync(OPENCLAW_CONFIG, 'utf8'));
    const primary = 'stepfun/step-3.5-flash:free';

    // Update provider.models
    const providerModels = verifiedModels.map(modelId => ({
        id: modelId,
        name: modelId.split('/').pop(),
        api: 'openai-completions'
    }));
    config.models.providers.openrouter.models = providerModels;
    log(`Updated provider.models with ${providerModels.length} models`);

    // Update fallbacks (excluding primary)
    const fallbacks = verifiedModels
        .filter(m => m !== primary)
        .map(m => `openrouter/${m}`);
    config.agents.defaults.model.fallbacks = fallbacks;
    log(`Updated fallbacks with ${fallbacks.length} models`);

    // Update agents.defaults.models
    for (const modelId of verifiedModels) {
        const key = `openrouter/${modelId}`;
        if (!config.agents.defaults.models[key]) {
            config.agents.defaults.models[key] = {};
        }
    }
    log(`Ensured ${verifiedModels.length} models in agents.defaults.models`);

    // Write back with formatting
    fs.writeFileSync(OPENCLAW_CONFIG, JSON.stringify(config, null, 2) + '\n');

    // Validate
    const validation = validateJSON(OPENCLAW_CONFIG);
    if (validation.valid) {
        log('OpenClaw config updated and validated', 'success');
    } else {
        log(`OpenClaw config JSON error: ${validation.error}`, 'error');
        process.exit(1);
    }
}

function main() {
    log('=== OpenClaw Model Update Tool ===');

    // Check input file
    if (!fs.existsSync(VERIFIED_MODELS_FILE)) {
        log(`${VERIFIED_MODELS_FILE} not found. Please run test_models.js first.`, 'error');
        process.exit(1);
    }

    const verifiedModels = fs.readFileSync(VERIFIED_MODELS_FILE, 'utf8')
        .trim()
        .split('\n')
        .filter(line => line.trim().length > 0);

    log(`Applying ${verifiedModels.length} verified models...`);

    updateOpenClawConfig(verifiedModels);

    log('✅ All configurations updated successfully!');
    log('\nNext steps:');
    log('  1. Restart OpenClaw: ./restart_openclaw.sh');
    log('  2. Test with: openclaw (verify fallbacks work)');
}

if (require.main === module) {
    main();
}

module.exports = { updateOpenClawConfig };
