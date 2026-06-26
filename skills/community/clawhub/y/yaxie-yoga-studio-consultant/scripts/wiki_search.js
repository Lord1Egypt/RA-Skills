/**
 * 亚协知识库文件搜索脚本
 * 用法: node wiki_search.js <关键词>
 * 示例: node wiki_search.js 销售
 */

const https = require('https');
const fs = require('fs');

// 飞书应用凭证
const APP_ID = 'cli_a93b38f075b89cc4';
const APP_SECRET = 'CRSq1ZHlMM0QE488w9ph1fX0gG2eDXox';
const SPACE_ID = '7547251789502922755';

// 获取token
function getToken() {
  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'open.feishu.cn', port: 443,
      path: '/open-apis/auth/v3/tenant_access_token/internal',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    }, res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => {
        const resp = JSON.parse(d);
        resolve(resp.tenant_access_token);
      });
    });
    req.on('error', reject);
    req.write(JSON.stringify({ app_id: APP_ID, app_secret: APP_SECRET }));
    req.end();
  });
}

// 搜索文件
async function searchFiles(keyword) {
  const token = await getToken();
  
  // 获取所有文件
  let pageToken = null;
  let hasMore = true;
  let allFiles = [];
  
  while (hasMore) {
    let path = `/open-apis/wiki/v2/spaces/${SPACE_ID}/nodes?page_size=50`;
    if (pageToken) path += '&page_token=' + pageToken;
    
    const resp = await api('GET', path, token);
    if (resp.data && resp.data.items) {
      allFiles = allFiles.concat(resp.data.items);
      hasMore = resp.data.has_more;
      pageToken = resp.data.page_token;
    } else {
      break;
    }
  }
  
  // 搜索关键词
  const keywordLower = keyword.toLowerCase();
  const results = allFiles.filter(f => 
    f.title.toLowerCase().includes(keywordLower) ||
    f.title.replace(/\.(docx|pdf|xls)$/i, '').toLowerCase().includes(keywordLower)
  );
  
  console.log(`\n搜索关键词: "${keyword}"`);
  console.log(`找到 ${results.length} 个匹配文件:\n`);
  
  results.forEach((f, i) => {
    const ext = f.title.match(/\.(docx|pdf|xls)$/i)?.[0] || '';
    console.log(`${i + 1}. ${f.title.replace(/\.(docx|pdf|xls)$/i, '')}${ext}`);
    console.log(`   obj_token: ${f.obj_token}`);
    console.log('');
  });
  
  if (results.length === 0) {
    console.log('未找到匹配文件，请尝试其他关键词。');
  }
}

function api(method, path, token) {
  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'open.feishu.cn', port: 443, path, method,
      headers: { 'Authorization': 'Bearer ' + token }
    }, res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => resolve(JSON.parse(d)));
    });
    req.on('error', reject);
    req.end();
  });
}

// 主入口
const keyword = process.argv[2];
if (!keyword) {
  console.log('用法: node wiki_search.js <关键词>');
  console.log('示例: node wiki_search.js 销售');
  process.exit(1);
}

searchFiles(keyword).catch(console.error);
