#!/usr/bin/env node

/**
 * X to NotebookLM - 将 X (Twitter) 文章解析并上传到 NotebookLM
 * 
 * 使用方法:
 * node x-to-notebooklm.mjs <X 文章 URL> [选项]
 * 
 * 选项:
 *   --notebook-name <name>  指定 Notebook 名称（默认："X Articles"）
 *   --notebook-id <id>      使用现有 Notebook ID
 *   --verbose               详细输出模式
 *   --timeout <seconds>     超时时间（默认：30）
 *   --help                  显示帮助信息
 */

import { execSync } from 'child_process';
import { writeFileSync, unlinkSync, existsSync } from 'fs';
import { tmpdir } from 'os';
import { join } from 'path';

// 配置
const NOTEBOOKLM_CLI_PATH = process.env.NOTEBOOKLM_CLI_PATH || 
  `${process.env.HOME}/.openclaw/skills/tiangong-notebooklm-cli/scripts/notebooklm.mjs`;
const DEFAULT_NOTEBOOK_NAME = 'X Articles';
const DEFAULT_TIMEOUT = 30;

// 解析命令行参数
function parseArgs(args) {
  const options = {
    url: null,
    notebookName: process.env.NOTEBOOKLM_DEFAULT_NOTEBOOK || DEFAULT_NOTEBOOK_NAME,
    notebookId: null,
    verbose: process.env.X_TO_NOTEBOOKLM_VERBOSE === 'true',
    timeout: DEFAULT_TIMEOUT,
    help: false
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--help' || arg === '-h') {
      options.help = true;
    } else if (arg === '--verbose' || arg === '-v') {
      options.verbose = true;
    } else if (arg === '--notebook-name' && args[i + 1]) {
      options.notebookName = args[++i];
    } else if (arg === '--notebook-id' && args[i + 1]) {
      options.notebookId = args[++i];
    } else if (arg === '--timeout' && args[i + 1]) {
      options.timeout = parseInt(args[++i], 10);
    } else if (!arg.startsWith('-') && !options.url) {
      options.url = arg;
    }
  }

  return options;
}

// 显示帮助信息
function showHelp() {
  console.log(`
📖 X to NotebookLM - 将 X 文章解析并上传到 NotebookLM

使用方法:
  node x-to-notebooklm.mjs <X 文章 URL> [选项]

选项:
  --notebook-name <name>  指定 Notebook 名称（默认："X Articles"）
  --notebook-id <id>      使用现有 Notebook ID
  --verbose               详细输出模式
  --timeout <seconds>     超时时间（默认：30）
  --help                  显示帮助信息

示例:
  node x-to-notebooklm.mjs "https://x.com/elonmusk/status/1234567890"
  node x-to-notebooklm.mjs "https://x.com/..." --notebook-name "My Articles"
  node x-to-notebooklm.mjs "https://x.com/..." --notebook-id notebook_abc123
`);
}

// 执行命令并返回输出
function execCommand(command, timeout = 30) {
  try {
    const output = execSync(command, {
      encoding: 'utf-8',
      timeout: timeout * 1000,
      maxBuffer: 10 * 1024 * 1024 // 10MB
    });
    return { success: true, output: output.trim() };
  } catch (error) {
    return {
      success: false,
      error: error.message,
      output: error.stdout?.toString() || '',
      stderr: error.stderr?.toString() || ''
    };
  }
}

// 使用 r.jina.ai 抓取 X 文章内容
function fetchXContent(url, timeout = 30) {
  console.log('🕸️  正在抓取 X 文章内容...');
  
  const jinaUrl = `https://r.jina.ai/${url}`;
  const result = execCommand(`curl -s "${jinaUrl}"`, timeout);
  
  if (!result.success) {
    throw new Error(`抓取失败：${result.error}`);
  }
  
  const content = result.output;
  
  if (!content || content.length < 10) {
    throw new Error('抓取的内容为空或过短');
  }
  
  // 提取标题（第一行通常是标题）
  const lines = content.split('\n');
  let title = lines[0]?.trim() || 'X Article';
  
  // 清理标题中的特殊字符
  title = title.replace(/^[#*\s]+/, '').trim();
  if (title.length > 100) {
    title = title.substring(0, 97) + '...';
  }
  
  console.log(`📄 文章标题：${title}`);
  console.log(`📏 内容长度：${content.length} 字符`);
  
  return { title, content };
}

// 创建临时文件
function createTempFile(content, prefix = 'x-article') {
  const filename = `${prefix}-${Date.now()}.md`;
  const filepath = join(tmpdir(), filename);
  
  writeFileSync(filepath, content, 'utf-8');
  
  return filepath;
}

// 检查 NotebookLM CLI 是否可用
function checkNotebookLMCLI() {
  if (!existsSync(NOTEBOOKLM_CLI_PATH)) {
    throw new Error(`NotebookLM CLI 未找到：${NOTEBOOKLM_CLI_PATH}`);
  }
  
  const result = execCommand(`node "${NOTEBOOKLM_CLI_PATH}" status --json`, 10);
  
  if (!result.success) {
    throw new Error('NotebookLM CLI 未认证或不可用，请先运行：node ' + NOTEBOOKLM_CLI_PATH + ' login');
  }
  
  try {
    const status = JSON.parse(result.output);
    if (!status.authenticated) {
      throw new Error('NotebookLM CLI 未认证，请先运行登录命令');
    }
  } catch (e) {
    // 如果无法解析 JSON，可能是旧版本，继续尝试
  }
  
  console.log('✅ NotebookLM CLI 已就绪');
}

// 创建或获取 Notebook
function getOrCreateNotebook(notebookId, notebookName, timeout = 30) {
  if (notebookId) {
    console.log(`📓 使用现有 Notebook: ${notebookId}`);
    return { id: notebookId, created: false };
  }
  
  console.log(`📓 创建新 Notebook: ${notebookName}`);
  
  const result = execCommand(
    `node "${NOTEBOOKLM_CLI_PATH}" create "${notebookName}" --json`,
    timeout
  );
  
  if (!result.success) {
    throw new Error(`创建 Notebook 失败：${result.error}`);
  }
  
  // 解析 Notebook ID
  let notebookIdMatch;
  try {
    const notebook = JSON.parse(result.output);
    notebookIdMatch = notebook.id || notebook.notebookId;
  } catch (e) {
    // 尝试从输出中提取 ID
    const match = result.output.match(/notebook[_-]?[a-zA-Z0-9]+/i);
    notebookIdMatch = match ? match[0] : null;
  }
  
  if (!notebookIdMatch) {
    throw new Error('无法从响应中提取 Notebook ID');
  }
  
  console.log(`✅ Notebook 创建成功：${notebookIdMatch}`);
  
  return { id: notebookIdMatch, created: true };
}

// 上传文章到 Notebook
function uploadToNotebook(notebookId, content, title, timeout = 30) {
  console.log('📤 正在上传文章到 NotebookLM...');
  
  // 创建临时文件
  const tempFile = createTempFile(content);
  
  try {
    // 使用 source add 命令上传文件（不使用 --json，因为某些版本不支持）
    const result = execCommand(
      `node "${NOTEBOOKLM_CLI_PATH}" source add "${tempFile}" --notebook "${notebookId}"`,
      timeout
    );
    
    if (!result.success) {
      throw new Error(`上传失败：${result.error}`);
    }
    
    // 解析 Source ID - 尝试多种方式
    let sourceId = 'pending';
    
    // 方式 1: 尝试 JSON 解析
    try {
      const source = JSON.parse(result.output);
      sourceId = source.id || source.sourceId || sourceId;
    } catch (e) {
      // 方式 2: 尝试从输出中提取 UUID 格式的 ID
      const uuidMatch = result.output.match(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i);
      if (uuidMatch) {
        sourceId = uuidMatch[0];
      } else {
        // 方式 3: 尝试 source_xxx 格式
        const match = result.output.match(/source[_-]?[a-zA-Z0-9_-]+/i);
        if (match) {
          sourceId = match[0];
        }
      }
    }
    
    console.log(`✅ 上传成功，Source ID: ${sourceId}`);
    console.log(`📄 临时文件：${tempFile}`);
    
    return { sourceId, tempFile };
  } catch (error) {
    // 清理临时文件
    try {
      unlinkSync(tempFile);
    } catch (e) {}
    throw error;
  }
}

// 验证上传状态
function verifyUpload(notebookId, sourceId, timeout = 30) {
  console.log('🔍 正在验证上传状态...');
  
  // 如果 Source ID 是 pending 或 undefined，跳过验证
  if (!sourceId || sourceId === 'pending' || sourceId === 'undefined') {
    console.log('⏳ Source 正在处理中，请稍后在 NotebookLM 中查看');
    return { verified: false, status: 'processing' };
  }
  
  const result = execCommand(
    `node "${NOTEBOOKLM_CLI_PATH}" source get "${sourceId}"`,
    timeout
  );
  
  if (!result.success) {
    console.warn('⚠️  无法获取 Source 详情（可能是 CLI 版本不支持）');
    return { verified: false, status: 'unknown' };
  }
  
  // 尝试解析状态
  let status = 'processed';
  try {
    const source = JSON.parse(result.output);
    status = source.state || source.status || status;
  } catch (e) {
    // 从文本输出中提取状态
    if (result.output.toLowerCase().includes('processing')) {
      status = 'processing';
    } else if (result.output.toLowerCase().includes('error')) {
      status = 'error';
    } else if (result.output.toLowerCase().includes('success')) {
      status = 'success';
    }
  }
  
  console.log(`📊 解析状态：${status}`);
  
  return {
    verified: true,
    status: status,
    details: result.output
  };
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  const options = parseArgs(args);
  
  if (options.help || !options.url) {
    showHelp();
    if (!options.url) {
      console.error('❌ 错误：请提供 X 文章 URL');
      process.exit(1);
    }
    process.exit(0);
  }
  
  console.log('🚀 X to NotebookLM - 开始处理');
  console.log(`🔗 URL: ${options.url}`);
  console.log('');
  
  try {
    // 步骤 1: 检查 CLI
    checkNotebookLMCLI();
    
    // 步骤 2: 抓取内容
    const { title, content } = fetchXContent(options.url, options.timeout);
    
    // 步骤 3: 创建或获取 Notebook
    const notebook = getOrCreateNotebook(options.notebookId, options.notebookName, options.timeout);
    
    // 步骤 4: 上传文章
    const { sourceId } = uploadToNotebook(notebook.id, content, title, options.timeout);
    
    // 步骤 5: 验证上传
    const verification = verifyUpload(notebook.id, sourceId, options.timeout);
    
    // 输出结果
    console.log('');
    console.log('✅ X 文章解析上传成功');
    console.log('');
    console.log('📋 详细信息:');
    console.log(`  📄 文章标题：${title}`);
    console.log(`  🔗 原始链接：${options.url}`);
    console.log(`  📓 Notebook ID: ${notebook.id}`);
    console.log(`  📝 Source ID: ${sourceId}`);
    console.log(`  📊 解析状态：${verification.status}`);
    console.log('');
    
    if (options.verbose) {
      console.log('📊 完整响应:');
      console.log(JSON.stringify(verification.details, null, 2));
    }
    
  } catch (error) {
    console.error('');
    console.error('❌ 处理失败:', error.message);
    console.error('');
    console.error('💡 提示:');
    console.error('  - 确保 X 文章 URL 正确且可公开访问');
    console.error('  - 确保 NotebookLM CLI 已认证：node ' + NOTEBOOKLM_CLI_PATH + ' login');
    console.error('  - 检查网络连接');
    process.exit(1);
  }
}

// 运行主函数
main();
