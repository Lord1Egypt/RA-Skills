/**
 * 使用 browser-use 进行浏览器自动化发布
 * 支持 AI 配图、手动发布等交互操作
 */

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

/**
 * 使用 browser-use 打开微信公众号后台并执行操作
 * @param {string} action - 执行的操作
 * @param {Object} options - 选项
 */
export async function browserAction(action, options = {}) {
  const {
    useProfile = true,  // 使用真实 Chrome 配置，保留登录态
    headed = true,      // 显示浏览器窗口
    session = 'wechat'  // 会话名称
  } = options;
  
  const browserOptions = [];
  
  if (useProfile) {
    browserOptions.push('--profile');
  }
  if (headed) {
    browserOptions.push('--headed');
  }
  if (session) {
    browserOptions.push(`--session ${session}`);
  }
  
  const optionsStr = browserOptions.join(' ');
  
  try {
    switch (action) {
      case 'open':
        console.log('🌐 打开微信公众号后台...');
        execSync(`uvx browser-use ${optionsStr} open https://mp.weixin.qq.com/`, {
          stdio: 'inherit'
        });
        console.log('✅ 浏览器已打开');
        break;
        
      case 'state':
        console.log('📊 获取页面状态...');
        execSync(`uvx browser-use ${optionsStr} state`, {
          stdio: 'inherit'
        });
        break;
        
      case 'create-article':
        await createArticle(options);
        break;
        
      case 'ai-cover':
        await generateAICover(options);
        break;
        
      case 'publish':
        await publishArticle(options);
        break;
        
      default:
        console.error('未知操作:', action);
    }
    
  } catch (error) {
    console.error('❌ 浏览器操作失败:', error.message);
    throw error;
  }
}

/**
 * 创建新文章
 */
async function createArticle(options = {}) {
  console.log('\n📝 创建新文章...');
  
  const browserOptions = [];
  if (options.useProfile) browserOptions.push('--profile');
  if (options.headed) browserOptions.push('--headed');
  if (options.session) browserOptions.push(`--session ${options.session}`);
  
  const optionsStr = browserOptions.join(' ');
  
  console.log('💡 请手动操作：');
  console.log('  1. 在首页找到「新的创作」');
  console.log('  2. 点击「文章」');
  console.log('  3. 输入文章标题');
  console.log('  4. 粘贴正文内容');
  
  // 打开公众号后台
  execSync(`uvx browser-use ${optionsStr} open https://mp.weixin.qq.com/`, {
    stdio: 'inherit'
  });
  
  return {
    success: true,
    message: '请手动完成文章创建'
  };
}

/**
 * 使用公众号 AI 配图功能生成封面
 */
async function generateAICover(options = {}) {
  console.log('\n🎨 使用公众号 AI 配图功能生成封面...');
  
  const browserOptions = [];
  if (options.useProfile) browserOptions.push('--profile');
  if (options.headed) browserOptions.push('--headed');
  
  const optionsStr = browserOptions.join(' ');
  
  console.log('💡 操作步骤：');
  console.log('  1. 点击封面区域（「拖拽或选择封面」）');
  console.log('  2. 选择「AI 配图」');
  console.log('  3. 输入封面描述（主体 + 场景 + 风格）');
  console.log('  4. 点击「开始创作」');
  console.log('  5. 等待 20-60 秒生成');
  console.log('  6. 选择合适的图片，点击「使用」');
  
  // 这里无法完全自动化，因为需要用户输入描述和选择图片
  // 打开公众号后台
  execSync(`uvx browser-use ${optionsStr} open https://mp.weixin.qq.com/`, {
    stdio: 'inherit'
  });
  
  return {
    success: true,
    message: '请手动完成 AI 配图操作'
  };
}

/**
 * 发布文章
 */
async function publishArticle(options = {}) {
  console.log('\n📱 发布文章...');
  
  const browserOptions = [];
  if (options.useProfile) browserOptions.push('--profile');
  if (options.headed) browserOptions.push('--headed');
  
  const optionsStr = browserOptions.join(' ');
  
  console.log('💡 请手动操作：');
  console.log('  1. 检查文章内容和排版');
  console.log('  2. 确认封面图已设置');
  console.log('  3. 点击「保存」保存到草稿箱');
  console.log('     或点击「群发」直接发布');
  
  execSync(`uvx browser-use ${optionsStr} open https://mp.weixin.qq.com/`, {
    stdio: 'inherit'
  });
  
  return {
    success: true,
    message: '请手动完成发布操作'
  };
}

/**
 * 完整的浏览器自动化发布流程
 */
export async function fullBrowserPublish(markdownFile, options = {}) {
  console.log('\n🚀 开始浏览器自动化发布流程...\n');
  
  const {
    useProfile = true,
    headed = true,
    session = 'wechat-publish'
  } = options;
  
  // 1. 读取 Markdown 文件
  console.log('📖 读取文章内容...');
  const content = fs.readFileSync(markdownFile, 'utf-8');
  const title = extractTitle(content);
  const bodyContent = content.replace(/---\n[\s\S]*?\n---\n/, '');
  
  console.log(`  标题：${title}`);
  console.log(`  字数：${bodyContent.length}`);
  
  // 2. 打开浏览器
  console.log('\n🌐 打开浏览器...');
  await browserAction('open', { useProfile, headed, session });
  
  // 3. 创建文章
  console.log('\n📝 创建文章...');
  await browserAction('create-article', { useProfile, headed, session });
  
  // 4. 生成 AI 封面（如果需要）
  if (options.generateCover) {
    console.log('\n🎨 生成 AI 封面...');
    await browserAction('ai-cover', { useProfile, headed, session });
  }
  
  // 5. 发布
  console.log('\n📱 发布文章...');
  await browserAction('publish', { useProfile, headed, session });
  
  console.log('\n✅ 发布流程完成！');
  console.log('💡 浏览器已打开，请手动完成最后确认和发布');
  
  return {
    success: true,
    message: '浏览器已打开，请手动完成发布'
  };
}

/**
 * 从 Markdown 提取标题
 */
function extractTitle(content) {
  // 尝试从 frontmatter 提取
  const fmMatch = content.match(/---\n([\s\S]*?)\n---/);
  if (fmMatch) {
    const titleMatch = fmMatch[1].match(/title:\s*(.+)/);
    if (titleMatch) {
      return titleMatch[1].trim();
    }
  }
  
  // 尝试从 H1 提取
  const h1Match = content.match(/^#\s+(.+)/m);
  if (h1Match) {
    return h1Match[1].trim();
  }
  
  return '未命名文章';
}

/**
 * 检查浏览器环境
 */
export function checkBrowserEnv() {
  try {
    // 检查 browser-use 是否可用
    execSync('uvx browser-use --help', { stdio: 'pipe' });
    console.log('✅ browser-use 已安装');
    
    // 检查 Chromium 是否安装
    try {
      execSync('uvx browser-use doctor', { stdio: 'pipe' });
      console.log('✅ Chromium 已安装');
    } catch {
      console.log('⚠️  Chromium 未安装，正在安装...');
      execSync('uvx browser-use install', { stdio: 'inherit' });
      console.log('✅ Chromium 安装成功');
    }
    
    return true;
  } catch (error) {
    console.error('❌ browser-use 未安装');
    console.log('💡 请先运行：uvx browser-use install');
    return false;
  }
}
