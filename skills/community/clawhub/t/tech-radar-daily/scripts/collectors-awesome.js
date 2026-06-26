/**
 * 情报源：Awesome Lists
 * README 通过 CDN 获取，不消耗 GitHub API
 * Star 查询带缓存，避免重复调用
 */

const fetch = require('node-fetch');
const ProxyAgent = require('proxy-agent');
const fs = require('fs');
const path = require('path');

// ============ 全局代理配置 ============
// 自动识别 http/https 协议，无需手动配置
const globalAgent = new ProxyAgent(process.env.https_proxy || process.env.HTTPS_PROXY || process.env.http_proxy || process.env.HTTP_PROXY);
// ====================================

const CACHE_PATH = path.join(__dirname, '../data/github_cache.json');

/* ---------------- 缓存 ---------------- */

function loadCache() {
 try {
 if (fs.existsSync(CACHE_PATH)) {
 return JSON.parse(fs.readFileSync(CACHE_PATH, 'utf-8'));
 }
 } catch (e) {}
 return {};
}

function saveCache(cache) {
 try {
 const dir = path.dirname(CACHE_PATH);
 if (!fs.existsSync(dir)) {
 fs.mkdirSync(dir, { recursive: true });
 }

 fs.writeFileSync(
 CACHE_PATH,
 JSON.stringify(cache, null, 2),
 'utf-8'
 );
 } catch (e) {
 console.error('⚠️ 保存缓存失败:', e.message);
 }
}

/* ---------------- GitHub Stars ---------------- */

async function getStars(repo, cache) {
 if (cache[repo]) {
 return cache[repo];
 }

 try {
 const url = `https://api.github.com/repos/${repo}`;
 const options = {
 headers: process.env.GITHUB_TOKEN
 ? { 'Authorization': `token ${process.env.GITHUB_TOKEN}` }
 : {},
 agent: globalAgent
 };

 const response = await fetch(url, options);
 const data = await response.json();
 const stars = data.stargazers_count || 0;

 cache[repo] = stars;

 return stars;
 } catch (e) {
 return 0;
 }
}

/* ---------------- 工具函数 ---------------- */

function extractRepo(url) {
 const match = url.match(/github\.com\/([^/]+\/[^/)]+)/);
 return match ? match[1] : null;
}

/* ---------------- 解析 Awesome README ---------------- */

function parseAwesomeList(readme, listName) {
 if (!readme) return [];

 const items = [];
 const seen = new Set();

 const regex =
 /^- \[([^\]]+)\]\(https:\/\/github\.com\/([^/\s]+)\/([^/\s\)]+)\)/gm;

 let match;

 while ((match = regex.exec(readme)) !== null) {
 const owner = match[2];
 const repo = match[3];
 const repoName = `${owner}/${repo}`;

 if (seen.has(repoName)) continue;
 seen.add(repoName);

 const url = `https://github.com/${repoName}`;

 const lineStart = match.index;
 const lineEnd = readme.indexOf('\n', lineStart);

 const line = readme.substring(
 lineStart,
 lineEnd > 0 ? lineEnd : readme.length
 );

 let description = line.replace(match[0], '').trim();
 description = description.replace(/^[\s\-:]*/, '').trim();

 if (description.length > 150) {
 description = description.slice(0, 147) + '...';
 }

 items.push({
 name: repoName,
 repoName,
 url,
 awesomeList: listName,
 description: description || `From ${listName}`,
 sourceType: 'tools',
 source: 'awesome_list',
 category: 'tools',
 lastUpdate: new Date().toISOString()
 });

 if (items.length >= 30) break;
 }

 return items;
}

/* ---------------- Star 过滤 ---------------- */

async function filterByStars(projects, cache) {
 const filtered = [];

 const limited = projects.slice(0, 10); // 限制 API 调用

 for (const project of limited) {
 const repo = extractRepo(project.url);
 if (!repo) continue;

 const stars = await getStars(repo, cache);

 if (stars > 1000) {
 project.stars = stars;
 filtered.push(project);
 }
 }

 return filtered;
}

/* ---------------- 主函数 ---------------- */

async function collectAwesomeLists() {
 console.log('📡 抓取 Awesome Lists...');

 const cache = loadCache();

 const lists = [
 {
 name: 'awesome-nodejs',
 url: 'https://cdn.jsdelivr.net/gh/sindresorhus/awesome-nodejs@main/readme.md'
 }
 ];

 const allProjects = [];

 for (const list of lists) {
 try {
 console.log(`📖 读取 ${list.name}...`);

 // 使用 fetch 替代 curl
 const response = await fetch(list.url, { agent: globalAgent });
 const readme = await response.text();

 const projects = parseAwesomeList(readme, list.name);
 allProjects.push(...projects);
 } catch (e) {
 console.error(`⚠️ ${list.name} 读取失败:`, e.message);
 }
 }

 // Star 过滤
 const filtered = await filterByStars(allProjects, cache);

 // 保存缓存
 saveCache(cache);

 console.log(`✅ awesome-nodejs: ${filtered.length} 个项目`);

 return filtered;
}

module.exports = { collectAwesomeLists };
