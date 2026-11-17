/**
 * example-cron.js — 定時公車監控 Cron Job 設定範例
 *
 * 說明：如何使用 qclaw-cron-skill 設定定時公車監控
 * 請先閱讀 qclaw-cron-skill 的 SKILL.md 了解 Cron Job 格式
 *
 * 使用情境：
 * 1. 每 5 分鐘檢查特定路線是否有車
 * 2. 發現脫班立即推播通知
 * 3. 定時回報路線概況
 *
 * 底下為 cron job payload 範例（需配合 qclaw-cron-skill 使用）
 */

const { detectAnomalies, findByRoute, fetchAll } = require('../lib/bus-api.js');

// ============================================================
// 情境 A：每 5 分鐘檢查特定路線，發現脫班就通知
// ============================================================
const ROUTE_MONITOR_CRON = {
  name: '臺北市公車脫班偵測',
  // 每 5 分鐘執行一次
  schedule: { kind: 'every', everyMs: 5 * 60 * 1000 },
  sessionTarget: 'isolated',
  payload: {
    kind: 'agentTurn',
    message: `【公車脫班偵測任務】

請執行以下檢查並回報：

1. 執行 detectAnomalies() 檢查全系統異常公車
2. 若有異常，格式化輸出異常公車資訊（車牌、路綫、異常原因）
3. 若無異常，回覆「✅ 目前全系統公車正常」

只輸出實質結果，不需多餘說明。`,
    timeoutSeconds: 60
  },
  delivery: {
    mode: 'announce',      // 結果直接發到當前對話
    // 若要發到其他頻道（如 LINE/Telegram），設定：
    // mode: 'announce',
    // channel: 'line',
    // to: '<LINE user ID>'
  },
  description: '每5分鐘檢查臺北市公車是否有脫班或異常'
};

// ============================================================
// 情境 B：早上 7:30 定時回報熱門路線概況
// ============================================================
const MORNING_REPORT_CRON = {
  name: '早晨公車路線概況',
  schedule: { kind: 'cron', expr: '30 7 * * *', tz: 'Asia/Taipei' },
  sessionTarget: 'isolated',
  payload: {
    kind: 'agentTurn',
    message: `【早晨公車概況回報】

請執行以下任務：

1. 執行 routeSummary() 取得全系統路線車數
2. 找出目前線上車數最多的前 5 條路線
3. 格式化輸出：
   - 每條路線代碼、目前車數
   - 該路線最新一台公車的更新时间
4. 輸出摘要後結束

只輸出實質資料，不需多餘說明。`,
    timeoutSeconds: 90
  },
  delivery: {
    mode: 'announce'
  },
  description: '每日早上7:30回報熱門公車路線概況'
};

// ============================================================
// 情境 C：查特定路線到站（一次性提醒）
// ============================================================
function createOneShotEtaCheck(routeId, stopId, targetMinutes) {
  return {
    name: `路線${routeId}到站提醒`,
    schedule: { kind: 'every', everyMs: 2 * 60 * 1000 },
    sessionTarget: 'isolated',
    payload: {
      kind: 'agentTurn',
      message: `【到站時間追蹤：路線 ${routeId} → 站點 ${stopId}】

若 ${targetMinutes} 分鐘內有車到站，立即回報：
路線 ${routeId} 已接近站點 ${stopId}，請準備上車！

若 ${targetMinutes} 分鐘內無車，忽略此觸發。

只回報實際結果。`,
      timeoutSeconds: 60
    },
    delivery: { mode: 'announce' },
    deleteAfterRun: false   // 設為 true 可在首次觸發後自動刪除
  };
}

// 匯出設定範例
module.exports = {
  ROUTE_MONITOR_CRON,
  MORNING_REPORT_CRON,
  createOneShotEtaCheck
};

// ============================================================
// 使用說明：如何將上述設定寫入 Cron Job
// ============================================================
// 請使用 cron tool (add action) 建立 job，範例：
//
// cron(action='add', job={
//   name: '臺北市公車脫班偵測',
//   schedule: { kind: 'every', everyMs: 5 * 60 * 1000 },
//   sessionTarget: 'isolated',
//   payload: {
//     kind: 'agentTurn',
//     message: '執行 detectAnomalies() 並回報...',
//     timeoutSeconds: 60
//   },
//   delivery: { mode: 'announce' }
// })
//
// 詳細語法請參閱 qclaw-cron-skill/SKILL.md
