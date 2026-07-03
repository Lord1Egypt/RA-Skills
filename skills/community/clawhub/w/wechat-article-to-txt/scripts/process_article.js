#!/usr/bin/env node

/**
 * process_article.js - 微信公众号文章一键处理（抓取 + 总结 + 生成笔记 + 存入 vault）
 *
 * 用法: node process_article.js <article_url> [options]
 *
 * 选项:
 *   --dir, -d     <dir>     Obsidian 子目录（默认: 未分类）
 *   --tags, -t    <tags>    额外标签 (逗号分隔)
 *   --dry-run, -n           仅预览，不写入 vault
 *   --vault, -v   <path>    vault 路径（覆盖配置）
 *   --output, -o  <path>    输出到指定文件（不写入 vault）
 */

const fs = require('fs');
const path = require('path');
const { execSync, spawn } = require('child_process');

const SCRIPTS_DIR = __dirname;

// 读取配置
const configPath = path.join(SCRIPTS_DIR, 'config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

function parseArgs() {
  const args = process.argv.slice(2);
  const result = {
    url: null,
    dir: '未分类',
    tags: '',
    dryRun: false,
    vault: '',
    output: '',
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--dir': case '-d': result.dir = args[++i]; break;
      case '--tags': case '-t': result.tags = args[++i]; break;
      case '--dry-run': case '-n': result.dryRun = true; break;
      case '--vault': case '-v': result.vault = args[++i]; break;
      case '--output': case '-o': result.output = args[++i]; break;
      default:
        if (!args[i].startsWith('-')) result.url = args[i];
    }
  }
  return result;
}

/**
 * 运行子进程并返回 stdout
 */
function runScript(script, args, options = {}) {
  const scriptPath = path.join(SCRIPTS_DIR, script);
  const cmd = `${scriptPath} ${args}`;
  try {
    const result = execSync(cmd, {
      encoding: 'utf-8',
      timeout: 60000,
      ...options,
    });
    return result;
  } catch (err) {
    console.error(`❌ 脚本执行失败: ${script}`);
    console.error(err.stderr || err.message);
    throw err;
  }
}

/**
 * 使用 node 运行脚本
 */
function runNodeScript(script, args, options = {}) {
  const scriptPath = path.join(SCRIPTS_DIR, script);
  const cmd = ['node', scriptPath, ...args];
  try {
    const result = execSync(cmd.join(' '), {
      encoding: 'utf-8',
      timeout: 60000,
      ...options,
    });
    return result;
  } catch (err) {
    console.error(`❌ 脚本执行失败: ${script}`);
    console.error(err.stderr || err.message);
    throw err;
  }
}

/**
 * 获取 Obsidian vault 路径
 */
function getVaultPath(args) {
  if (args.vault) return args.vault;

  // 尝试从 Obsidian 配置读取
  const obsidianConfigPath = path.join(
    os.homedir(),
    'Library/Application Support/obsidian/obsidian.json'
  );

  if (fs.existsSync(obsidianConfigPath)) {
    try {
      const obsidianConfig = JSON.parse(fs.readFileSync(obsidianConfigPath, 'utf-8'));
      const vaults = obsidianConfig.vaults || {};
      for (const info of Object.values(vaults)) {
        if (info.open) return info.path;
      }
      return Object.values(vaults)[0]?.path || '';
    } catch (e) {
      // ignore
    }
  }
  return '';
}

async function main() {
  const args = parseArgs();

  if (!args.url) {
    console.error('❌ 请提供微信公众号文章链接');
    console.error('用法: node process_article.js <article_url> [options]');
    console.error('选项:');
    console.error('  --dir, -d   <dir>     Obsidian 子目录（默认: 未分类）');
    console.error('  --tags, -t  <tags>    额外标签 (逗号分隔)');
    console.error('  --dry-run, -n          仅预览，不写入 vault');
    console.error('  --vault, -v <path>     vault 路径');
    console.error('  --output, -o <path>    输出到指定文件');
    process.exit(1);
  }

  // ===================== 步骤1: 抓取文章 =====================
  console.error('\n📥 [1/4] 正在抓取文章...');
  const tmpDir = fs.mkdtempSync(path.join(require('os').tmpdir(), 'wechat-'));
  const articleJsonPath = path.join(tmpDir, 'article.json');

  let articleData;
  try {
    const result = runNodeScript('fetch_article.js', [
      `"${args.url}"`,
      '-o', `"${articleJsonPath}"`,
    ]);
    articleData = JSON.parse(fs.readFileSync(articleJsonPath, 'utf-8'));
    console.error(`   ✅ 标题: ${articleData.title}`);
    console.error(`   ✅ 公众号: ${articleData.author}`);
    console.error(`   ✅ 正文长度: ${articleData.contentText.length} 字`);
  } catch (err) {
    console.error('❌ 文章抓取失败，请检查链接是否正确');
    console.error('💡 也可以手动复制文章内容粘贴给我');
    process.exit(1);
  }

  // ===================== 步骤2: AI 总结（由 agent 在外部完成） =====================
  console.error('\n🧠 [2/4] 正在生成 AI 总结...');
  // 注意：AI 总结由 agent 自身能力完成
  // 此处只输出文章数据供 agent 处理
  console.error(`   ⏳ 等待 agent 进行 AI 总结...`);

  // 输出文章数据（供 agent 读取进行总结）
  console.log('---ARTICLE_DATA_START---');
  console.log(JSON.stringify({
    title: articleData.title,
    author: articleData.author,
    date: articleData.publishDate,
    url: articleData.url,
    content: articleData.contentText,
  }));
  console.log('---ARTICLE_DATA_END---');

  // ===================== 步骤3-4: 由 agent 在 SKILL 工作流中完成 =====================
  // 提示 agent 继续后续步骤
  console.error('\n📝 [3/4] 请根据上述文章内容进行多维度总结');
  console.error('💾 [4/4] 然后生成 Obsidian 笔记并存入 vault');
}

main().catch((err) => {
  console.error(`\n❌ 处理失败: ${err.message}`);
  process.exit(1);
});
