#!/usr/bin/env node
/**
 * 抖音热搜抓取 - Skill 版本 (v2 - 直接API调用)
 * 自动抓取抖音热搜榜 Top 50
 */
const https = require('https');
const fs = require('fs');
const path = require('path');

// Skill 工作目录（使用 workspace 下的 scripts 目录）
const WORKSPACE = process.env.WORKSPACE || '/home/openclaw/.openclaw/workspace';
const OUTPUT_DIR = path.join(WORKSPACE, 'scripts');

/**
 * 直接调用抖音热搜API
 * 更稳定、更快速、不依赖浏览器
 */
async function fetchDouyinHot() {
  console.log('🚀 正在请求抖音热搜API...');
  
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'www.douyin.com',
      path: '/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=120.0.0.0&browser_online=true',
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://www.douyin.com/hot/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive'
      },
      timeout: 15000
    };
    
    const req = https.get(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          
          if (parsed.data && Array.isArray(parsed.data.word_list)) {
            const wordList = parsed.data.word_list;
            console.log(`✅ 成功获取到 ${wordList.length} 条热搜`);
            
            // 清洗数据
            const cleaned = wordList
              .filter(item => item.word && item.word.trim())
              .map(item => ({
                rank: item.position || 0,
                title: item.word.trim(),
                heat: item.hot_value ? (item.hot_value / 10000).toFixed(1) + '万' : '无热度',
                heat_value: item.hot_value || 0,
                sentence: item.sentence || '',
                label: item.label || ''
              }))
              .sort((a, b) => b.heat_value - a.heat_value)
              .slice(0, 50);
            
            resolve(cleaned);
          } else {
            console.log('❌ API返回格式异常');
            console.log('响应数据:', data.substring(0, 300));
            reject(new Error('API返回格式异常'));
          }
        } catch (e) {
          console.log('❌ 解析JSON失败:', e.message);
          console.log('原始数据:', data.substring(0, 200));
          reject(e);
        }
      });
    });
    
    req.on('error', (err) => {
      console.log('❌ 网络请求失败:', err.message);
      reject(err);
    });
    
    req.setTimeout(15000, () => {
      req.destroy();
      reject(new Error('请求超时（15秒）'));
    });
  });
}

async function main() {
  try {
    const data = await fetchDouyinHot();
    
    if (!data) {
      console.log('❌ 抓取失败');
      process.exit(1);
    }

    // 输出表格
    console.log('\n📊 抖音热搜榜:');
    console.log('='.repeat(60));
    data.forEach((item, idx) => {
      console.log(`${String(idx + 1).padStart(2)}. ${item.title}`);
      if (item.heat) console.log(`   🔥 ${item.heat}`);
    });

    // 保存 JSON
    const outputPath = path.join(OUTPUT_DIR, 'douyin-hot-clean.json');
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    fs.writeFileSync(outputPath, JSON.stringify(data, null, 2));
    console.log(`\n✅ 已保存到 ${outputPath}`);

    // 返回数据供 Skill 系统使用
    return data;
  } catch (e) {
    console.error('❌ 错误:', e.message);
    process.exit(1);
  }
}

// 如果直接运行，执行主函数
if (require.main === module) {
  main();
}

module.exports = { fetchDouyinHot };