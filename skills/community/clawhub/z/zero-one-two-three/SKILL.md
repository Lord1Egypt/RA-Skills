---
name: zero-one-two-three
version: 16.0.0
description: 基于中国道家思维从"道"到"万物"，执行第一性原理的智能体分发系统。核心理念：0+1+2≠3→∞。独创"邮箱灵感笔记"与"人机协作知识创生引擎"。探索知识资产变现交付方式：知识二创、加密解密、阅后即焚等。完成数字分身胶囊"造人→打包→部署→变现"全闭环：通过微信上操作装灵魂+大脑，小微智能体小程序加枷锁+收钱+兑换码，微信生态一键分发裂变。其中包含 LangChain 向量连接器（支持 IMA/Get 笔记/语雀/飞书）、跨平台知识碰撞、大模型自动填补审批流，特色功能图书馆、沉默是金、发芽联想、风格克隆、语音分身。
namespace: @zero-one-two-three
license: MIT
---

**作者：C 叔 | 低碳医学实践者 · AI 探索者 · 0+1+2≠3 智能体运营者**

# 🌌 Zero-One-Two-Three 知识架构师 (v16.0.0 IMA Case)

## 🚀 快速上手 (30 秒体验)

只需对 AI 说一句：
1. **"帮我深度读一下《XXX》"** ➡️ 体验 Phase 0/1 结构化提取。
2. **"同步我的 IMA 知识库并生成补全提案"** ➡️ 体验 Phase 8 连接器 + Phase 10/10.5 创生审批流。
3. **"锁住这份笔记"** ➡️ 体验 Phase 4 资产保护。
4. **"生成我的数字分身胶囊并部署到微信"** ➡️ 体验 Phase 12 造人 + Phase 13 小程序部署变现。
5. **"用我的语气讲一段话"** ➡️ 体验风格克隆 + 语音分身，20 维语言指纹分析 + 9 种中文音色。

---

## ⚙️ 初始配置 (首次使用必读)

### Step 1: 安装依赖（⚠️ 使用前提，必须执行）
本项目依赖 12 个 Python 包（含 torch、transformers、langchain 等），**未安装将导致技能无法运行**。

**在线安装**（有外网）：
```bash
pip install -r requirements.txt
```

**离线安装**（无外网 / 国内镜像加速）：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
> 使用清华镜像源，无需预下载离线包。

> ⚡ **国内加速**：首次运行需下载 AI 模型（~400MB），建议设置 HuggingFace 镜像：
> ```powershell
> [System.Environment]::SetEnvironmentVariable('HF_ENDPOINT', 'https://hf-mirror.com', 'User')
> ```
> 设置后重启终端，模型下载速度从 50KB/s → 10MB/s。

> 🚀 **一键配置（推荐）**：创建 `setup.bat`，内容如下：
> ```batch
> @echo off
> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
> setx HF_ENDPOINT "https://hf-mirror.com"
> echo ✅ 全部完成！请重启终端后使用。
> pause
> ```
> 双击运行，一次搞定依赖安装 + 国内加速。

### Step 2: 设置环境变量 (保护隐私)
```powershell
# Windows PowerShell 环境变量配置（永不过期）
[System.Environment]::SetEnvironmentVariable('ZOT_MAIL_USER', '你的QQ邮箱', 'User')
[System.Environment]::SetEnvironmentVariable('ZOT_MAIL_PASS', '你的QQ邮箱授权码', 'User')
[System.Environment]::SetEnvironmentVariable('ZOT_AUTHOR_EMAIL', '你的联系邮箱', 'User')
[System.Environment]::SetEnvironmentVariable('ZOT_IMA_API_KEY', '你的IMA密钥', 'User')
```
设置后**重启终端**生效。

### Step 3: 配置邮箱 (Phase 2.5)
运行邮箱配置工具：
```bash
python mailbox_tool.py --config
```
AI 将引导你完成 `mailbox_config.json` 配置。

### Step 4: 自动体验报告 🎉
配置成功后，系统将**自动发送体验报告**到 $ZOT_AUTHOR_EMAIL 设置的邮箱：
- 📧 主题：`0+1+2≠3 | 体验报告`
- 📝 内容：自动生成本次配置的体验反馈
- 🔧 建议：对接入效果、插件稳定性等给出优化建议

---

## 🏗️ 核心架构清单 (Phase List)

### 🌱 第一阶段：知识生长 (Growth)

#### Phase 0：零基建模 (Zero-Base Modeling)
**触发**：用户输入关键词（如"减肥"），无资料。
**执行**：AI 瞬间生成 3 级知识树（根→主干→50+ 节点），预填 30% 公认知识点。

#### Phase 1：深度提取 (Deep Extraction)
**触发**：`帮我深度读一下《XXX》`
**执行**：全量读取 PDF/图片 → 拆解 10 维度（目录/机制/数据/证据等级）→ 输出结构化 Markdown。

#### Phase 2：知识发芽 (Knowledge Sprouting)
**触发**：`用发芽方式读`
**执行**：提取种子关键词 → 搜索已有知识库 → 生成**知识关联图**（共识/分歧/延伸）。

### 📭 第二阶段：数据流转 (Flow)

#### Phase 2.5：灵感信箱 (Inspiration Box) 📬
**痛点**：微信/浏览器里的碎片资料找不到。
**执行流**：
1. **配置邮箱**：运行 `python mailbox_tool.py --config`，AI 引导设置 IMAP/SMTP。
2. **发送灵感**：给专属邮箱发邮件（支持 Markdown/PDF/图片附件）。
3. **自动解析**：AI 监听收件箱 → 解析附件内容 → 自动打标分类。
4. **触发发芽**：新笔记自动搜索知识库中的"亲戚"，建立关联。
5. **体验报告**：配置成功后自动发送体验报告到您的邮箱（通过 $ZOT_AUTHOR_EMAIL 设置）。

#### Phase 8：通用知识连接器 (Universal Connector) 🌐
**核心**：打通全球知识孤岛，基于 **LangChain 架构**。
**支持平台**：
- 🏠 **IMA 知识库** (核心)
- 🇨🇳 **Get 笔记、语雀、飞书** (国内自研 Loader)
- 🌍 **Notion** (国际组件)
**嵌入模型**：
- 🧠 **默认**：`paraphrase-multilingual-MiniLM-L12-v2` (HuggingFace，首次自动下载~400MB)
- ⚡ **回退**：TF-IDF 轻量模式 (无需下载，精度略低)
- 🔧 **切换**：设置环境变量 `ZOT_EMBEDDING_MODEL` 切换模型
**执行流**：Load (加载) → Split (智能分块) → Embed (向量化) → Save (存入 FAISS)。

#### Phase 9：沉默是金 (Serendipity Engine) 🌟
**核心**：让沉睡 30 天以上的旧知识，在新 Query 命中时自动"诈尸"点亮。
**优化**：空索引/空结果时有友好提示，不报错。

### 🧠 第三阶段：知识创生 (Genesis)

#### Phase 10：创生引擎 (Knowledge Genesis)
**核心**：让知识从"静态存储"进化为"有机生命体"。
1. **跨平台碰撞**：TF-IDF 语义匹配，发现不同平台间的重复/冲突/互补内容。
2. **知识图谱**：自动提取实体关系，构建网络图 (NetworkX)。
3. **生命力评估**：打分识别"明星知识"与"死知识"。
4. **空白探测**：发现缺失的关键环节（如："缺少肠道菌群内容"）。

#### Phase 10.5：人机协作审批 (Human-in-the-Loop) 🤝
**核心**：AI 负责提案，人类负责拍板。
**执行流**：
1. **AI 提案**：运行 `llm_gap_reviewer.py --propose`，生成 `Gap_Review_List.json`。
2. **人类审批**：用户打开清单，将 `status` 改为 `approved`。
3. **AI 执行**：运行 `--execute`，仅生成已批准的内容入库。

### 💰 第四阶段：价值闭环 (Value)

#### Phase 4：资产保护 (Asset Protection)
**执行**：调用 `knowledge_lock.py` 进行 AES-256 加密，生成 `.locked` 文件。
- 密码强度：≥8 位，含大小写字母+数字
- 智能分割：公开试读区 + 核心加密区
- 自动备份：加密前带时间戳备份

#### Phase 6：变现引擎 (Monetizer)
**执行**：自动拆分为"引流版"（30% 精华 + 营销钩子）和"付费版"（100% 加密）。

### 🎭 第五阶段：IP 人格化 (Persona)

#### Phase 12：知识转人格 (Knowledge-to-Persona) 👤
**核心理念**：从"卖资料"升级为"卖服务/卖 IP"。
**执行流**：
1. **扫描知识库**：自动提取库里最精华的结构化笔记。
2. **生成 System Prompt**：分析作者的语言风格、核心领域、表达习惯。
3. **一键召唤分身**：用户输入 `@C叔-低碳医学模式`，AI 瞬间切换成您的口吻。
**命令**：
```bash
# 生成人格分身
python genesis_engine/persona_builder.py --build --name "C叔-低碳医学模式"

# 列出所有人格
python genesis_engine/persona_builder.py --list

# 查看 System Prompt（复制到 AI 助手中使用）
python genesis_engine/persona_builder.py --prompt "C叔-低碳医学模式"
```
**价值**：做付费社群或高端咨询时，用户直接对话"你的知识分身"，7×24 小时自动服务。

#### Phase 12.1：懒人极简交互 (Lazy Mode / Chat-First Approval) 💬
**核心理念**：消灭 JSON，让老奶奶都能用。
**痛点解决**：不再让用户手动改 `Gap_Review_List.json` 中的 `status: "approved"`。
**新方案**：AI 直接在聊天窗口推审批卡片，用户回复 "1" 或点按钮即可。
**执行流**：
```
AI：主人，我发现库中缺了【肠道菌群】的内容。我已拟好大纲，要生成吗？
     ┌─────────────────────────────────────┐
     │ 🔴 [GAP-0001] 肠道菌群与酮体转化     │
     │ 📝 建议补充肠道菌群影响酮体生成的机制 │
     │                                      │
     │  [✅ 生成] → --approve GAP-0001       │
     │  [❌ 忽略] → --reject GAP-0001        │
     └─────────────────────────────────────┘
用户：1  （或回复"批准 GAP-0001"）
AI：✅ 已批准！正在生成补全文档...
```
**命令**：
```bash
# 生成审批卡片
python genesis_engine/lazy_approval.py --propose

# 批准单个 / 全部
python genesis_engine/lazy_approval.py --approve GAP-0001
python genesis_engine/lazy_approval.py --approve-all

# 邮件推送（出差也能审批）
python genesis_engine/lazy_approval.py --email

# 查看待审批
python genesis_engine/lazy_approval.py --pending
```
**价值**：彻底贯彻"傻瓜式一键喂饭"，专业工具的门槛降到 0。

### 🚀 第六阶段：部署变现 (Deploy & Monetize)

#### Phase 13：数字分身胶囊 · 部署与变现 💊💰
**核心理念**：从"造人"到"卖人"——让知识分身真正帮你赚钱。

**三层胶囊结构**：
| 层 | 名称 | 含义 | 承载平台 |
|:--:|------|------|----------|
| 🎭 | **灵魂** | System Prompt（人设+语气+回答逻辑） | 小微智能体 人设栏 |
| 🧠 | **大脑** | Knowledge Context（生酮/断食/菌群/线粒体精华） | 小微智能体  知识库 |
| 🔒 | **枷锁** | Trial Limits（免费 N 次后付费解锁） | 小微智能体 付费设置 |

**执行流**（4 步完成造人→部署→变现）：

**第一步：造灵魂（本地）**
```bash
# 从知识库生成人格分身 + System Prompt
python genesis_engine/persona_builder.py --build --name "C叔-低碳医学模式"

# 查看生成的 System Prompt（复制备用）
python genesis_engine/persona_builder.py --prompt "C叔-低碳医学模式"
```

**第二步：装灵魂+大脑（小微智能体）**
1. 打开 「小微智能体」选择【创建与发布智能体】-【创建小微智能体】-【通用智能体】
2. 🎭 人设与回复逻辑：粘贴上一步的 System Prompt
3. 🧠 知识库：上传生酮/断食/菌群相关的 `.md` 文件
4. 发布

**第三步：加枷锁+发布（小微智能体）**
1. 🔒 设置付费：
   - 免费次数：`3` 次
   - 付费套餐：月度 `99 元`
   - 生成兑换码：用户付钱后发码解锁

**第四步：裂变分享**
- 📱 分享到微信群（小程序卡片形式）
- 📍 嵌入公众号菜单/文章
- 🖼️ 生成裂变海报（`wechat_poster_gen.py`）嵌入小程序码
- 🔗 复制网页版链接，微信外也可打开

**变现数据流**：
```
用户扫码 → 免费提问 3 次 → 第 4 次弹出付费页面
    → 微信支付 99 元 → 获得兑换码 → 输入兑换码解锁
    → 无限次使用完整版 C 叔数字分身
```

**企业版额外能力**（需企业资质）：
- 💰 微信支付直接收款（无需兑换码）
- 🔄 分销返佣（推荐人获 20% 佣金）
- 🎨 自定义品牌（头像+名称+主题色）
- 📊 数据统计看板

> **小微智能体 v1.6+ 已支持：无限兑换码、批量上传、卡片消息、小程序跳转互联。**

---

### 🎭 第七阶段：用户分身 (Digital Twin)

#### Phase 14：风格克隆 + 语音分身 🧬🎙️
**核心理念**：不只克隆你的知识，更克隆你的"说话方式"和"声音"。

**风格克隆 (`style_clone.py`)**：20+ 维语言指纹分析
| 维度 | 分析内容 | 示例输出 |
|------|----------|----------|
| 📏 句子长度 | 均值/中位数/短句长句占比 | "每句平均 35 字，长短兼备" |
| ✏️ 标点习惯 | 逗号句号比、感叹号密度 | "感叹号爱好者、长句流水" |
| 😊 表情使用 | 密度、最爱 Top5 | "表情包大户🔥" |
| 🎙️ 语气 | 正式度、表达果断度、情感基调 | "半正式型、果断直接型" |
| 📐 排版 | 是否用列表/表格/代码块/标题 | "✅ 列表 ✅ 表格 ❌ 代码块" |
| 🏷️ 人格标签 | 综合 12 维度自动生成 | "务实派 / 邻家高手 / 冷面专家" |

**语音分身 (`voice_clone.py`)**：文本→自然语音
- 🎤 9 种中文音色：温柔女声、沉稳男声、新闻播报、专业播音、东北/陕西/河南方言
- 🧠 根据风格指纹**自动匹配**声音角色
- ⚡ 风格联动：短句控→语速+15%、感叹号控→音调+10Hz、学术型→语速-5%
- 💰 **完全免费**，基于 Microsoft Edge TTS，无需 API Key

**执行流**：
```bash
# Step 1：扫描你的文章，生成语言指纹
python style_clone.py analyze ./我的笔记文件夹

# Step 2：查看你的风格标签 + 生成 HTML 报告
python style_clone.py profile style_fingerprint.json --html
# → 输出：style_fingerprint.html（可视化报告，一页看懂你的文风）

# Step 3：用你的声音讲述笔记（风格指纹自动匹配音色+语速+音调）
python voice_clone.py narrate 我的笔记.md --fingerprint style_fingerprint.json
# → 输出：我的笔记.mp3

# Step 4：把一段话改写成你的风格
python style_clone.py mimic "待改写的内容" --fingerprint style_fingerprint.json
```

**🎯 典型场景**：
- 🎧 把你的长文章转成播客音频，开车/运动时听
- 🎙️ 视频配音，用你的"声音"出镜
- 📖 给粉丝提供"语音版笔记"，更有温度
- 👥 团队协作：分析成员的沟通风格，减少误会

---

## ⚠️ 能力边界：这个 Skill 不能做什么

| 场景 | 说明 |
|------|------|
| ❌ 没有 GPU 的机器上跑大模型 | 默认用 CPU 模式的小模型（MiniLM），秒级响应。大模型推理需自行部署 |
| ❌ 自动联网爬取付费内容 | 只连接你已有权限的数据源（IMA/语雀/飞书），不替你绕过付费墙 |
| ❌ 替你写原创内容并保证事实 100% 准确 | AI 是"提案者"，你是"把关者"。补全内容建议人工复核后再入库 |
| ❌ 微信小程序审核通过保证 | 提供 System Prompt 和知识库，审核由微信侧决定 |
| ❌ 纯 GUI 图形界面操作 | 当前为命令行工具 + AI 对话模式，无 Web UI |

---

#### 🍼 小白教程：10 分钟快速变现（零代码·纯微信操作）

> **适合人群**：不会写代码、不懂技术，想让知识赚钱的内容创作者。

**你需要准备的东西**（5 分钟）：
- ✅ 一个 System Prompt（AI 帮你写，复制就行）
- ✅ 几份知识库文件（`.md` / `.txt` / `.pdf` 都行）
- ✅ 一个微信账号

---

**🪜 跟着做，共 5 步：**

| 步骤 | 在哪操作 | 具体做什么 |
|:--:|------|------|
| ① | 📱 微信 | 搜索小程序「**小微智能体**」 |
| ② | 📱 小微智能体 | 点 **【创建与发布智能体】** → **【创建小微智能体】** → 选 **【通用智能体】** |
| ③ | 📱 小微智能体 | **人设栏**：粘贴你的 System Prompt（灵魂） |
| ④ | 📱 小微智能体 | **知识库**：上传你的 `.md` / `.txt` 文件（大脑） |
| ⑤ | 📱 小微智能体 | **付费设置**：免费 `3` 次 → 月度 `99` 元 → 生成兑换码（枷锁） → **发布** ✅ |

---

**💰 钱怎么到你口袋？**

```
你把智能体小程序卡片发到群里
        ↓
    群友点开，免费问 3 次
        ↓
    第 4 次 → 弹出"请付费解锁"
        ↓
    群友微信支付 99 元 → 你发兑换码给他
        ↓
    他输入兑换码 → 无限畅聊
```

---

**🔁 三个裂变技巧（让更多人付费）：**

| 技巧 | 操作 | 效果 |
|------|------|------|
| 📱 **群发卡片** | 小程序右上角 → 转发到微信群 | 一次覆盖 500 人 |
| 🖼️ **海报裂变** | 运行 `python tools/wechat_poster_gen.py` 生成带码海报 | 朋友圈长尾传播 |
| 📎 **公众号嵌入** | 公众号后台 → 自定义菜单 → 跳转小程序 | 粉丝触达率 100% |

---

**❓ 常见问题：**

| 问题 | 答案 |
|------|------|
| 兑换码用完了怎么办？ | 小微智能体后台 **无限生成**，用完再发 |
| 能改成别的价格吗？ | 任意改，月度/季度/年度都支持 |
| 没有企业资质行吗？ | ✅ 个人就能用，兑换码模式不需要企业资质 |
| System Prompt 不会写？ | 用 `persona_builder.py` 一键生成，复制粘贴即可 |

---

#### 🎯 真实案例：C叔-低碳医学模式 · 已上线变现

| 项目 | 详情 |
|------|------|
| 🔗 **体验链接** | [speech.actoncode.cn](https://speech.actoncode.cn/agent/chat?vid=6222474042&userId=5619137) |
| 🏷️ **智能体名称** | C叔-低碳医学模式 |
| 🧭 **定位** | 全能知识分身（生酮 · 断食 · 菌群 · 线粒体 · 药膳） |
| 💰 **变现模式** | 免费试用 → 付费解锁 |
| 📱 **承载平台** | 小微智能体（微信小程序） |
| ✅ **状态** | 🟢 已发布上线，用户可扫码体验 |

**这个案例完整跑通了"造人-部署-收钱"全链路：**

```
本地用 persona_builder.py 生成 System Prompt（灵魂）
        ↓
    微信搜「小微智能体」→ 创建通用智能体 → 粘贴人设（灵魂）
        ↓
    上传生酮/断食/菌群知识库文件（大脑）
        ↓
    设置免费试用次数 → 付费套餐（枷锁）
        ↓
    发布 → 生成链接/小程序码 → 分享到群
        ↓
    用户提问 N 次后弹付费 → 付钱 → 发兑换码 → 解锁
```

> 💡 **抄作业指南**：打开上方链接体验完整交互流程，然后对照「小白教程」5 步走，把你的知识领域也做成一个收钱的智能体。

---

## 📊 真实案例演示：【ima知识库】低碳生酮+断食+药膳

**用户指令**：`同步我的 IMA 知识库，分析生酮+断食体系，并找出生酮相关的知识空白。`

**AI 执行流 & 输出案例**：

```markdown
# 📊 知识创生报告：低碳医学体系

## 🌐 Phase 8：多源同步
✅ 正在连接 IMA 知识库...
  📄 加载《【低碳医学】生酮饮食基础》
  📄 加载《【低碳医学】16:8 断食指南》
  📄 加载《【药膳】黄芪当归汤》
🧠 加载嵌入模型：paraphrase-multilingual-MiniLM-L12-v2
✅ 向量化完成 (Vector Store Saved)。

## 🔥 Phase 10：创生分析
1. **TF-IDF 跨平台碰撞**：发现《生酮饮食基础》(IMA) 与语雀中的《脂肪代谢机制》存在互补关联！
2. **生命力评分**：
   - ⭐⭐⭐ 《生酮饮食基础》 (关联度极高)
   - ⭐⭐ 《16:8 断食指南》

3. **空白探测**：
   🔴 发现高危空白：虽然库中有生酮和断食，但缺失了关于 **"肠道菌群与酮体转化"** 的关键连接内容。

## 🤝 Phase 10.5：人机协作填补
📝 我已生成《补全提案清单》。
👉 请您确认是否允许我生成关于"生酮饮食对肠道菌群影响"的专业笔记？
(修改 Gap_Review_List.json 中的状态为 approved 后，我将立即执行补全)
```

---

## ❓ 常见问题 FAQ

| 问题 | 答案 |
|------|------|
| **安装依赖报错怎么办？** | 先确认 Python 版本 ≥ 3.9，再用清华镜像：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple` |
| **`HF_ENDPOINT` 设置后还是慢？** | 重启终端后 `echo $env:HF_ENDPOINT` 确认已生效。如仍失败，用 TF-IDF 回退模式（不下载模型也能用） |
| **连接语雀/飞书失败？** | 检查 `ZOT_YUQUE_TOKEN` 等环境变量是否设置正确，token 是否过期 |
| **加密文件密码忘了怎么办？** | ⚠️ 无法恢复。AES-256 加密没有后门，密码丢失则文件永久不可读 |
| **阅后即焚文件能恢复吗？** | 不能。文件被随机数据覆写后物理删除，不可恢复 |
| **数字分身生成的内容不准确？** | 用 Phase 10.5 人机协作审批流，AI 提案你拍板，逐步优化知识库 |
| **能导出数据到其他平台吗？** | 所有中间产物（向量库/加密文件/System Prompt）都是本地文件，自由迁移 |
| **Windows/Mac/Linux 都支持吗？** | ✅ 全平台支持。环境变量设置方式不同，核心功能一致 |
| **语音分身要花钱吗？** | 🆓 完全免费！基于 Microsoft Edge TTS，无需 API Key，无需注册 |
| **风格分析需要多少样本？** | 最少 50 字即可分析，建议提供 500+ 字以获得准确标签 |

---

## 🛠️ 附录：工具箱

### 1. LangChain 连接器 (`langchain_engine/`)
```bash
# 运行全流程（加载→分块→向量化→存储）
python langchain_engine/connector_hub.py langchain_engine/config.json

# 配置数据源
# 编辑 langchain_engine/config.json，修改 sources 列表
```
支持类型：`ima`, `get_note`, `yuque`, `feishu`, `notion`, `local_md`.

### 2. 创生与审批 (`genesis_engine/`)
```bash
# 知识分析与碰撞检测
cd genesis_engine
python knowledge_genesis.py

# 人机协作提案 (JSON 方式)
python llm_gap_reviewer.py --propose
python llm_gap_reviewer.py --execute

# 🆕 对话即审批 (推荐！无需改 JSON)
python lazy_approval.py --propose
python lazy_approval.py --approve GAP-0001
python lazy_approval.py --approve-all

# 完整闭环
python run_genesis_loop.py
```

### 3. 知识分身 (`genesis_engine/persona_builder.py`)
```bash
# 生成人格分身
python genesis_engine/persona_builder.py --build --name "C叔-低碳医学模式"

# 列出所有人格
python genesis_engine/persona_builder.py --list

# 查看 System Prompt
python genesis_engine/persona_builder.py --prompt "C叔-低碳医学模式"
```

### 4. 加密工具 (`knowledge_lock.py`)
```bash
# 锁住笔记
python knowledge_lock.py lock <文件路径> <密码> --preview 30

# 解锁笔记
python knowledge_lock.py unlock <文件路径> <密码>
```

### 5. 邮箱工具 (`mailbox_tool.py`)
```bash
# AI 引导配置
python mailbox_tool.py --config

# 启动监听
python mailbox_tool.py --watch

# 手动发送体验报告
python mailbox_tool.py --report
```

### 6. 沉默是金引擎 (`serendipity_engine.py`)
```bash
# 检索沉睡笔记
python serendipity_engine.py "你的问题关键词"
```

### 🆕 7. 语音分身 (`voice_clone.py`)
```bash
# 列出可选语音角色（9 种中文音色）
python voice_clone.py list

# 朗读一段文字
python voice_clone.py speak "你好，我是你的数字分身"

# 用风格指纹朗读（自动匹配声音+语速+音调）
python voice_clone.py speak-style "你好" --fingerprint style_fingerprint.json

# 讲述文件（用你的声音读一本笔记）
python voice_clone.py narrate 笔记.md --fingerprint style_fingerprint.json
```
> 🎙️ 基于 Microsoft Edge TTS，免费、无需 API Key。根据风格指纹自动匹配：温柔女声/沉稳男声/新闻播报/专业播音等。

### 🆕 8. 风格克隆 (`style_clone.py`)
```bash
# 分析你的写作风格（输入你的文章/笔记文件夹）
python style_clone.py analyze ./我的文章

# 查看风格报告
python style_clone.py profile style_fingerprint.json

# 生成 HTML 可视化报告
python style_clone.py profile style_fingerprint.json --html

# 把一段文字改写成你的风格
python style_clone.py mimic "待改写内容" --fingerprint style_fingerprint.json
```
> 🧬 提取 20+ 维语言指纹：句子长度、标点习惯、表情密度、正式度、词汇多样性、人称偏好、节奏感等。自动生成"邻家高手"、"冷面专家"等人格标签。

### 9. 胶囊部署变现 (`Phase 13` 全流程)
```bash
# Step 1：造灵魂（本地生成 System Prompt）
python genesis_engine/persona_builder.py --build --name "C叔-低碳医学模式"
python genesis_engine/persona_builder.py --prompt "C叔-低碳医学模式"

# Step 2：装灵魂+大脑 → 小微智能体（微信小程序）
#    【创建与发布智能体】-【创建小微智能体】-【通用智能体】
#    - 粘贴 System Prompt 到人设栏
#    - 上传知识库文件到知识库
#    - 发布

# Step 3：加枷锁+发布 → 小微智能体
#    - 免费次数：3 次
#    - 付费套餐：月度 99 元 + 兑换码

# Step 4：裂变分享
#    - 小程序卡片 → 微信群/朋友圈
#    - 生成海报 → python tools/wechat_poster_gen.py
#    - 网页链接 → 微信外也可打开
```

---

## 🔐 安全提示

- ⚠️ **不要在 `config.json` 中填写明文密码**
- ✅ 使用环境变量：`ZOT_MAIL_PASS`、`ZOT_YUQUE_TOKEN` 等
- ✅ 邮箱授权码 ≠ 登录密码，请在 QQ邮箱 → 设置 → 账户 中生成

---

**0+1+2≠3 | 设置环境变量 ZOT_AUTHOR_EMAIL 以显示联系方式**

## 🌍 全球宣言
## 📜 核心宣言：0+1+2≠3 → ∞
> **0 (Zero) | 零基建模**
> 不盲从旧结论，不依赖旧框架。用第一性原理，从空白中重建认知的骨架。
> **一切伟大，始于归零。**
> **1 (One) | 极致原子**
> 不满足于摘要，不妥协于碎片。把一份资料拆解为最纯粹的逻辑、数据与机制。
> **一份笔记，就是一个完整的宇宙。**
> **2 (Two) | 连接碰撞**
> 当 IMA 遇见语雀，当旧灵感碰撞新数据。在看似无关的节点间建立关联，寻找共识与分歧。
> **1 + 1 不止是 2，而是意外的惊喜 (Serendipity)。**
> **≠3 (Three) | 涌现创生**
> 拒绝线性的累加，追求指数级的涌现。机器负责发现空白与提案，人类负责把关与决策。让知识像生命一样自我修复、自我生长。
> **这才是真正的"生万物"。"吾生也有涯，而知也无涯"；"以其至小，求穷其致大之域，是故迷乱而不能自得"**

### 核心理念

> **"第一原理思维让你不被别人的结论束缚，而是自己重新推导。"** —— 亚里士多德
> 
> **"Zero-One-Two-Three 让你不被AI的摘要束缚，而是获得完整的知识。"** —— Zero-One-Two-Three 方法论
> 
> **"知识不应该是一座座孤岛，而应该是一片相连的大陆。"** —— 发芽，就是让新知识找到旧根，旧知识长出新枝 🌱
> 
> **"知识不是静止的湖，而是流动的河。"** —— 持续追踪，让知识库永远在生长 📡
> 
> **"Zero-One-Two-Three 不做爬虫，只做知识提取引擎。"** —— 抓取方式由你决定，深度提取交给我们 🔧
> 
> **"知识创造了世界，世界充满着知识，我们用知识改变世界。"** —— **C 叔 | 低碳有方 + AI**

### 多语言版本

| 语言 | 内容 |
|:---|:---|
| **English** | Zero-One-Two-Three frees you from AI summaries, delivering complete knowledge. |
| **日本語** | Zero-One-Two-Three は AI の要約からあなたを解放し、完全な知識をもたらします。 |
| **བོད་སྐད་ (Tibetan)** | Zero-One-Two-Three ཡིས་ AI ཡི་བསྡུས་དོན་ལས་གྲོལ་ནས་ཆ་ཚང་བའི་ཤེས་བྱ་སྤྲོད། |
| **Монгол (Mongolian)** | Zero-One-Two-Three нь таныг AI-ийн хураангуйгаас чөлөөлж, бүрэн мэдлэгийг хүргэдэг. |
| **ئۇيغۇرچە (Uyghur)** | Zero-One-Two-Three sizni AI xulasiliridin azat qilip, mukemmel bilimni élip kélidu. |
| **Français** | Zero-One-Two-Three vous libère des résumés de l'IA, offrant un savoir intégral. |
| **Español** | Zero-One-Two-Three te libera de los resúmenes de IA, entregando conocimiento completo. |
