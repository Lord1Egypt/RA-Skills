---
name: travel-city-game
description: >
  根据用户输入的城市名，自动调用 flyai 搜索该城市的景点、体验、美食产品，
  然后生成一个游戏化的3节点叙事行程 H5 页面。每个节点包含 AI 生成的故事文案
  和飞猪真实预订链接。使用方式: /travel-city-game 城市名。
  当用户提到 "travel-city-game"、"生成行程"、"旅行叙事"、"游戏化行程"、
  想要为某个城市创建探索路线、或者想把旅游景点串成故事线时使用此 Skill。
  即使用户只是说"帮我生成XX城市的旅行路线"也应触发。
compatibility:
  requires:
    skills:
      - name: flyai
        install_hint: "Install from https://clawhub.ai/yealexchen/flyai or run: claude skill install flyai"
    bins:
      - python3
      - node
      - flyai
---

# City Game — AI 叙事行程生成器

将任意城市的真实旅游产品串联成一条游戏化叙事路线。玩家逐步解锁节点、预订真实飞猪产品、收集奖励，体验"剧情驱动"的旅行方式。

## 输入

用户提供一个城市名，如 `长沙`、`大理`、`厦门` 等。从用户消息中提取城市名，赋值给变量 `CITY`。

## 完整工作流程

### Step 0: 验证 flyai CLI 已就绪

本 Skill 依赖 `flyai` Skill 提供的 CLI 工具。`flyai` 必须由用户预先安装（不在运行时自动安装，以避免供应链安全风险）。

执行以下命令确认 flyai 可用：

```bash
flyai --help
```

如果命令不存在（返回 "command not found"），**停止执行并提示用户**：

> ⚠️ 未检测到 flyai CLI。请先安装 flyai Skill：
> - 方式一：访问 https://clawhub.ai/yealexchen/flyai 安装
> - 方式二：在终端执行 `claude skill install flyai`
>
> 安装完成后重新运行本 Skill。

**绝对不能在 Skill 流程中自动执行 `npm install` 安装 flyai**——这会引入未经用户确认的第三方代码，存在供应链安全风险。同样，**绝对不能跳过 flyai 搜索直接编造数据。**

#### API 限流处理

在后续 Step 1 的搜索过程中，如果 flyai 返回了限流相关的错误（如 HTTP 429、"rate limit"、"quota exceeded" 或返回结果为空且提示频率过高），**停止继续请求并提示用户获取专属 API Key**：

> ⚠️ flyai API 请求被限流，免费额度可能已用尽。请按以下步骤获取 API Key：
> 1. 登录 https://flyai.open.fliggy.com/
> 2. 注册/登录后在控制台获取你的专属 API Key
> 3. 将 API Key 配置到环境变量：`export FLYAI_API_KEY="你的Key"`
> 4. 配置完成后重新运行本 Skill

设置好 API Key 后，flyai CLI 会自动使用该 Key 进行认证，不再受公共限流约束。

### Step 1: 用 flyai CLI 搜索 3 类旅游产品

#### 安全执行 flyai 命令（避免 Shell 注入）

⚠️ **严禁直接将 CITY 变量拼接到 Bash 命令字符串中执行**。必须使用以下安全方式：

**方式一：使用 Python 子进程调用（推荐，最安全）**

用 Python 执行 flyai 命令，参数作为列表传递（不经过 Shell 解析）：

```python
import subprocess, json

def flyai_search(args):
    """安全调用 flyai CLI，参数作为列表传入，Shell 无法解析特殊字符"""
    result = subprocess.run(
        ["flyai"] + args,
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    return json.loads(result.stdout)

# 示例：搜索历史古迹
data = flyai_search(["search-poi", "--city-name", CITY, "--category", "历史古迹"])
```

**方式二：如果必须用 Bash，使用单引号包裹所有变量**

```bash
# 使用单引号包裹 CITY 和其他参数值，防止 Shell 解析
flyai search-poi --city-name 'CITY' --category '历史古迹'
```

> ⚠️ 方式二仍有风险（如果 CITY 本身包含单引号），优先使用方式一。

**绝对禁止的做法**：
```bash
# ❌ 危险！CITY 如果包含 " 或 ; 等字符会导致命令注入
flyai search-poi --city-name "CITY" --category "历史古迹"
```

---

使用上述安全方式执行以下 flyai 搜索。每条命令返回 JSON 到 stdout。

**重要：两种命令的返回结构不同：**

- `search-poi` 返回: `data.itemList[].{name, address, mainPic, jumpUrl, ticketInfo.ticketName}`
- `keyword-search` 返回: `data.itemList[].info.{title, picUrl, jumpUrl, price, tags}`

---

**搜索 A — 节点1（文化探索）：历史/文化景点**

首选命令（使用单引号）：
```bash
flyai search-poi --city-name 'CITY' --category '历史古迹'
```

如果返回结果少于 2 个，依次尝试：
```bash
flyai search-poi --city-name 'CITY' --category '人文古迹'
flyai search-poi --city-name 'CITY' --category '博物馆'
flyai keyword-search --query 'CITY 著名景点门票'
```

从结果中选 **1 个最佳产品**，提取字段：
- `skuName`: 来自 `name`（search-poi）或 `info.title`（keyword-search）
- `jumpUrl`: 来自 `jumpUrl`（search-poi）或 `info.jumpUrl`（keyword-search）
- `picUrl`: 来自 `mainPic`（search-poi）或 `info.picUrl`（keyword-search）
- `address`: 来自 `address`（search-poi）或自行根据产品名推断（keyword-search 无 address 字段）

---

**搜索 B — 节点2（特色体验）：演出/体验/特色项目**

首选命令（使用单引号）：
```bash
flyai keyword-search --query 'CITY 特色体验 演出'
```

如果返回结果不理想，依次尝试：
```bash
flyai keyword-search --query 'CITY 非遗体验'
flyai search-poi --city-name 'CITY' --category '演出赛事'
flyai keyword-search --query 'CITY 休闲玩乐'
```

从结果中选 **2 个产品**（主产品 + 备选产品，备选用于 Step 4 意外引擎）。

---

**搜索 C — 节点3（美食收官）：美食/夜游/特色民宿**

首选命令（使用单引号）：
```bash
flyai keyword-search --query 'CITY 美食体验'
```

如果返回结果不理想，依次尝试：
```bash
flyai keyword-search --query 'CITY 夜游'
flyai keyword-search --query 'CITY 特色民宿'
flyai keyword-search --query 'CITY 网红餐厅'
```

从结果中选 **1 个最佳产品**。

---

### Step 2: 验证所选产品

确认每个所选产品都满足以下条件（必须全部满足）：
- `jumpUrl` 存在且为有效 URL（非空字符串）
- `picUrl` 存在且为有效图片 URL
- `skuName` 非空且有地域特色

如果某个产品不满足，从同一搜索结果中选择下一个产品，或换关键词重新搜索。

### Step 3: 为每个节点生成叙事故事

为 3 个节点分别撰写沉浸式第二人称故事文案（80-120 字），格式要求：

- 使用第二人称"你"作为主角
- 包含场景描写和感官细节（视觉、听觉、味觉、触觉至少 2 种）
- 包含一个 NPC 角色的对话（如守门大爷、老板娘、茶馆掌柜、夜市摊主）
- 以省略号或悬念结尾
- 融入该城市独有的文化元素和地标特征（不要写任何城市都通用的万能文案）

三章结构：
1. **第一章** — 到达城市，被某个历史/文化元素吸引，节奏舒缓
2. **第二章** — 发现城市的隐藏魅力，节奏加快，情节推进
3. **终章** — 夜幕降临，在美食或夜景中完成旅程，余韵悠长

### Step 4: 构建意外引擎数据

为节点2设置意外引擎，模拟"产品售罄→AI 重新搜索→剧情反转"的体验。使用 Step 1 搜索 B 的备选产品作为替代：

```json
{
  "reason": "很抱歉，{主产品名} 的热门场次已售罄，节假日期间一票难求...",
  "aiThinking": "FlyAI 正在重新搜索 CITY 周边体验项目...\n\n发现了一个隐藏宝藏：{备选产品名}！",
  "newStory": "为备选产品写的新故事文案（80-120字）",
  "newSkuName": "备选产品的 skuName",
  "newJumpUrl": "备选产品的 jumpUrl",
  "newPicUrl": "备选产品的 picUrl",
  "newAddress": "备选产品的 address",
  "compensationReward": { "type": "coupon", "name": "剧情反转补偿券", "icon": "🎭" }
}
```

### Step 5: 组装数据并生成 HTML

**5a. 构建 LOADING_STEPS 数组**

反映实际执行的 flyai 搜索命令：
```json
[
  "> flyai search-poi --city-name \"CITY\" --category \"历史古迹\"",
  "  ✓ 发现 N 个文化景点",
  "> flyai keyword-search --query \"CITY 特色体验 演出\"",
  "  ✓ 发现 N 个特色体验",
  "> flyai keyword-search --query \"CITY 美食体验\"",
  "  ✓ 发现 N 个美食推荐",
  "> AI 正在编织叙事故事线...",
  "  ✓ 3 段沉浸式故事已生成",
  "> 意外引擎已就绪"
]
```

**5b. 构建 NODES 数组**

3 个节点对象，结构如下：

```json
[
  {
    "id": "{城市拼音}_node1",
    "title": "节点标题（来自产品名或景点名）",
    "chapter": "第一章",
    "story": "Step 3 生成的故事文案",
    "skuName": "飞猪产品名",
    "jumpUrl": "https://...（来自 flyai 搜索结果）",
    "picUrl": "https://...（来自 flyai 搜索结果）",
    "address": "具体地址",
    "reward": { "type": "coupon", "name": "XX体验券", "icon": "🎫" },
    "status": "unlocked",
    "willTriggerRedirect": false,
    "redirectData": null
  },
  {
    "id": "{城市拼音}_node2",
    "title": "节点标题",
    "chapter": "第二章",
    "story": "Step 3 生成的故事文案",
    "skuName": "飞猪产品名",
    "jumpUrl": "https://...",
    "picUrl": "https://...",
    "address": "具体地址",
    "reward": { "type": "coupon", "name": "XX探秘券", "icon": "🎪" },
    "status": "locked",
    "willTriggerRedirect": true,
    "redirectData": {
      "reason": "...",
      "aiThinking": "...",
      "newStory": "...",
      "newSkuName": "...",
      "newJumpUrl": "...",
      "newPicUrl": "...",
      "newAddress": "...",
      "compensationReward": { "type": "coupon", "name": "剧情反转补偿券", "icon": "🎭" }
    }
  },
  {
    "id": "{城市拼音}_node3",
    "title": "节点标题",
    "chapter": "终章",
    "story": "Step 3 生成的故事文案",
    "skuName": "飞猪产品名",
    "jumpUrl": "https://...",
    "picUrl": "https://...",
    "address": "具体地址",
    "reward": { "type": "title", "name": "CITY行者 称号", "icon": "🏆" },
    "status": "locked",
    "willTriggerRedirect": false,
    "redirectData": null
  }
]
```

**5c. 读取模板并替换占位符**

⚠️ **强制要求：必须使用 Bash 工具读取 `assets/template.html` 的完整原始内容，不得从记忆重建或自行编写 HTML。**

```bash
cat assets/template.html
```

读取到文件内容后，**仅**对以下 7 个占位符做字符串替换，其余所有字符（包括所有 `<style>` CSS 样式、`<script>` 逻辑、HTML 结构标签）一律保持原样，不得增删或修改：

| 占位符 | 替换为 | 示例 |
|--------|--------|------|
| `{{CITY_NAME}}` | 城市名 | `长沙` |
| `{{CITY_TITLE}}` | 城市名 + "篇" | `长沙篇` |
| `{{CITY_BADGE}}` | 城市名 + " · " + 主题短语 | `长沙 · 湘江寻味` |
| `{{LOADING_STEPS_JSON}}` | 5a 的 JSON 数组（合法 JS） | `["> flyai ...", ...]` |
| `{{FINISH_TITLE}}` | 城市名 + "副本通关!" | `长沙副本通关!` |
| `{{FINISH_TEXT}}` | 通关提示文案 | `你已解锁长沙全部隐藏...` |
| `{{NODES_JSON}}` | 5b 的 JSON 数组（合法 JS） | `[{...}, {...}, {...}]` |

**关键：JSON 必须是合法的 JavaScript 字面量，不能有语法错误（注意转义引号、换行符）。**

> 🚫 严禁行为：不得重新生成 HTML 骨架、不得修改 CSS 颜色/布局/动画、不得增减 `<script>` 中的函数、不得对模板做任何"优化"或"美化"。输出文件的内容必须与模板文件逐字一致，仅 7 处占位符被替换。

### Step 6: 输出文件并启动本地预览

将替换后的 HTML 保存到 outputs 目录：

```
outputs/city-game-CITY.html
```

保存后，**必须使用 Bash 工具在后台启动本地 HTTP 服务**，自动打开浏览器预览。不要用 `file://` 协议（会被浏览器安全策略拦截），也不要只是告诉用户手动打开。

```bash
python3 scripts/serve.py "outputs/city-game-CITY.html"
```

> `scripts/serve.py` 会自动找到空闲端口、启动 HTTP 服务、打开浏览器访问 `http://localhost:{port}/city-game-CITY.html`。
> 这条命令需要用 `run_in_background` 模式执行（因为服务会持续运行），然后立即向用户输出链接。

执行后向用户展示：
- 本地预览链接（`http://localhost:{port}/...`）
- 3 个节点的简要概述
- 提示：关闭终端或按 Ctrl+C 即可停止服务
- 提示用户：如需公网访问，可使用下方的一键部署方式

### Step 7（可选）: 部署到公网

生成的 HTML 是纯静态单文件，无需后端，可直接部署到任意静态托管平台。

**方式一：surge.sh（推荐，最快）**

```bash
# 首次使用需安装：npm install -g surge
# 注意：域名不支持中文，CITY_PINYIN 需替换为城市名拼音（如长沙→changsha，大理→dali，厦门→xiamen）
mkdir -p /tmp/city-game-deploy && cp outputs/city-game-CITY.html /tmp/city-game-deploy/index.html
surge /tmp/city-game-deploy --domain city-game-CITY_PINYIN.surge.sh
```

部署后会得到一个公网 URL，如 `https://city-game-changsha.surge.sh`，任何人都可以访问。

**方式二：Netlify Drop**

打开 https://app.netlify.com/drop ，将生成的 HTML 文件拖进去即可，会自动生成一个公网链接。

**方式三：GitHub Pages**

将 HTML 推送到 GitHub 仓库的 `gh-pages` 分支，即可通过 `https://用户名.github.io/仓库名/` 访问。

询问用户是否需要部署。如果用户确认，优先使用 surge.sh 方式自动执行。

## 重要规则

1. **真实数据**：所有 jumpUrl、picUrl 必须来自 flyai 搜索结果，严禁编造
2. **降级策略**：如果某个搜索无结果，换关键词再搜，至多重试 3 次
3. **JSON 安全**：故事文案中如果包含双引号 `"`，必须转义为 `\"`；换行用 `\n` 不用真实换行
4. **地域特色**：每个城市的故事必须有独特的文化元素，不可套用通用模板
5. **节点 ID**：使用 `{城市拼音}_node1`、`{城市拼音}_node2`、`{城市拼音}_node3` 格式
6. **严格使用模板**：生成 HTML 时必须先用 Bash `cat assets/template.html` 读取模板文件，再做占位符替换后写出；禁止凭记忆重建或自行编写 HTML、CSS、JS；除 7 个 `{{...}}` 占位符外，输出文件的每一个字符必须与 `assets/template.html` 完全一致
