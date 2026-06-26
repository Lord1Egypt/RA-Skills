---
name: flink-auth
description: Flink 认证与账号管理技能，用于检查 `volc_flink` 登录状态、登录/退出、账号切换与本地凭证安全口径（不输出明文 AK/SK）。优先使用 `volc_flink login status` 检查登录状态。Use this skill when the user needs auth/account actions for `volc_flink` (login status, login/logout, account switching) with strict secret-handling. Prefer `volc_flink login status` for status checks. Always trigger only when the request contains an auth/account intent + a concrete action/object.
required_binaries:
  - volc_flink
may_access_config_paths:
  - ~/.volc_flink
  - $VOLC_FLINK_CONFIG_DIR
credentials:
  primary: volc_flink_local_config
  optional_env_vars:
    - VOLCENGINE_ACCESS_KEY
    - VOLCENGINE_SECRET_KEY
    - VOLCENGINE_REGION
---

# Flink 认证与多账号管理技能

用于管理登录状态、多账号切换、AK/SK 安全管理等认证相关操作。

---

## 通用约定（必读）

本技能的基础约定与安全约定统一收敛在：

- `../../COMMON.md`
- `../../COMMON_SECURITY.md`

本技能涉及登录、账号切换和本地凭证配置等安全敏感操作，必须遵循 `COMMON_SECURITY.md` 中的秘密输入、脱敏展示和安全输出规则。

---

## 🎯 核心功能

### 0. 当前登录状态检测
**在执行任何操作前，先检测当前登录状态！**

如果检测到 `volc_flink` 未安装或不可用，请先转交给 `flink-volc` 完成安装/修复。

**检测步骤（首选）**：

```bash
volc_flink login status
```

**兼容性兜底（当 login status 不可用/报错时）**：
1. `volc_flink config show`
2. `volc_flink projects list`（能列出项目通常代表已登录且权限正常）

**输出要求**：
- 明确给出：已登录/未登录/无法判断（工具不可用）
- 若未登录：给出下一步（`volc_flink login`），但不要在聊天中索要或回显 AK/SK

---

### 1. 登录管理

#### 1.1 交互式登录
使用 `volc_flink login` 进行交互式登录。

**命令格式**：
```bash
# 交互式登录（推荐）
volc_flink login
```

**交互式登录说明**：
- 交互输入发生在用户本地终端中，不在聊天里传递任何密钥信息
- 登录完成后，请用 `volc_flink login status` 复核

#### 1.2 安全登录说明
出于安全原因，本插件不提供 `--ak/--sk` 的“直接粘贴式命令示例”。

推荐方式：
1. 使用交互式登录：`volc_flink login`
2. 如需非交互式登录，请使用企业内部安全方式（例如密钥管理/环境变量注入），并遵循仓库 `../../COMMON.md` 的安全原则。

**支持的区域**：
- `cn-beijing` - 华北2（北京）
- `cn-shanghai` - 华东2（上海）
- `cn-guangzhou` - 华南1（广州）
- `ap-singapore` - 亚太东南1（新加坡）

#### 1.3 验证登录状态
登录后，验证登录是否成功：
```bash
# 首选：查看登录状态
volc_flink login status

# 兜底：尝试列出项目
volc_flink projects list
```

---

### 2. 退出登录

使用 `volc_flink logout` 退出登录。

**命令格式**：
```bash
volc_flink logout
```

**退出前确认**：
在退出前，向用户确认：
```
⚠️ 确认退出登录？
- 当前登录账号：[账号信息]
- 退出后需要重新登录才能使用 Flink 功能

请确认是否退出？(yes/no)
```

---

### 3. 多账号管理（高级功能）

虽然 volc_flink 原生不支持多账号切换，但可以通过以下方式实现：

#### 3.1 使用不同的配置目录

**为每个账号创建独立的配置目录（推荐，避免复制凭证文件）**：
```bash
# 账号 A 的配置目录
~/.volc_flink/account_a/

# 账号 B 的配置目录
~/.volc_flink/account_b/

# 账号 C 的配置目录
~/.volc_flink/account_c/
```

#### 3.2 账号切换流程

**步骤 1：切换到目标账号（使用环境变量选择配置目录）**
```bash
# 选择账号目录作为配置目录（不会修改/覆盖其他账号的目录内容）
export VOLC_FLINK_CONFIG_DIR=~/.volc_flink/account_<目标账号>

# 如该账号目录尚未登录过，执行一次交互式登录
volc_flink login
```

**步骤 2：验证切换结果**
```bash
# 查看当前配置
volc_flink config show

# 确认登录状态（不回显明文密钥）
volc_flink login status
```

#### 3.3 账号列表管理

**列出所有已配置的账号**：
```bash
ls -la ~/.volc_flink/ | grep account_
```

**账号命名建议**：
- `account_公司_生产` - 公司生产环境账号
- `account_公司_测试` - 公司测试环境账号
- `account_个人` - 个人账号
- `account_<项目名>` - 特定项目账号

---

### 4. AK/SK 安全管理

#### 4.1 安全提示

⚠️ **重要：AK/SK 安全规则**：

1. **不要在聊天中直接粘贴 AK/SK**
   - 建议使用交互式登录
   - 如果必须提供，请使用安全的方式

2. **妥善保管 AK/SK**
   - 不要提交到代码仓库
   - 不要记录在公共文档中
   - 使用密码管理器保存

3. **定期轮换 AK/SK**
   - 建议每 90 天轮换一次
   - 发现泄露立即轮换

4. **使用最小权限原则**
   - 为 AK/SK 分配最小必要权限
   - 不要使用管理员账号进行日常操作

5. **启用访问日志**
   - 监控 AK/SK 的使用情况
   - 发现异常使用立即处理

#### 4.2 获取 AK/SK 的指引

如果用户没有 AK/SK，提供获取指引：

**获取步骤**：
1. 登录火山引擎控制台
2. 进入"访问控制" → "API 密钥管理"
3. 点击"新建密钥"
4. 保存 Access Key 和 Secret Key
5. 妥善保管

**控制台地址**：
https://console.volcengine.com/iam/keymanage

---

## 工具调用顺序

### 查看当前登录状态
1. **检测登录状态** - `volc_flink login status`
2. **展示登录信息** - 向用户展示当前登录的账号和区域

### 登录新账号
1. **确认操作** - 询问用户是否要登录新账号
2. **保存当前配置**（如果已有账号）- 备份当前配置
3. **执行登录** - `volc_flink login`（交互式或使用 AK/SK）
4. **验证登录** - `volc_flink login status`
5. **保存新账号配置** - 保存到账号目录
6. **确认结果** - 向用户确认登录成功

### 切换账号
1. **列出可用账号** - 列出所有已配置的账号
2. **用户选择目标账号** - 让用户选择要切换到的账号
3. **保存当前配置** - 备份当前账号配置
4. **切换到目标账号** - 复制目标账号配置到当前配置
5. **验证切换结果** - `volc_flink login status`
6. **确认结果** - 向用户确认切换成功

### 退出登录
1. **确认退出** - 向用户确认是否退出
2. **保存当前配置**（可选）- 备份当前配置
3. **执行退出** - `volc_flink logout`
4. **确认结果** - 向用户确认退出成功

---

## 常用命令速查

### 登录与认证
```bash
# 查看登录状态
volc_flink login status

# 交互式登录
volc_flink login

# 退出登录
volc_flink logout

# 查看当前配置
volc_flink config show
```

### 配置目录管理
```bash
# 列出所有账号配置
ls -la ~/.volc_flink/ | grep account_

# 切换到指定账号（推荐：通过环境变量选择配置目录，不做复制覆盖）
export VOLC_FLINK_CONFIG_DIR=~/.volc_flink/account_<账号名>
volc_flink login status
```

---

## 输出格式

### 当前登录状态反馈
```
# 🔐 当前登录状态

## 📋 登录信息
- **状态**: [已登录 / 未登录]
- **区域**: [区域]
- **检查时间**: [时间]

## 💡 可用操作
- 登录新账号
- 切换账号（如有多个配置）
- 退出登录
```

### 登录成功反馈
```
# ✅ 登录成功

## 📋 账号信息
- **区域**: [区域]
- **登录时间**: [时间]
- **配置已保存到**: [账号目录]

## 💡 后续操作
1. 查看项目: `flink-projects`
2. 设置默认项目: `flink-config`
3. 开始使用其他 Flink 技能
```

### 账号切换反馈
```
# 🔄 账号切换成功

## 📋 切换信息
- **原账号**: [原账号名]
- **新账号**: [新账号名]
- **区域**: [新区域]
- **切换时间**: [时间]

## ✅ 验证结果
- **配置已加载**
- **登录状态**: 已登录

## 💡 后续操作
1. 查看新项目: `flink-projects`
2. 设置默认项目: `flink-config`
```

---

## 错误处理

### 常见错误及处理

#### 错误 1：登录失败
**错误信息**：`Invalid AccessKey or SecretKey`

**处理方式**：
- 提示："登录失败，请检查 AccessKey 和 SecretKey 是否正确"
- 建议重新登录：`volc_flink login`
- 提供获取 AK/SK 的指引

#### 错误 2：配置目录不存在
**错误信息**：目标账号配置目录不存在

**处理方式**：
- 提示："未找到目标账号的配置"
- 列出可用的账号配置
- 引导用户先登录并保存配置

#### 错误 3：权限不足
**错误信息**：AK/SK 权限不足

**处理方式**：
- 提示："当前 AK/SK 权限不足"
- 建议检查 AK/SK 的权限配置
- 建议使用有足够权限的 AK/SK

---

## 注意事项

### 重要：安全第一

⚠️ **关于 AK/SK 的安全**：
1. **绝对不要在聊天中直接粘贴完整的 AK/SK**
2. **建议使用交互式登录** - 更安全
3. **妥善保管 AK/SK** - 不要泄露给他人
4. **定期轮换 AK/SK** - 提高安全性
5. **使用最小权限原则** - 为 AK/SK 分配最小必要权限

### 重要：配置备份

⚠️ **切换账号前务必备份**：
- 总是先备份当前配置
- 使用时间戳命名备份目录
- 保留最近几个备份

### 通用注意事项

1. **先检测登录状态**：在执行任何操作前，先检测当前登录状态
2. **安全提示**：每次涉及 AK/SK 时都要提醒安全注意事项
3. **配置备份**：切换账号前务必备份当前配置
4. **友好的错误处理**：如果操作失败，向用户说明失败原因，并提供解决方案
5. **提供清晰指引**：为用户提供清晰的操作指引和后续建议

---

## 🎯 技能总结

### 核心功能
1. ✅ **登录状态检测** - 查看当前登录状态
2. ✅ **登录管理** - 交互式登录、AK/SK 登录
3. ✅ **退出登录** - 安全退出登录
4. ✅ **多账号切换** - 通过配置目录实现多账号管理
5. ✅ **AK/SK 安全管理** - 安全提示和最佳实践
6. ✅ **配置备份** - 自动备份和恢复配置

### 与其他技能的关系
- **基础技能** - 其他所有技能都依赖认证状态
- **配合 flink-volc** - 可以配合使用进行工具安装和基础登录
- **被其他技能依赖** - 其他技能在操作前会检查登录状态

这个技能是认证管理的核心，让用户可以安全、方便地管理多个账号！
