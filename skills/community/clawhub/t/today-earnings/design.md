# today-earnings-skill 轻量技术设计文档

## 1. 背景

当前项目通过 OpenClaw browser 打开 Yahoo Finance earnings 页面，并在页面内执行 JavaScript 抓取财报数据。

本次改造目标是：

- 直接替换现有 OpenClaw browser 方案
- 改为 Chrome Extension + Native Messaging 架构
- 保持命令入口不变
- 让脚本可以直接触发浏览器侧采集并拿到 JSON 结果

本次只做第一版最小闭环，不追求功能铺满。

---

## 2. 需求范围

### 已确认需求

- 命令入口保持不变：

```bash
./scripts/get-company-list.sh 2026-03-14
```

- 底层改为：
  - Chrome 插件负责页面采集
  - Native Messaging Host 负责本地脚本与插件通信
  - 不再依赖 OpenClaw browser

- 输出要求：
  - stdout 只输出纯 JSON
  - 不输出中文摘要

- 第一版范围：
  - 只支持单日期
  - 不支持翻页

- JSON 字段：
  - `date`
  - `code`
  - `companyName`
  - `earningType`
  - `marketCap`

- 过滤规则全部保留：
  - 排除 `-B`
  - `-A` 标准化
  - 只保留 `AMC/BMO`
  - 排除 `marketCap === '--'`

- 错误处理：
  - 失败时退出非 0
  - 错误打印到 stderr

- 替换策略：
  - 直接替换旧实现
  - 不保留旧链路 fallback

### 第一版明确不做

- 不做翻页抓取
- 不做日期范围批量抓取
- 不做摘要输出
- 不保留 OpenClaw browser 兼容模式
- 不做复杂配置中心

---

## 3. 总体架构

执行链路如下：

```text
shell script
  -> Node CLI
    -> Native Messaging Host
      -> Chrome Extension background
        -> 打开 Yahoo Finance 页面
        -> 注入 content script
        -> 执行 parser
      <- 返回结构化结果
    <- 输出 JSON
```

### 分层职责

#### 3.1 shell 脚本层

文件：`scripts/get-company-list.sh`

职责：
- 接收日期参数
- 做基础参数校验
- 调用 Node CLI
- 将 Node CLI 的 stdout 原样输出
- 保持现有命令入口不变

#### 3.2 Node CLI 层

建议新增：`scripts/get-company-list.mjs`

职责：
- 接收 shell 传入的日期
- 连接 Native Host
- 发送抓取请求
- 接收抓取结果
- 成功时向 stdout 输出 JSON
- 失败时向 stderr 输出错误并退出非 0

#### 3.3 Native Messaging Host 层

建议目录：`native-host/`

职责：
- 实现 Chrome Native Messaging 协议
- 接收本地请求并转发给 Chrome 插件
- 等待插件处理结果
- 将结果回传给 CLI

说明：
- 这一层是 Chrome 插件与本地脚本的官方桥梁
- 采用 stdin/stdout 协议，不需要额外 HTTP 服务

#### 3.4 Chrome Extension Background 层

建议目录：`chrome-extension/`

职责：
- 接收来自 Native Host 的抓取请求
- 按日期构造 Yahoo Finance URL
- 打开目标页面
- 等待页面加载完成
- 协调 content script 提取数据
- 将结果回传给 Native Host

#### 3.5 Content Script 层

职责：
- 运行在 Yahoo Finance earnings 页面中
- 等待目标表格出现
- 调用 parser 提取页面数据
- 返回结构化结果

#### 3.6 Parser 层

职责：
- 只处理 DOM 解析和字段标准化
- 不负责消息通信、tab 控制和命令行输出
- 作为页面解析唯一来源，替代当前散落在脚本里的解析逻辑

---

## 4. 目录结构建议

建议调整为：

```text
today-earnings-skill/
  SKILL.md
  design.md
  scripts/
    get-company-list.sh
    get-company-list.mjs
  chrome-extension/
    manifest.json
    background.js
    content.js
    parser.js
  native-host/
    host.js
    com.today.earnings.host.json
  references/
    yahoo_earnings_calendar.md
```

说明：
- `format-earnings.py` 第一版可以移除，因为不再输出摘要
- `scripts/get-company-list.js` 中现有解析逻辑迁移到 `chrome-extension/parser.js`

---

## 5. 关键模块设计

## 5.1 命令入口

命令形式保持：

```bash
./scripts/get-company-list.sh 2026-03-14
```

行为：
- 用户传日期时使用传入日期
- 用户不传日期时，默认今天
- 日期格式必须为 `YYYY-MM-DD`

输出：
- 成功：stdout 输出 JSON 数组
- 失败：stderr 输出错误文本，进程退出非 0

---

## 5.2 请求协议

Node CLI 发给 Native Host 的请求建议为：

```json
{
  "type": "fetchEarnings",
  "date": "2026-03-14"
}
```

Chrome 插件返回成功结果：

```json
{
  "ok": true,
  "data": [
    {
      "date": "2026-03-14",
      "code": "HPE",
      "companyName": "Hewlett Packard Enterprise",
      "earningType": "AMC",
      "marketCap": "28.37B"
    }
  ]
}
```

Chrome 插件返回失败结果：

```json
{
  "ok": false,
  "error": {
    "code": "PAGE_TIMEOUT",
    "message": "等待 Yahoo Finance 财报表格超时"
  }
}
```

CLI 行为：
- `ok=true`：只打印 `data`
- `ok=false`：打印 `error.message` 到 stderr，并退出非 0

---

## 5.3 Yahoo 页面 URL 规则

第一版固定使用：

```text
https://finance.yahoo.com/calendar/earnings?day=YYYY-MM-DD&offset=0&size=100
```

说明：
- `offset=0`
- `size=100`
- 第一版不翻页，因此只抓这一页

---

## 5.4 页面等待策略

content script 需要等待表格加载，而不是页面一打开就立即抓取。

第一版建议策略：
- 轮询查找表格区域
- 每 300ms 检查一次
- 超时时间 10 秒
- 超时则返回 `PAGE_TIMEOUT`

原因：
- 简单直接
- 比硬编码 `sleep 5` 更稳
- 第一版先不引入复杂 `MutationObserver`

---

## 5.5 Parser 规则

parser 从页面表格提取原始记录后，执行以下逻辑：

### 字段提取
- `date`：由请求日期透传
- `code`：股票代码
- `companyName`：公司名称
- `earningType`：财报发布时间
- `marketCap`：市值

### 过滤规则
- 排除代码以 `-B` 结尾的股票
- 代码以 `-A` 结尾时去掉 `-A`
- 只保留 `earningType` 为 `AMC` 或 `BMO`
- 排除 `marketCap === '--'`

### 输出结构

```json
[
  {
    "date": "2026-03-14",
    "code": "HPE",
    "companyName": "Hewlett Packard Enterprise",
    "earningType": "AMC",
    "marketCap": "28.37B"
  }
]
```

---

## 5.6 Chrome Extension 设计

### manifest.json
权限建议：
- `tabs`
- `scripting`
- `nativeMessaging`
- host permission：`https://finance.yahoo.com/*`

### background.js
职责：
- 接收 host 请求
- 打开目标 tab
- 等待 `tabs.onUpdated` 进入 `complete`
- 向 content script 发消息请求提取
- 收到结果后回传给 host
- 成功后关闭 tab

### content.js
职责：
- 响应 background 发来的 `extract` 消息
- 等待表格可见
- 调用 parser
- 返回结构化结果

### parser.js
职责：
- 集中管理 DOM 查询与字段转换逻辑
- 避免解析逻辑散落在多个文件里

---

## 5.7 Native Host 设计

### host.js
职责：
- 作为 Chrome Native Messaging Host 运行
- 接收 CLI 输入
- 与扩展建立连接
- 转发请求
- 输出响应

### host manifest
文件建议：`native-host/com.today.earnings.host.json`

内容示意：

```json
{
  "name": "com.today.earnings.host",
  "description": "Today Earnings Native Messaging Host",
  "path": "/absolute/path/to/native-host/host.js",
  "type": "stdio",
  "allowed_origins": [
    "chrome-extension://YOUR_EXTENSION_ID/"
  ]
}
```

注意：
- `path` 必须是绝对路径
- `allowed_origins` 需要匹配最终扩展 ID
- macOS 需要把 manifest 安装到 Chrome 识别目录

---

## 6. 实施步骤

建议按下面顺序开发：

### 第 1 步：抽离 parser
- 从现有 `scripts/get-company-list.js` 中提取解析逻辑
- 改成 `chrome-extension/parser.js`
- 顺手补上 `companyName`

### 第 2 步：实现 content script
- 页面加载后等待表格
- 调 parser
- 返回 JSON

### 第 3 步：实现 background
- 接请求
- 开 tab
- 调 content script
- 收结果
- 关 tab

### 第 4 步：实现 Native Host
- 建立 host 与扩展通信
- 打通请求/响应

### 第 5 步：实现 Node CLI
- 从 shell 进入 Node
- 输出标准 JSON / 错误

### 第 6 步：替换 shell 脚本
- 保留命令形式
- 改成调用 Node CLI

---

## 7. 验收标准

满足以下条件即可认为第一版完成：

1. 可以通过以下命令执行：

```bash
./scripts/get-company-list.sh 2026-03-14
```

2. 不依赖 OpenClaw browser

3. 成功时 stdout 只输出 JSON 数组

4. JSON 每项包含：
- `date`
- `code`
- `companyName`
- `earningType`
- `marketCap`

5. 过滤规则符合当前既有逻辑

6. 失败时退出非 0，并把错误输出到 stderr

---

## 8. 后续可扩展项

这些不是第一版范围，但后续可以继续做：

- 自动翻页抓取
- 日期范围批量抓取
- 调试日志开关
- 安装脚本（自动注册 Native Host）
- 扩展状态检测
- 命令行参数扩展（如 `--json-pretty`）
- 抓取结果缓存

---

## 9. 结论

本次第一版采用“Chrome 插件负责采集 + Native Messaging 负责桥接 + shell 保持原入口”的方案。

这个方案能满足当前最核心目标：
- 摆脱 OpenClaw browser 控制
- 保留现有命令入口
- 面向脚本化使用
- 输出稳定纯 JSON

同时范围控制得足够小，适合快速落地第一版。 
