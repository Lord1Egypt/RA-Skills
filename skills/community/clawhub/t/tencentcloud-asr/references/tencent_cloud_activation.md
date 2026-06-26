# 腾讯云 ASR 开通与凭证获取

## 何时阅读本文档

仅在以下情况阅读：

- 用户还没有注册或登录腾讯云
- 用户还没有开通 ASR
- 用户不知道去哪里查看赠送资源包
- 用户不知道去哪里创建密钥
- 用户缺少 `SecretId`、`SecretKey`
- 用户需要额外找到 `AppId`（例如要运行 `flash_recognize.py`）

如果用户已经提供了可用凭证，则不要继续展开本文档。

## 使用原则

- 优先给用户最短路径，不要解释过多产品背景
- 优先告诉用户“当前页标题”和“要点哪个按钮”，而不是复述整页内容
- 如果 `assets/tencent-cloud-activation/` 下存在对应截图，优先把匹配图片返回给用户
- 如果截图不存在，就只返回文字步骤，不要假装图片可用
- 默认不要向用户讲解环境变量、shell 配置或底层命令；只有当用户明确要手工配置时，才提供对应系统的详细指引

## 最终目标

引导用户完成以下事项：

- 注册并登录腾讯云
- 进入 ASR 语音识别控制台
- 确认赠送资源包已到账
- 创建 API 密钥
- 保存 `SecretId`、`SecretKey`
- 找到并保存 `AppId`

## 截图资源命名约定

如果要给用户回传截图，优先使用以下文件名：

- `assets/tencent-cloud-activation/01-register.png`
- `assets/tencent-cloud-activation/02-search-asr.png`
- `assets/tencent-cloud-activation/03-enter-console.png`
- `assets/tencent-cloud-activation/04-resource-pack.png`
- `assets/tencent-cloud-activation/05-overview-create-key.png`
- `assets/tencent-cloud-activation/06-new-secret.png`
- `assets/tencent-cloud-activation/07-save-secret.png`
- `assets/tencent-cloud-activation/08-appid.png`

## 最短开通路径

### 步骤 1：注册并登录腾讯云

入口：

- 打开腾讯云官网
- 点击右上角“免费注册”或登录入口

当前页判断：

- 顶部左侧能看到“腾讯云”
- 右上角有注册或登录入口

配图：

- `assets/tencent-cloud-activation/01-register.png`

### 步骤 2：搜索 ASR 并进入语音识别产品页

入口：

- 在官网搜索框输入 `asr`
- 点击搜索结果里的“语音识别”产品页

当前页判断：

- 搜索结果出现“语音识别”
- 结果项通常带“产品”标签

配图：

- `assets/tencent-cloud-activation/02-search-asr.png`

### 步骤 3：进入 ASR 控制台

入口：

- 在语音识别产品页点击“立即使用”

当前页判断：

- 页面标题是“语音识别”
- 页面中有“立即使用”按钮

配图：

- `assets/tencent-cloud-activation/03-enter-console.png`

### 步骤 4：确认赠送资源包已到账

入口：

- 进入控制台后，左侧点击“语音识别资源包”

当前页判断：

- 列表里通常能看到赠送资源
- 常见项目包括：
  - 录音文件识别免费包
  - 录音文件识别极速版免费包
  - 语音流异步识别免费包
  - 实时语音识别免费包
  - 一句话识别免费包

如果用户能看到这些赠送额度，说明 ASR 服务通常已经可用。

配图：

- `assets/tencent-cloud-activation/04-resource-pack.png`

### 步骤 5：进入概览页并点击创建密钥

入口：

- 左侧点击“语音识别概览”
- 在“开始使用 ASR”区域点击“创建密钥”

当前页判断：

- 页面处于“语音识别概览”
- 页面中有“创建密钥”按钮

配图：

- `assets/tencent-cloud-activation/05-overview-create-key.png`

### 步骤 6：在 API 密钥管理页新建密钥

入口：

- 进入“访问密钥 > API 密钥管理”
- 点击“新建密钥”

当前页判断：

- 左侧导航高亮“API 密钥管理”
- 页面中有“新建密钥”按钮

配图：

- `assets/tencent-cloud-activation/06-new-secret.png`

### 步骤 7：立刻保存 SecretId 和 SecretKey

入口：

- 创建成功后，系统会弹窗显示 `SecretId` 和 `SecretKey`

必须提醒用户：

- `SecretKey` 通常只在创建当下展示一次
- 后续不能再次查看同一个 `SecretKey`
- 用户应立刻复制或下载保存

配图：

- `assets/tencent-cloud-activation/07-save-secret.png`

### 步骤 8：记录 AppId

入口：

- 回到 API 密钥管理列表页
- 在列表第一列找到 `APPID`

当前页判断：

- 列表里能看到 `APPID`
- 同行通常还能看到密钥状态或操作按钮

说明：

- 使用极速版脚本时需要 `AppId`
- 建议让用户和密钥一起保存

配图：

- `assets/tencent-cloud-activation/08-appid.png`

## 交付给 Agent 的最小口径

如果只是需要对用户说清楚要准备什么，必须先按会话类型选择口径：

- **群聊**：`❌ 这是群聊，不要把 SecretId、SecretKey、AppId 直接发出来，否则会泄漏。建议你手工配置，或者切到私聊后我再帮你配置。`
- **私聊**：`⚠️ 即使是私聊，密钥也会经过 LLM，存在泄漏风险。更建议你手工配置；如果你确认要我代配，可以把 SecretId、SecretKey 发给我；如果要用极速版，再补 AppId。`
- **无法判断是否群聊/私聊**：按群聊处理，先阻止用户直接发送密钥。

如果用户明确说“我要手工配置”或“给我详细步骤”，继续阅读 [env_config.md](env_config.md)。

## 常见提醒

- 如果用户找不到“创建密钥”，先让用户确认是否在“语音识别概览”或“API 密钥管理”页
- 如果用户已经创建过密钥但没有保存 `SecretKey`，通常需要新建一组密钥
- 如果用户只做普通一句话识别或录音文件识别，通常先要 `SecretId` 和 `SecretKey`
- 如果要运行 `flash_recognize.py`，还要补 `AppId`
