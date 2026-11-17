# Fintech Web 应用代码结构

> 当用户要求修改 racingai.top 网站功能、添加策略展示特性、修改持仓页面时参考。
> 仓库：Gitee warwickInv/fintech，部署在阿里云 ECS 47.121.180.199。

## 项目结构

```
fintech/
├── backend/                    # Go 后端（Gin 框架）
│   ├── config/config.go        # 数据库配置
│   ├── main.go                 # 入口
│   └── internal/
│       ├── router/router.go    # 路由定义
│       ├── handler/            # HTTP handler（参数解析 → 调 service）
│       │   └── strategy_handler.go
│       ├── service/            # 业务逻辑（核心计算在这里）
│       │   ├── strategy_service.go   # 策略服务（列表/详情/持仓/指标）
│       │   └── position_sizing.go    # 仓位管理优化
│       ├── dao/                # 数据访问层
│       │   ├── strategy_dao.go       # MySQL 查询
│       │   └── entity/               # 实体定义
│       ├── model/              # 数据模型
│       │   ├── strategy.go           # Strategy/Holding/Metrics 结构体
│       │   └── response.go           # API 响应包装
│       ├── middleware/cors.go  # CORS 中间件
│       └── database/db.go      # 数据库连接
├── my-app/                     # React 前端（Vite + TypeScript）
│   └── src/
│       ├── main.tsx            # 入口
│       ├── app/router.tsx      # React Router 路由
│       ├── pages/
│       │   ├── StrategyPlaza.tsx    # 策略广场页（列表）
│       │   └── StrategyDetail.tsx   # 策略详情页（走势图+持仓表+AI解读）
│       ├── services/
│       │   └── strategy.ts     # API 调用封装
│       ├── types/
│       │   └── strategy.ts     # TypeScript 类型定义
│       ├── utils/
│       │   ├── request.ts      # Axios 封装
│       │   └── format.ts       # 格式化工具
│       └── constants/index.ts
├── start-backend.sh / start-frontend.sh / start.sh / stop.sh
└── DEPLOYMENT.md / README.md / QUICKSTART.md
```

## 后端开发规范

### 新增 API 端点流程

1. **router.go** — 添加路由：
   ```go
   strategy.GET("/:id/new-feature", handler.NewFeature)
   ```

2. **handler** — 参数解析 + 调 service：
   ```go
   func NewFeature(c *gin.Context) {
       strategyID, _ := url.QueryUnescape(c.Param("id"))
       param := c.Query("param")  // ?param=value
       result, err := getStrategyService().NewFeature(strategyID, param)
       if err != nil {
           c.JSON(http.StatusInternalServerError, model.Error("失败"))
           return
       }
       c.JSON(http.StatusOK, model.Success(result))
   }
   ```

3. **service** — 业务逻辑：
   ```go
   func (s *StrategyService) NewFeature(strategyID string, param string) (*model.Result, error) {
       // 查数据库 → 计算 → 返回
   }
   ```

4. **model** — 如果有新数据结构，在 `model/strategy.go` 添加 struct + JSON tag

### GetHoldings 方法签名

```go
func (s *StrategyService) GetHoldings(strategyID string, asOfDate string, targetOnly bool, optimized bool) ([]model.Holding, error)
```

- `asOfDate`: 空=最新持仓；非空=该日历史截面
- `targetOnly`: true=仅最新截面，不做周期对比
- `optimized`: true=应用仓位管理优化（10%单仓上限+50%总仓位保底）

### Holding 模型

```go
type Holding struct {
    Rank      int     `json:"rank"`
    StockCode string  `json:"stockCode"`
    StockName string  `json:"stockName"`
    Weight    float64 `json:"weight"`       // 百分比（如 10.0 = 10%）
    Rebalance string  `json:"rebalance"`    // 买入/卖出/持有
    Change1D  float64 `json:"change1d"`     // 小数形式（0.01 = 1%）
    Change5D  float64 `json:"change5d"`
    Change20D float64 `json:"change20d"`
    Industry  string  `json:"industry"`
    Industry2 *string `json:"industry2,omitempty"`
}
```

⚠️ `Weight` 是百分比（如 10.0 = 10%），前端展示时 `w * 100` 转为百分比数字。
⚠️ `Change1D/5D/20D` 是小数形式（0.01 = 1%），前端展示时 `change * 100`。

## 前端开发规范

### 修改策略详情页

`StrategyDetail.tsx` 是核心页面，包含：
- 策略基本信息卡片
- AI 策略解读卡片
- 业绩走势图（ECharts + Segmented 时间段切换）
- 业绩指标卡片（年化收益/最大回撤/Sharpe/Calmar/信息比率/波动率）
- 策略持仓卡片（调仓一览表 + 目标持仓表 + DatePicker 日期选择）

### 持仓数据获取模式

```tsx
// 持仓数据独立于其他数据获取，支持开关切换
useEffect(() => {
  if (!id) return
  const dateStr = targetHoldingsDate?.format('YYYY-MM-DD')
  Promise.all([
    getHoldings(id, dateStr, false, optimized),  // 调仓交易
    getHoldings(id, dateStr, true, optimized),     // 目标持仓
  ]).then(([holdings, target]) => {
    setHoldingsDisplay(holdings)
    setTargetHoldingsDisplay(target)
  })
}, [id, optimized, targetHoldingsDate])
```

### API 调用

```typescript
// services/strategy.ts
export const getHoldings = (strategyId: string, tradeDate?: string, targetOnly?: boolean, optimized?: boolean) => {
  const params: { trade_date?: string; target?: string; optimized?: string } = {}
  if (tradeDate) params.trade_date = tradeDate
  if (targetOnly) params.target = '1'
  if (optimized) params.optimized = '1'
  return request.get<Holding[]>(`/strategy/${strategyId}/holdings`, { params: ... })
}
```

### UI 组件库

- **Ant Design 5.x**：Card, Table, Segmented, Statistic, Switch, DatePicker, Badge, Tooltip, Spin, Button, Space, Row, Col, message
- **ECharts**：`echarts-for-react`，走势图配置在 `getChartOption()` 函数中
- **dayjs**：日期处理

## 基础设施与运维

### Nginx 配置
- 配置文件：`/etc/nginx/conf.d/port_mapping.conf`
- 仅监听 **HTTP 80**，未配置 HTTPS/443（`nginx.conf` 中 TLS server 被注释）
- 代理：`racingai.top` -> `127.0.0.1:5173`（Vite dev server）
- **注意**：`https://racingai.top` 会连接超时，需用 `http://` 访问

### Systemd 服务
- **fintech-backend.service**：Go 后端，端口 8080
  - 配置：`/etc/systemd/system/fintech-backend.service`
  - WorkingDirectory: `/home/horserace/fintech/backend`
  - ExecStart: `/home/horserace/fintech/backend/fintech-backend`
  - 环境变量：`GIN_MODE=release`
  - 日志：`StandardOutput/StandardError` -> `/var/log/fintech/backend.log`
  - ⚠️ Go 应用 `log.Printf` 输出在 `/var/log/fintech/backend.log`，**不在 journalctl 中**（journalctl 只有 systemd 层面的启停日志）
- **frontend.service**：Vite dev server，端口 5173

### 双数据库配置
后端连接两个 MySQL 数据库（定义在 `config/config.go`）：

| 用途 | Host | Database | User | 说明 |
|------|------|----------|------|------|
| DisplayDB | localhost:3306 | db_strategy | display | 策略信息、持仓 |
| MonitorDB | 106.15.107.93:3306 | StockSignal | display | 业绩监控、净值数据 |

### Entity -> 表名映射
| Go Entity | MySQL 表名 | 说明 |
|-----------|----------|------|
| StrategyInfo | strategy_information | 策略基本信息 |
| StrategyMonitoring | strategy_pool_monitoring | 策略监控（净值/业绩走势） |
| StrategySnapshot | strategy_pool_monitoring_snap | 策略快照（指标统计） |
| StrategyHolding | 动态表名（strategy_table 字段值） | 每个策略的持仓数据 |
| StockInfo | stock_info_display | 股票信息 |
| AIExplainForStrategy | ai_explain_for_strategy | AI 策略解读 |

### API 路由总览
所有路由前缀 `/api/strategy`（定义在 `router/router.go`）：
- `GET /api/strategy/list` - 策略列表（支持 category/page/pageSize 参数）
- `GET /api/strategy/:id` - 策略详情
- `GET /api/strategy/:id/performance?period=3m` - 业绩走势数据（1m/3m/12m/all）
- `GET /api/strategy/:id/holdings?trade_date=&target=1` - 持仓
- `GET /api/strategy/:id/metrics?period=3m` - 业绩指标
- `GET /api/strategy/:id/stock-ai-explanation?stockCode=` - 股票AI解读

## 部署流程

```bash
# 在服务器上（SSH root@47.121.180.199）
cd /home/horserace/fintech
git fetch origin
git checkout <branch>

# 后端：编译 + 重启
cd backend && go build -o fintech-backend . && cd ..
systemctl restart fintech-backend

# 前端（如需构建生产版本）
cd my-app && npm run build
systemctl restart frontend
```

systemd 服务：`fintech-backend.service`（端口 8080）+ `frontend.service`（端口 5173）

## 调试指南

### 网站功能异常排查流程
1. **SSH 登录**：`ssh root@47.121.180.199`
2. **检查服务状态**：`systemctl is-active fintech-backend && systemctl is-active frontend`
3. **检查端口监听**：`ss -tlnp | grep -E ':(80|8080|5173) '`
4. **检查 nginx**：`cat /etc/nginx/conf.d/port_mapping.conf`
5. **测试 API**：`curl -sS http://127.0.0.1:8080/api/strategy/list?page=1&pageSize=5`
6. **查看后端日志**：`tail -50 /var/log/fintech/backend.log`（不是 journalctl！）
7. **检查数据库**：`mysql -u display -p"display999!" -h 106.15.107.93 StockSignal -e "SQL"`

### ⚠️ GORM 反模式：全局 MAX(date)
**问题**：不同策略的数据更新日期可能不一致。使用全局 `MAX(calculate_date)` 取到的最新日期只属于部分策略，用该日期查其他策略会返回 `record not found`。

**错误写法**：
```go
// 先取全局最新日期
dao.db.Select("MAX(calculate_date)").Scan(&latestDate) // ← 全局MAX
// 再用该日期查特定策略 → 可能查不到
dao.db.Where("strategy_id = ? AND calculate_date = ?", id, latestDate).First(&m)
```

**正确写法**（单策略）：
```go
dao.db.Select("MAX(calculate_date)").Where("strategy_id = ?", id).Scan(&latestDate)
```

**正确写法**（批量，多策略各自最新日期）：
```go
// 使用 INNER JOIN 子查询，每个策略取各自最新日期
dao.db.Raw(`
    SELECT t1.* FROM strategy_pool_monitoring t1
    INNER JOIN (
        SELECT strategy_id, MAX(calculate_date) AS max_date
        FROM strategy_pool_monitoring
        WHERE strategy_id IN (?)
        GROUP BY strategy_id
    ) t2 ON t1.strategy_id = t2.strategy_id AND t1.calculate_date = t2.max_date
`, strategyIDs).Scan(&results)
```

## Git 操作

```bash
# clone（私有仓库需 token）
GIT_TERMINAL_PROMPT=0 git clone https://oauth2:{TOKEN}@gitee.com/warwickInv/fintech.git

# 创建分支并推送
git checkout -b dev_hermes
git add -A
git config user.name 'Hermes Agent'
git config user.email 'hermes@nousresearch.com'
git commit -m "feat: description"
git push origin dev_hermes
```

⚠️ 如果以 root SSH 登录但仓库属于 horserace 用户，Git 会报 "dubious ownership"：
`git config --global --add safe.directory /home/horserace/fintech`

## 实战案例

2026-07-01 为 stgetf0001 策略添加仓位管理优化：
- 新建 `position_sizing.go`（107 行）— 核心仓位管理逻辑
- 修改 `strategy_service.go` — GetHoldings 新增 `optimized` 参数
- 修改 `strategy_handler.go` — 接收 `?optimized=1` 查询参数
- 修改 `strategy.ts` — API 新增 `optimized` 参数
- 修改 `StrategyDetail.tsx` — 持仓卡片新增「仓位优化」Switch 开关
- 新建 `POSITION_SIZING.md` — 优化方案文档
- 推送到 `dev_hermes` 分支（6 文件 +219/-35 行）
