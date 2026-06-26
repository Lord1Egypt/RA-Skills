---
name: tianshu-script-analyzer
description: 🎭 天枢剧本库：短剧爆款因子分析。输入剧名返回爆款因子分析报告（免费预览：基础画像+核心结论 / 完整版：7维度深度拆解+可复用公式）。数据覆盖200+部短剧，面向国内短剧行业人士。当用户询问：短剧分析、爆款原因、剧本评估、某部剧为什么火时触发。
---

# 🎭 天枢剧本库（v1.0.0）

短剧爆款因子分析引擎。输入一部短剧的剧名或关键词，返回该剧的**爆款因子分析报告**——为什么火？靠什么火的？这套模式能不能复制？

**支持支付宝支付（9.90元/次），仅限国内用户。**

---

## 报告ID速查

| 剧名 | API ID |
|------|--------|
| 十八岁太奶奶驾到，重整家族荣耀 | `shaobing_tainainai` |
| 好一个乖乖女 | `guai_guai_nu` |
| 冒姓琅琊 | `maoxing_langya` |
| 重生之我在霸总短剧里当保姆 | `bazong_baomu` |
| 阴差阳错，成了老板的女仆 | `laoban_nvpu` |
| 离婚后，爸妈带我走上巅峰 | `lihun_fumudai` |
| 隐身侍卫 | `yinshen_shiwei` |
| 九个太阳，我们是九个外甥女 | `jiuge_taiyang` |

> 用户输入剧名不精确也没关系，Agent 拿到目录后模糊匹配。

---

## Agent 工作流程

### 报告查询
1. 用户输入剧名 → Agent 调 `GET /v1/analyzer/plays` 获取目录，本地模糊匹配
2. 调 `GET /v1/analyzer/report?id=xxx` 返回免费预览（基础画像+核心结论）
3. 如需完整版，Agent 调 `GET /v1/analyzer/report?id=xxx&alipay_trade_no=ORDER_xxx` 返回完整报告

### 支付流程（仅限国内用户，支付宝）
1. Agent 调 `GET /api/analyzer-alipay/create-order?amount=9.90&subject=天枢剧本库-爆款因子分析报告` → 返回 `shortLink` 和 `out_trade_no`
2. 拼上域名：`https://sinodata.io/api/analyzer-alipay/go/ORDER_xxx`，向用户展示此链接
3. 用户打开链接 → 302跳转到支付宝 → 完成支付
4. Agent 调 `GET /api/analyzer-alipay/query?trade_no=ORDER_xxx` 确认支付状态
5. `trade_status === "TRADE_SUCCESS"` → 带 `alipay_trade_no` 调完整版报告

### API 端点

通过 `https://sinodata.io` 访问。所有分析器API走独立3003服务（与黄道库完全隔离）。

### 付费接口（需 alipay_trade_no）

#### 一、爆款因子分析报告（完整版）

```
GET https://sinodata.io/v1/analyzer/report?id=shaobing_tainainai&alipay_trade_no=ORDER_xxx
```

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| id | 是 | 报告ID（如上表） |
| alipay_trade_no | 是（付费版） | 支付宝支付订单号（ORDER_开头） |

**返回（付费）：**
- `type: "full"` — 标识完整版
- `report_id` — 报告ID
- `content` — 完整报告全文（Markdown格式，约3000-8000字）

**返回结构：**
1. ✅ **免费预览部分**：基础画像 + 300字核心结论
2. 🔒 **完整版包含**：
   - 一、基础数据层（成绩画像+市场定位）
   - 二、选题与赛道策略（蓝海指数+话题杠杆+金手指）
   - 三、用户心理与情绪共鸣（爽感结构+嘴替效应+解压阀）
   - 四、剧本结构与叙事节奏（钩子系统+反转设计+付费点）
   - 五、表演与角色魅力（角色设计+表演技法）
   - 六、视听语言与竖屏语法（10项适配度评估）
   - 七、社会情绪与时代共鸣
   - 八、商业模式与分发
   - 九、可复用公式（创作者可直接套用）

---

### 免费接口

#### 二、报告预览（免费）

```
GET https://sinodata.io/v1/analyzer/report?id=shaobing_tainainai
```

**返回：**
- `type: "preview"` — 标识免费预览
- `report_id` — 报告ID
- `content` — 基础画像+核心结论摘要（约1000-1500字）
- `pay_link` — 支付宝创单链接

#### 三、剧集目录（免费）

```
GET https://sinodata.io/v1/analyzer/plays?limit=200
```

返回所有可查询剧集的基础信息（剧名、类型标签、核心设定）。

推荐的模糊搜索策略：Agent 获取目录后在本地匹配用户输入。

#### 四、支付宝创单

```
GET https://sinodata.io/api/analyzer-alipay/create-order?amount=9.90&subject=天枢剧本库-爆款因子分析报告
```

**返回：**
- `success` — Boolean
- `payUrl` — 支付宝原生支付链接
- `shortLink` — 短跳转路径（如 `/api/analyzer-alipay/go/ORDER_xxx`）
- `out_trade_no` — 订单号（ORDER_开头）
- `amount` — 金额

#### 五、支付宝短跳转（推荐使用）

```
GET https://sinodata.io/api/analyzer-alipay/go/ORDER_xxx
```

**说明：** Agent 用 `shortLink` 拼上域名生成最终支付链接。服务端缓存payUrl，302跳转到支付宝。链接短，不会被截断。缓存5分钟有效。

#### 六、支付宝查询

```
GET https://sinodata.io/api/analyzer-alipay/query?trade_no=ORDER_xxx
```

#### 六、支付宝查询

```
GET https://sinodata.io/api/analyzer-alipay/query?trade_no=ORDER_xxx
```

**返回：**
- `success` — Boolean
- `trade_status` — `WAIT_BUYER_PAY` / `TRADE_SUCCESS` / `TRADE_CLOSED`

---

## 报告全貌（付费版包含的内容）

付费9.90元解锁的完整版包含以下模块：

### 一、基础数据层（爆款画像的"身份证"）
- 剧名、类型、出品方、导演、主演
- 播放量、热力值、榜单排名
- 上线时间线、日榜周榜月度趋势

### 二、选题与赛道策略
- 蓝海指数：这个题材在短剧赛道中的独特程度
- 话题杠杆率：剧集的社交媒体传播效率
- 金手指新颖度：金手指设定的创新性

### 三、用户心理与情绪共鸣
- 确定性的爽感：观众为什么愿意追下去
- 嘴替效应：角色替观众说出不敢说的话
- 解压阀机制：情绪释放的方式和效率

### 四、剧本结构与叙事节奏
- 前30秒钩子系统（如有批1数据）：0-3秒/3-10秒/10-30秒的逐秒拆解
- 全剧钩子类型分布（反转型/悬念型/情绪断裂型/日常型）
- 反转设计策略（每集约/5集约/全剧级三层结构）
- 付费点卡点设计

### 五、表演与角色魅力
- 核心角色的符号化设计
- 表演技法与演员适配度
- 表情、动作、台词的记忆点

### 六、视听语言与竖屏语法
- 10项竖屏表现手法适配度评估
- 竖屏镜头语言的亮点分析

### 七、社会情绪与时代共鸣
- 时代情绪捕捉度
- 公共议题转化能力
- 文化符号运用

### 八、商业模式与分发
- IAP/IAA匹配度
- 算法友好度
- 广告植入空间
- IP潜力

### 九、可复用公式（核心资产）
- 3-6条创作者可直接套用的经验
- 每个经验附具体操作建议

---

## 数据覆盖

当前子库包含8部深度分析报告，涵盖多种短剧类型：

| 类型 | 代表作品 | 数据来源 |
|------|---------|---------|
| 穿越女频 | 十八岁太奶奶驾到 | 四源合一（最丰富） |
| 女频复仇甜宠 | 好一个乖乖女 | 三源合一 |
| 古装权谋 | 冒姓琅琊 | 三源合一 |
| 职场吐槽 | 重生之我在霸总短剧里当保姆 | 三源合一 |
| 霸总甜宠 | 阴差阳错，成了老板的女仆 | 三源合一 |
| 豪门逆袭 | 离婚后爸妈带我走上巅峰 | 双源 |
| 男频异能 | 隐身侍卫 | 双源 |
| 系统亲情 | 九个太阳我们是九个外甥女 | 双源 |

---

## 扣费机制

- **价格：** 9.90元/次（支付宝）
- **付费项目：** 爆款因子分析报告完整版（所有剧集）
- **免费赠送：** 基础画像+核心结论预览、剧集目录
- **流程：** Agent 创单 → 拿到shortLink → 拼域名给用户（302跳转）→ 用户支付 → Agent 带订单号调API
- **验证：** 独立3003支付服务，与黄道库完全隔离

---

## 隐私与条款

- 本服务不存储用户个人信息
- 支付信息由支付宝处理，服务端仅保留订单号和支付状态
- 报告内容基于已公开发布作品的合理引用与分析
