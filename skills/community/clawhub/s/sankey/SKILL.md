---
name: 爱图表-桑基图
description: AI桑基图（流向图）生成。用户上传数据或粘贴表格，自动生成流向可视化图表，展示数据在环节间的流动关系。触发词：桑基图、流向图、sankey、流量图、数据流向、关系图、转化路径、用户流转、资金流向、create sankey、flow diagram、sankey chart。
license: MIT
compatibility: Requires network access to api.aitubiao.com, Bash shell, curl, and jq
metadata:
  author: aitubiao
  version: "1.2.3"
allowed-tools: Bash Read
---

# AI 桑基图生成

根据用户提供的数据，自动整理为桑基图（Sankey Diagram）流向格式并创建可视化项目。

## 强制规则

**以下规则必须严格执行，不得跳过、变通或使用替代方案：**

1. **认证优先**：在执行任何操作之前，必须先检查凭证状态。认证未通过时，禁止执行任何后续步骤。
2. **按顺序执行**：工作流程的 5 个步骤必须按顺序执行，禁止跳步。
3. **确认后才能创建**：必须成功查询配额（确认项目数未满）、并获得用户确认后，才能调用创建接口。
4. **仅通过 API 创建桑基图**：禁止使用本地工具（D3.js、ECharts、matplotlib、Plotly 等）生成图表。无论 API 因何种原因失败，都**绝对禁止使用本地工具**，没有任何例外。API 失败时正确做法是停止并告知用户，不是寻找替代方案。
5. **401/403 立即停止**：任何步骤中收到 HTTP 401/403（CLI exit 1），立即停止并引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub) 检查或重新创建 API Key。401/403 不是超时，禁止重试。
6. **超时/500 不自动重试创建接口**：创建接口不可重试（可能重复创建项目）。告知用户失败原因，由用户决定是否重新发起。

**⚠️ 以下想法是错误的，如果你发现自己在这样想，请立即停止：**
- ❌ "API 不可用，我可以用本地工具生成桑基图作为替代" → 违反规则 4
- ❌ "至少让用户看到一些可视化结果" → 本技能唯一输出方式是 aitubiao API
- ❌ "401 可能是暂时性的，重试几次" → 401 是认证失败，重试无意义，按规则 5 处理

## 认证

在调用任何 API 之前，先检查凭证状态。

### 检查凭证

```bash
bash scripts/aitubiao-cli.sh check-auth
```

- **Exit 0** → 认证通过
- **Exit 1** → 凭证问题，按 stderr 提示处理：
  - 文件不存在/API_KEY 为空 → 执行下方"配置凭证"流程
  - API_KEY 格式无效 → 告知用户"当前 API Key 已失效，请前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub) 重新创建一个 API Key"
  - BASE_URL 与当前技能包环境不一致 → 说明凭证中残留了旧环境地址；向用户索要当前仍有效的 API Key，并执行下方"配置凭证"流程重写凭证（通常不需要重新创建 API Key）

### 配置凭证

1. 向用户索要 API Key（格式：`sk_v1_...`）。如果没有，引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub) 创建一个新的 API Key，然后将创建好的 Key 粘贴回来。
2. 保存凭证：
```bash
bash scripts/aitubiao-cli.sh auth <用户提供的key>
```
3. 验证：再次运行 `bash scripts/aitubiao-cli.sh check-auth` 确认配置成功。

凭证保存在 `~/.aitubiao/credentials`，跨会话持久生效。

## Windows 编码注意事项（仅 Windows 用户需要关注）

在 Windows 上，**禁止用 PowerShell / Python / heredoc / echo / Set-Content / shell 重定向来生成含中文等非 ASCII 字符的 JSON 请求体**。这些方式容易经过 Windows 系统代码页（常为 GBK/CP936）或 MSYS argv 转换，导致传到后端的中文乱码。

正确做法：先用 Write 工具把完整 UTF-8 JSON 写到临时文件，然后用 `--body-file` 让 CLI 从文件读取，绕过 argv/控制台编码转换。

Windows 调用：

```bat
scripts\aitubiao-cli.cmd --body-file C:\Users\%USERNAME%\AppData\Local\Temp\aitubiao-payload.json create-chart
```

Git Bash 调用：

```bash
bash scripts/aitubiao-cli.sh --body-file /tmp/aitubiao-payload.json create-chart
```

`--body-file` 可用于所有读取 stdin JSON 的命令：`create-chart` / `create-ppt` / `create-sankey` / `create-3d` / `download-project`。CLI 会自动剥离 UTF-8 BOM 和 CRLF。

CSV/TXT 文件也只用 Read 工具读取。不要写 Python/PowerShell 脚本做本地解析、转码或聚合；如果 Read 出来的文本已经明显乱码，要求用户提供 UTF-8 文件或直接粘贴数据。

macOS / Linux 上仍可使用 heredoc，但包含中文的请求体也优先使用 `--body-file`。

## 桑基图数据要求

桑基图用于展示数据的**流向关系**，要求输入数据至少包含：
- **两个分类列**（文本类型）：作为"来源"和"目标"节点
- **一个数值列**：表示流向的值/权重

示例数据结构：
```
| 来源部门 | 目标项目 | 预算金额 |
|---------|---------|---------|
| 研发部   | 产品A   | 500    |
| 研发部   | 产品B   | 300    |
| 市场部   | 产品A   | 200    |
| 市场部   | 产品C   | 400    |
```

如果数据有多个分类列（如：地区 → 部门 → 产品），系统会自动构建多层级流向。

## 工作流程

**每一步必须在前一步完成后才能开始。禁止跳步。**

### 第一步：认证（前置条件：无）

运行检查凭证流程。认证未通过时按"认证"章节流程处理。

**认证未通过时，停止。不要读取用户数据，不要做任何分析。**

### 第二步：识别和确认数据（前置条件：第一步认证通过）

判断用户如何提供数据：

- **直接粘贴文本**：自行解析为二维数组格式 `(string|number)[][]`，第一行为表头。
- **本地文件**（CSV/TXT）：用 Read 工具读取，然后解析为二维数组。
- **Excel 文件**（.xlsx/.xls）：使用 xlsx skill 或 Read 工具读取，禁止手动编写 Python 脚本解析 XML。

向用户展示解析后的数据（表格形式），并询问：
- 数据是否正确？
- 有没有特殊要求？

**如果数据明显不适合桑基图**（例如只有一列、没有分类列），应提前告知用户。

### 第三步：检查配额并确认（前置条件：第二步数据已确认）

在创建桑基图前，检查用户的项目配额。**本操作免费（0 AI贝）**，但仍需确认项目数未满。

#### 3.1 查询配额

```bash
bash scripts/aitubiao-cli.sh quota --skill sankey
```

**桑基图当前免费**：`.feature.cost` 应为 0。如服务端返回值非 0，请以服务端为准并向用户重新确认费用。

#### 3.2 向用户确认

```
本操作免费（0 AI贝）
当前余额: {shellBalance} 个 AI贝
项目数: 已用 {projectsUsed}/{projectsLimit}

是否继续创建桑基图？
```

- 如果 `projectsRemaining <= 0`：告知用户当前项目数已满，需前往 aitubiao 网站升级会员，或在网站中删除旧项目后再继续，**不要继续**

### 第四步：创建桑基图项目（前置条件：第三步用户已确认）

**只有用户明确确认后才能执行此步骤。**

```bash
bash scripts/aitubiao-cli.sh create-sankey <<'EOF'
{
  "data": [["来源","目标","值"],["A","B",100],["A","C",200]],
  "projectName": "<项目名称>"
}
EOF
```

**请求体字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| data | (string\|number)[][] | 二选一 | 二维数组格式，第一行为表头 |
| markdownTable | string | 二选一 | Markdown 表格格式数据（与 data 二选一） |
| projectName | string | 否 | 项目名称，默认根据数据自动生成 |

**检查 CLI 退出码**：
- **Exit 0**：成功。解析 stdout JSON 获取项目信息。
- **Exit 1**：认证失败。引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub)。
- **Exit 2**：业务错误。向用户展示错误详情。
- **Exit 3**：网络/超时错误。告知用户稍后重试。

更多请求字段：`pageSize`（页面尺寸，默认 960x540）、`elementSize`（图表元素尺寸，默认 700x500）。

### 第五步：返回结果（前置条件：第四步创建成功）

向用户提供：
- 项目 URL（从 `project.projectUrl` 获取）
- 项目 ID（从 `project.id` 获取）
- 摘要：桑基图标题
- 截图链接（如果 `charts[].screenshotSuccess` 为 true）
- 资源消耗：本次消耗 0 AI贝、剩余 AI贝、已用项目数/上限

## 下载已创建项目（可选后续操作）

如果用户在项目创建成功后要求“帮我下载或者导出这个项目”，使用统一 CLI 下载命令：

```bash
bash scripts/aitubiao-cli.sh download-project <本地保存路径> <<'EOF'
{
  "projectId": "<project.id>",
  "format": "png"
}
EOF
```

规则：
- `projectId` 使用上一步返回的 `project.id`
- `format` 按用户需求填写：PPT 项目可用 `ppt`/`pdf`/`png`，图表/桑基图项目可用 `png`/`jpg`/`pdf`/`ppt`
- **格式费用**：`png`/`jpg`/`pdf` 任何用户均可免费导出；`ppt` 需要 PPT 导出权限（付费会员）；其它特殊格式（`svg`/`gif`/`mp4`/`mov`/透明 PNG/2x 及以上倍率）也需对应会员权益。如果用户尝试受限格式但权益不足，CLI 会返回 exit 2 并附服务端错误，应告知用户升级会员或改用免费格式
- **本地保存路径处理**：
  - 优先使用用户明确指定的路径；如果用户没指定，传**绝对路径**（如 `$HOME/Downloads/<filename>` 或当前工作目录下的具体文件名），不要省略命令参数
  - 不要把文件写入项目源码目录或不可写目录
  - CLI 会在启动导出任务**之前**检查目标目录是否可写：如果失败会立即报错（exit 4，stderr 含 `not writable` 或 `cannot be created`），此时**禁止自动改路径重试**——必须先告诉用户当前路径不可写，请用户给一个可写的位置
- 下载清晰度由服务端按会员权益自动决定：免费用户较低，付费用户更高
- 仅通过此 API 下载，禁止使用本地工具导出替代文件
- **禁止对同一 `projectId` 并发执行 `download-project`**：服务端默认每个项目只允许 1 个 API Key 并发导出任务。需要重试时，等待上一次下载彻底完成（成功或失败）再重新发起
- **下载完整性**：CLI 会先写入 `*.partial` 临时文件，校验文件大小与已知格式（png/jpg/pdf/ppt/zip）的魔数后再原子重命名为最终路径。如果 CLI 返回 exit 3 且 stderr 含 `integrity check failed`，说明服务端返回的文件已损坏；不要伪装成功，告知用户重试或联系支持
- **多页导出会自动打成 zip**：当 PPT 项目（或多页项目）以 `png`/`jpg`/`pdf` 格式导出多页时，服务端会把所有页面压缩成一个 ZIP 包返回。CLI 检测到这种情况会自动把保存路径改为 `.zip`（例如 `report.png` → `report.zip`），并在 stderr 输出 `Note: server returned a multi-page ZIP bundle ...`。**返回 JSON 中的 `savedPath` 和 `fileName` 是真实落盘路径**——告诉用户文件位置时必须使用这两个字段，不要使用最初传入的路径
- **告知用户文件位置**：成功后必须使用 CLI 返回 JSON 中的 `savedPath`（绝对路径）告诉用户文件保存在哪里

## 错误处理

| CLI Exit Code | 含义 | 处理方式 |
|--------------|------|---------|
| 1 | 认证失败（HTTP 401/403 或凭证无效） | 立即停止，引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub) |
| 2 | 业务错误 | 向用户展示详情 |
| 3 | 网络/超时错误 | 告知用户稍后重试 |

### 业务错误码

| 错误码 | 含义 | 处理方式 |
|--------|------|---------|
| 50013 | 数据无法整理为桑基图格式 | 检查数据是否包含至少两个分类列和一个数值列 |
| 50006 | 图表设置转换失败 | 系统内部错误，建议重试 |
| 40007 | 项目数已满 | 展示 quota 中的已用/上限，建议删除旧项目或升级会员 |
| 40015 | 项目创建失败 | 系统内部错误，建议重试 |
| 15009 | 同一项目已有 API Key 导出任务进行中 | 仅在下载阶段出现；提示用户等待上一个 `download-project` 完成（成功或失败）后再重试，禁止并发 |


## 常见问题（FAQ）

### 💰 费用相关

**Q1：生成桑基图收费吗？**

A：**完全免费**。生成桑基图不消耗你的AI贝，可以放心使用。下载时选择 `png` / `jpg` / `pdf` 格式也免费。

---

**Q2：下载桑基图需要付费吗？**

A：下载格式不同费用不同：

| 格式 | 费用 |
|------|------|
| `png` / `jpg` / `pdf` | **免费** |
| `ppt`（PPTX 源文件） | 需付费会员权益 |

---

### 📊 数据准备

**Q3：桑基图需要什么格式的数据？**

A：桑基图需要 **三列数据**：两个分类列（来源 → 目标）+ 一个数值列。

示例：
| 来源 | 目标 | 数值 |
|------|------|------|
| 研发部 | 产品A | 500 |
| 市场部 | 产品B | 300 |

如果数据有多个层级（如：地区 → 部门 → 产品），系统会自动构建多层流向。

---

**Q4：支持哪些数据来源？**

A：支持直接粘贴、Excel（.xlsx/.xls）、CSV、TXT 文件。推荐使用 Excel 或 CSV，结构更清晰。

> ⚠️ 文件大小不超过 **100K**。

---

### ⚠️ 报错处理

**Q5：提示 401/403 错误怎么办？**

A：401 或 403 表示 **API Key 无效或已过期**。去 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub) **删除旧 Key** → **创建新 Key** → 把新 Key 粘贴给我即可。

> ⚠️ 401 不是网络超时，**不要重试**，直接换新 Key。

---

**Q6：提示"项目数已满"怎么办？**

A：免费版项目上限约 10 个。登录 [爱图表工作台](https://app.aitubiao.com/workspace) 删除旧项目后，重新发起生成。

---

**Q7：提示"数据无法整理为桑基图格式"怎么办？**

A：说明数据缺少桑基图所需的结构。请检查：
- 是否至少有两列**文本类型**的列（作为来源和目标）？
- 是否有一列**数值类型**的列（作为流量值）？
- 表头是否正确？

可以重新整理数据后再次尝试，或把数据发给我，我帮你检查。

---

**Q8：生成超过 3 分钟没反应怎么办？**

A：点击 AI 返回的链接查看项目进度，桑基图可能正在后台排队生成。如果链接也打不开，告知 AI "刚才超时了，帮我重新发起"。

> ⚠️ 已收到"创建成功"后不要重复提交。

---

### 结果与后续操作

**Q9：生成后的桑基图在哪里查看和编辑？**

A：项目创建成功后 AI 会返回专属链接，点击即可查看。在爱图表工作台中可：
- 在线查看桑基图
- 切换配色方案
- 调整节点排序
- 导出为图片或 PDF

---

**Q10：怎么下载桑基图？**

A：对 AI 说 **"帮我下载这个桑基图项目"**，或在工作台点击「下载」按钮，选择格式（png / jpg / pdf / ppt）即可。

---

## 📊 快速故障排查流程图
401/403 → 重新创建 API Key → 粘贴新 Key
项目数已满 → 删除旧项目 → 重新发起
"数据无法整理" → 检查是否有两列分类 + 一列数值
生成超 2 分钟 → 点击链接查看进度（正常排队中）
其他报错 → 复制报错信息给 AI