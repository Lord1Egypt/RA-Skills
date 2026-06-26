/**
 * 使用 wenyan-cli 发布文章到微信公众号
 */

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { loadOpenClawEnv, resolveWechatAppId, resolveWechatAppSecret } from '../lib/openclaw_env.js';

const __pubDir = path.dirname(fileURLToPath(import.meta.url));
loadOpenClawEnv({ skillRoot: path.join(__pubDir, '..') });

/**
 * 使用 wenyan-cli 发布文章
 * @param {string} markdownFile - Markdown 文件路径
 * @param {Object} options - 选项
 * @returns {Promise<Object>} 发布结果
 */
export async function publishWithWenyan(markdownFile, options = {}) {
  const {
    theme = 'lapis',
    highlight = 'solarized-light'
  } = options;
  
  console.log('\n📱 准备发布文章...');
  console.log(`  文件：${markdownFile}`);
  console.log(`  主题：${theme}`);
  console.log(`  代码高亮：${highlight}`);
  
  try {
    // 检查文件是否存在
    if (!fs.existsSync(markdownFile)) {
      throw new Error(`文件不存在：${markdownFile}`);
    }
    
    // 读取并规范化编码与换行，降低发布乱码概率
    let content = fs.readFileSync(markdownFile, 'utf-8');
    content = normalizeMarkdown(content);

    // 检查 frontmatter
    if (!content.startsWith('---')) {
      console.log('  ⚠️  文件缺少 frontmatter，自动添加...');
      const title = extractTitle(content);
      const cover = './images/cover.jpg';
      
      const newContent = `---
title: ${safeYamlValue(title)}
cover: ${cover}
---

${content}`;
      
      content = newContent;
    }

    const coverPath = getCoverPathFromFrontmatter(content, markdownFile);
    if (coverPath && !fs.existsSync(coverPath)) {
      console.log(`  ⚠️  封面文件不存在：${coverPath}`);
      console.log('  💡 移除 frontmatter 中的 cover 字段，避免发布因无效封面失败');
      content = content.replace(/^cover:\s*.+$/m, '');
    }

    fs.writeFileSync(markdownFile, content, 'utf-8');
    
    // 检查 wenyan-cli 是否安装
    try {
      execSync('wenyan --version', { stdio: 'pipe' });
    } catch {
      console.log('  ⚠️  wenyan-cli 未安装，正在安装...');
      execSync('npm install -g @wenyan-md/cli', { stdio: 'inherit' });
      console.log('  ✅ wenyan-cli 安装成功');
    }
    
    const appId = resolveWechatAppId();
    const secret = resolveWechatAppSecret();
    
    if (!appId || !secret) {
      throw new Error('未配置微信公众号 API 凭证\n请设置环境变量：\n  export WECHAT_APP_ID=xxx\n  export WECHAT_APP_SECRET=xxx');
    }
    
    // 执行发布命令
    console.log('  🚀 执行发布...');
    
    const env = {
      ...process.env,
      WECHAT_APP_ID: appId,
      WECHAT_APP_SECRET: secret
    };
    
    execSync(`wenyan publish -f "${markdownFile}" -t ${theme} -h ${highlight}`, {
      env,
      stdio: 'inherit'
    });
    
    console.log('\n✅ 发布成功！');
    console.log('📱 请前往微信公众号后台草稿箱查看：');
    console.log('   https://mp.weixin.qq.com/');
    
    return {
      success: true,
      message: '发布成功'
    };
    
  } catch (error) {
    console.error('\n❌ 发布失败！');
    console.error('错误信息:', error.message);
    
    console.log('\n💡 常见问题：');
    console.log('  1. IP 未在白名单 → 添加到公众号后台');
    console.log('  2. Frontmatter 缺失 → 文件顶部添加 title + cover');
    console.log('  3. API 凭证错误 → 检查环境变量');
    console.log('  4. 封面尺寸错误 → 需要 1080×864 像素');
    
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * 从 Markdown 内容提取标题
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
  
  // 默认标题
  return '未命名文章';
}

function normalizeMarkdown(raw) {
  return raw
    .replace(/^\uFEFF/, '')
    .replace(/\r\n/g, '\n')
    .replace(/\r/g, '\n');
}

function safeYamlValue(value) {
  const escaped = String(value).replace(/"/g, '\\"');
  return `"${escaped}"`;
}

function getCoverPathFromFrontmatter(content, markdownFile) {
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) return null;

  const coverMatch = fmMatch[1].match(/^cover:\s*(.+)$/m);
  if (!coverMatch) return null;

  const raw = coverMatch[1].trim().replace(/^['"]|['"]$/g, '');
  if (!raw) return null;
  if (raw.startsWith('http://') || raw.startsWith('https://')) return null;

  return path.resolve(path.dirname(markdownFile), raw);
}

/**
 * 使用 browser-use 发布文章（处理需要浏览器交互的场景）
 */
export async function publishWithBrowser(markdownFile, options = {}) {
  const {
    useProfile = true,  // 使用真实 Chrome 配置，保留登录态
    headed = true       // 显示浏览器窗口
  } = options;
  
  console.log('\n📱 使用浏览器自动化发布...');
  console.log(`  文件：${markdownFile}`);
  console.log(`  配置：${useProfile ? '使用真实浏览器配置' : '无头模式'}`);
  
  try {
    // 读取 Markdown 文件
    const content = fs.readFileSync(markdownFile, 'utf-8');
    const title = extractTitle(content);
    const bodyContent = content.replace(/---\n[\s\S]*?\n---\n/, '');
    
    console.log('  📰 文章标题:', title);
    
    // 使用 browser-use 打开微信公众号后台
    console.log('  🌐 打开微信公众号后台...');
    
    const browserOptions = [];
    if (useProfile) {
      browserOptions.push('--profile');
    }
    if (headed) {
      browserOptions.push('--headed');
    }
    
    // 打开公众号后台
    execSync(`uvx browser-use ${browserOptions.join(' ')} open https://mp.weixin.qq.com/`, {
      stdio: 'inherit'
    });
    
    console.log('  ✅ 浏览器已打开');
    console.log('  💡 请在浏览器中手动完成以下操作：');
    console.log('     1. 点击「新的创作」→「文章」');
    console.log('     2. 输入标题:', title);
    console.log('     3. 粘贴正文内容');
    console.log('     4. 上传封面图');
    console.log('     5. 保存草稿或群发');
    
    return {
      success: true,
      message: '浏览器已打开，请手动完成发布',
      manualSteps: true
    };
    
  } catch (error) {
    console.error('  ❌ 浏览器操作失败:', error.message);
    
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * 处理视频文章发布（特殊处理）
 */
export async function publishWithVideo(markdownFile, options = {}) {
  console.log('\n📱 发布含视频的文章...');
  
  // 使用 publish_with_video.js 脚本
  // TODO: 实现视频文章发布
  
  return {
    success: false,
    message: '视频文章发布功能开发中...'
  };
}
