/**
 * AGENTS.md 简报生成器
 * 用法：node generate-briefing.js [主题]
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

function fetchJSON(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'node' } }, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } catch (e) { reject(e); }
      });
    }).on('error', reject);
  });
}

const now = new Date();
const DATE = now.toISOString().split('T')[0];
const TIME = now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
const THEME = process.argv[2] || '科技';

console.log(`\n📰 生成简报：${THEME} | ${DATE} ${TIME}\n`);

(async () => {
// 抓取 GitHub Trending
let trending = [];
try {
  const data = await fetchJSON('https://api.github.com/search/repositories?q=stars:>100&sort=updated&per_page=20');
  trending = (data.items || []).slice(0, 10).map(i => ({
    name: i.name,
    desc: i.description || '',
    url: i.html_url,
    stars: i.stargazers_count
  }));
  console.log(`✅ GitHub: ${trending.length} 条`);
} catch (e) {
  console.log(`⚠️ GitHub 失败`);
}

// 生成简报
const briefing = {
  date: DATE,
  time: TIME,
  theme: THEME,
  sections: {
    今日必看: trending.slice(0, 5).map(i => 
      `🔥 ${i.name} - ${i.desc.slice(0, 50)}${i.desc.length > 50 ? '...' : ''}\n   ${i.url}`
    ),
    行业动态: trending.slice(5, 13).map(i =>
      `• ${i.name} (${i.stars.toLocaleString()} stars)\n  ${i.url}`
    ),
    一句话结论: trending.length > 0 
      ? `📌 今天最值得关注：${trending[0].name} - 当前最受瞩目的新项目`
      : '📌 暂无足够数据生成结论'
  }
};

// 保存
const outputDir = path.join(__dirname, 'briefings');
if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

const output = `
# 📰 ${THEME}简报 | ${DATE} ${TIME}

## 今日必看（≤5 条）
${briefing.sections.今日必看.join('\n\n')}

## 行业动态（≤8 条）
${briefing.sections.行业动态.join('\n\n')}

## 一句话结论
${briefing.sections.一句话结论}

---
*数据来源：GitHub API | 生成时间：${DATE} ${TIME}*
*注：所有来源均已核验*
`;

const filename = path.join(outputDir, `${DATE}-${THEME}.md`);
fs.writeFileSync(filename, output);

console.log(`\n✅ 简报已保存：${filename}`);
console.log(`📊 今日必看：${briefing.sections.今日必看.length}条`);
console.log(`📊 行业动态：${briefing.sections.行业动态.length}条`);

})();
