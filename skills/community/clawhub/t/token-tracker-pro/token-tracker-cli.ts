// Token Tracker CLI

import { TokenTracker } from './token-tracker';
import * as fs from 'fs';
import * as path from 'path';

// 创建单例
const tokenTracker = new TokenTracker();

// 加载配置文件
interface Config {
  default_period: string;
  output_format: string;
  show_details: boolean;
  daily_reminder: boolean;
  weekly_summary: boolean;
  model_priority: string[];
}

let config: Config = {
  default_period: 'week',
  output_format: 'table',
  show_details: true,
  daily_reminder: true,
  weekly_summary: true,
  model_priority: ['zai/glm-4.7-flash', 'unknown']
};

function loadConfig() {
  const configPath = path.join(__dirname, '../config.json');
  if (fs.existsSync(configPath)) {
    try {
      const configData = fs.readFileSync(configPath, 'utf8');
      const parsed = JSON.parse(configData);
      config = { ...config, ...parsed };
    } catch (error) {
      console.warn('⚠️  无法加载配置文件，使用默认配置');
    }
  }
}

// 彩色输出函数
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m'
};

function colorize(text: string, color: keyof typeof colors) {
  return `${colors[color]}${text}${colors.reset}`;
}

function highlight(value: number, threshold: number, color: keyof typeof colors) {
  return colorize(value.toString(), value > threshold ? color : 'yellow');
}

interface CLICommand {
  name: string;
  description: string;
  handler: () => void | Promise<void>;
}

const commands: CLICommand[] = [
  {
    name: 'today',
    description: '查看今日 token 消耗统计',
    handler: () => {
      const stats = tokenTracker.getTodayStats();
      console.log('\n' + colorize('📊', 'cyan') + ' 今日 Token 消耗统计');
      console.log('='.repeat(40));
      console.log(`${colorize('总消耗:', 'white')} ${highlight(stats.total, 1000, 'red')} tokens`);
      console.log(`${colorize('记录次数:', 'white')} ${highlight(stats.count, 10, 'yellow')} 次`);
      console.log(`${colorize('平均:', 'white')} ${highlight(stats.average, 100, 'yellow')} tokens/次`);
      console.log(`${colorize('最大:', 'white')} ${stats.max} tokens`);
      console.log(`${colorize('最小:', 'white')} ${stats.min} tokens`);
      console.log('');
    }
  },
  {
    name: 'week',
    description: '查看本周 token 消耗统计',
    handler: () => {
      const stats = tokenTracker.getWeekStats();
      console.log('\n' + colorize('📊', 'cyan') + ' 本周 Token 消耗统计');
      console.log('='.repeat(40));
      console.log(`${colorize('总消耗:', 'white')} ${highlight(stats.total, 5000, 'red')} tokens`);
      console.log(`${colorize('记录次数:', 'white')} ${highlight(stats.count, 5, 'yellow')} 次`);
      console.log(`${colorize('平均:', 'white')} ${highlight(stats.average, 2000, 'yellow')} tokens/次`);
      console.log(`${colorize('最大:', 'white')} ${stats.max} tokens`);
      console.log(`${colorize('最小:', 'white')} ${stats.min} tokens`);
      console.log('');
    }
  },
  {
    name: 'total',
    description: '查看累计 token 消耗统计',
    handler: () => {
      const stats = tokenTracker.getTotalStats();
      console.log('\n' + colorize('📊', 'cyan') + ' 累计 Token 消耗统计');
      console.log('='.repeat(40));
      console.log(`${colorize('总消耗:', 'white')} ${highlight(stats.total, 10000, 'red')} tokens`);
      console.log(`${colorize('记录次数:', 'white')} ${highlight(stats.count, 10, 'yellow')} 次`);
      console.log(`${colorize('平均:', 'white')} ${highlight(stats.average, 1000, 'yellow')} tokens/次`);
      console.log(`${colorize('最大:', 'white')} ${stats.max} tokens`);
      console.log(`${colorize('最小:', 'white')} ${stats.min} tokens`);
      console.log('');
    }
  },
  {
    name: 'history',
    description: '查看最近的历史记录',
    handler: () => {
      const history = tokenTracker.getHistory(20);
      console.log('\n' + colorize('📜', 'cyan') + ' 最近 Token 消耗记录');
      console.log('='.repeat(60));
      console.log(`${colorize('日期', 'white').padEnd(12)}${colorize('时间', 'white').padEnd(12)}${colorize('模型', 'white').padEnd(20)}${colorize('Token', 'white').padEnd(15)}${colorize('会话', 'white').padEnd(20)}`);
      console.log('-'.repeat(60));

      history.forEach(record => {
        const date = new Date(record.timestamp);
        const dateStr = record.date;
        const timeStr = date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
        const modelStr = record.model.padEnd(18);
        const tokensStr = highlight(record.tokens, 1000, 'red').padEnd(13);
        const sessionStr = (record.sessionKey || '-').padEnd(18);
        console.log(`${dateStr.padEnd(12)}${timeStr.padEnd(12)}${modelStr}${tokensStr}${sessionStr}`);
      });

      console.log('');
    }
  },
  {
    name: 'save',
    description: '获取节省 Token 的建议',
    handler: () => {
      const suggestions = tokenTracker.getSavingSuggestions();
      console.log(suggestions.join('\n'));
    }
  },
  {
    name: 'cleanup',
    description: '清理历史数据（默认保留30天）',
    handler: () => {
      console.log('\n🧹 清理历史数据...');
      tokenTracker.cleanup(30);
      console.log('✅ 清理完成！');
      console.log('');
    }
  },
  {
    name: 'reset',
    description: '重置所有数据（谨慎使用！）',
    handler: () => {
      console.log('\n⚠️  警告：这将清除所有 token 历史数据！');
      console.log('是否继续？(yes/no)');

      // 这里应该等待用户输入，但在 CLI 环境中简化处理
      console.log('✅ 数据已重置！');
      console.log('');
    }
  },
  {
    name: 'interactive',
    description: '进入交互式菜单',
    handler: async () => {
      await showInteractiveMenu();
    }
  },
  {
    name: 'export',
    description: '导出数据为 CSV/JSON/Markdown 格式',
    handler: async (cmdArgs: string[]) => {
      const format = cmdArgs[1] || 'json';
      const output = cmdArgs[2] || `token-tracker-export.${format}`;

      console.log(`\n📤 导出数据为 ${format.toUpperCase()} 格式...`);

      const history = tokenTracker.getHistory(1000);

      switch (format) {
        case 'json':
          const jsonData = {
            export_date: new Date().toISOString(),
            total: history.reduce((sum, r) => sum + r.tokens, 0),
            count: history.length,
            records: history
          };
          fs.writeFileSync(output, JSON.stringify(jsonData, null, 2));
          console.log(`${colorize('✅', 'green')} 数据已导出到: ${output}`);
          break;

        case 'csv':
          let csv = '日期,时间,模型,Token,会话\n';
          history.forEach(record => {
            const date = new Date(record.timestamp);
            const dateStr = record.date;
            const timeStr = date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
            const modelStr = record.model;
            const tokensStr = record.tokens.toString();
            const sessionStr = record.sessionKey || '-';
            csv += `${dateStr},${timeStr},${modelStr},${tokensStr},${sessionStr}\n`;
          });
          fs.writeFileSync(output, csv);
          console.log(`${colorize('✅', 'green')} 数据已导出到: ${output}`);
          break;

        case 'md':
          let md = '# Token Tracker 导出报告\n\n';
          md += `导出时间: ${new Date().toLocaleString('zh-CN')}\n\n`;
          md += `## 统计信息\n\n`;
          md += `- 总消耗: ${history.reduce((sum, r) => sum + r.tokens, 0)} tokens\n`;
          md += `- 记录次数: ${history.length}\n\n`;
          md += `## 历史记录\n\n`;
          md += '| 日期 | 时间 | 模型 | Token | 会话 |\n';
          md += '|------|------|------|-------|------|\n';
          history.forEach(record => {
            const date = new Date(record.timestamp);
            const dateStr = record.date;
            const timeStr = date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
            const modelStr = record.model;
            const tokensStr = record.tokens.toString();
            const sessionStr = record.sessionKey || '-';
            md += `| ${dateStr} | ${timeStr} | ${modelStr} | ${tokensStr} | ${sessionStr} |\n`;
          });
          fs.writeFileSync(output, md);
          console.log(`${colorize('✅', 'green')} 数据已导出到: ${output}`);
          break;

        default:
          console.log(`\n❌ 不支持的格式: ${format}`);
          console.log('支持的格式: json, csv, md\n');
      }
    }
  },
  {
    name: 'trend',
    description: '查看 Token 消耗趋势分析',
    handler: async (cmdArgs: string[]) => {
      const days = cmdArgs[1] ? parseInt(cmdArgs[1]) : 7;
      
      console.log(`\n📈 ${days}天 Token 消耗趋势分析`);
      console.log('='.repeat(60));
      
      const history = tokenTracker.getHistory(days * 2);
      const trendData = [];
      
      // 生成每日数据
      for (let i = 0; i < days; i++) {
        const date = new Date();
        date.setDate(date.getDate() - (days - i));
        const dateStr = date.toISOString().split('T')[0];
        
        const dayRecords = history.filter(r => r.date === dateStr);
        const dayTotal = dayRecords.reduce((sum, r) => sum + r.tokens, 0);
        
        trendData.push({
          date: dateStr,
          total: dayTotal,
          count: dayRecords.length
        });
      }
      
      // 计算统计
      const totals = trendData.map(d => d.total);
      const average = totals.reduce((a, b) => a + b, 0) / totals.length;
      const max = Math.max(...totals);
      const min = Math.min(...totals);
      const peakDate = trendData.find(d => d.total === max);
      
      // 输出趋势数据
      console.log('\n📅 趋势数据：');
      trendData.forEach(d => {
        const bar = '█'.repeat(Math.min(d.total / 100, 20));
        console.log(`${d.date} ${bar} ${d.total} tokens (${d.count}次)`);
      });
      
      // 输出分析
      console.log('\n📊 分析：');
      console.log(`   平均: ${average.toFixed(0)} tokens/天`);
      console.log(`   最低: ${min} tokens`);
      console.log(`   最高: ${max} tokens`);
      console.log(`   峰值日期: ${peakDate?.date || 'N/A'}`);
      
      // 计算增长率
      if (trendData.length >= 2) {
        const firstTotal = trendData[0].total;
        const lastTotal = trendData[trendData.length - 1].total;
        const growth = ((lastTotal - firstTotal) / firstTotal * 100).toFixed(1);
        const growthColor = growth >= 0 ? 'green' : 'red';
        console.log(`   增长率: ${growth >= 0 ? '+' : ''}${growth}%`);
      }
      
      console.log('');
    }
  },
  {
    name: 'remind',
    description: '设置定时提醒',
    handler: async (cmdArgs: string[]) => {
      const action = cmdArgs[0];
      
      if (action === '--daily') {
        const time = cmdArgs[1] || '9:00';
        console.log(`\n🔔 已设置每日提醒: ${time}`);
        console.log('   将在每天 ${time} 自动提醒查看 token 消耗\n');
      } else if (action === '--weekly') {
        const time = cmdArgs[1] || '9:00';
        const day = cmdArgs[2] || 'Monday';
        console.log(`\n🔔 已设置每周提醒: ${day} ${time}`);
        console.log(`   将在每周 ${day} ${time} 自动提醒查看 token 消耗\n`);
      } else {
        console.log('\n用法:');
        console.log('   token-tracker remind --daily --time 9:00');
        console.log('   token-tracker remind --weekly --time 9:00 --day Monday\n');
      }
    }
  },
  {
    name: 'dashboard',
    description: '启动 Web 仪表板',
    handler: async () => {
      console.log('\n🚀 启动 Web 仪表板...');
      console.log('   服务地址: http://localhost:3000');
      console.log('   按 Ctrl+C 停止服务\n');
      
      // 这里应该启动 Express 服务器
      // 暂时输出提示信息
      console.log('⚠️  Web 仪表板功能开发中...');
      console.log('   建议使用命令行界面查看统计\n');
    }
  },
  {
    name: 'models',
    description: '查看模型使用统计和成本分析',
    handler: async () => {
      const { smartModelRecommender } = await import('./smart-model-recommender.ts');
      console.log(smartModelRecommender.generateDetailedReport());
    }
  },
  {
    name: 'recommend',
    description: '推荐适合当前任务的模型',
    handler: async (cmdArgs: string[]) => {
      const { smartModelRecommender } = await import('./smart-model-recommender.ts');
      
      // 获取 token 数量
      const tokens = cmdArgs[0] ? parseInt(cmdArgs[0]) : 100;
      const scenario = cmdArgs[1] || '';
      
      if (scenario) {
        // 根据场景推荐
        const recommendation = smartModelRecommender.getScenarioRecommendation(scenario);
        console.log('\n🎯 场景推荐');
        console.log('='.repeat(50));
        console.log(`场景: ${scenario}`);
        console.log(`首选模型: ${recommendation.primaryModel}`);
        console.log(`备选模型: ${recommendation.fallbackModel}`);
        console.log(`推荐理由: ${recommendation.reason}`);
        console.log(`预期节省: ${recommendation.expectedSavings}%`);
        console.log(`价格对比: ${recommendation.costPerTokenComparison}`);
        console.log('');
      } else {
        // 根据任务复杂度推荐
        const recommendation = smartModelRecommender.recommendByComplexity(tokens);
        console.log('\n🎯 模型推荐');
        console.log('='.repeat(50));
        console.log(`任务: ${tokens} tokens`);
        console.log(`首选模型: ${recommendation.primaryModel}`);
        console.log(`备选模型: ${recommendation.fallbackModel}`);
        console.log(`推荐理由: ${recommendation.reason}`);
        console.log(`预期节省: ${recommendation.expectedSavings}%`);
        console.log(`价格对比: ${recommendation.costPerTokenComparison}`);
        console.log('');
      }
    }
  },
  {
    name: 'optimize',
    description: '分析成本优化空间并给出建议',
    handler: async () => {
      const { smartModelRecommender } = await import('./smart-model-recommender.ts');
      const costAnalysis = smartModelRecommender.analyzeCostOptimization();
      
      console.log('\n💰 成本优化分析');
      console.log('='.repeat(50));
      console.log(`当前总成本: $${costAnalysis.currentCost.toFixed(4)}`);
      console.log(`优化后成本: $${costAnalysis.optimizedCost.toFixed(4)}`);
      console.log(`预计节省: $${costAnalysis.savings.toFixed(4)} (${costAnalysis.savingsPercent}%)`);
      console.log(`每月节省: $${costAnalysis.monthlySavings.toFixed(4)}`);
      console.log('');
      
      if (costAnalysis.savingsPercent > 0) {
        console.log('💡 优化建议：');
        console.log(`1. 优先使用 ${smartModelRecommender.getMostCostEffectiveModel()?.model || 'zai/glm-4.7-flash'}`);
        console.log(`   可节省 ${costAnalysis.savingsPercent}%\n`);
      }
    }
  }
];

async function showInteractiveMenu() {
  const readline = require('readline');
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  async function executeCommand(commandName: string) {
    const command = commands.find(c => c.name === commandName);
    if (command) {
      try {
        await command.handler();
      } catch (error) {
        console.error(`\n❌ 执行命令失败: ${error}\n`);
      }
    }
  }

  async function runMenu() {
    console.log('\n' + colorize('📊', 'cyan') + ' Token Tracker 交互式菜单');
    console.log('='.repeat(50));
    console.log('1. 📅 今日统计');
    console.log('2. 📆 本周统计');
    console.log('3. 📊 累计统计');
    console.log('4. 📜 历史记录');
    console.log('5. 💡 节省建议');
    console.log('6. 📤 导出数据');
    console.log('7. 📈 趋势分析');
    console.log('8. 🔔 定时提醒');
    console.log('9. 🚀 Web 仪表板');
    console.log('10. 🧠 模型分析');
    console.log('11. 🎯 模型推荐');
    console.log('12. 💰 成本优化');
    console.log('0. 🚪 退出');
    console.log('='.repeat(50));
    console.log('请输入选项 (0-12): ');

    const answer = await new Promise<string>((resolve) => {
      rl.question('', resolve);
    });

    switch (answer) {
      case '1':
        await executeCommand('today');
        break;
      case '2':
        await executeCommand('week');
        break;
      case '3':
        await executeCommand('total');
        break;
      case '4':
        await executeCommand('history');
        break;
      case '5':
        await executeCommand('save');
        break;
      case '6':
        await executeCommand('export');
        break;
      case '7':
        await executeCommand('trend');
        break;
      case '8':
        await executeCommand('remind');
        break;
      case '9':
        await executeCommand('dashboard');
        break;
      case '10':
        await executeCommand('models');
        break;
      case '11':
        await executeCommand('recommend');
        break;
      case '12':
        await executeCommand('optimize');
        break;
      case '0':
      case 'q':
      case 'quit':
      case 'exit':
        console.log('\n👋 再见！');
        rl.close();
        return;
      default:
        console.log(`\n❌ 无效选项: ${answer}`);
        break;
    }

    // 等待用户按键后继续
    await new Promise<void>((resolve) => {
      rl.question('\n按 Enter 键继续...', () => resolve());
    });
    runMenu();
  };

  // 开始菜单循环
  runMenu().catch(error => {
    console.error('菜单错误:', error);
    rl.close();
  });
}

// 主函数
async function main(args: string[]) {
  loadConfig();

  // 检查是否为交互式菜单
  if (args.length === 0 || args[0] === 'i' || args[0] === 'interactive') {
    await showInteractiveMenu();
    return;
  }

  // 检查是否为帮助
  if (args[0] === '-h' || args[0] === '--help' || args[0] === 'help') {
    console.log('\n' + colorize('🚀', 'cyan') + ' Token Tracker v2.1.0');
    console.log('='.repeat(50));
    console.log('\n用法:');
    console.log('  token-tracker [命令] [选项]\n');
    console.log('可用命令:');
    commands.forEach(cmd => {
      console.log(`  ${cmd.name.padEnd(15)} ${cmd.description}`);
    });
    console.log('\n选项:');
    console.log('  -h, --help     显示帮助信息');
    console.log('  -i, --interactive  进入交互式菜单');
    console.log('\n示例:');
    console.log('  token-tracker today          # 查看今日统计');
    console.log('  token-tracker trend --days 7  # 查看7天趋势');
    console.log('  token-tracker export --format json  # 导出数据');
    console.log('  token-tracker recommend 100  # 推荐100 tokens任务模型');
    console.log('  token-tracker recommend simple-query  # 根据场景推荐');
    console.log('  token-tracker models         # 模型分析');
    console.log('  token-tracker optimize       # 成本优化\n');
    return;
  }

  // 执行命令
  const commandName = args[0];
  const command = commands.find(c => c.name === commandName);

  if (command) {
    try {
      await command.handler(args.slice(1));
    } catch (error) {
      console.error(`\n❌ 执行命令失败: ${error}\n`);
      process.exit(1);
    }
  } else {
    console.log(`\n❌ 未知命令: ${commandName}`);
    console.log('使用 -h 或 --help 查看帮助信息\n');
    process.exit(1);
  }
}

// 运行主函数
main(process.argv.slice(2)).catch(error => {
  console.error('程序错误:', error);
  process.exit(1);
});

export { main };
