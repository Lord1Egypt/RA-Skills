# Real mousic-skills (真正的音乐)

<p align="center">
  <img src="real-mousic.jpg" alt="Mousic 吉祥物 - 哞听歌" width="200">
</p>

> 🐄 **Mousic** = **Mou** (奶牛叫声) + **Sic** = 真正的音乐！
> 
> 吉祥物：一头热爱音乐的奶牛 🐄🎵

歌曲下载 Skills，基于 Python CDP 浏览器自动化引擎。

支持 [OpenClaw](https://github.com/anthropics/openclaw) 及所有兼容 `SKILL.md` 格式的 AI Agent 平台（如 Claude Code）。

## ⚠️ 重要免责声明

**使用本工具前请务必阅读并理解以下声明：**

### 1. 项目性质与功能范围
- 本项目**仅供技术学习和研究使用**，展示浏览器自动化技术的应用
- **严禁用于任何商业用途**，包括但不限于：付费服务、数据倒卖、商业爬虫等
- 本项目不提供任何形式的担保，也不保证持续可用

### 2. 功能限制声明
- 本项目**不提供直接下载功能**，只提供下载链接
- 本项目**不保证下载链接的有效性**，链接可能随时失效
- 下载链接来源于第三方网站，请用户自行判断安全性

### 3. 版权声明
- 本工具仅提供搜索和链接获取功能，**不存储任何音乐文件**
- 所有音乐版权归原版权方所有
- 请用户遵守相关法律法规，**不要下载未经授权的音乐作品**
- 如有版权问题，请通过官方渠道获取音乐

### 4. 法律免责
- 使用者需自行遵守相关法律法规
- 使用者需自行承担因使用本工具产生的一切法律责任和后果
- 本工具开发者**不对任何因使用本工具导致的法律纠纷负责**

### 5. 魔改免责声明
- 任何人对本项目进行修改、增删功能、二次开发等行为，均与原作者无关
- 修改后的版本所产生的一切问题和后果，由修改者自行承担
- 原作者不对任何衍生版本、分支版本负责

### 6. 项目来源
- 本项目基于 [xiaohongshu-skills](https://github.com/Auto-Claw-CC/xiaohongshu-skills) 改造
- 核心自动化引擎继承自该项目
- 若有关于自动化引擎的问题，可向原作者反馈

### 7. 权利保留
- 若任何权利方认为本项目侵犯其合法权益，请通过 GitHub Issue 联系我们
- 收到通知后，我们将在 **24 小时内** 对争议内容进行评估并采取相应措施
- 我们尊重所有权利方的合法权益，并愿意积极配合处理

**继续使用本工具即表示您已阅读、理解并同意以上全部内容。如有异议，请立即停止使用。**

---

## 功能概览

### 核心功能：搜索歌曲并获取下载链接

通过歌曲海网站 (gequhai.com) 搜索歌曲，返回下载链接（支持夸克网盘和直链下载）。

### 功能列表

| 功能 | 说明 |
|------|------|
| **搜索歌曲** | 根据歌名搜索，返回最多10个结果 |
| **获取下载链接** | 获取高品质（夸克网盘）和低品质下载链接 |
| **链接验证** | 验证夸克网盘链接格式，提示非夸克链接风险 |

## 安装

### 前置条件

- Python >= 3.11
- [uv](https://docs.astral.sh/uv/) 包管理器
- Google Chrome 浏览器

### 方法一：下载 ZIP 安装（推荐）

1. 在 GitHub 仓库页面点击 **Code → Download ZIP**，下载项目压缩包。
2. 解压到你的 Agent 的 skills 目录下：

```
# OpenClaw 示例
<openclaw-project>/skills/real-mousic-skills/

# Claude Code 示例
<your-project>/.claude/skills/real-mousic-skills/
```

3. 安装 Python 依赖：

```bash
cd real-mousic-skills
uv sync
```

### 方法二：Git Clone

```bash
cd <your-agent-project>/skills/
git clone https://github.com/Xiaoyiyebuaijianghua/real-mousic-skills.git
cd real-mousic-skills
uv sync
```

## 使用方式

### 作为 AI Agent 技能使用（推荐）

安装到 skills 目录后，直接用自然语言与 Agent 对话即可：

> "帮我下载《渡口》这首歌"

> "搜索周杰伦的《稻香》"

### 作为 CLI 工具使用

#### 1. 启动 Chrome

```bash
python -m real_mousic.chrome_launcher
```

#### 2. 搜索歌曲

```bash
python -m real_mousic.cli search --song "渡口"
```

#### 3. 获取下载链接

```bash
python -m real_mousic.cli download --detail-url "https://www.gequhai.com/song/xxx" --title "渡口" --artist "蔡琴"
```

#### 4. 搜索+下载一步到位

```bash
python -m real_mousic.cli get --song "渡口" --index 1
```

## CLI 命令参考

| 子命令 | 说明 |
|--------|------|
| `search --song` | 搜索歌曲 |
| `download --detail-url` | 获取下载链接 |
| `get --song --index` | 搜索+下载一步到位 |

## 项目结构

```
real-mousic-skills/
├── src/real_mousic/             # Python CDP 自动化引擎
│   ├── music/                   # 歌曲下载模块
│   │   └── search.py            # 搜索和下载链接获取
│   ├── xhs/                     # CDP 浏览器控制
│   │   ├── cdp.py               # CDP WebSocket 客户端
│   │   ├── stealth.py           # 反检测脚本
│   │   └── ...
│   ├── cli.py                   # 统一 CLI 入口
│   └── chrome_launcher.py       # Chrome 进程管理
├── SKILL.md                     # 技能入口
├── pyproject.toml               # uv 项目配置
└── README.md
```

## 技术架构

```
用户 ──→ AI Agent ──→ SKILL.md ──→ CLI ──→ CDP 引擎 ──→ Chrome ──→ 歌曲海网站
```

## 开发

```bash
uv sync                    # 安装依赖
uv run ruff check .        # Lint 检查
uv run ruff format .       # 代码格式化
uv run pytest              # 运行测试
```

## 致谢

本项目基于 [xiaohongshu-skills](https://github.com/Auto-Claw-CC/xiaohongshu-skills) 改造，保留了核心的 CDP 自动化引擎。

## License

MIT

Copyright (c) 2026 Auto-Claw-CC
Copyright (c) 2026 Xiaoyiyebuaijianghua
