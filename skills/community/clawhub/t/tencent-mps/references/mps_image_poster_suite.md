# 套图生成参数与示例 — `mps_image_poster_suite.py`

**功能**：上传商品主图，按指定主题列表批量产出多张广告海报 panel。
调用 MPS `ProcessImage` 接口的 `ImageTask.AiPosterSuiteConfig` 字段，通过 `DescribeImageTaskDetail` 轮询等待结果，
返回变量回显 + panel 图片列表。

适用场景：电商商品图批量生成、广告海报制作、营销素材快速产出、多平台商品图定制等。

> **参数命名约定**：套图脚本使用 `--product-url` / `--product-cos-key`（商品主图输入），**不是**其他脚本的 `--url` / `--cos-input-key`。所有脚本均支持 `--dry-run`（预演）和 `--no-wait`（异步不等待）。

### 最常用参数速查

| 参数 | 说明 | 示例 |
|------|------|------|
| `--product-url` | 商品主图 URL | `--product-url "https://example.com/p.jpg"` |
| `--product-cos-key` | 商品主图 COS Key | `--product-cos-key "/input/product.jpg"` |
| `--definition` | 平台 ID（必填） | `--definition 50`（50=淘宝 51=亚马逊 52=京东 53=拼多多 54=Temu 55=TikTok） |
| `--recipe` | 主题:数量（必填） | `--recipe hero:2 --recipe detail:2` |
| `--ext-prompt` | 用户文案变量 | `--ext-prompt BrandName AURASKIN` |
| `--user-prompt` | 自由文 | `--user-prompt "强调按压泵设计"` |
| `--mode` | auto（默认）/ modify | `--mode modify` |
| `--dry-run` | 预演不调用 API | `--dry-run` |
| `--no-wait` | 提交后不等待 | `--no-wait` |

---

## 两种执行模式

| 模式 | 是否自动提取商品信息 | `ExtPrompt` 作用 | 典型场景 |
|------|------------|----------------|---------|
| **auto**（默认） | 是，自动从商品图提取品牌、卖点、配色等 | 可选地覆盖个别字段、补充自由文 | 第一次生成整套 panel |
| **modify** | 否，不做自动提取 | **必须回填所有 9 个标准变量**（不可只传子集） | 基于 auto 结果本地修改字段后迭代 |

> **最佳实践（auto → modify）**：第一次用 auto 拿到响应；从响应 `[0].Output.Content` 解析出变量回显，本地修改某些字段后，原样塞回 `AddOnParameter`，同 Definition + Recipe 用 modify 重发。

---

## Definition 与平台对应

| Definition | 平台 |
|---|---|
| `50` | 淘宝/天猫 |
| `51` | 亚马逊（Amazon） |
| `52` | 京东 |
| `53` | 拼多多 |
| `54` | Temu |
| `55` | TikTok |

不同 Definition 在视觉风格上各有差异（如京东偏克制精致、拼多多偏热闹高饱和、Temu 偏明亮简洁），但所有平台共享相同的 6 个标准 `Theme` 名。

---

## 标准主题（6 类）

| `Theme` | 用途 |
|---|---|
| `hero` | 主图，产品居中、视觉冲击力最强的封面图 |
| `selling` | 卖点图，图标 / 标注呈现核心卖点信息 |
| `scene` | 场景图，产品在真实使用场景中的呈现 |
| `detail` | 细节图，微距特写突出材质 / 工艺 / 质感 |
| `angles` | 多角度图，不同视角展示产品外观 |
| `atmosphere` | 氛围图，强调品牌调性 / 生活感 |

---

## 参数说明

### 输入参数

| 参数 | 说明 |
|------|------|
| `--product-url` | 商品主图 URL（与 `--product-cos-key` **二选一**，必填） |
| `--product-cos-key` | 商品主图 COS 对象 Key（如 `/input/product.jpg`），与 `--product-url` 二选一 |
| `--product-cos-bucket` | 商品主图 COS Bucket（默认读取 `TENCENTCLOUD_COS_BUCKET`） |
| `--product-cos-region` | 商品主图 COS Region（默认读取 `TENCENTCLOUD_COS_REGION`） |
| `--image-url` | 附加商品视角图 URL，可重复传入多次（最多 3 张） |
| `--image-cos-key` | 附加商品视角图 COS 对象 Key，可重复传入多次（最多 3 张） |
| `--image-cos-bucket` | 附加商品视角图 COS Bucket（默认读取 `TENCENTCLOUD_COS_BUCKET`） |
| `--image-cos-region` | 附加商品视角图 COS Region（默认读取 `TENCENTCLOUD_COS_REGION`） |

> **说明**：商品主图必须指定 `--product-url` 或 `--product-cos-key` 之一；附加商品视角图可选，最多 3 张。

### 套图配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--definition` | —（必填） | 模板包 ID：`50`=淘宝/天猫 / `51`=亚马逊 / `52`=京东 / `53`=拼多多 / `54`=Temu / `55`=TikTok |
| `--recipe` | —（必填） | 主题与数量，格式 `Theme:Num`（如 `hero:2`），可重复；单主题 Num 1-4，全部 panel 总数 4-12 |
| `--mode` | `auto` | 执行模式：`auto` / `modify` |
| `--language` | `zh-CN` | 文案语言：`zh-CN` / `en-US` |
| `--panel-ratio` | `1:1` | Panel 宽高比：`1:1` / `3:2` / `2:3` / `3:4` / `4:3` / `9:16` / `16:9` |
| `--panel-resolution` | `1K` | Panel 分辨率：`720` / `1K` / `2K` / `4K` |
| `--model` | `WAND-suite-1.0-flash` | 模型（当前可用） |

### ExtPrompt（用户文案变量）

| 参数 | 说明 |
|------|------|
| `--ext-prompt ROLE PROMPT` | 用户文案变量条目，格式 `Role Prompt`（如 `--ext-prompt BrandName AURASKIN`），可重复 |
| `--user-prompt TEXT` | 自由文条目（`Role=UserPrompt`），整请求至多 1 条；与 `--ext-prompt UserPrompt` 不可同时使用 |

#### 标准变量 Role（9 个）

| `Role` | 含义 | 示例值 |
|---|---|---|
| `BrandName` | 商品包装上呈现的品牌名（不存在则留空，不允许译写） | `AURASKIN` |
| `Headline` | 广告主标语，4–8 个字，有冲击力 | `持续焕活，敏肌可用` |
| `SellingPointsText` | 卖点列表，3–4 条用 ` / ` 拼接，描述性语言、不写具体数字 | `保湿 / 紧致 / 抗氧化` |
| `ProductCategory` | 商品类目，"主类-子类"格式，5–8 字 | `美妆-护肤` |
| `ProductVisualIdentity` | 商品视觉特征：颜色 / 形状 / 材质 / 比例 / 表面光泽等 | `matte glass dropper bottle, amber, frosted` |
| `TextureDescription` | 商品质地或材质描述 | `silky cream` / `lightweight gel` |
| `ColorPalette` | 品牌色板，3 个 HEX 值用 `,` 分隔（与文案语言无关） | `#F5C2C7,#A8DADC,#F1FAEE` |
| `TargetAudience` | 目标人群画像 | `都市白领女性 22–35 岁` |
| `SceneContext` | 推荐展示场景 + 使用时刻 | `晨间梳妆台 / 户外运动后` |

> 文案类字段（`Headline` / `SellingPointsText` / `ProductCategory` / `TargetAudience` / `SceneContext` / `TextureDescription` / `ProductVisualIdentity`）的输出语言跟随请求的 `Language`；`BrandName`、`ColorPalette` 与语言无关。

### 自定义变量（仅 auto 模式）

| 参数 | 说明 |
|------|------|
| `--custom-variable TYPE DESC` | 自定义变量条目，格式 `Type Description`（如 `--custom-variable MaterialKeyword '材质关键词'`），可重复 |

> 让服务在标准变量之外再额外提取您指定的字段。`Type` 用 PascalCase；不可与 `UserPrompt` 同名；同请求内不可重名。自定义变量需配合个性化模板使用。

### 输出参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--output-bucket` | `TENCENTCLOUD_COS_BUCKET` | 输出 COS Bucket |
| `--output-region` | `TENCENTCLOUD_COS_REGION` | 输出 COS Region |
| `--output-dir` | `/output/poster_suite/` | 输出目录 |

### 任务控制

| 参数 | 说明 |
|------|------|
| `--no-wait` | 只提交任务，不等待结果（返回 TaskId 后退出） |
| `--poll-interval` | 轮询间隔秒数（默认 10） |
| `--timeout` | 最长等待时间秒数（默认 1800，即 30 分钟） |
| `--dry-run` | 模拟执行，打印请求 payload 不实际调用 API |
| `--region` | MPS API 接入地域（默认读取 `TENCENTCLOUD_API_REGION`，否则 `ap-guangzhou`） |

---

## 强制规则

0. **职责边界**：本脚本仅处理"批量生成多张海报 panel"的场景（用户同时表达"商品图 + 平台 + 主题/多张"意图）。以下情况应改用其它脚本：
   - "用 AI 生成一张海报/产品海报" → `mps_aigc_image.py`（AIGC 文生图）
   - "商品图换背景/做成电商风格" → `mps_image_bg_fusion.py`（背景融合）
   - "海报图片超分/降噪/提升清晰度" → `mps_imageprocess.py`（图片处理）

1. **`--definition` 必填**，取值 `50-55`，对应不同电商平台。
2. **`--recipe` 必填**，至少 1 条；单主题 Num 取值 `1-4`；全部 panel 总数（sum(Num)）取值 `4-12`。
3. **`Theme` 必须在标准列表内**：`hero` / `selling` / `scene` / `detail` / `angles` / `atmosphere`。
4. **modify 模式必须回填 auto 获得的所有标准变量（9 个，不可只传子集）**：先执行 auto 模式 → 从响应 `[0].Output.Content` 解析变量回显 → 修改某些字段值后，**全部塞回** ExtPrompt（标准变量 Role 见上表）。缺失任一标准变量会报错退出。
5. **`--custom-variable` 仅 auto 模式可用**，modify 模式传入会报错。
6. **UserPrompt 整请求至多 1 条**：`--ext-prompt UserPrompt` 与 `--user-prompt` 不可同时使用。
7. **附加商品视角图最多 3 张**（`--image-url` + `--image-cos-key` 总数）。
8. URL 输入需公网可访问；COS 输入需确保 MPS 服务有权限读取对应 Bucket 的文件。
9. 任务 `Status=FINISH` 不等于成功，需同时检查 `ErrMsg` 是否为空。
10. 脚本默认等待任务完成；若只需提交获取 TaskId，加 `--no-wait`。
11. 手动查询套图生成任务状态使用 `mps_get_image_task.py`，不要用 `mps_get_video_task.py`。
12. **auto → modify 迭代工作流**：先 auto 拿响应 → 从 `[0].Output.Content` 解析变量回显 → 修改字段后塞回 modify 请求的 `AddOnParameter`。
13. **modify 迭代时务必用 `--output-dir` 指定与 auto 不同的输出目录**：默认输出目录为 `/output/poster_suite/`，若 modify 不改 `--output-dir`，panel 文件名相同（如 `hero_0.png`）会**覆盖** auto 的结果。建议 auto 用 `/output/poster_suite_auto/`、modify 用 `/output/poster_suite_modify/`。

---

## 示例命令

```bash
# Auto 模式（最少必填）：商品图 URL + Definition + Recipe
python3 scripts/mps_image_poster_suite.py \
    --product-url "https://example.com/product.jpg" \
    --definition 50 \
    --recipe hero:2 --recipe detail:2 \
    --output-dir /output/poster_suite_auto/

# Auto 模式 + 用户文案变量 + 自定义变量
python3 scripts/mps_image_poster_suite.py \
    --product-url "https://example.com/product.jpg" \
    --definition 50 \
    --recipe hero:2 --recipe detail:2 \
    --panel-ratio 3:4 --panel-resolution 2K \
    --ext-prompt BrandName AURASKIN \
    --ext-prompt Headline "持续焕活" \
    --user-prompt "瓶身 32cm，强调按压泵与磨砂质感" \
    --custom-variable MaterialKeyword "材质关键词"

# Auto 模式 + 附加商品视角图（3 张）
python3 scripts/mps_image_poster_suite.py \
    --product-url "https://example.com/product.jpg" \
    --image-url "https://example.com/view1.jpg" \
    --image-url "https://example.com/view2.jpg" \
    --image-url "https://example.com/view3.jpg" \
    --definition 50 \
    --recipe hero:2 --recipe selling:2 --recipe detail:2

# Auto 模式 + 英文文案
python3 scripts/mps_image_poster_suite.py \
    --product-url "https://example.com/product.jpg" \
    --definition 51 \
    --recipe hero:2 --recipe detail:2 \
    --language en-US \
    --ext-prompt BrandName AURASKIN \
    --ext-prompt Headline "Revitalize Your Skin"

# Modify 模式（基于上一次 auto 结果迭代，必须回填所有 9 个标准变量，--output-dir 与 auto 不同避免覆盖）
python3 scripts/mps_image_poster_suite.py \
    --product-url "https://example.com/product.jpg" \
    --definition 50 \
    --recipe hero:2 --recipe detail:2 \
    --mode modify \
    --output-dir /output/poster_suite_modify/ \
    --ext-prompt BrandName AURASKIN \
    --ext-prompt Headline "敏感肌也能用的高效精华" \
    --ext-prompt SellingPointsText "保湿 / 紧致 / 抗氧化" \
    --ext-prompt ProductCategory "美妆-护肤" \
    --ext-prompt ProductVisualIdentity "matte glass dropper bottle, amber" \
    --ext-prompt TextureDescription "silky cream" \
    --ext-prompt ColorPalette "#F5C2C7,#A8DADC,#F1FAEE" \
    --ext-prompt TargetAudience "都市白领女性 22-35 岁" \
    --ext-prompt SceneContext "晨间梳妆台" \
    --user-prompt "Headline 字号再加大一档"

# 商品图使用 COS 路径输入
python3 scripts/mps_image_poster_suite.py \
    --product-cos-key "/input/product.jpg" \
    --definition 50 \
    --recipe hero:2 --recipe detail:2

# 只提交任务，不等待结果（返回 TaskId）
python3 scripts/mps_image_poster_suite.py \
    --product-url "https://example.com/product.jpg" \
    --definition 50 --recipe hero:2 --recipe detail:2 --no-wait

# 模拟执行，打印请求 payload 不调用 API
python3 scripts/mps_image_poster_suite.py \
    --product-url "https://example.com/product.jpg" \
    --definition 50 --recipe hero:2 --recipe detail:2 --dry-run

# 手动查询套图生成任务状态
python3 scripts/mps_get_image_task.py --task-id <TaskId>
```

---

## 输出示例

任务完成后输出 JSON：

```json
{
  "TaskId": "2600007696-WorkflowTask-xxxxxxxx",
  "Status": "FINISH",
  "CreateTime": "2026-07-06T10:00:00Z",
  "FinishTime": "2026-07-06T10:05:00Z",
  "VariableEcho": {
    "ExtPrompt": [
      {"Role": "BrandName", "Prompt": "AURASKIN"},
      {"Role": "Headline", "Prompt": "持续焕活"},
      {"Role": "SellingPointsText", "Prompt": "保湿 / 紧致 / 抗氧化"}
    ]
  },
  "Panels": [
    {
      "theme_label": "hero_0",
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/poster_suite/hero_0.jpg",
      "cos_uri": "cos://mps-bucket-125xxx/output/poster_suite/hero_0.jpg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/poster_suite/hero_0.jpg"
    },
    {
      "theme_label": "hero_1",
      "bucket": "mps-bucket-125xxx",
      "region": "ap-guangzhou",
      "path": "/output/poster_suite/hero_1.jpg",
      "cos_uri": "cos://mps-bucket-125xxx/output/poster_suite/hero_1.jpg",
      "url": "https://mps-bucket-125xxx.cos.ap-guangzhou.myqcloud.com/output/poster_suite/hero_1.jpg"
    }
  ]
}
```

### 响应结构说明

- `ImageProcessTaskResultSet[0].Output.Content`：JSON 字符串，反序列化后即一个 `AddOnParameter` 结构，可直接挂到下一次 modify 请求的 `AddOnParameter` 上做迭代。
- `ImageProcessTaskResultSet[1..N].Output.Path`：图片落地的存储位置。
- `ImageProcessTaskResultSet[1..N].Output.Content`：`{Theme}_{Index}` 标签，便于区分主题与位次。

---

## API 参考

| 接口 | 说明 |
|------|------|
| `ProcessImage` | 提交套图生成任务，`ImageTask.AiPosterSuiteConfig` |
| `DescribeImageTaskDetail` | 查询任务状态与输出结果 |

官方文档：
- [ProcessImage](https://cloud.tencent.com/document/product/862/112896)
- [DescribeImageTaskDetail](https://cloud.tencent.com/document/api/862/118509)
