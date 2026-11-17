# 附录 · curl 示例与常见错误码

> 根地址、`API_BASE`、统一响应与鉴权见 [api.md](./api.md)。

## 二、curl 快速示例

```bash
API_BASE="${SLZQ_OPENCLAW_DOMAIN:-https://slzqapi.sxslqhsh.com}/mobile-api"
API_KEY="${SLZQ_OPENCLAW_API_KEY:?}"
ENV="${SLZQ_OPENCLAW_ENV:-sim}"

# 健康检查（无需鉴权）
curl -s "$API_BASE/open/v1/health" | jq .

# 首次安装：登录领取模拟盘密钥（三步均无需鉴权）
curl -s "$API_BASE/open/v1/auth/agreement" | jq .

curl -s -X POST "$API_BASE/open/v1/auth/sms/send" \
  -H "Content-Type: application/json" \
  -d '{"mobileNum":"13800000000"}' | jq .

# verifyCode 位数以上一步响应的 codeLength 为准（当前 4 位纯数字），字符串原样传、保留前导零
# codeKey 不用传：服务端按手机号暂存并自动取回
curl -s -X POST "$API_BASE/open/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
        "mobileNum": "13800000000",
        "verifyCode": "1234",
        "agreementVersion": "sim-risk-1"
      }' | jq .

# 当前上下文
curl -s "$API_BASE/open/v1/me" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "X-Trading-Env: ${ENV}" | jq .

# 账户摘要
curl -s "$API_BASE/open/v1/account/summary" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "X-Trading-Env: ${ENV}" | jq .

# 持仓列表（sim 为 PositionDetailResponseModel[]；live 为 PositionModel[]；sim 可附加 ?positionDateType=今|昨）
curl -s "$API_BASE/open/v1/positions" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "X-Trading-Env: ${ENV}" | jq .

# 当前委托
curl -s "$API_BASE/open/v1/orders/open" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "X-Trading-Env: ${ENV}" | jq .

# 成交列表（指定时间范围）
curl -s "$API_BASE/open/v1/trades?insertTimeStart=2026-03-27+09:00:00&insertTimeEnd=2026-03-27+15:30:00" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "X-Trading-Env: ${ENV}" | jq .

# 行情快照
curl -s "$API_BASE/open/v1/market/snapshot?instrumentId=au2606" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "X-Trading-Env: ${ENV}" | jq .

# 批量快照
curl -s "$API_BASE/open/v1/market/snapshots?instrumentIds=au2606,ag2612,cu2506" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "X-Trading-Env: ${ENV}" | jq .

# K 线（日线）
curl -s "$API_BASE/open/v1/market/kline?exchangeId=SHFE&instrumentId=au2606&type=6" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "X-Trading-Env: ${ENV}" | jq .

# 下单（限价买入开仓，sim）
curl -s -X POST "$API_BASE/open/v1/orders" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "X-Trading-Env: sim" \
  -H "Content-Type: application/json" \
  -d '{
    "instrumentId": "cu2506",
    "orderRef": "1001",
    "direction": "BUY",
    "offsetFlag": "OPEN",
    "priceType": "LIMIT",
    "limitPrice": 78500.0,
    "count": 1
  }' | jq .

# 下单（市价平仓，live）
curl -s -X POST "$API_BASE/open/v1/orders" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "X-Trading-Env: live" \
  -H "Content-Type: application/json" \
  -d '{
    "instrumentId": "cu2506",
    "direction": "SELL",
    "offsetFlag": "CLOSE",
    "priceType": "ANY",
    "limitPrice": 78400.0,
    "count": 1
  }' | jq .

# 撤单（使用下单回报中的字段）
curl -s -X POST "$API_BASE/open/v1/orders/cancel" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "X-Trading-Env: ${ENV}" \
  -H "Content-Type: application/json" \
  -d '{
    "instrumentId": "cu2506",
    "exchangeId": "SHFE",
    "orderRef": "1001",
    "orderSysId": "31574",
    "frontID": 1,
    "sessionId": 123456
  }' | jq .
```

---

## 三、常见错误码

| errorCode | 含义 | 处理建议 |
|-----------|------|----------|
| `10411` | API Key 缺失、格式错误、无效或已吊销 | 没有密钥时把两种方式摆给用户选：A 走 [api-auth.md](./api-auth.md) 的登录流程现场领取（已有模拟盘密钥会原样返回），B 去 App「我的 → 期货辅助交易」一键复制已有密钥（要实盘密钥只能走 B）；有密钥则检查是否复制完整 |
| `10412` | 交易环境不被密钥档位允许（模拟盘密钥请求 live） | 改用 `sim`，或按 `liveUpgradeSteps` 引导用户在 App 内开通实盘密钥 |
| `10413` | 实盘密钥未绑定 CTP 凭据 | 在 App 内完成凭据绑定 |
| `10414` | 实盘 CTP 自动登录失败 | 到 App 检查实盘账号状态与交易密码 |
| `10415` | 未同意协议 / 风险告知 | 登录时补传 `agreementVersion`；App 场景在 App 内确认协议 |
| `10416` | 创建实盘密钥时 CTP 交易密码校验失败 | 由用户在 App 内重试，Agent 不得代填密码 |
| `10008` | 手机号格式错误 | 让用户重新提供 11 位手机号 |
| `10011` | 短信验证码错误 | 请用户核对；错误累计超限会锁 1 小时，不要替用户猜 |
| `10012` | 短信验证码已过期 | 重新调用 `POST /open/v1/auth/sms/send` |
| `00004` | 参数错误 | 按 `errorInfo` 补齐或修正参数 |
| 业务错误 | CTP 报错（如持仓不足、价格超限） | 见 `errorInfo` 详细说明 |

## 四、面向智能体的错误恢复策略

所有 Open API 失败时仍返回 HTTP 200，但 `success=false`。智能体必须先读取 `errorInfo` 中的“下一步”，不要自行猜测参数或回退到自由 HTTP。

| 典型 errorInfo | 下一步动作 | 推荐工具/接口 |
|----------------|------------|---------------|
| 缺少 API Key | 把两种取钥方式都给用户选：**A** 展示风险告知 → 发验证码 → 登录领取（**没注册 MCP 也要照走**，这三个接口免鉴权，直接发 HTTP）；**B** 去 App「我的 → 期货辅助交易」一键复制已有密钥（要实盘密钥只能走 B） | `auth_agreement`、`auth_send_code`、`auth_login`；无 MCP 时用 `GET /open/v1/auth/agreement`、`POST /open/v1/auth/sms/send`、`POST /open/v1/auth/login`（见 [api-auth.md](./api-auth.md)） |
| API Key 格式无效 / 无效或已吊销 | 重新领取密钥，或在 App「我的 → 期货辅助交易」重新生成后替换环境变量并重启客户端 | `auth_login`、安装脚本 `doctor.sh` |
| 当前密钥为「模拟盘」权限，不支持 live | 改用 `X-Trading-Env: sim`；确需实盘则把 `liveUpgradeSteps` 转述给用户，由其在 App 内开通 | `GET /open/v1/me` |
| contractCode 不能为空 / 合约代码无效 | 先选取合法合约，合约代码应为字母+数字且不带交易所后缀；保持目录接口返回的原样大小写 | `GET /open/v1/catalog/hot`、`GET /open/v1/catalog/goods`、`GET /open/v1/catalog/contract` |
| 行情快照需要 instrumentId 或 contractCode | 从热门合约或品种列表取当前有效主力合约后重试 | `GET /open/v1/catalog/hot`、`GET /open/v1/market/snapshot` |
| 下单参数不完整 | 补齐 `instrumentId`、`direction`、`offsetFlag`、`priceType`、`count`；sim 还要补 `orderRef` | `place_order`、`GET /open/v1/catalog/contract` |
| 撤单参数不完整 | 使用上一笔下单回报或当前委托中的 `instrumentId`、`exchangeId`、`orderRef`、`orderSysId`、`frontID` | `GET /open/v1/orders/open`、`cancel_order` |
| 可用手数不足 / 持仓不足 | 先查持仓可用手数；SHFE/INE 按今昨仓拆分 | `GET /open/v1/positions?positionDateType=今|昨` |
| 价格不正确 | 获取当前行情并按合约最小变动价位修正价格 | `GET /open/v1/market/snapshot`、`GET /open/v1/catalog/contract` |
| 非交易时段 | 查询合约交易时段和当晚夜盘日历，等待交易时段再下单 | `GET /open/v1/catalog/contract`、`GET /open/v1/catalog/session/night-today` |
| 实盘 CTP 自动登录失败 | 到 App 检查实盘账号状态与交易密码，更新凭据后重启会话 | App「我的 → 期货辅助交易」 |

