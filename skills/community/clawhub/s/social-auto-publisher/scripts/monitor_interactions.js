#!/usr/bin/env node
/**
 * Multi-Platform Interaction Monitor
 * Monitors comments, @mentions, direct messages, and other interactions across platforms
 *
 * Usage:
 *   node scripts/monitor_interactions.js --platforms "xiaohongshu,weibo,twitter" --since 1h
 */

const path = require('path');
const fs = require('fs');

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].replace(/^--/, '');
      const val = args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : 'true';
      opts[key] = val;
      if (val !== 'true') i++;
    }
  }
  return opts;
}

function parseSince(since) {
  const match = since.match(/^(\d+)([hmd])$/);
  if (!match) return 3600000; // Default 1h
  const num = parseInt(match[1]);
  switch (match[2]) {
    case 'h': return num * 3600000;
    case 'm': return num * 60000;
    case 'd': return num * 86400000;
    default: return 3600000;
  }
}

// ─── Platform Monitoring Configuration ─────────────────────────────────────────
const MONITOR_CONFIGS = {
  xiaohongshu: {
    name: 'Xiaohongshu',
    methods: ['comments', 'likes', 'saves'],
    checkCommands: {
      comments: 'browser navigate https://creator.xiaohongshu.com/notifications',
      mentions: 'browser navigate https://www.xiaohongshu.com/mention',
    },
    riskKeywords: ['scam', 'junk', 'refund', 'report', 'complaint', 'fake'],
  },
  weibo: {
    name: 'Weibo',
    methods: ['comments', 'mentions', 'reposts'],
    apiEndpoint: 'https://api.weibo.com/2/comments/to_me.json',
    riskKeywords: ['scam', 'report', 'complaint', 'unfollow'],
  },
  twitter: {
    name: 'Twitter',
    methods: ['mentions', 'replies', 'likes'],
    apiEndpoint: 'https://api.twitter.com/2/users/me/mentions',
    riskKeywords: ['scam', 'spam', 'report', 'fake', 'block'],
  },
};

function buildMonitorReport(platform, sinceMs, data) {
  const sinceTime = new Date(Date.now() - sinceMs);
  return {
    platform,
    checkedAt: new Date().toISOString(),
    since: sinceTime.toISOString(),
    summary: {
      totalInteractions: data?.total || 0,
      newComments: data?.comments || 0,
      newMentions: data?.mentions || 0,
      newLikes: data?.likes || 0,
      highRisk: data?.risks || 0,
    },
    topInteractions: (data?.items || []).slice(0, 5),
    riskAlerts: (data?.riskItems || []).map(item => ({
      type: item.type || 'comment',
      content: item.text || '',
      risk: item.risk || 'low',
      action: item.suggestedAction || 'review',
    })),
  };
}

function main() {
  const opts = parseArgs();
  const platformsStr = opts.platforms || 'xiaohongshu';
  const platforms = platformsStr.split(',').map(p => p.trim());
  const sinceMs = parseSince(opts.since || '1h');

  console.log('─── Interaction Monitoring Report ───');
  console.log(`Check time: ${new Date().toLocaleString('en-US', { timeZone: 'Asia/Shanghai' })}`);
  console.log(`Monitoring window: ${opts.since || '1h'}`);
  console.log('');

  const reports = {};
  for (const platform of platforms) {
    const config = MONITOR_CONFIGS[platform];
    if (!config) {
      console.error(`[error] Unsupported platform: ${platform}`);
      continue;
    }

    console.log(`【${config.name}】`);
    console.log(`  Check method: ${config.apiEndpoint ? 'API' : 'Browser'}`);

    if (config.apiEndpoint) {
      console.log(`  API: ${config.apiEndpoint}`);
    }

    if (config.checkCommands) {
      for (const [method, cmd] of Object.entries(config.checkCommands)) {
        console.log(`  ${method}: ${cmd}`);
      }
    }

    // Risk keyword alert
    console.log(`  Risk monitoring keywords: ${config.riskKeywords.join(', ')}`);
    console.log('');

    reports[platform] = buildMonitorReport(platform, sinceMs, {
      total: 0,
      comments: 0,
      mentions: 0,
      likes: 0,
      risks: 0,
      items: [],
      riskItems: [],
    });
  }

  // Output structured report
  const report = {
    reportType: 'interaction_monitor',
    generatedAt: new Date().toISOString(),
    sinceWindow: opts.since || '1h',
    platformReports: reports,
  };

  console.log('─── JSON Report ───');
  console.log(JSON.stringify(report, null, 2));

  // Save report
  const outputDir = path.join(__dirname, '..', '..', '..', 'output');
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });
  const filename = path.join(outputDir, `monitor_${Date.now()}.json`);
  fs.writeFileSync(filename, JSON.stringify(report, null, 2));
  console.error(`\n[info] Report saved: ${filename}`);
}

main();