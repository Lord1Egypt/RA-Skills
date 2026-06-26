---
name: stock-select
description: AI驱动的智能选股与交易助手。自然语言选股（如"涨停股"、"主力净流入>10%"），Level2主力资金数据，集合竞价异动监控，多券商账户管理与AI辅助下单。让选股→分析→交易一站式完成。触发词：选股、问财、股票查询、主力资金、大单净额、涨停、集合竞价、股票行情、交易下单。
author: hailong787@163.com
license: MIT
version: 2.0.2
---

# 智能选股技能

基于自然语言的智能选股工具，类似同花顺问财。支持行情查询、动态选股、用户认证、Level2数据、交易下单。

**官网**: https://stockbot.me

## 外部依赖声明

本技能依赖以下外部 API 服务：

| 服务 | 地址 | 用途 | 认证 |
|------|------|------|------|
| Stockboot API | `https://api.stockbot.me` | 股票行情查询、动态选股、用户认证、交易 | 部分接口需要 Token |

### 隐私与数据安全

- **数据流向**：仅向 Stockboot API 发送请求
- **数据类型**：股票代码、选股条件、用户认证信息
- **传输安全**：所有请求使用 HTTPS 加密传输
- **Token 存储**：建议在会话中使用，不要持久化存储

### 自托管选项

本技能的 API 服务可自行部署。如需自托管，请参考：
- 后端源码：私有仓库
- 部署后修改环境变量 `STOCKBOOT_API_URL` 指向您的服务地址

---

## 环境配置

默认 API 地址：`https://api.stockbot.me`

可通过环境变量自定义：
```bash
export STOCKBOOT_API_URL="https://your-server/api"
```

---

## 一、用户认证接口 (/auth)

### 1.1 用户登录
- **接口**: `POST ${STOCKBOOT_API_URL}/auth/login`
- **说明**: 用户登录，返回 Token 和账户列表
- **Body**: `{"username": "xxx", "password": "xxx"}`
- **返回字段**:
  - `userInfo`: 用户信息（vipLevel, role, phone, nickname, vipExpireTime）
  - `accounts`: 账户列表（id, accountName, brokerType, brokerAccount, availableBalance 等）
  - `token`: JWT Token（有效期7天）
  - `refreshToken`: 刷新 Token（有效期14天）
- **示例**:
  ```bash
  curl -X POST "${STOCKBOOT_API_URL}/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username": "18680859800", "password": "abcd1234"}'
  ```
- **VIP等级说明**:
  - vipLevel=0: 普通用户，仅基础行情
  - vipLevel=1: VIP用户，Level2数据
  - vipLevel=2: 超级VIP，Level2数据 + 交易功能

### 1.2 用户注册
- **接口**: `POST ${STOCKBOOT_API_URL}/auth/register`
- **说明**: 用户注册（需要短信验证码）
- **Body**: `{"phone": "xxx", "password": "xxx", "confirmPassword": "xxx", "code": "xxx"}`
- **示例**:
  ```bash
  curl -X POST "${STOCKBOOT_API_URL}/auth/register" \
    -H "Content-Type: application/json" \
    -d '{"phone": "13800138000", "password": "test123", "confirmPassword": "test123", "code": "123456"}'
  ```

### 1.3 发送验证码
- **接口**: `POST ${STOCKBOOT_API_URL}/auth/sms/send`
- **说明**: 发送短信验证码（用于注册/登录）
- **Body**: `{"phone": "xxx", "type": "register/login"}`
- **示例**:
  ```bash
  curl -X POST "${STOCKBOOT_API_URL}/auth/sms/send" \
    -H "Content-Type: application/json" \
    -d '{"phone": "13800138000", "type": "register"}'
  ```

### 1.4 刷新 Token
- **接口**: `POST ${STOCKBOOT_API_URL}/auth/refresh`
- **说明**: 使用 refreshToken 刷新 access token
- **Header**: `Authorization: Bearer ${refreshToken}`
- **示例**:
  ```bash
  curl -X POST "${STOCKBOOT_API_URL}/auth/refresh" \
    -H "Authorization: Bearer ${refreshToken}"
  ```

### 1.5 退出登录
- **接口**: `POST ${STOCKBOOT_API_URL}/auth/logout`
- **说明**: 退出登录，Token失效
- **Header**: `Authorization: Bearer ${token}`
- **示例**:
  ```bash
  curl -X POST "${STOCKBOOT_API_URL}/auth/logout" \
    -H "Authorization: Bearer ${token}"
  ```

---

## 二、行情接口 (/quote)

> **注意**: 带 Token 访问行情接口会返回 Level2 数据（VIP功能）

### 2.1 获取单只股票行情
- **接口**: `GET ${STOCKBOOT_API_URL}/quote/{stockCode}`
- **说明**: 获取股票实时行情，包括五档买卖
- **Header**: 无需认证（普通行情）；带 Token 返回 Level2 数据
- **示例**:
  ```bash
  # 普通行情
  curl "${STOCKBOOT_API_URL}/quote/600519"
  
  # Level2 数据（需要 Token）
  curl "${STOCKBOOT_API_URL}/quote/600519" \
    -H "Authorization: Bearer ${token}"
  ```
- **返回字段**:
  - 基础字段: stockCode, stockName, currentPrice, changeRate, volume, amount, 五档买卖等
  - **Level2 字段** (VIP):
    - `mainNetInflow`: 大单净额（主力净额，单位：元）
    - `mainNetInflowRate`: 大单净量占比（主力净量占比，百分比）

### 2.2 批量获取股票行情
- **接口**: `POST ${STOCKBOOT_API_URL}/quote/batch`
- **说明**: 批量获取多只股票实时行情（优化传输格式）
- **Body**: `["600519", "000001", "300750"]`
- **Header**: 带 Token 返回 Level2 数据
- **示例**:
  ```bash
  # 普通行情
  curl -X POST "${STOCKBOOT_API_URL}/quote/batch" \
    -H "Content-Type: application/json" \
    -d '["600519", "000001", "300750"]'
  
  # Level2 数据
  curl -X POST "${STOCKBOOT_API_URL}/quote/batch" \
    -H "Authorization: Bearer ${token}" \
    -H "Content-Type: application/json" \
    -d '["600519", "000001", "300750"]'
  ```
- **返回字段**: fields（字段名数组，含 mainNetInflow、mainNetInflowRate）, items（数据二维数组）

### 2.3 搜索股票
- **接口**: `POST ${STOCKBOOT_API_URL}/quote/search`
- **说明**: 根据股票代码、简称或名称搜索股票
- **Body**: `{"keyword": "xxx"}`
- **示例**:
  ```bash
  curl -X POST "${STOCKBOOT_API_URL}/quote/search" \
    -H "Content-Type: application/json" \
    -d '{"keyword": "茅台"}'
  ```

### 2.4 获取分时数据
- **接口**: `GET ${STOCKBOOT_API_URL}/quote/minute/{stockCode}?tradeDate=xxx`
- **说明**: 获取股票分时行情数据，不指定日期则获取当天
- **示例**:
  ```bash
  curl "${STOCKBOOT_API_URL}/quote/minute/600519"
  ```
- **返回字段**: time, volume, amount, avgPrice, cumulativeAvgPrice, changeRate, close

### 2.5 获取分时数据（优化传输）
- **接口**: `GET ${STOCKBOOT_API_URL}/quote/minute/{stockCode}/optimized?tradeDate=xxx`
- **说明**: 获取分时数据，字段名和数据分离，减少网络传输量

### 2.6 获取集合竞价数据
- **接口**: `GET ${STOCKBOOT_API_URL}/quote/call-auction/{stockCode}?tradeDate=xxx`
- **说明**: 获取早盘集合竞价数据（9:15-9:25）
- **示例**:
  ```bash
  curl "${STOCKBOOT_API_URL}/quote/call-auction/600519"
  ```
- **返回字段**: time, price, bid1-5, ask1-5, bidSize1-5, askSize1-5, volume, amount

### 2.7 获取集合竞价数据（优化传输）
- **接口**: `GET ${STOCKBOOT_API_URL}/quote/call-auction/{stockCode}/optimized?tradeDate=xxx`

### 2.8 获取股票基础数据
- **接口**: `GET ${STOCKBOOT_API_URL}/quote/basic-data/{stockCode}`
- **说明**: 获取融资融券、次新、市盈率、市净率、板块、概念等基础数据
- **示例**:
  ```bash
  curl "${STOCKBOOT_API_URL}/quote/basic-data/600519"
  ```

### 2.9 获取历史K线数据
- **接口**: `GET ${STOCKBOOT_API_URL}/quote/kline/{stockCode}?interval=D&startDate=xxx&endDate=xxx&appendToday=false`
- **参数**:
  - `interval`: K线周期 (D=日, W=周, M=月, Q=季, Y=年)
  - `startDate`: 开始日期
  - `endDate`: 结束日期
  - `appendToday`: 是否包含今天
- **示例**:
  ```bash
  curl "${STOCKBOOT_API_URL}/quote/kline/600519?interval=D&appendToday=true"
  ```

### 2.10 获取历史K线数据（优化传输）
- **接口**: `GET ${STOCKBOOT_API_URL}/quote/kline/{stockCode}/optimized`

---

## 三、账户接口 (/account)

> **需要 Token 认证**

### 3.1 获取账户列表
- **接口**: `GET ${STOCKBOOT_API_URL}/account/list`
- **说明**: 获取用户绑定的所有交易账户
- **Header**: `Authorization: Bearer ${token}`
- **示例**:
  ```bash
  curl "${STOCKBOOT_API_URL}/account/list" \
    -H "Authorization: Bearer ${token}"
  ```
- **返回字段**:
  - `id`: 账户ID
  - `accountName`: 账户名称
  - `brokerType`: 券商类型（0=东方财富, 7=国金证券）
  - `brokerTypeName`: 券商名称
  - `brokerAccount`: 券商账号
  - `isCreditAccount`: 是否信用账户
  - `availableBalance`: 可用余额
  - `totalAssets`: 总资产
  - `positionValue`: 持仓市值
  - `todayProfit`: 今日盈亏
  - `deviceOnline`: 设备在线状态
  - `isPrimary`: 是否主账户
  - `status`: 账户状态（1=正常）

---

## 四、交易接口 (/trade)

> **需要 Token 认证 + VIP等级 >= 2**

### 4.1 下单
- **接口**: `POST ${STOCKBOOT_API_URL}/trade/order`
- **说明**: 买入或卖出股票
- **Header**: `Authorization: Bearer ${token}`
- **Body**:
  ```json
  {
    "accountId": 1001,           // 账户ID（从账户列表获取）
    "stockCode": "600666",       // 股票代码
    "stockName": "奥瑞德",       // 股票名称
    "price": 6.00,               // 价格（市价单可忽略）
    "quantity": 100,             // 数量（股）
    "orderType": 0,              // 0=买入, 1=卖出
    "priceType": "LIMIT"         // LIMIT=限价, MARKET=市价
  }
  ```
- **示例**:
  ```bash
  # 限价买入
  curl -X POST "${STOCKBOOT_API_URL}/trade/order" \
    -H "Authorization: Bearer ${token}" \
    -H "Content-Type: application/json" \
    -d '{"accountId":1001,"stockCode":"600666","stockName":"奥瑞德","price":6.00,"quantity":100,"orderType":0,"priceType":"LIMIT"}'
  
  # 市价卖出
  curl -X POST "${STOCKBOOT_API_URL}/trade/order" \
    -H "Authorization: Bearer ${token}" \
    -H "Content-Type: application/json" \
    -d '{"accountId":1001,"stockCode":"600666","stockName":"奥瑞德","quantity":100,"orderType":1,"priceType":"MARKET"}'
  ```
- **返回字段**:
  - `id`: 订单ID
  - `status`: 状态（5=失败，其他状态待补充）
  - `errorMessage`: 错误信息（如"委托价格超过跌停价格"）

---

## 五、动态选股接口 (/dynamic-select)

- **接口**: `POST ${STOCKBOOT_API_URL}/dynamic-select/execute`
- **说明**: 使用自然语言选股
- **Body**: `{"sentence": "选股条件"}`
- **示例**:
  ```bash
  curl -X POST "${STOCKBOOT_API_URL}/dynamic-select/execute" \
    -H "Content-Type: application/json" \
    -d '{"sentence": "涨停"}'
  ```

---

## 六、动态选股查询语法

当用户提出选股需求时，将自然语言转换为查询条件。

### 支持的查询模式

1. **涨跌停类**:
   - `涨停` / `跌停`
   - `涨幅大于8%未涨停非ST`
   - `非一字涨停非ST`

2. **涨幅类**:
   - `涨幅大于5%` / `涨幅小于-3%`
   - `连续3天上涨`
   - `前5日平均涨幅大于20%`

3. **财务指标**:
   - `市盈率小于20` / `市净率小于2`
   - `流通市值小于50亿`

4. **组合条件** (分号分隔):
   - `涨幅大于5%;非ST`
   - `前5日平均涨幅大于20%;前10日涨停次数大于1`
   - `连续5日净买入且主力净流入占比大于10%非ST`

5. **排除条件**:
   - `非ST` / `非新股`

---

## 七、使用流程

### 7.1 基础行情（无需登录）

```bash
# 查询股票行情
curl "${STOCKBOOT_API_URL}/quote/600519"

# 动态选股
curl -X POST "${STOCKBOOT_API_URL}/dynamic-select/execute" \
  -H "Content-Type: application/json" \
  -d '{"sentence": "涨停"}'
```

### 7.2 VIP 用户（Level2数据）

```bash
# 1. 登录获取 Token
RESPONSE=$(curl -s -X POST "${STOCKBOOT_API_URL}/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"18680859800","password":"abcd1234"}')
TOKEN=$(echo $RESPONSE | jq -r '.data.token')

# 2. 获取 Level2 数据
curl "${STOCKBOOT_API_URL}/quote/600519" \
  -H "Authorization: Bearer $TOKEN"
# 返回: mainNetInflow（主力净额）, mainNetInflowRate（主力净量占比）
```

### 7.3 超级VIP（交易功能）

```bash
# 1. 登录
TOKEN=$(...)

# 2. 获取账户列表
curl "${STOCKBOOT_API_URL}/account/list" \
  -H "Authorization: Bearer $TOKEN"

# 3. 下单交易
curl -X POST "${STOCKBOOT_API_URL}/trade/order" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"accountId":1001,"stockCode":"600666","stockName":"奥瑞德","price":6.00,"quantity":100,"orderType":0,"priceType":"LIMIT"}'
```

---

## 八、示例对话

**用户**: 帮我找今天涨停的股票
**助手**: 调用 `/dynamic-select/execute` 查询"涨停"，返回涨停股票列表

**用户**: 查询茅台的行情，我要看主力净额
**助手**: 需要先登录获取 Token，然后调用 `/quote/600519` 带 Authorization header，返回包含 mainNetInflow 的数据

**用户**: 我要买入奥瑞德100股，价格6元
**助手**: 
1. 确认用户已登录且有交易权限
2. 获取账户列表确认 accountId
3. 调用 `/trade/order` 下单

**用户**: 市盈率低的小盘股有哪些？
**助手**: 调用 `/dynamic-select/execute` 查询"市盈率小于20;流通市值小于50亿"

---

## 九、错误处理

| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| 9001 | 参数错误 | 检查请求参数格式 |
| 403 | 未授权/Token失效 | 重新登录获取 Token |
| 500 | 系统异常 | 稍后重试或联系管理员 |

---

## 十、更新日志

### v2.0.0 (2026-04-20)
- ✨ 新增用户认证接口（登录、注册、验证码、刷新Token、退出）
- ✨ 新增 Level2 数据支持（主力净额、主力净量）- VIP功能
- ✨ 新增账户接口（获取账户列表）
- ✨ 新增交易接口（下单买入/卖出）- 超级VIP功能
- 📝 完善接口文档和使用示例

### v1.5.1 (2026-03-21)
- 基础行情查询
- 动态选股功能