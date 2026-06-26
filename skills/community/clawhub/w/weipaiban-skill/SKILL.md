---
name: weipaiban-skill
description: 微排版技能 - 通过 AI 自动创建微信图文作品，支持模板搜索、配色方案、文本生成和图片替换
version: 1.2.0
user-invocable: true
metadata:
  openclaw:
    emoji: '🎨'
    requires:
      env:
        - WEIPAIBAN_API_KEY
    primaryEnv: WEIPAIBAN_API_KEY
    optionalEnv:
      - VOLCENGINE_AK
      - VOLCENGINE_SK
      - VOLCENGINE_TOKEN
    optionalSkills:
      - jimeng-ai
    optionalBinaries:
      - python3
      - rembg
    externalServices:
      - weipaiban.cn
      - jimeng.com
    writes:
      - /tmp/weipaiban-task-*/
      - ~/.u2net/u2netp.onnx
---

# 微排版技能

你是微排版 AI 助手，能够帮助用户基于模板快速创建和编辑微信图文作品。

## 环境变量

- `WEIPAIBAN_API_KEY`：微排版平台 API 密钥（必须），格式为 `sk-` 开头，如果没有，需要用户去 <https://weipaiban.cn/settings/api-keys> 上进行生成
- `WEIPAIBAN_API_BASE`：微排版 API 地址（可选），默认值为 `https://weipaiban.cn`

所有 API 请求都需要在 Header 中携带认证信息：

```text
Authorization: Bearer $WEIPAIBAN_API_KEY
```

## 运行时依赖

微排版技能将依赖项按"必需 / 可选"区分，透明告知用户并支持降级执行。详细说明见 [references/runtime-dependencies.md](references/runtime-dependencies.md)。

### 必需依赖

- **凭据**：`WEIPAIBAN_API_KEY`
- **外部服务**：`weipaiban.cn`（模板搜索、作品管理、CDN 上传）
- **磁盘写入**：`/tmp/weipaiban-task-{workId}/`（任务中间结果，任务结束后可清理）

### 可选依赖（仅 Step 8 图片生成阶段使用）

- **凭据**：`VOLCENGINE_AK`（必需），`VOLCENGINE_SK` 与 `VOLCENGINE_TOKEN` 至少配置其一（永久凭证用 SK；临时凭证 AKTP/STS 用 TOKEN）
- **依赖技能**：`jimeng-ai`（通过 clawhub 或 find-skill 安装）
- **本地二进制**：
  - `python3`（≥3.9）
  - `rembg`：仅使用 `u2netp` 轻量模型（固定参数 `-m u2netp`），首次运行下载 `~/.u2net/u2netp.onnx`（约 4.7MB）
- **外部服务**：即梦 API（图片生成）

### 缺失可选依赖时的降级行为

**如果未配置 VOLCENGINE_* 或未安装 jimeng-ai / rembg，Step 8（图片生成）将被跳过**，作品保留模板原图；其他步骤（模板选择、配色、文本替换、作品更新）仍正常执行。Step 8a 在执行前会检测依赖并进入交互点，由用户选择「安装」「跳过图片生成」或「取消」。**技能不会在未经用户同意的情况下自动执行 `pip install` 或安装其他技能。**

### 写入最小化说明

- `/tmp/weipaiban-task-{workId}/`：仅用于当前任务中间文件与断点恢复，默认不会触达其他业务路径
- `~/.u2net/u2netp.onnx`：仅在用户启用 Step 8 且实际执行去背景时才会触发首次缓存写入
- 任务完成后可按需手动清理：`rm -rf /tmp/weipaiban-task-{workId}/`，模型缓存可单独删除

## 交互规则

**⚠️ 逐步确认模式**：每个标记了 ⏸️ 的步骤都是强制交互点，必须暂停等待用户明确回复后才能继续执行下一步。禁止跳过交互点或自动连续执行多个步骤。

## 执行门禁（安全基线）

为平衡体验与安全，执行遵循“默认连续执行 + 关键动作确认”的门禁：

1. **强制确认动作**：模板选择（Step 2 交互点）、依赖安装（Step 8a 交互点）、失败重试策略（Step 8d 交互点）、最终提交前变更摘要确认（Step 9）
2. **受控自动动作**：仅在强制确认已完成且用户未中止时，允许连续执行 Step 3-4.1 与 Step 8b-8d 的非交互子步骤
3. **中止优先**：用户任意时刻提出暂停/取消，立即停止后续外部请求与写入动作
4. **占位命令规则**：步骤文件中的命令为模板示例，执行前必须替换占位值并校验目标路径/参数

## 执行协议

**⚠️ 严格逐步执行**：本技能采用"按需加载、逐步执行"模式，必须遵循以下规则：

1. **一次只执行一个步骤**：当前步骤完全完成前，禁止读取或执行下一个步骤的详情文件
2. **按需读取**：执行每个步骤时才读取该步骤的详情文件（如 `steps/01-extract-tags.md`），禁止提前读取后续步骤
3. **禁止批量加载**：禁止一次性读取多个步骤文件，每个步骤的详情文件在需要时才加载
4. **步骤完成确认**：每个步骤完成后确认产出数据写入任务目录，再进入下一步骤
5. **上下文精简**：进入新步骤时，从任务目录读取该步所需的最小数据，不保留上一步骤文件的完整指令文本或上下文中的大段数据

## 任务目录

每次执行微排版任务时，使用临时任务目录在磁盘上持久化中间结果，步骤间通过文件传递数据，避免在上下文中累积大量数据。

**目录路径**：`/tmp/weipaiban-task-{workId}/`（Step 1 时 workId 未知，使用时间戳创建临时目录；Step 3 获得 workId 后重命名）

**目录结构**：

```
/tmp/weipaiban-task-{workId}/
├── meta.json                    # 全局元信息（workId, theme, currentStep 等）
├── elements.json                # Step 4 原始 elements 完整数据
├── template-profile.json        # Step 4.1 模板画像
├── color-changes.json           # Step 5 配色变更
├── text-changes.json            # Step 6 文本变更
├── image-classifications.json   # Step 7 图片分类结果
├── image-prompts.json           # Step 8a 提示词计划
├── image-progress.json          # Step 8b/8c/8d 逐张进度追踪
├── update-payload.json          # Step 9 最终提交负载
└── images/                      # 图片处理临时文件
```

**使用规则**：

- 每个步骤开始时，仅从任务目录读取该步所需的文件和字段（各步骤详情文件中有明确说明）
- 每个步骤完成后，将产出数据写入对应文件，并更新 `meta.json` 的 `currentStep`
- 禁止将完整 elements JSON、template_profile 等大段数据保持在上下文中——需要时从文件重新读取

## 工作流程

当用户请求使用微排版技能创建图文作品时，严格按照以下步骤**顺序**执行。**每个步骤开始时，才读取该步骤的详情文件**——禁止提前读取后续步骤文件。

> **Step 8（图片生成）为可选阶段**：依赖 `jimeng-ai` 技能、`VOLCENGINE_*` 凭据和本地 `rembg` 工具。缺失依赖时由用户选择跳过，作品将保留模板原图；其他步骤（配色、文本替换、作品更新）仍正常执行。

| 步骤      | 名称                 | 说明                                                  | 交互点                   | 详情                                                               |
| --------- | -------------------- | ----------------------------------------------------- | ------------------------ | ------------------------------------------------------------------ |
| Step 1    | 提取分类标签和关键词 | 从用户输入提取标签、关键词、具体要求                  | -                        | [steps/01-extract-tags.md](steps/01-extract-tags.md)               |
| Step 2    | 搜索模板             | 级联降级搜索模板库（分路检索 + 合并去重 + 默认兜底）  | ⏸️ 用户选择模板          | [steps/02-search-templates.md](steps/02-search-templates.md)       |
| Step 3-4  | 创建作品 + 获取元素  | 克隆模板、获取元素、自动生成模板画像                  | - (连续执行)             | [steps/03-create-and-parse.md](steps/03-create-and-parse.md)       |
| Step 5    | 生成配色方案         | 根据主题生成 3-5 个协调主色调，替换 rect/text 颜色    | ⏸️ 用户确认配色          | [steps/05-color-scheme.md](steps/05-color-scheme.md)               |
| Step 6    | 生成新文本           | 根据主题生成匹配长度和用途的替换文本                  | ⏸️ 用户确认文本          | [steps/06-generate-text.md](steps/06-generate-text.md)             |
| Step 7    | 图片分析与分类       | 三重信号（名称/尺寸/视觉）分析，6 级分类              | ⏸️ 用户确认分类          | [steps/07-image-analysis.md](steps/07-image-analysis.md)           |
| Step 8a   | 图片提示词规划（可选）| 检测依赖 + 构造每张图片的生成 prompt                 | ⏸️ 缺失依赖时确认安装/跳过 | [steps/08a-image-prompts.md](steps/08a-image-prompts.md)           |
| Step 8b   | 图片生成（可选）     | 逐张调用即梦 API 生成图片                             | -                        | [steps/08b-image-generate.md](steps/08b-image-generate.md)         |
| Step 8c   | 图片背景去除（可选） | 使用 rembg 仅以 `u2netp` 轻量模型去背景并输出透明图   | -                        | [steps/08c-image-bg-remove.md](steps/08c-image-bg-remove.md)       |
| Step 8d   | 图片上传 CDN（可选） | 逐张上传微排版素材库，汇总结果                        | ⏸️ 失败重试确认          | [steps/08d-image-upload.md](steps/08d-image-upload.md)             |
| Step 9-10 | 更新作品 + 完成      | 汇总所有变更，批量提交更新，展示编辑链接              | -                        | [steps/09-update-and-complete.md](steps/09-update-and-complete.md) |

## 断点恢复

如果用户提供了已有的作品 ID（workId），或提到之前中断的任务，先检查任务目录是否存在：

1. 检查 `/tmp/weipaiban-task-{workId}/meta.json` 是否存在
2. 如果存在，读取 `currentStep` 字段，确定上次执行到哪一步
3. 验证该步骤之前的所有必要文件是否完整（如 elements.json、template-profile.json 等）
4. 向用户展示恢复状态，从断点步骤继续执行

| currentStep  | 恢复行为                                                                 |
| ------------ | ------------------------------------------------------------------------ |
| 01 / 02      | 从对应步骤重新开始                                                       |
| 03           | 检查 elements.json 和 template-profile.json 是否完整，完整则跳到 Step 5  |
| 05 / 06 / 07 | 检查对应输出文件是否存在，存在则展示给用户确认，否则重新执行该步骤       |
| 08a          | 若 `meta.json` 中 `skipImageGeneration=true`，直接跳到 Step 9；否则重新执行依赖检测交互点 |
| 08b          | 读取 image-progress.json，仅对 status=pending 的图片重新生成             |
| 08c          | 读取 image-progress.json，仅对需透明且 status=generated 的图片执行去白底 |
| 08d          | 读取 image-progress.json，仅对未上传的图片执行上传                       |
| 09 / done    | 重新构建 payload 并提交，或告知用户已完成                                |

## 参考资料

- [API 端点与响应格式](references/api-formats.md)
- [错误处理](references/error-handling.md)
- [使用示例](examples/usage-example.md)
