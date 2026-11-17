'use strict';
/**
 * lib/registry-fetch-child.js —— 内置拉包的子进程入口（内部工具，勿直接调用）。
 *
 * 父进程（lib/registry-fetch.js fetchPackageSync）经 stdin 传入 JSON：
 *   { skill: {slug, pkg, version}, opts: {pin, registry}, packDir }
 * stdout 最后一行输出 JSON：{ ok: true, result } 或 { ok: false, error }。
 * 这样安装管线保持同步契约，网络 I/O 仍走同一套异步核心。
 */

const fetchLib = require('./registry-fetch');

async function main() {
  let payload;
  try {
    payload = JSON.parse(require('fs').readFileSync(0, 'utf8'));
  } catch (error) {
    process.stdout.write(JSON.stringify({ ok: false, error: '入参解析失败: ' + error.message }) + '\n');
    return;
  }
  try {
    const result = await fetchLib.fetchPackage(payload.skill, payload.opts || {}, payload.packDir);
    process.stdout.write(JSON.stringify(result.ok ? { ok: true, result } : { ok: false, error: result.error }) + '\n');
  } catch (error) {
    process.stdout.write(JSON.stringify({ ok: false, error: '内置拉包异常: ' + (error && error.message ? error.message : String(error)) }) + '\n');
  }
}

main();
