#!/usr/bin/env node
/**
 * Skill-B: pre_brief — CLI entry point
 *
 * 命令：
 *   node main.js scan                          扫描所有仓库，返回待发简报会议列表
 *   node main.js commit [options]              保存简报文件，更新 meta.yaml 状态
 *
 * OpenClaw 负责：
 *   - 读取 scan 结果
 *   - 调用 gitea-routine-report 拉取 Gitea 活动数据
 *   - 作为 AI 生成 ai_overview / ai_suggestion / member_summaries / risk_notes
 *   - 调用 render_email.py 渲染 HTML
 *   - 调用 imap-smtp-email 发送简报邮件
 *
 * Skill-B 只负责：
 *   - 扫描仓库元数据
 *   - 计算时间窗口
 *   - 保存文件到 Gitea
 *   - 更新 meta.yaml 状态
 *   - 写日志
 */

const { spawnSync } = require('child_process');
const path = require('path');

const SCRIPT_DIR = path.join(__dirname, 'scripts');

function runPython(script, args) {
  const result = spawnSync(
    'python3',
    [path.join(SCRIPT_DIR, script), ...args],
    {
      encoding: 'utf8',
      stdio: ['inherit', 'pipe', 'pipe'],
      env: process.env,
    }
  );

  if (result.error) {
    console.error(`Failed to launch ${script}:`, result.error.message);
    process.exit(1);
  }

  if (result.stderr && result.stderr.trim()) {
    process.stderr.write(result.stderr);
  }

  if (result.status !== 0) {
    try {
      const parsed = JSON.parse(result.stdout);
      if (parsed.error) {
        console.error(`Error: ${parsed.error}`);
      } else {
        console.log(result.stdout);
      }
    } catch {
      console.error(
        result.stdout || result.stderr || `${script} exited with code ${result.status}`
      );
    }
    process.exit(result.status);
  }

  return result.stdout;
}

const args = process.argv.slice(2);
const command = args[0];

if (!command) {
  console.error('Usage: node main.js <scan|commit> [args...]');
  console.error('');
  console.error('Commands:');
  console.error('  scan');
  console.error('    → 扫描所有受管仓库，返回待发简报会议列表（含时间窗口）');
  console.error('');
  console.error('  commit --repo OWNER/REPO --meeting-dir DIR [options]');
  console.error('    --topic TEXT              会议主题');
  console.error('    --html-file PATH          渲染好的 HTML 简报文件路径');
  console.error('    --attendee-emails LIST    逗号分隔的参会人邮箱');
  console.error('    --since YYYY-MM-DD        活动统计开始日期');
  console.error('    --until YYYY-MM-DD        活动统计结束日期');
  console.error('    --mark-only               只更新状态，不保存简报文件（改期会议用）');
  process.exit(1);
}

if (command === 'scan') {
  const output = runPython('scan.py', args.slice(1));
  process.stdout.write(output);
} else if (command === 'commit') {
  const output = runPython('commit_brief.py', args.slice(1));
  process.stdout.write(output);
} else {
  console.error(`Unknown command: ${command}`);
  process.exit(1);
}
