---
name: tsmf-wechat-oa
description: |
  微信公众号全自动写作系统。支持 20 种精美主题，自动生成封面，一键推送草稿箱。
  
  适用场景：
  - 用户需要生成公众号文章草稿
  - 用户想要切换多种排版主题
  - 用户需要自动化内容生产流程
  - 用户想要批量生成主题演示文章
  
  <example>用户: "帮我写一篇关于人工智能的公众号文章"</example>
  <example>用户: "Generate a WeChat article about coffee culture"</example>
  <example>用户: "公众号文章排版，用科技主题"</example>
license: MIT
compatibility: agent-skills-standard
metadata:
  category: content-creation
  version: "3.0.0"
  tags: [wechat, writing, publishing, automation, themes]
version: "3.0.0"
---

# 微信公众号自动写作 Skill

> 让 OpenClaw 模型自动理解并执行公众号文章写作、排版、推送的全流程。

## 核心理念

这是一个 **指导性 Skill**，而非传统的 API 调用文档。OpenClaw 模型在接收到用户请求后，应：

1. **主动询问** 用户需求细节
2. **自主决策** 写作方式和主题选择
3. **灵活执行** 写作 → 排版 → 推送流程

---

## 用户交互流程（必须遵循）

### 第一步：询问写作需求

当用户表达写作意图时，**必须先询问以下问题**：

```
1. 您想写什么主题的文章？
2. 目标读者是谁？（专业人士/大众/特定群体）
3. 文章类型偏好？
   - 技术教程
   - 商业分析
   - 生活随笔
   - 行业洞察
   - 其他（请说明）
4. 是否有参考资料？（文件路径或内容）
```

### 第二步：询问风格偏好

展示可用主题，让用户选择或接受推荐：

```
推荐主题：【根据内容自动推荐】

可选主题：
━━━━━━━━━━ 经典主题 ━━━━━━━━━━
1. 极简商务 (minimal_business) - 适合职场、管理、商业分析
2. 科技现代 (tech_modern) - 适合技术、编程、AI
3. 温暖文艺 (warm_artistic) - 适合读书、情感、随笔
4. 活泼清新 (fresh_lively) - 适合美食、旅行、生活方式
5. 杂志高级 (magazine_premium) - 适合时尚、艺术、深度阅读
6. 学术专业 (academic_professional) - 适合论文、研究、深度分析
7. 数据洞察 (data_analytics) - 适合数据报告、趋势分析
8. 舒适生活 (cozy_lifestyle) - 适合家居、慢生活、治愈系
9. 创意大胆 (creative_bold) - 适合设计、创意、灵感
10. 青春活力 (energetic_youth) - 适合校园、励志、正能量
11. 自然清新 (nature_fresh) - 适合环保、户外、植物
12. 复古经典 (retro_classic) - 适合历史、传统文化、回忆录
13. 极客科技 (geek_tech) - 适合游戏、二次元、夜间阅读

━━━━━━━━━━ 马卡龙主题 ━━━━━━━━━━
14. 马卡龙粉 (macaron_pink) - 甜美温柔
15. 马卡龙蓝 (macaron_blue) - 清新宁静
16. 马卡龙薄荷 (macaron_mint) - 清爽自然
17. 马卡龙薰衣草 (macaron_lavender) - 浪漫优雅
18. 马卡龙蜜桃 (macaron_peach) - 温暖甜美
19. 马卡龙柠檬 (macaron_lemon) - 明亮活力
20. 马卡龙珊瑚 (macaron_coral) - 热情活力
21. 马卡龙鼠尾草 (macaron_sage) - 自然清新
22. 马卡龙丁香 (macaron_lilac) - 优雅浪漫
23. 马卡龙奶油 (macaron_cream) - 温馨治愈
24. 马卡龙天空 (macaron_sky) - 清新明亮
25. 马卡龙玫瑰 (macaron_rose) - 浪漫精致

是否接受推荐？或指定其他主题？
```

### 第三步：询问发布方式

```
1. 立即生成并保存到本地？
2. 推送到微信公众号草稿箱？（需要配置）
3. 定时发布？（检测是否有定时任务）
```

### 第四步：确认执行

```
━━━━━━━ 写作确认 ━━━━━━━
主题：【用户选择的主题】
类型：【文章类型】
风格：【选择的排版主题】
发布：【发布方式】

确认开始写作？(是/否)
```

---

## 技术实现指南

### 项目结构

```
wechat-allauto-gzh/
├── SKILL.md                    # 本文件（OpenClaw 指引）
├── README.md                   # 详细用户教程
├── requirements.txt            # Python 依赖
├── .env.example               # 配置模板
│
├── scripts/                   # 核心脚本
│   ├── write_article.py       # 主写作流程
│   ├── outline_generator.py   # 大纲生成
│   ├── html_writer.py         # HTML 排版
│   ├── markdown_to_wechat_html.py  # 主题转换
│   ├── push_draft.py          # 微信推送
│   ├── generate_covers.py     # 封面生成
│   └── content_validator.py   # 内容验证
│
├── themes/                    # 主题配置
│   ├── classic/              # 经典主题（10个）
│   │   ├── minimal_business.yaml
│   │   ├── tech_modern.yaml
│   │   └── ...
│   └── macaron/              # 马卡龙主题（12个）
│       ├── pink.yaml
│       ├── blue.yaml
│       └── ...
│
└── output/                    # 输出目录
    └── YYYY-MM-DD/
        ├── article.html       # 排版后的文章
        ├── article.json       # 文章结构
        └── cover.html         # 封面
```

### 核心流程

```
用户输入话题
    ↓
[1] 询问需求 → 确认主题、类型、风格
    ↓
[2] 生成大纲 → 按文章类型分配结构
    ↓
[3] AI 写作 → 使用 OpenClaw 模型生成内容
    ↓
[4] Markdown 写作 → 先生成 Markdown 格式
    ↓
[5] 主题转换 → 应用选择的主题样式
    ↓
[6] 封面生成 → 根据内容生成封面 HTML
    ↓
[7] 内容验证 → 使用 Tavily 搜索验证事实
    ↓
[8] 推送草稿 → 上传封面，创建图文草稿
    ↓
[9] 保存文件 → HTML + JSON + 封面
```

---

## 写作模式

### 模式一：全自动写作

**触发条件**：
- 用户只提供主题，无额外要求
- 检测到定时任务环境（`WECHAT_AUTO_MODE=true`）

**执行流程**：
```bash
python scripts/write_article.py "主题" --mode auto
```

### 模式二：半自动写作

**触发条件**：
- 用户指定了主题风格
- 用户提供了参考材料
- 用户有特殊要求

**执行流程**：
```bash
python scripts/write_article.py "主题" --theme tech_modern
python scripts/write_article.py "主题" --reference ref.txt
python scripts/write_article.py "主题" --type tutorial
```

### 模式三：交互式写作

**触发条件**：
- 用户希望参与每个环节
- 用户使用了 `--interactive` 参数

**执行流程**：
```
1. 显示大纲 → 用户确认或修改
2. 逐章写作 → 显示内容，询问是否满意
3. 预览效果 → 显示排版预览
4. 确认推送 → 用户确认后推送
```

---

## 文章类型模板

OpenClaw 可根据内容自动选择或混合使用：

### 技术教程型
```
引言（10%）→ 背景（15%）→ 核心内容（40%）→ 实践案例（20%）→ 总结（15%）
```

### 商业分析型
```
现象（10%）→ 背景（20%）→ 深度分析（35%）→ 案例（20%）→ 趋势（15%）
```

### 生活随笔型
```
开篇（10%）→ 个人经历（25%）→ 感悟探讨（35%）→ 实用建议（20%）→ 结语（10%）
```

### 行业洞察型
```
现状（10%）→ 问题分析（25%）→ 深度解读（35%）→ 未来展望（20%）→ 建议（10%）
```

### 产品评测型
```
概述（10%）→ 第一印象（15%）→ 核心体验（40%）→ 优缺点（20%）→ 购买建议（15%）
```

---

## 主题系统

### 主题推荐算法

基于关键词匹配自动推荐主题：

```
技术/AI/编程 → tech_modern
职场/管理/商业 → minimal_business
美食/旅行/生活方式 → fresh_lively
读书/情感/随笔 → warm_artistic
数据/报告/趋势 → data_analytics
女性/浪漫/甜美 → macaron_pink 或 macaron_rose
```

### 自定义主题

用户可创建自定义主题：

1. 复制现有主题 YAML 文件
2. 修改颜色和样式
3. 保存到 `themes/custom/` 目录
4. 使用 `--theme custom/主题名` 调用

---

## 封面生成

**重要**：微信公众号新建草稿必须上传封面图片！

### 封面生成规则

```python
def generate_cover(title: str, theme: str) -> str:
    """
    根据文章标题和主题生成封面 HTML
    
    包含：
    - 文章标题（大字体）
    - 副标题/摘要（可选）
    - 主题色背景渐变
    - 装饰性元素
    - 发布日期
    """
```

### 封面尺寸

- 推荐尺寸：900 × 500 像素
- 格式：HTML（用户截图保存）或自动转图片

---

## 微信推送

### 配置要求

```bash
# .env 文件
WECHAT_APP_ID=your_app_id
WECHAT_APP_SECRET=your_app_secret
```

### 获取配置步骤

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 进入「设置与开发」→「基本配置」
3. 复制 AppID 和 AppSecret

### API 参考（类似 wechatpy）

```python
# 获取 access_token
GET https://api.weixin.qq.com/cgi-bin/token
    ?grant_type=client_credential
    &appid={APP_ID}
    &secret={APP_SECRET}

# 上传图片
POST https://api.weixin.qq.com/cgi-bin/media/uploadimg
    ?access_token={ACCESS_TOKEN}

# 创建草稿
POST https://api.weixin.qq.com/cgi-bin/draft/add
    ?access_token={ACCESS_TOKEN}
Body: {
    "articles": [{
        "title": "标题",
        "content": "HTML内容",
        "thumb_media_id": "封面media_id"
    }]
}
```

---

## 内容验证

### 使用 Tavily 搜索验证

```bash
# 安装
pip install tavily-python

# 使用
from tavily import TavilyClient
client = TavilyClient(api_key="your_key")
result = client.search("验证内容")
```

### 验证流程

```
1. 识别文章中的事实性陈述（数字、年份、引用等）
2. 使用 Tavily 搜索验证
3. 标注需要人工核实的内容
4. 在文末添加「来源」部分
```

---

## 定时任务检测

### 检测方式

```python
def detect_scheduled_task():
    """
    方式1：环境变量 - WECHAT_AUTO_MODE=true
    方式2：crontab - 检查是否有相关 cron job
    方式3：配置文件 - ~/.wechat_auto_config
    """
```

### 定时任务配置示例

```bash
# crontab 示例
0 9 * * * cd /path/to/project && python scripts/write_article.py "今日热点" --mode auto
```

---

## 输出文件

### 文件结构

```
output/2026-03-11/
├── article.html       # 排版后的完整 HTML
├── article.json       # 文章结构（大纲、章节）
├── article.md         # 原始 Markdown
├── cover.html         # 封面 HTML
└── cover.png          # 封面图片（如果转换）
```

### JSON 结构

```json
{
  "title": "文章标题",
  "theme": "tech_modern",
  "type": "tutorial",
  "created_at": "2026-03-11T10:00:00",
  "sections": [...],
  "total_words": 2000,
  "media_id": "微信media_id"
}
```

---

## 决策建议

OpenClaw 在执行过程中可能需要自行决策：

### 字数控制建议

| 文章类型 | 建议字数 |
|---------|---------|
| 技术教程 | 1500-2500 |
| 商业分析 | 2000-3000 |
| 生活随笔 | 800-1500 |
| 行业洞察 | 1500-2500 |
| 产品评测 | 1000-2000 |

### 错误处理建议

```
AI 写作失败 → 重试 3 次，或切换写作策略
推送失败 → 保存到本地，提示用户手动推送
封面生成失败 → 使用默认封面模板
```

---

## 快速开始

### 用户输入 GitHub 链接后

OpenClaw 应：

1. **克隆项目**
```bash
git clone https://github.com/user/wechat-allauto-gzh.git
cd wechat-allauto-gzh
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境**
```bash
cp .env.example .env
# 编辑 .env 填写微信公众号配置
```

4. **开始交互**
```
您好！已成功加载微信公众号自动写作系统。
请问您想写什么主题的文章？
```

---

## 依赖

```
requests>=2.28.0          # 微信 API 调用
python-dotenv>=0.19.0     # 环境变量管理
pyyaml>=6.0               # 主题配置文件（可选）
tavily-python>=0.3.0      # 内容验证（可选）
```

---

## 版本历史

- **v3.0.0** - 重构为 OpenClaw 指向型 Skill，20+ 精美主题，配置驱动架构
- **v2.0.0** - 添加马卡龙主题系列，优化移动端适配
- **v1.0.0** - 初始版本，8 个经典主题

---

**MIT License • Open Source**

*此 Skill 由 OpenClaw 模型自主理解和执行，以上内容为指引而非硬性规定。*