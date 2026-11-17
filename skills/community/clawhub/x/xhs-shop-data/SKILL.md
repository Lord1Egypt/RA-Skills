---
name: xhs-shop-data
slug: xhs-shop-data
displayName: 小红书电商数据采集
summary: 采集小红书商品搜索、店铺商品列表、商品详情（名称/到手价/划线价/店铺销量粉丝/轮播图与详情图），统一 100 点/次（注册送 1000 点），支持筛选标签、翻页、幂等防重复扣点、大响应落盘，适合选品分析、竞品比价与店铺监控。
description: 小红书电商数据采集（商品搜索/店铺商品列表/商品详情）。当用户需要按关键词搜索小红书的在售商品、拉取某个小红书店铺的全部商品、或获取某个小红书商品的详情（价格、销量、店铺、图片）时使用。对接AI数据平台，按次扣点，批量任务前可免费查询余额与单价。
version: 1.0.7
license: MIT
---

# Skill：小红书电商数据采集（xhs-shop-data）

对接「AI数据平台」，采集小红书商城（不是笔记/内容）的商品数据。
每次调用消耗平台点数，**单价以 `GET /api/v1/account/balance` 返回的 `price` 字段为准**
（当前统一 100 点/次 = 0.1 元，查询余额本身不扣点）。

## 一、前置条件（缺一不可，先向用户确认）

| 项 | 说明 |
|---|---|
| 平台地址 | **https://zlh.aidata366.com**（正式服务，直接可用）；也可用环境变量 `XHS_PLATFORM_BASE_URL` 覆盖 |
| API Key | **推荐直接运行 `login` 自动获取并保存到本机**（见下文「首次使用」）；也可显式设置环境变量 `XHS_PLATFORM_API_KEY`，优先级更高 |
| 点数 | 新用户注册赠送 1000 点；不足时按「六、客服与充值」联系客服充值（当前为人工充值） |

> 没有 Key 时不要尝试调用：会返回 `40100`，且浪费排查时间。先执行 `login` 拿 Key。

### 首次使用：一条命令完成登录（推荐）

没有 API Key 时，不要让用户手动去创建，直接执行：

```bash
python xhs_api.py login --skill-name xhs-shop-data --ai-entry claude-code
```

把输出里的「二维码图片 / 授权链接」发给用户，让用户扫码或打开链接登录并点「确认授权」。
用户确认后执行（pending 时退出码为 6，3~5 秒后重试即可）：

```bash
python xhs_api.py login_check --access-token <上一步输出的 access_token> --skill-name xhs-shop-data --ai-entry claude-code
```

成功后 API Key 会自动保存到 `~/.zhi_liao_hou/config.json`（仅本机），以后所有命令直接调用即可，
无需再设置环境变量；四个 skill 共用这份凭证。授权链接 10 分钟内有效且只能使用一次。

### 备选：手动注册 + 创建 Key（浏览器操作，约 1 分钟）

没有账号或自动登录失败时走这条路；**先注册，再执行上面的 `login`** 即可自动保存 Key。

1. **注册**：浏览器打开 `https://zlh.aidata366.com/auth/register?skill=xhs-shop-data`，填**手机号** →
   输入右侧**图片验证码** → 点「获取短信验证码」→ 填入收到的 6 位短信码 → 提交。
   **用户名和初始密码由平台自动分配**，注册成功页会一次性显示（请提醒用户立即记录）。
   注册即送 **1000 点**（同一 IP 每天最多注册 3 个账号）。注册必须由**用户本人在浏览器完成**
   （图片码与短信码无法、也不应被脚本绕过）。
2. **创建 API Key**：登录后进入左侧「API Key」页，起个名字点创建。**明文 Key 仅创建成功后
   的那一次页面显示**，立刻复制保存；关掉后只能看到前缀（`jh_` 开头 10 位），丢了只能重建。
3. **配置环境变量**后即可上手：
   ```bash
   export XHS_PLATFORM_BASE_URL="https://zlh.aidata366.com"
   export XHS_PLATFORM_API_KEY="jh_xxxxxxxx"
   ```

## 二、安装与 30 秒上手

**安装**：本 skill 只有两个文件（`SKILL.md` + `xhs_api.py`），`xhs_api.py` 为 **Python 纯标准库实现
（零第三方依赖，Python 3.8+ 可跑）**，把整个 `xhs-shop-data/` 目录放入 agent 的 skills 目录即完成安装。

## AI 调用来源参数（必填）

所有会访问后端 API 的命令必须携带 `--skill-name xhs-shop-data` 和
`--ai-entry <AI工具标识>`（如 `claude-code`）。IP 无需传递，由服务端自动获取。
首次缺参会告警放行，第二次起拒绝。
`login` / `login_check` 也建议携带这两个参数，其余采集命令必须携带。

```bash
export XHS_PLATFORM_BASE_URL="https://zlh.aidata366.com"
export XHS_PLATFORM_API_KEY="jh_xxxxxxxx"

python xhs_api.py balance --skill-name xhs-shop-data --ai-entry claude-code  # 免费：余额 + 各接口单价
python xhs_api.py search 玩偶 --out ./search_p1.json --skill-name xhs-shop-data --ai-entry claude-code  # 商品搜索
python xhs_api.py shop_list 5f3f2d9d6024760001911467 --skill-name xhs-shop-data --ai-entry claude-code  # 店铺商品列表
python xhs_api.py shop_detail 692eaf40e5da7400142c345a --skill-name xhs-shop-data --ai-entry claude-code  # 商品详情
```

参数支持三种写法：**位置参数** / **`key=value`** / **整段 JSON**：

```bash
python xhs_api.py shop_list seller_id=5f3f2d9d6024760001911467 sort=sales_qty page=1 --skill-name xhs-shop-data --ai-entry claude-code
python xhs_api.py search '{"keyword":"玩偶","page":1,"filters_tags":["现货"]}' --skill-name xhs-shop-data --ai-entry claude-code
```

## 三、命令一览（统一 100 点/次）

| 命令 | 平台接口 | 必填 | 可选 | 说明 |
|---|---|---|---|---|
| `search` | `/api/v1/xhs/product_search` | `keyword` | `page` `sort` `filters_tags` | 关键词搜商品，每页 20 条 |
| `shop_list` | `/api/v1/xhs/shop_list` | `seller_id` | `sort` `page` | 某店铺的在售商品，每页 20 条 |
| `shop_detail` | `/api/v1/xhs/shop_detail` | `goods_id` | — | 单商品详情（含图集） |
| `login` | `POST /auth/cli-session` | — | — | 扫码/链接登录授权（**免费、不扣点**，无需 API Key） |
| `login_check` | `POST /auth/cli-session/check` | `--access-token` | — | 校验授权并保存 API Key（**免费、不扣点**） |

### 参数说明

| 参数 | 说明 |
|---|---|
| `seller_id` | 小红书店铺 ID，24 位十六进制。可从 `search` 结果的 `content.vendor.seller_id` 取，或从店铺页链接取 |
| `goods_id` | 小红书商品 ID，24 位十六进制。可从 `shop_list` 的 `items[].item_id` 或 `search` 的 `content.id` 取 |
| `sort` | `shop_list`：`default` 综合 / `sales_qty` 销量 / `new_arrival` 上新；`search`：`综合` / `销量` / `最新` |
| `page` | **两个接口类型不同**：`shop_list` 必须传**字符串**（`page=1`，传数字上游会 422）；`search` 传**整数**（`page=1`）。CLI 已按接口自动转换，用 `key=value` 时照常写 `page=1` 即可 |
| `filters_tags` | 筛选标签**数组**。命令行用逗号分隔：`filters_tags=现货,七天无理由`；也可直接传 `["现货"]` |

## 四、返回结构与取值路径（重点，字段嵌套很深）

> 平台统一包了一层：`{"code":0,"msg":"success","data":{...,"_platform":{...}},"request_id":"req_..."}`。
> 下面写的路径都**省略开头的 `data.`**。上游的 `cost`/`balance` 已被平台剥离，不会出现在响应里。

### 4.1 `search` → 商品在 `module.data[].content`

```
data.module.data[]              # 每页 20 条
  └─ content
      ├─ id                     # 商品 ID（喂给 shop_detail 的 goods_id）
      ├─ title                  # 商品标题
      ├─ image                  # ⚠️ 是**数组**：[{url,width,height,aspect_ratio}]，不是字符串
      ├─ link                   # 深链 xhsdiscover://goods_detail/<id>?...
      ├─ price_info
      │    ├─ price             # 到手价
      │    ├─ origin_price      # 原价
      │    ├─ rds_price         # 折后价
      │    ├─ symbol            # ⚠️ 币种符号，实测可能返回 "$"
      │    └─ foreign_price     # ⚠️ 如 "≈$5.9"，出现时说明这条被按外币展示
      └─ vendor
           ├─ seller_id         # 店铺 ID（喂给 shop_list）
           ├─ vendor_name       # 店铺名
           ├─ vendor_link       # 店铺深链
           └─ vendor_id         # ⚠️ 名字叫 id，实际是**店铺头像 URL**（上游命名如此）
```

响应约 **437 KB**（含小红书搜索页的 DSL：`container`/`hierarchy`/`template`）。
**批量任务务必用 `--out` 落盘**，否则会刷屏并把上下文撑爆。

### 4.2 `shop_list` → 商品在 `items[]`

```
data.items[]                    # 每页 20 条
  ├─ item_id                    # 商品 ID（喂给 shop_detail）
  ├─ card_title                 # 商品标题
  ├─ desc                       # 描述（通常与标题相同）
  ├─ image                      # 主图 URL（字符串）
  ├─ link                       # 深链
  ├─ seller_id                  # 店铺 ID
  ├─ on_shelf_time              # 上架时间，**毫秒**时间戳
  ├─ stock_status               # 库存状态
  ├─ buyable / purchasable      # 是否可买
  └─ price_info
       ├─ expected_price.price  # 售价
       ├─ sku_price.price       # SKU 价
       └─ minor_price           # 划线价，**可能为 null**
```

### 4.3 `shop_detail` → 业务字段全在 `template_data[0]`

```
data.template_data[0]
  ├─ descriptionH5.name                   # 商品名称
  ├─ descriptionH5.skuId                  # 商品 ID
  ├─ priceH5.dealPrice.price              # 券后到手价
  ├─ priceH5.dealPrice.priceText          # 价格文案（如「券后价」）
  ├─ priceH5.highlightPrice               # 划线价
  ├─ sellerH5.name / id                   # 店铺名 / 店铺 ID
  ├─ sellerH5.salesVolume                 # 店铺总销量（字符串，如「已售 6.4万」）
  ├─ sellerH5.fansAmount                  # 粉丝数（字符串，如「粉丝数 4766」）
  ├─ sellerH5.grade                       # 店铺评分
  ├─ carouselH5.images[]                  # 轮播图，元素含 url / media / cover / videoId
  ├─ graphicDetailsV4.images[]            # 详情长图
  └─ variantsParams.list                  # 规格参数
```

⚠️ 两个坑：
1. `data.common_data` 和 `data.template` 是 **JSON 字符串**，要用时需要再 `json.loads` 一次
   （`common_data` 里有 `statisticInfo.skuNum` 等）。
2. `template_data` 是**数组**，业务字段裹在 `[0]` 里；不要直接去 `data.name` 取商品名。

## 五、错误码与处置

| code | 含义 | 怎么办 |
|---|---|---|
| 40100 / 40101 | Key 无效 / 已停用 | 检查 `XHS_PLATFORM_API_KEY`，或到平台重新创建 |
| 40200 | 点数不足 | 先 `balance` 估成本，引导用户充值；**不要重试** |
| 40201 | 接口未开放 | 该接口已停用，换接口或联系客服 |
| 40300 | 触发限频 | 等约 60 秒，降低并发 |
| 40911 | 同幂等键正在处理 | 等 2~3 秒用**同一个** `--idem` 键重试 |
| 40912 | 响应过大未缓存 | **本次未扣费**，换一个新 `--idem` 键重调即可 |
| 50000 | 本次取数失败（上游失败） | 看返回里的 `refunded`：有值表示已退点；**没退说明成本已产生**，不要盲目重试 |
| 50002 / 50003 | 上游超时 / 平台并发满 | 用同一幂等键重试，或降并发 |

CLI 已内置：可重试错误自动重试 1 次（复用同一幂等键，不会重复扣点）、
未知参数**本地拦截**（避免白扣点）、大响应提示落盘。

## 六、客服与充值

- 客服电话：**18722121663**（微信同号，扫码加客服微信在登录页底部）
- 充值目前为人工：提供注册手机号 + 充值金额，客服在后台加点
- 开票、接口定制、额度提升同样走客服

## 七、注意事项

- **只做小红书商城商品数据**，不含笔记/内容/达人口碑类接口。
- 分页：`shop_list` 与 `search` 都是每页 20 条、页码从 1 开始；**翻到底再继续翻会返回空数组**，
  但仍会扣点，批量采集请用"返回条数 < 20 就停"作为终止条件。
- 幂等：同一 `--idem` 键 + 同一接口 + 同一参数，重复请求**只扣一次点**；参数变了会被判 `40910`。
- 价格为平台原样透传，`symbol`/`foreign_price` 出现时说明该条被按外币展示，**不要直接当人民币用**。
