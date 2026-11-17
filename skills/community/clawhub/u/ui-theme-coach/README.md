# OpenClaw UI Theme Coach 🎨

通过问答引导帮用户定制任意风格的 UI 主题：**OpenClaw Control UI、DSH web UI、任意 Web 项目**（像素/赛博朋克/卡通/极简/暗色科技等）。

## 五大能力
- 🎨 **通用方法论**：注入架构、设计令牌、可读性、验证
- 📚 **风格技术库**：references/styles/ 数据化模板（5 种内置 + 社区可扩展）
- 🛡️ **升级自愈**：检测 dist 升级 → 自动从快照恢复注入
- 🔁 **反馈学习**：记录用户偏好，越用越贴合
- 🧠 **自助检索 + 素材指路**：主动 web_search/clawhub 找工具；用户要某 IP/风格时帮找官方/授权素材渠道（给链接+教用法，用户自备自用，skill 不搬运）

## 使用
1. 告诉 Agent 你想做什么风格的主题
2. 跟着问答引导走（风格→色彩→氛围→可读性）
3. 主色派生自动生成调色板
4. 双保险注入到 Control UI
5. 对比度必查配对清单逐对跑 + 反模式自查
6. 升级自愈快照存档

## 文件结构
```
openclaw-ui-theme-coach/
├── SKILL.md                          # 主文档
├── README.md                         # 本文件
├── references/
│   ├── minecraft-example.md          # MC 像素风完整案例
│   └── styles/                       # 风格技术库（数据化：社区加风格只加文件，不改主文档）
│       ├── TEMPLATE.md               # 新风格空模板（复制改名即用）
│       ├── pixel-game.md             # 像素/游戏
│       ├── cyberpunk.md              # 赛博/霓虹
│       ├── cartoon-cute.md           # 卡通/可爱
│       ├── minimal-modern.md         # 极简/现代
│       └── dark-tech.md              # 暗色科技
├── scripts/
│   ├── derive-palette.py             # 主色派生调色板（20 个 CSS 变量；--light 浅色亮度反转；border 自动对齐 ≥3:1）
│   ├── contrast-check.py             # WCAG 对比度检查
│   └── heal.sh                       # 升级自愈脚本（--force 先验目标快照再卸载；含上游版本比对）
├── test-prompts.json                 # 自测用例（3 happy path + 3 负面/边界）
└── data/
    └── feedback.json                 # 用户偏好记录
```

## 版本
1.5.0 — 素材策略改版（默认官方，自绘兜底）：默认帮用户找 IP 明确的官方/授权素材（官方图最贴原版），自绘仅当用户明确要求或官方素材不可得；核心哲学 #3 与第五步·素材指路同步
1.4.1 — 明确支持 **DSH web UI（DeepSeek Harness 界面）** 换皮：何时使用 + 3.0 目标环境判定形态 A 点名 DSH（技术早在 1.3.0 的通用方法论覆盖，本次为能力声明）+ 同步 ClawHub
1.4.0 — 素材责任归属改版：版权红线 →「素材指路」——skill 帮用户寻找官方/授权素材（所有主题通用），下载与存放发生在用户侧，skill 包内素材必须干净（自绘/已授权），用户个人使用官方素材属合理使用；新增第五步·素材指路小节
1.3.0 — 环境无关升级（源自 DSH 适配版回合）：新增 3.0 目标环境判定（形态 A 构建产物/B 静态稿/C 其他运行时）+ 7.0 主题包交付标准形态 + 通用设计令牌说明；Control UI 仍是主场景（形态 A），但设计成果可交付任意 Web 项目
1.2.1 — border 类派生自动对齐 WCAG UI 组件 ≥3:1（深/浅色，任意色相二分对齐不刺眼）+ heal.sh --force 先验目标快照再卸载（快照缺失/契约违反报错退出、不动现有主题，契约检查挪到备份前）
1.2.0 — derive-palette 浅色模式（--light 亮度反转）+ 非法 hex 友好报错 + 切换/还原工作流文档化（heal.sh --force / uninstall）+ scanAll 递归扫套娃 shadow root + PIL 纹理块状噪声 + feedback.json 统一落点（skill 内 data/）
1.1.0 — 风格技术库数据化（references/styles/）+ 对比度必查配对清单 + 自愈上游版本比对 + 变量数统一为 20
1.0.0 — 初始版本，含 MC 像素风 worked example