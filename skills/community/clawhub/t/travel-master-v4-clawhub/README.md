# 旅游大师 V4 🦞

> **数学收敛守卫 + 真实API + 并行商家链接 + 拟人化响应式HTML攻略**

---

## 功能特点

| 特点 | 说明 |
|------|------|
| **数学收敛守卫** | 关键词匹配替代LLM，收敛度100%可达 |
| **记忆保持** | 多轮对话不丢失，context累积 |
| **真实API** | 高德景点/酒店 + FlyAI航班票价 |
| **并行商家链接** | 飞猪+美团+高德+携程4商家并行 |
| **拟人化文案** | 开场白+结尾语，像朋友聊天 |
| **毛玻璃风格** | Glassmorphism，PC/移动端响应式 |

---

## 快速开始

### 安装

```bash
# ClawHub一键安装
clawhub install travel-master-v4

# 手动安装
git clone https://github.com/Timo2026/travel-master-v4.git
pip install flask python-dotenv aiohttp
```

### 配置

```bash
# 复制配置模板
cp .env.example .env

# 填入真实API Key
nano .env
```

### 启动

```bash
python3.8 core/main_v4_2.py
```

---

## API申请地址

| API | 地址 | 用途 |
|-----|------|------|
| **高德** | https://lbs.amap.com | 景点/酒店POI |
| **FlyAI** | https://flyai.com | 航班票价 |
| **腾讯地图** | https://lbs.qq.com | 导航 |
| **美团** | https://open.meituan.com | 酒店/美食 |

---

## 使用示例

```
用户: "帮我规划五一敦煌旅游"
系统: "嘿！我是旅游大师，五一想去哪儿玩呀？"
用户: "2大人1小孩，预算5000，玩5天"
系统: "收到！咱们继续完善行程～"
用户: "慢生活，大雁塔，不吃辣，高铁"
系统: "搞定！攻略已生成，祝旅途愉快！🦞"
→ HTML攻略发送（飞猪+美团+高德+携程并行链接）
```

---

## 核心算法

### 数学收敛公式

```python
convergence_rate = confirmed_fields / 7
# 7个必填字段（5W+2H）
```

### 强制收敛机制

```python
if round_count >= 3:
    auto_fill_optional()  # 第3轮自动填充
```

---

## 输出格式

- HTML攻略网页（Glassmorphism风格）
- 并行商家链接（飞猪+美团+高德+携程）
- P0强制发送用户（交付闭环）

---

## 文件结构

```
travel-master-v4/
├── SKILL.md              # 技能文档
├── clawhub.json          # ClawHub配置
├── README.md             # 说明文档
├── LICENSE               # MIT许可证
├── .env.example          # 配置模板
├── core/                 # 核心代码
│   ├── main_v4_2.py
│   ├── engine.py
│   ├── socratic_agent.py
│   ├── debate_engine.py
│   ├── amap_client.py
│   └── report_generator.py
├── templates/            # HTML模板
│   └── index.html
└── docs/                 # 教程文档
    ├── 保姆教程.md
    └── 开源推文.md
```

---

## License

MIT

---

🦫 海狸 | 靠得住、能干事、在状态