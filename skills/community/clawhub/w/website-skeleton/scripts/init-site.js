#!/usr/bin/env node
/**
 * init-site.js — 交互式网站初始化
 * 引导用户选择模板、配置环境变量、执行迁移
 *
 * 用法：
 *   node scripts/init-site.js
 *
 * 模板数据从 templates/*.json 读取，实现模板联动。
 * 依赖：Node.js 18+ 内置 readline 模块（无需外部依赖）
 */

import { createInterface } from 'node:readline';
import { stdin, stdout } from 'node:process';
import { existsSync, readFileSync, mkdirSync, appendFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT = resolve(__dirname, '..');

// ──────────────────────────────────────────────
// 读取模板文件
// ──────────────────────────────────────────────

const TEMPLATE_FILES = ['e-commerce.json', 'ai-assistant.json', 'saas-admin.json'];

function loadTemplates() {
  return TEMPLATE_FILES.map((f) => {
    const filePath = resolve(ROOT, 'templates', f);
    if (!existsSync(filePath)) {
      console.error('\u26a0\ufe0f  模板文件不存在: ' + filePath);
      return null;
    }
    return JSON.parse(readFileSync(filePath, 'utf-8'));
  }).filter(Boolean);
}

// ──────────────────────────────────────────────
// 辅助函数
// ──────────────────────────────────────────────

function readline(question) {
  return new Promise((resolve) => {
    const rl = createInterface({ input: stdin, output: stdout });
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

function readchoice(question, options, defaultIdx = 0) {
  const labels = options.map((o, i) => '  ' + (i + 1) + ') ' + o);
  const prompt = '\n' + question + '\n' + labels.join('\n') + '\n\n请选择 (1-' + options.length + ', 默认 ' + (defaultIdx + 1) + '): ';
  return readline(prompt).then((answer) => {
    const num = parseInt(answer, 10);
    if (num >= 1 && num <= options.length) return num;
    return defaultIdx + 1;
  });
}

function confirm(question, defaultYes = true) {
  const hint = defaultYes ? '[Y/n]' : '[y/N]';
  return readline(question + ' ' + hint + ': ').then((answer) => {
    const a = answer.toLowerCase();
    if (a === 'y' || a === 'yes') return true;
    if (a === 'n' || a === 'no') return false;
    return defaultYes;
  });
}

function printBanner() {
  console.log([
    '',
    '\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557',
    '\u2551        \U0001f680 网站骨架 — 交互式初始化向导           \u2551',
    '\u2551     Website Skeleton — Interactive Setup         \u2551',
    '\u2551        EdgeOne Pages 全栈网站快速启动             \u2551',
    '\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d',
    '',
  ].join('\n'));
}

// ──────────────────────────────────────────────
// 根据模板构建默认功能配置
// ──────────────────────────────────────────────

function buildFeaturesFromTemplate(template) {
  const layer1 = template.layer1 || {};
  const layer2 = template.layer2 || {};

  return {
    auth:         layer1.auth === true,
    aiChat:       layer1.aiChat === true,
    admin:        layer1.admin === true,
    cart:         layer1.cart === true,
    payment:      layer1.payment === true,
    orders:       layer1.orders === true,
    notification: layer2.notification === true,
    seo:          layer2.seo === true,
    analytics:    layer2.analytics === true,
    i18n:         layer2.i18n === true,
  };
}

// ──────────────────────────────────────────────
// .env 生成
// ──────────────────────────────────────────────

function generateEnv(data) {
  const dbLines = data.database === 'D1'
    ? 'DB_TYPE=d1\nDB_NAME=' + data.projectName + '-db'
    : 'DB_TYPE=mysql\nDB_HOST=localhost\nDB_PORT=3306\nDB_NAME=' + data.projectName + '\nDB_USER=root\nDB_PASSWORD=';

  const aiLines = data.features.aiChat
    ? 'OPENAI_API_KEY=\nAI_MODEL=gpt-4o-mini'
    : '# AI features disabled';

  const lines = [
    '# ====================================================',
    '# 网站骨架 — 自动生成 .env 配置',
    '# 生成时间: ' + new Date().toISOString(),
    '# ====================================================',
    '',
    '# -- 项目 --',
    'PROJECT_NAME="' + data.projectName + '"',
    'DOMAIN="' + data.domain + '"',
    'APP_ENV=production',
    '',
    '# -- 数据库 --',
    dbLines,
    '',
    '# -- 功能开关 --',
    'ENABLE_AUTH=' + data.features.auth,
    'ENABLE_AI_CHAT=' + data.features.aiChat,
    'ENABLE_ADMIN=' + data.features.admin,
    'ENABLE_CART=' + data.features.cart,
    'ENABLE_PAYMENT=' + data.features.payment,
    'ENABLE_ORDERS=' + data.features.orders,
    'ENABLE_SEO=' + data.features.seo,
    'ENABLE_ANALYTICS=' + data.features.analytics,
    'ENABLE_NOTIFICATION=' + data.features.notification,
    'ENABLE_I18N=' + data.features.i18n,
    '',
    '# -- Auth --',
    'JWT_SECRET=change-me-to-a-random-string',
    'JWT_EXPIRES_IN=7d',
    '',
    '# -- AI Chat (可选) --',
    aiLines,
    '',
    '# -- 模板 --',
    'SITE_TEMPLATE="' + data.template + '"',
  ];
  return lines.join('\n');
}

function writeEnv(data) {
  const envPath = resolve(ROOT, '.env');
  const content = generateEnv(data);
  const dir = dirname(envPath);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  appendFileSync(envPath, content + '\n');
  console.log('\n\u2705 .env 配置文件已写入: ' + envPath);
}

// ──────────────────────────────────────────────
// 功能开关交互确认
// ──────────────────────────────────────────────

async function confirmFeatures(features, template) {
  console.log('\n\u2500\u2500 功能模块配置 (模板: ' + template.label + ') \u2500\u2500');
  console.log('模板推荐的功能已自动勾选，如需调整请逐一确认:\n');

  const featureList = [
    { key: 'auth',         label: '用户认证 (Auth)' },
    { key: 'admin',        label: '管理后台 (Admin)' },
    { key: 'aiChat',       label: 'AI 聊天 (AI Chat)' },
    { key: 'cart',         label: '购物车 (Cart)' },
    { key: 'payment',      label: '支付 (Payment)' },
    { key: 'orders',       label: '订单管理 (Orders)' },
    { key: 'seo',          label: 'SEO 优化' },
    { key: 'analytics',    label: '网站分析 (Analytics)' },
    { key: 'notification', label: '通知 (Notification)' },
    { key: 'i18n',         label: '国际化 (i18n)' },
  ];

  const result = { ...features };
  for (const f of featureList) {
    const current = result[f.key];
    result[f.key] = await confirm('  ' + f.label + '？', current);
  }

  return result;
}

// ──────────────────────────────────────────────
// 主流程
// ──────────────────────────────────────────────

async function main() {
  printBanner();

  // 1. 加载模板
  const templates = loadTemplates();
  if (templates.length === 0) {
    console.error('\u274c 未找到任何模板文件 (templates/*.json)');
    process.exit(1);
  }

  // 2. 选择模板 — 使用模板 JSON 中的 label 和 description
  const templateOptions = templates.map((t) => '\U0001f6d2 ' + t.label + ' - ' + t.description);
  const templateChoice = await readchoice('请选择网站模板:', templateOptions);
  const selectedTemplate = templates[templateChoice - 1];

  console.log('\n\u2705 已选择模板: ' + selectedTemplate.label + ' (' + selectedTemplate.labelEn + ')');

  // 3. 项目基本信息
  const projectName = await readline('请输入项目名称 (默认: my-site): ') || 'my-site';
  const domain = await readline('请输入域名 (默认: my-site.example.com): ') || 'my-site.example.com';

  // 4. 从模板自动配置功能开关，让用户确认
  let features = buildFeaturesFromTemplate(selectedTemplate);
  features = await confirmFeatures(features, selectedTemplate);

  // 5. 数据库选择
  const dbChoice = await readchoice('请选择数据库:', ['D1 (SQLite — EdgeOne Pages 内置)', 'MySQL']);
  const database = dbChoice === 1 ? 'D1' : 'MySQL';
  console.log('\n\u2705 已选择数据库: ' + database);

  // 6. 生成配置
  const config = {
    projectName,
    domain,
    template: selectedTemplate.name,
    templateLabel: selectedTemplate.label,
    features,
    database,
  };

  console.log('\n\u2500\u2500 配置摘要 \u2500\u2500');
  console.log(JSON.stringify(config, null, 2));

  const ok = await confirm('\n确认以上配置？', true);
  if (!ok) {
    console.log('\n\u274c 已取消。请重新运行脚本。');
    process.exit(1);
  }

  // 7. 写入 .env
  writeEnv(config);

  // 8. 后续步骤提示
  console.log([
    '',
    '\\u2554\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2550\\u2557',
    '\\u2551           \\U0001f4cb 后续步骤                            \\u2551',
    '\u2551                                                   \u2551',
    '\u2551   1\ufe0f\u20e3  配置数据库连接（编辑 .env 文件）           \u2551',
    '\u2551                                                   \u2551',
    '\u2551   2\ufe0f\u20e3  执行数据库迁移:                            \u2551',
    '\u2551       $ node scripts/migrate.js                   \u2551',
    '\u2551       # 或: $ node scripts/migrate.js --db mysql  \u2551',
    '\u2551                                                   \u2551',
    '\u2551   3\ufe0f\u20e3  导入种子数据:                              \u2551',
    '\u2551       $ node scripts/sample-data.js > db/seed.sql \u2551',
    '\u2551       $ node scripts/sample-data.js --hash-passwords > db/seed.sql \u2551',
    '\u2551                                                   \u2551',
    '\u2551   4\ufe0f\u20e3  本地开发:                                   \u2551',
    '\u2551       $ npm run dev                               \u2551',
    '\u2551                                                   \u2551',
    '\u2551   5\ufe0f\u20e3  部署到 EdgeOne Pages:                       \u2551',
    '\u2551       $ edgeone pages deploy .                    \u2551',
    '\u2551                                                   \u2551',
    '\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d',
    '',
  ].join('\n'));

  console.log('\U0001f389 初始化完成！祝编码愉快！');
}

main().catch((err) => {
  console.error('\u274c 初始化失败:', err.message);
  process.exit(1);
});
