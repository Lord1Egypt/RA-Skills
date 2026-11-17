---
name: socratic-reading-coach
description: 书读完了，但说不出学到了什么——用五个问题把它问出来。苏格拉底式伴读教练：打开就是一个本地网页，搜到一本书，先给全书结构导图（非虚构→结构图，虚构→人物关系图），再让你勾出真正划过的句子，然后陪你走完五轮追问（理解原文 → 联系自身 → 批判分析 → 实际应用 → 沉淀收获），最后出一份带出处的读书小结和 Markdown 笔记。**适合「读完就忘」「划线一堆没回看」「想写书评下不了笔」。**全程在你自己电脑上跑：本地服务只监听 127.0.0.1，会话存本机，不经过任何第三方服务器；导出的划线内容属版权内容，仅供个人学习、不要公开传播。需要两样东西：微信读书 API Key（读你的书架与划线）和一个大模型 Key（生成导图与对话），都只存在你自己的机器上。 A Socratic reading companion that runs a local web app against the WeRead API: book search, whole-book structure map, highlight-driven five-round questioning, reading summary, and Markdown export. Use when the user wants to read a book deeply, turn highlights into understanding, or prepare to write a book review.
version: 1.3.0
metadata:
  openclaw:
    requires:
      env:
        - WEREAD_API_KEY
      bins:
        - node
    primaryEnv: WEREAD_API_KEY
    envVars:
      - name: WEREAD_API_KEY
        required: true
        description: 微信读书 API Key，用于搜书、获取书籍信息、热门划线、个人划线/想法
    network:
      - host: i.weread.qq.com
        purpose: 微信读书只读接口代理（搜书、书籍详情、热门划线、个人划线/想法），由本 Skill 独占代理
      - host: user-configured
        purpose: 用户在「⚙️ 设置」中填写的智谱 GLM / DeepSeek / 自定义 OpenAI 兼容端点，用于生成思维导图、苏格拉底对话和读书小结。仅在用户主动点击生成时调用
    filesystem:
      - path: ~/.zshrc ~/.bashrc
        purpose: 启动脚本只读 grep 提取 WEREAD_API_KEY，绝不执行或写入
      - path: <skill_dir>/assets/.server.pid
        purpose: 本地服务 PID 文件，用于 stop.sh 精准停止本应用进程
    emoji: "📚"
    homepage: https://github.com/bonniegeng-max/socratic-reading-coach
---

# socratic-reading-coach · AI 伴读阅读教练

本地运行的 Web 应用，将微信读书的结构化整书数据（目录+简介+热门划线+你的个人划线）与大模型结合，提供"先建全局认知 → 再钻细节 → 对话内化 → 沉淀输出"的深读体验。

## 前置条件

启动前依次检查：

1. **Node.js** — 运行 `node --version`，需 v16+。未安装则提示用户安装。
2. **微信读书 API Key** — 检查环境变量 `WEREAD_API_KEY`。未配置时搜书和划线功能不可用，需提示用户在 `~/.zshrc` 或 `~/.bashrc` 中添加 `export WEREAD_API_KEY=你的key`。
3. **大模型 API Key** — 应用首次打开后在右上角「⚙️ 设置」中配置，支持智谱 GLM 和 DeepSeek，Key 存浏览器 localStorage，可随时在设置中一键清除。未配置时思维导图和对话功能不可用。

## 启动流程

1. 定位 Skill 目录：本文件所在目录即为 Skill 根目录。
2. 运行启动脚本：
   ```bash
   bash scripts/start.sh
   ```
   脚本会自动检查 Node.js、从 shell 配置文件中**静态读取**（不执行）WEREAD_API_KEY、停掉本应用残留的旧服务、启动并打开浏览器。
3. 验证服务：访问 `http://localhost:3456/api/status`，应返回 `{"ok":true,"weread":true/false}`。
4. 浏览器自动打开 `http://localhost:3456`，若未自动打开则手动访问。

> 注意 1：本应用必须在用户本地机器上运行，不能在远程/沙箱环境中启动后让用户访问。如果当前环境不是用户本地，告知用户将 Skill 目录复制到本地后执行 `bash scripts/start.sh`。
>
> 注意 2：启动与停止脚本只管理本应用自己的服务进程。若端口 3456 被其他程序占用，脚本会提示而不是强行终止，请用户确认后自行处理。

## 隐私与安全说明

- **微信读书 API Key**：仅由本地服务进程读取，用于向 `i.weread.qq.com` 发起请求；本地代理只放行搜书、书籍信息、章节目录、热门划线、个人划线、个人想法六个只读接口，其余一律拒绝。
- **大模型 API Key**：仅保存在用户浏览器 localStorage，不经过任何第三方服务器；设置弹窗提供「清除已保存的 Key」按钮。
- **本地服务范围**：服务仅监听 `127.0.0.1:3456`，外网不可达；PID 文件用于精准停止本应用进程，不会误杀其他占用 3456 的进程。
- **前端渲染安全**：所有用户搜索词、书籍元数据、错误字符串、章节标题在写入 DOM 前均通过 `escapeHtml` 转义或 `textContent` 赋值；Mermaid 渲染使用 `securityLevel: 'antiscript'`，禁用图表内脚本执行。
- **内容外发**：对话过程中，用户勾选的划线原文（含个人划线/想法）会发送给用户自己选择的大模型供应商（智谱 / DeepSeek）。会话仅保存在本机浏览器 localStorage，不会上传到任何服务器。
- **笔记导出**：导出的 Markdown 含书籍原文划线，属受版权保护内容，仅供个人学习使用，请勿公开传播。
- **无外部依赖**：Mermaid 渲染库已打包在 `assets/mermaid.min.js` 本地加载，页面不加载任何第三方 CDN 脚本。

## 使用路径

### 路径一：搜书 → 全书导图 → 划线对话 → 沉淀输出

1. **搜索书籍**：在输入框输入书名（如《智能》《关键跃升》），点击搜索。结果书卡可直接点击跳转微信读书对应书页。
2. **查看全书结构**：搜索结果自动生成思维导图（非虚构类生成结构 mindmap，虚构类生成人物关系图 graph）。支持预览、编辑 Mermaid 代码、复制代码、导出 PNG。
3. **多选划线**：划线区顶部可在「💬 热门划线」与「🗂 我的划线」之间切换——热门划线按划线人数排序；我的划线拉取当前账号在本书的划线+想法，帮你围绕"自己真正标记过的话"对话。可多选感兴趣的段落。
4. **开始引导对话**：点击「💬 开始对话」，AI 以苏格拉底式教练身份发起 5 轮递进提问（理解原文→联系自身→批判分析→实际应用→沉淀收获），用户逐轮回答；AI 回复**流式输出**。对话进度自动保存在本机，**刷新页面可一键恢复**。
5. **读书小结**：5 轮结束后点击「📝 生成读书小结」，AI 按"核心观点 / 我的启发 / 可应用点"输出 300–500 字小结。
6. **导出笔记**：点击「📥 导出笔记」，下载带书名/作者/评分等出处元数据、按章节分组的 Markdown 文件（含原文与可选读书小结，仅供个人学习）。

### 路径二：仅生成全书思维导图

搜索书籍后，思维导图自动生成在结果上方。可直接编辑、导出，无需进入对话。

## 核心功能说明

| 功能 | 依赖 | 说明 |
|---|---|---|
| 微信读书搜书 | WEREAD_API_KEY | 调用 `/store/search`，返回书名/作者/封面/评分 |
| 全书结构导图 | 大模型 API Key | 基于书籍简介+章节目录，自动判断书籍类型后生成 mindmap 或 graph；流式输出 |
| 万人热门划线 | WEREAD_API_KEY | 调用 `/book/bestbookmarks`，按划线人数排序 |
| 我的划线/想法 | WEREAD_API_KEY | 调用 `/book/bookmarklist` + `/review/list/mine`，与热门划线一键切换 |
| 苏格拉底对话 | 大模型 API Key | 5 轮递进提问，流式输出；基于勾选的划线原文（热门/个人均可） |
| 会话恢复 | 无 | localStorage 持久化，刷新后恢复对话进度并续问 |
| 读书小结 | 大模型 API Key | 对话结束后一键生成，核心观点/我的启发/可应用点 |
| 笔记导出 | 无 | 前端生成带出处元数据的 Markdown 并下载 |

## 故障排查

| 现象 | 原因 | 解决 |
|---|---|---|
| 页面显示"无法连接到本地服务" | 在 Preview 面板或非本地环境中打开 | 在浏览器中访问 `http://localhost:3456`，必须在运行服务的同一台机器上 |
| 搜索失败 / errcode 非 0 | WEREAD_API_KEY 未配置或无效 | 检查环境变量，重新配置后重启服务 |
| 思维导图区域提示"还没有配置 API Key" | 未在设置中填大模型 Key | 点击右上角「⚙️ 设置」，配置智谱或 DeepSeek 的 API Key |
| 我的划线/想法为空 | 该书未划线，或接口权限问题 | 先在微信读书 App 中划线后重试；若报错请查看浏览器 Console 中的错误码 |
| 对话中途刷新后进度丢失 | 未点击恢复横幅 | 刷新后页面顶部出现"检测到未完成的对话"，点击「恢复会话」即可续问 |
| 端口 3456 被占用 | 之前的服务未正常关闭 | 运行 `bash scripts/stop.sh` 释放端口后重新启动；若是其他程序占用，脚本会提示，请自行确认处理 |
| 导图渲染为纯文本代码 | Mermaid 语法有误 | 点击「✏️ 编辑」修改代码后点击「🔄 重新渲染」 |
| PNG 导出失败 | SVG 尚未渲染完成或浏览器兼容性问题 | 稍等渲染完成后重试，或复制代码到 mermaid.live 导出 |

## 停止服务

- 方式一：在运行服务的终端按 `Ctrl+C`
- 方式二：另开终端运行 `bash scripts/stop.sh`（只终止本应用进程，不影响端口上的其他程序）

## 扩展参考

- 微信读书 API 接口详情、参数和返回字段：见 [references/weread-api.md](references/weread-api.md)
- 前端源码：`assets/ai-reading-companion.html`
- 服务端源码：`assets/server.js`（端口 3456，代理微信读书 API + 静态文件服务）
