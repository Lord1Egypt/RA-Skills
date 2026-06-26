#!/usr/bin/env node
/**
 * Evaluate readiness path from simulation mode to real execution mode.
 * Usage: node evaluate-execution-mode.js [--lang zh|en] [--json]
 */
const fs = require('fs');
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');

const config = require(path.join(sharedDir, 'config'));
const { initDatabase, getDb } = require(path.join(sharedDir, 'database'));
const { formatError } = require(path.join(sharedDir, 'errors'));

const lang = process.argv.includes('--lang') ? process.argv[process.argv.indexOf('--lang') + 1] : 'zh';
const asJson = process.argv.includes('--json');
const isZh = lang !== 'en';

function count(sql) {
    return getDb().prepare(sql).get().count;
}

function statusWeight(status) {
    if (status === 'pass') return 1;
    if (status === 'warn') return 0.5;
    return 0;
}

function statusBadge(status) {
    if (status === 'pass') return '✅ PASS';
    if (status === 'warn') return '⚠️ WARN';
    return '❌ FAIL';
}

function evaluateChecks(context) {
    const docsDir = path.resolve(__dirname, '..', '..', '..', 'docs');
    const requiredDocs = ['compliance-policy.md', 'terms-of-service.md', 'risk-disclosure.md'];
    const existingDocs = requiredDocs.filter((name) => fs.existsSync(path.join(docsDir, name)));

    const checks = [
        {
            key: 'simulation_only',
            status: 'warn',
            zh: '当前执行仍为模拟模式，未进行链上真实交换。',
            en: 'Execution is currently simulation-only, with no live on-chain swaps.',
            actionZh: '保留模拟模式用于回归测试，同时规划真实执行灰度。',
            actionEn: 'Keep simulation for regression tests and plan phased live execution rollout.',
        },
        {
            key: 'network',
            status: config.solanaNetwork === 'mainnet-beta' ? 'pass' : 'warn',
            zh: `当前网络为 ${config.solanaNetwork}。`,
            en: `Current network is ${config.solanaNetwork}.`,
            actionZh: '上线前建议先在 devnet/testnet 完成全链路演练，再切换 mainnet-beta。',
            actionEn: 'Before launch, complete end-to-end rehearsal on devnet/testnet, then switch to mainnet-beta.',
        },
        {
            key: 'helius',
            status: config.heliusApiKey ? 'pass' : 'warn',
            zh: config.heliusApiKey ? '已配置 HELIUS_API_KEY。' : '未配置 HELIUS_API_KEY（可用性与监控能力受限）。',
            en: config.heliusApiKey ? 'HELIUS_API_KEY is configured.' : 'HELIUS_API_KEY is missing (availability/monitoring reduced).',
            actionZh: '配置专用 Helius Key 并设置限流/告警阈值。',
            actionEn: 'Configure dedicated Helius key and define rate-limit/alert thresholds.',
        },
        {
            key: 'notification',
            status: process.env.TELEGRAM_BOT_TOKEN ? 'pass' : 'warn',
            zh: process.env.TELEGRAM_BOT_TOKEN ? '已配置 Telegram 通知通道。' : '未配置 Telegram 通知通道。',
            en: process.env.TELEGRAM_BOT_TOKEN ? 'Telegram notification channel is configured.' : 'Telegram notification channel is not configured.',
            actionZh: '确保策略执行失败、价格触发、风控事件均可即时通知。',
            actionEn: 'Ensure execution failures, alert triggers, and risk events notify users immediately.',
        },
        {
            key: 'signer_control',
            status: process.env.EXECUTION_SIGNER_REF ? 'warn' : 'fail',
            zh: process.env.EXECUTION_SIGNER_REF
                ? '检测到执行签名器引用（需进一步审计权限边界）。'
                : '未检测到执行签名器控制面（HSM/MPC/KMS）。',
            en: process.env.EXECUTION_SIGNER_REF
                ? 'Execution signer reference detected (permission boundaries still need audit).'
                : 'No signer control-plane detected (HSM/MPC/KMS).',
            actionZh: '生产执行前需引入托管签名、密钥轮换与最小权限策略。',
            actionEn: 'Before live execution, add managed signing, key rotation, and least-privilege controls.',
        },
        {
            key: 'compliance_docs',
            status: existingDocs.length === requiredDocs.length ? 'pass' : (existingDocs.length > 0 ? 'warn' : 'fail'),
            zh: `合规文档覆盖 ${existingDocs.length}/${requiredDocs.length}。`,
            en: `Compliance document coverage ${existingDocs.length}/${requiredDocs.length}.`,
            actionZh: '补齐风控披露、服务条款、辖区合规策略，并完成法律审核。',
            actionEn: 'Complete risk disclosure, terms, jurisdiction policy, and legal review.',
        },
        {
            key: 'audit_trail',
            status: context.totalTransactions > 0 ? 'pass' : 'warn',
            zh: `当前交易记录 ${context.totalTransactions} 条。`,
            en: `Current transaction records: ${context.totalTransactions}.`,
            actionZh: '上线前确保交易日志可追溯（签名、失败原因、通知记录）。',
            actionEn: 'Ensure full traceability (signatures, failure reasons, notification logs) before go-live.',
        },
    ];

    const readinessScore = checks.length === 0
        ? 0
        : Math.round((checks.reduce((sum, item) => sum + statusWeight(item.status), 0) / checks.length) * 100);

    return {
        checks,
        readinessScore,
        existingDocs,
        requiredDocs,
    };
}

function printText(result, context) {
    console.log(isZh ? '🧭 执行模式评估（模拟 -> 真实）' : '🧭 Execution Mode Evaluation (Simulation -> Live)');
    console.log(`${isZh ? '准备度评分' : 'Readiness Score'}: ${result.readinessScore}/100`);
    console.log(`${isZh ? '用户数' : 'Users'}: ${context.totalUsers} | ${isZh ? '活跃策略' : 'Active Strategies'}: ${context.activeStrategies} | ${isZh ? '活跃警报' : 'Active Alerts'}: ${context.activeAlerts}`);
    console.log('');

    for (const item of result.checks) {
        console.log(`${statusBadge(item.status)} ${isZh ? item.zh : item.en}`);
        console.log(`   ${isZh ? '下一步' : 'Next'}: ${isZh ? item.actionZh : item.actionEn}`);
    }

    console.log('');
    console.log(isZh ? '📌 合规推进路径（建议）:' : '📌 Recommended Compliance Path:');
    console.log(isZh ? '1) 治理与法务：明确目标辖区、牌照边界、风险披露文本。' : '1) Governance & legal: define jurisdictions, licensing boundaries, and risk disclosures.');
    console.log(isZh ? '2) 技术与控制：引入签名器控制面、额度与熔断风控、异常告警。' : '2) Technical controls: add signer control-plane, limits/circuit-breakers, and alerting.');
    console.log(isZh ? '3) 小规模灰度：仅白名单用户 + 低限额 + 人工复核。' : '3) Limited pilot: whitelist-only users, low limits, and manual review.');
    console.log(isZh ? '4) 正式上线：分阶段放量并持续审计。' : '4) Production rollout: phased scaling with continuous audits.');
    console.log('');
    console.log(isZh
        ? '⚠️ 说明：本评估仅用于工程与运营准备，不构成法律意见。'
        : '⚠️ Note: This evaluation is for engineering/operations readiness and is not legal advice.');
}

function main() {
    try {
        initDatabase();
        const context = {
            totalUsers: count('SELECT COUNT(*) AS count FROM users'),
            activeStrategies: count("SELECT COUNT(*) AS count FROM dca_strategies WHERE status = 'active'"),
            activeAlerts: count('SELECT COUNT(*) AS count FROM price_alerts WHERE is_active = 1'),
            totalTransactions: count('SELECT COUNT(*) AS count FROM transactions'),
        };
        const result = evaluateChecks(context);

        if (asJson) {
            console.log(JSON.stringify({
                generatedAt: new Date().toISOString(),
                network: config.solanaNetwork,
                context,
                ...result,
            }, null, 2));
            return;
        }

        printText(result, context);
    } catch (err) {
        console.log(`❌ ${formatError(err.code || 'INTERNAL_ERROR', lang)}`);
        process.exit(1);
    }
}

main();
