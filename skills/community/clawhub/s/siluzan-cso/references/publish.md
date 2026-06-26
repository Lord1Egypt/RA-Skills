## 发布流程（AI 必须按此顺序与用户交互）

> **⚠️ AI 行为要求：每一步都必须等用户确认后再执行下一步。不要跳步或替用户做选择。**

---

### Step 1：确认 Token

首先检查用户是否已配置 Token：

```bash
siluzan-cso config show
```

- 若已配置，继续下一步。
- 若未配置，引导用户执行 `siluzan-cso login`，详见 `references/setup.md`。

---

### Step 2：询问发布类型

**明确询问用户：**

> "请问这次要发布的是 **视频** 还是 **图文**（图片+文案）？"

根据用户回答确定 `contentType`：

- 视频 → `contentType: 1`
- 图文 → `contentType: 2`

---

### Step 3：查询并让用户选择账号

```bash
siluzan-cso list-accounts
```

命令输出包含每个账号的名称、平台类型和过期时间。  
**展示给用户后，明确询问：**

> "以上是可用账号，请告诉我要发布到哪些账号（可多选）？"

注意：

- 过期账号（`到期`日期已过）不可选，告知用户
- 记住用户选择的账号 `entityId`，后续写入配置文件

> 需要精准查找某个账号的完整字段？→ 参见 `references/list-accounts.md`

---

### Step 4（视频）：收集视频内容

若为**视频**发布，依次询问：

1. **视频文件**：本地路径还是已在素材库中的 `videoId`？
   - 本地文件：继续执行 Step 4a（上传）
   - 已有素材 ID：跳到 Step 4b

2. **封面图片**：本地路径（上传视频时必须提供封面）

3. **标题（文案）**：这就是视频的主文案，所有平台共用。

4. **描述**（可选）：YouTube / Facebook 有独立描述字段；其他平台忽略此项

5. **话题/标签**（可选）：`#话题` 标签列表

6. **发布方式**：立即发布 or 定时发布？→ 参见下方"定时发布"说明

#### Step 4a：上传本地视频（含封面）

> 详细用法和字段说明 → 参见 `references/upload.md`

```bash
siluzan-cso upload -f /path/to/video.mp4 --cover /path/to/cover.jpg
```

命令成功后输出 JSON（含 `videoId`、`cover.sourceImageId`），直接用于生成配置文件。

若没有现成封面，可先截取 → 参见 `references/extract-cover.md`

#### Step 4b：素材库已有视频

直接使用用户提供的 `videoId`，封面 URL 同样需要用户提供。

---

### Step 5（图文）：收集图文内容

若为**图文**发布，依次询问：

1. **图片**：本地路径或已有 URL？
   - 本地文件：先上传（参见 `references/upload.md`）：`siluzan-cso upload -f /path/to/image.jpg`
   - 已有 URL：直接使用
2. **文案（标题）**：图文的主要文案，写在 `title` 字段。
3. **发布方式**：立即 or 定时 → 参见下方"定时发布"说明

**注意：TikTok 与 YouTube 当前不支持图文发布。若选择在这些平台上发布图文，请自动跳过，并提示用户："该平台暂不支持图文发布，已为您跳过。" 不执行发布操作。**

---

### 文案编写与润色

文案对应配置文件中的 `title` 字段（视频和图文均如此）：

- `title`：所有平台共用的主文案/标题
- `description`：YouTube、Facebook 专有的独立描述（其他平台忽略）
- `topics`：话题标签数组，如 `["美妆", "Facebook"]`
- `platformOverrides.<平台>.title`：给特定平台单独定制文案

AI 可直接帮助润色：加钩子开头、适配平台风格、加 SEO 关键词、控制字数（YouTube ≤100字建议）。

---

### 定时发布 vs 立即发布

**立即发布**

```json
"publishMode": "immediate"
```

**定时发布**

```json
"publishMode": "scheduled",
"publishAt": "2026-04-08T10:00:00+08:00"
```

`publishAt` 时间格式：**ISO 8601，必须包含时区**，中国时间后缀 `+08:00`。

| 用户说                      | publishAt 值                |
| --------------------------- | --------------------------- |
| 明天上午 10 点（北京时间）  | `2026-04-08T10:00:00+08:00` |
| 后天下午 3 点半（北京时间） | `2026-04-09T15:30:00+08:00` |

> AI 须根据今天日期自动推算"明天"、"后天"等相对时间，不需要让用户手动输入 ISO 格式。

**多平台不同时间发布**

全局 `publishMode` / `publishAt` 作为默认值；某平台需要不同时间时，在 `platformOverrides.<平台>` 中覆盖：

```json
"publishMode": "scheduled",
"publishAt": "2026-04-08T10:00:00+08:00",
"platformOverrides": {
  "YouTube": {
    "publishMode": "scheduled",
    "publishAt": "2026-04-08T18:00:00+08:00"
  }
}
```

某平台可单独设为立即发布：`"publishMode": "immediate"`（无需 `publishAt`）。

**多平台不同封面（仅视频）**

全局 `cover` 作为默认封面；某平台需要不同封面时：

```json
"cover": {
  "imageUrl": "https://cdn.example.com/cover-default.jpg",
  "imageName": "cover-default.jpg",
  "imageSourceType": 1,
  "sourceImageId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
},
"platformOverrides": {
  "YouTube": {
    "cover": {
      "imageUrl": "https://cdn.example.com/cover-youtube.jpg",
      "imageName": "cover-youtube.jpg",
      "imageSourceType": 1,
      "sourceImageId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
  }
}
```

---

### Step 6：汇总确认

将收集到的信息汇总展示给用户：

> "我将为你创建以下发布任务，请确认：
>
> - 类型：视频 / 图文
> - 账号：XXX（YouTube）
> - 标题：XXX
> - 发布方式：立即 / 定时（时间）
>   确认提交？"

---

### Step 7：生成配置文件 & 预览

- **图文配置文件结构：** 参见 `assets/publish-config-image.example.json`
- **视频配置文件结构：** 参见 `assets/publish-config.example.json`

**⚠️ UUID 字段必须用真实值，不能用占位符文本**

以下字段后端会做严格 GUID 格式校验，填写错误将导致 HTTP 500：

| 字段                                     | 来源                                                                     |
| ---------------------------------------- | ------------------------------------------------------------------------ |
| `accounts[].entityId`                    | `list-accounts --json-out` 落盘数据的 `entityId` 字段                    |
| `accounts[].externalMediaAccountTokenId` | `list-accounts --json-out` 落盘数据的 `externalMediaAccountTokenId` 字段 |
| `videos[].videoId`                       | `upload` 命令返回的 `videoId`                                            |
| `cover.sourceImageId`                    | `upload` 命令返回的 `sourceImageId`                                      |

> `mediaCustomerId` 不是 UUID，是各平台账号 ID，直接填写即可。

生成 `publish-config.json` 后，先预览：

```bash
siluzan-cso publish -c publish-config.json --dry-run
```

---

### Step 8：提交发布

用户确认 dry-run 无误后：

```bash
siluzan-cso publish -c publish-config.json
```

成功后：

1. 记录返回的**任务 ID（publishId）**，后续查询状态时需要用到
2. 告知用户：
   - 立即发布：正在发布，可用 `siluzan-cso task list` 查看进度
   - 定时发布：任务已创建，到时间自动发布

> 查询发布状态、处理失败项 → 参见 `references/task.md`

前往 CSO 任务管理页面查看进度：`https://www.siluzan.com/v3/foreign_trade/cso/task`

---

## 交叉引用

- 获取账号 entityId / externalMediaAccountTokenId → 参见 `references/list-accounts.md`
- 上传视频/图片/封面 → 参见 `references/upload.md`
- 截取视频封面 → 参见 `references/extract-cover.md`
- 查看发布状态 / 处理失败 → 参见 `references/task.md`
