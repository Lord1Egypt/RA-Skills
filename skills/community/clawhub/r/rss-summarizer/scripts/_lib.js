import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'fs';
import Parser from 'rss-parser';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const skillDir = join(__dirname, '..');
const dataDir = join(skillDir, 'data');
const subsFile = join(dataDir, 'subscriptions.json');
const configFile = join(dataDir, 'config.json');

if (!existsSync(dataDir)) mkdirSync(dataDir, { recursive: true });

const defaultConfig = {
  summaryMode: 'medium',
  language: 'zh',
  maxItems: 10,
  filters: []
};

export function loadConfig() {
  if (existsSync(configFile)) {
    try {
      return { ...defaultConfig, ...JSON.parse(readFileSync(configFile, 'utf-8')) };
    } catch (e) {
      return defaultConfig;
    }
  }
  return defaultConfig;
}

export function saveConfig(config) {
  writeFileSync(configFile, JSON.stringify(config, null, 2));
}

export function loadSubs() {
  if (existsSync(subsFile)) {
    try {
      return JSON.parse(readFileSync(subsFile, 'utf-8'));
    } catch (e) {
      return [];
    }
  }
  return [];
}

export function saveSubs(subs) {
  writeFileSync(subsFile, JSON.stringify(subs, null, 2));
}

export function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substring(2, 7);
}

export async function addSubscription(url, name) {
  const subs = loadSubs();
  if (subs.some(s => s.url === url)) {
    return { success: false, error: '该订阅源已存在' };
  }
  const newSub = {
    id: generateId(),
    url,
    name: name || url,
    addedAt: new Date().toISOString(),
    lastFetchedAt: null
  };
  subs.push(newSub);
  saveSubs(subs);
  return { success: true, message: '订阅源已添加', subscription: newSub };
}

export function listSubscriptions() {
  const subs = loadSubs();
  return { success: true, subscriptions: subs };
}

export function removeSubscription(id) {
  const subs = loadSubs();
  const idx = subs.findIndex(s => s.id === id);
  if (idx === -1) {
    return { success: false, error: '未找到该订阅源' };
  }
  subs.splice(idx, 1);
  saveSubs(subs);
  return { success: true, message: '已删除' };
}

export async function fetchSubscriptions(targetId = null, format = 'markdown', notify = false, sendFn = null) {
  const subs = loadSubs();
  const targets = targetId ? subs.filter(s => s.id === targetId) : subs;
  if (targets.length === 0) {
    return { success: false, error: '没有找到订阅源' };
  }

  const config = loadConfig();
  const parser = new Parser();
  const results = [];

  for (const sub of targets) {
    try {
      const feed = await parser.parseURL(sub.url);
      let items = feed.items;

      if (config.filters && config.filters.length > 0) {
        items = items.filter(item => {
          const text = (item.title + ' ' + (item.contentSnippet || '')).toLowerCase();
          return config.filters.some(f => text.includes(f.toLowerCase()));
        });
      }

      items = items.slice(0, config.maxItems);

      results.push({
        subscription: sub.name,
        feedTitle: feed.title,
        items: items.map(item => ({
          title: item.title,
          link: item.link,
          pubDate: item.pubDate,
          contentSnippet: item.contentSnippet
        }))
      });

      sub.lastFetchedAt = new Date().toISOString();
      saveSubs(subs);
    } catch (e) {
      results.push({
        subscription: sub.name,
        error: e.message
      });
    }
  }

  if (notify && sendFn) {
    try {
      const msg = results.map(r =>
        `📰 ${r.subscription}${r.feedTitle ? ` (${r.feedTitle})` : ''}:\n` +
        (r.error ? `❌ 错误: ${r.error}` :
          (r.items || []).slice(0, 3).map(i => `• ${i.title}\n  ${i.link}`).join('\n') +
          (r.items && r.items.length > 3 ? `\n... 等 ${r.items.length} 条` : '')
        )
      ).join('\n\n');
      await sendFn(msg);
    } catch (e) {
      // ignore
    }
  }

  // Format output
  let output;
  if (format === 'json') {
    output = { results };
  } else if (format === 'plain') {
    const text = results.map(r =>
      `${r.subscription}${r.feedTitle ? ` - ${r.feedTitle}` : ''}:\n` +
      (r.error ? `错误: ${r.error}` :
        (r.items || []).map(i => `${i.title}\n${i.link}\n`).join('\n')
      )
    ).join('\n');
    output = { text };
  } else { // markdown
    const text = results.map(r =>
      `## ${r.subscription}${r.feedTitle ? ` - ${r.feedTitle}` : ''}\n` +
      (r.error ? `❌ ${r.error}` :
        (r.items || []).map(i => `- [${i.title}](${i.link})`).join('\n')
      )
    ).join('\n\n');
    output = { text };
  }

  return { success: true, ...output };
}

export function configure(newConfig) {
  const config = loadConfig();
  if (newConfig.summaryMode !== undefined) config.summaryMode = newConfig.summaryMode;
  if (newConfig.language !== undefined) config.language = newConfig.language;
  if (newConfig.maxItems !== undefined) config.maxItems = newConfig.maxItems;
  if (newConfig.filters !== undefined) config.filters = newConfig.filters;
  saveConfig(config);
  return { success: true, message: '设置已保存', config };
}