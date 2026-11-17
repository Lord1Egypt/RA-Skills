# 薅羊毛助手·全网比价领券 · WorkBuddy Skill

怕买贵怕漏券？一句话全网比价领券。12 大生活场景意图路由：电商购物/吃喝外卖/出行旅宿/数码家电/会员文娱/金融支付/教育成长/健康医疗/宠物/政府公共/AI数字服务/副业变现。

## 解决什么问题

- **"XX 哪里买最便宜？"** → 一句话比价淘宝/京东/拼多多/苏宁/唯品会/抖音 6 大平台，返回最低价和优惠券
- **"今天外卖有什么红包？"** → 实时拉取美团/饿了么/京东外卖/淘宝闪购 20+ 活动，附一键领券链接
- **"信用卡/会员/医疗/消费券有什么优惠？"** → RSS 五场景聚合官方权威域名信息（Bing 数据源，国内可直连）
- **"这个淘宝链接转成返佣链接"** → 淘宝联盟转链（🟡 待上线，邀约制权限申请中）

**已上线**：外卖红包、跨平台比价、Coze 兜底、美团本地、AI Token、RSS 五场景
**🟡 待上线**：淘宝关键词选品（appkey 需基于媒体备案创建）、万能转链（邀约制）

## 服务架构（重要）

主通道走作者提供的远程服务端（`http://8.148.235.41:8001`），使用者零配置：

| 通道 | 端点 |
|------|------|
| 外卖红包 | `GET /api/waimai?section=外卖` |
| 跨平台比价 | `GET /api/compare?q=关键词` |
| RSS 五场景 | `GET /api/rss/{s5,s6,s8,s10,s12}` |

> ⚠️ 该服务由作者个人维护，非商业服务，可能不稳定或暂停。每个通道均有本地备用脚本（`scripts/` 下免 key 可独立运行），详见 SKILL.md「服务架构说明」。

## 安装

### WorkBuddy 技能市场（推荐）

在 WorkBuddy 中搜索「薅羊毛助手·全网比价领券」一键安装。

### 手动安装

```bash
git clone https://github.com/guipi888/wool-hunter.git \
  ~/.workbuddy/skills/薅羊毛助手
```

### 环境依赖

- Python ≥ 3.10（纯标准库，本地备用脚本无需第三方依赖）
- 远程主通道：只需能访问 `http://8.148.235.41:8001`
- Coze 兜底通道：需自配 token（环境变量 `COZE_API_TOKEN`）

## 使用

作为 WorkBuddy 技能，由 Agent 按场景自动路由调用。手动验证命令：

```bash
# 比价（6 大平台）
curl -s "http://8.148.235.41:8001/api/compare?q=抽纸"

# 外卖红包（全部活动）
curl -s "http://8.148.235.41:8001/api/waimai"

# RSS 五场景（带默认关键词）
curl -s "http://8.148.235.41:8001/api/rss/s6"
```

本地备用脚本（免 key）：

```bash
python3 scripts/xiaxiayouhui.py search '蓝牙耳机'
python3 scripts/s6_finance.py "信用卡优惠"
```

## 项目结构

```
SKILL.md                    # 技能说明（12 场景路由 + 各通道详细用法）
README.md                   # 本文件
LICENSE                     # MIT
scripts/
├── xiaxiayouhui.py         # 跨平台比价（本地备用）
├── huilife.py              # 惠生活外卖红包（本地备用，需自配密钥）
├── rss_common.py           # RSS 公共模块（Bing Web RSS + host 过滤）
├── s5_entertainment.py     # S5 会员文娱（本地备用）
├── s6_finance.py           # S6 金融支付（本地备用）
├── s8_health.py            # S8 健康医疗（本地备用）
├── s10_public.py           # S10 政府公共（本地备用）
├── s12_affiliate.py        # S12 副业变现（本地备用）
├── taobao_affiliate.py     # 淘宝联盟选品/转链（🟡 待上线）
├── call_bot.py             # Coze 兜底（需自配 token）
└── search.py               # 旧版比价（🟡 待修复：缺 aiohttp）
```

## 输出

各通道返回结构化 JSON / 终端表格：商品名、平台、原价、到手价、优惠券、店铺、领券链接；RSS 返回标题、来源、时间、直链（官方/权威域名过滤）。

## 关于作者

**桂皮 Guipi** — AI Agent 开发者 · 超级个体践行者
专注 AI 效率工具与一人公司方法论，帮普通人用 AI 成为超级个体

| 平台 | 账号 |
|------|------|
| 📱 小红书 | [桂皮AI实战](https://www.xiaohongshu.com/user/profile/5a409dda44363b313b9d7e15) |
| 🎬 抖音 | [桂皮AI实战](https://v.douyin.com/QJRjHGAtrvA/) |
| 📺 视频号 | 微信内搜「桂皮AI实战」 |
| 💬 公众号 | 微信搜「桂皮AI实战」 |
| 🌟 知识星球 | [AI超级个体](https://t.zsxq.com/guSUk) — AI工具 · 创作 · 产品 · 流量 · 变现 |
| 🐙 GitHub | [guipi888](https://github.com/guipi888) |
| 💬 微信 | guipi996（注明来意） |

## License

MIT License — 详见 [LICENSE](./LICENSE)

原始惠生活逻辑移植自开源项目 [YKred/waimaiquan-skill](https://github.com/YKred/waimaiquan-skill)（MIT），保留原作者版权。
