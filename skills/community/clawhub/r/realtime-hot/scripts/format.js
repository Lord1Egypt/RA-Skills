/**
 * 实时热榜格式化脚本
 * 零依赖：只用 Node.js 内置模块
 */

import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const jsonFile = process.argv[2] || join(__dirname, 'hot-data.json');

const data = JSON.parse(readFileSync(jsonFile, 'utf8'));

// ========== 聚类算法 ==========
function ngrams(text) {
  const words = text.split('');
  const grams = [];
  for (let i = 0; i < words.length - 1; i++) grams.push(words[i] + words[i+1]);
  return new Set(grams);
}

function jaccard(a, b) {
  const g1 = ngrams(a), g2 = ngrams(b);
  const inter = [...g1].filter(x => g2.has(x));
  const union = new Set([...g1, ...g2]);
  return union.size === 0 ? 0 : inter.length / union.size;
}

function cluster(data) {
  const items = Object.entries(data).flatMap(([platform, list]) =>
    (list || []).map(i => ({ ...i, platform }))
  ).filter(i => !i.title.match(/总书记|国家领导人|主席|预售|开售|价格/));

  const n = items.length;
  const parents = Array.from({ length: n }, (_, i) => i);
  function uf(x) { return parents[x] !== x ? parents[x] = uf(parents[x]) : parents[x]; }
  const union = (a, b) => { parents[uf(a)] = uf(b); };

  for (let i = 0; i < n; i++)
    for (let j = i + 1; j < n; j++)
      if (jaccard(items[i].title, items[j].title) > 0.10) union(i, j);

  const groups = {};
  for (let i = 0; i < n; i++) {
    const r = uf(i);
    if (!groups[r]) groups[r] = [];
    groups[r].push(items[i]);
  }

  return Object.values(groups)
    .filter(g => new Set(g.map(i => i.platform)).size >= 2)
    .map(g => {
      // 标题选取：优先非微博平台，5-20字最短的
      const nonWeibo = g.filter(i => i.platform !== '微博');
      const weiboOnly = g.filter(i => i.platform === '微博');
      const pickBest = (arr) => {
        const within = arr.filter(i => i.title.length >= 5 && i.title.length <= 20);
        const list = within.length > 0 ? within : arr;
        return list.reduce((b, i) => i.title.length < b.title.length ? i : b, list[0]);
      };
      const best = nonWeibo.length > 0 ? pickBest(nonWeibo) : pickBest(weiboOnly);

      // 同平台去重：取最高排名
      const seen = {};
      g.forEach(i => { if (!seen[i.platform] || i.rank < seen[i.platform].rank) seen[i.platform] = i; });

      return {
        title: best.title,
        url: best.url,
        topics: Object.values(seen).map(i => ({ platform: i.platform, rank: i.rank, url: i.url })),
        score: Math.pow(new Set(g.map(i => i.platform)).size, 2) / (g.reduce((s, i) => s + i.rank, 0) / g.length)
      };
    })
    .sort((a, b) => b.score - a.score);
}

// ========== 格式化 ==========
const topics = cluster(data);
const lines = [];

lines.push('## 🔥 全网热点\n');

topics.slice(0, 5).forEach((t, i) => {
  const platStr = t.topics.map(tp => `${tp.platform.replace('今日头条','头条')}#${tp.rank}`).join(' · ');
  lines.push(`### ${i+1}. [${t.title}](${t.url})`);
  lines.push(platStr);
  lines.push('---');
});

lines.push('[微博](https://rebang.today/?tab=weibo) · [抖音](https://rebang.today/?tab=douyin) · [头条](https://rebang.today/?tab=toutiao) · [百度](https://rebang.today/?tab=baidu) · [知乎](https://rebang.today/?tab=zhihu) · [腾讯](https://tophub.today/n/qndg48xeLl)');

console.log(lines.join('\n'));
