/**
 * 轮询主循环：独立后台进程跑，不占 OpenClaw event loop。
 *
 * 由 card-tools.mjs startPollProcess() 启动。
 * - 每 N 秒调一次 pollEvents.main()
 * - 检测到 stop 信号（poll_state.active=False）→ 自然退出
 * - 不写 stdout（spawn 启动后没人读）
 * - 异常写 data/poll_loop.log
 * - 无最大时长限制，一直轮询直到流程结束
 */
import { writeFileSync, readFileSync, existsSync, unlinkSync, appendFileSync, statSync, readdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';
import { main as pollEventsMain } from './poll-events.mjs';
import { DATA_DIR, _ensureDir, _skillCfg, pollStateLoad, pollStopped, setRuntimeChannel, _webchatBuffer, webchatFlush, GATEWAY_URL, _gatewayToken } from './card-tools.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const LOG_PATH = join(DATA_DIR, 'poll_loop.log');
const PID_PATH = join(DATA_DIR, 'poll_loop.pid');
const LOCK_PATH = join(DATA_DIR, 'poll_loop.lock');
const PENDING_OUTPUT_PATH = join(DATA_DIR, 'webchat_pending_output.txt');

// 代码版本指纹：lib-js 下所有 .mjs 文件的最新 mtime。
// clawhub update 替换文件时 mtime 会变，据此检测"我在跑旧代码"。
function _codeFingerprint() {
  let latest = 0;
  try {
    for (const f of readdirSync(__dirname)) {
      if (!f.endsWith('.mjs')) continue;
      try {
        const m = statSync(join(__dirname, f)).mtimeMs;
        if (m > latest) latest = m;
      } catch { /* */ }
    }
  } catch { /* */ }
  return latest;
}

function _log(msg) {
  try {
    _ensureDir();
    const ts = new Date().toISOString().replace('T', ' ').slice(0, 19);
    appendFileSync(LOG_PATH, `[${ts}] ${msg}\n`, 'utf-8');
  } catch { /* */ }
}

function _writePid() {
  _ensureDir();
  writeFileSync(PID_PATH, String(process.pid), 'utf-8');
}

function _clearPid() {
  try { if (existsSync(PID_PATH)) unlinkSync(PID_PATH); } catch { /* */ }
}

function _sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ========== 单实例保护（跨平台） ==========
function _isPidAlive(pid) {
  try {
    process.kill(pid, 0); // signal 0 不杀进程，只检查是否存在
    return true;
  } catch {
    return false;
  }
}

/**
 * 获取单实例锁。如果已有另一个进程在跑，返回 false。
 * 兼容 Windows / Linux / macOS。
 */
function _acquireLock() {
  _ensureDir();

  // 检查现有锁文件
  if (existsSync(LOCK_PATH)) {
    try {
      const content = readFileSync(LOCK_PATH, 'utf-8').trim();
      const lockedPid = parseInt(content, 10);
      if (lockedPid && _isPidAlive(lockedPid) && lockedPid !== process.pid) {
        // 另一个进程还活着，不启动
        return false;
      }
      // 锁文件存在但进程已死，清除残留锁
    } catch { /* 读失败当作无锁 */ }
  }

  // 写入当前 PID
  writeFileSync(LOCK_PATH, String(process.pid), 'utf-8');

  // 双重检查（防竞态）
  try {
    const check = readFileSync(LOCK_PATH, 'utf-8').trim();
    if (parseInt(check, 10) !== process.pid) return false;
  } catch { return false; }

  return true;
}

function _releaseLock() {
  try { if (existsSync(LOCK_PATH)) unlinkSync(LOCK_PATH); } catch { /* */ }
}

async function main() {
  // 单实例检查：已有进程在跑则直接退出
  if (!_acquireLock()) {
    _log(`another instance already running, exit pid=${process.pid}`);
    process.exit(0);
  }

  _writePid();
  _log(`poll_loop started pid=${process.pid}`);

  // 记录启动时的代码指纹，用于检测热更新
  const startFingerprint = _codeFingerprint();

  // 恢复启动时的渠道设置
  const initState = pollStateLoad();
  if (initState.channel) {
    setRuntimeChannel(initState.channel, initState.target || null);
    _log(`channel restored: ${initState.channel} target: ${initState.target || 'null'}`);
  } else {
    // poll_state 没存渠道 → 默认 webchat（哪来的回哪去，不自作主张跳外部渠道）
    setRuntimeChannel('webchat', null);
    _log(`channel default: webchat (no channel in poll_state)`);
  }

  const cfg = _skillCfg().poll || {};
  const interval = Number(cfg.interval_seconds || 30);
  let consecutiveErrors = 0;
  let handedOff = false; // 热更新交接标志：为 true 时 finally 不清理 PID/锁（已归新进程）

  try {
    while (true) {
      // 1) 检查 active 标志
      const state = pollStateLoad();
      if (!state.active) {
        _log('inactive, exit');
        break;
      }

      // 1.5) 热更新检测：代码文件被 clawhub update 替换了 → 重启加载新代码
      const nowFingerprint = _codeFingerprint();
      if (nowFingerprint > startFingerprint) {
        _log(`code updated (fingerprint ${startFingerprint} -> ${nowFingerprint}), restarting to load new version`);
        try {
          // 先释放锁和 PID，让新进程能拿到
          _clearPid();
          _releaseLock();
          const child = spawn(process.execPath, [join(__dirname, 'poll-loop.mjs')], {
            cwd: dirname(__dirname),
            stdio: 'ignore',
            detached: true,
            windowsHide: true,
          });
          child.unref();
          handedOff = true; // 已交接给新进程，finally 不要再清理 PID/锁
          _log(`spawned new poll_loop pid=${child.pid}, old pid=${process.pid} exiting`);
        } catch (se) {
          _log(`restart spawn failed: ${se.message}, continuing with old code`);
        }
        // 无论 spawn 成败都退出旧进程（成功→新进程接管；失败→下次 trigger 会重启）
        return;
      }

      // 2) 跑一轮
      try {
        const result = await pollEventsMain();
        consecutiveErrors = 0;
        if (result && result.stopped) {
          _log(`poll_events stopped: ${JSON.stringify(result)}`);
          break;
        }
        if (result && (result.processed || result.duped)) {
          _log(`tick: ${JSON.stringify(result)}`);
        }
      } catch (e) {
        consecutiveErrors++;
        _log(`tick error #${consecutiveErrors}: ${e.message}`);
        _log(e.stack || '');
        if (consecutiveErrors >= 5) {
          _log('too many errors, exit');
          pollStopped();
          break;
        }
      }

      // 3) 推送 webchat 内容：合并「之前没推成功的积压(pending文件)」+「本轮 buffer」
      // 一起 sessions_send 推。成功→清空 pending 文件；失败→全部留 pending 等下轮重试。
      // pending 文件是 poll-loop 自己的重试队列，不再由 trigger/poll-events 外泄带出。
      {
        const fresh = _webchatBuffer.length ? webchatFlush() : '';
        let backlog = '';
        try {
          if (existsSync(PENDING_OUTPUT_PATH)) {
            // 积压超过 30 分钟还没推出去 → 丢弃（用户早已不需要，避免堆积后一次性涌出）
            const ageMin = (Date.now() - statSync(PENDING_OUTPUT_PATH).mtimeMs) / 60000;
            if (ageMin > 30) {
              try { unlinkSync(PENDING_OUTPUT_PATH); } catch { /* */ }
              _log(`pending output expired (${ageMin.toFixed(0)}min old), discarded`);
            } else {
              backlog = readFileSync(PENDING_OUTPUT_PATH, 'utf-8').trim();
            }
          }
        } catch { /* */ }
        const payload = [backlog, fresh].filter(s => s && s.trim()).join('\n\n');
        if (payload) {
          let sent = false;
          const st = pollStateLoad();
          const key = st.sessionKey || 'agent:main:main';
          if (key) {
            try {
              // cron wake 主动推送（不产生announce回弹）
              const forwardMsg = '[tkseller_forward]\n---\n' + payload + '\n---';
              const res = await fetch(GATEWAY_URL, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${_gatewayToken()}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({ tool: 'cron', args: { action: 'wake', text: forwardMsg, mode: 'now' } }),
                signal: AbortSignal.timeout(10000),
              });
              if (res.ok) {
                const j = await res.json().catch(() => ({}));
                if (j && j.ok !== false) {
                  sent = true;
                  _log(`cron_wake OK (${payload.length} chars)`);
                } else {
                  _log(`cron_wake rejected: ${JSON.stringify(j).slice(0,120)}`);
                }
              } else {
                _log(`cron_wake HTTP ${res.status}`);
              }
            } catch (se) {
              _log(`cron_wake error: ${se.message}`);
            }
          } else {
            _log(`no valid sessionKey in poll_state (got: ${key || 'none'})`);
          }
          if (sent) {
            // 推成功 → 清空重试队列
            try { if (existsSync(PENDING_OUTPUT_PATH)) unlinkSync(PENDING_OUTPUT_PATH); } catch { /* */ }
          } else {
            // 失败 → 全部(积压+本轮)写回 pending，下轮重试
            try {
              writeFileSync(PENDING_OUTPUT_PATH, payload + '\n', 'utf-8');
              _log(`pending output saved for retry (${payload.length} chars)`);
            } catch (we) {
              _log(`CRITICAL: failed to write pending file: ${we.message}`);
            }
          }
        }
      }

      // 4) 睡到下一轮
      await _sleep(interval * 1000);
    }
  } finally {
    if (!handedOff) {
      _clearPid();
      _releaseLock();
      _log('poll_loop exited');
    } else {
      _log('poll_loop handed off to new version, exiting without cleanup');
    }
  }
}

main().catch(e => {
  _log(`fatal: ${e.message}`);
  _clearPid();
  _releaseLock();
  process.exit(1);
});
