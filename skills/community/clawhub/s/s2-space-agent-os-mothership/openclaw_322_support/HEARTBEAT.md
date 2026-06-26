# S2 Mothership Heartbeat Configuration (For OpenClaw 3.22+)

## 🌌 四维时序记忆阵列：折叠压缩 (Chronos Memory Delta-Compression)
- cron: "0 * * * *"  # 每小时执行一次
  action: s2_chronos_compress
  params:
    mode: "delta_folding"
    target_db: "s2_chronos.db"
    description: "主动将过去一小时的声光气电磁碎片日志，折叠压缩为四维因果长期记忆。"

## 🛸 4㎡ 标准物理网格：生命体征巡逻 (SSSU Vital Sweeping)
- cron: "*/15 * * * *"  # 每 15 分钟执行一次
  action: s2_grid_vital_scan
  params:
    radar_mode: "mmWave_zero_BPM"
    sector: "ALL_ACTIVE_PODS"
    description: "主动扫描所有分配给 Agent 的物理栖息舱，检测宠物或人类的异常生命体征并记录。"