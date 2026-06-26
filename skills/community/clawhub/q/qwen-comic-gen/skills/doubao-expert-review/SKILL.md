# Skill: 豆包会话专家点评系统

**版本**: v1.0  
**创建时间**: 2026-03-06  
**作者**: 阿福（基于与 Xiabi 的协作）

---

## 📋 技能描述

自动处理豆包会话内容，生成专家级点评 HTML 网页，包含知识架构图、深度洞察和行动建议。

**核心流程：**
```
豆包会话 → AI 分析 → 专家点评 → HTML 网页 → Chrome 打开 → TTS 语音 → 飞书发送
```

---

## 🎯 触发条件

**触发词：** 消息以 "豆包" 开头

**示例：**
```
豆包 [粘贴豆包会话内容...]
```

---

## 🚀 自动执行流程（4 步）

### 1️⃣ 保存原始内容
**位置：** `doubao-sessions/YYYY-MM-DD (周*) -N worklog.md`

**命名规则：**
- 格式：`YYYY-MM-DD (周*) -N worklog.md`
- 序号 N 自动递增（同一天多次会话）
- 完整保存豆包会话原始内容

### 2️⃣ 更新 worklog.txt
**位置：** `C:\Users\Xiabi\.openclaw\workspace\worklog.txt`

**格式：**
```markdown
### 2026-03-06 (周五)
- [完成] 豆包会话：[主题摘要]
- [进行中] xxx
- [待办] xxx
```

### 3️⃣ 生成专家点评 HTML
**位置：** `expert-review-YYYY-MM-DD-主题.html`

**格式标准：**
- **视觉风格：** 科学杂志 + 小红书视觉
- **排版：** Nature 杂志风格，微软雅黑字体
- **元素：** Mermaid 知识架构图、对比表格、专家洞察框

**结构要求（金字塔原理）：**
1. **专家评分** - 完整性/正确性/缺失项
2. **核心观点** - 结论先行，Critical Thinking
3. **深度洞察** - ≥3 个大观点，MECE 法则
4. **知识架构** - Mermaid 图表
5. **对比分析** - 表格或对比图
6. **行动建议** - 可落地的建议

**核心原则：**
- 第一性原理：回归事物本质
- MECE 法则：不重不漏
- 业务价值导向：先回答价值是什么
- Critical Thinking：质疑假设、验证逻辑

### 4️⃣ Chrome 自动打开 + TTS 语音 + 飞书发送
**步骤：**
1. `Start-Process "chrome.exe" -ArgumentList "<html-file-path>"` - 独立窗口打开
2. `tts` 工具生成核心内容语音
3. `message` 工具发送到飞书（文字 + 语音）
4. 本地自动播放语音（0 步操作）

---

## 📐 用户偏好（必须遵守）

### 学习偏好
- ✅ **视觉学习者** - 喜欢结构化图表
- ✅ **专业绘制** - 不要手绘风格，要专业架构图
- ✅ **知识要点** - 需要 Mermaid 图表 + 文字说明
- ✅ **结合自身** - 点评要联系实际业务场景

### 语音偏好
- ✅ **自动播放** - TTS 生成后自动本地播放
- ✅ **文字 + 语音** - 飞书同时发送文字版和语音版
- ✅ **0 步操作** - 全自动，无需手动点击

### 行文风格
- ✅ **金字塔原理** - 结论先行，以上统下
- ✅ **Critical Thinking** - 主动思考，不被动接受
- ✅ **业务价值导向** - 先说价值，再说实现
- ✅ **MECE 法则** - 论据不重不漏

### 视觉设计
- ✅ **科学杂志风** - 参考《Nature》排版
- ✅ **小红书图标** - emoji + 简洁图标点缀
- ✅ **双栏布局** - 主内容 + 侧边栏导航
- ✅ **专业配色** - 学术风格，不花哨

---

## 📁 文件结构

```
workspace/
├── skills/doubao-expert-review/       # Skill 目录
│   ├── SKILL.md                       # 本文件
│   ├── scripts/                       # 脚本目录
│   │   ├── fetch-doubao-history.ps1   # 豆包历史获取
│   │   ├── generate-expert-review.ps1 # 专家点评生成
│   │   └── auto-open-chrome.ps1       # Chrome 自动打开
│   └── templates/                     # 模板目录
│       └── expert-review-template.html # HTML 模板
├── doubao-sessions/                   # 豆包会话归档
│   ├── 2026-03-06 (周五) -1 worklog.md
│   └── ...
├── worklog.txt                        # 日常工作日志
├── expert-review-*.html               # 专家点评 HTML
└── memory/2026-03-06.md              # 当日记忆
```

---

## 🔧 核心脚本

### fetch-doubao-history.ps1
**功能：** 从豆包读取会话历史

**参数：**
- `-ConversationId` - 会话 ID（可选）
- `-OutputPath` - 输出路径

**示例：**
```powershell
powershell -ExecutionPolicy Bypass -File fetch-doubao-history.ps1 -OutputPath "doubao-sessions"
```

### generate-expert-review.ps1
**功能：** 生成专家点评 HTML

**参数：**
- `-InputPath` - 豆包会话文件
- `-OutputPath` - HTML 输出路径
- `-Theme` - 主题（可选）

**示例：**
```powershell
powershell -ExecutionPolicy Bypass -File generate-expert-review.ps1 `
  -InputPath "doubao-sessions\2026-03-06-1.md" `
  -OutputPath "expert-review-2026-03-06-xiaomi-auto.html"
```

### auto-open-chrome.ps1
**功能：** Chrome 自动打开 HTML

**参数：**
- `-HtmlPath` - HTML 文件路径

**示例：**
```powershell
powershell -ExecutionPolicy Bypass -File auto-open-chrome.ps1 `
  -HtmlPath "expert-review-2026-03-06-xiaomi-auto.html"
```

---

## 🎨 HTML 模板结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>[主题] - 专家评点</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        /* 科学杂志风格 CSS */
        body { font-family: 'Microsoft YaHei'; background: white; }
        .container { max-width: 1600px; margin: 0 auto; padding: 40px; }
        .expert-comment { background: linear-gradient(135deg, #f093fb, #f5576c); color: white; }
        .knowledge-map { background: #f8f9fa; border-radius: 15px; padding: 30px; }
        .insight-box { background: #fff3cd; border: 2px solid #ffc107; }
        .action-items { background: #d4edda; border: 2px solid #28a745; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 [主题] - 专家评点</h1>
        
        <!-- 1. 专家评分 -->
        <section class="expert-comment">
            <h3>💡 专家评分</h3>
            <ul>
                <li>完整性：X/10</li>
                <li>正确性：X/10</li>
                <li>缺失项：xxx</li>
            </ul>
        </section>
        
        <!-- 2. 核心观点 -->
        <section>
            <h2>🎯 核心观点</h2>
            <p>结论先行...</p>
        </section>
        
        <!-- 3. 深度洞察 -->
        <section>
            <h2>🔍 深度洞察</h2>
            <div class="insight-box">
                <h4>洞察 1</h4>
                <p>...</p>
            </div>
        </section>
        
        <!-- 4. 知识架构 -->
        <section class="knowledge-map">
            <h3>🧠 知识架构</h3>
            <div class="mermaid">
                graph TD
                A[核心概念] --> B[子概念 1]
                A --> C[子概念 2]
            </div>
        </section>
        
        <!-- 5. 对比分析 -->
        <section>
            <h2>📊 对比分析</h2>
            <table>
                <thead>
                    <tr><th>维度</th><th>方案 A</th><th>方案 B</th></tr>
                </thead>
                <tbody>
                    <tr><td>性能</td><td>高</td><td>中</td></tr>
                </tbody>
            </table>
        </section>
        
        <!-- 6. 行动建议 -->
        <section class="action-items">
            <h3>✅ 行动建议</h3>
            <ul>
                <li>建议 1...</li>
                <li>建议 2...</li>
            </ul>
        </section>
    </div>
    
    <script>mermaid.initialize({startOnLoad:true, theme: 'rough'});</script>
</body>
</html>
```

---

## 📊 示例会话

### 输入
```
豆包
今天学习了小米汽车的感知与行动中心项目，主要包括：
1. 感知侧已落地，115 家供应商调研完成
2. 工单闭环规划中，风险预警→任务派发→执行跟踪→验收闭环
3. 数据治理完成，23 个字段标准化
4. 6 大核心指标：决策通过 115 家，SBC 签约 87 家 75.7%，验收通过率 94%，产能达标率 68%
```

### 输出
1. **保存：** `doubao-sessions/2026-03-06 (周五) -1 worklog.md`
2. **更新：** `worklog.txt` 添加今日记录
3. **生成：** `expert-review-2026-03-06-xiaomi-auto.html`（14846 字节）
4. **打开：** Chrome 独立窗口显示 HTML
5. **语音：** TTS 生成核心内容 MP3
6. **发送：** 飞书消息（文字 + 语音）

---

## 🔗 相关文件

- **MEMORY.md** - 长期记忆，包含项目知识库
- **memory/2026-03-06.md** - 当日详细记录
- **worklog.txt** - 日常工作日志
- **DOUBAO_AUTO_GUIDE.md** - 豆包自动化指南
- **tasks/projects/感知与行动中心 - 交付域风险管控.md** - 项目卡片

---

## ⚠️ 注意事项

1. **触发词识别** - 必须严格以 "豆包" 开头
2. **序号递增** - 同一天多次会话自动递增序号
3. **HTML 标准** - 必须包含 6 个必备章节
4. **语音自动播放** - 使用 `Start-Process` 本地播放
5. **飞书发送** - 文字版和语音版都要发送
6. **知识归档** - 重要内容归档到项目卡片

---

## 🎯 成功标准

- ✅ 豆包会话完整保存，不遗漏
- ✅ worklog.txt 及时更新
- ✅ HTML 符合专家点评格式标准
- ✅ Chrome 自动打开独立窗口
- ✅ TTS 语音生成并自动播放
- ✅ 飞书消息发送成功（文字 + 语音）
- ✅ 项目知识归档完成

---

## 📞 维护者

**阿福（AI 助理）**
- 飞书应用 ID: `cli_a91d70683c789bc7`
- 工作 location: 上海金桥 5G 小米公司
- 用户：Xiabi（上海佩玛山丘）

**最后更新：** 2026-03-06
