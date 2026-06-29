#!/usr/bin/env node
"use strict";
// ============================================================
// task-orchestrate.ts · AO 编排包装（TypeScript 版）
// ============================================================
// v0.97: 两档拆解（拆 vs. 不拆），砍掉 L1-L4 四级深度。
// AO compose 只做一次拆解，不做渐进减薄。
// 缓存复用：同一节点有历史 DAG 则跳过 compose。
// 简单任务直接跳过 AO compose。
//
// 用法:
//   node task-orchestrate.ts "任务描述"
//   node task-orchestrate.ts "任务描述" --dry-run
//   node task-orchestrate.ts "任务描述" --worktree
//   node task-orchestrate.ts "任务描述" --model flash|pro
// ============================================================
Object.defineProperty(exports, "__esModule", { value: true });
const child_process_1 = require("child_process");
const fs_1 = require("fs");
const path_1 = require("path");
const crypto_1 = require("crypto");
/** ao compose 编排超时（180s） */
const AO_TIMEOUT = 180_000;
/** ao 其他操作超时（30s） */
const AO_UTIL_TIMEOUT = 30_000;
const VERSION = '0.97';
const RED = '\x1b[0;31m';
const GREEN = '\x1b[0;32m';
const YELLOW = '\x1b[1;33m';
const BLUE = '\x1b[0;34m';
const NC = '\x1b[0m';
function info(msg) { console.log(`${BLUE}[orchestrate]${NC} ${msg}`); }
function ok(msg) { console.log(`${GREEN}[✓]${NC} ${msg}`); }
function warn(msg) { console.log(`${YELLOW}[!]${NC} ${msg}`); }
function err(msg) { console.error(`${RED}[✗]${NC} ${msg}`); }
// 两档拆解模式
const BINARY_MODE = { SPLIT: '拆', DIRECT: '不拆' };
// ── Arg parsing ──
let taskDesc = '';
let dryRun = false;
let useWorktree = false;
let aoModel = '';
const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
    const a = args[i];
    switch (a) {
        case '--dry-run':
            dryRun = true;
            break;
        case '--worktree':
            useWorktree = true;
            break;
        case '--model':
            aoModel = args[++i];
            break;
        case '--version':
            console.log(`sofagent-task-orchestrate v${VERSION}`);
            process.exit(0);
        case '--help':
            showHelp();
            process.exit(0);
        default:
            if (a.startsWith('--model=')) {
                aoModel = a.split('=')[1];
                break;
            }
            if (!a.startsWith('--')) {
                taskDesc = a;
                break;
            }
    }
}
if (!taskDesc) {
    err('缺少任务描述。用法: task-orchestrate "你的任务"');
    process.exit(1);
}
// ── Pre-check: ao ──
if (!commandExists('ao')) {
    warn('agency-orchestrator (ao) 未安装——编排引擎不可用');
    warn('降级方案：手动拆任务 → 逐条手动记录 → 手动闭环');
    defaultOrchestrate(taskDesc);
    process.exit(0);
}
console.log('');
console.log('  ╔═══════════════════════════════════╗');
console.log('  ║   sofagent · task orchestrate    ║');
console.log('  ╚═══════════════════════════════════╝');
console.log('');
// ── Task slug ──
const taskSlug = (0, crypto_1.createHash)('sha256').update(taskDesc).digest('hex').slice(0, 8);
// ── Data directory ──
const homeDir = process.env.HOME || '/tmp';
const sofagentData = process.env.SOFAGENT_DATA || (0, path_1.join)(homeDir, '.sofagent');
const orchestratorDir = (0, path_1.join)(sofagentData, 'orchestrator');
const workflowsDir = (0, path_1.join)(orchestratorDir, 'workflows');
const cachedYaml = (0, path_1.join)(workflowsDir, `${taskSlug}.yaml`);
(0, fs_1.mkdirSync)(workflowsDir, { recursive: true });
// ── History analysis ──
function analyzeTrackRecord(slug) {
    const logDir = (0, path_1.join)(sofagentData, 'task', 'logs');
    let total = 0, success = 0;
    try {
        for (const sub of (0, fs_1.readdirSync)(logDir, { withFileTypes: true })) {
            if (!sub.isDirectory())
                continue;
            for (const f of (0, fs_1.readdirSync)((0, path_1.join)(logDir, sub.name))) {
                if (!f.endsWith('.md'))
                    continue;
                const content = (0, fs_1.readFileSync)((0, path_1.join)(logDir, sub.name, f), 'utf-8');
                if (!content.includes(slug))
                    continue;
                total++;
                if (/状态\s*\|\s*成功/.test(content))
                    success++;
            }
        }
    }
    catch { /* log dir may not exist */ }
    return [total, success];
}
const [totalRuns, successRuns] = analyzeTrackRecord(taskDesc);
if (totalRuns > 0) {
    const pct = Math.round(successRuns * 100 / totalRuns);
    info(`历史记录: ${totalRuns} 次运行 · 成功率 ${pct}%`);
}
// ── 两档判定：拆 vs. 不拆 ──
// 吸收 L3 缓存复用能力：有历史缓存 → 跳过 compose
// 吸收 L4 跳编排能力：简单任务 → 直接执行
let mode;
let skipAoCompose = false;
if ((0, fs_1.existsSync)(cachedYaml)) {
    // 有历史缓存 → 复用（吸收 L3）
    skipAoCompose = true;
    mode = BINARY_MODE.DIRECT;
    ok(`缓存复用 — ${taskSlug}.yaml（跳编排）`);
}
else if (totalRuns >= 3 && successRuns >= totalRuns) {
    // 连续 3+ 次成功 → 直接执行（吸收 L4）
    mode = BINARY_MODE.DIRECT;
    info(`${BINARY_MODE.DIRECT} — 任务稳定（连续 ${successRuns}/${totalRuns} 成功），直接交付 Agent`);
}
else {
    // 默认走拆解
    mode = BINARY_MODE.SPLIT;
    info(`编排模式: ${BINARY_MODE.SPLIT} — AO compose 一次性拆解`);
}
console.log('');
// ── 不拆：跳过编排，直接执行 ──
if (mode === BINARY_MODE.DIRECT && !skipAoCompose) {
    info('跳过编排/Harness/worktree，直接执行...');
    const start = Date.now();
    const r = runAo([taskDesc]);
    const elapsed = Math.round((Date.now() - start) / 1000);
    console.log('');
    r.code === 0 ? ok(`任务完成（耗时 ${elapsed}s）`) : warn(`任务结束（exit ${r.code}，耗时 ${elapsed}s）`);
    console.log('');
    console.log(`  编排结束。exit code: ${r.code} · 模式: ${BINARY_MODE.DIRECT}`);
    console.log('');
    process.exit(r.code);
}
// ════════════════════════════════════════
// 拆模式：AO compose 一次性拆解 → 执行
// ════════════════════════════════════════
// ── Step 1: AO compose（仅一次，不做渐进减薄）──
let workflowFile = '';
if (skipAoCompose) {
    workflowFile = cachedYaml;
    info(`Step 1/3 · 使用缓存模板`);
}
else {
    info('Step 1/3 · AO 编排分析（一次性拆解）...');
    if (aoModel)
        info(`  模型: ${aoModel}`);
    workflowFile = (0, path_1.join)(process.env.TMPDIR || '/tmp', `sofagent-workflow-${process.pid}.yaml`);
    try {
        const aoArgs = aoModel ? ['compose', '--model', aoModel, taskDesc] : ['compose', taskDesc];
        const output = (0, child_process_1.execFileSync)('ao', aoArgs, { encoding: 'utf-8', timeout: AO_TIMEOUT });
        (0, fs_1.writeFileSync)(workflowFile, output);
    }
    catch {
        warn('ao compose 未生成 YAML，尝试直接执行...');
        try {
            (0, child_process_1.execFileSync)('ao', ['compose', taskDesc, '--run'], { stdio: 'inherit', timeout: AO_TIMEOUT });
            process.exit(0);
        }
        catch {
            process.exit(1);
        }
    }
    if ((0, fs_1.existsSync)(workflowFile)) {
        ok('编排计划已生成');
        try {
            info('编排预览:');
            (0, child_process_1.execFileSync)('ao', ['explain', workflowFile], { stdio: 'inherit', timeout: AO_UTIL_TIMEOUT });
        }
        catch {
            console.log((0, fs_1.readFileSync)(workflowFile, 'utf-8').split('\n').slice(0, 20).join('\n'));
        }
    }
}
console.log('');
// ── Dry-run exit ──
if (dryRun) {
    info('dry-run 模式，退出');
    process.exit(0);
}
// ── Step 2: Worktree 隔离 ──
const worktrees = [];
function cleanupWorktrees() {
    for (const wt of worktrees) {
        if ((0, fs_1.existsSync)(wt)) {
            info(`清理 worktree: ${wt}`);
            try {
                (0, child_process_1.execFileSync)('git', ['worktree', 'remove', wt, '--force'], { stdio: 'ignore', timeout: AO_UTIL_TIMEOUT });
            }
            catch {
                try {
                    (0, fs_1.rmSync)(wt, { recursive: true, force: true });
                }
                catch { /* */ }
            }
        }
    }
}
process.on('exit', cleanupWorktrees);
process.on('SIGINT', () => { cleanupWorktrees(); process.exit(130); });
process.on('SIGTERM', () => { cleanupWorktrees(); process.exit(143); });
if (useWorktree) {
    let inGitRepo = false;
    try {
        (0, child_process_1.execFileSync)('git', ['rev-parse', '--git-dir'], { stdio: 'ignore' });
        inGitRepo = true;
    }
    catch { /* */ }
    if (inGitRepo) {
        info('Step 2/3 · 创建 worktree 隔离...');
        let subCount = 1;
        const cachedFile = skipAoCompose ? cachedYaml : workflowFile;
        if ((0, fs_1.existsSync)(cachedFile)) {
            try {
                const yamlContent = (0, fs_1.readFileSync)(cachedFile, 'utf-8');
                const matches = yamlContent.match(/subtask|agent|workflow/gi);
                if (matches)
                    subCount = Math.min(Math.max(matches.length, 1), 5);
            }
            catch { /* */ }
        }
        let baseBranch = 'main';
        try {
            baseBranch = (0, child_process_1.execFileSync)('git', ['branch', '--show-current'], { encoding: 'utf-8', timeout: AO_UTIL_TIMEOUT }).trim() || 'main';
        }
        catch { /* */ }
        for (let i = 1; i <= subCount; i++) {
            const wtName = `sofagent-task-${i}-${process.pid}`;
            const wtPath = (0, path_1.join)(process.env.TMPDIR || '/tmp', wtName);
            info(`  创建 worktree ${i}/${subCount}: ${wtPath}`);
            try {
                (0, child_process_1.execFileSync)('git', ['worktree', 'add', wtPath, baseBranch], { stdio: 'ignore', timeout: AO_UTIL_TIMEOUT });
                worktrees.push(wtPath);
            }
            catch {
                warn(`  worktree 创建失败，跳过隔离`);
            }
        }
        if (worktrees.length > 0) {
            ok(`${worktrees.length} 个 worktree 就绪`);
        }
    }
    else {
        warn('不在 git 仓库中，跳过 worktree 隔离');
    }
}
else {
    info('Step 2/3 · 跳过 worktree 隔离（加 --worktree 启用）');
}
console.log('');
// ── Step 3: Harness ──
info('Step 3/3 · Harness 约束...');
const hookDir = (0, path_1.join)(homeDir, '.openclaw', 'hooks', 'sofagent-load-chain');
if ((0, fs_1.existsSync)((0, path_1.join)(hookDir, 'handler.ts')) && (0, fs_1.existsSync)((0, path_1.join)(hookDir, 'HOOK.md'))) {
    ok('加载链 hook 就绪');
}
else {
    warn(`加载链 hook 未部署: ${hookDir}`);
    warn('子 Agent 可能拿不到 think.md/rules.md');
}
console.log('');
// ── Execute ──
info('执行任务编排...');
const startTime = Date.now();
let result;
const executeFile = (0, fs_1.existsSync)(workflowFile) ? workflowFile : '';
if (executeFile) {
    result = runAo(['run', executeFile]);
}
else {
    result = runAo(['compose', taskDesc, '--run']);
}
const elapsed = Math.round((Date.now() - startTime) / 1000);
console.log('');
if (result.code === 0) {
    ok(`任务完成（耗时 ${elapsed}s）`);
    // Cache workflow on success
    if (!skipAoCompose && (0, fs_1.existsSync)(workflowFile)) {
        try {
            (0, fs_1.mkdirSync)(orchestratorDir, { recursive: true });
            (0, fs_1.copyFileSync)(workflowFile, cachedYaml);
            info(`工作流已缓存: ${taskSlug}.yaml`);
        }
        catch { /* */ }
    }
}
else {
    warn(`任务结束（exit ${result.code}，耗时 ${elapsed}s）`);
}
console.log('');
console.log(`  编排结束。exit code: ${result.code} · 模式: ${mode}`);
console.log('');
process.exit(result.code);
// ════════════════════════════════════════
// Helpers
// ════════════════════════════════════════
function commandExists(cmd) {
    try {
        (0, child_process_1.execFileSync)('which', [cmd], { stdio: 'ignore' });
        return true;
    }
    catch {
        return false;
    }
}
function runAo(aoArgs) {
    try {
        (0, child_process_1.execFileSync)('ao', aoArgs, { stdio: 'inherit', timeout: AO_TIMEOUT });
        return { code: 0 };
    }
    catch (e) {
        return { code: e.status ?? e.code ?? 1 };
    }
}
function defaultOrchestrate(task) {
    console.log('');
    console.log('  ╔═══════════════════════════════════╗');
    console.log('  ║   sofagent · 默认编排（无 ao）    ║');
    console.log('  ╚═══════════════════════════════════╝');
    console.log('');
    console.log(`  任务: ${task}`);
    console.log('');
    console.log('  建议手动拆为 3-5 个子任务：');
    console.log('    1. 分析/准备 → developer');
    console.log('    2. 核心实现 → developer');
    console.log('    3. 验证/测试 → qa-engineer');
    console.log('    4. 文档/收尾 → technical-writer');
    console.log('');
}
function showHelp() {
    console.log(`sofagent task-orchestrate v${VERSION}`);
    console.log('  包装 ao compose，加 worktree 隔离 + 约束注入');
    console.log('');
    console.log('  用法:');
    console.log('    task-orchestrate "任务描述"');
    console.log('    task-orchestrate "任务描述" --dry-run    仅预览编排');
    console.log('    task-orchestrate "任务描述" --worktree   创建独立 worktree');
    console.log('    task-orchestrate "任务描述" --model flash|pro  指定模型');
    console.log('');
    console.log('  两档拆解:');
    console.log('    拆    首次运行或复杂任务，AO compose 一次性拆解');
    console.log('    不拆  历史成功率100%或有缓存 → 直接交付 Agent');
    console.log('');
    console.log('  依赖: agency-orchestrator (ao), git (worktree 模式)');
}
//# sourceMappingURL=task-orchestrate.js.map