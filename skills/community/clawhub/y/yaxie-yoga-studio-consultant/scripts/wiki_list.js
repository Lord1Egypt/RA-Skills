/**
 * 亚协知识库文件列表脚本
 * 用法: node wiki_list.js
 */

const https = require('https');

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

// 获取所有文件
async function getAllFiles() {
  const token = await getToken();
  
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
      console.log(`已获取 ${allFiles.length} 个文件...`);
    } else {
      console.log('响应:', JSON.stringify(resp).substring(0, 200));
      break;
    }
  }
  
  return allFiles;
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
async function main() {
  console.log('获取知识库文件列表...\n');
  
  const files = await getAllFiles();
  
  console.log(`\n=== 知识库文件列表 (共 ${files.length} 个) ===\n`);
  
  // 按类型分组
  const byType = {};
  files.forEach(f => {
    const ext = f.title.match(/\.(docx|pdf|xls)$/i)?.[0] || 'other';
    if (!byType[ext]) byType[ext] = [];
    byType[ext].push(f);
  });
  
  // 输出统计
  for (const [type, items] of Object.entries(byType)) {
    console.log(`${type}: ${items.length}个`);
  }
  
  // 输出完整列表
  console.log('\n=== 完整文件列表 ===\n');
  files.forEach((f, i) => {
    const ext = f.title.match(/\.(docx|pdf|xls)$/i)?.[0] || '';
    const name = f.title.replace(/\.(docx|pdf|xls)$/i, '');
    console.log(`${String(i + 1).padStart(2, '0')}. ${name}${ext}`);
    console.log(`    obj_token: ${f.obj_token}`);
  });
}

main().catch(console.error);
