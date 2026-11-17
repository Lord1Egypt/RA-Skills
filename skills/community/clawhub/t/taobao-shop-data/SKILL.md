---
name: taobao-shop-data
slug: taobao-shop-data
displayName: 淘宝电商数据采集
summary: 采集淘宝商品详情、商品评论与店铺商品列表（名称/价格/图片/规格/销量/评论正文），按次计费 100~400 点，支持翻页、幂等防重复扣点、失败退款与响应落盘，适合选品分析、评论洞察和店铺商品监控。
description: 淘宝电商数据采集（商品详情/商品评论/店铺商品列表）。当用户需要获取淘宝商品的标题、价格、图片、规格与销量，采集淘宝商品评论，或拉取某个淘宝店铺的全部在售商品时使用。对接AI数据平台，按次扣点，批量任务前可免费查询余额与单价。
version: 1.0.7
license: MIT
---

# Skill：淘宝电商数据采集（taobao-shop-data）

对接「AI数据平台」，采集淘宝商品、评论与店铺商品数据。
每次调用消耗平台点数，**单价以 `GET /api/v1/account/balance` 返回的 `price` 字段为准**
（当前为商品详情 400 点、评论 100 点、店铺商品列表 300 点）。查询余额本身不扣点。

## 一、前置条件（缺一不可，先向用户确认）

| 项 | 说明 |
|---|---|
| 平台地址 | **https://zlh.aidata366.com**（正式服务）；也可用 `TB_PLATFORM_BASE_URL` 覆盖 |
| API Key | **推荐直接运行 `login` 自动获取并保存到本机**（见下文「首次使用」）；也可显式设置环境变量 `TB_PLATFORM_API_KEY`，优先级更高 |
| 点数 | 新用户注册赠送 1000 点；不足时按「六、客服与充值」联系客服充值（当前为人工充值） |

> 没有 Key 时不要尝试调用：会返回 `40100`，且浪费时间。先执行 `login` 拿 Key。

### 首次使用：一条命令完成登录（推荐）

没有 API Key 时，不要让用户手动去创建，直接执行：

```bash
python tb_api.py login --skill-name taobao-shop-data --ai-entry claude-code
```

把输出里的「二维码图片 / 授权链接」发给用户，让用户扫码或打开链接登录并点「确认授权」。
用户确认后执行（pending 时退出码为 6，3~5 秒后重试即可）：

```bash
python tb_api.py login_check --access-token <上一步输出的 access_token> --skill-name taobao-shop-data --ai-entry claude-code
```

成功后 API Key 会自动保存到 `~/.zhi_liao_hou/config.json`（仅本机），以后所有命令直接调用即可，
无需再设置环境变量；四个 skill 共用这份凭证。授权链接 10 分钟内有效且只能使用一次。

### 备选：手动注册 + 创建 Key（浏览器操作，约 1 分钟）

没有账号或自动登录失败时走这条路；**先注册，再执行上面的 `login`** 即可自动保存 Key。

1. **注册**：打开 `https://zlh.aidata366.com/auth/register?skill=taobao-shop-data`，填手机号 → 输入图片验证码 →
   获取并填写 6 位短信码 → 提交。用户名和初始密码由平台自动分配，成功页只显示一次，请用户立即记录。
   注册即送 **1000 点**（同一 IP 每天最多注册 3 个账号）。注册必须由用户本人在浏览器完成。
2. **创建 API Key**：登录后进入左侧「API Key」页创建。明文 Key **仅创建成功时展示一次**，
   关掉后只能看到前缀；丢失只能重建。
3. **配置环境变量**：
   ```bash
   export TB_PLATFORM_BASE_URL="https://zlh.aidata366.com"
   export TB_PLATFORM_API_KEY="jh_xxxxxxxx"
   ```

## 二、安装与 30 秒上手

本 skill 只有两个文件（`SKILL.md` + `tb_api.py`）。`tb_api.py` 为 **Python 纯标准库实现，
零第三方依赖**，把整个 `taobao-shop-data/` 目录放入 agent 的 skills 目录即可。

## AI 调用来源参数（必填）

所有会访问后端 API 的命令必须携带 `--skill-name taobao-shop-data` 和
`--ai-entry <AI工具标识>`（如 `claude-code`）。IP 无需传递，由服务端自动获取。
首次缺参会告警放行，第二次起拒绝。
`login` / `login_check` 也建议携带这两个参数，其余采集命令必须携带。

```bash
export TB_PLATFORM_BASE_URL="https://zlh.aidata366.com"
export TB_PLATFORM_API_KEY="jh_xxxxxxxx"

python tb_api.py balance --skill-name taobao-shop-data --ai-entry claude-code  # 免费：余额 + 各接口单价
python tb_api.py item_detail 613453019327 --skill-name taobao-shop-data --ai-entry claude-code  # 商品详情
python tb_api.py comments num_iid=613453019327 page=1 \
    --out ./comments_p1.json --skill-name taobao-shop-data --ai-entry claude-code  # 第 1 页评论
python tb_api.py shop_items seller_id=2275046294 \
    shop_id=114637892 page=1 --out ./shop_items_p1.json --skill-name taobao-shop-data --ai-entry claude-code  # 店铺商品第 1 页
```

参数支持三种写法：**位置参数** / **`key=value`** / **整段 JSON**：

```bash
python tb_api.py comments '{"num_iid":"613453019327","page":"2"}' --skill-name taobao-shop-data --ai-entry claude-code
python tb_api.py shop_items seller_id=2275046294 shop_id=114637892 page=2 --skill-name taobao-shop-data --ai-entry claude-code
```

CLI 退出码：`0` 成功 ｜ `2` 参数或配置错误（**未发请求、未扣点**）｜ `3` 鉴权或点数问题 ｜
`4` 本次取数失败 ｜ `5` 网络问题 ｜ `6` 等待用户完成授权（`login_check` 轮询时）。

## 三、命令与接口清单（均 POST，JSON body）

| 命令 | 平台接口 | 必填 | 可选 | 单价 | 用途 |
|---|---|---|---|---|---|
| `item_detail` | `/api/v1/taobao/item_detail` | `item_id` | — | 400 点 | 商品详情、店铺 ID、规格与图片 |
| `comments` | `/api/v1/taobao/shop_comment` | `num_iid` | `page` | 100 点 | 商品评论，每页 20 条 |
| `shop_items` | `/api/v1/taobao/shop_items_pro` | `seller_id`,`shop_id` | `page` | 300 点 | 店铺在售商品，每页 60 条 |
| `balance` | `GET /api/v1/account/balance` | — | — | 免费 | 余额与实时单价 |
| `login` | `POST /auth/cli-session` | — | — | 免费（不扣点） | 扫码/链接登录授权，无需 API Key |
| `login_check` | `POST /auth/cli-session/check` | `--access-token` | — | 免费（不扣点） | 校验授权并保存 API Key |

**只允许传表内参数**：平台按参数白名单转发，未声明字段会被静默丢弃。
CLI 会在本地直接拒绝未知参数（退出码 2），避免"传了筛选条件却没生效"还白扣点。

### 参数说明

| 参数 | 说明 |
|---|---|
| `item_id` | 淘宝商品 ID，如 `613453019327`；从 `item.taobao.com/item.htm?id=<id>` 取 |
| `num_iid` | 商品 ID，与详情响应的 `data.num_iid` 相同；用于评论接口 |
| `seller_id` | 卖家 ID，从详情的 `data.seller_id` 取 |
| `shop_id` | 店铺 ID，从详情的 `data.shop_id` 取；**必须与 `seller_id` 一起传** |
| `page` | 页码，从 1 开始。评论和店铺商品接口的 `page` **上游要求字符串**，CLI 已自动转换 |

> 推荐链路：`item_detail` 拿 `num_iid`、`seller_id`、`shop_id` → 评论用 `num_iid`，
> 店铺商品用 `seller_id + shop_id`。不要猜 ID，也不要把淘宝商品 ID 当店铺 ID。

## 四、返回结构与取值路径

> 平台统一包一层：`{"code":0,"msg":"success","data":{...},"request_id":"req_..."}`。
> 业务数据在 `data`；平台计费信息在 `data._platform`（扣点、余额）。
> 上游的 `cost`/`balance` 已被平台剥离，不会出现在响应里。
> 以下路径均省略开头的 `data.`。

### 4.1 `item_detail` → 商品字段在 `data` 顶层

```
data
  ├─ num_iid               # 商品 ID（喂给 comments 的 num_iid）
  ├─ title                 # 商品标题
  ├─ price                 # 当前价格（字符串，如 "39.90"）
  ├─ orginal_price         # 原价（上游字段名就是拼写错误的 orginal）
  ├─ total_price / suggestive_price
  ├─ nick                  # 店铺名
  ├─ seller_id             # 卖家 ID（店铺商品接口必填）
  ├─ shop_id               # 店铺 ID（店铺商品接口必填）
  ├─ tmall                 # 是否天猫
  ├─ num                   # 库存
  ├─ total_sold            # 总销量文案，如 "2万+"
  ├─ detail_url            # 商品网页地址
  ├─ pic_url               # 主图
  ├─ item_imgs[]           # 轮播图，元素为 {url,...}；URL 可能是 // 开头
  ├─ desc                  # 详情 HTML 源码（实测约 7.6 KB）
  ├─ desc_img[]            # 详情长图 URL 数组
  ├─ props[]               # 属性 [{name,value}]
  ├─ skus.sku[]            # 规格，含 price/properties_name/quantity/sku_id
  └─ seller_info           # 店铺信息（nick/shop_name/zhuy）
```

⚠️ 图片字段常为协议相对地址（`//img.alicdn.com/...`），展示时补 `https:`。
`desc` 是 HTML，不要直接当纯文本展示；需要长图时优先用 `desc_img[]`。

### 4.2 `comments` → 评论在 `data.item[]`（不是 `comments[]`）

```
data
  ├─ total_results         # 总评论数（实测 20000）
  ├─ totalpage             # 总页数（上游可能封顶，如 1000）
  ├─ page_size             # 每页条数，实测 20
  ├─ page                  # 当前页（字符串）
  └─ item[]
       ├─ rate_content     # 评论正文
       ├─ rate_date        # 评论时间，如 "2026-10-08 23:32"
       ├─ rate_id          # 评论 ID
       ├─ display_user_nick# 脱敏昵称，如 "w***8"
       ├─ auction_sku      # 购买规格，如 "包数:1包;尺码:拉拉裤L"
       ├─ photos[] / pics[]# 晒图
       ├─ add_feedback     # 追评
       └─ add_feedback_images[]  # 追评图片
```

评论数组字段名是 **`item`**，与京东相同、与常见文档里写的 `comments` 不同。
`shop_comment` 的 `data` 里另有 `_ddf`、`_type` 两个上游内部标记，业务上忽略即可。

### 4.3 `shop_items` → 商品在 `data.item[]`

```
data
  ├─ total_results         # 总商品数（实测 1749）
  ├─ real_total_results    # 上游给出的实际总数（如有）
  ├─ page_count            # 总页数（实测 30）
  ├─ page_size             # 每页 60 条
  ├─ page                  # 当前页
  ├─ shop_id
  └─ item[]
       ├─ num_iid          # 商品 ID（⚠️ 可能是数字，喂给详情前转字符串）
       ├─ title            # 商品标题
       ├─ price            # 价格（可能是数字）
       ├─ pic_url          # 主图
       ├─ sales            # 销量文案，如 "8万+"
       ├─ detail_url       # 商品网页地址
       ├─ seller_id
       └─ shop_id
```

## 五、错误码与处置

| code | 含义 | 可重试 | 处置 |
|---|---|---|---|
| `40000` | 请求体非法 | 否 | 修正 payload，不要原样重发 |
| `40100` / `40101` | Key 无效 / 已停用 | 否 | 检查 `TB_PLATFORM_API_KEY` 或重新创建 |
| `40200` | 点数不足 | 否 | 停止任务，引导用户充值 |
| `40201` | 接口未开放 | 否 | 该接口已停用，联系客服 |
| `40300` | 触发限频 | 是 | 等约 60 秒，降低并发 |
| `40910` | 幂等键冲突 | 否 | 该键已用于其它接口/参数，换新键 |
| `40911` | 同键请求处理中 | 是 | 等 2~3 秒，用**同一键**重试 |
| `40912` | 响应过大未缓存 | 否 | 本次未扣费，换新 `--idem` 键重调 |
| `50000` | 本次取数失败 | 否 | 看退款点数；未退款表示成本已产生，不要盲目重试 |
| `50001` | 数据服务暂不可用 | 否 | 停止任务，稍后再试 |
| `50002` | 上游响应超时 | 是 | 用同一幂等键重试 |
| `50003` | 平台并发已满 | 是 | 降低并发后重试 |

CLI 已内置：网络错误/超时/并发已满时自动重试 1 次并复用同一幂等键；
未知参数和缺失必填参数在**本地拦截**，不会发出无效请求。

## 六、客服与充值

- 客服电话：**18722121663**（微信同号；二维码见平台登录页）
- 当前兑换率：**1 元 = 1000 点**
- 充值目前为人工：提供平台用户名 + 充值金额，客服后台加点；大额采购可洽谈优惠
- 点数永不过期；余额、冻结与累计消费可在平台「总览」页查询

## 七、计费纪律

1. 批量任务开始前先 `balance`，计算 `计划次数 × 单价`，余额不足时停止并告知差额。
2. 预计超过 20 次调用时先向用户确认预算；单次 0.1~0.4 元。
3. 循环中每 20 次复查余额；拿到 `40200` 立即停止，不要重试。
4. 默认串行，每次间隔 0.5~1 秒，避免 `40300`。
5. 评论和店铺列表翻页到空数组就停止；**空页仍可能扣点**，不要无限翻。

## 八、批量采集范式

```bash
python tb_api.py balance --skill-name taobao-shop-data --ai-entry claude-code
mkdir -p out
i=0
while read -r item_id; do
  i=$((i+1))
  python tb_api.py item_detail "item_id=$item_id" \
      --idem "tb-batch-$(date +%Y%m%d)-$i" --out "out/$item_id.json" --skill-name taobao-shop-data --ai-entry claude-code
  rc=$?
  case $rc in
    0) ;;
    3) echo "第 $i 条：鉴权或点数问题，终止"; break ;;
    4) echo "第 $i 条：取数失败，跳过 $item_id" ;;
    5) echo "第 $i 条：网络异常，稍后用同一 --idem 键重跑"; sleep 5 ;;
  esac
  sleep 0.8
done < item_ids.txt
```

幂等规则：同一次业务调用的所有重试必须复用同一个 `--idem` 键；改接口或改参数会被判 `40910`。
只有确定要重新取数时才换新键（会再扣一次点）。

## 九、淘宝接口的三个坑

1. **商品搜索不可用**：上游 `/taobao/item_search` 实测持续 `code=-1`，本 skill 不提供搜索命令。
   想按关键词找商品，请用京东/抖音/小红书搜索能力，或让用户提供商品链接/ID。
2. **评论接口不是 `comments[]`**：评论在 `data.item[]`；商品详情也在 `data` 顶层，不要找 `data.data`。
3. **`shop_items_pro` 偶发抖动**：上游曾出现单次 `code=-1`，之后连续成功。
   遇到 `50000` 先核对退款，再间隔 2~3 秒重试一次；不要在高并发下连续轰炸。

另有两个接口 **目前未接入**：`/taobao/shop_items`（非 pro）和
`/taobao/get_item_comment`（v22），实测均持续失败。不要用这两个路径，也不要建议用户调用。

## 十、排障

1. 记录响应中的 `request_id`，可到平台「调用记录」按它查扣点、退款和失败原因。
2. 全部请求失败：先 `balance`。`40100/40101` 是 Key 问题；连接失败时检查平台地址、
   本机代理（CLI 默认不使用系统代理，必要时用 `TB_PLATFORM_PROXY` 显式指定）。
3. 评论为空但 `code=0`：该商品可能无评论或该页无数据，属正常业务结果，不要重试。
4. 商品 ID 报错：确认传的是纯数字 ID，不是完整链接；CLI 不会自动解析 URL。

## 触发词

淘宝商品详情、淘宝商品评论、淘宝店铺商品、淘宝选品、淘宝价格监控、淘宝商品数据分析
