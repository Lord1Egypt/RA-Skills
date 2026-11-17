# 图形资产管线 · 原样复刻 × 从文字生成（v2.3）

> 本文件是 reading-notes-master 的图形工具链总纲：笔记里需要的任何**图型 / 图片 / 图表**，
> 要么从既有素材**原样复刻**（路径 A），要么从文字**直接生成**（路径 B）。
> 全部工具已于 2026-10-20 在本机（macOS arm64 + WorkBuddy 托管运行时）安装并用真实样张实测。
> 包装脚本见 `scripts/`，开箱即用；工具缺失时按 §4 安装命令补齐。

## 1. 路径 A · 原样复刻（7 环节）

适用：复刻已有 PDF/PPTX 笔记中的图形资产（矢量器型图、位图照片、图表）。

| # | 环节 | 工具/技能 | 状态 |
|---|---|---|---|
| A1 | 分层解析提取（矢量/位图/文字分离） | PyMuPDF 1.28（managed venv）+ python-pptx 1.0.2 | ✅ |
| A2 | 版式克隆三件套复刻 | `brand-pdf-deck-replica`（探针→反解 CSV→重画→pptx+pdf+html） | ✅ 技能 |
| A3 | 视觉理解（看懂图） | `sn-image-base` VLM（SenseNova）；本地兜底 `ollama pull qwen2.5vl` | ✅ 走 API |
| A4 | 风格模仿重绘 | `sn-image-imitate`（标注→改写→生成）+ 内置 ImageGen | ✅ |
| A5 | **位图→矢量描摹** | **vtracer 0.6.15**（彩色）/ **potrace 1.16**（黑白）→ `scripts/bitmap2vector.sh` | ✅ 实测 |
| A6 | **高清化超分** | **upscayl-bin**（Real-ESRGAN ncnn-vulkan，realesrgan-x4plus 模型内嵌）→ `scripts/superres.sh` | ✅ 实测 |
| A7 | 矢量图表按反解数据重画 | `brand-pdf-deck-replica` + `consulting-chart-book` | ✅ |

**A5+A6 组合拳**（位图照片→出版级矢量）：先 `superres.sh` 4× 超分提升细节，再
`bitmap2vector.sh` 描摹成 SVG——描摹质量显著优于直接对原图描摹。

## 2. 路径 B · 从文字生成（9 环节，工具层强化）

| # | 环节 | 工具/技能 | 状态 |
|---|---|---|---|
| B1 | 要点→器型转译 | 本技能 `references/visual-grammar.md` §2 映射表（12 类） | ✅ |
| B2 | 组件化器型 | `references/chart-catalog.md`（10 类 SVG 组件） | ✅ |
| B3 | 数据图表 | `chart-image` / `market-chart-cookbook`（涨红跌绿）/ matplotlib 3.11 | ✅ |
| B4 | **图表即代码** | **mermaid-cli 12.0.0**（mmdc：流程图/时序图/甘特）→ `scripts/mermaid-export.sh` | ✅ 实测 |
| B5 | **思维导图** | **markmap-cli 0.18.12**（md→交互 HTML）+ **cognigraph MCP**（§5） | ✅ 实测 |
| B6 | AI 位图/信息图 | 内置 ImageGen + `sn-infographic` + `openai-image-gen` | ✅ |
| B7 | 找参考图 | `sn-search-image`（需 SERPER_API_KEY）+ `refero-design` | ✅ |
| B8 | 组装 16:9 幻灯片 | 本技能模板 + `html-ppt` | ✅ |
| B9 | 导出 PDF/PPTX/长图 | `templates/output-pipelines.md` + `html-to-pdf-cdp` | ✅ |
| B4+ | **文本→SVG 图表（极客线）** | **asmuth/clip 0.8.0**（.clp 图表语言）→ `scripts/clip-chart.sh` | ✅ 实测 |

## 3. 工具注册表（本机实测锚点）

| 工具 | 版本 | 发现路径 | 用途 | 关键产物 SHA256（前 16） |
|---|---|---|---|---|
| vtracer | 0.6.15 | managed venv `.../envs/default/bin/vtracer`（自写 CLI 包装器） | 彩色位图→SVG | 854c521d（样张描摹） |
| potrace | 1.16 | `potrace`（brew） | 黑白位图→SVG | d6ad7629 |
| mmdc | 12.0.0 | managed node workspace `.bin/mmdc` | mermaid→SVG/PNG/PDF | f31e1806 / 1ad3403b / 51bdc89f |
| markmap | 0.18.12 | managed node workspace `.bin/markmap` | md→思维导图 HTML | 347,974 字节样张 |
| upscayl-bin | 20251207 | `~/.workbuddy/bin/upscayl-bin` | Real-ESRGAN 4× 超分 | 3833b825（2808×2804 样张） |
| clip | 0.8.0 | `~/.workbuddy/bin/clip` | .clp 文本→SVG 图表 | 429ed60c（官方 demo 导出） |
| cognigraph-mcp-server | 0.1.7 | managed node workspace（MCP，见 §5） | markmap+mermaid 封装 4 工具 | 4c47b4af（握手日志） |

输入样张：从《未来呼啸而来》p1 抽取的真实位图 702×701（SHA256 前 16：8fa48dfd）。

## 4. 安装命令（新机器补装清单）

依 WorkBuddy 托管运行时隔离规则：**禁 `pip install -g/--user`、禁 `npm install -g`**，全部入托管环境。

```bash
# ① 位图→矢量描摹
/Users/wdj/.workbuddy/binaries/python/envs/default/bin/pip install vtracer   # PyPI 版无 CLI，包装器见 scripts/
brew install potrace pkg-config

# ② 图表即代码（PUPPETEER_SKIP_DOWNLOAD=1 复用本机 Chrome，不下载 Chromium）
cd ~/.workbuddy/binaries/node/workspace && npm install @mermaid-js/mermaid-cli markmap-cli

# ③ Real-ESRGAN 超分（预编译，arm64 universal；勿走 pip realesrgan——basicsr 1.4.2 与 Python 3.13 不兼容）
curl -L -o upscayl-bin-macos.zip https://github.com/upscayl/upscayl-ncnn/releases/latest
#   注：经代理时若下载为空，先 curl -sI 取 Location 直链再下载（见 §6 踩坑 3）
unzip upscayl-bin-macos.zip && cp upscayl-bin-*/upscayl-bin ~/.workbuddy/bin/

# ④ 文本→SVG 图表 CLI（源码编译，约 12s）
git clone https://github.com/asmuth/clip.git && cd clip \
  && cmake . -DCMAKE_BUILD_TYPE=Release -DCMAKE_POLICY_VERSION_MINIMUM=3.5 && make -j7 \
  && cp clip ~/.workbuddy/bin/          # git 被代理拦截时改用 codeload tarball（见 §6 踩坑 4）

# ⑤ cognigraph MCP（见 §5）

# ⑥ 可选：本地视觉模型（离线 VLM 兜底）
ollama pull qwen2.5vl
```

## 5. MCP 集成：cognigraph-mcp-server（markmap+mermaid 封装）

将 mermaid/markmap 封装为 4 个 MCP 工具，供任何 MCP 宿主（WorkBuddy/OpenClaw）直接调用：
`generate_mindmap` / `generate_and_save_mindmap` / `generate_relationship_graph` / `generate_knowledge_graph`。

**配置**（`~/.workbuddy/mcp.json`，与其他服务器 merge 勿整体覆盖）：

```json
"cognigraph-mcp-server": {
  "command": "npx",
  "args": ["-y", "cognigraph-mcp-server"],
  "env": {
    "MINDMAP_DEFAULT_SAVE_DIR": "~/WorkBuddy/cognigraph-output",
    "PATH": "<托管 workspace>/.bin:<托管 node>:/opt/homebrew/bin:/usr/bin:/bin",
    "PUPPETEER_EXECUTABLE_PATH": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "OPENAI_BASE_URL": "http://localhost:11434/v1",
    "OPENAI_API_KEY": "ollama",
    "OPENAI_DEFAULT_MODEL": "qwen3.8:27b-mtp-q8-ctx16k"
  }
}
```

- OPENAI_* 指向本地 Ollama（README 推荐模式，零 key）；仅 `generate_knowledge_graph` 用到 LLM。
- 写入后**需在连接器管理页面对该服务器点 Trust 激活**。
- **stdio 握手验证**（装完必做）：见 §6 踩坑 5 的保活脚本，预期能捕获
  `initialize → mindmap-server 0.1.0` 与 `tools/list → 4 工具`。

## 6. 踩坑库（实测血泪，排障先查这里）

| # | 坑 | 根因 | 修复 |
|---|---|---|---|
| 1 | mmdc 报 `unknown option '-w'` | mermaid-cli 12 移除了 `-w/-H` | 用 `-s 2`（Puppeteer scale factor）控制分辨率 |
| 2 | mmdc 下载 Chromium 失败/被杀 | 沙箱内无头下载易 SIGKILL | `PUPPETEER_SKIP_DOWNLOAD=1` + puppeteer-config.json 指向本机 Chrome：`{"executablePath": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "args": ["--no-sandbox", "--disable-gpu"]}` |
| 3 | GitHub release 下载得到空文件 | 代理对 302 重定向吞 content-length:0 | 先 `curl -sI <release-url>` 取 `location:` 直链（release-assets.githubusercontent.com），再对直链 `curl -L` 下载 |
| 4 | `git clone github.com` 报 Empty reply from server | 代理拦截 git 协议 | 改用 `codeload.github.com/<user>/<repo>/tar.gz/refs/heads/master` |
| 5 | `npx -y <pkg>` 报 CODEBUDDY_BROKER_DENY | npx 缓存 rename 被 broker 拒 | `npm install <pkg>` 入 managed workspace 后 node 直跑入口；MCP 服务器建议直跑入口而非 npx |
| 6 | pip realesrgan 构建失败 EEXIST | basicsr 1.4.2 sdist 与 Python 3.13 不兼容 | 弃 pip 版，用 upscayl-bin 预编译（Real-ESRGAN ncnn-vulkan 官方模型内嵌） |
| 7 | clip 编译报 Could NOT find HarfBuzz | FindHarfBuzz 依赖 pkg-config，本机未装 | `brew install pkg-config` 后重跑 cmake |
| 8 | clip 用 CMake 4.x 编译失败 | CMake 4 移除 <3.5 兼容 | `cmake . -DCMAKE_POLICY_VERSION_MINIMUM=3.5` |
| 9 | vtracer pip 装完无命令 | PyPI 版只提供 Python bindings，无 CLI 二进制 | 用 `scripts/` 内包装器（argparse 封 vtracer.convert_image_to_svg_py），输出与 Python API 哈希一致 |
| 10 | 主模型读图报错 does not support reading images | GLM 文本模型无视觉 | 图像理解走 sn-image-base VLM；或本地 `ollama pull qwen2.5vl` |
| 11 | mmdc 报 EEXIST: mkdir '<临时目录>' | mmdc 12 对 puppeteer-config 所在 mktemp 临时目录 mkdir 冲突 | config 写到**输出文件同目录**（已存在），用完删除（`scripts/mermaid-export.sh` 已内置） |
| 12 | clip 报 error while reading file: data 文件不存在 | clip 的 `data:` 相对路径按**调用者 cwd** 解析，包装脚本不应改变 cwd | `scripts/clip-chart.sh` 保持调用者 cwd，仅对输入输出传绝对路径 |

## 7. 与技能主工作流的对接点

- **Step 3 转译**产出的器型清单，凡是"流程/关系/层级"类 → 优先 B4（mmdc 出 SVG 内嵌），
  复杂多分支可试 clip（.clp 语言，精确控制轴/线型）；"全书结构一图流"收尾页 → markmap。
- **Step 4 排页**需要素材位图高清化时 → A6 超分后再嵌入模板；位图要可编辑矢量时 → A5 描摹。
- **Step 5 导出**前，混合素材（SVG 器型 + mermaid SVG + 照片）统一 16:9 校验，再走 output-pipelines.md。
- 所有图表输出遵守中国市场约定：**涨红跌绿**、货币 ¥（详见 design-system.md）。
