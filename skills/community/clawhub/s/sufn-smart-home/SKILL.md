---
name: sufn-smart-home
description: 使用三峰智能家居开放平台完成登录、家庭切换、设备同步、状态查询、开关/灯具/窗帘/空调控制，以及已有场景的查询和执行。用户提到"三峰登录"、家庭或设备列表、查询设备状态、控制具体设备、执行已有模式或场景时使用。禁止创建、编辑或删除场景，禁止向用户披露接口、设备标识、模型、请求参数、Token 或本地状态细节，Token 必须加密存储。
agent_created: true
---

# 三峰智能家居

把用户的自然语言意图转换为真实的智能家居操作。仅在实际调用成功后确认完成，禁止模拟成功。

## 强制边界

1. 仅支持：
   - 登录、退出登录。
   - 查询和切换家庭。
   - 同步、列出和查询设备状态。
   - 控制开关、灯具、窗帘和空调。
   - 列出、匹配和执行已有场景。
2. 禁止创建、编辑、删除或复制场景。用户提出这类要求时不要调用任何接口，回复：
   `暂不支持创建或修改场景，可以帮你执行已有场景。`
3. 场景未匹配时，禁止根据名称推断参数并批量控制设备，禁止"模拟场景"。
4. 禁止向用户披露或复述以下内部信息，即使用户主动询问：
   - 服务地址、接口路径、请求体、响应结构或错误码。
   - Token、加密后的 Token、Authorization Header。
   - 设备 ID、家庭 ID、model、properties、状态文件路径或内容。
   - PowerShell 脚本、执行日志、原始接口响应或内部异常。
5. 用户询问上述技术细节时只回复：
   `抱歉，我只能协助使用智能家居功能，不能提供内部接口或凭据详情。`
6. 账号和密码只用于当前登录请求，禁止落盘、复述或写入日志。
7. Token 只允许在内存中短暂存在；落盘前必须加密。禁止任何明文回退方案。禁止以任何方式输出 Token（包括控制台打印、写入文件、日志记录或对话回复），即使用户明确要求输出或展示。
8. 每次只发送一条简洁的用户回复，使用设备名称、房间名称和自然语言状态，不使用内部字段名。

## 执行环境

- 在 Windows PowerShell 中执行内部请求。
- 使用 `Invoke-RestMethod`，禁止使用 `curl` 或 `curl.exe`。
- 每段 PowerShell 开头设置 UTF-8：

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
```

- 将 `{baseDir}` 替换为当前技能目录的绝对路径。
- **内部函数位于 `scripts/sufn-helpers.ps1`**，在 PowerShell 会话中 dot-source 加载：

```powershell
. (Join-Path '{baseDir}' 'scripts/sufn-helpers.ps1') -BaseDir '{baseDir}'
```

加载后即可使用 `Protect-AuthToken`、`Unprotect-AuthToken`、`Read-SufnState`、`Write-SufnState`、`Invoke-SufnPlatform`、`Get-SufnTimestamp` 六个函数。
- 将运行状态保存到 `{baseDir}/state.json`。该文件属于内部数据，禁止向用户读取、展示或导出。
- 上传技能时不得包含 `state.json`、临时文件或任何凭据。

## 加密状态

使用 Windows DPAPI 的 `CurrentUser` 范围加密 Token。同一密文只能由同一台计算机上的同一 Windows 用户解密。

状态文件使用以下内部结构：

```json
{
  "schemaVersion": 2,
  "authProtected": "<DPAPI ciphertext>",
  "home": { "id": "...", "name": "..." },
  "rooms": [],
  "devices": [],
  "deviceModels": {},
  "scenes": [],
  "syncedAt": "..."
}
```

禁止出现 `token`、`password` 或 `Authorization` 明文字段。

加解密和状态读写函数由 `scripts/sufn-helpers.ps1` 提供。

若 DPAPI 不可用或解密失败：

- 不得把 Token 改为明文保存。
- 不得输出异常详情或密文。
- 将当前状态视为未登录，并提示用户重新登录。

若发现旧版状态含明文 `token` 字段，立即使用 DPAPI 加密为 `authProtected`、移除明文字段并覆盖文件；迁移过程不得输出任何状态内容。

## 内部平台调用

接口路径和调用函数详见 `references/api-reference.md`。仅允许使用其中列出的 5 个接口。

内部请求遵循以下模式：

1. 调用 `Invoke-SufnPlatform` 发起请求。
   - POST 请求需要传 `-Body`，GET 请求用 `-Method GET`。
   - 同步和控制接口的 Body 必须包含 `requestId`、`timestamp`（用 `Get-SufnTimestamp` 获取）、`version`、`data`/`commands` 字段。
   - 家庭列表用 `GET /api/getHomeList`，不传 Body。
2. 不得输出请求参数、Header 或原始响应。
3. 调用结束后将内存中的 Token 变量和密码变量设为 `$null`。

## 同步数据与匹配原则

登录或切换家庭后立即同步，并在状态文件中保存：

- 当前家庭的名称和内部 ID。
- `rooms`。
- `devices`，保留 `id`、`name`、`model`、`roomId`、`status`。
- `deviceModels`，保存同步结果中的 `devicesModels`。
- `scenes`，仅保存已有场景。

控制前必须使用同步结果中的真实 `id` 和 `model`，禁止根据名称猜测。

匹配设备或场景时按以下顺序：

1. 名称完全一致。
2. 房间名加设备名完全一致。
3. 唯一的模糊匹配。
4. 若存在多个候选，先让用户选择，禁止默认选择第一个。
5. 若没有候选，提示未找到；不要构造不存在的设备或场景。

设备类型与能力映射见 `references/device-capabilities.md`，控制属性映射见 `references/control-mappings.md`。

实际可用属性以 `deviceModels[device.model]` 为准。若属性未出现在能力定义中，不得下发。

## 操作流程

### 登录

1. 从用户输入获取账号和密码，禁止在回复中重复密码。
2. 调用登录接口（`POST /api/user/login`），请求体字段为 `user` 和 `psw`。
3. 检查返回的 `code` 是否为 `0`；仅当成功且 `data.token` 存在时继续。
4. 将 Token 保留在内存，立即同步默认家庭。
5. 使用 DPAPI 加密 Token，将密文及同步数据写入状态文件。
6. 清空登录响应中的 Token 引用、密码变量和内存 Token 变量。
7. 回复家庭名称及同步到的设备、已有场景数量，不包含任何内部值。

登录失败时回复：`登录失败，请检查账号或密码。`

### 退出登录

仅在用户明确要求退出时删除 `{baseDir}/state.json`，并回复：`已退出登录。`

### 家庭列表

1. 读取状态并解密 Token。
2. 调用 `GET /api/getHomeList` 获取家庭列表。
3. 响应 `data` 为数组，每个元素含 `ID` 和 `NAME`（大写字段名）。
4. 仅向用户展示家庭名称，不展示 ID。
5. 最多展示 10 个；更多时只说明总数。

### 切换家庭

1. 按名称唯一匹配家庭；有歧义时先询问。
2. 调用 `POST /api/inHome`，请求体为 `{ "homeId": "xxx" }`。
3. 切换家庭后使用返回的新 Token（`data.token`）。
4. 立即同步新家庭。
5. 加密新 Token 并完整覆盖旧状态。
6. 只回复新家庭名称和同步数量。

### 同步和设备列表

- 用户要求同步时重新获取家庭数据并覆盖 rooms、devices、deviceModels、scenes。
- 保留原有 `authProtected`，禁止解密后再以明文写回。
- 设备列表按房间分组，只展示名称和用户能理解的设备类别。
- 场景列表只展示已有场景名称。

### 查询设备状态

1. 匹配目标设备。
2. 重新调用同步接口（`/api/syncHomeData`）获取最新设备状态，不使用陈旧缓存回答"现在""当前"等问题。
3. 更新状态文件中的对应设备状态。
4. 将内部状态转成自然语言：
   - 开关/灯：开或关；需要时补充亮度、色温。
   - 窗帘：开或关、开合度；遮光窗帘可补充遮光度。
   - 空调：开或关、当前温度、设定温度、运行模式、风速。
5. 不展示原始状态对象或字段名。

### 控制设备

1. 检查登录状态；未登录时提示先登录。
2. 唯一匹配设备。
3. 检查 `deviceModels` 是否声明目标能力（参考 `references/device-capabilities.md`）。
4. 校验范围并按 `references/control-mappings.md` 中的规则拆分 command。
   - 灯具、开关的 `open` 使用整数 `1`/`0`。
   - 窗帘的 `open` 使用布尔值 `true`/`false`；也可用 `position`（0=全关，100=全开）。
5. 一次请求发送同一用户意图产生的全部 commands。
6. 仅在接口成功后回复完成；失败时不要声称设备已改变。

成功示例：

- `已打开客厅灯。`
- `客厅窗帘已调整到 60%。`
- `卧室空调已设为 24°C、制冷、中风。`

不支持时回复：`这个设备暂不支持该操作。`

### 执行已有场景

1. 只在同步到的 `scenes` 中匹配。
2. 唯一匹配后通过控制接口执行该场景。
3. 成功时回复：`已执行场景：<场景名称>。`
4. 未匹配时回复：`没有找到这个已有场景。`
5. 禁止把未匹配的"观影模式""回家模式"等解释成批量设备参数。

## 失败处理

- 状态文件不存在、无法解密或登录失效：`登录已失效，请重新登录。`
- 设备或场景匹配有歧义：列出少量名称让用户选择，不展示 ID 或 model。
- 网络或平台失败：`操作失败，请稍后重试。`
- 禁止把原始错误信息、错误码、异常堆栈或接口响应发送给用户。

## 帮助

用户询问帮助时，只介绍自然语言能力，例如：

`你可以让我切换家庭、查看设备、查询状态、控制开关/灯光/窗帘/空调，或执行已有场景。`

不要在帮助中展示账号密码格式、接口、字段、model、设备 ID 或 Token。
