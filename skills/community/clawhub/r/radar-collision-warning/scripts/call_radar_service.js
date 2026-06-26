#!/usr/bin/env node
/**
 * 雷达防撞预警 — 通过 rosbridge WebSocket 调用 ROS2 Service
 *
 * 架构:
 *   本机 -> ws://192.168.137.100:8080 (rosbridge_server)
 *   -> ROS2 Service: /radar_collision_warning (std_srvs/srv/Trigger)
 *
 * 用法:
 *   node call_radar_service.js              # 单次查询
 *   node call_radar_service.js --monitor     # 持续监控（Ctrl+C 停止）
 *   node call_radar_service.js -t 0.10      # 自定义阈值（米）
 *   node call_radar_service.js -i 2.0       # 监控间隔（秒）
 *
 * 依赖: Node.js 18+ 内置 WebSocket（globalThis.WebSocket），无需安装任何包
 */

'use strict';

const WS = globalThis.WebSocket;

// ============ 配置 ============
const ROSBRIDGE_HOST = process.env.RADAR_HOST || '192.168.137.100';
const ROSBRIDGE_PORT = process.env.RADAR_PORT  || '8080';
const SERVICE_NAME   = '/radar_collision_warning';
const DEFAULT_THRESHOLD = 0.05; // 5cm
// ==============================

// ── 命令行参数解析 ──
const args     = process.argv.slice(2);
const isMonitor = args.includes('--monitor') || args.includes('-m');
let threshold   = DEFAULT_THRESHOLD;
let interval    = 1.0;

for (let i = 0; i < args.length; i++) {
  if ((args[i] === '--threshold' || args[i] === '-t') && args[i + 1]) {
    threshold = parseFloat(args[i + 1]); i++;
  }
  if ((args[i] === '--interval' || args[i] === '-i') && args[i + 1]) {
    interval = parseFloat(args[i + 1]); i++;
  }
}

const wsUrl = `ws://${ROSBRIDGE_HOST}:${ROSBRIDGE_PORT}`;

// ── 调用 ROS2 Service，返回 Promise ──
function callRadarService() {
  return new Promise((resolve) => {
    let ws;
    let done = false;
    let timer;

    const finish = (result) => {
      if (done) return;
      done = true;
      if (timer) clearTimeout(timer);
      if (ws) try { ws.close(); } catch (_) {}
      resolve(result);
    };

    timer = setTimeout(() => finish({
      success: false,
      error: `连接 rosbridge 超时（${ROSBRIDGE_HOST}:${ROSBRIDGE_PORT}）`,
      message: '⚠️ 连接树莓派雷达服务超时，请检查树莓派是否在线且 rosbridge 已启动'
    }), 5000);

    try {
      ws = new WS(wsUrl);
    } catch (e) {
      finish({ success: false, error: `WebSocket 创建失败: ${e.message}`, message: '⚠️ 无法创建连接' });
      return;
    }

    ws.onopen = () => {
      const callId = `c${Date.now()}${Math.random().toString(36).slice(2, 6)}`;
      // rosbridge JSON-RPC 2.0 — call_service
      ws.send(JSON.stringify({
        op: 'call_service',
        id: callId,
        service: SERVICE_NAME,
        args: {},
        type: 'std_srvs/srv/Trigger'
      }));

      // 监听本轮响应
      ws.addEventListener('message', function handler(ev) {
        try {
          const msg = JSON.parse(ev.data);
          // 匹配我们的 callId
          if (msg.id !== callId) return;
          ws.removeEventListener('message', handler);

          let success = false, message = '';
          if (msg.values) {
            success = msg.values.success ?? false;
            message  = msg.values.message  ?? '';
          } else if (msg.result !== undefined) {
            const v = msg.result ?? {};
            success = v.success ?? false;
            message  = v.message  ?? '';
          }

          // 从 message 中同时匹配 cm 和 m 单位
          const dmCm = message.match(/([\d.]+)\s*cm/i);
          const dmM  = message.match(/([\d.]+)\s*m\b/i);
          let distM;
          if (dmCm) {
            distM = parseFloat(dmCm[1]) / 100;  // cm → m
          } else if (dmM) {
            distM = parseFloat(dmM[1]);
          } else {
            distM = threshold;  // 解析失败用阈值
          }

          finish({
            success: true,
            distance_m: distM,
            distance_cm: parseFloat((distM * 100).toFixed(1)),
            warning: distM < threshold,
            message,
            threshold_m: threshold,
            service_response_success: success
          });
        } catch (_) {}
      });
    };

    ws.onerror = () => finish({
      success: false,
      error: 'WebSocket 连接失败',
      message: '⚠️ 连接树莓派失败，请检查网络和 rosbridge 服务状态'
    });

    ws.onclose = () => {
      if (!done) finish({
        success: false,
        error: 'WebSocket 连接关闭',
        message: '⚠️ 连接意外中断'
      });
    };
  });
}

// ── 持续监控模式 ──
async function monitorMode() {
  console.log(`[雷达监控] 阈值=${(threshold * 100).toFixed(0)}cm | 间隔=${interval}s | Ctrl+C 停止\n`);
  let consecutive = 0, lastWarned = false;

  while (true) {
    const r = await callRadarService();
    const now = new Date().toLocaleTimeString('zh-CN', { hour12: false });

    if (r.success) {
      if (r.warning) {
        consecutive++;
        if (!lastWarned || consecutive % 5 === 1) {
          console.log(
            `🚨 [${now}] ⚠️ 碰撞危险！距离: ${r.distance_cm}cm (< ${(threshold * 100).toFixed(0)}cm) | 连续: ${consecutive}次`
          );
        }
        lastWarned = true;
      } else {
        consecutive = 0;
        console.log(`✅ [${now}] 安全 | 距离: ${r.distance_cm}cm`);
        lastWarned = false;
      }
    } else {
      consecutive = 0;
      console.log(`❌ [${now}] ${r.message}`);
      lastWarned = false;
    }

    await new Promise(r => setTimeout(r, interval * 1000));
  }
}

// ── 主入口 ──
async function main() {
  if (isMonitor) {
    await monitorMode();
  } else {
    const r = await callRadarService();
    process.stdout.write(JSON.stringify(r, null, 2) + '\n');
  }
}

main().catch(e => {
  console.error(JSON.stringify({ success: false, error: e.message }));
  process.exit(1);
});
