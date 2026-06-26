#!/usr/bin/env node

/**
 * 微信公众号文章发布工具
 * 
 * 功能：将精心排版的 HTML 文章直接推送到公众号草稿箱
 * 
 * 使用方式：
 *   1. 复制 config.example.json 为 config.json，填入你的 AppID 和 AppSecret
 *   2. 运行 node publish.js [html文件路径]
 * 
 * 原理：通过微信公众号 draft/add API 直接创建草稿，
 *       绕过公众号编辑器的样式过滤，完整保留内联 CSS 排版效果
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ============================================================
// 配置
// ============================================================

function loadConfig() {
  const configPath = path.join(__dirname, 'config.json');
  if (!fs.existsSync(configPath)) {
    console.error('\n❌ 未找到 config.json');
    console.error('请先复制 config.example.json 为 config.json，并填入你的公众号配置：');
    console.error('\n  cp config.example.json config.json');
    console.error('  然后编辑 config.json 填入 appId 和 appSecret\n');
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
}

// ============================================================
// 微信 API 封装
// ============================================================

const WX_API_BASE = 'https://api.weixin.qq.com/cgi-bin';

/**
 * 获取 access_token
 */
async function getAccessToken(appId, appSecret) {
  const url = `${WX_API_BASE}/token?grant_type=client_credential&appid=${appId}&secret=${appSecret}`;
  const res = await fetch(url);
  const data = await res.json();
  
  if (data.errcode) {
    throw new Error(`获取 access_token 失败: ${data.errcode} - ${data.errmsg}`);
  }
  
  console.log(`✅ 获取 access_token 成功（有效期 ${data.expires_in} 秒）`);
  return data.access_token;
}

/**
 * 上传图文消息内的图片，获取微信认可的 URL
 * （如果 HTML 中有图片，需要先上传）
 */
async function uploadContentImage(accessToken, imagePath) {
  const url = `${WX_API_BASE}/media/uploadimg?access_token=${accessToken}`;
  
  const formData = new FormData();
  const imageBuffer = fs.readFileSync(imagePath);
  const blob = new Blob([imageBuffer]);
  formData.append('media', blob, path.basename(imagePath));
  
  const res = await fetch(url, {
    method: 'POST',
    body: formData,
  });
  const data = await res.json();
  
  if (data.errcode) {
    throw new Error(`上传图片失败: ${data.errcode} - ${data.errmsg}`);
  }
  
  return data.url; // 微信认可的图片 URL
}

/**
 * 上传永久素材（用于封面图）
 */
async function uploadThumbMedia(accessToken, imagePath) {
  const url = `${WX_API_BASE}/material/add_material?access_token=${accessToken}&type=image`;
  
  const formData = new FormData();
  const imageBuffer = fs.readFileSync(imagePath);
  const blob = new Blob([imageBuffer]);
  formData.append('media', blob, path.basename(imagePath));
  
  const res = await fetch(url, {
    method: 'POST',
    body: formData,
  });
  const data = await res.json();
  
  if (data.errcode) {
    throw new Error(`上传封面图失败: ${data.errcode} - ${data.errmsg}`);
  }
  
  console.log(`✅ 封面图上传成功 (media_id: ${data.media_id})`);
  return data.media_id;
}

/**
 * 创建草稿
 */
async function createDraft(accessToken, article) {
  const url = `${WX_API_BASE}/draft/add?access_token=${accessToken}`;
  
  const body = {
    articles: [article]
  };
  
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  
  if (data.errcode) {
    throw new Error(`创建草稿失败: ${data.errcode} - ${data.errmsg}`);
  }
  
  console.log(`✅ 草稿创建成功！(media_id: ${data.media_id})`);
  return data.media_id;
}

// ============================================================
// HTML 处理
// ============================================================

/**
 * 从 HTML 文件中提取文章内容
 * 只提取 ARTICLE CONTENT 标记之间的内容
 * 并剥离外层无用的 wrapper div
 */
function extractArticleContent(htmlContent) {
  const startMarker = '<!-- ========== ARTICLE CONTENT START ========== -->';
  const endMarker = '<!-- ========== ARTICLE CONTENT END ========== -->';
  
  let content = htmlContent;
  
  const startIdx = content.indexOf(startMarker);
  const endIdx = content.indexOf(endMarker);
  
  if (startIdx !== -1 && endIdx !== -1) {
    content = content.substring(startIdx + startMarker.length, endIdx);
  }
  
  // 先去掉 HTML 注释（干扰后续正则匹配）
  content = content.replace(/<!--[\s\S]*?-->/g, '').trim();
  
  // 剥离外层无样式的 wrapper div（递归剥离多层）
  // 这些 div 只有 class/id，没有 style，微信会过滤掉 class/id 留下空 div
  let changed = true;
  while (changed) {
    changed = false;
    // 匹配最外层 div：只有 class/id 属性，没有 style
    const m = content.match(/^\s*<div(?:\s+(?:class|id)="[^"]*")*\s*>\s*([\s\S]*)\s*<\/div>\s*$/);
    if (m && !content.match(/^\s*<div[^>]*style=/)) {
      // 确认这个 div 没有 style 属性才剥离
      const openTag = content.match(/^\s*<div[^>]*>/);
      if (openTag && !openTag[0].includes('style=')) {
        content = m[1].trim();
        changed = true;
      }
    }
  }
  
  return content;
}

/**
 * 压缩 HTML（去除多余的换行和空格）
 * 这是关键步骤！不压缩的话，微信后台会插入 <span leaf> 标签导致排版错乱
 */
function compressHTML(html) {
  return html
    // 去除 HTML 注释
    .replace(/<!--[\s\S]*?-->/g, '')
    // 去除标签之间的空白
    .replace(/>\s+</g, '><')
    // 去除多余的空格
    .replace(/\s{2,}/g, ' ')
    // 去除行首行尾空白
    .trim();
}

/**
 * 移除公众号不支持的 CSS 属性，修复手机端兼容性，并精简内联样式
 * 
 * 核心发现：微信公众号通过 draft/add API 上传时，<div> 标签的 style 属性
 * 会被过滤掉！必须用 <section> 替代 <div> 才能保留内联样式。
 * 
 * 关键限制：content 字段必须 < 2万字符
 */
function sanitizeForWechat(html) {
  let result = html;
  
  // ===== 最关键的一步：<div> → <section> =====
  // 微信 draft/add API 会过滤 <div> 的 style 属性
  // 但 <section> 的 style 属性会被保留（135编辑器、秀米等工具的标准做法）
  result = result.replace(/<div(\s)/g, '<section$1');
  result = result.replace(/<div>/g, '<section>');
  result = result.replace(/<\/div>/g, '</section>');
  
  // 1. 移除 font-family（微信有自己的字体栈，不需要指定）
  result = result.replace(/font-family\s*:[^;"]*(?:'[^']*'[^;"]*|"[^"]*"[^;"]*)*;?/g, '');
  
  // 2. 移除所有 id/class 属性（微信会剥离 id，class 无 <style> 标签无意义）
  result = result.replace(/\s+id="[^"]*"/g, '');
  result = result.replace(/\s+class="[^"]*"/g, '');
  
  // 3. rgba() → hex（手机端兼容性更好）
  result = result.replace(/rgba\(255,\s*255,\s*255,\s*0\.12\)/g, '#FFFFFF1F');
  result = result.replace(/rgba\(255,\s*255,\s*255,\s*0\.2\)/g, '#FFFFFF33');
  result = result.replace(/rgba\(255,\s*255,\s*255,\s*0\.8\)/g, '#FFFFFFCC');
  result = result.replace(/rgba\(255,\s*255,\s*255,\s*0\.55\)/g, '#FFFFFF8C');
  result = result.replace(/rgba\(0,\s*0,\s*0,\s*[\d.]+\)/g, '#00000026');
  
  // 4. max-width → width:100%
  result = result.replace(/max-width\s*:\s*578px/g, 'width:100%');
  
  // 5. 移除 position/z-index（微信会删除）
  result = result.replace(/position\s*:\s*[^;]+;?/g, '');
  result = result.replace(/z-index\s*:\s*[^;]+;?/g, '');
  
  // 6. 移除与父级相同的冗余 color 声明
  result = result.replace(/;color:#2D2A3E(?=[";}])/g, '');
  result = result.replace(/color:#2D2A3E;/g, '');
  
  // 7. 移除 vertical-align:middle（节省约 460 字符，section 标签不太依赖它）
  result = result.replace(/;?vertical-align:middle;?/g, ';');
  
  // 8. 精简 #1B1642 的重复 color 声明（strong 标签已默认继承父级深色）
  result = result.replace(/<strong style="color:#1B1642">/g, '<strong>');
  result = result.replace(/<strong style="color:#1B1642;/g, '<strong style="');
  
  // 7. 清理连续分号和空 style
  result = result.replace(/;\s*;/g, ';');
  result = result.replace(/style=";\s*/g, 'style="');
  result = result.replace(/;\s*"/g, '"');
  result = result.replace(/style="\s*"/g, ''); // 删除空的 style 属性
  
  return result;
}

// ============================================================
// 主流程
// ============================================================

async function main() {
  console.log('\n🚀 微信公众号文章发布工具\n');
  console.log('━'.repeat(50));
  
  // 加载配置
  const config = loadConfig();
  
  // 确定 HTML 文件路径
  const htmlFile = process.argv[2] || path.join(__dirname, '..', 'blog-post-wechat.html');
  
  if (!fs.existsSync(htmlFile)) {
    console.error(`\n❌ 找不到 HTML 文件: ${htmlFile}`);
    process.exit(1);
  }
  
  console.log(`📄 HTML 文件: ${path.basename(htmlFile)}`);
  
  // 读取并处理 HTML
  const rawHTML = fs.readFileSync(htmlFile, 'utf-8');
  let articleContent = extractArticleContent(rawHTML);
  
  // 关键：移除可能有问题的样式
  articleContent = sanitizeForWechat(articleContent);
  
  // 关键：压缩 HTML（防止 <span leaf> 问题）
  const compressedContent = compressHTML(articleContent);
  
  console.log(`📊 原始大小: ${articleContent.length} 字符`);
  console.log(`📊 压缩后: ${compressedContent.length} 字符`);
  
  if (compressedContent.length > 20000) {
    console.error(`❌ 内容超过 2 万字符限制 (${compressedContent.length} 字符)！`);
    console.error('   微信会拒绝或在手机端降级为纯文本。请精简 HTML 内容。');
    process.exit(1);
  }
  
  // 获取 access_token
  console.log('\n🔑 正在获取 access_token...');
  const accessToken = await getAccessToken(config.appId, config.appSecret);
  
  // 上传封面图（如果配置了的话）
  let thumbMediaId = config.thumbMediaId || '';
  
  if (!thumbMediaId && config.thumbImagePath) {
    const thumbPath = path.resolve(__dirname, config.thumbImagePath);
    if (fs.existsSync(thumbPath)) {
      console.log('🖼️  正在上传封面图...');
      thumbMediaId = await uploadThumbMedia(accessToken, thumbPath);
    } else {
      console.warn(`⚠️  封面图不存在: ${thumbPath}`);
    }
  }
  
  if (!thumbMediaId) {
    console.error('\n❌ 需要封面图！请在 config.json 中设置 thumbMediaId 或 thumbImagePath');
    console.error('   提示：你可以在公众号后台上传一张图，然后用素材管理 API 获取 media_id');
    console.error('   或者设置 thumbImagePath 指向本地图片文件，脚本会自动上传\n');
    process.exit(1);
  }
  
  // 创建草稿
  console.log('\n📝 正在创建草稿...');
  
  const article = {
    article_type: 'news',
    title: config.title || 'AI 时代，产品经理怎么做产品决策？',
    author: config.author || '',
    digest: config.digest || '',
    content: compressedContent,
    content_source_url: config.contentSourceUrl || '',
    thumb_media_id: thumbMediaId,
    need_open_comment: config.needOpenComment || 0,
    only_fans_can_comment: config.onlyFansCanComment || 0,
  };
  
  const mediaId = await createDraft(accessToken, article);
  
  console.log('\n━'.repeat(50));
  console.log('🎉 搞定！文章已推送到公众号草稿箱');
  console.log(`   media_id: ${mediaId}`);
  console.log('   去公众号后台 → 草稿箱 查看和编辑');
  console.log('   确认无误后点击「发布」即可\n');
}

main().catch(err => {
  console.error(`\n❌ 发生错误: ${err.message}\n`);
  process.exit(1);
});
