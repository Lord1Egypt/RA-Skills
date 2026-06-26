#!/usr/bin/env node
/**
 * 校验规则管理 CLI - 路由入口
 *
 * 用法（在 skill 目录下执行一次 npm install，之后）：
 *   npx vr <action> [--key value ...]
 *
 * 示例：
 *   npx vr create-rule --groupId 1 --ruleName "名称校验" --ruleCode CN-001 --objectId Invoice --countryCode CN --ruleType required
 *   npx vr query-scenes --status enabled
 *   npx vr enable-rule --id 42 --status disabled
 *   npx vr help
 */

const { parseArgs } = require('./lib/arg-parser');
const scenes     = require('./commands/scenes');
const ruleGroups = require('./commands/rule-groups');
const rules      = require('./commands/rules');

// 所有 action → handler 的统一路由表
const router = {
  ...scenes,
  ...ruleGroups,
  ...rules,
};

(async () => {
  const { action, params } = parseArgs(process.argv);

  if (!action || action === 'help' || action === '--help' || action === '-h') {
    printHelp();
    process.exit(0);
  }

  const handler = router[action];
  if (!handler) {
    console.error(`❌ 未知操作：${action}`);
    console.error(`   运行 npx vr help 查看全部可用操作`);
    process.exit(1);
  }

  try {
    await handler(params);
  } catch (e) {
    console.error(`\n❌ 执行失败：${e.message}`);
    process.exit(1);
  }
})();

function printHelp() {
  const domains = [
    { label: '规则组', cmds: Object.keys(ruleGroups) },
    { label: '规则',   cmds: Object.keys(rules) },
    { label: '场景',   cmds: Object.keys(scenes) },
  ];

  console.log('\n校验规则管理 CLI\n');
  console.log('用法：npx vr <action> [--key value ...]\n');
  console.log('可用操作：');
  for (const { label, cmds } of domains) {
    console.log(`  [${label}]  ${cmds.join('  ')}`);
  }
  console.log('\n参数格式：');
  console.log('  --key value         标准格式（推荐）');
  console.log('  --key=value         等号格式');
  console.log("  --json '{...}'      整体传入 JSON（含特殊字符时使用）");
  console.log('\n配置（任选其一）：');
  console.log('  环境变量：VALIDATE_BASE_URL=http://... VALIDATE_TOKEN=xxx npx vr ...');
  console.log('  config.json：{ "baseUrl": "...", "token": "...", "appId": "..." }');
  console.log();
}
