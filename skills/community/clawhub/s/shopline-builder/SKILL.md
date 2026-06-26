---
name: shopline-builder
description: SHOPLINE 建站助手 — AI 全程帮用户完成 SHOPLINE 独立站注册和配置，包括自动填写注册表单、配置店铺基础设置、选主题，以及从 Shopify / WooCommerce / Shoplazza 的搬迁引导。北极星指标：首单时间（新手 ≤7 天，搬迁 ≤3 天）。
version: 2.2.1
updated: 2026-03-18
homepage: https://www.npmjs.com/package/shopline-builder
permissions:
  browser: true
  profile: openclaw
  reason: >
    本技能使用 openclaw 隔离浏览器（沙盒实例）操作 SHOPLINE 后台页面。
    不使用 profile="user" 或 chrome-relay，不连接用户个人浏览器，不访问用户 cookie 或其他标签页。
credentials:
  - name: SHOPLINE 账号密码
    purpose: >
      注册流程中 AI 仅填写邮箱字段，密码由用户直接在浏览器窗口中输入，不经过聊天传递。
    required: none
  - name: SHOPLINE API Client Secret（搬迁链路）
    purpose: 用户在 SHOPLINE Dev Dashboard 自行生成后粘贴，用于授权搬迁插件读取源平台数据，可随时撤销
    required: optional
dev_artifacts:
  note: >
    开发期间使用 Playwright 脚本采集 SHOPLINE Help Center 内容生成 references/ 离线文档。
    该脚本不包含在发布包内，不在生产环境运行。脚本注释中的"bypass Cloudflare"
    描述的是降低请求频率、模拟标准浏览器头等采集策略，非 skill 运行时功能。
attribution:
  utm: true
  disclosure: >
    注册链接携带 UTM 参数（utm_source=openclaw）用于归因统计。
    在信息收集环节向用户明确披露，并提供无参数原始链接作为替代。
triggers:
  - SHOPLINE 怎么开店
  - 我想开一个独立站
  - 帮我注册 SHOPLINE
  - 帮我在 SHOPLINE 建店
  - 怎么从 Shopify 搬到 SHOPLINE
  - 从 WooCommerce 迁移到 SHOPLINE
  - Shoplazza 搬迁到 SHOPLINE
  - SHOPLINE 注册
  - 独立站建站教程
  - SHOPLINE 套餐怎么选
  - SHOPLINE 支付怎么配置
  - SHOPLINE 域名绑定
  - how to set up SHOPLINE store
  - migrate to SHOPLINE
  - SHOPLINE store setup
  - start selling on SHOPLINE
  - SHOPLINE payment setup
  - bind domain to SHOPLINE
---

# SHOPLINE 建站助手 — AI 自动化执行指令

> 本 SKILL.md 是 AI 的执行剧本。**核心原则：AI 帮用户自动完成注册和配置，用户只需要提供信息。**
>
> **透明度原则：** 本技能通过浏览器自动化操作 SHOPLINE 后台页面。执行前应向用户说明 AI 将代为操作浏览器完成建站配置；对于密码、API 密钥等敏感信息，每次使用前需明确告知用途并获得用户确认。

---

## 零、浏览器模式

本技能**始终使用 `openclaw` 隔离浏览器**（OpenClaw 管理的沙盒浏览器实例，与用户个人 Chrome 完全隔离）。

不使用 `profile="user"`（CDP 连接用户个人浏览器）或 `chrome-relay`。原因：CDP 连接在技术上可访问用户所有标签页和 cookie，无法在 skill 层面强制约束范围，不符合最低权限原则。

**对用户的说明：** AI 会打开一个独立的浏览器窗口来操作 SHOPLINE，这个窗口与你的个人 Chrome 完全隔离。如果需要登录已有账号，AI 会引导你在这个独立窗口里手动登录（只需一次）。

**批量操作规范（v2.0 新增）：**

多个顺序操作尽量合并为批量调用以减少往返延迟：

```python
# 推荐：一次调用执行多个动作
browser(action="act", request=[
    {"kind": "click", "ref": "e12"},
    {"kind": "type", "text": "TrendyGoods Store"},
    {"kind": "press", "key": "Tab"}
])

# selector 定位（当 ref 不稳定时使用）
browser(action="act", request={"kind": "click", "selector": "#next-btn"})

# 延迟点击（等页面动画/渲染完成）
browser(action="act", request={"kind": "click", "ref": "e12", "delayMs": 500})
```

---

## 一、触发后立即执行：信息收集

触发 skill 后，**不要说废话**，直接输出以下信息收集请求（一次性问完，用户填完就开始操作）：

---

👋 好的！我来帮你在 SHOPLINE 开店，全程 AI 帮你搞定，你只需要提供几个基本信息：

**请一次性填写（填完我立刻帮你开始）：**

1. **姓名**：名字 / 姓氏（例：张 / 伟）
2. **店铺名称**：你的品牌名或店铺名（例：TrendyGoods Store）
3. **目标市场**：你主要卖给哪个国家/地区（例：United States / 美国）
4. **注册邮箱**：用来创建 SHOPLINE 账号的邮箱
5. **公司名称**（选填）：如有品牌/公司名可填，没有跳过

> 📌 **说明**：注册链接包含 UTM 归因参数（`utm_source=openclaw`），用于统计通过本 skill 完成注册的用户数量。这不影响你的注册流程和账号权益，SHOPLINE 不会因此向你收取额外费用。如不希望携带追踪参数，可直接访问 [https://www.shopline.com/register](https://www.shopline.com/register) 自行注册。

填好后我马上帮你注册 ✈️

---

收到用户信息后，进入注册流程。

---

## 二、注册流程（Step 1-6）

SHOPLINE 注册是一个多步骤 onboarding 表单，URL：
`https://admin.myshopline.com/user/onboarding/6565889082504519950/en`

| 步骤 | 页面内容 | 需要用户数据 | 可跳过 |
|------|---------|------------|------|
| Step 1 | 姓名 + 公司名 | ✅ First Name / Last Name / Company Name | ❌ 必填 |
| Step 2 | 身份选择 | 选「I am just starting」| ❌（自动选） |
| Step 3 | 销售方式 | 选「Online Store」| ❌（自动选） |
| Step 4 | 店铺名称 | ✅ Store name | ✅ 可 Skip |
| Step 5 | 销售地区 | ✅ 从下拉选用户的目标国家 | ❌ 必填 |
| Step 6 | 创建账号 | ✅ Email + Password（用户自填）| ❌ 必填 |

### Step 1 — 姓名 + 公司名

**执行步骤：**

```python
# 使用 openclaw profile（注册无需登录态）
browser(action="open", url="https://admin.myshopline.com/user/onboarding/6565889082504519950/en")
browser(action="snapshot")  # 确认页面加载，看到 "What is your full name" 字样

# 批量填写姓名 + 公司名 + 点下一步（一次调用）
browser(action="act", request=[
    {"kind": "type", "ref": "<First Name textbox ref>", "text": "<用户名字>"},
    {"kind": "type", "ref": "<Last Name textbox ref>", "text": "<用户姓氏>"},
    {"kind": "type", "ref": "<Company Name textbox ref>", "text": "<公司名，无则填店铺名>"},
    {"kind": "click", "ref": "<Next button ref>", "delayMs": 200}
])
```

### Step 2 — 身份选择

**执行步骤：**

```python
browser(action="snapshot")  # 确认到了 "Which of these best describe you?" 页面

# 批量：选身份 + 点下一步
browser(action="act", request=[
    {"kind": "click", "ref": "<'I am just starting' 选项 ref>"},
    {"kind": "click", "ref": "<Next button ref>", "delayMs": 200}
])
```

> ⚠️ 如果用户是搬迁用户，改选「I am currently selling online or in-person」

### Step 3 — 销售方式

**执行步骤：**

```python
browser(action="snapshot")  # 确认到了 "How would you like to sell on SHOPLINE?" 页面

# 批量：选 Online Store + 点下一步
browser(action="act", request=[
    {"kind": "click", "ref": "<'Online Store' 选项 ref>"},
    {"kind": "click", "ref": "<Next button ref>", "delayMs": 200}
])
```

### Step 4 — 店铺名称

**执行步骤：**

```python
browser(action="snapshot")  # 确认到了 "Give your store a name" 页面

# 批量：填店铺名 + 点下一步
browser(action="act", request=[
    {"kind": "type", "ref": "<Store name textbox ref>", "text": "<用户店铺名>"},
    {"kind": "click", "ref": "<Next button ref>", "delayMs": 200}
])
```

> 如用户未提供店铺名，点 Skip 跳过

### Step 5 — 销售地区

**执行步骤：**

```python
browser(action="snapshot")  # 确认到了 "Which country you are selling to?" 页面

# 点开下拉
browser(action="act", request={"kind": "click", "ref": "<Sales region 下拉 ref>"})
browser(action="snapshot")  # 查看国家列表

# 点选目标国家 + 点下一步
browser(action="act", request=[
    {"kind": "click", "ref": "<目标国家选项 ref>"},
    {"kind": "click", "ref": "<Next button ref>", "delayMs": 300}
])
```

> 常用地区映射：美国 → United States，中国 → China，英国 → United Kingdom

### Step 6 — 创建账号（🛑 AI 停止操作，用户在浏览器中自行完成）

**执行步骤：**

```python
browser(action="snapshot")  # 确认到了 "Create Your SHOPLINE Account" 页面
browser(action="act", request={"kind": "type", "ref": "<Email textbox ref>", "text": "<用户提供的邮箱>"})
browser(action="screenshot")  # 截图展示当前状态
```

**截图后告知用户：**

---

🎯 最后一步到了！邮箱已经帮你填好了。

**请你直接在刚才弹出的浏览器窗口里完成：**
1. 在「Password」框里输入你的密码（8-20位，含大写/小写/数字/特殊字符）
2. 在「Confirm Password」框里再次输入密码
3. 勾选同意条款
4. 点「SIGN UP」按钮

> 🔒 **为什么要你自己输入？** 密码这种高敏感信息不应该通过聊天传递。请直接在浏览器里输入，这样密码不经过任何中间环节。

完成后告诉我「注册好了」，我继续帮你配置店铺 ✅

---

**用户确认注册成功后，AI 继续：**

```python
browser(action="screenshot")  # 截图确认已进入 SHOPLINE 后台
browser(action="snapshot")    # 获取当前后台 URL 提取 store handle
```

### 注册完成 — 获取 store handle 并进入配置

**执行步骤：**

```
browser(action=snapshot)  # 获取当前后台 URL
# 从 URL 中提取 store handle，例如：
# https://fashion333222.myshopline.com/admin/...  →  storeHandle = "fashion333222"
```

将 storeHandle 保存到进度文件：

```json
{
  "storeHandle": "<提取到的 handle>",
  "registeredEmail": "<用户邮箱>",
  "storeName": "<店铺名称>",
  "targetMarket": "<目标市场>",
  "step": "onboarding"
}
```

**完成后告知用户：**

---

✅ 注册成功！你有 14 天免费试用期，无需立刻选套餐。

接下来我来帮你完成 4 步快速配置，让店铺准备好接单 🚀

---

> ⚠️ 后续所有 browser 操作的后台 URL 格式均为：
> `https://<storeHandle>.myshopline.com/admin/...`
> 若 storeHandle 无法自动获取，询问用户登录 SHOPLINE 后台后，地址中 `.myshopline.com` 前面的那段名称。

---

## 三、Onboarding 配置（Step A/B/C/D）

注册成功后，AI 依次引导用户完成以下 4 个核心配置步骤。**每步结束后截图确认，再进入下一步。**

---

### Step A：首页装修（AI 辅助）

**先询问用户：**

---

🏪 **Step 1/4 — 首页装修**

你这个店铺主要卖什么？用一句话描述一下
（例如：我们卖高端女装，风格简约优雅）

---

收到用户描述后，提供两个选择：

---

明白！你有两种方式来装修首页：

**选 1：AI 自动建站**（推荐）— SHOPLINE 内置 AI 建站功能，根据你的店铺类型自动生成完整主题、图片和文案，一键搞定 ✨

**选 2：自己手动装修** — 我给你打开设计器，你自己来调

你选哪个？回复「1」或「2」

---

**如果用户选 1（AI 自动建站）：**

**执行步骤：**

```python
# 1. 导航到 AI Builder 入口（已验证路由）
browser(action="navigate", url="https://<storeHandle>.myshopline.com/admin/website/shopSetting")
browser(action="screenshot")  # 确认页面加载

# 2. 点「Try it Now」进入 AI Builder
browser(action="act", request={"kind": "click", "selector": "button:has-text('Try it Now')", "delayMs": 300})
browser(action="screenshot")  # 确认进入 /admin/website/shopSetting/aiBuild

# 3. 如弹出「建议先创建商品」→ 点 Continue website building 跳过
browser(action="act", request={"kind": "click", "selector": "button:has-text('Continue website building')"})

# 4. 选品类（下拉树形选单）
browser(action="snapshot")
browser(action="act", request={"kind": "click", "ref": "<品类下拉 ref>"})  # 展开下拉
browser(action="snapshot")  # 看品类列表
browser(action="act", request={"kind": "click", "ref": "<匹配品类 ref>"})  # 点选对应品类

# 5. 填写描述（描述框有示例内容，不用清空，直接用示例也可）
# 如需自定义描述：
browser(action="act", request={"kind": "type", "ref": "<描述文本框 ref>",
    "text": "Style: <风格>; Category: <品类>; Main products: <主要商品>; Other details: <关键词>"})
browser(action="act", request={"kind": "click", "ref": "<Next 按钮 ref>", "delayMs": 300})

# 6. 如弹出「AI 创建商品分类」→ Create categories
browser(action="snapshot")
browser(action="act", request={"kind": "click", "selector": "button:has-text('Create categories')"})

# 7. 等待 AI 生成（约 60-120 秒），轮询截图直到进度完成出现「Publish directly」
browser(action="screenshot")  # 查看进度，重复几次直到完成

# 8. 发布主题
browser(action="act", request={"kind": "click", "selector": "button:has-text('Publish directly')", "delayMs": 300})

# 9. 弹出「生成其他页面」对话框 → 全选辅助页面一并生成
# 推荐全选：About us / Order tracking + Privacy/Return/Shipping policy / Terms of service
browser(action="snapshot")  # 找各 checkbox ref
# 依次点选所有 checkbox（跳过已默认勾选的 Contact us）
# 最后点：
browser(action="act", request={"kind": "click", "selector": "button:has-text('Publish after generating the page')", "delayMs": 300})

browser(action="screenshot")  # 截图确认发布成功（顶部 toast: "Theme published successfully"）
```

> ⚠️ **路由说明（已实测验证）：**
> - 主题管理入口：`/admin/website/shopSetting`
> - AI Builder 页面：`/admin/website/shopSetting/aiBuild`
> - ~~`/admin/themes`~~ 和 ~~`/admin/online-store/themes`~~ 均为 404，不可用

**完成后告知用户：**

---

✅ **AI 建站完成！** 你的店铺主题已上线 🎉

SHOPLINE AI 根据你的店铺描述自动生成了专属主题，包括图片、文案和页面布局，已直接发布。辅助页面（Contact us、Privacy Policy 等）也一并生成完毕。

---

**如果用户选 2（手动装修）：**

**执行步骤：**

```python
# 侧边栏 Online Store → Design 子菜单
browser(action="navigate", url="https://<storeHandle>.myshopline.com/admin/website/shopSetting")
browser(action="screenshot")
```

**完成后告知用户：**

---

好的！这是你的主题设计器链接，你可以自己去调：

🔗 `https://<storeHandle>.myshopline.com/admin/theme-sline-editor/editing/Home`

调好后告诉我，我们继续下一步 ✅

---

> ⚠️ AI 建站每个店铺免费使用 1 次。整个流程 AI 全程代操作，用户无需做任何选择。

---

### Step B：上架第一个商品（AI 全自动）

AI 根据用户之前提供的店铺描述，自动生成商品信息并上架，**不需要询问用户任何信息**。

**商品信息生成规则（根据店铺描述推断）：**

| 店铺类型 | 商品示例 | 价格区间 |
|---------|---------|---------|
| 运动/户外 | Lightweight Hiking Backpack 35L | $49.99 - $89.99 |
| 时尚/女装 | Classic Linen Casual Dress | $29.99 - $69.99 |
| 家居/装饰 | Nordic Minimalist Table Lamp | $39.99 - $79.99 |
| 美妆/护肤 | Hydrating Daily Face Serum | $24.99 - $49.99 |
| 3C/科技 | Wireless Bluetooth Earbuds Pro | $39.99 - $79.99 |

**图片来源：Unsplash（下载到本地再上传）**

根据商品类型，从 Unsplash 下载 1-2 张匹配图片：
- 运动背包：`https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=1200`
- 户外装备：`https://images.unsplash.com/photo-1484704849700-f032a568e944?w=1200`
- 时尚女装：`https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=1200`
- 家居装饰：`https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1200`

下载命令：`exec("curl -L '<URL>' -o /tmp/openclaw/uploads/product-1.jpg")`

**执行步骤：**

```python
# 1. 根据店铺描述生成商品信息（商品名称、价格、描述完全由 AI 生成，不问用户）

# 2. 下载商品图片到本地
exec("mkdir -p /tmp/openclaw/uploads && curl -L '<匹配图片URL>' -o /tmp/openclaw/uploads/product-1.jpg")
exec("curl -L '<匹配图片URL2>' -o /tmp/openclaw/uploads/product-2.jpg")

# 3. 打开商品添加页面（使用 profile="user" 保持登录态）
browser(action="navigate", url="https://<storeHandle>.myshopline.com/admin/products/add", profile="user")
browser(action="snapshot", profile="user")

# 4+5. 批量填写商品名称 + 价格
browser(action="act", profile="user", request=[
    {"kind": "type", "ref": "<商品名称输入框 ref>", "text": "<AI生成的商品名>"},
    {"kind": "type", "ref": "<价格输入框 ref>", "text": "<AI生成的价格>"}
])

# 6. 填写库存（固定 100）
# ⚠️ input[placeholder="Please enter"] 多个，index 对应：0=零售价 1=比较价 2=成本价 3=库存 4=SKU 5=条码
# 必须用 native value setter，直接 type 无效（React controlled input）
browser(action="act", profile="user", request={"kind": "evaluate", "fn": """
    (() => {
        const inputs = Array.from(document.querySelectorAll('input[placeholder="Please enter"]'));
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(inputs[3], '100');
        inputs[3].dispatchEvent(new Event('input', {bubbles:true}));
        return 'inventory=' + inputs[3].value;
    })()
"""})

# 7. 填写商品描述（富文本编辑器在 iframe contentDocument 里）
browser(action="act", profile="user", request={"kind": "evaluate", "fn": """
    (() => {
        const iframe = document.querySelectorAll('iframe')[0];
        const editor = iframe.contentDocument.querySelector('[contenteditable]');
        editor.focus();
        editor.innerHTML = '<p><AI生成的描述文本></p>';
        editor.dispatchEvent(new Event('input', {bubbles:true}));
        return 'done';
    })()
"""})

# 8. 上传商品图片
browser(action="act", profile="user", request={"kind": "click", "ref": "<Add from file library 按钮 ref>"})
browser(action="upload", profile="user", ref="<Upload file 按钮 ref>", paths=["/tmp/openclaw/uploads/product-1.jpg"])
# 等上传完成后，用 evaluate 遍历父级点击图片容器选中
browser(action="act", profile="user", request={"kind": "evaluate", "fn": """
    (() => {
        const dialog = document.querySelector('[role=dialog]');
        const imgs = dialog.querySelectorAll('img');
        [0].forEach(idx => {
            let el = imgs[idx];
            while(el && el !== dialog){
                if(el.classList && (el.className.includes('item') || el.className.includes('card') ||
                   el.className.includes('file') || el.className.includes('media'))){
                    el.click(); break;
                }
                el = el.parentElement;
            }
        });
        return 'selected';
    })()
"""})
browser(action="act", profile="user", request={"kind": "click", "ref": "<Complete 按钮 ref>", "delayMs": 300})

# 9. 发布商品
browser(action="act", profile="user", request={"kind": "click", "ref": "<Save/Publish 按钮 ref>", "delayMs": 500})
browser(action="screenshot", profile="user")  # 截图确认商品已上架
```

**完成后告知用户：**

---

✅ **第一个商品已上架！**

🛍️ 商品：<商品名>
💰 价格：$<价格>
📝 描述：<一句话描述>
📦 库存：100

---

---

### Step C：配置支付

**导航：** `https://<storeHandle>.myshopline.com/admin/settings/payments`

**执行策略（三种支付方式，处理方式不同）：**

| 支付方式 | AI 能否代操作 | 说明 |
|---------|------------|------|
| Cash on delivery | ✅ 可以 | 直接点 Enable → Add Cash On Delivery |
| PayPal | ❌ 不行 | Cloudflare 安全拦截，跳转后被阻止，需用户手动登录 PayPal 授权 |
| SHOPLINE Payments | ❌ 不行 | 需要 KYC 身份认证，必须用户手动提交 |

**执行步骤：**

```python
# 1. 导航到支付页（profile="user" 保持登录态）
browser(action="navigate", url="https://<storeHandle>.myshopline.com/admin/settings/payments", profile="user")
browser(action="snapshot", profile="user")

# 2. 开启 Cash on delivery（AI 全自动）
browser(action="act", profile="user", request={"kind": "click", "ref": "<Cash on delivery Enable 按钮 ref>", "delayMs": 500})
# 进入配置页后，直接点「Add Cash On Delivery」（用 selector 精准定位，无需依赖 ref）
browser(action="act", profile="user", request={"kind": "evaluate", "fn": """
    Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Add Cash On Delivery'))?.click()
"""})
browser(action="screenshot", profile="user")  # 确认 COD 出现在 Custom payment methods 列表

# 3. PayPal 和 SHOPLINE Payments → 告知用户需手动完成
```

**完成后告知用户：**

---

✅ **货到付款（Cash on delivery）已开启！**

另外还有两个支付方式需要你手动完成：

**PayPal（推荐，美国客户常用）：**
1. 在支付设置页找到 PayPal → 点 Enable
2. 在弹出页面登录你的 PayPal 企业账号完成授权

**SHOPLINE Payments（信用卡收款）：**
1. 点「Activate SHOPLINE Payments」
2. 按提示完成身份认证（KYC）

---

> ⚠️ PayPal 和 SHOPLINE Payments 均有安全验证机制，AI 无法代替登录，必须由真人操作。

---

### Step D：配置物流

**导航：** `https://<storeHandle>.myshopline.com/admin/settings/delivery`

**执行步骤（全自动，无需询问用户）：**

```python
# 1. 进入运费设置（profile="user" 保持登录态）
browser(action="navigate", url="https://<storeHandle>.myshopline.com/admin/settings/delivery", profile="user")
browser(action="snapshot", profile="user")
browser(action="act", profile="user", request={"kind": "evaluate", "fn": """
    Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Shipping rate settings'))?.click()
"""})

# 2. 创建 US Domestic zone
browser(action="act", profile="user", request={"kind": "evaluate", "fn": """
    Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Add a shipping zone'))?.click()
"""})
browser(action="snapshot", profile="user")
# 弹窗中：填 Zone name + 搜选 United States（62 states）+ 点 Create（批量）
browser(action="act", profile="user", request=[
    {"kind": "type", "ref": "<Zone name 输入框 ref>", "text": "US Domestic"},
    {"kind": "type", "ref": "<国家搜索框 ref>", "text": "United States", "delayMs": 300}
])
browser(action="act", profile="user", request={"kind": "evaluate", "fn": """
    (() => {
        const dialog = document.querySelector('[role=dialog]');
        const paras = dialog.querySelectorAll('p,li,[class*=item],[class*=country]');
        for(const p of paras){
            if(p.textContent.includes('United States') && !p.textContent.includes('Minor')){
                p.click(); break;
            }
        }
    })()
"""})
browser(action="act", profile="user", request={"kind": "click", "ref": "<Create 按钮 ref>", "delayMs": 500})

# 3. 给 US Domestic 加运费（selector 精准点击第一个「Add the shipping rates」）
browser(action="snapshot", profile="user")
browser(action="act", profile="user", request={"kind": "evaluate", "fn": """
    document.querySelectorAll('button, a')[
        Array.from(document.querySelectorAll('button, a')).findIndex(b => b.textContent.includes('Add the shipping rates'))
    ]?.click()
"""})
browser(action="snapshot", profile="user")
# 弹窗填写运费名称和价格（native setter，spinbutton 格式为「$ 5.99」）
browser(action="act", profile="user", request={"kind": "evaluate", "fn": """
    (() => {
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        const combobox = document.querySelector('[role=combobox]');
        setter.call(combobox, 'Standard Shipping');
        combobox.dispatchEvent(new Event('input', {bubbles:true}));
        const spinbutton = document.querySelector('[role=spinbutton]');
        setter.call(spinbutton, '$ 5.99');
        spinbutton.dispatchEvent(new Event('input', {bubbles:true}));
        return 'done';
    })()
"""})
browser(action="act", profile="user", request={"kind": "click", "ref": "<Done 按钮 ref>", "delayMs": 300})

# 4. 创建 International zone（Rest of World）
browser(action="act", profile="user", request={"kind": "evaluate", "fn": """
    Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Add a shipping zone'))?.click()
"""})
browser(action="snapshot", profile="user")
# 填 Zone name + 勾选 Rest of world checkbox + 点 Create（批量）
browser(action="act", profile="user", request=[
    {"kind": "type", "ref": "<Zone name 输入框 ref>", "text": "International"},
    {"kind": "click", "ref": "<Rest of world checkbox ref>", "delayMs": 300},
    {"kind": "click", "ref": "<Create 按钮 ref>", "delayMs": 500}
])

# 5. 给 International 加运费（14.99）
browser(action="act", profile="user", request={"kind": "evaluate", "fn": """
    const btns = Array.from(document.querySelectorAll('button, a')).filter(b => b.textContent.includes('Add the shipping rates'));
    btns[btns.length - 1]?.click()
"""})
browser(action="snapshot", profile="user")
browser(action="act", profile="user", request={"kind": "evaluate", "fn": """
    (() => {
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        const combobox = document.querySelector('[role=combobox]');
        setter.call(combobox, 'International Shipping');
        combobox.dispatchEvent(new Event('input', {bubbles:true}));
        const spinbutton = document.querySelector('[role=spinbutton]');
        setter.call(spinbutton, '$ 14.99');
        spinbutton.dispatchEvent(new Event('input', {bubbles:true}));
        return 'done';
    })()
"""})
browser(action="act", profile="user", request={"kind": "click", "ref": "<Done 按钮 ref>", "delayMs": 300})

# 6. 保存
browser(action="act", profile="user", request={"kind": "evaluate", "fn": """
    Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Update' && !b.disabled)?.click()
"""})
browser(action="screenshot", profile="user")  # 截图确认两个 Zone 出现在列表
```

**默认运费标准（AI 自动填入，无需询问用户）：**

| Zone | 运费名称 | 价格 |
|------|---------|------|
| US Domestic（美国全境） | Standard Shipping | $5.99 |
| International（全球 242 国） | International Shipping | $14.99 |

**完成后告知用户：**

---

✅ **物流配置完成！**

已设置两个运费区：
- 🇺🇸 美国境内：Standard Shipping $5.99
- 🌍 全球配送：International Shipping $14.99

---

> ⚠️ 技术注意：运费名称和价格输入框需用 `native value setter` + `dispatchEvent('input')` 填入，不能直接 type。spinbutton 的 value 格式为 `$ 14.99`（带空格和 $）。

---

### 🎉 Onboarding 完成

4 步全部完成后，输出：

---

🎉 **恭喜！你的 SHOPLINE 店铺已经准备好接单了！**

✅ 首页装修 — 完成
✅ 第一个商品 — 已上架
✅ 支付方式 — 已配置
✅ 物流规则 — 已设置

**下一步建议：**
- 绑定你的独立域名（Settings > Domains）
- 继续上架更多商品
- 开启 Facebook / Google 广告引流

有任何问题随时问我！祝你早日首单 🚀

---

---

## 四、错误处理

| 场景 | AI 处理方式 |
|------|------------|
| 遇到验证码（CAPTCHA）| 截图给用户，让用户手动处理，完成后告诉 AI 继续 |
| 遇到短信/邮箱验证码 | 截图给用户，用户输入验证码后 AI 继续 |
| 遇到二步验证（2FA）| 截图给用户，指导用户完成，然后继续 |
| 页面加载超时 | 刷新页面重试，超过3次告知用户 |
| 表单验证错误 | 截图显示错误信息，根据错误内容修正后重试 |
| 登录被重定向 | 截图给用户，引导用户手动登录后继续 |

**截图原则：** 凡需要用户介入，必先截图，让用户看到当前状态再操作。

```
browser(action=screenshot)  # 截图并自动发给用户
```

---

## 五、通用原则

- 语气简洁友好，像有经验的朋友帮你操作
- 不说废话，每步都有实质动作
- 每次截图后，将截图内容发给用户确认
- 遇到不确定的页面结构，先 `browser(action=snapshot)` 看清楚再操作
- 用户说「继续」就继续下一步，用户说「等一下」就暂停

### 关键链接

| 用途 | 链接 |
|------|------|
| 注册入口 | https://admin.myshopline.com/user/onboarding/6565889082504519950/en |
| 后台登录 | https://admin.myshopline.com/user/signIn |
| 帮助中心（中文）| https://help.shopline.com/hc/zh-cn |
| 帮助中心（英文）| https://help.shopline.com/hc/en-001 |
| App Store | https://apps.shopline.com/?lang=en |

---

## 附录 A：基础店铺设置（可选）

如果用户需要调整基础设置（语言、货币、联系方式等），在 Onboarding 完成后执行：

### 基础店铺设置

**路径：** Settings > Basic settings
**后台 URL：** `https://<storeHandle>.myshopline.com/admin/settings/basic`

```
browser(action=navigate, url="https://<storeHandle>.myshopline.com/admin/settings/basic")
browser(action=snapshot)
```

需要确认/配置的字段：
- Store name（店铺显示名称）
- Store description（店铺描述，可选）
- Contact email（联系邮箱）
- Store address（店铺地址，影响税务和发票）

操作完成后截图给用户确认。

### 语言与货币设置

**路径：** Settings > Languages & Currencies
**后台 URL：** `https://<storeHandle>.myshopline.com/admin/settings/language`

```
browser(action=navigate, url="https://<storeHandle>.myshopline.com/admin/settings/language")
browser(action=snapshot)
```

根据用户目标市场自动设置：
- 默认语言（如 US 市场 → English）
- 货币（如 US 市场 → USD）
- 时区（如 US 市场 → America/New_York 或 America/Los_Angeles）

### 主题选择

**路径：** Online Store > Design（侧边栏），或首页「Design Your Store」按钮
**后台 URL（已实测）：** `https://<storeHandle>.myshopline.com/admin/website/shopSetting`

> ⚠️ `/admin/themes` 和 `/admin/online-store/themes` 均为 404，不可用，请用上方正确路由。

```python
browser(action="navigate", url="https://<storeHandle>.myshopline.com/admin/website/shopSetting")
browser(action="screenshot")  # 截图给用户看主题管理页面
```

推荐走 AI Website Builder 流程（`/admin/website/shopSetting/aiBuild`），完整步骤见 Step A 章节。

---

## 附录 B：搬迁路径（Shopify / WooCommerce / Shoplazza）

如果用户说「我要从 Shopify / WooCommerce / Shoplazza 搬迁」，在完成注册 + 基础 Onboarding 后额外执行本流程。

> 触发关键词：「我现在在 Shopify / 从 Shopify 搬 / WooCommerce 迁移 / Shoplazza 转 SHOPLINE」
> 注册时 Step 2 身份选择改为「I am currently selling online or in-person」

---

### B.1 搬迁插件信息

| 项目 | 内容 |
|------|------|
| 插件名 | **Multi-platform Store Migration** |
| 开发商 | By SHOPLINE（官方出品） |
| 费用 | 免费 |
| 评分 | ⭐ 4.7（35条评价） |
| 支持平台 | Shopify、Shoplazza、WooCommerce |
| 搬迁内容 | 商品、客户、订单、301设置、Google Product Feed |
| App Store 详情页 | `https://apps.shopline.com/detail?appHandle=shopify_store_one_click_relocation&lang=en` |

---

### B.2 安装插件（AI 全自动）

```python
# 1. 进入 My Apps 页面（profile="user" 保持登录态）
browser(action="navigate", url="https://<storeHandle>.myshopline.com/admin/app-store", profile="user")
browser(action="snapshot", profile="user")

# 2. 批量：点搜索框 + 输入 "migration"（等下拉出现）
browser(action="act", profile="user", request=[
    {"kind": "click", "ref": "<搜索 combobox ref>"},
    {"kind": "type", "ref": "<搜索 combobox ref>", "text": "migration", "delayMs": 500}
])
browser(action="snapshot", profile="user")  # 确认下拉出现

# 3. 点击「Multi-platform Store Migration」menuitem
# ⚠️ 点击会在新标签页打开 App Store 详情页，需切换 targetId
browser(action="act", profile="user", request={"kind": "click", "ref": "<Multi-platform Store Migration menuitem ref>"})
browser(action="tabs", profile="user")  # 获取所有 tabs，找到 apps.shopline.com 新标签

# 4. 切换到新标签页，点击 Install（传入新标签的 targetId）
browser(action="snapshot", profile="user", targetId="<新标签 targetId>")
browser(action="act", profile="user", request={"kind": "click", "ref": "<Install 按钮 ref>", "delayMs": 500}, targetId="<新标签 targetId>")

# 5. 如弹窗「store mismatch」→ 点 Re-login 重新授权
browser(action="snapshot", profile="user")
# 如出现「The logged-in store does not match」→ 点击 Re-login
```

> ⚠️ **技术注意**：
> - App Store 页面（apps.shopline.com）与后台（myshopline.com/admin）是不同域，session 独立
> - 如弹窗「The logged-in store does not match」→ 点「Re-login」重新授权即可
> - 安装成功后会自动跳回后台并进入插件配置页
> - `profile="user"` 在此场景优势明显：保持后台已登录状态，避免跨域 session 丢失问题

---

### B.3 执行搬迁（安装后引导用户）

插件安装成功后，对用户说：

---

🎉 搬迁插件已安装！接下来需要你在 Shopify 这边做一个简单的授权配置，我来一步步告诉你怎么做。

**⚠️ 重要提示：搬迁插件现在使用新版授权方式（Client ID + Secret），需要从 Shopify Dev Dashboard 创建应用获取，不是旧版的 API Access Token。**

请按以下步骤操作（约5分钟）：

**第一步：** 打开 Shopify 开发者面板：https://shopify.dev/dashboard
（注意：这是开发者专用入口，不是店铺后台）

**第二步：** 点右上角 **【Create app】** → 选 **【Start from Dev Dashboard】** → App name 填 `Migration Tool` → 点 **【Create】**

**第三步：** 进入应用配置页：
- 找 **【App URL】** 填：`https://shopify.dev/apps/default-app-home`
- 找 **【Access > Select scopes】** → 勾选 **Admin API** 和 **Customer Account API** 下所有读写权限（Shopify Payments 相关可以不勾）
- 点 **【Release】** 发布

**第四步：** 点左侧 **【Home】** → 右上角 **【Install app】** → 选你的店铺，确认安装

**第五步：** 点左侧 **【Settings】** → 在 **Credentials** 区域找到：
- **Client ID**（直接复制）
- **Secret**（点眼睛图标显示后复制）

把 Client ID、Secret 和你的 Shopify 店铺 handle（`yourstore.myshopify.com` 前面那段）发给我，我来帮你填到搬迁工具里 ✅

---

> 📖 官方参考文档：https://help.shopline.com/hc/zh-cn/articles/53643605291929
>
> ⚠️ **注意事项：**
> - 如果点 Install app 报错「此应用无法安装」：进入 Settings → Distribution → 选「自定义分发」→ 填入店铺域名 → 点 Generate Link → 在新标签页打开链接安装
> - 如果搬迁插件界面仍然是要求输入 API Access Token 的旧版界面，则用旧版流程（在 Shopify 后台 Settings → Apps → Develop apps 里生成 Access Token）

---

用户提供信息后，AI 填写插件配置页并启动搬迁：

```python
# 进入搬迁插件（通过签名 URL 方式，避免跨域 session 问题）
# 1. 先从后台获取签名 URL
browser(action="act", request={"kind": "evaluate", "fn": """
    fetch('/admin/appstore/get-install-url?appKey=dbbfe1732acc9915a5732369f5060aaa92698eb3')
        .then(r=>r.json()).then(d=>d.data?.url)
        .then(url => { window._migrationUrl = url; return url; })
"""})
# 2. navigate 到签名 URL，自动进入搬迁主界面
browser(action="act", request={"kind": "evaluate", "fn": "window.location.href = window._migrationUrl"})
browser(action="screenshot")  # 截图给用户看搬迁主界面

# 3. 选 Shopify 平台 + 点开始搬迁 + 确认弹窗
browser(action="act", request={"kind": "evaluate", "fn": """
    Array.from(document.querySelectorAll('div')).find(el => el.textContent.trim() === 'Shopify' && el.offsetParent !== null)?.click()
"""})
browser(action="act", request={"kind": "evaluate", "fn": """
    Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('开始搬迁'))?.click()
"""})
browser(action="screenshot")  # 截图确认弹窗
browser(action="act", request={"kind": "evaluate", "fn": """
    Array.from(document.querySelectorAll('button')).filter(b => b.textContent.includes('开始搬迁')).pop()?.click()
"""})
# 关闭「我知道了」提示弹窗（如出现）
browser(action="act", request={"kind": "evaluate", "fn": """
    Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('我知道了'))?.click()
"""})

# 4. 填写授权信息（三个字段）
# ⚠️ 字段顺序（可见 input 按 index）：
#   index 0：隐藏字段（跳过）
#   index 1：店铺域名（Shopify handle，如 yourstore）
#   index 2：Client ID
#   index 3：Secret（从 Shopify Dev Dashboard → Settings → Credentials 获取）
# ⚠️ 必须用 native value setter，Vue/React controlled input 直接 type 无效
browser(action="act", request={"kind": "evaluate", "fn": """
    (() => {
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        const inputs = Array.from(document.querySelectorAll('input')).filter(i => i.offsetParent !== null);
        setter.call(inputs[1], '<用户 Shopify handle>');
        inputs[1].dispatchEvent(new Event('input', {bubbles:true}));
        setter.call(inputs[2], '<用户 Client ID>');
        inputs[2].dispatchEvent(new Event('input', {bubbles:true}));
        setter.call(inputs[3], '<用户 Secret>');
        inputs[3].dispatchEvent(new Event('input', {bubbles:true}));
        return inputs[1].value + ' | ' + inputs[2].value.slice(0,8) + '...';
    })()
"""})
browser(action="screenshot")  # 截图确认填写内容

# 5. 点下一步
browser(action="act", request={"kind": "evaluate", "fn": """
    Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('下一步'))?.click()
"""})
browser(action="screenshot")  # 截图确认进入数据选择页

# 6. 选择搬迁模块（第2步）
# ⚠️ 搬迁插件使用 Vue 自定义 checkbox 组件，JS click() 和 dispatchEvent 均无法触发
# 唯一有效方法：用坐标 + 完整 pointer/mouse 事件序列点击
#
# 模块名文字元素 class：`._moduleName_2weus_5`
# 获取坐标：
browser(action="act", request={"kind": "evaluate", "fn": """
    (() => {
        const els = Array.from(document.querySelectorAll('._moduleName_2weus_5')).filter(el => el.offsetParent !== null);
        return els.map(e => { const r = e.getBoundingClientRect(); return e.textContent.trim() + ':' + Math.round(r.left) + ',' + Math.round(r.top); }).join(' | ');
    })()
"""})
# 根据坐标，checkbox 在文字左侧约 -40px，点击方式：
browser(action="act", request={"kind": "evaluate", "fn": """
    new Promise(resolve => {
        // 按顺序点：折扣码 → 发货物流 → 商品 → 客户 → 订单（订单需先勾选商品+客户+折扣码）
        const nameEls = Array.from(document.querySelectorAll('._moduleName_2weus_5')).filter(el => el.offsetParent !== null);
        const targets = ['客户', '商品', '折扣码', '发货物流', '订单'];
        const coords = targets.map(name => {
            const el = nameEls.find(e => e.textContent.trim() === name);
            if(!el) return null;
            const r = el.getBoundingClientRect();
            return {name, x: Math.round(r.left - 25), y: Math.round(r.top + r.height/2)};
        }).filter(Boolean);

        let i = 0;
        function clickNext() {
            if(i >= coords.length) { resolve('done'); return; }
            const {x, y} = coords[i++];
            const el = document.elementFromPoint(x, y);
            ['pointerover','pointerenter','pointermove','pointerdown','mousedown','pointerup','mouseup','click'].forEach(t => {
                el.dispatchEvent(new MouseEvent(t, {bubbles:true, cancelable:true, clientX:x, clientY:y, view:window}));
            });
            setTimeout(clickNext, 400);
        }
        clickNext();
    })
"""})
browser(action="screenshot")  # 确认勾选状态（若有依赖提示弹窗，点关闭后重新点击订单）

# ⚠️ 订单依赖关系：必须先勾选「商品」+「客户」+「折扣码」，否则弹提示框拦截
# 如订单未勾上，单独用坐标点击：
# browser(action="act", request={"kind": "evaluate", "fn": "document.elementFromPoint(<订单x>, <订单y>)..."})

# 7. 确认统计数据 → 点「立即搬迁」
browser(action="act", request={"kind": "evaluate", "fn": """
    Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('下一步'))?.click()
"""})
browser(action="screenshot")  # 截图确认进入第3步（数据统计页）

browser(action="act", request={"kind": "evaluate", "fn": """
    Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('立即搬迁'))?.click()
"""})
browser(action="screenshot")  # 截图确认搬迁已开始（进度页）
```

> ⚠️ **技术注意：**
> - 搬迁插件托管在 `admin.innovelabs.com`，与 SHOPLINE 后台跨域，需用签名 URL 方式进入
> - 签名 URL 有效期约 30 分钟，过期需重新调 `/admin/appstore/get-install-url` 获取
> - 三个 input 中 index 0 为隐藏字段，从 index 1 开始是可见字段
> - Secret 字段填的是 Shopify Dev Dashboard → Settings → Credentials 里的 **Secret**（格式 `shpss_...`，不是旧版 Access Token `shpat_...`）
> - 模块选择 checkbox 为 Vue 组件，必须用 `elementFromPoint` + 完整鼠标事件序列点击，JS click/dispatchEvent 无效
> - 订单必须在商品+客户+折扣码全部勾选后再勾，否则弹依赖提示

搬迁启动后告知用户：

---

🚀 **搬迁已启动！**

数据正在从 [原平台] 迁移到你的 SHOPLINE 店铺，根据数据量大小通常需要几分钟到几小时。

迁移完成后你会收到邮件通知。期间店铺正常运营不受影响。

---

### B.4 平台专属文档

| 来源平台 | 官方搬迁文档 |
|---------|------------|
| Shopify | https://help.shopline.com/hc/en-001/articles/4669702695193 |
| WooCommerce | https://help.shopline.com/hc/en-001/articles/16784282483353 |
| Shoplazza | https://help.shopline.com/hc/en-001/articles/5943463861145 |

---

## 附录 C：References 索引

| 文件 | 内容 |
|------|------|
| `references/flow-newbie.md` | 新手流程话术参考（旧版，可参考细节） |
| `references/flow-migrate.md` | 搬迁流程话术参考（旧版，可参考细节） |
| `references/faq-zh.md` | 中文 FAQ |
| `references/faq-en.md` | 英文 FAQ |
