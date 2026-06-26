# 行业适配手册

> 各行业 TG 搜索策略、两步法命令示例、已知高价值频道、实战经验。
> 主 Skill 文档 `SKILL.md` 只保留速查表，详细内容见本文档。

---

## 行业关键词映射

| 目标行业 | 正确的 TG 搜索关键词 | ❌ 无效关键词 | 说明 |
|----------|---------------------|---------------|------|
| 🎮 游戏 | 游戏名、外挂、辅助、破解、Crack | 优惠券、漏洞单 | 游戏黑产集中在破解/外挂频道 |
| 🥛 快消/零售 | 优惠券、薅羊毛、漏洞、线报、Bug价、0元购 | 外挂、破解 | 快消黑产集中在羊毛/优惠券频道 |
| 💰 金融/投资 | 套利、路子、代刷、水钱 | 外挂、优惠券 | 金融黑产集中在套利/代刷群 |
| 📱 App/工具 | 破解版、Mod、去广告、解锁 | 优惠券、外挂 | App 黑产集中在破解/Mod 频道 |
| 💬 社交/交友 | 交友、同城约、号商、引流、脚本、代聊 | 外挂、优惠券 | 社交黑产集中在引流/灰产号群 |
| ✈️ 航司/OTA | 里程、积分、代订、机票诈骗、退改签 | 外挂、破解 | 航司黑产集中在里程买卖/诈骗群 |
| 🚗 汽车 | 二手车、车贷、违章、代办、改表 | 优惠券、外挂 | 汽车黑产集中在车贷诈骗/灰产代办 |

---

## 🎮 游戏行业

```bash
# 标准两步法
python3 main.py --mode hybrid \
  --keywords "无尽冬日,Whiteout Survival,辅助,外挂" \
  --backfill-keywords "无尽冬日,辅助,破解" \
  --targets gaming \
  --env ../config/.env
```

## 🥛 快消/零售

```bash
# 第1步：发现羊毛频道（搜生态词）
python3 main.py --mode discover \
  --keywords "优惠券,薅羊毛,漏洞单,线报,Bug价,0元购" \
  --targets retail \
  --env ../config/.env

# 第2步：回溯品牌关键词
python3 main.py --mode backfill \
  --keywords "伊利,安慕希,金典,纯牛奶" \
  --backfill-keywords "伊利,安慕希,金典,纯牛奶" \
  --targets retail \
  --env ../config/.env
```

### 已知高价值羊毛频道

| 频道 | username | 类型 | 说明 |
|------|----------|------|------|
| 今日有羊毛 | @jdbroo | 综合线报 | 涵盖 Bug价、小程序活动、抽奖 |
| 薅羊毛 | @xbcia | 淘宝/京东线报 | 高活跃、伊利产品频繁出现 |
| 超级薅羊毛党 | @superbuffg | 综合羊毛 | 3.27K 成员，奶粉/雪糕/牛奶 |
| 羊毛捡漏中心 | @supershop66 | 捡漏/优惠 | 伊利全线产品低价线报 |
| 优惠线报 | @get_coupons | 拼多多/京东 | CPS推广为主，批量发布 |

### 快消品牌舆情替代渠道（TG 不足时）

| 渠道 | 寻址方式 | 适用场景 |
|------|----------|----------|
| 黑猫投诉 | `web_search: "品牌名 site:12315.cn"` | 消费者投诉/产品质量 |
| 知乎 | `web_search: "品牌名 site:zhihu.com"` | 深度分析/行业讨论 |
| 微博 | `web_search: "品牌名 投诉 OR 曝光"` | 舆情爆发/话题传播 |
| 天眼查/裁判文书 | `web_search: "品牌名 诉讼"` | 法律纠纷/窜货案件 |

## 💬 社交/交友

```bash
# 第1步：发现灰产引流群
python3 main.py --mode discover \
  --keywords "交友,同城,号商,引流,聊单,脚本,注册机" \
  --targets social \
  --env ../config/.env

# 第2步：回溯品牌关键词
python3 main.py --mode backfill \
  --keywords "探探,陌陌,Soul,积目,他趣" \
  --backfill-keywords "探探,陌陌,Soul,积目,他趣" \
  --targets social \
  --env ../config/.env
```

## ✈️ 航司/OTA

```bash
# 第1步：发现航旅灰产群
python3 main.py --mode discover \
  --keywords "里程,积分,代订,机票,退改签,选座" \
  --targets airline \
  --env ../config/.env

# 第2步：回溯品牌关键词
python3 main.py --mode backfill \
  --keywords "国航,南航,东航,海航,携程,飞猪,去哪儿,亚万" \
  --backfill-keywords "国航,南航,东航,海航,携程,飞猪,去哪儿,亚万" \
  --targets airline \
  --env ../config/.env
```

## 🚗 汽车

```bash
# 第1步：发现汽车灰产群
python3 main.py --mode discover \
  --keywords "车贷,二手车,违章代办,改表,套牌,代处理" \
  --targets auto \
  --env ../config/.env

# 第2步：回溯品牌关键词
python3 main.py --mode backfill \
  --keywords "大众,丰田,本田,宝马,奔驰,比亚迪,4S,车险" \
  --backfill-keywords "大众,丰田,本田,宝马,奔驰,比亚迪,4S,车险" \
  --targets auto \
  --env ../config/.env
```

---

## 实战经验

### 2026-06-03：伊利集团（快消行业）

**教训：** 不同行业的 TG 黑产生态完全不同。用游戏行业的「搜外挂」策略去搜快消品牌 → 零产出。

**关键发现：**
- 快消品牌不靠破解/外挂，靠的是**优惠券漏洞利用 + 小程序批量薅福利 + Bug价线报**
- 正确路径：搜「优惠券/薅羊毛/线报/漏洞单」→ 发现羊毛频道 → 在频道内搜品牌名
- TG Web 端 `?q=` 参数可作为 Flood Wait 时的应急扫描手段
- web_fetch 只能获取最近 ~20 条，不可替代完整 backfill

### 2026-06-03：IP 代理池架构搭建

**教训：** Flood Wait 的根因不是账号不够，是 IP 太单一。TG 限速按 `(IP, 账号)` 二维统计，三账号走同一 IP → 三个窗口共享同一个 IP 维度的请求配额。

**已实现：** 三账号代理隔离 + SOCKS5 认证，详见 `references/proxy-pool-setup.md`。

### 2026-06-03：三账号切换

配置：`.env` 中 `TG1_*` + `TG2_*` + `TG3_*` 三组凭证。`--account 2` / `--account 3` 切换备号。`--failover N` 自动 failover。

### 2026-06-02：迷你枪战精英（游戏行业）

**结论：** 游戏行业搜「游戏名 + 外挂/辅助」→ 直接命中破解频道，遵循标准 TG 搜索策略，不需要特殊适配。
