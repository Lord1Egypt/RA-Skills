# 统一错误处理模板

## 适用范围

本模板适用于 PostgreSQL skill 在调用腾讯云 OpenAPI 前后的公共错误引导，重点覆盖：
- 凭证缺失
- 地域非法
- 巡检目标缺失
- SDK 缺失

## 总原则

- **先指出具体缺了什么**，不要只说“配置错误”
- **直接给下一步修复动作**，不要让用户自己猜
- **优先给可直接操作的控制台 / 产品网站入口，不要默认先给文档页**
- **如果必须补充文档，放在控制台入口之后，不能让文档页成为首个动作**
- **如果缺的是非密钥且当前 skill 具备安全代查能力，要同时提供“我可以代你查”选项**
- **密钥、Token、API Key 等敏感值只给官方控制台 / 产品网站入口和配置方式，不承诺代取**
- **涉及命令执行时先征求用户确认**，不要在未确认前自动安装依赖
- **如果已有 TC3 fallback 路径可继续执行，应先说明 fallback 是否可用**

## `missing-credentials` 模板

### 触发条件
- 缺少 `TENCENTCLOUD_SECRET_ID`
- 缺少 `TENCENTCLOUD_SECRET_KEY`
- 缺少 `TENCENTCLOUD_REGION`
- 或宿主尚未把自定义凭证变量映射到标准 `TENCENTCLOUD_*` 变量

### 必须输出的内容
- 缺失的变量名
- 一段最小可复制配置示例
- 官方控制台 / 产品网站入口链接
- 最短点击路径或操作步骤
- 对可安全代查的非密钥项，补一句我可以代查什么
- 明确说明修好后用户应把信息放在哪里

### 推荐回复模板

```text
当前缺少运行 PostgreSQL skill 所需的凭证/地域信息：<缺失变量列表>。

先获取和核对这些信息：
- API 密钥控制台：https://console.cloud.tencent.com/cam/capi
  - 如果还没有密钥，进入后点击“新建密钥”或“创建密钥”
  - 推荐优先使用最小权限 CAM 子账号
  - 创建后立即保存 `SecretId` / `SecretKey`
  - `SecretKey` 一般只在创建时完整展示一次，丢失后需要重新创建并轮换旧密钥
- PostgreSQL 控制台：https://console.cloud.tencent.com/postgres
  - 打开后先看右上角地域选择器
  - 如果已有实例，可直接在实例列表查看目标实例所属地域
  - 如果你准备新建实例，也可以先在这里确认计划使用的地域

如果你是从 CLI 启动，就直接在执行启动命令前运行：
export TENCENTCLOUD_SECRET_ID="你的 SecretId"
export TENCENTCLOUD_SECRET_KEY="你的 SecretKey"
export TENCENTCLOUD_REGION="ap-guangzhou"
# 如果你使用临时凭证，再补 TENCENTCLOUD_SESSION_TOKEN

然后验证：
echo $TENCENTCLOUD_SECRET_ID
echo $TENCENTCLOUD_REGION

如果你使用的是 WorkBuddy 或其他桌面客户端（macOS），不要只做临时 `export`，而是先在终端运行：
launchctl setenv TENCENTCLOUD_SECRET_ID "你的 SecretId"
launchctl setenv TENCENTCLOUD_SECRET_KEY "你的 SecretKey"
launchctl setenv TENCENTCLOUD_REGION "ap-guangzhou"
# launchctl setenv TENCENTCLOUD_SESSION_TOKEN "你的 SessionToken"

再验证：
launchctl getenv TENCENTCLOUD_SECRET_ID
launchctl getenv TENCENTCLOUD_REGION

验证通过后，完全退出并重新打开客户端。
如果你更希望改配置文件，也可以直接打开 `~/.zshrc`：
- `open ~/.zshrc`
- 或 `nano ~/.zshrc`

把变量写进去后执行 `source ~/.zshrc`。

如果你现在不想自己查地域，我也可以基于当前可用凭证先帮你查 PostgreSQL 支持地域，再继续收敛到标准地域码。
`SecretId` / `SecretKey` / `SessionToken` 这类敏感值仍需要你自己在控制台创建并放到运行环境里，不要发到聊天里。
```

## `invalid-region` 模板

### 触发条件
- 用户输入的地域不能被安全归一化
- 用户输入不在公共别名表中
- 地域值不是 PostgreSQL 当前支持的合法售卖地域

### 必须输出的内容
- 回显原始输入值
- 给出合法示例
- 提供官方控制台入口和最短核对步骤
- 提供一个可代查的下一步选项，例如我可以先帮你查支持地域
- 明确要求用户返回标准地域码或可确认的中文地域

### 推荐回复模板

```text
当前提供的地域值无法确认：<用户原始输入>。

请改成腾讯云标准地域码，或提供可以明确映射的中文地域，例如：
- 广州 -> ap-guangzhou
- 上海 -> ap-shanghai
- 成都 -> ap-chengdu
- 北京 -> ap-beijing

你可以直接打开 PostgreSQL 控制台核对：
- 控制台入口：https://console.cloud.tencent.com/postgres
- 最短操作：
  1. 打开后先看右上角的地域选择器
  2. 如果已有实例，在实例列表里直接查看目标实例所属地域
  3. 确认后把标准地域码发给我，例如 `ap-guangzhou`

如果你不想自己对照，我也可以先基于当前凭证帮你查 PostgreSQL 支持地域，并一起把候选值收敛到标准地域码。

确认后，把地域改成标准值再继续，例如：
export TENCENTCLOUD_REGION="ap-guangzhou"
```

## `missing-target-scope` 模板

### 触发条件
- 用户请求巡检/诊断，但没有提供可以定位实例的必要信息：
  - 缺少地域
  - 缺少实例 ID（如 `postgres-xxxxxxxx`）或明确可辨识的实例名称

### 必须输出的内容
- 回显用户当前提供了什么
- 列出缺少的字段（地域 / 实例 ID）
- 给出腾讯云控制台入口链接，指导用户直接复制
- 对可安全代查的字段给出代查选项，例如我可以先帮你列地域或实例
- 给出一个完整的补全示例，方便用户一键回复

### 推荐回复模板

```text
我准备好执行 PG 巡检了，还需要你补充一下目标信息：

当前缺少：<地域 / 实例 ID / 两者都缺>

你可以在腾讯云 PostgreSQL 控制台直接查到并复制这些信息：
- 实例列表控制台：https://console.cloud.tencent.com/postgres
- 最短操作：
  1. 打开控制台并切到目标地域
  2. 在实例列表找到目标实例
  3. 直接复制实例 ID（格式：`postgres-xxxxxxxx`）和所属地域

如果你不想自己翻控制台，我也可以代你查：
- 如果你已经知道地域，我可以先帮你列出该地域下的 PostgreSQL 实例，再一起确认实例 ID
- 如果你连地域也还没确定，我可以先帮你查 PostgreSQL 支持地域，你再选一个继续

确认后，直接像下面这样发给我就行：
ap-guangzhou postgres-abc12345
```

## `missing-sdk` 模板

### 触发条件
- 当前环境未检测到腾讯云官方 SDK
- 且当前执行路径确实希望补齐 SDK，而不是继续使用 TC3 fallback

### 必须输出的内容
- 先说明 SDK 缺失是否会阻断当前执行
- 如果 fallback 可用，要先告诉用户“可以继续”
- 给出可复制安装命令
- 给出 SDK 官方文档链接
- 真正执行安装命令前必须询问用户是否同意

### 推荐回复模板

```text
当前环境未检测到腾讯云官方 SDK。

这个问题不一定会阻断当前 skill：如果当前链路允许，我可以先使用本地 TC3 签名 HTTPS 请求继续执行。
如果你更希望补齐官方 SDK，我也可以帮你执行安装。

可参考腾讯云官方 SDK 文档：
- Python SDK：https://cloud.tencent.com/document/sdk/Python
- 云 API / SDK 总入口：https://cloud.tencent.com/document/api

常用安装命令如下：
- Python: python3 -m pip install -U tencentcloud-sdk-python
- Node.js: npm install tencentcloud-sdk-nodejs

如果你愿意，我可以直接帮你执行对应安装命令。
```

## 使用要求

- 只要命中上述错误之一，就优先使用本模板，而不是临时自由发挥
- 若错误同时涉及“凭证缺失”和“地域�