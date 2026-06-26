# Response Speed Test Skill

精確測量 OpenClaw 系統響應速度的 Skill，提供毫秒級時間測量和詳細報告生成。

## 安裝

```bash
clawhub install response-speed-test
```

## 使用

### 單次測試

```bash
response-speed-test run
```

### 基準測試

```bash
response-speed-test benchmark --iterations 10
```

### 生成報告

```bash
response-speed-test report --format markdown
```

## 測量階段

| 階段 | 代碼 | 說明 |
|------|------|------|
| T0 | MESSAGE_SENT | 用戶發送消息 |
| T1 | GATEWAY_RECEIVE | Gateway 收到消息 |
| T2 | SESSION_DISPATCH | Session 分發 |
| T3 | MEMORY_LOAD | Memory 載入 |
| T4 | LLM_REQUEST_START | LLM 請求開始 |
| T5 | LLM_FIRST_TOKEN | 第一個 Token (TTFT) |
| T6 | LLM_RESPONSE_COMPLETE | LLM 響應完成 |
| T7 | MESSAGE_SENT | 消息發送完成 |

## 關鍵指標

- TTFT: Time To First Token
- TPS: Tokens Per Second
- Total Response Time

## 配置

在 `HEARTBEAT.md` 或對話中使用：

```markdown
- response-speed-test: run benchmark every 6 hours
```
