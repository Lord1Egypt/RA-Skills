# MCP 回写映射（Write-back Mapping）

本文件把「分析结论 / 优化点」映射到具体的建站 MCP 工具调用，并列明强制约束。仅当第 1 步已拿到 MCP 地址 + Token 且 `test` 通过后才可调用写工具。

> 表单底层结构（`FnGetCustomForm`、`field.FieldType`、校验/提交 JS）与建站模板语法见本技能 `references/customform-democode-base.md` 与 `references/mcp-tools.md`（已随技能附带）。编辑前**必须**读取并遵守其中的强制规则。

## 1. 分析阶段用到的查询工具（只读，认证后可直接调用）

| 目的 | 工具 | 关键参数 |
| --- | --- | --- |
| 连通性 | `test` | `{message}` |
| 页面清单 | `list_page` | `{keyword?, page?, pageSize?}`（最大 500） |
| 页面源码 | `get_page_info` | `{pageId}`（仅 AI 自定义页 `PageType=99`，返回 `SourceCode`） |
| 普通表单清单 | `list_custom_form` | 无（返回 `ID`+`Name`，`FormType=CustomForm`） |
| 询盘表单 ID | `get_enquiry_form_id` | 无（首次可能自动初始化，调用前说明并取得同意） |
| 历史询盘记录 | `list_enquiry_records` | `{keyword?, status?(-1/0/1), page?, pageSize?}`（只读；分析阶段反推漏点） |
| 产品清单 | `get_product_list` | `{classId?, keyword?, page?, pageSize?}` |
| 产品详情 | `get_product_info` | `{productId}` |


> 改已有页面/表单前，必须先 `get_page_info` / `list_custom_form` 读取现状，禁止凭渲染后 HTML 当源码。

## 2. 优化点 → 写工具映射

| 优化动作 | 落到的工具 | 备注 |
| --- | --- | --- |
| P1/P2/P3/P4/P5/P6/P7 页面区块/CTA/信任/FAQ/页头拨打 | `save_ai_page` | `pageId` 正数=更新；`html`=完整源码；写前展示差异 |
| 新建普通表单（站点尚无合适表单时） | `add_custom_form` | 固定 `FormType=CustomForm`；参数详见 §5 |
| F1/F2/F3/F4/F5/F6/F7/F9 普通表单字段与属性调整 | `edit_custom_form` | 仅改 `FormType=CustomForm`；字段类型/必填/校验见 `references/customform-democode-base.md` 与 §5 |
| F8 询盘表单接 `EnquiryProduct` | 后台 + `get_enquiry_form_id` | 产品页询盘页接系统询盘表单，固定 `EnquiryProduct` 必填 |
| F10 删字段 | `edit_custom_form`（high，确认后） | `deleteFieldIds` 传字段 ID 数组；`NoDel=1` 字段禁止删；有提交记录时仅隐藏不物理删 |
| R1/R2/R3 产品信息补全/询价入口 | `edit_product` | `productId` 必填；`summary`/`content`/`mainImage` 部分更新 |
| 改完清缓存 | `clear_site_cache` | 说明并确认 |

## 3. save_ai_page 强制约束

- 改前必须 `get_page_info` 取 `SourceCode`，基于源码改，**禁止**用 HTTP 渲染后的页面当基础代码。
- **严禁改动 `{{}}` / `{%%}` 数据标签及其上下文逻辑**：`{{ ... }}`（含 `{{DataTag.sys.*}}`、`FnGet*`、`|raw`、变量取值）与 `{% ... %}`（控制语句 `if`/`for`/`block` 等）一律**原样保留**，不得删除、改写、挪位、合并或重排其所在元素上下文（包裹它们的容器、循环/条件父子结构）。只允许在标签/区块外部做获客相关的 HTML/CSS/JS 追加，或改与数据无关的静态文本/样式/布局；涉及数据标签的文案只能改标签之外的静态文案，不能改标签本身或其求值逻辑。
- 控制语句 `{% if %}`/`{% for %}` 只放完整 HTML 元素外部，禁止写进标签属性或 `<title>`。
- CSS 用清晰唯一的类名前缀，避免影响既有页面。
- 多表单页面各表单样式/校验/JS 隔离。
- 写前展示：新建 or 更新、pageId、名称、友好 URL、是否可能替换首页。

## 4. 表单编辑强制约束（普通 + 询盘）

- 普通表单：`list_custom_form` 展示 `ID`+`Name` → 用户选定 → 再 `edit_custom_form`；联系页表单 ID 与询盘表单 ID 不得相同。
- 以本技能 `references/customform-democode-base.md` 为基础，**必须完整保留表单相关 JS 逻辑，禁止删除或简化替换**，至少包含（但不限于）：
  - **验证码逻辑**：图形/短信验证码、滑块等的触发、刷新、校验流程；
  - **必填项校验逻辑**：`isrequire` / `validatetype` 等字段校验规则与错误提示；
  - **文件上传逻辑**：`enctype="multipart/form-data"`、图片/文件/多图控件的上传、预览、回显；
  - **地区联动逻辑**：省/市/区三级联动的加载与联动刷新；
  - **表单提交逻辑**：AJAX/无刷新提交、隐藏提交字段、`action`/`method`、`onsubmit` 拦截、成功/失败回调；
  - 另须保留隐藏提交字段、`action`、`enctype`、字段元数据、校验脚本、AJAX 提交整体不被简化版 HTML 替换。
- 字段类型用平台规定控件（单行/多行/单选/下拉/多选/图片/文件/多图/地区/日期时间/静态文本）。
- 改字段后先 `list_custom_form`/`get_enquiry_form_id` 复核，必要时 `clear_site_cache`。

## 5. 表单写回工具参数详解（add_custom_form / edit_custom_form）

两个工具都只作用于 `FormType=CustomForm` 的普通自定义表单，**不能**修改在线询盘表单（询盘表单用 `get_enquiry_form_id`）。均为写入工具，调用前必须向用户展示目标、字段、通知/支付影响并取得明确确认。完整参数以 `references/mcp-tools.md` 为准，这里列出获客优化最常改动的参数。

### 5.1 add_custom_form（新增普通表单）

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `name` | 是 | 表单名称，1–50 字符 |
| `intro` | 否 | 表单介绍，≤200 字符 |
| `enableEmailNotification` / `enableSmsNotification` / `isPay` / `payType` | 否 | 取值 `0`/`1`，默认 `0` |
| `receivedEmail` | 否（启用邮件通知时必填） | 邮件通知接收地址，多地址用换行/分号/逗号分隔，最多 10 个 |
| `payAmount` | 否 | 非负数字 |
| `payTips` | 否 | 支付提示语 |
| `calculations` | 否 | 表单计算配置字符串，可引用字段临时 ID |
| `fields` | 否 | 字段数组，顺序决定 `ShowOrder`；默认空 |

**字段对象 `fields[]`**（新增字段 `id` 必须以 `New` 开头，如 `NewName`，不能用数字 ID）：

| 字段参数 | 说明 |
| --- | --- |
| `name` | 必填，字段名称，1–50 字符 |
| `fieldType` | `1` 单行文本 / `2` 多行文本 / `3` 单选 / `4` 下拉 / `5` 多选 / `6` 图片 / `7` 地区 / `8` 时间 / `9` 文件 / `10` 多图 / `11` 静态文本 |
| `isRequire` | `0`/`1`，是否必填 |
| `validateType` | `0` 不验证 / `1` 文本 / `2` 数字 / `3` 手机 / `4` 固话 / `5` 固话或手机 / `6` 邮箱 / `7` 身份证（仅文本/多行文本有效，其他字段必须为 `0`） |
| `fieldValues` | 单选/下拉/多选选项，用 `\|` 或换行分隔 |
| `isSmsValidate` | `1` 仅适用于 `fieldType=1` 且 `validateType=3` 的手机字段，并自动置必填 |
| `intro`/`placeholder`/`icon`/`extendName` | 可选字符串 |
| `isShow`/`isSmsValidate`/`isShowTitle`/`pcShowType`/`mobileShowType` | 可选，`0`/`1` |
| `fieldValuesRel`/`calculationsItem` | 可选，选项联动/字段计算，可传 JSON 字符串、对象或数组 |

> 限制：表单创建与字段写入不是跨调用事务，失败不会自动回滚，失败后用 `list_custom_form` 复核实际状态。创建后页面接入必须用 `FnGetCustomForm(表单ID)`，不得猜测 ID。

### 5.2 edit_custom_form（修改已有表单 / 字段 / 删字段）

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `formId` | 是 | 当前站点普通自定义表单 ID，正整数或正数字符串 |
| `name` / `intro` / `enableEmailNotification` / `enableSmsNotification` / `receivedEmail` / `isPay` / `payAmount` / `payTips` / `payType` / `calculations` | 否 | 仅提交需要修改的表单主体字段 |
| `fields` | 否 | 带数字 `id`=更新已有字段；带 `New` 开头临时 ID 或不带 `id`=新增字段；顺序决定本次 `ShowOrder`；未列出的已有字段保持不变 |
| `deleteFieldIds` | 否 | 要删除的字段 ID 数组；字段不能同时出现在 `fields` 与 `deleteFieldIds` |

**删除语义**：`NoDel=1` 的字段禁止删除；无提交记录时物理删除，有提交记录时仅置 `IsShow=0` 隐藏以保留历史数据；未列入 `deleteFieldIds` 的字段不会被删除。

> 限制：更新/字段/删字段不是跨调用事务，失败不回滚，失败后必须 `list_custom_form` 复核。字段配置、字段类型、校验类型、临时 ID 规则与 `add_custom_form` 完全相同。

## 6. 典型回写片段示例（页面追加 CTA 区块）

在已有 AI 页源码合适位置（首屏结尾 / 页尾前）插入：

```html
<!-- 获客优化：主 CTA 区块（P1） -->
<section class="lead-cta">
  <h2>获取专属报价方案</h2>
  <p>留下联系方式，资深顾问 1 对 1 为您定制。</p>
  <a class="btn-lead" href="#contact">免费获取报价</a>
</section>
<style>
.lead-cta{text-align:center;padding:48px 16px;background:#0f1f17;}
.lead-cta h2{color:#e8c87a;font-size:28px;margin:0 0 12px;}
.btn-lead{display:inline-block;margin-top:16px;padding:14px 32px;background:#1faa6b;color:#fff;border-radius:8px;font-weight:600;}
</style>
```

> 该片段为获客新增内容，不触碰现有数据标签；深色奢华风配色（深底 + 绿/金）可按站点主题调整。改后 `save_ai_page` 并 `clear_site_cache`。
