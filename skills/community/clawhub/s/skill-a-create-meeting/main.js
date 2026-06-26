#!/usr/bin/env node
/**
 * Skill-A: create_meeting — execution-only entry point
 *
 * OpenClaw 负责：
 *   1. 解析自然语言
 *   2. 必要追问（项目归属 / 时间 / 主题等）
 *   3. 调 tencent-meeting-skill 创建会议，拿到 meeting_id / meeting_code / join_url
 *   4. 调用本脚本完成 Gitea 侧落库与邮件内容编排
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
      console.error(result.stdout || result.stderr || `${script} exited with code ${result.status}`);
    }
    process.exit(result.status);
  }

  return result.stdout;
}

const args = process.argv.slice(2);
const command = args[0];

if (!command) {
  console.error('Usage: node main.js <prepare> [args...]');
  console.error('');
  console.error('Command:');
  console.error('  prepare --time ISO8601 --topic TEXT --repo OWNER/REPO --category single|cross-project');
  console.error('          --organizer USERNAME --meeting-id ID --meeting-code CODE --join-url URL');
  console.error('          [--duration 60] [--attendees user1,user2] [--meeting-type ad-hoc|recurring] [--series-id ID]');
  process.exit(1);
}

if (command === 'prepare') {
  const output = runPython('create_meeting.py', args.slice(1));
  process.stdout.write(output);
} else {
  console.error(`Unknown command: ${command}`);
  process.exit(1);
}
