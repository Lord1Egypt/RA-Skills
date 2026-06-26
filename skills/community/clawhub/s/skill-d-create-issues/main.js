#!/usr/bin/env node
/**
 * Skill-D: create_issues — CLI entry point
 *
 * 命令：
 *   node main.js check          [options]   校验前置条件，返回 confirmed_issue.md 内容
 *   node main.js create-issues  [options]   批量建 Gitea issue + 依赖回填
 *   node main.js finish         [options]   收尾：更新状态、写日志、返回邮件参数
 *
 * OpenClaw 负责：
 *   - 被 webhook（方式A）或对话（方式B）触发
 *   - 调用 check 验证前置条件
 *   - 解析 confirmed_issue.md 内容，提取结构化 action items
 *   - 判断 single vs cross-project
 *   - 单项目：调用 create-issues 批量建 issue
 *   - 调用 finish 获取邮件参数
 *   - 调用 imap-smtp-email 发送正式纪要邮件 + 个人任务通知
 *   - 跨项目：调用 finish，再调用 imap-smtp-email 发组织者建议邮件
 *
 * Skill-D 只负责：
 *   - 前置条件校验
 *   - Gitea issue 创建与依赖回填
 *   - meta.yaml 状态更新
 *   - 日志写入
 *   - 邮件 HTML 构建与参数封装
 *
 * webhook 监听服务（独立进程）：
 *   python3 scripts/webhook.py
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
  check --repo OWNER/REPO --meeting-dir DIR
    校验前置条件（status==draft-pending-review，confirmed_issue.md 存在）
    返回 confirmed_issue.md 内容、minutes.md 内容、meta 信息

  create-issues --repo OWNER/REPO --meeting-dir DIR --topic TEXT
    --issues-json JSON_ARRAY_STRING
    批量在 Gitea 建 issue，完成依赖回填
    返回 created / failed 列表

  finish --repo OWNER/REPO --meeting-dir DIR --topic TEXT
    --category single|cross-project
    --organizer-email EMAIL --attendee-emails EMAIL_LIST
    [--created-issues-json JSON]
    [--failed-issues-json JSON]
    更新 meta.yaml → minutes-published，写日志
    返回三种邮件参数（minutes_email / assignee_emails / cross_email）
`.trim();

if (!command) {
  console.error(USAGE);
  process.exit(1);
}

const commandMap = {
  'check':          'check.py',
  'create-issues':  'create_issues.py',
  'finish':         'finish.py',
};

if (!commandMap[command]) {
  console.error(`Unknown command: ${command}\n\n${USAGE}`);
  process.exit(1);
}

const output = runPython(commandMap[command], args.slice(1));
process.stdout.write(output);
