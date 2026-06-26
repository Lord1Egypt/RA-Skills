#!/usr/bin/env bash
set -euo pipefail

CMD="${1:-}"
MARKER="openclaw-fakeip-patch"

usage() {
  echo "用法:"
  echo "  bash patch-openclaw-global-fakeip.sh status"
  echo "  bash patch-openclaw-global-fakeip.sh inspect"
  echo "  bash patch-openclaw-global-fakeip.sh apply"
  echo "  bash patch-openclaw-global-fakeip.sh revert"
}

get_pkg_dir() {
  if [ -n "${OPENCLAW_PKG_DIR:-}" ]; then
    printf '%s\n' "$OPENCLAW_PKG_DIR"
    return
  fi

  local root=""
  root="$(npm root -g 2>/dev/null || true)"
  if [ -n "$root" ] && [ -d "$root/openclaw" ]; then
    printf '%s\n' "$root/openclaw"
    return
  fi

  local bin=""
  bin="$(command -v openclaw 2>/dev/null || true)"
  if [ -n "$bin" ]; then
    bin="$(readlink -f "$bin" 2>/dev/null || printf '%s' "$bin")"
    local maybe
    maybe="$(dirname "$bin")"
    if [ -f "$maybe/package.json" ]; then
      printf '%s\n' "$maybe"
      return
    fi
  fi

  return 1
}

run_node() {
  local mode="$1"
  local pkg
  pkg="$(get_pkg_dir)" || {
    echo "[ERROR] 找不到 openclaw 安装目录"
    echo "[HINT] 可以手动指定:"
    echo "       OPENCLAW_PKG_DIR=/你的/node_modules/openclaw bash $0 $mode"
    exit 1
  }

  echo "[INFO] package dir: $pkg"

  OPENCLAW_PKG_DIR="$pkg" MODE="$mode" node <<'NODE'
const fs = require('fs');
const path = require('path');

const pkg = process.env.OPENCLAW_PKG_DIR;
const mode = process.env.MODE;
const marker = 'openclaw-fakeip-patch';

function walk(dir, out = []) {
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) {
      if (ent.name === '.git') continue;
      walk(p, out);
    } else if (ent.isFile() && p.endsWith('.js') && !p.includes('.fakeip.')) {
      out.push(p);
    }
  }
  return out;
}

function findCandidates() {
  const files = walk(pkg);
  const out = [];
  for (const file of files) {
    let text = '';
    try {
      text = fs.readFileSync(file, 'utf8');
    } catch {
      continue;
    }

    if (
      text.includes('fetchWithWebToolsNetworkGuard({') &&
      text.includes('runWebFetch') &&
      (text.includes('name:"web_fetch"') || text.includes('name: "web_fetch"'))
    ) {
      out.push({ file, text });
    }
  }
  return out;
}

function findPatchPoint(text) {
  const lines = text.split('\n');

  const starts = [];
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('fetchWithWebToolsNetworkGuard({')) {
      starts.push(i);
    }
  }

  if (starts.length !== 1) {
    throw new Error(`目标调用块起点数量异常: ${starts.length}`);
  }

  const start = starts[0];
  let timeoutIdx = -1;
  let initIdx = -1;

  for (let i = start; i < Math.min(lines.length, start + 40); i++) {
    if (
      timeoutIdx === -1 &&
      (
        lines[i].includes('timeoutSeconds: params.timeoutSeconds') ||
        lines[i].includes('timeoutSeconds:params.timeoutSeconds')
      )
    ) {
      timeoutIdx = i;
      continue;
    }

    if (
      timeoutIdx !== -1 &&
      (
        /^\s*init:\s*\{\s*$/.test(lines[i]) ||
        lines[i].includes('init:{') ||
        lines[i].includes('init: {')
      )
    ) {
      initIdx = i;
      break;
    }
  }

  if (timeoutIdx === -1 || initIdx === -1 || initIdx <= timeoutIdx) {
    throw new Error('没找到预期的 timeoutSeconds -> init 结构');
  }

  return { lines, start, timeoutIdx, initIdx };
}

function showPatchWindow(text) {
  const { lines, start, timeoutIdx, initIdx } = findPatchPoint(text);

  console.log('--- exact patch window ---');
  for (let i = Math.max(0, start - 2); i <= Math.min(lines.length - 1, initIdx + 4); i++) {
    console.log(lines[i]);
  }

  console.log('');
  console.log('--- exact insert line ---');
  console.log(lines[timeoutIdx]);
  console.log('>>> WILL INSERT BELOW THIS LINE <<<');
  console.log(lines[initIdx]);
}

const candidates = findCandidates();

if (candidates.length === 0) {
  console.log('[STATUS] no-candidate');
  process.exit(0);
}

if (candidates.length > 1) {
  console.log('[STATUS] multiple-candidates');
  for (const c of candidates) {
    console.log(' - ' + c.file + (c.text.includes(marker) ? ' [patched]' : ' [clean]'));
  }
  process.exit(0);
}

const { file, text } = candidates[0];

if (mode === 'status') {
  console.log('[STATUS] ' + (text.includes(marker) ? 'patched' : 'clean'));
  console.log('[TARGET] ' + file);
  process.exit(0);
}

if (mode === 'inspect') {
  console.log('[STATUS] ' + (text.includes(marker) ? 'patched' : 'clean'));
  console.log('[TARGET] ' + file);
  console.log('');

  try {
    showPatchWindow(text);
  } catch (e) {
    console.log('[INSPECT-ERROR] ' + e.message);
    process.exit(1);
  }

  process.exit(0);
}

if (mode === 'apply') {
  if (text.includes(marker)) {
    console.log('[INFO] 已经打过补丁，跳过');
    console.log('[TARGET] ' + file);
    process.exit(0);
  }

  const { lines, initIdx } = findPatchPoint(text);
  const indent = (lines[initIdx].match(/^(\s*)/) || ['', ''])[1];
  const patchLine = `${indent}policy: { allowRfc2544BenchmarkRange: true }, // ${marker}`;

  const backup = file + '.fakeip.bak';
  if (!fs.existsSync(backup)) {
    fs.copyFileSync(file, backup);
  }

  lines.splice(initIdx, 0, patchLine);
  fs.writeFileSync(file, lines.join('\n'), 'utf8');

  const verify = fs.readFileSync(file, 'utf8');
  if (!verify.includes(marker)) {
    throw new Error('补丁校验失败');
  }

  console.log('[OK] 已应用补丁');
  console.log('[TARGET] ' + file);
  console.log('[BACKUP] ' + backup);
  process.exit(0);
}

if (mode === 'revert') {
  if (!text.includes(marker)) {
    console.log('[INFO] 当前未打补丁，无需回滚');
    console.log('[TARGET] ' + file);
    process.exit(0);
  }

  const lines = text.split('\n');
  const before = lines.length;
  const next = lines.filter(line => !line.includes(marker));
  const removed = before - next.length;

  if (removed !== 1) {
    throw new Error(`预期删除 1 行补丁，实际删除 ${removed} 行`);
  }

  const backup = file + '.fakeip.revert.bak';
  if (!fs.existsSync(backup)) {
    fs.copyFileSync(file, backup);
  }

  fs.writeFileSync(file, next.join('\n'), 'utf8');

  const verify = fs.readFileSync(file, 'utf8');
  if (verify.includes(marker)) {
    throw new Error('回滚后仍检测到补丁标记');
  }

  console.log('[OK] 已回滚补丁');
  console.log('[TARGET] ' + file);
  console.log('[BACKUP] ' + backup);
  process.exit(0);
}

throw new Error('未知模式');
NODE
}

case "$CMD" in
  status) run_node status ;;
  inspect) run_node inspect ;;
  apply) run_node apply ;;
  revert) run_node revert ;;
  *)
    usage
    exit 1
    ;;
esac
