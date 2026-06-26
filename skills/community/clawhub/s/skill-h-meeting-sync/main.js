#!/usr/bin/env node
/**
 * Skill-H: meeting_sync — CLI entry point
 *
 * 命令：
 *   node main.js scan                          扫描 Gitea 所有活跃会议，返回供三向对比的数据
 *   node main.js cancel        [options]       标记会议为已取消
 *   node main.js reschedule    [options]       处理会议改期（更新旧目录 + 创建新目录）
 *   node main.js create-pending [options]      在 aifusion-meta 创建 repo:pending 占位记录
 *   node main.js archive                       归档超过 30 天的 cancelled/rescheduled 目录
 *
 * OpenClaw 负责：
 *   - 触发 scan
 *   - 调用 tencent-meeting-skill 获取腾讯会议列表
 *   - 做三向对比分析
 *   - 根据分析结果调用对应命令
 *   - 调用 imap-smtp-email 发送通知邮件
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

const USAGE = `
Usage: node main.js <command> [options]

Commands:
  scan
    扫描所有 Gitea 受管仓库，返回 status ∈ {scheduled, brief-sent} 的活跃会议列表

  cancel --repo OWNER/REPO --meeting-dir DIR --attendee-emails LIST
    [--cancel-reason TEXT]
    将指定会议标记为 cancelled，返回取消通知邮件参数

  reschedule --repo OWNER/REPO --old-meeting-dir DIR
    --new-time ISO8601 --new-meeting-id ID --new-meeting-code CODE --new-join-url URL
    --attendee-emails LIST
    更新旧目录为 rescheduled，创建新时间目录，返回改期通知邮件参数

  create-pending --meeting-id ID --meeting-code CODE --topic TEXT
    --time ISO8601 --join-url URL [--duration 60]
    在 aifusion-meta 创建 repo:pending 占位记录，返回待确认通知邮件参数

  archive
    归档所有受管仓库中 status ∈ {cancelled, rescheduled} 且超过 30 天的会议目录
`.trim();

if (!command) {
  console.error(USAGE);
  process.exit(1);
}

const commandMap = {
  scan:             'scan.py',
  cancel:           'cancel.py',
  reschedule:       'reschedule.py',
  'create-pending': 'create_pending.py',
  archive:          'archive.py',
};

if (!commandMap[command]) {
  console.error(`Unknown command: ${command}\n\n${USAGE}`);
  process.exit(1);
}

const output = runPython(commandMap[command], args.slice(1));
process.stdout.write(output);
