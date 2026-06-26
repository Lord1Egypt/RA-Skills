---
name: flink-dependency
description: Flink 依赖管理技能，用于管理 Flink 任务的 JAR 包依赖和 UDF 库，包括 TOS 文件管理、添加依赖、删除依赖、查看依赖列表等。Use this skill when the user wants to add/remove/list concrete dependency jars, manage UDF libraries, or operate on TOS-backed dependency files for a specific draft or job. Always trigger only when the request contains a dependency/file-management intent + a concrete object/action.
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

# Flink 依赖管理技能

基于 `volc_flink` 命令行工具，管理 Flink 任务的 JAR 包依赖和 UDF 库，包括添加依赖、删除依赖、查看依赖列表等。

---

## 通用约定（必读）

本技能的基础约定与变更约定统一收敛在：

- `../../COMMON.md`
- `../../COMMON_MUTATION.md`

本技能涉及依赖增删、TOS 文件上传与草稿依赖变更，必须遵循 `COMMON_MUTATION.md` 中的 Risk Confirmation、变更前检查和操作后验证规则。

---

## 🎯 核心流程

### 0. 登录状态检测（从其他 flink 技能借鉴）
**在执行任何操作前，先检测登录状态！**

**检测步骤**：
1. 尝试执行一个简单的命令（如 `volc_flink config show`）
2. 如果提示"请先登录"，则提示用户需要登录
3. 提供登录指引：请使用交互式登录 `volc_flink login`（或企业内部安全方式），不要在对话/命令行参数中粘贴 AK/SK，详见 `../../COMMON.md`

**错误处理**：
- 如果检测到未登录，立即停止后续操作
- 友好提示用户需要先登录

---

### 1. 信息提取与智能选择（从其他 flink 技能借鉴）

#### 1.1 信息提取
从用户提问中提取关键信息：
- **Flink 项目名** (project_name)
- **草稿名/草稿 ID** (draft_name/draft_id)
- **操作类型**：添加依赖、删除依赖、查看依赖
- **JAR 包路径**：本地路径或 tos://... 路径
- **JAR 包描述**：UDF 库、自定义函数等

如果用户没有明确提供，主动询问缺失的关键信息。

#### 1.2 智能项目和草稿选择
**如果用户没有明确提供项目名或草稿名，按以下流程处理**：

**场景 A：用户只提供了草稿名，没有提供项目名**
1. 列出所有项目：`volc_flink projects list`
2. 列出草稿目录：`volc_flink drafts dirs`
3. 列出草稿列表：`volc_flink drafts apps`
4. 展示所有匹配的草稿供用户选择

**场景 B：用户没有提供任何信息**
1. 先列出所有项目供用户选择
2. 用户选择项目后，列出该项目下的草稿目录供用户选择
3. 列出草稿列表供用户选择
4. 用户选择草稿后，询问操作类型

**场景 C：用户提供的项目名或草稿名不明确**
1. 列出所有草稿供用户选择
2. 或者提供搜索功能

---

### 2. 操作类型与流程

#### 2.0 TOS 文件管理（TOS File Management）【新增】

**使用场景**：
- 上传 JAR 包到 TOS
- 查看已上传的文件列表
- 获取文件详情
- 更新文件
- 获取文件下载链接

**前置条件检查**：
在进行 TOS 文件操作前，检查是否已配置 TOS Jar 存储路径：

**检查步骤**：
1. 查看当前配置：`volc_flink config show`
2. 如果未配置 TOS Jar 路径，提示用户配置
3. 引导使用 `flink-config` 技能进行配置

---

##### 2.0.1 列出 TOS 文件（List TOS Files）

**使用场景**：
- 查看已上传到 TOS 的所有文件
- 确认文件是否已上传
- 查看文件列表和信息

**操作步骤**：
1. **检查 TOS 配置** - 确认已配置 TOS Jar 路径
   ```bash
   volc_flink config show
   ```

2. **列出文件**
   ```bash
   # 列出所有文件
   volc_flink files list

   # 列出指定前缀的文件
   volc_flink files list --prefix <子目录前缀>

   # 限制返回数量
   volc_flink files list --limit <数量>

   # 输出原始 JSON
   volc_flink files list --raw
   ```

3. **展示文件信息**，包括：
   - 文件名
   - 文件大小
   - 最后修改时间
   - 文件类型

---

##### 2.0.2 上传文件到 TOS（Upload File to TOS）

**使用场景**：
- 上传 JAR 包到 TOS
- 上传 UDF 库
- 上传依赖文件

**操作步骤**：
1. **检查 TOS 配置** - 确认已配置 TOS Jar 路径
   ```bash
   volc_flink config show
   ```

2. **确认文件信息**
   - 本地文件路径
   - 对象名（可选，默认使用文件名）

3. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
   - ⚠️ 上传文件会占用 TOS 存储空间
   - ⚠️ 确认文件路径正确
   - ⚠️ 确认文件内容正确

4. **上传文件**
   ```bash
   # 上传文件（使用默认文件名）
   volc_flink files upload --file <本地文件路径>

   # 上传文件并指定对象名
   volc_flink files upload --file <本地文件路径> --name <对象名>
   ```

5. **验证上传** - 列出文件确认上传成功
   ```bash
   volc_flink files list
   ```

---

##### 2.0.3 查看文件详情（View File Detail）

**使用场景**：
- 查看已上传文件的详细信息
- 确认文件大小和属性
- 获取文件元数据

**操作步骤**：
1. **列出文件** - 让用户选择要查看的文件
   ```bash
   volc_flink files list
   ```

2. **查看文件详情**
   ```bash
   volc_flink files detail --name <对象名>
   ```

3. **展示文件详情**，包括：
   - 文件名
   - 文件大小
   - 最后修改时间
   - ETag
   - 其他元数据

---

##### 2.0.4 更新文件（Update File）

**使用场景**：
- 更新已上传的文件
- 覆盖旧版本的文件
- 替换 JAR 包

**操作步骤**：
1. **列出文件** - 让用户选择要更新的文件
   ```bash
   volc_flink files list
   ```

2. **确认文件信息**
   - 要更新的对象名
   - 新的本地文件路径

3. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
   - ⚠️ 更新会覆盖原有文件
   - ⚠️ 确认新文件内容正确
   - ⚠️ 确认对象名正确

4. **更新文件**
   ```bash
   volc_flink files update --name <对象名> --file <本地文件路径>
   ```

5. **验证更新** - 查看文件详情确认更新成功
   ```bash
   volc_flink files detail --name <对象名>
   ```

---

##### 2.0.5 获取文件下载链接（Get File Download URL）

**使用场景**：
- 获取文件的预签名下载链接
- 分享文件给他人
- 下载文件到本地

**操作步骤**：
1. **列出文件** - 让用户选择要获取链接的文件
   ```bash
   volc_flink files list
   ```

2. **获取下载链接**
   ```bash
   # 获取默认有效期（3600秒）的链接
   volc_flink files url --name <对象名>

   # 获取指定有效期的链接
   volc_flink files url --name <对象名> --expires <有效期秒数>
   ```

3. **展示下载链接**，包括：
   - 预签名 URL
   - 有效期
   - 使用说明

---

#### 2.1 查看依赖列表（List Dependencies）

**使用场景**：
- 查看当前草稿已添加的依赖
- 确认依赖是否已添加
- 检查依赖版本

**操作步骤**：
1. **获取草稿内容** - 查看当前依赖列表
   ```bash
   volc_flink drafts content -i <草稿ID>
   ```

2. **展示依赖信息**，包括：
   - JAR 包名称
   - JAR 包路径
   - 添加时间
   - JAR 包大小（如果有）

---

#### 2.2 添加依赖（Add Dependency）

**使用场景**：
- 添加自定义 UDF 库
- 添加第三方依赖 JAR
- 添加自定义 Connector

**操作步骤**：
1. **获取草稿信息** - 确认草稿 ID
   ```bash
   volc_flink drafts apps
   ```

2. **确认 JAR 包信息**
   - 本地路径：`/path/to/your.jar`
   - TOS 路径：`tos://bucket/path/to/your.jar`

3. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
   - ⚠️ 添加依赖后需要重新发布草稿
   - ⚠️ 任务需要重启才能生效
   - ⚠️ 确认 JAR 包路径正确
   - ⚠️ 确认 JAR 包兼容性

4. **添加依赖**
   ```bash
   # 添加单个 JAR
   volc_flink drafts dependency add -i <草稿ID> --jar <JAR路径>

   # 添加多个 JAR
   volc_flink drafts dependency add -i <草稿ID> --jar <JAR路径1> --jar <JAR路径2>
   ```

5. **验证依赖** - 查看草稿内容确认添加成功
   ```bash
   volc_flink drafts content -i <草稿ID>
   ```

6. **发布草稿**（可选，如果需要立即生效）
   ```bash
   volc_flink drafts publish -i <草稿ID>
   ```

---

#### 2.3 删除依赖（Remove Dependency）

**使用场景**：
- 移除不再需要的依赖
- 更新依赖版本（先删后加）
- 清理冲突的依赖

**操作步骤**：
1. **查看当前依赖列表** - 让用户选择要删除的依赖
   ```bash
   volc_flink drafts content -i <草稿ID>
   ```

2. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
   - ⚠️ 删除后无法恢复
   - ⚠️ 删除后需要重新发布草稿
   - ⚠️ 任务需要重启才能生效
   - ⚠️ 确认 JAR 包路径正确
   - ⚠️ 确认不会影响任务运行

3. **删除依赖**
   ```bash
   # 删除单个 JAR
   volc_flink drafts dependency remove -i <草稿ID> --jar <JAR的tos全路径>

   # 删除多个 JAR
   volc_flink drafts dependency remove -i <草稿ID> --jar <JAR路径1> --jar <JAR路径2>
   ```

4. **验证删除** - 查看草稿内容确认删除成功
   ```bash
   volc_flink drafts content -i <草稿ID>
   ```

5. **发布草稿**（可选，如果需要立即生效）
   ```bash
   volc_flink drafts publish -i <草稿ID>
   ```

---

## 依赖管理最佳实践

### 添加依赖注意事项
- **先测试再生产**：建议先在测试环境验证依赖
- **版本兼容性**：确认依赖与 Flink 版本兼容
- **依赖冲突**：检查是否有依赖冲突
- **大小限制**：注意 JAR 包大小限制
- **依赖数量**：避免添加过多不必要的依赖

### 删除依赖注意事项
- **确认不再使用**：删除前确认没有代码在使用该依赖
- **备份配置**：删除前备份当前配置
- **逐步清理**：不要一次性删除太多依赖
- **验证影响**：删除后验证任务仍然正常运行

### UDF 库管理
- **命名规范**：UDF 库使用清晰的命名
- **版本管理**：UDF 库包含版本信息
- **文档说明**：为 UDF 库提供使用文档
- **测试覆盖**：为 UDF 库提供测试用例

---

## 风险提示模板

注意：以下为风险要点汇总。执行任何会影响草稿/任务的变更（发布、重启、依赖变更等）前，必须使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认。

### 添加依赖风险
- 添加依赖后需要重新发布草稿
- 任务需要重启才能生效
- 可能存在依赖冲突
- 需要验证 JAR 包兼容性
- 建议先在测试环境验证

### 删除依赖风险
- 删除后无法恢复
- 删除后需要重新发布草稿
- 任务需要重启才能生效
- 可能影响任务运行
- 确认 JAR 包不再被使用

---

## 输出格式

### TOS 文件列表反馈

```
# 📁 TOS 文件列表

## 📋 查询信息
- **TOS 路径**: [TOS Jar Prefix]
- **查询时间**: [时间]

## 📁 文件列表

| 序号 | 文件名 | 大小 | 最后修改时间 |
|------|--------|------|-------------|
| 1 | [文件名] | [大小] | [时间] |
| 2 | [文件名] | [大小] | [时间] |

## 💡 操作建议
[给出后续操作建议]
```

### 上传文件反馈

```
# ✅ 文件上传成功

## 📋 操作信息
- **操作类型**: 上传文件到 TOS
- **本地文件**: [本地文件路径]
- **TOS 对象名**: [对象名]
- **执行时间**: [时间]

## 📦 上传结果
- **状态**: ✅ 上传成功
- **文件大小**: [大小]

## 💡 后续建议
1. 查看文件列表确认上传成功
2. 可以将此文件添加到草稿依赖
3. 查看文件详情：`volc_flink files detail --name <对象名>`
```

### 查看文件详情反馈

```
# 📄 TOS 文件详情

## 📋 文件信息
- **对象名**: [对象名]
- **查询时间**: [时间]

## 📊 文件详情
- **文件大小**: [大小]
- **最后修改时间**: [时间]
- **ETag**: [ETag]
- **其他元数据**: [元数据]

## 💡 后续建议
1. 获取下载链接：`volc_flink files url --name <对象名>`
2. 更新文件：`volc_flink files update --name <对象名> --file <新文件>`
3. 可以将此文件添加到草稿依赖
```

### 获取下载链接反馈

```
# 🔗 TOS 文件下载链接

## 📋 文件信息
- **对象名**: [对象名]
- **生成时间**: [时间]

## 🔗 下载链接
```
[预签名 URL]
```

## ⏰ 有效期
- **有效期**: [有效期] 秒
- **到期时间**: [到期时间]

## 💡 使用说明
- 此链接为预签名 URL，可直接用于下载
- 请在有效期内使用
- 链接过期后需要重新生成
```

### 依赖列表反馈

```
# 📦 Flink 依赖列表

## 📋 草稿信息
- **项目名**: [项目名]
- **草稿名**: [草稿名]
- **草稿 ID**: [草稿 ID]
- **查询时间**: [时间]

## 📦 当前依赖

| 序号 | JAR 包名称 | 路径 | 添加时间 |
|------|-----------|------|---------|
| 1 | [名称] | [路径] | [时间] |
| 2 | [名称] | [路径] | [时间] |

## 💡 操作建议
[给出后续操作建议]
```

### 添加依赖反馈

```
# ✅ Flink 依赖添加成功

## 📋 操作信息
- **操作类型**: 添加依赖
- **项目名**: [项目名]
- **草稿名**: [草稿名]
- **草稿 ID**: [草稿 ID]
- **执行时间**: [时间]

## 📦 添加的依赖
- **JAR 包**: [JAR 包路径]
- **状态**: ✅ 添加成功

## 💡 后续建议
1. 查看草稿内容确认依赖已添加
2. 如需立即生效，请发布草稿
3. 发布后需要重启任务
```

### 删除依赖反馈

```
# ✅ Flink 依赖删除成功

## 📋 操作信息
- **操作类型**: 删除依赖
- **项目名**: [项目名]
- **草稿名**: [草稿名]
- **草稿 ID**: [草稿 ID]
- **执行时间**: [时间]

## 📦 删除的依赖
- **JAR 包**: [JAR 包路径]
- **状态**: ✅ 删除成功

## 💡 后续建议
1. 查看草稿内容确认依赖已删除
2. 如需立即生效，请发布草稿
3. 发布后需要重启任务
4. 验证任务仍然正常运行
```

---

## 常用 volc_flink 依赖管理命令速查

### TOS 文件管理【新增】
```bash
# 列出 TOS 文件
volc_flink files list

# 列出指定前缀的文件
volc_flink files list --prefix <子目录前缀>

# 限制返回数量
volc_flink files list --limit <数量>

# 输出原始 JSON
volc_flink files list --raw

# 上传文件到 TOS
volc_flink files upload --file <本地文件路径>

# 上传文件并指定对象名
volc_flink files upload --file <本地文件路径> --name <对象名>

# 查看文件详情
volc_flink files detail --name <对象名>

# 更新文件（覆盖上传）
volc_flink files update --name <对象名> --file <本地文件路径>

# 获取文件下载链接（默认有效期 3600 秒）
volc_flink files url --name <对象名>

# 获取指定有效期的下载链接
volc_flink files url --name <对象名> --expires <有效期秒数>
```

### 草稿管理
```bash
# 列举草稿目录
volc_flink drafts dirs

# 列举草稿
volc_flink drafts apps

# 获取草稿内容
volc_flink drafts content -i <草稿ID>
```

### 依赖管理
```bash
# 添加依赖 JAR
volc_flink drafts dependency add -i <草稿ID> --jar <JAR路径>

# 添加多个依赖 JAR
volc_flink drafts dependency add -i <草稿ID> --jar <JAR路径1> --jar <JAR路径2>

# 删除依赖 JAR
volc_flink drafts dependency remove -i <草稿ID> --jar <JAR的tos全路径>

# 删除多个依赖 JAR
volc_flink drafts dependency remove -i <草稿ID> --jar <JAR路径1> --jar <JAR路径2>
```

### 项目管理
```bash
# 列举项目
volc_flink projects list

# 查看项目详情
volc_flink projects detail <项目名>
```

### 配置管理
```bash
# 查看当前配置
volc_flink config show

# 设置 TOS Jar 存储路径
volc_flink config set-tos-jar-prefix <TOS路径>
```

---

## 注意事项

### 重要：依赖管理的特殊要求

⚠️ **依赖管理时必须遵守以下规则**：

1. **先确认草稿范围** - 明确是哪个草稿的依赖操作
2. **先查看当前依赖** - 添加或删除前，先查看当前依赖列表
3. **风险确认** - 执行任何依赖操作前，必须使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
4. **验证操作结果** - 操作完成后，验证结果是否成功
5. **JAR 包路径注意**：
   - 添加时：可以是本地路径或 tos:// 路径
   - 删除时：必须是 tos:// 全路径

### 通用注意事项

1. **先检测登录状态**：在执行任何操作前，先检测是否已登录
2. **先确认草稿范围**：在执行任何操作前，明确确认是哪个草稿
3. **先查看当前依赖**：添加或删除前，先查看当前依赖列表
4. **始终先确认风险**：在执行任何变更操作前，必须使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
5. **先获取草稿信息**：在执行操作前，先获取草稿的详细信息
6. **验证操作结果**：操作执行完成后，必须验证结果
7. **提供清晰的反馈**：向用户提供清晰的操作结果和后续建议
8. **使用友好的语言**：用用户能理解的语言解释操作和风险
9. **避免过度技术化**：除非用户要求，否则避免过度技术化的解释
10. **友好的错误处理**：如果操作失败，向用户说明失败原因，并提供解决方案

---

## 错误处理优化

### 常见错误及处理

#### 错误 1：未登录
**错误信息**：`❌ 请先登录`

**处理方式**：
- 友好提示："检测到未登录火山引擎账号，请先登录"
- 提供登录指引：请使用交互式登录 `volc_flink login`（或企业内部安全方式），详见 `../../COMMON.md`
- 停止后续操作，等待用户登录后重试

#### 错误 2：草稿不存在
**错误信息**：草稿 ID 不存在

**处理方式**：
- 提示："未找到草稿，请检查草稿名或草稿 ID 是否正确"
- 提供帮助：列出该项目下的所有草稿供用户选择

#### 错误 3：JAR 包路径错误
**错误信息**：JAR 包路径不存在或格式错误

**处理方式**：
- 提示："JAR 包路径错误，请检查路径是否正确"
- 提供帮助：说明正确的路径格式
- 添加时：支持本地路径或 tos:// 路径
- 删除时：需要 tos:// 全路径

#### 错误 4：依赖添加失败
**错误信息**：依赖添加失败

**处理方式**：
- 立即通知用户添加失败
- 建议检查 JAR 包是否存在
- 建议检查 JAR 包大小是否超限
- 建议检查网络连接

#### 错误 5：依赖删除失败
**错误信息**：依赖删除失败

**处理方式**：
- 立即通知用户删除失败
- 建议检查 JAR 包路径是否正确
- 建议确认使用的是 tos:// 全路径
- 建议查看当前依赖列表确认

---

## 工具调用顺序（优化版）

### 列出 TOS 文件
1. **检测登录状态** - 确认已登录
2. **检查 TOS 配置** - 确认已配置 TOS Jar 路径
3. **列出文件** - `volc_flink files list`
4. **展示文件列表** - 向用户展示所有文件

### 上传文件到 TOS
1. **检测登录状态** - 确认已登录
2. **检查 TOS 配置** - 确认已配置 TOS Jar 路径
3. **确认文件信息** - 确认本地文件路径和对象名
4. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
5. **上传文件** - `volc_flink files upload --file <本地文件路径>`
6. **验证结果** - `volc_flink files list` 确认上传成功

### 查看文件详情
1. **检测登录状态** - 确认已登录
2. **检查 TOS 配置** - 确认已配置 TOS Jar 路径
3. **列出文件** - `volc_flink files list` 供用户选择
4. **查看文件详情** - `volc_flink files detail --name <对象名>`
5. **展示文件详情** - 向用户展示文件信息

### 更新文件
1. **检测登录状态** - 确认已登录
2. **检查 TOS 配置** - 确认已配置 TOS Jar 路径
3. **列出文件** - `volc_flink files list` 供用户选择
4. **确认文件信息** - 确认对象名和新文件路径
5. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
6. **更新文件** - `volc_flink files update --name <对象名> --file <本地文件路径>`
7. **验证结果** - `volc_flink files detail --name <对象名>` 确认更新成功

### 获取下载链接
1. **检测登录状态** - 确认已登录
2. **检查 TOS 配置** - 确认已配置 TOS Jar 路径
3. **列出文件** - `volc_flink files list` 供用户选择
4. **获取下载链接** - `volc_flink files url --name <对象名>`
5. **展示下载链接** - 向用户展示预签名 URL

### 查看依赖列表
1. **检测登录状态** - 确认已登录
2. **智能选择草稿** - 如果用户没有提供，列出项目和草稿供选择
3. **获取草稿内容** - `volc_flink drafts content -i <草稿ID>`
4. **展示依赖列表** - 向用户展示当前依赖

### 添加依赖
1. **检测登录状态** - 确认已登录
2. **智能选择草稿** - 如果用户没有提供，列出项目和草稿供选择
3. **查看当前依赖** - `volc_flink drafts content -i <草稿ID>`
4. **确认 JAR 包信息** - 确认路径和描述
5. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
6. **添加依赖** - `volc_flink drafts dependency add -i <草稿ID> --jar <JAR路径>`
7. **验证结果** - `volc_flink drafts content -i <草稿ID>` 确认添加成功
8. **可选：发布草稿** - 如果需要立即生效

### 删除依赖
1. **检测登录状态** - 确认已登录
2. **智能选择草稿** - 如果用户没有提供，列出项目和草稿供选择
3. **查看当前依赖** - `volc_flink drafts content -i <草稿ID>` 供用户选择
4. **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
5. **删除依赖** - `volc_flink drafts dependency remove -i <草稿ID> --jar <JAR的tos全路径>`
6. **验证结果** - `volc_flink drafts content -i <草稿ID>` 确认删除成功
7. **可选：发布草稿** - 如果需要立即生效

---

## 🎯 技能总结

### 核心功能
1. ✅ **TOS 文件管理** - 列出、上传、查看、更新 TOS 文件，获取下载链接【新增】
2. ✅ **查看依赖列表** - 查看草稿已添加的依赖
3. ✅ **添加依赖** - 添加 JAR 包依赖（本地或 TOS）
4. ✅ **删除依赖** - 删除不需要的依赖
5. ✅ **登录状态检测** - 操作前检测登录状态
6. ✅ **智能项目和草稿选择** - 交互式选择
7. ✅ **风险确认** - 使用 `../../COMMON.md` 的 Risk Confirmation 模板完成用户确认
8. ✅ **错误处理优化** - 友好的错误提示和解决方案

### TOS 文件管理功能详解【新增】

| 功能 | 命令 | 说明 |
|------|------|------|
| **列出文件** | `volc_flink files list` | 列出 TOS Jar Prefix 下的所有文件 |
| **上传文件** | `volc_flink files upload --file <path>` | 上传本地文件到 TOS |
| **查看详情** | `volc_flink files detail --name <name>` | 查看文件的详细信息 |
| **更新文件** | `volc_flink files update --name <name> --file <path>` | 覆盖更新已有的文件 |
| **获取链接** | `volc_flink files url --name <name>` | 获取预签名下载链接 |

### 完整工作流程【新增】

**使用 TOS 文件管理 + 依赖管理的完整流程**：

1. **上传 JAR 包到 TOS**
   ```bash
   volc_flink files upload --file /path/to/your.jar
   ```

2. **查看文件列表确认上传成功**
   ```bash
   volc_flink files list
   ```

3. **将 TOS 文件添加到草稿依赖**
   ```bash
   volc_flink drafts dependency add -i <草稿ID> --jar <TOS路径>
   ```

4. **发布草稿并重启任务**

这个技能可以完整地覆盖 Flink 任务的依赖管理流程，包括 TOS 文件的完整管理！
