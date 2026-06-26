---
name: flink-config
description: Flink 配置管理技能，用于设置与校验本地 `volc_flink` 关键配置项（如默认项目、TOS Jar 存储路径等）。不负责 `volc_flink` 的安装/升级（由 `flink-volc` 负责），也不负责登录/退出/登录状态检查/账号切换（由 `flink-auth` 负责，优先 `volc_flink login status`）。Use this skill when the user wants to view or change concrete local `volc_flink` configuration items (default project, TOS jar prefix, etc.). Do NOT use it for CLI install/upgrade (use `flink-volc`) or auth/account (use `flink-auth`). Always trigger only when the request contains a config intent + a concrete config object/action.
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

# Flink 配置管理技能

用于设置与校验 `volc_flink` 的关键配置项，包括默认项目、TOS Jar 存储路径等。

分工边界：
- 工具安装/升级/命令不可用：`flink-volc`
- 登录/退出/登录状态检查/账号切换：`flink-auth`

---

## 通用约定（必读）

本技能的基础约定与只读约定统一收敛在：

- `../../COMMON.md`
- `../../COMMON_READONLY.md`

本技能当前按只读层管理：只修改本地 `volc_flink` 常用配置项（不变更云端任务/资源），例如默认项目、TOS Jar 存储前缀。
为避免误操作，执行会写入配置的命令前仍应向用户明确展示将写入的值并等待确认。

---

## 🎯 核心功能

### 0. 登录状态检测（从 flink-auth 借鉴）
**在执行任何操作前，先检测登录状态！**

如果检测到 `volc_flink` 未安装或不可用，请先转交 `flink-volc` 完成安装/修复。

**检测步骤（首选）**：
```bash
volc_flink login status
```

**兼容性兜底（当 login status 不可用/报错时）**：
1. `volc_flink config show`
2. `volc_flink projects list`

**错误处理**：
- 如果检测到未登录，立即停止后续操作
- 友好提示用户需要先登录
- 引导使用 `flink-auth` 技能

---

### 1. 查看当前配置

使用 `volc_flink config show` 查看当前配置。

**命令格式**：
```bash
volc_flink config show
```

**输出内容包括**：
- 当前登录的区域
- 默认项目（如果已设置）
- TOS Jar 存储路径（如果已设置）

---

### 2. 设置默认项目

使用 `volc_flink config set-default-project` 设置默认项目。

#### 2.1 信息提取与智能选择
从用户提问中提取关键信息：
- **项目名** (project_name)

**如果用户没有明确提供项目名**：
1. 列出所有项目：`volc_flink projects list`
2. 让用户选择项目
3. 然后执行设置默认项目

#### 2.2 执行设置
**命令格式**：
```bash
# 设置默认项目
volc_flink config set-default-project <项目名称>
```

执行前要求：
- 明确目标项目（name / id）
- 展示将要写入的配置项
- 等待用户确认后再执行

#### 2.3 验证设置
设置完成后，验证设置是否成功：
```bash
volc_flink config show
```

#### 2.4 为什么需要设置默认项目
- 设置后，后续操作可以省略 `-p <项目名>` 参数
- 提高操作效率，减少重复输入
- 避免因忘记指定项目而导致的错误

---

### 3. 设置 TOS Jar 存储路径

使用 `volc_flink config set-tos-jar-prefix` 设置 TOS Jar 存储路径。

#### 3.1 信息提取
从用户提问中提取关键信息：
- **TOS 路径** (tos_path)

**TOS 路径格式**：
```
tos://<bucket-name>/<path>
```

**示例**：
```
tos://my-flink-jars/jars/
tos://company-flink-udf/libs/
```

#### 3.2 执行设置
**命令格式**：
```bash
# 设置 TOS Jar 存储路径
volc_flink config set-tos-jar-prefix <TOS路径>
```

执行前要求：
- 展示将要写入的配置项
- 等待用户确认后再执行

#### 3.3 验证设置
设置完成后，验证设置是否成功：
```bash
volc_flink config show
```

#### 3.4 什么时候需要设置
- 当需要上传自定义 JAR 包时
- 当使用 JAR 任务时
- 当需要管理 UDF 库时
- 配合 `flink-dependency` 技能使用时

---

## 工具调用顺序

### 查看配置
1. **检测登录状态** - 确认已登录
2. **查看配置** - `volc_flink config show`
3. **展示配置信息** - 向用户展示当前配置

### 设置默认项目
1. **检测登录状态** - 确认已登录
2. **智能选择项目** - 如果用户没有提供，列出项目供选择
3. **风险确认** - 明确将写入的默认项目
4. **设置默认项目** - `volc_flink config set-default-project <项目名>`
5. **验证设置** - `volc_flink config show`
6. **确认结果** - 向用户确认设置成功

### 设置 TOS Jar 路径
1. **检测登录状态** - 确认已登录
2. **获取 TOS 路径** - 从用户提问中提取或询问用户
3. **验证路径格式** - 确认路径格式正确
4. **风险确认** - 明确将写入的 TOS 前缀
5. **设置 TOS 路径** - `volc_flink config set-tos-jar-prefix <路径>`
6. **验证设置** - `volc_flink config show`
7. **确认结果** - 向用户确认设置成功

---

## 常用 volc_flink config 命令速查

### 配置管理
```bash
# 查看当前配置
volc_flink config show

# 设置默认项目
volc_flink config set-default-project <项目名>

# 设置 TOS Jar 存储路径
volc_flink config set-tos-jar-prefix <TOS路径>
```

---

## 输出格式

### 查看配置反馈
```
# ⚙️ Flink 当前配置

## 📋 配置信息
- **区域**: [区域]
- **默认项目**: [项目名 / 未设置]
- **TOS Jar 路径**: [路径 / 未设置]

## 💡 可用操作
- 设置默认项目
- 设置 TOS Jar 路径
- 查看项目列表
```

### 设置默认项目反馈
```
# ✅ 默认项目设置成功

## 📋 配置变更
- **原默认项目**: [原项目 / 未设置]
- **新默认项目**: [新项目]

## 💡 后续使用
现在可以省略 `-p <项目名>` 参数了！
示例：`volc_flink jobs list` （无需指定项目）
```

### 设置 TOS Jar 路径反馈
```
# ✅ TOS Jar 路径设置成功

## 📋 配置变更
- **原 TOS 路径**: [原路径 / 未设置]
- **新 TOS 路径**: [新路径]

## 💡 使用场景
- 上传自定义 JAR 包
- 管理 UDF 库
- JAR 任务部署
```

---

## 错误处理

### 常见错误及处理

#### 错误 1：未登录
**错误信息**：`❌ 请先登录`

**处理方式**：
- 友好提示："检测到未登录火山引擎账号，请先登录"
- 引导使用 `flink-auth` 技能："请使用 flink-auth 技能完成登录/登录状态检查"
- 停止后续操作

#### 错误 2：项目不存在
**错误信息**：`Project not found`

**处理方式**：
- 提示："未找到指定的项目，请检查项目名是否正确"
- 列出可用项目：`volc_flink projects list`
- 让用户重新选择

#### 错误 3：TOS 路径格式错误
**错误信息**：`Invalid TOS path format`

**处理方式**：
- 提示："TOS 路径格式不正确"
- 说明正确格式：`tos://<bucket-name>/<path>`
- 提供示例：`tos://my-flink-jars/jars/`
- 让用户重新输入

---

## 注意事项

### 重要：默认项目的作用

⚠️ **设置默认项目后**：
- 所有操作都会默认使用该项目
- 可以省略 `-p <项目名>` 参数
- 如果需要操作其他项目，仍需指定 `-p <项目名>`

### 重要：TOS 路径的要求

⚠️ **TOS 路径要求**：
- 必须以 `tos://` 开头
- Bucket 必须存在且有读写权限
- 路径建议以 `/` 结尾
- 确保有足够的存储空间

### 通用注意事项

1. **先检测登录状态**：在执行任何操作前，先检测是否已登录
2. **验证配置变更**：设置完成后，务必验证配置是否生效
3. **提供清晰的反馈**：向用户展示配置变更前后的对比
4. **说明配置的作用**：告诉用户设置后的好处和使用方法
5. **友好的错误处理**：如果操作失败，向用户说明失败原因，并提供解决方案

---

## 🎯 技能总结

### 核心功能
1. ✅ **查看配置** - 查看当前 volc_flink 配置
2. ✅ **设置默认项目** - 设置和管理默认项目
3. ✅ **设置 TOS Jar 路径** - 配置 TOS Jar 存储路径
4. ✅ **智能项目选择** - 交互式项目选择
5. ✅ **配置验证** - 验证配置变更是否成功

### 与其他技能的关系
- **依赖 flink-auth** - 需要先登录才能管理配置
- **依赖 flink-volc** - 需要 `volc_flink` CLI 可用
- **被其他技能依赖** - 其他技能可能需要读取配置信息
- **配合 flink-dependency** - 设置 TOS 路径后可以更好地管理依赖

这个技能是配置管理的核心，让用户可以更高效地使用其他 Flink 技能！
