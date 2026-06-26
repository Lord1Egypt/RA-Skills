# ⏱️ Response Speed Test Skill

**精確測量 OpenClaw 系統響應速度的 Skill**

## 📊 測量目標

| 階段 | 測量項目 | 說明 |
|------|----------|------|
| T0 | 消息發送時間 | 用戶發送消息的精確時間戳 |
| T1 | Gateway 接收時間 | OpenClaw Gateway 收到消息的時間 |
| T2 | Session 啟動時間 | Session 開始處理的時間 |
| T3 | Memory 載入時間 | Soul Memory 索引載入完成時間 |
| T4 | 模型 API 調用開始 | 發送請求到 LLM API 的時間 |
| T5 | 模型 API 響應開始 | 收到第一個 token 的時間（TTFT） |
| T6 | 模型 API 響應完成 | 收到完整響應的時間 |
| T7 | 消息發送完成 | 回覆消息送達用戶的時間 |

## 🎯 關鍵指標

- **TTFT (Time To First Token)**: 從請求發送到收到第一個 token 的時間
- **TPS (Tokens Per Second)**: 每秒生成的 token 數
- **Memory Load Time**: Soul Memory 索引載入時間
- **Total Response Time**: 完整響應時間

## 📁 項目結構

```
response-speed-test/
├── SKILL.md           # 技能說明文檔
├── core.py            # 核心測量引擎
├── probes/
│   ├── gateway_probe.py   # Gateway 層探針
│   ├── session_probe.py   # Session 層探針
│   ├── memory_probe.py    # Memory 載入探針
│   └── llm_probe.py       # LLM API 探針
├── reporters/
│   ├── console.py         # 控制台輸出
│   ├── json_export.py     # JSON 報告導出
│   └── markdown_report.py # Markdown 報告生成
└── tests/
    └── benchmark.py       # 基準測試腳本
```

## 🚀 安裝

```bash
clawhub install response-speed-test
```

## 📝 使用方法

```bash
# 運行單次測試
response-speed-test run

# 運行基準測試
response-speed-test benchmark --iterations 10

# 生成報告
response-speed-test report --format markdown
```

## 📊 報告範例

```markdown
# ⏱️ 響應速度測試報告

**測試 ID**: `20260303_092345_123456`
**總時間**: 2.345 秒 (2345.678 ms)

## 📊 各階段時間分析

| 階段 | 耗時 | 佔比 |
|------|-------------|------|
| T1_GATEWAY_RECEIVE | **45.123** | 1.92% |
| T2_SESSION_DISPATCH | **12.456** | 0.53% |
| T3_MEMORY_LOAD | **165.023** | 7.04% |
| T5_LLM_FIRST_TOKEN | **1234.567** | 52.63% |
| T6_LLM_RESPONSE_COMPLETE | **856.234** | 36.50% |
| T7_MESSAGE_SENT | **26.597** | 1.13% |
```

## 🔧 開發狀態

- [x] 研究報告完成
- [ ] 核心測量引擎開發
- [ ] 各層探針開發
- [ ] 報告生成器開發
- [ ] 基準測試腳本
- [ ] ClawHub 發布

## 📜 License

MIT

## 👤 Author

kingofqin2026
