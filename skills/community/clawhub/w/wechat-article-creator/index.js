#!/usr/bin/env node

/**
 * WeChat Article Creator
 * 根据主题自动生成微信公众号文章草稿
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// 加载环境变量
const envPath = path.join(process.cwd(), '.env');
if (fs.existsSync(envPath)) {
  const envContent = fs.readFileSync(envPath, 'utf8');
  envContent.split('\n').forEach(line => {
    const match = line.match(/^([^=]+)=(.*)$/);
    if (match) {
      process.env[match[1]] = match[2];
    }
  });
}

// 配置
const CONFIG = {
  WECHAT_APPID: process.env.WECHAT_APPID,
  WECHAT_SECRET: process.env.WECHAT_SECRET,
  SEARCH_COUNT: 5,
  DEFAULT_WORDS: 1500
};

// 工具函数：HTTP 请求
function httpRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, { ...options, timeout: 30000 }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch {
          resolve(data);
        }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
  });
}

// 获取微信 Access Token
async function getAccessToken() {
  if (!CONFIG.WECHAT_APPID || !CONFIG.WECHAT_SECRET) {
    throw new Error('请先配置 WECHAT_APPID 和 WECHAT_SECRET');
  }
  
  const url = `https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${CONFIG.WECHAT_APPID}&secret=${CONFIG.WECHAT_SECRET}`;
  const data = await httpRequest(url);
  
  if (data.errcode) {
    throw new Error(`获取 Token 失败: ${data.errmsg}`);
  }
  
  return data.access_token;
}

// 创建微信草稿
async function createDraft(accessToken, title, content, author = 'AI助手') {
  const url = `https://api.weixin.qq.com/cgi-bin/draft/add?access_token=${accessToken}`;
  
  const article = {
    articles: [{
      title: title,
      author: author,
      digest: content.substring(0, 100).replace(/<[^>]+>/g, '') + '...',
      content: content,
      content_source_url: '',
      thumb_media_id: '',
      need_open_comment: 0,
      only_fans_can_comment: 0
    }]
  };
  
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify(article);
    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };
    
    const req = https.request(url, options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.errcode) {
            reject(new Error(`创建草稿失败: ${result.errmsg}`));
          } else {
            resolve(result);
          }
        } catch (e) {
          reject(e);
        }
      });
    });
    
    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    console.log(`
使用方法:
  wechat-article-creator "主题" [选项]

选项:
  --words, -w    目标字数 (默认: 1500)
  --style, -s    写作风格 (默认: 专业分析)
  --author, -a   作者名称 (默认: AI助手)
  --help, -h     显示帮助

示例:
  wechat-article-creator "人工智能发展趋势"
  wechat-article-creator "新能源汽车市场" --words 2000 --style "轻松科普"
`);
    process.exit(0);
  }
  
  const topic = args[0];
  let words = CONFIG.DEFAULT_WORDS;
  let style = '专业分析';
  let author = 'AI助手';
  
  // 解析参数
  for (let i = 1; i < args.length; i++) {
    if ((args[i] === '--words' || args[i] === '-w') && args[i + 1]) {
      words = parseInt(args[i + 1]);
      i++;
    } else if ((args[i] === '--style' || args[i] === '-s') && args[i + 1]) {
      style = args[i + 1];
      i++;
    } else if ((args[i] === '--author' || args[i] === '-a') && args[i + 1]) {
      author = args[i + 1];
      i++;
    }
  }
  
  console.log(`\n📝 主题: ${topic}`);
  console.log(`🎯 字数: ${words}`);
  console.log(`🎨 风格: ${style}`);
  console.log(`\n⏳ 正在生成文章...\n`);
  
  // 这里会调用搜索和AI生成
  // 实际使用时需要集成搜索API和LLM
  
  console.log('✅ 文章生成完成！');
  console.log('\n💡 提示: 此技能需要配合搜索API和LLM使用。');
  console.log('   作为OpenClaw技能使用时，由Agent调用相应工具完成。');
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
