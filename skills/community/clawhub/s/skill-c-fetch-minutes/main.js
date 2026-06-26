#!/usr/bin/env node
/**
 * Skill-C: fetch_minutes — CLI entry point
 *
 * 命令：
 *   node main.js scan                       扫描三类待处理会议（A/B/C类）
 *   node main.js set-waiting   [options]    brief-sent → waiting-transcript
 *   node main.js set-failed    [options]    waiting-transcript → transcript-failed
 *   node main.js commit-content [options]   提交四个文件，status → draft-pending-review
 *
 * OpenClaw 负责：
 *   - 触发 scan，读取三类会议
 *   - 判断 A 类会议是否已结束
 *   - 调用 tencent-meeting-skill 拉取转录与 AI 智能纪要（三层降级）
 *   - 对 C 类从 Gitea 读取已有 transcript.md
 *   - 两阶段 AI issue 抽取，生成四个文件内容写入 /tmp
 *   - 调用 imap-smtp-email 发送通知邮件
 *
 * Skill-C 只负责：
 *   - Gitea 状态读写
 *   - 文件提交
 *   - 日志写入
 *   - 邮件参数封装
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
    扫描所有 Gitea 受管仓库，返回三类待处理会议：
      class_a: status=brief-sent（需判断是否已结束）
      class_b: status=waiting-transcript（需拉取转录或判断超时）
      class_c: status=transcript-failed 且 transcript.md 已存在

  set-waiting --repo OWNER/REPO --meeting-dir DIR
    将指定会议 brief-sent → waiting-transcript
    记录 transcript_started_at 时间戳

  set-failed --repo OWNER/REPO --meeting-dir DIR --organizer-email EMAIL
    将指定会议 waiting-transcript → transcript-failed
    返回发给组织者的手动上传通知邮件参数

  commit-content --repo OWNER/REPO --meeting-dir DIR --topic TEXT
    --organizer-email EMAIL
    --transcript-file PATH
    --minutes-file PATH
    --draft-issue-file PATH
    [--ai-summary-file PATH]
    [--source ai_summary|transcript_only|manual_upload]
    将四个文件提交到 Gitea，status → draft-pending-review
    返回发给组织者的审核通知邮件参数
`.trim();

if (!command) {
  console.error(USAGE);
  process.exit(1);
}

const commandMap = {
  'scan':           'scan.py',
  'set-waiting':    'set_waiting.py',
  'set-failed':     'set_failed.py',
  'commit-content': 'commit_content.py',
};

if (!commandMap[command]) {
  console.error(`Unknown command: ${command}\n\n${USAGE}`);
  process.exit(1);
}

const output = runPython(commandMap[command], args.slice(1));
process.stdout.write(output);
