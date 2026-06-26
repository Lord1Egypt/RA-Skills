#!/usr/bin/env node

const { ensureWenyanReady } = require('../publisher/wenyan_runner');

try {
    const runner = ensureWenyanReady({ forceBootstrap: true });
    console.log(`内置 wenyan-cli 已就绪: ${runner.label}`);
} catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exit(1);
}
