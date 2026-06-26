#!/usr/bin/env node

// 初始化 ~/.tesla_cn.json 的小工具
// 用法示例：
//   node init-tesla-config.js apiKey="YOUR_API_KEY"

const fs = require('fs');
const path = require('path');

const CONFIG_FILE_NAME = '.tesla_cn.json';

function parseArgs(argv) {
  const result = {};

  for (const token of argv) {
    const eqIndex = token.indexOf('=');
    if (eqIndex === -1) continue;

    const key = token.slice(0, eqIndex);
    let value = token.slice(eqIndex + 1);

    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }

    result[key] = value;
  }

  return result;
}

function main() {
  const args = process.argv.slice(2);
  const parsed = parseArgs(args);

  const apiKey = parsed.apiKey;

  if (!apiKey || !apiKey.trim()) {
    console.error('error');
    console.error('apiKey is required, usage: apiKey="YOUR_API_KEY"');
    console.log(
      JSON.stringify({
        error: 'missing_apiKey',
        message:
          '缺少 apiKey 参数。示例：node init-tesla-config.js apiKey="YOUR_API_KEY"',
      }),
    );
    process.exit(1);
  }

  const homeDir = process.env.HOME || process.env.USERPROFILE;
  if (!homeDir) {
    console.error('error');
    console.error('cannot determine home directory');
    console.log(
      JSON.stringify({
        error: 'no_home_directory',
        message:
          '无法确定用户主目录（HOME/USERPROFILE）。请手动创建 ~/.tesla_cn.json。',
      }),
    );
    process.exit(1);
  }

  const configPath = path.join(homeDir, CONFIG_FILE_NAME);
  const payload = {
    apiKey: apiKey.trim(),
  };

  try {
    fs.writeFileSync(configPath, JSON.stringify(payload, null, 2), {
      encoding: 'utf8',
    });
  } catch (e) {
    console.error('error');
    console.error('failed to write config file');
    console.log(
      JSON.stringify({
        error: 'write_failed',
        message: `写入配置文件失败：${configPath}`,
      }),
    );
    process.exit(1);
  }

  console.log(
    JSON.stringify({
      ok: true,
      file: configPath,
      message: '已写入 ~/.tesla_cn.json，可直接使用 tesla-cn 技能。',
    }),
  );
}

main();

