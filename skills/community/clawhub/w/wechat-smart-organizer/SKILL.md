---
name: wechat-smart-organizer
description: 微信聊天记录智能整理技能。当用户想要读取微信聊天记录、提取关键信息、存储到Obsidian笔记、或创建日历事件时使用此技能。功能包括：查询会话、读取聊天记录、搜索关键词、提取任务/时间/待办事项、智能分类存储到Obsidian、创建日历提醒。
agent_created: true
version: 1.0.0
author: ppj
tags: [wechat, organizer, obsidian, productivity]
homepage: https://github.com/ppj/wechat-smart-organizer
---

# 微信聊天记录智能整理技能

本技能整合 wechat-cli、Obsidian 笔记系统和日历系统，帮助用户从微信聊天记录中提取关键信息并智能整理。

## 核心能力

1. **读取微信数据** - 通过 wechat-cli 访问本地微信聊天记录
2. **智能信息提取** - 从聊天内容中识别任务、截止日期、会议、联系人等关键信息
3. **Obsidian 存储** - 将整理后的信息存储到 Obsidian 知识库
4. **日历事件创建** - 识别时间相关事项并创建日历事件和提醒

# 微信聊天记录智能整理技能

本技能整合 wechat-cli、Obsidian 笔记系统和日历系统，帮助用户从微信聊天记录中提取关键信息并智能整理。

## 核心能力

1. **读取微信数据** - 通过 wechat-cli 访问本地微信聊天记录
2. **智能信息提取** - 从聊天内容中识别任务、截止日期、会议、联系人等关键信息
3. **Obsidian 存储** - 将整理后的信息存储到 Obsidian 知识库
4. **日历事件创建** - 识别时间相关事项并创建日历事件和提醒

## 前置检查

### 检查 wechat-cli 安装状态

```bash
which wechat-cli
```

如果未安装，提示用户执行：
```bash
npm install -g @canghe_ai/wechat-cli
# 或
pip install wechat-cli
```

### 初始化微信数据访问

首次使用需要初始化：
```bash
sudo wechat-cli init
```

> ⚠️ macOS 用户需要授予终端「完全磁盘访问权限」

## 核心命令参考

### 会话管理
```bash
wechat-cli sessions                    # 最近会话列表
wechat-cli sessions --limit 10        # 指定数量
wechat-cli unread                     # 未读会话
```

### 聊天记录读取
```bash
wechat-cli history "联系人/群名" --limit 50           # 最近50条
wechat-cli history "联系人" --start-time "2026-01-01" --end-time "2026-01-31"  # 时间范围
wechat-cli history "群名" --type link                  # 仅链接类消息
```

### 搜索功能
```bash
wechat-cli search "关键词"                              # 全局搜索
wechat-cli search "deadline" --chat "项目群"          # 指定聊天搜索
wechat-cli search "会议" --type text                   # 仅文本消息
```

### 联系人与统计
```bash
wechat-cli contacts --query "姓名"     # 搜索联系人
wechat-cli stats "群名"               # 群聊统计
wechat-cli members "群名"            # 群成员列表
```

### 导出功能
```bash
wechat-cli export "联系人" --format markdown --output chat.md
wechat-cli favorites                   # 微信收藏
```

## Obsidian Vault 检测

### 获取 Obsidian Vault 列表

在 macOS 上，Obsidian vault 配置存储在：
```
~/Library/Application Support/obsidian/obsidian.json
```

**检测步骤：**

1. 读取 Obsidian 配置文件：
```bash
cat ~/Library/Application\ Support/obsidian/obsidian.json
```

2. 解析 vault 信息：
```json
{
  "vaults": {
    "vault_id_1": {
      "path": "/Users/xxx/Documents/obsidian/vault1",
      "ts": 1234567890,
      "open": true
    },
    "vault_id_2": {
      "path": "/Users/xxx/另一个笔记库",
      "ts": 1234567890,
      "open": false
    }
  }
}
```

3. **优先规则**：
   - 如果只有一个 vault，直接使用
   - 如果有多个 vault，询问用户选择
   - 优先使用 `open: true` 的 vault

### Obsidian 存储路径

**重要**：Obsidian vault 路径不是 `~/Obsidian/`，而是实际配置的路径。

常见路径格式：
- `/Users/{用户名}/Documents/obsidian/{vault名}/`
- `/Users/{用户名}/{自定义路径}/`

## 智能信息提取流程

### 步骤1：获取原始数据

根据用户需求选择合适的命令获取聊天记录：

- **日常浏览**：`wechat-cli sessions --limit 20`
- **特定联系人**：`wechat-cli history "姓名" --limit 100 --format json`
- **关键词搜索**：`wechat-cli search "关键词" --limit 50 --format json`

### 步骤2：识别关键信息

从聊天内容中智能识别以下类型的信息：

| 类型 | 识别关键词 | 示例 |
|------|-----------|------|
| 任务/待办 | "需要做"、"麻烦"、"帮我"、"记得" | "记得明天帮我带文件" |
| 截止日期 | "截止"、"deadline"、"周X"、"X号" | "这个任务截止到周五" |
| 会议/约定 | "会议"、"约"、"几点"、"什么时候" | "我们约明天下午3点开会" |
| 电话/联系方式 | "电话"、"微信"、"加我" | "加我微信: xxx" |
| 地址/位置 | "地址"、"去哪"、"位置" | "公司地址是xxx" |
| 金额/交易 | "多少钱"、"转账"、"收款" | "这个产品298元" |
| 重要文件 | "文件"、"发给你"、"附件" | "我把合同发给你" |

### 步骤3：分类存储

根据信息类型选择存储目标：

#### 存储到 Obsidian

**重要**：先检测 Obsidian vault 的实际路径，不要假设为 `~/Obsidian/`。

**步骤**：

1. **检测 Obsidian vault 路径**：
```bash
# 读取 Obsidian 配置文件
cat ~/Library/"Application Support"/obsidian/obsidian.json

# 解析 JSON，获取 vault 路径
# 格式：{"vaults":{"vault_id_1":{"path":"/actual/path","ts":...,"open":true}}}
```

2. **确定目标路径**：
   - 如果只有一个 vault，直接使用
   - 如果有多个 vault，询问用户选择
   - 优先使用 `open: true` 的 vault

3. **按类型创建/更新笔记**（使用检测到的 vault 路径）：
   - **任务** → `{vault_path}/待办事项/{日期}.md`
   - **会议** → `{vault_path}/会议记录/{日期}-{主题}.md`
   - **联系人** → `{vault_path}/联系人/{姓名}.md`
   - **项目** → `{vault_path}/项目/{项目名}/相关沟通.md`
   - **幼儿教育** → `{vault_path}/幼儿教育/{主题分类}/`

**注意**：
- Vault 路径可能包含空格（如 `/Users/xxx/Documents/obsidian/ppj/`），复制文件时需要用引号包裹路径
- 如果无法读取 Obsidian 配置，再回退到询问用户

**Obsidian 笔记模板格式**：
```markdown
---
type: wechat-extract
source: {联系人/群名}
created: {当前日期}
tags: [#微信 #待办] 或 [#微信 #会议]
---

# {标题}

## 原始内容
> {引用原文}

## 提取信息
{关键字段}

## 提取时间
{当前时间}

## 相关上下文
{周围聊天内容}
```

#### 存储到日历

对于包含明确时间的事项，创建日历事件：

1. 识别时间表达式（"明天3点"、"周五下午"、"下周一"）
2. 构建日历事件：
   - 事件标题：从聊天内容提取
   - 开始/结束时间：基于识别的时间
   - 提醒：提前15-30分钟
   - 备注：完整聊天上下文

**使用腾讯会议技能创建会议**（如涉及多方）：
```bash
# 调用 tencent-meeting-skill 创建会议
```

## 使用场景示例

### 场景1：整理项目沟通

```
用户：帮我把「项目A群」里关于「周五上线」的消息整理一下
```

执行流程：
1. `wechat-cli search "上线" --chat "项目A群" --format json`
2. 提取所有相关消息
3. 创建 Obsidian 笔记：`项目/项目A/周五上线沟通.md`
4. 如有明确时间，创建日历提醒

### 场景2：提取待办事项

```
用户：从和老板的聊天记录里找出所有待办
```

执行流程：
1. `wechat-cli history "老板" --limit 200 --format json`
2. 筛选包含待办关键词的消息
3. 生成待办清单
4. 存储到 `~/Obsidian/待办/老板安排.md`

### 场景3：备份重要联系人信息

```
用户：把最近加的联系人信息存到笔记里
```

执行流程：
1. `wechat-cli contacts --query "关键词"`
2. 获取联系人详情
3. 创建 Obsidian 联系人笔记

## 输出格式规范

### 终端输出
使用 `--format text` 参数获取人类可读的输出格式。

### JSON 输出
使用 `--format json` 参数获取结构化数据，便于程序处理。

### 文件导出
使用 `--output {文件名}` 将内容导出到文件。

## 注意事项

1. **隐私保护**：微信数据仅本地处理，不上传任何数据
2. **微信运行要求**：执行命令时微信需处于运行状态
3. **权限要求**：macOS 需授予「完全磁盘访问权限」
4. **首次使用**：先运行 `sudo wechat-cli init` 初始化
5. **Obsidian 路径检测**：**必须先检测 Obsidian vault 的实际路径**，不要假设为 `~/Obsidian/`
   - 读取 `~/Library/Application Support/obsidian/obsidian.json`
   - 解析 `vaults` 字段获取实际路径
   - 示例：`/Users/peterpan/Documents/obsidian/ppj/`（不是 `~/Obsidian/`）
6. **时间识别**：时间表达式的解析需结合上下文确认准确性
7. **文件权限**：微信本地文件默认只读（`-r--r--r--`），复制后可能需要修改权限

## 错误处理

| 错误信息 | 解决方案 |
|---------|---------|
| "微信未运行" | 启动微信后重试 |
| "需要初始化" | 运行 `sudo wechat-cli init` |
| "权限被拒绝" | 检查终端是否具有完全磁盘访问权限 |
| "找不到联系人" | 使用 `wechat-cli sessions` 确认正确的联系人名称 |
