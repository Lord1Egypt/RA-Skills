---
name: taobao-native
version: 1.0.41
description: "Shopping assistant via Taobao Desktop client. Use when the user needs to search products, view details, add to cart, place orders, check orders, request shipping, or perform any Taobao/Tmall shopping operation."
description_zh: "通过淘宝桌面客户端完成购物相关操作。当用户需要搜索商品、查看详情、加入购物车、下单购买、查看订单、催发货、开发票等淘宝/天猫购物操作时使用。"
metadata:
  openclaw:
    requires:
      anyBins:
        - taobao-native
      config:
        - "%APPDATA%/taobao/install-location.txt"
        - "~/Library/Application Support/taobao/cli/taobao-runner"
    os:
      - windows
      - macos
---

# 淘宝桌面客户端购物助手

## 适用场景

当用户的任务涉及以下购物相关操作时，**必须通过 taobao-native CLI 调用桌面客户端工具**：

- 搜索商品、比价
- 查看商品详情（价格、店铺、图片）
- 加入购物车
- 查看/管理订单（催发货、开发票等）
- 查看浏览历史、收藏
- 通过旺旺与商家聊天
- 任何涉及淘宝、天猫的页面操作

---

## ⚠️ 核心规则（必须遵守）

### 1. 价格场景必须获取真实SKU价格

**凡涉及商品价格的场景（比价、找最便宜、价格排序等），都必须进入商品详情页获取真实SKU价格！**

**原因**：搜索结果价格 / 页面默认价格 ≠ 真实SKU价格
- 搜索结果价格往往是**最低规格/配件的起步价**
- 页面显示的"￥xxx起"是**默认起步价**，非目标规格真实价格
- **实测案例**：爱奇艺黄金会员年卡，搜索显示￥88，点击年卡SKU后真实价格￥135

### 2. 价格获取的等待时间

**点击SKU后必须 `sleep 3` 秒！**

价格元素是异步刷新的，点击SKU后需等待价格异步刷新完成，**不可省略等待时间**。

### 3. SKU点击必须用 index 精确点击

**禁止用 `click_element --args '{"text":"xxx"}'` 点击SKU！**

原因：SKU文本可能有重复（如"年卡"和"年卡推荐"），text匹配会点击第一个。

正确做法：`scan_page_elements` 获取完整DOM → 找精确 index → `click_element --args '{"index":N}'`

---

## `taobao-native` 命令不可识别时的处理规则

当 `taobao-native` 命令无法识别或调用失败（如 `command not found`）时，按操作系统分别处理：

### Windows
1. 查看 %APPDATA%\taobao\install-location.txt 中的程序安装目录 {location} ，使用cmd: `{locatoin}\bin\taobao-native.cmd` 或者 bash：`{locatoin}\bin\taobao-native` （这是 taobao-native 这个path实际指向的路径）进行命令调用；
2. 若仍然失败，尝试：每次执行 taobao-native 指令前，都先刷新当前会话的 `Path` 环境变量，具体刷新方法需根据实际情况决定，示例：
   ```powershell
   $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
   ```
3. 如果仍然失败，则提示用户：`需要重启当前Agent，以识别新添加的指令`
4. 提示后立即停止任务，不再继续尝试其他操作

### macOS
1. 调用 `open -a /Applications/淘宝桌面版.app` 尝试打开，若失败，提示可以帮用户下载安装，若成功，执行2～6
2. 重新尝试执行 taobao-native。
3. 若仍然失败，使用 `~/Library/Application\ Support/taobao/cli/taobao-runner` 进行命令调用（这是软链所指向的完整路径）
4. 若仍然失败，将安装器写入的 bin 目录追加到当前会话 PATH：
   ```bash
   export PATH="$HOME/Library/Application Support/taobao/cli/bin:$PATH"
   ```
   然后重试 taobao-native
5. 如果仍然失败，则提示用户：`需要重启当前Agent，以识别新添加的指令`
6. 提示后立即停止任务，不再继续尝试其他操作

## 调用协议（强制执行）

使用本机已安装的 **taobao-native** 命令（淘宝桌面版 CLI），格式：

```bash
taobao-native <工具名> --args '<JSON 参数>'
```

### Shell 环境要求

#### 调用方式（按优先级）

**方式 1：Bash—— 最可靠**

Bash 中单引号原样传递
```bash
taobao-native add_to_cart --args '{"sku":["50g 【抗皱饱满】"],"sourceApp":"Qoderwork"}'
```

**方式 2：`--request <文件>` —— 任何 Shell 通用，推荐非 Bash 环境使用**

参数在文件中以 UTF-8 读取，完全绕过 Shell 和 `.cmd` 的参数处理：
```
# request.json 内容：{"tool":"add_to_cart","arguments":{"sku":["50g 【抗皱饱满】"],"sourceApp":"Qoderwork"}}
taobao-native --request request.json -o result.json
```

**方式 3：CMD / PowerShell 直接传参**

```powershell
# PowerShell
powershell -Command 'taobao-native add_to_cart --args ''{"sku":["50g 【抗皱饱满】","混合偏干性肤质 轻润版"],"sourceApp":"Qoderwork"}'' -o "C:\Users\admin\.qoderwork\workspace\mnpnvqeasd3hwtn3\add_cart.json"'
```

### 重要规则

**所有工具调用必须传入 `sourceApp` 参数**，用于标识调用来源的 AI 应用名称。例如：

```bash
taobao-native navigate --args '{"page":"home","sourceApp":"Qcoderwork"}'
taobao-native search_products --args '{"keyword":"iPhone","sourceApp":"openClaw"}'
```

`sourceApp` 值根据当前 AI 客户端确定，如：`Qcoderwork`、`openClaw`、`copaw` 等。

### 第一步：查看工具帮助

本 Skill 文档中的「工具速查」已包含常用工具的完整说明，**优先参考本文档直接调用**。仅在以下情况使用 CLI **`--help`**：

- 工具参数不确定，或者工具返回错误时：`taobao-native --help <工具名>` 或 `taobao-native <工具名> --help`，查看最新用法
- 需确认最新可用工具时：`taobao-native --help`（或 `-h`）列出全部工具

```bash
taobao-native --help
taobao-native --help open_chat
taobao-native open_chat --help
```

## 典型工作流

1. `navigate` / `navigate_to_url` — 导航到目标页面
2. `read_page_content` — 读取页面可见文本（用 scope 限定范围）
3. `scan_page_elements` — 扫描可交互元素（用 filter 过滤）
4. `click_element` / `input_text` — 执行交互

> **⚠️ 避免截断**：返回数据量较大时（如 `search_products` 通常 50+ 条），环境可能将 stdout 截断显示为 `...(truncated)`。**必须对可能返回大量数据的工具使用 `-o <文件>`**，将完整结果写入文件，stdout 仅输出摘要（含 `resultFile` 绝对路径）。拿到 `resultFile` 后读取该文件获取完整 JSON。
> - **推荐**：`taobao-native search_products --args '{"keyword":"连衣裙"}' -o result.json`，再读取 `result.json`
> - 其他易产生大结果的工具（如 `read_page_content`、`scan_page_elements` 未加 filter）也建议加 `-o`
> - **`-o` 路径须可写且在授权范围内**：在 Agent / 沙箱等受限环境中，**必须使用当前工作区或环境允许写入的目录**（如任务给出的 `workspace` 绝对路径下的文件）。相对路径需保证 cwd 落在该范围内；若出现 `OUTSIDE_AUTHORIZED_ROOT` 或写入被拒，改为 **` -o "<workspace 下的绝对路径>.json"`** 再试。

## 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| 点击元素失败 | 页面未加载完成 | 等待后重试 |
| SKU 选择失败 | sku 参数格式不对 | 使用返回的精确文本 |
| 读取内容为空 | 页面还在加载 | 等待后再读取 |
| 找不到元素 | 页面已变化 | 重新扫描页面 |
| 连接失败 / error | 桌面版未启动 | 先启动淘宝桌面版或等待 CLI 自动拉起 |
| **误以为返回为空** | 输出被截断显示 `...(truncated)` | **调用时加 `-o result.json`**，从 stdout 的 resultFile 路径读取完整 JSON |
| **`OUTSIDE_AUTHORIZED_ROOT` / 写入被拒** | `-o` 指向了沙箱或策略不允许的路径 | 将输出文件改到**当前任务 workspace（或环境允许）下的绝对路径**，例如 `-o "D:\\…\\workspace\\cart_result.json"` |
| 价格错误 | sleep 时间不够 | 点击SKU后 **sleep 3秒** |
| SKU点击错误 | 用 text 匹配 | 用 **index** 精确点击 |
| **JSON 解析错误**（含中文 `【】` 等字符） | Windows `.cmd` 剥离双引号破坏 JSON 结构 | **优先用 Bash**；否则用 `--request <文件>` 传参 |

---

## 工具速查

### 帮助（CLI，非页面工具）

| 命令 | 用途 | 说明 |
|------|------|------|
| `--help` / `-h` | 列出当前可用工具及 `description` / `inputSchema` |  |
| `--help <工具名>` | 当工具返回错误时，帮助排查错误 |  |

### 启动

| 工具 | 用途 | 注意 |
|------|------|----------|
| launch | 启动淘宝桌面版 | macOS 下可用 `open "/Applications/淘宝桌面版.app"` 作为兜底 |

### 导航

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| list_available_pages | 获取所有可用页面名称和链接 | **不确定页面名称时先调用此工具** |
| navigate | 导航到淘宝预设页面 | page: 页面名称；**若 page 不在列表中将返回所有可用页面及链接，禁止自行编造 URL** |
| navigate_to_url | 打开已知有效的淘宝 URL | url（必须是淘宝/天猫等可信域名）；**禁止编造 URL，预设页面请使用 navigate 工具** |
| close_page | 关闭当前任务页面 | - |

### 页面读取

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| get_current_tab | 获取当前标签页 URL 和标题 | - |
| read_page_content | 提取页面可见文本 | scope?, maxLength?, offset? |
| scroll_page | 滚动页面 | direction: up/down/top/bottom, selector?, amount? |
| inspect_page | 诊断页面 DOM 状态（排查操作失败原因） | - |

### 页面交互

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| scan_page_elements | 扫描可交互元素，返回带序号的列表 | filter?, scope? |
| click_element | 点击元素 | index（序号，精确）或 text（文本，模糊匹配） |
| input_text | 输入文本 | text, index?, placeholder?, scope?, submit? |
| trigger_keyboard_event | 触发单个键盘事件（keydown/keyup/keypress） | key 或 keyCode, eventType?, ctrlKey?, altKey?, shiftKey?, metaKey? |
| trigger_key_sequence | 连续触发按键序列 | text（自动拆分字符）或 sequence（精细控制） |
| hold_keyboard_key | 长按某个键（keydown → 保持 → keyup） | key 或 keyCode, duration?, repeatEvents? |

### 搜索 & 商品

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| search_products | 文字搜索商品并返回结果列表 | keyword；type?（可选，默认 all：all=商品、shop=店铺、tmall=天猫商品、22pc_b=企业购、pc_taobao=淘宝；用户提到「店铺」「找店」「进店」等时优先 type=shop） |
| image_search | 以图搜图（淘宝相似商品）。【调用前准备】需先获取图片地址，推荐方式：1）从系统剪切板获取图片，判断是否与用户发送的图片相同；2）询问用户图片本地存储位置。支持三种图片输入格式：本地文件路径、CDN地址、base64数据。会自动点击页面上的图片分类小卡获取每个分类的商品列表 | imagePath（图片数据：1）本地绝对路径如 /tmp/xxx.jpg；2）CDN地址如 https://example.com/img.jpg；3）base64数据如 data:image/png;base64,xxx） |
| get_product_skus | **【加购前必调】** 获取商品 SKU 维度与可选规格列表 | itemId?（不传则使用当前商详页） |
| add_to_cart | 加入购物车（自动处理 SKU 选择和弹窗）。**必须先调用 `get_product_skus` 获取可选规格，再传入完整 sku 参数** | itemId?, sku（必须与页面 SKU 维度完全匹配） |
| get_browse_history | 获取浏览历史 | type: product/search/shop |
| submit_product_rating | 提交商品评价（自动填充表单并提交）。**【评价专用工具-唯一方式】评价页面内禁止使用 input_text、click_element、scan_page_elements 等工具！这些工具无法正确操作评价表单，必须使用本工具！** | qualityContent?(单商品评价内容)、qualityContents?(多商品评价内容数组，每个商品一条不同内容)、merDsr?(描述相符评分1-5)、serviceQualityScore?(卖家服务评分1-5)、saleConsignmentScore?(物流服务评分1-5)、isAppend?(是否追加评价)、serviceContent?(服务评价内容)、imageUrls?(图片路径数组)、gender?(1=男,2=女)、birthday?(格式YYYY-MM-DD)、anonymous?(是否匿名)、submit?(是否自动提交) |

### 旺旺聊天

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| open_chat | 【发消息必选】打开旺旺聊天并发送消息，复合工具自动完成全流程 | source(场景), message(消息内容), imagePath?(图片路径，支持单张或多张) |
| send_chat_message | 在已打开的旺旺页面中继续发消息，支持同时发送图片 | message(消息内容), imagePath?(单张路径、路径数组或JSON字符串数组), shopName?(切换店铺) |

**imagePath 参数说明：**
- 单张图片：`"/path/to/image.png"` 或 `"https://cdn.com/img.jpg"` 或 `"data:image/png;base64,..."`
- 多张图片（数组格式）：`["/path/img1.png", "/path/img2.png"]`
- 图文发送顺序：**先发图片（逐张）再发文字**，每张图片发送后等待弹窗确认

**open_chat 场景说明：**
- `source: cart` - 从购物车找商品发消息，需传 `productName`(商品关键词)
- `source: order` - 从订单列表找商品发消息，需传 `productName`(商品关键词)
- `source: search` - 搜索商品后给商家发消息，需传 `query`(搜索词)

**触发关键词：** 当用户提到"问问商家"、"旺旺"、"聊天"、"咨询"、"发消息"时，必须使用 `open_chat` 工具

### 键盘操作

| 工具 | 用途 | 关键参数 |
|------|------|----------|
| trigger_keyboard_event | 触发单个键盘事件 | key（键名）或 keyCode（数字）, eventType（keydown/keyup/keypress）, 修饰键（ctrlKey/altKey/shiftKey/metaKey） |
| trigger_key_sequence | 连续触发按键序列 | text（自动拆分字符）或 sequence（精细控制数组） |
| hold_keyboard_key | 长按某个键 | key/keyCode, duration（长按毫秒，默认500）, repeatEvents（是否重复触发keydown） |

**键盘操作使用说明：**

- **trigger_keyboard_event**：用于触发单个键盘事件
  - `key`：键名如 `"Enter"`、`"Escape"`、`"ArrowUp"`、`"ArrowDown"`、`"Backspace"`、`"Delete"`、`"Tab"`、`"Space"`、字母数字等
  - `keyCode`：数字键码，如 13(Enter)、27(Escape)、38(上箭头)
  - `eventType`：事件类型，`keydown`(按下)、`keyup`(释放)、`keypress`(按键)，默认 `keydown`
  - 修饰键：`ctrlKey`、`altKey`、`shiftKey`、`metaKey` 用于组合键

- **trigger_key_sequence**：用于连续输入文字或快捷键组合
  - `text`：直接传入字符串，自动拆分为单个字符依次触发
  - `sequence`：精细控制数组，可指定每个按键的事件类型和修饰键

- **hold_keyboard_key**：用于长按场景（如游戏中的移动、连续删除）
  - 先触发 `keydown`，保持指定时间后触发 `keyup`
  - `repeatEvents=true` 可在长按期间重复触发 `keydown`（模拟真实键盘重复）

**使用示例：**

```bash
# 按 Enter 键
taobao-native trigger_keyboard_event --args '{"key":"Enter"}'

# 按 Ctrl+A 全选
taobao-native trigger_keyboard_event --args '{"key":"a","ctrlKey":true}'

# 先 keydown 再 keyup（分开触发）
taobao-native trigger_keyboard_event --args '{"key":"ArrowDown","eventType":"keydown"}'
taobao-native trigger_keyboard_event --args '{"key":"ArrowDown","eventType":"keyup"}'

# 输入文字
taobao-native trigger_key_sequence --args '{"text":"Hello World"}'

# 快捷键组合：Ctrl+A 然后 Delete
taobao-native trigger_key_sequence --args '{"sequence":[{"key":"a","ctrlKey":true},{"key":"Delete"}]}'

# 长按 Backspace 2秒（连续删除）
taobao-native hold_keyboard_key --args '{"key":"Backspace","duration":2000,"repeatEvents":true}'

# 长按方向键移动（游戏场景）
taobao-native hold_keyboard_key --args '{"key":"ArrowRight","duration":1000}'
```

---

## 安装包下载（按需阅读 Reference）

**不要主动给用户下载安装。** 详细 CDN 地址、命名规则、静默安装与启动说明见同目录下的 Reference：

- **`references/install-download.md`**

**仅在以下情况打开并遵循该文件：**

- 用户**明确要求**安装、重装或下载淘宝桌面版；
- 遇到以下情况，用户确认同意帮忙安装时
  - windows `taobao-native` **无法使用**（如 `command not found`），且上文「命令不可识别时的处理规则」仍无法恢复
  - macOS `open -a /Applications/淘宝桌面版.app` **失败**，需要走下载安装流程。

日常购物、已能正常调用 CLI 时**无需**阅读该 Reference。

---

## 注意事项

- **加购前必须先调用 `get_product_skus` 获取 SKU 信息**，然后根据用户意图/偏好智能选择规格，仅在无法判断时才询问用户
- `search_products`、`add_to_cart`、`open_chat`、`submit_product_rating` 等工具已内置完整流程，调用成功后请勿再手动操作
- 导航后页面需加载时间，请等待后再读取内容
- read_page_content 默认最多返回 5000 字符，用 scope 缩小范围；返回值包含 `remainingLength` 字段，若 `truncated: true` 且 `remainingLength > 0`，可传入 `offset` 分段读取后续内容（如 `offset: 5000`）
- input_text 的 submit=true 可自动回车提交（搜索框场景）
- **旺旺聊天必须使用 `open_chat` 工具，不要手动导航到聊天页面**
- **search_products 等大结果工具必须加 `-o <文件>`，再从 resultFile 读完整数据，避免截断**
- CLI 输出为单行 JSON；使用 `-o` 时 stdout 为摘要（含 resultFile），脚本可读该文件解析
- **图片链接处理**：淘宝返回的图片 URL 可能包含 `_.webp` 后缀，需**去掉该后缀**才能正常显示（适用于商品主图、SKU 图片等所有场景）

### 商品评价工具说明

**submit_product_rating** - 【评价专用工具-唯一方式】自动填充并提交淘宝/天猫商品评价表单

**绝对禁止**：评价页面内禁止使用 input_text、click_element、scan_page_elements 等工具！这些工具无法正确操作评价表单，必须使用本工具！

**多商品必须差异化文案**：一个订单有多个商品时，每个商品的评价内容必须不同！禁止复制相同内容！

**使用流程：**
1. 第一步：调用本工具（不传qualityContent），获取商品数量和商品信息
2. 第二步：根据每个商品的名称、规格，为每个商品生成不同的评价内容
3. 第三步：再次调用本工具，传入 qualityContents 数组（每个商品一条不同的评价）

**参数规则：**
- 单商品：使用 qualityContent 参数
- 多商品：必须使用 qualityContents 数组，数组长度=商品数量，每个元素内容必须不同！

**评分必填：**首次评价必须填：merDsr(描述相符)、serviceQualityScore(卖家服务)、saleConsignmentScore(物流服务)，各1-5星。

**图片可选：**imageUrls 传入图片路径数组，所有商品共用这些图片。

**追加评价：**isAppend=true 时评分可不填。

**参数说明：**

| 参数 | 类型 | 说明 |
|------|------|------|
| qualityContent | string | 【单商品专用】单个商品的评价内容必填。仅当订单只有一个商品时使用。多商品时禁止使用此参数！ |
| qualityContents | string[] | 【多商品必填】多商品评价内容数组必填。要求：1.数组长度必须等于商品数量；2.每个元素必须是不同的评价内容，禁止重复！3.顺序与页面商品顺序一致。 |
| merDsr | number | 描述相符评分，1-5星（首次评价必填） |
| serviceQualityScore | number | 卖家服务评分，1-5星（首次评价必填） |
| saleConsignmentScore | number | 物流服务评分，1-5星（首次评价必填） |
| isAppend | boolean | 是否追加评价，默认false。追加评价时评分可不填 |
| serviceContent | string | 服务评价内容（评价服务） |
| imageUrls | string[] | 图片路径数组，最多5张。支持：本地文件路径、CDN地址、base64数据。所有商品共用这些图片。 |
| gender | number | 性别，1=男，2=女 |
| birthday | string | 生日/预产期，格式：YYYY-MM-DD，如2026-03-13 |
| anonymous | boolean | 是否匿名评价，默认为true |
| submit | boolean | 是否自动点击提交按钮，默认为true |

**使用示例：**

```bash
# 基础评价（只打星）
taobao-native submit_product_rating --args '{"merDsr":5,"serviceQualityScore":5,"saleConsignmentScore":5}'

# 带文字评价
taobao-native submit_product_rating --args '{"merDsr":5,"serviceQualityScore":5,"saleConsignmentScore":5,"qualityContent":"商品质量很好，非常满意","serviceContent":"卖家服务态度很好"}'

# 带晒图的评价
taobao-native submit_product_rating --args '{"merDsr":5,"qualityContent":"很好","imageUrls":["/tmp/xxx.jpg","/tmp/yyy.jpg"]}'

# 多商品评价（每个商品不同内容）
taobao-native submit_product_rating --args '{"merDsr":5,"serviceQualityScore":5,"saleConsignmentScore":5,"qualityContents":["商品A很好","商品B不错","商品C满意"]}'
```

---

## 场景示例

### 商品加购（完整流程）
- **目标**：将指定商品加入购物车。
- **CLI 调用链路**：
  1. `taobao-native get_product_skus --args '{"itemId":"<商品ID>"}'`：**【必须】** 先获取商品 SKU 维度与可选规格（含图片）
  2. 返回示例：`{"success":true,"hasSku":true,"availableSkus":[{"label":"颜色","options":[{"text":"黑色","image":"https://..."},{"text":"白色","image":"https://..."}]},{"label":"尺码","options":[{"text":"M"},{"text":"L"},{"text":"XL"}]}],...}`
  3. **智能选择 SKU**（按优先级判断）：
     - **情况A - 用户已表达意图**：若用户请求中已包含规格信息（如「加购黑色XL的T恤」「买大号的」），直接匹配 `availableSkus` 中对应的选项，自动填充 sku 参数
     - **情况B - 可推断用户偏好**：若上下文中能推断用户偏好（如历史对话提到喜欢某颜色、之前购买过某尺码），自动选择匹配的规格
     - **情况C - 无法确定**：仅当完全无法判断用户意图和偏好时，向用户展示可选规格，**必须同时展示 `image` 图片**（使用 Markdown 图片语法 `![颜色名](图片URL)`），帮助用户直观选择
  4. `taobao-native add_to_cart --args '{"itemId":"<商品ID>","sku":["黑色","XL"]}'`：传入完整 sku 数组加购
- **关键说明**：
  - `sku` 参数必须与页面 SKU 维度数量完全匹配，例如页面有「颜色」「尺码」两个维度，则必须传入两个值
  - 若 `get_product_skus` 返回 `hasSku: false`，说明商品无多规格，可直接调用 `add_to_cart` 不传 sku
  - 若 `get_product_skus` 返回 `allSelected: true`，说明页面规格已全选，可直接加购
  - 自动选择 SKU 时，若选择的规格无货（`disabled: true`），需告知用户并让其重新选择
  - **展示规格给用户时，必须将有图片的 SKU 选项以图文形式呈现**，例如：
    ```
    请选择颜色：
    1. ![黑色](https://img.alicdn.com/xxx.jpg) 黑色
    2. ![白色](https://img.alicdn.com/yyy.jpg) 白色
    ```
  - **⚠️ 图片链接处理**：SKU 图片 URL 如包含 `_.webp` 后缀，需**去掉该后缀**才能正常显示

### 获取商品真实SKU价格（比价场景）
- **目标**：获取商品详情页中**特定SKU规格的真实价格**，用于比价、价格排序等场景。
- **⚠️ 核心问题**：搜索结果价格 / 页面默认显示价格 ≠ 真实SKU价格
  - 搜索结果中的价格往往是**配件/最低规格的起步价**，不是主体商品价格
  - 直接读取页面显示的"￥xxx起"也是**默认起步价**，非目标规格真实价格
  - 例如：爱奇艺黄金会员年卡，搜索显示￥88，点击年卡SKU后真实价格￥135
- **唯一可靠的方法**：
  ```bash
  # 1. 打开商品页
  taobao-native navigate_to_url --args '{"url":"https://item.taobao.com/item.htm?id=xxx","sourceApp":"copaw"}'
  sleep 3  # 等待页面加载

  # 2. 获取SKU维度
  taobao-native get_product_skus --args '{"sourceApp":"copaw"}'

  # 3. 扫描完整DOM，找到目标SKU索引
  taobao-native scan_page_elements --args '{"sourceApp":"copaw"}' -o elements.json
  # 从DOM中找到目标SKU的精确 index

  # 4. 用 index 精确点击SKU（禁止用 text！）
  taobao-native click_element --args '{"index":80,"sourceApp":"copaw"}'

  # 5. ⚠️ 等待3秒让价格刷新（必须！）
  sleep 3

  # 6. 获取真实价格
  taobao-native scan_page_elements --args '{"filter":"￥","sourceApp":"copaw"}'
  ```
- **常见陷阱**：

  | 陷阱 | 表现 | 正确做法 |
  |------|------|---------|
  | 搜索价格≠真实价格 | 显示￥88，实际￥135 | 进详情页获取SKU真实价格 |
  | 价格未刷新 | sleep不够取到旧价 | **sleep 3秒** |
  | SKU点击错误 | text匹配点错SKU | 用 **index** 精确点击 |
  | read_page_content取错价 | 多个价格混淆 | 用 `scan_page_elements --args '{"filter":"￥"}'` |

### 商详获取主图图片
- **目标**：提取商品详情页的主图图片链接。
- **CLI 调用链路**：
  1. `taobao-native navigate_to_url --args '{"url":"<商详URL>"}'`：打开商详页
  2. `taobao-native read_page_content --args '{}'`：读取页面内容，返回值中 `[商品主图]` 和 `[商品图]` 标签已自动提取图片 URL，**无需指定 scope**
- **实测返回示例**：
  ```
  [商品图] https://img.alicdn.com/imgextra/.../O1CN01yyy.jpg
  ```
- **⚠️ 图片链接处理**：返回的图片 URL 需**去掉 `_.webp` 后缀**才能正常显示

### 评价查看与总结
- **目标**：查看并总结某个商品的用户评价。
- **CLI 调用链路**：
  1. `taobao-native navigate_to_url --args '{"url":"<商详URL>"}'`：进入商详
  2. `taobao-native click_element --args '{"text":"用户评价"}'`：点击评价 tab，`pageChanges.added` 会直接返回评价内容
  3. `taobao-native read_page_content --args '{}'`：读取完整页面，评价内容在「用户评价·N」之后；**商详页默认只展示约 2 条预览评价**
  4. （可选）`taobao-native click_element --args '{"text":"查看全部评价"}'`：如需查看更多评价，点击后会打开左侧评价抽屉面板（非 URL 跳转）
  5. （可选）`taobao-native read_page_content --args '{"scope":"[class*=Drawer]"}'`：读取抽屉中的全部评价内容（**约 20 条**，以实际页面为准）；可用 `taobao-native scroll_page --args '{"direction":"down"}'` 在抽屉内加载更多

### 购物车删除商品
- **目标**：在购物车中删除指定商品。
- **CLI 调用链路**：
  1. `taobao-native navigate --args '{"page":"cart"}'`：进入购物车
  2. `taobao-native input_text --args '{"text":"商品关键词","placeholder":"搜索购物车内商品","submit":true}'`：在购物车搜索框中搜索目标商品，筛选后只显示匹配的商品
  3. `taobao-native scan_page_elements --args '{}'`：**不传 filter**，扫描完整 DOM 树；搜索已大幅减少商品数量，完整树中商品名 `<a>商品标题</a>` 和删除按钮 `<div>删除</div>` 按顺序交替排列，可准确对应
  4. 根据 DOM 树中商品标题和规格信息（如 `颜色分类：冲牙器-绿色`），找到目标商品**紧跟其后**的 `<div>删除</div>` 对应索引
  5. `taobao-native click_element --args '{"index":<删除按钮索引>}'`：点击该商品的删除按钮（**无需先勾选复选框**）
  6. `taobao-native click_element --args '{"text":"删除"}'`或`taobao-native click_element --args '{"index":<确认索引>}'`：在确认弹窗中点击确认删除

### 商详旺旺聊天中发送商品链接
- **目标**：在商品详情页打开旺旺聊天，将商品（或右侧推荐商品）发送给商家。
- **CLI 调用链路**：
  1. `taobao-native navigate_to_url --args '{"url":"<商详URL>"}'`：打开商详页
  2. `taobao-native click_element --args '{"text":"联系客服"}'`：点击商详页底部「联系客服」，打开旺旺聊天页面
  3. `taobao-native scan_page_elements --args '{"filter":"发送"}'`：扫描右侧栏，返回例如：
     - `发送宝贝链接` — 发送当前正在咨询的商品
     - `发送商品`（多个） — 发送右侧「历史逛过」或「本店推荐」中的商品
     - 商品名 `<div>商品标题</div>` 紧跟在对应 `<div>发送商品</div>` **之前**
  4. `taobao-native click_element --args '{"index":<对应索引>}'`：点击「发送宝贝链接」或「发送商品」，商品链接自动发送到聊天中
- **实测 DOM 结构**：
  ```
  [146] <div>发送宝贝链接</div>          ← 当前咨询的商品
  [152] <div>商品A标题</div>             ← 历史逛过 / 本店推荐
  [153] <div>发送商品</div>              ← 点击发送商品A
  [156] <div>商品B标题</div>
  [157] <div>发送商品</div>              ← 点击发送商品B
  ```
- **关键说明**：
  - 右侧栏分为「正在咨询的宝贝」「本店订单」「历史逛过」「本店推荐」四个区域
  - 如需发送特定推荐商品，先从 DOM 中匹配商品标题，再点击其紧跟的 `发送商品` 按钮
