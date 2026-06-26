#!/usr/bin/env node

/**
 * 微信公众号 API 发布脚本
 * 使用标准草稿箱 API 流程
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import axios from 'axios';
import { loadOpenClawEnv, resolveWechatAppId, resolveWechatAppSecret } from '../lib/openclaw_env.js';

const __apiPubDir = path.dirname(fileURLToPath(import.meta.url));
loadOpenClawEnv({ skillRoot: path.join(__apiPubDir, '..', '..') });

// 读取文章内容
const articlePath = process.argv[2];
if (!articlePath) {
  console.log('\n❌ 错误：请指定文章路径\n');
  console.log('用法：node scripts/publisher/api_publish.js <文章路径>\n');
  process.exit(1);
}

if (!fs.existsSync(articlePath)) {
  console.log(`\n❌ 错误：文件不存在 ${articlePath}\n`);
  process.exit(1);
}

const rawContent = fs.readFileSync(articlePath, 'utf-8');

function stripFrontmatter(md) {
  const fmMatch = md.match(/^---\n([\s\S]*?)\n---\n?/);
  if (!fmMatch) return { body: md, meta: {} };
  const meta = {};
  for (const line of fmMatch[1].split('\n')) {
    const idx = line.indexOf(':');
    if (idx > 0) {
      const key = line.slice(0, idx).trim();
      let val = line.slice(idx + 1).trim();
      if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
        val = val.slice(1, -1);
      }
      meta[key] = val;
    }
  }
  return { body: md.slice(fmMatch[0].length), meta };
}

const { body: content, meta: frontmatter } = stripFrontmatter(rawContent);
const titleFromFM = frontmatter.title;
const titleFromH1 = (content.match(/^#\s+(.+)/m) || [])[1];
const title = (titleFromFM || titleFromH1 || '未命名文章').trim();
const digest = frontmatter.digest || content.replace(/[#*_~`>\[\]!\(\)]/g, '').replace(/\s+/g, ' ').trim().substring(0, 120);

console.log('\n🚀 开始 API 发布流程...');
console.log(`   标题：${title}`);
console.log(`   字数：${content.length} 字`);

// 获取 access_token
async function getAccessToken() {
  const appId = resolveWechatAppId();
  const appSecret = resolveWechatAppSecret();
  
  if (!appId || !appSecret) {
    throw new Error('未配置 WECHAT_APP_ID 或 WECHAT_APP_SECRET 环境变量');
  }
  
  try {
    const response = await axios.get(
      `https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${appId}&secret=${appSecret}`
    );
    
    if (response.data.access_token) {
      console.log('✅ access_token 获取成功');
      return response.data.access_token;
    } else {
      throw new Error(`获取 access_token 失败: ${JSON.stringify(response.data)}`);
    }
  } catch (error) {
    throw new Error(`API 请求失败: ${error.message}`);
  }
}

// 创建草稿
async function createDraft(accessToken) {
  try {
    // 先创建空草稿
    const createResponse = await axios.post(
      `https://api.weixin.qq.com/cgi-bin/draft/add?access_token=${accessToken}`,
      {
        articles: [
          {
            title,
            author: frontmatter.author || '',
            digest,
            content: '<p>正在加载中...</p>',
            content_source_url: '',
            show_cover_pic: 0,
            need_open_comment: 0,
            only_fans_can_comment: 0
          }
        ]
      },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );
    
    if (createResponse.data.errcode === 0 && createResponse.data.media_id) {
      console.log(`✅ 草稿已创建，media_id: ${createResponse.data.media_id}`);
      return createResponse.data.media_id;
    } else {
      throw new Error(`创建草稿失败: ${JSON.stringify(createResponse.data)}`);
    }
  } catch (error) {
    throw new Error(`创建草稿失败: ${error.message}`);
  }
}

// 更新草稿内容
async function updateDraft(accessToken, mediaId, htmlContent) {
  try {
    const response = await axios.post(
      `https://api.weixin.qq.com/cgi-bin/draft/update?access_token=${accessToken}&media_id=${mediaId}`,
      {
        articles: [
          {
            title,
            author: frontmatter.author || '',
            digest,
            content: htmlContent,
            content_source_url: '',
            show_cover_pic: 0,
            need_open_comment: 0,
            only_fans_can_comment: 0
          }
        ]
      },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );
    
    if (response.data.errcode === 0) {
      console.log('✅ 草稿内容更新成功');
      return true;
    } else {
      throw new Error(`更新草稿失败: ${JSON.stringify(response.data)}`);
    }
  } catch (error) {
    throw new Error(`更新草稿失败: ${error.message}`);
  }
}

// 主函数
async function main() {
  try {
    console.log('\n🔑 正在验证公众号凭证...');
    
    // 验证环境变量
    if (!resolveWechatAppId()) {
      throw new Error('WECHAT_APP_ID 未配置');
    }
    if (!resolveWechatAppSecret()) {
      throw new Error('WECHAT_APP_SECRET 未配置');
    }
    
    console.log('✅ 公众号凭证验证通过');
    
    // 获取 access_token
    const accessToken = await getAccessToken();
    
    // 创建草稿
    const mediaId = await createDraft(accessToken);
    
    const htmlContent = content
      .replace(/^#\s+(.+)/gm, '<h1>$1</h1>')
      .replace(/^##\s+(.+)/gm, '<h2>$1</h2>')
      .replace(/^###\s+(.+)/gm, '<h3>$1</h3>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br/>')
      .replace(/^/, '<p>')
      .replace(/$/, '</p>');
    
    // 更新草稿内容
    await updateDraft(accessToken, mediaId, htmlContent);
    
    console.log('\n🎉 发布完成！');
    console.log('📊 发布摘要：');
    console.log(`   📝 文章标题：${title}`);
    console.log(`   📏 字数统计：${content.length} 字`);
    console.log(`   🆔 草稿ID：${mediaId}`);
    console.log(`   📌 查看位置：微信公众号后台 → 草稿箱`);
    console.log('\n✅ 文章已成功保存到微信公众号草稿箱！');
    
  } catch (error) {
    console.error('\n❌ 发布失败:', error.message);
    console.error('\n💡 解决方案：');
    console.error('   1. 检查网络连接');
    console.error('   2. 确认公众号已认证');
    console.error('   3. 检查 WECHAT_APP_ID 和 WECHAT_APP_SECRET 是否正确');
    console.error('   4. 在微信公众号后台查看「草稿箱」');
    process.exit(1);
  }
}

main();
