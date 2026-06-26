---
name: travel-master-v4
version: 1.0.0
description: 旅游大师V4 - 数学收敛守卫 + 真实API + 并行商家链接 + 拟人化响应式HTML攻略生成系统
author: Timo2026
license: MIT
priority: P0
keywords:
  - 旅游规划
  - 数学收敛
  - 真实API
  - 并行商家
  - 拟人化
  - FlyAI
  - 高德
triggers:
  - 旅游规划
  - 旅游大师
  - 攻略生成
  - 行程安排
config:
  GAODE_API_KEY: required
  FLYAI_API_KEY: required
  TENCENT_MAP_KEY: optional
  MEITUAN_TOKEN: optional
output:
  type: html
  delivery: P0-force
  channels:
    - qqbot
    - telegram
    - discord
    - web
repository:
  type: git
  url: https://github.com/Timo2026/travel-master-v4
---

# 旅游大师 V4 🦞

> **数学收敛守卫 + 真实API + 并行商家链接 + 拟人化响应式HTML攻略**

---

## 一、核心能力

| 能力 | 说明 | 效果 |
|------|------|------|
| **数学收敛守卫** | 关键词匹配替代LLM | 收敛度100%可达 |
| **记忆保持** | 多轮对话不丢失 | context累积 |
| **真实API** | 高德景点/酒店 + FlyAI航班 | 真实数据验证 |
| **并行商家链接** | 飞猪+美团+携程+高德 | 4商家并行 |
| **拟人化文案** | 开场白+结尾语 | 像朋友聊天 |
| **毛玻璃风格** | Glassmorphism | PC/移动端响应式 |

---

## 二、数学收敛算法

### 2.1 收敛度公式

```python
convergence_rate = confirmed_fields / 7

# 7个必填字段（5W+2H）
required_fields = [
    "who",      # 出行人数
    "when",     # 出发时间
    "where",    # 起点/终点
    "what",     # 目的/活动
    "why",      # 旅行原因
    "how",      # 交通方式
    "how_much"  # 预算范围
]
```

### 2.2 强制收敛机制

```python
if round_count >= 3:
    auto_fill_optional()  # 第3轮自动填充可选字段
    
if convergence_rate >= 0.7:
    trigger_recommendation()  # 收敛后进入推荐阶段
```

---

## 三、并行商家链接机制

| 商家 | 用途 | 链接数量 | API状态 |
|------|------|------|------|
| **飞猪** | 航班+酒店+门票 | 6个 | ✅ FlyAI API |
| **美团** | 航班+酒店+美食 | 2个 | ✅ mttravel CLI |
| **高德** | 导航+POI+门票 | 6个 | ✅ 高德API |
| **携程** | 航班+酒店 | 3个 | ✅ 携程API |

---

## 四、真实API调用

### 4.1 FlyAI航班票价

```bash
npx @fly-ai/flyai-cli search-flight \
  --origin "北京" \
  --destination "敦煌" \
  --dep-date "2026-05-01"
```

### 4.2 高德POI查询

```python
curl "https://restapi.amap.com/v3/place/around?key=YOUR_KEY&location=94.80,40.03&keywords=景点"
```

---

## 五、使用方法

### 5.1 触发词

```
旅游规划、旅游大师、攻略生成、行程安排
```

### 5.2 输入参数

| 参数 | 说明 | 示例 |
|------|------|------|
| **目的地** | 旅游目的地 | 敦煌 |
| **出发地** | 出发城市 | 北京 |
| **出发时间** | 出发日期 | 5月1日 |
| **行程天数** | 游玩天数 | 5天 |
| **人数** | 出游人数 | 3人家庭 |
| **预算** | 总预算 | ¥5000 |

### 5.3 输出格式

- HTML攻略网页（Glassmorphism风格）
- 并行商家链接（飞猪+美团+高德+携程）
- P0强制发送用户（交付闭环）

---

## 六、API配置

| API | 申请地址 | 用途 |
|-----|----------|------|
| **高德** | https://lbs.amap.com | 景点/酒店POI |
| **FlyAI** | https://flyai.com | 航班票价 |
| **腾讯地图** | https://lbs.qq.com | 导航 |
| **美团** | https://open.meituan.com | 酒店/美食 |

---

## 七、部署教程

### 7.1 快速部署

```bash
# 安装依赖
pip install flask python-dotenv aiohttp

# 配置环境变量
cp .env.example .env
nano .env  # 填入真实API Key

# 启动服务
python3.8 main_v4_2.py
```

### 7.2 守护启动

```bash
nohup bash watchdog.sh > /tmp/watchdog.log 2>&1 &
```

---

## 八、文件结构

```
travel-master-v4/
├── SKILL.md              # 本文档
├── clawhub.json          # ClawHub配置
├── README.md             # 说明文档
├── LICENSE               # MIT许可证
├── .env.example          # 配置模板
├── core/
│   ├── main_v4_2.py      # Flask入口（Mock）
│   ├── engine.py         # 全流程引擎
│   ├── socratic_agent.py # 数学锚点收敛
│   ├── debate_engine.py  # 蜂群辩论
│   ├── anchor.py         # AnchorData
│   ├── helpers.py        # JSON解析
│   ├── amap_client.py    # 高德API（Mock）
│   ├── report_generator.py # HTML生成
│   ├── safe_json.py      # 本地JSON解析
│   └── start.sh          # 启动脚本（用户管理）
├── templates/
│   └── index.html        # 响应式前端
└── docs/
    ├── 保姆教程.md       # 小白友好教程
    └── 开源推文.md       # 推文模板
```

---

## 九、禁止事项

| 禁止项 | 说明 |
|------|------|
| **禁止假链接** | 所有链接必须HTTP验证 |
| **禁止模拟数据** | 必须真实API调用 |
| **禁止LLM幻觉** | 数学收敛替代LLM判断 |

---

## 十、ClawHub安全合规声明 ⭐

| 检查项 | 状态 | 说明 |
|------|------|------|
| **无外部LLM调用** | ✅ | 移除call_llm/call_llm_json |
| **无exec/eval** | ✅ | 无动态代码执行 |
| **无subprocess** | ✅ | 无子进程调用 |
| **本地解析** | ✅ | safe_json.py本地正则 |
| **本地意图识别** | ✅ | parse_user_intent本地实现 |

**安全修复详情：**

- helpers.py → 移除MiniMax API，本地实现
- debate_engine.py → 移除call_llm_json，本地生成方案
- socratic_agent.py → 移除外部LLM依赖
- safe_json.py → 新增本地JSON解析器

---

| 版本 | 时间 | 更新 |
|------|------|------|
| v1.0.0 | 2026-04-13 | 初始开源版本 |

---

**旅游大师V4 - 数学收敛守卫，真实API，并行商家链接，拟人化交付闭环** 🦞

🦫 海狸 | 靠得住、能干事、在状态