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
import { writeFileSync, readFileSync, existsSync, unlinkSync, appendFileSync } from 'fs';
import { join } from 'path';
import { main as pollEventsMain } from './poll-events.mjs';
import { DATA_DIR, _ensureDir, _skillCfg, pollStateLoad, pollStopped, setRuntimeChannel, detectChannelFromSessions } from './card-tools.mjs';

const LOG_PATH = join(DATA_DIR, 'poll_loop.log');
const PID_PATH = join(DATA_DIR, 'poll_loop.pid');
const LOCK_PATH = join(DATA_DIR, 'poll_loop.lock');

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

  // 恢复启动时的渠道设置
  const initState = pollStateLoad();
  if (initState.channel) {
    setRuntimeChannel(initState.channel, initState.target || null);
    _log(`channel restored: ${initState.channel} target: ${initState.target || 'auto'}`);
  } else {
    // poll_state 没存渠道，自动从 sessions 检测
    const detected = await detectChannelFromSessions();
    if (detected) {
      setRuntimeChannel(detected.channel, detected.target);
      _log(`channel auto-detected: ${detected.channel} target: ${detected.target}`);
    }
  }

  const cfg = _skillCfg().poll || {};
  const interval = Number(cfg.interval_seconds || 30);
  let consecutiveErrors = 0;

  try {
    while (true) {
      // 1) 检查 active 标志
      const state = pollStateLoad();
      if (!state.active) {
        _log('inactive, exit');
        break;
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

      // 3) 睡到下一轮
      await _sleep(interval * 1000);
    }
  } finally {
    _clearPid();
    _releaseLock();
    _log('poll_loop exited');
  }
}

main().catch(e => {
  _log(`fatal: ${e.message}`);
  _clearPid();
  _releaseLock();
  process.exit(1);
});
