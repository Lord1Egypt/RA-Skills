# 连接认证流程

## 前置检查

启动陶朱账本技能后，**首先执行以下检查**：

1. **Token**: 在 memory 或配置中查找已保存的 Token
2. **身份标识ID**（仅 API 方式需要）: 在 memory 或配置中查找已保存的 32 位身份标识ID

### Token 有效性验证

如果有已保存的 Token，尝试调用一次 MCP 查询接口（如 `get_platform_list`）验证：
- ✅ 返回成功 → Token 有效，跳过认证流程，直接开始使用
- ❌ 返回认证错误 → Token 已失效，清理失效 Token，进入认证流程

### 无有效 Token

没有 Token 或 Token 失效时，进入认证流程。

---

## 认证流程

### Step 1: 告知用户需要认证

向用户说明需要先完成认证才能使用陶朱账本。

### Step 2: 提供两个选项（**必须等待用户选择**）

向用户展示以下两个选项，等用户明确选择后再执行对应流程。

---

### 选项一：提供 Token（推荐）⭐

用户在陶朱账本微信小程序中自行获取 Token 后提供给 AI。

**优点**:
- ✅ 账户与微信账户打通，可在微信小程序查看账本数据
- ✅ 不需要保存身份标识ID（Token 已包含用户信息）

**用户操作**:
1. 打开陶朱账本微信小程序
2. 找到 Token/设置页面，复制 Token
3. 把 Token 提供给 AI

**AI 操作**:
1. 接收用户提供的 Token
2. 保存 Token 到 memory（持久化）
3. 验证 Token 可用性

---

### 选项二：自动获取 Token

AI 通过 API 自动获取 Token，无需用户提供。

**缺点**:
- ❌ 不支持在微信小程序查看账本
- 账户与本机绑定，更换设备需重新获取

**AI 操作**:
1. **生成身份标识ID**：
   - 通过 `ifconfig` 获取 MAC 地址
   - 对 MAC 地址取 MD5，生成 32 位身份标识ID

2. **保存身份标识ID**：立即保存到 memory（⚠️ 更换会导致历史数据丢失！）

3. **获取 Token**：
   - 构造 code: `身份标识ID + 10位时间戳 + f5138595b7b93cd08b8c03bbaa825ddb`
   - 调用 `POST https://moneydata.cn/api/user/token`，body: `{"code": "<构造的code>"}`
   - 从响应中提取 Token

4. **保存 Token**：将 Token 保存到 memory

---

### Step 3: 保存凭证到 memory

获取到凭证后，根据认证方式分别保存：

**选项一（微信Token）**:
- 只保存 Token 到 memory
- 不需要保存身份标识ID（Token 已包含用户信息）

**选项二（API获取）**:
- 保存身份标识ID 到 memory（生成后立即保存）
- 保存 Token 到 memory
- 后续 Token 过期后，用同一身份标识ID 重新获取即可

保存示例：

**选项一（微信Token）：**
```json
{
  "zhangben_token": "用户提供的Token",
  "auth_method": "wechat"
}
```

**选项二（API获取）：**
```json
{
  "zhangben_identity_id": "32位身份标识ID",
  "zhangben_token": "API获取的Token",
  "auth_method": "api"
}
```

### Step 4: 验证连接

保存凭证后，调用一次 `get_platform_list` 确认连接正常，然后开始处理用户请求。
