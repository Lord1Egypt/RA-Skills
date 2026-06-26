/**
 * MongoDB Watchdog Service
 * ========================
 * 監控 MongoDB 服務狀態，自動重啟，分析 crash 原因，發送 Telegram 通知
 * 
 * 部署在 WEB-SV (10.0.0.213) 上，用 PM2 管理
 * 
 * 功能：
 * 1. 每 30 秒 ping MongoDB，偵測服務是否存活
 * 2. MongoDB 掛了 → 自動重啟 Windows Service
 * 3. 分析 mongod.log 找出 crash 原因
 * 4. 透過 Telegram Bot 發通知
 * 5. 記錄歷史事件到本地 JSON log
 */

const { MongoClient } = require('mongodb');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const https = require('https');

// ===== 設定 =====
const CONFIG = {
  mongo: {
    uri: 'mongodb://127.0.0.1:27017',
    pingIntervalMs: 30000,        // 每 30 秒檢查一次
    connectTimeoutMs: 5000,       // 連線超時 5 秒
    maxRetries: 2,                // 連續失敗 2 次才判定為掛了
  },
  service: {
    name: 'MongoDB',              // Windows Service 名稱
    restartDelayMs: 5000,         // 重啟前等待 5 秒
    maxAutoRestarts: 5,           // 1 小時內最多自動重啟 5 次
    autoRestartWindowMs: 3600000, // 1 小時
  },
  log: {
    mongodLogPath: 'C:\\ProgramData\\MongoDB\\log\\mongod.log',
    watchdogLogPath: 'D:\\ProPower_System\\logs\\mongodb-watchdog.json',
    maxLogEntries: 1000,          // 最多保留 1000 筆紀錄
  },
  telegram: {
    // 用環境變數或直接填入
    botToken: process.env.TELEGRAM_BOT_TOKEN || '',
    chatId: process.env.TELEGRAM_CHAT_ID || '1663667034',
    enabled: true,
  },
  report: {
    dailyReportHour: 8,           // 每天早上 8 點發日報
  }
};

// ===== 狀態追蹤 =====
let state = {
  consecutiveFailures: 0,
  lastPingOk: null,
  lastCrashTime: null,
  lastCrashReason: null,
  autoRestarts: [],               // 紀錄重啟時間
  totalCrashes: 0,
  totalAutoRestarts: 0,
  startTime: new Date(),
  lastDailyReport: null,
};

// ===== MongoDB 連線檢查 =====
async function pingMongo() {
  let client;
  try {
    client = new MongoClient(CONFIG.mongo.uri, {
      connectTimeoutMS: CONFIG.mongo.connectTimeoutMs,
      serverSelectionTimeoutMS: CONFIG.mongo.connectTimeoutMs,
      directConnection: true,
    });
    await client.connect();
    const result = await client.db('admin').command({ ping: 1 });
    return result.ok === 1;
  } catch (err) {
    return false;
  } finally {
    if (client) {
      try { await client.close(); } catch (_) {}
    }
  }
}

// ===== Windows Service 操作 =====
function execCmd(cmd) {
  return new Promise((resolve, reject) => {
    exec(cmd, { timeout: 30000 }, (err, stdout, stderr) => {
      if (err) reject(new Error(`${cmd} failed: ${stderr || err.message}`));
      else resolve(stdout.trim());
    });
  });
}

async function restartMongoService() {
  log('WARN', 'Attempting to restart MongoDB service...');
  
  try {
    // 先嘗試停止（可能已經停了）
    try {
      await execCmd(`net stop "${CONFIG.service.name}"`);
      log('INFO', 'MongoDB service stopped');
    } catch (_) {
      log('INFO', 'MongoDB service was already stopped');
    }

    // 等待一下
    await sleep(CONFIG.service.restartDelayMs);

    // 啟動
    await execCmd(`net start "${CONFIG.service.name}"`);
    log('INFO', 'MongoDB service started successfully');

    // 等待 MongoDB 就緒
    await sleep(3000);
    const ok = await pingMongo();
    if (ok) {
      log('INFO', 'MongoDB is responding after restart');
      return true;
    } else {
      log('ERROR', 'MongoDB not responding after restart');
      return false;
    }
  } catch (err) {
    log('ERROR', `Failed to restart MongoDB: ${err.message}`);
    return false;
  }
}

// ===== Crash 原因分析 =====
function analyzeCrashReason() {
  try {
    const logPath = CONFIG.log.mongodLogPath;
    if (!fs.existsSync(logPath)) return 'Log file not found';

    // 讀最後 50KB 來找 crash 原因
    const stats = fs.statSync(logPath);
    const readSize = Math.min(stats.size, 50 * 1024);
    const fd = fs.openSync(logPath, 'r');
    const buf = Buffer.alloc(readSize);
    fs.readSync(fd, buf, 0, readSize, stats.size - readSize);
    fs.closeSync(fd);

    const content = buf.toString('utf8');
    const lines = content.split('\n').filter(l => l.trim());

    // 找 Fatal 級別的訊息
    const fatalLines = lines.filter(l => {
      try {
        const obj = JSON.parse(l);
        return obj.s === 'F';
      } catch (_) { return false; }
    });

    if (fatalLines.length > 0) {
      const reasons = [];
      for (const line of fatalLines) {
        try {
          const obj = JSON.parse(line);
          if (obj.msg) reasons.push(obj.msg);
          if (obj.attr?.message) reasons.push(obj.attr.message.trim());
          if (obj.attr?.exceptionString) reasons.push(`Exception: ${obj.attr.exceptionString}`);
        } catch (_) {}
      }
      return reasons.filter(r => r).join(' | ') || 'Fatal error (details unclear)';
    }

    // 找 unclean shutdown
    const unclean = lines.find(l => l.includes('unclean shutdown'));
    if (unclean) return 'Unclean shutdown detected';

    return 'Unknown (no fatal messages in recent log)';
  } catch (err) {
    return `Analysis failed: ${err.message}`;
  }
}

// ===== Telegram 通知 =====
function sendTelegram(message) {
  if (!CONFIG.telegram.enabled || !CONFIG.telegram.botToken) {
    log('INFO', `[Telegram disabled] ${message}`);
    return;
  }

  const payload = JSON.stringify({
    chat_id: CONFIG.telegram.chatId,
    text: message,
    parse_mode: 'HTML',
  });

  const options = {
    hostname: 'api.telegram.org',
    port: 443,
    path: `/bot${CONFIG.telegram.botToken}/sendMessage`,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(payload),
    },
    timeout: 10000,
  };

  const req = https.request(options, (res) => {
    if (res.statusCode !== 200) {
      log('WARN', `Telegram API returned ${res.statusCode}`);
    }
  });

  req.on('error', (err) => {
    log('WARN', `Telegram send failed: ${err.message}`);
  });

  req.write(payload);
  req.end();
}

// ===== 日誌 =====
function log(level, message) {
  const entry = {
    time: new Date().toISOString(),
    level,
    message,
  };
  
  console.log(`[${entry.time}] [${level}] ${message}`);

  // 寫入 JSON log
  try {
    const logDir = path.dirname(CONFIG.log.watchdogLogPath);
    if (!fs.existsSync(logDir)) fs.mkdirSync(logDir, { recursive: true });

    let logs = [];
    if (fs.existsSync(CONFIG.log.watchdogLogPath)) {
      try {
        logs = JSON.parse(fs.readFileSync(CONFIG.log.watchdogLogPath, 'utf8'));
      } catch (_) { logs = []; }
    }
    
    logs.push(entry);
    
    // 保留最新的 N 筆
    if (logs.length > CONFIG.log.maxLogEntries) {
      logs = logs.slice(-CONFIG.log.maxLogEntries);
    }
    
    fs.writeFileSync(CONFIG.log.watchdogLogPath, JSON.stringify(logs, null, 2));
  } catch (err) {
    console.error(`Failed to write log: ${err.message}`);
  }
}

// ===== 重啟次數限制 =====
function canAutoRestart() {
  const now = Date.now();
  // 清理超過視窗的記錄
  state.autoRestarts = state.autoRestarts.filter(
    t => now - t < CONFIG.service.autoRestartWindowMs
  );
  return state.autoRestarts.length < CONFIG.service.maxAutoRestarts;
}

// ===== 主監控迴圈 =====
async function monitorLoop() {
  const ok = await pingMongo();

  if (ok) {
    if (state.consecutiveFailures > 0) {
      log('INFO', `MongoDB recovered after ${state.consecutiveFailures} failed pings`);
    }
    state.consecutiveFailures = 0;
    state.lastPingOk = new Date();
  } else {
    state.consecutiveFailures++;
    log('WARN', `MongoDB ping failed (consecutive: ${state.consecutiveFailures}/${CONFIG.mongo.maxRetries})`);

    if (state.consecutiveFailures >= CONFIG.mongo.maxRetries) {
      // MongoDB 確認掛了
      state.totalCrashes++;
      state.lastCrashTime = new Date();

      // 分析原因
      const reason = analyzeCrashReason();
      state.lastCrashReason = reason;
      log('ERROR', `MongoDB DOWN! Crash reason: ${reason}`);

      // 發通知
      sendTelegram(
        `🚨 <b>MongoDB 掛了！</b>\n\n` +
        `⏰ 時間: ${state.lastCrashTime.toLocaleString('zh-TW', { timeZone: 'Asia/Taipei' })}\n` +
        `📋 原因: ${reason}\n` +
        `🔢 累計 crash: ${state.totalCrashes} 次\n` +
        `\n⏳ 正在嘗試自動重啟...`
      );

      // 嘗試自動重啟
      if (canAutoRestart()) {
        const success = await restartMongoService();
        state.autoRestarts.push(Date.now());
        state.totalAutoRestarts++;

        if (success) {
          state.consecutiveFailures = 0;
          sendTelegram(
            `✅ <b>MongoDB 已自動重啟成功</b>\n\n` +
            `⏰ 恢復時間: ${new Date().toLocaleString('zh-TW', { timeZone: 'Asia/Taipei' })}\n` +
            `📊 本小時重啟次數: ${state.autoRestarts.length}/${CONFIG.service.maxAutoRestarts}`
          );
        } else {
          sendTelegram(
            `❌ <b>MongoDB 自動重啟失敗！</b>\n\n` +
            `需要人工介入處理。\n` +
            `SSH: administrator@10.0.0.213\n` +
            `指令: net start MongoDB`
          );
        }
      } else {
        log('ERROR', 'Auto-restart limit reached, skipping');
        sendTelegram(
          `⚠️ <b>MongoDB 自動重啟已達上限</b>\n\n` +
          `1 小時內已重啟 ${CONFIG.service.maxAutoRestarts} 次，不再自動重啟。\n` +
          `可能有根本性問題，需要人工檢查。\n` +
          `SSH: administrator@10.0.0.213`
        );
      }
    }
  }

  // 每日報告
  checkDailyReport();
}

// ===== 每日報告 =====
function checkDailyReport() {
  const now = new Date();
  const hour = now.getHours();
  const today = now.toISOString().slice(0, 10);

  if (hour === CONFIG.report.dailyReportHour && state.lastDailyReport !== today) {
    state.lastDailyReport = today;
    
    const uptimeMs = Date.now() - state.startTime.getTime();
    const uptimeH = Math.floor(uptimeMs / 3600000);
    const uptimeM = Math.floor((uptimeMs % 3600000) / 60000);

    sendTelegram(
      `📊 <b>MongoDB Watchdog 日報</b>\n\n` +
      `📅 ${today}\n` +
      `⏱ Watchdog 運行: ${uptimeH}h ${uptimeM}m\n` +
      `💚 MongoDB 狀態: ${state.consecutiveFailures === 0 ? '正常' : '異常'}\n` +
      `💥 累計 crash: ${state.totalCrashes} 次\n` +
      `🔄 累計自動重啟: ${state.totalAutoRestarts} 次\n` +
      `${state.lastCrashTime ? `⚠️ 最近 crash: ${state.lastCrashTime.toLocaleString('zh-TW', { timeZone: 'Asia/Taipei' })}\n📋 原因: ${state.lastCrashReason}` : '✅ 無 crash 記錄'}`
    );
  }
}

// ===== 工具函數 =====
function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

// ===== 啟動 =====
async function main() {
  log('INFO', '========================================');
  log('INFO', 'MongoDB Watchdog Service starting...');
  log('INFO', `Ping interval: ${CONFIG.mongo.pingIntervalMs}ms`);
  log('INFO', `Max retries before restart: ${CONFIG.mongo.maxRetries}`);
  log('INFO', `Telegram notifications: ${CONFIG.telegram.enabled ? 'ON' : 'OFF'}`);
  log('INFO', '========================================');

  // 初始檢查
  const initialOk = await pingMongo();
  if (initialOk) {
    log('INFO', 'Initial ping: MongoDB is UP');
  } else {
    log('WARN', 'Initial ping: MongoDB is DOWN');
  }

  sendTelegram(
    `🐕 <b>MongoDB Watchdog 啟動</b>\n\n` +
    `MongoDB 狀態: ${initialOk ? '✅ 正常' : '❌ 異常'}\n` +
    `監控間隔: ${CONFIG.mongo.pingIntervalMs / 1000} 秒`
  );

  // 主迴圈
  while (true) {
    try {
      await monitorLoop();
    } catch (err) {
      log('ERROR', `Monitor loop error: ${err.message}`);
    }
    await sleep(CONFIG.mongo.pingIntervalMs);
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
