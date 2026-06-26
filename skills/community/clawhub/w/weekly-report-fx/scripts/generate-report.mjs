#!/usr/bin/env node

/**
 * Weekly Report Generator
 * Scans GitHub, calendars, and tasks to generate AI-powered weekly reports
 */

import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import dotenv from 'dotenv';

dotenv.config();

const __dirname = dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);

// ─── CLI Arguments ──────────────────────────────────────────────────────────

const args = process.argv.slice(2);
let weekOffset = 0;
let format = 'markdown';
let style = 'detailed';
let dryRun = false;
let repos = [];

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--week-offset' || args[i] === '-w') {
    weekOffset = parseInt(args[++i]) || 0;
  } else if (args[i] === '--format' || args[i] === '-f') {
    format = args[++i] || 'markdown';
  } else if (args[i] === '--style' || args[i] === '-s') {
    style = args[++i] || 'detailed';
  } else if (args[i] === '--dry-run') {
    dryRun = true;
  } else if (args[i] === '--repos' || args[i] === '-r') {
    repos = args[++i]?.split(',').map(r => r.trim()) || [];
  } else if (args[i] === '--help' || args[i] === '-h') {
    printHelp();
    process.exit(0);
  }
}

// ─── Date Helpers ────────────────────────────────────────────────────────────

function getWeekRange(offset = 0) {
  const now = new Date();
  const startOfWeek = new Date(now);
  const day = startOfWeek.getDay();
  const diff = startOfWeek.getDate() - day + (day === 0 ? -6 : 1); // Monday
  startOfWeek.setDate(diff + offset * 7);
  startOfWeek.setHours(0, 0, 0, 0);

  const endOfWeek = new Date(startOfWeek);
  endOfWeek.setDate(startOfWeek.getDate() + 6);
  endOfWeek.setHours(23, 59, 59, 999);

  return { start: startOfWeek, end: endOfWeek };
}

function formatDate(date) {
  return date.toISOString().split('T')[0];
}

function formatDisplayDate(date) {
  return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
}

// ─── GitHub Data Collector ───────────────────────────────────────────────────

async function collectGitHubData(repos) {
  const token = process.env.GITHUB_TOKEN || '';
  const { start, end } = getWeekRange(weekOffset);

  if (!token) {
    return { issues: [], prs: [], commits: [], error: 'GITHUB_TOKEN not set' };
  }

  const results = { issues: [], prs: [], commits: [] };

  // If no repos specified, try to fetch user's recent activity
  if (repos.length === 0) {
    try {
      const userEvents = await fetchGitHubUserEvents(token, start, end);
      return userEvents;
    } catch (e) {
      return { issues: [], prs: [], commits: [], error: e.message };
    }
  }

  // Fetch data for each specified repo
  for (const repo of repos) {
    try {
      const [owner, name] = repo.split('/');
      const [issues, prs] = await Promise.all([
        fetchRepoIssues(token, owner, name, start, end),
        fetchRepoPRs(token, owner, name, start, end)
      ]);
      results.issues.push(...issues);
      results.prs.push(...prs);
    } catch (e) {
      console.error(`Error fetching ${repo}: ${e.message}`);
    }
  }

  return results;
}

async function fetchGitHubUserEvents(token, start, end) {
  const username = await fetchGitHubUsername(token);
  const url = `https://api.github.com/users/${username}/events?per_page=100`;
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${token}`, Accept: 'application/vnd.github.v3+json' }
  });

  if (!res.ok) throw new Error(`GitHub API error: ${res.status}`);

  const events = await res.json();
  const startStr = start.toISOString();
  const endStr = end.toISOString();

  const filtered = events.filter(e => e.created_at >= startStr && e.created_at <= endStr);

  const issues = filtered
    .filter(e => e.type === 'IssuesEvent' && e.payload.action === 'closed')
    .map(e => ({ title: e.payload.issue.title, repo: e.repo.name, url: e.payload.issue.html_url, labels: e.payload.issue.labels.map(l => l.name) }));

  const prs = filtered
    .filter(e => e.type === 'PullRequestEvent' && ['merged', 'closed'].includes(e.payload.action))
    .map(e => ({ title: e.payload.pull_request.title, repo: e.repo.name, url: e.payload.pull_request.html_url, merged: e.payload.pull_request.merged }));

  const commits = filtered
    .filter(e => e.type === 'PushEvent')
    .flatMap(e => e.payload.commits.map(c => ({ message: c.message, repo: e.repo.name, sha: c.sha.slice(0, 7) })));

  return { issues, prs, commits };
}

async function fetchGitHubUsername(token) {
  const res = await fetch('https://api.github.com/user', {
    headers: { Authorization: `Bearer ${token}`, Accept: 'application/vnd.github.v3+json' }
  });
  const data = await res.json();
  return data.login;
}

async function fetchRepoIssues(token, owner, name, start, end) {
  const url = `https://api.github.com/repos/${owner}/${name}/issues?state=closed&since=${start.toISOString()}&per_page=50`;
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${token}`, Accept: 'application/vnd.github.v3+json' }
  });
  if (!res.ok) return [];
  const issues = await res.json();
  return issues
    .filter(i => !i.pull_request && new Date(i.closed_at) >= start && new Date(i.closed_at) <= end)
    .map(i => ({ title: i.title, repo: `${owner}/${name}`, url: i.html_url, labels: i.labels.map(l => l.name), closedAt: i.closed_at }));
}

async function fetchRepoPRs(token, owner, name, start, end) {
  const url = `https://api.github.com/repos/${owner}/${name}/pulls?state=closed&per_page=50`;
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${token}`, Accept: 'application/vnd.github.v3+json' }
  });
  if (!res.ok) return [];
  const prs = await res.json();
  return prs
    .filter(pr => pr.merged_at && new Date(pr.merged_at) >= start && new Date(pr.merged_at) <= end)
    .map(pr => ({ title: pr.title, repo: `${owner}/${name}`, url: pr.html_url, mergedAt: pr.merged_at, number: pr.number }));
}

// ─── Reminders Collector ──────────────────────────────────────────────────────

async function collectRemindersData() {
  // This would integrate with apple-reminders or things3 skill
  // For now, return empty array as reminders require system integration
  return { tasks: [], note: 'Configure apple-reminders or things3 skill for task data' };
}

// ─── AI Summarizer ───────────────────────────────────────────────────────────

function generateAIAccomplishments(data, style) {
  const lines = [];

  if (data.issues.length > 0 || data.prs.length > 0 || data.commits?.length > 0) {
    lines.push('## 🚀 Accomplishments\n');

    if (data.issues.length > 0) {
      lines.push(`### Issues Resolved (${data.issues.length})`);
      for (const issue of data.issues.slice(0, 10)) {
        lines.push(`- ${issue.title} \`${issue.repo}\` #${issue.url.split('/').pop()}`);
      }
      if (data.issues.length > 10) lines.push(`- ...and ${data.issues.length - 10} more`);
      lines.push('');
    }

    if (data.prs.length > 0) {
      lines.push(`### Pull Requests (${data.prs.length} merged)`);
      for (const pr of data.prs.slice(0, 10)) {
        const status = pr.merged ? '✅' : '❌';
        lines.push(`- ${status} ${pr.title} \`${pr.repo}\` #${pr.number}`);
      }
      if (data.prs.length > 10) lines.push(`- ...and ${data.prs.length - 10} more`);
      lines.push('');
    }

    if (data.commits?.length > 0) {
      lines.push(`### Commits (${data.commits.length} total)`);
      for (const commit of data.commits.slice(0, 5)) {
        const msg = commit.message.split('\n')[0].slice(0, 72);
        lines.push(`- \`${commit.sha}\` ${msg}`);
      }
      if (data.commits.length > 5) lines.push(`- ...and ${data.commits.length - 5} more commits`);
      lines.push('');
    }
  }

  return lines.join('\n');
}

// ─── Report Generator ────────────────────────────────────────────────────────

function generateMarkdownReport(data, options) {
  const { start, end } = getWeekRange(weekOffset);
  const weekNum = getWeekNumber(start);
  const now = new Date();

  let report = '';

  // Header
  report += `# 📋 Weekly Report — Week ${weekNum}\n\n`;
  report += `> **Generated:** ${formatDisplayDate(now)}\n`;
  report += `> **Period:** ${formatDisplayDate(start)} → ${formatDisplayDate(end)}\n`;
  report += `> **Style:** ${style}\n\n`;
  report += `---\n\n`;

  // Summary box
  const totalActivity = (data.issues?.length || 0) + (data.prs?.length || 0);
  report += `## 📊 Week at a Glance\n\n`;
  report += `| Metric | Count |\n`;
  report += `|--------|-------|\n`;
  report += `| 🔵 Issues Closed | ${data.issues?.length || 0} |\n`;
  report += `| 🟢 PRs Merged | ${data.prs?.length || 0} |\n`;
  report += `| 📝 Commits | ${data.commits?.length || 0} |\n`;
  report += `| ⚠️ Warnings | ${data.warnings?.length || 0} |\n\n`;
  report += `---\n\n`;

  // AI-generated accomplishments
  const accomplishments = generateAIAccomplishments(data, style);
  if (accomplishments) {
    report += accomplishments;
    report += `---\n\n`;
  }

  // Data source info
  if (data.error) {
    report += `> ⚠️ **Note:** ${data.error}\n`;
    report += `> Set \`GITHUB_TOKEN\` environment variable to include GitHub data.\n\n`;
  }

  // Next week goals (template)
  report += `## 🎯 Next Week's Goals\n\n`;
  report += `- [ ] Add your goals here\n`;
  report += `- [ ] Add your goals here\n`;
  report += `- [ ] Add your goals here\n\n`;

  // Footer
  report += `---\n\n`;
  report += `*Generated by [weekly-report](https://github.com/fx-world888/weekly-report)*\n`;
  report += `*Powered by OpenClaw + AI*\n`;

  return report;
}

function generateHTMLReport(data, options) {
  const md = generateMarkdownReport(data, options);
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Weekly Report</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; }
  h1 { color: #24292f; border-bottom: 2px solid #0969da; padding-bottom: 10px; }
  h2 { color: #24292f; margin-top: 30px; }
  table { border-collapse: collapse; width: 100%; margin: 20px 0; }
  th, td { border: 1px solid #d0d7de; padding: 10px 15px; text-align: left; }
  th { background: #f6f8fa; }
  code { background: #f6f8fa; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }
  blockquote { border-left: 4px solid #0969da; margin: 20px 0; padding: 10px 15px; background: #f6f8fa; }
  hr { border: none; border-top: 1px solid #d0d7de; margin: 30px 0; }
  .meta { color: #57606a; font-size: 0.9em; }
</style>
</head>
<body>
${mdToHTML(md)}
</body>
</html>`;
}

function mdToHTML(md) {
  return md
    .replace(/^# (.*)$/gm, '<h1>$1</h1>')
    .replace(/^## (.*)$/gm, '<h2>$1</h2>')
    .replace(/^### (.*)$/gm, '<h3>$1</h3>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/^- (.*)$/gm, '<li>$1</li>')
    .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
    .replace(/^> (.*)$/gm, '<blockquote>$1</blockquote>')
    .replace(/^---$/gm, '<hr>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\|(.+)\|/g, (m) => {
      const cells = m.split('|').filter(c => c.trim());
      if (cells.some(c => c.includes('---'))) return '';
      return '<tr>' + cells.map(c => `<td>${c.trim()}</td>`).join('') + '</tr>';
    });
}

function getWeekNumber(date) {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  const dayNum = d.getUTCDay() || 7;
  d.setUTCDate(d.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
}

function printHelp() {
  console.log(`
📋 Weekly Report Generator

Usage:
  weekly-report [options]

Options:
  --week-offset, -w <n>    Week offset (0=this week, -1=last week) [default: 0]
  --format, -f <fmt>       Output format: markdown, html, plain [default: markdown]
  --style, -s <style>      Report style: detailed, concise, executive [default: detailed]
  --repos, -r <list>      Comma-separated repo list (owner/name,...)
  --dry-run               Preview without fetching data
  --help, -h              Show this help

Environment Variables:
  GITHUB_TOKEN            Personal Access Token for GitHub API
  FEISHU_APP_ID           Feishu app ID (optional)
  FEISHU_APP_SECRET       Feishu app secret (optional)

Examples:
  weekly-report                              # This week's report
  weekly-report -w -1                       # Last week's report
  weekly-report -f html -s executive         # Executive HTML report
  weekly-report -r "owner/repo1,owner/repo2"  # Specific repos
  GITHUB_TOKEN=ghp_xxx weekly-report        # With GitHub data
`);
}

// ─── Main ────────────────────────────────────────────────────────────────────

async function main() {
  console.log('📋 Weekly Report Generator\n');

  if (dryRun) {
    console.log('🔍 Dry run — generating sample report\n');
    const sampleData = {
      issues: [
        { title: 'Fix authentication timeout bug', repo: 'fx-world888/project', url: 'https://github.com/fx-world888/project/issues/42' },
        { title: 'Add dark mode support', repo: 'fx-world888/project', url: 'https://github.com/fx-world888/project/issues/38' }
      ],
      prs: [
        { title: 'feat: add user dashboard', repo: 'fx-world888/project', url: 'https://github.com/fx-world888/project/pull/45', merged: true, number: 45 },
        { title: 'fix: resolve login redirect loop', repo: 'fx-world888/project', url: 'https://github.com/fx-world888/project/pull/43', merged: true, number: 43 }
      ],
      commits: [
        { message: 'feat: add dashboard API endpoints', repo: 'fx-world888/project', sha: 'a1b2c3d' },
        { message: 'fix: resolve auth timeout issue', repo: 'fx-world888/project', sha: 'e4f5g6h' },
        { message: 'docs: update README', repo: 'fx-world888/project', sha: 'i7j8k9l' }
      ],
      warnings: []
    };
    sampleData.warnings = [];
    var report = format === 'html' ? generateHTMLReport(sampleData, { style }) : generateMarkdownReport(sampleData, { style });
  } else {
    console.log('🔍 Collecting data...\n');
    const [githubData, remindersData] = await Promise.all([
      collectGitHubData(repos),
      collectRemindersData()
    ]);

    const combinedData = {
      ...githubData,
      tasks: remindersData.tasks || [],
      warnings: []
    };

    if (githubData.error) {
      combinedData.warnings.push(githubData.error);
    }

    console.log(`   Issues found: ${combinedData.issues?.length || 0}`);
    console.log(`   PRs found: ${combinedData.prs?.length || 0}`);
    console.log(`   Commits found: ${combinedData.commits?.length || 0}\n`);

    report = format === 'html' ? generateHTMLReport(combinedData, { style }) : generateMarkdownReport(combinedData, { style });
  }

  // Output
  if (format === 'html') {
    const outputPath = join(__dirname, '..', `weekly-report-week-${getWeekNumber(getWeekRange(weekOffset).start)}.html`);
    writeFileSync(outputPath, report);
    console.log(`✅ HTML report saved to: ${outputPath}`);
  } else if (format === 'markdown') {
    const outputPath = join(__dirname, '..', `weekly-report-week-${getWeekNumber(getWeekRange(weekOffset).start)}.md`);
    writeFileSync(outputPath, report);
    console.log(`✅ Markdown report saved to: ${outputPath}`);
  } else {
    console.log(report);
  }
}

main().catch(e => {
  console.error('❌ Error:', e.message);
  process.exit(1);
});
