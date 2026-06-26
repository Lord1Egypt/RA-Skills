#!/usr/bin/env node
/**
 * Skill Discovery V3 - 主入口
 *
 * 完整功能：
 * - Phase 1: 基础封装（skills-cli.js）
 * - Phase 2: 自动化（auto-discover.js）
 * - Phase 3: 增强（openclaw-hook.js）
 */

const { skillsList, skillsFind, skillsAdd, skillsRemove } = require('./skills-cli');

const { analyzeNeed, autoDiscover } = require('./auto-discover');

const { onUserInput, generatePrompt, safeRemove, cleanTrash } = require('./openclaw-hook');

// ==================== 主函数 ====================

/**
 * 完整的 Skill Discovery 流程
 */
async function discoverAndInstall(userInput, options = {}) {
  const result = await autoDiscover(userInput, options);
  const prompt = generatePrompt(result);

  return {
    ...result,
    display: prompt
  };
}

// ==================== 导出 ====================
module.exports = {
  // Phase 1: CLI 封装
  skillsList,
  skillsFind,
  skillsAdd,
  skillsRemove,

  // Phase 2: 自动化
  analyzeNeed,
  autoDiscover,
  discoverAndInstall,

  // Phase 3: OpenClaw 集成
  onUserInput,
  generatePrompt,
  safeRemove,
  cleanTrash
};

// ==================== CLI 入口 ====================
if (require.main === module) {
  const args = process.argv.slice(2);

  // --help
  if (args.includes('--help') || args.includes('-h') || args.length === 0) {
    console.log(`
Skill Discovery - 自动发现并安装 skills

用法:
  skill-discovery "<query>" [options]

选项:
  --dry-run     模拟运行，不实际安装
  --json        以 JSON 格式输出结果
  --verbose     显示详细调试信息
  --help, -h    显示帮助信息

示例:
  skill-discovery "帮我部署到 Vercel" --dry-run
  skill-discovery "find a skill for testing" --json
  skill-discovery "优化 React 性能"

演示:
  node examples/demo.js
`);
    process.exit(0);
  }

  const dryRun = args.includes('--dry-run');
  const jsonOutput = args.includes('--json');
  const verbose = args.includes('--verbose');
  const query = args.filter((a) => !a.startsWith('--')).join(' ');

  if (!query) {
    console.error('错误: 请提供查询内容');
    process.exit(1);
  }

  (async () => {
    try {
      if (verbose) {
        console.log(`查询: "${query}"`);
        console.log(`选项: dryRun=${dryRun}, json=${jsonOutput}`);
      }

      const result = await discoverAndInstall(query, { dryRun });

      if (jsonOutput) {
        // JSON 输出（去掉 display 字段避免冗余）
        const { display: _display, ...data } = result;
        console.log(JSON.stringify(data, null, 2));
      } else if (result.display) {
        console.log('\n' + result.display);
      } else {
        console.log('\n[未触发自动发现]');
        if (verbose && result.confidence !== undefined) {
          console.log(`置信度: ${Math.round(result.confidence * 100)}%`);
        }
      }
    } catch (error) {
      console.error(`错误: ${error.message}`);
      process.exit(1);
    }
  })();
}
