#!/usr/bin/env node
/**
 * Token省钱管家 - CLI 工具
 */
const TokenCostController = require('./lib/index');

const controller = new TokenCostController();

const args = process.argv.slice(2);
const command = args[0];

async function main() {
  switch (command) {
    case 'report':
      console.log(JSON.stringify(controller.getReport(), null, 2));
      break;

    case 'top-skills':
      console.log('Top 消耗技能:');
      controller.getReport().topSkills.forEach((s, i) => {
        console.log(`${i + 1}. ${s.skill}: $${s.avgCost}/次 (${s.samples}次)`);
      });
      break;

    case 'alerts':
      const alerts = controller.getReport().alerts;
      if (alerts.length === 0) {
        console.log('暂无异常告警');
      } else {
        alerts.forEach(a => {
          console.log(`[${a.severity}] ${a.skill}: $${a.cost} (平时 $${a.avg}, 涨幅 ${a.spike})`);
        });
      }
      break;

    case 'controls':
      const ctrl = controller.getReport().controls;
      console.log('管控状态:');
      console.log('禁用技能:', ctrl.disabledSkills.length ? ctrl.disabledSkills.join(', ') : '无');
      console.log('暂停计划:', ctrl.pausedPlans.length ? ctrl.pausedPlans.join(', ') : '无');
      break;

    case 'disable-skill':
      if (args[1]) {
        console.log(controller.disableSkill(args[1]));
      } else {
        console.log('用法: disable-skill <技能名>');
      }
      break;

    case 'set-cost':
      if (args[1] && args[2]) {
        console.log(controller.setMaxCost(args[1], parseFloat(args[2])));
      } else {
        console.log('用法: set-cost <技能名> <最大金额>');
      }
      break;

    case 'cache':
      console.log('缓存统计:', controller.getReport().cache);
      break;

    default:
      console.log(`
Token省钱管家 CLI

用法:
  token-cost-controller report       - 查看成本报告
  token-cost-controller top-skills   - 查看Top消耗技能
  token-cost-controller alerts       - 查看异常告警
  token-cost-controller controls     - 查看管控状态
  token-cost-controller disable-skill <名> - 禁用技能
  token-cost-controller set-cost <名> <$>- 设置成本上限
  token-cost-controller cache        - 查看缓存统计
`);
  }
}

main().catch(console.error);
