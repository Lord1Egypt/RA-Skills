const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT_DIR = path.resolve(__dirname, '..', '..');
const BUNDLED_WENYAN_DIR = path.join(ROOT_DIR, 'vendor', 'wenyan-cli-main');
const BUNDLED_WENYAN_CLI_PATH = path.join(BUNDLED_WENYAN_DIR, 'dist', 'cli.js');

function commandExists(command, args = ['--version']) {
    try {
        execFileSync(command, args, { stdio: 'pipe' });
        return true;
    } catch {
        return false;
    }
}

function getNodeInvocation(cliPath) {
    return { command: 'node', prefixArgs: [cliPath], label: cliPath };
}

function isRunnableCli(cliPath) {
    if (!cliPath || !fs.existsSync(cliPath)) {
        return false;
    }

    try {
        execFileSync('node', [cliPath, '--version'], { stdio: 'pipe' });
        return true;
    } catch {
        return false;
    }
}

function resolvePackageManager() {
    if (commandExists('pnpm')) {
        return { command: 'pnpm', prefixArgs: [], label: 'pnpm' };
    }

    try {
        execFileSync('corepack', ['pnpm', '--version'], { stdio: 'pipe' });
        return { command: 'corepack', prefixArgs: ['pnpm'], label: 'corepack pnpm' };
    } catch {
        return null;
    }
}

function bootstrapBundledWenyan(options = {}) {
    const packageJsonPath = path.join(BUNDLED_WENYAN_DIR, 'package.json');
    if (!fs.existsSync(packageJsonPath)) {
        throw new Error(`未找到内置 wenyan-cli 源码: ${BUNDLED_WENYAN_DIR}`);
    }

    const packageManager = resolvePackageManager();
    if (!packageManager) {
        throw new Error('未找到 pnpm。请先安装 pnpm，或执行 `corepack enable` 后重试');
    }

    const log = options.log || console.log;
    log(`[wechat-toolkit] 初始化内置 wenyan-cli: ${BUNDLED_WENYAN_DIR}`);

    execFileSync(packageManager.command, [...packageManager.prefixArgs, 'install', '--frozen-lockfile'], {
        cwd: BUNDLED_WENYAN_DIR,
        stdio: 'inherit',
    });

    execFileSync(packageManager.command, [...packageManager.prefixArgs, 'build'], {
        cwd: BUNDLED_WENYAN_DIR,
        stdio: 'inherit',
    });

    if (!isRunnableCli(BUNDLED_WENYAN_CLI_PATH)) {
        throw new Error('内置 wenyan-cli 初始化失败，dist/cli.js 仍不可执行');
    }
}

function ensureWenyanReady(options = {}) {
    if (isRunnableCli(BUNDLED_WENYAN_CLI_PATH) && !options.forceBootstrap) {
        return getNodeInvocation(BUNDLED_WENYAN_CLI_PATH);
    }

    if (fs.existsSync(BUNDLED_WENYAN_DIR)) {
        bootstrapBundledWenyan(options);
        return getNodeInvocation(BUNDLED_WENYAN_CLI_PATH);
    }

    if (options.allowGlobalFallback && commandExists('wenyan')) {
        return { command: 'wenyan', prefixArgs: [], label: 'wenyan' };
    }

    throw new Error(
        '未找到可用的 wenyan-cli。请确认 skill 内置 vendor/wenyan-cli-main 存在，并先执行 `node scripts/bootstrap/install_wenyan.js`',
    );
}

function execWenyan(args, options = {}) {
    const { allowGlobalFallback, forceBootstrap, ...execOptions } = options;
    const runner = ensureWenyanReady({ allowGlobalFallback, forceBootstrap });
    return execFileSync(runner.command, [...runner.prefixArgs, ...args], execOptions);
}

module.exports = {
    BUNDLED_WENYAN_CLI_PATH,
    BUNDLED_WENYAN_DIR,
    ensureWenyanReady,
    execWenyan,
};
