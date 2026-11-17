# REA-CN 外部二进制 Provider 下载与安装指南

> **本文档回答一个问题**：REA 是「中间件」，自己不带任何二进制分析器。
> 它靠桥接你本机已安装的 provider（Ghidra / IDA / JADX / JEB / adb / apktool / binwalk / 浏览器）干活。
> 本技能**只自动装 Node 依赖**（见 `install-guide.md` 第 3.1 节，约 91MB、15s），
> **绝不自动下载/安装下面这些外部二进制软件**——它们体积大（全装齐约 2GB+），需你按目标类型**自备**。
>
> 本文档给出每个 provider 的：**官方下载地址 · 体积 · 平台 · 授权 · REA 用途 · 配置方式 · 安装步骤**。

---

## 0. 先分清两类依赖（避免混淆）

| 类别 | 是什么 | 体积 | 谁负责装 | 文档 |
|---|---|---|---|---|
| **A. Node 依赖** | `engine/` 运行所需的 npm 包（zod、@modelcontextprotocol 等 143 个） | 约 91MB | 本技能 `run-mcp.mjs` / `cn-installer.mjs` **自动装**（npmmirror，15s） | `install-guide.md` §3.1 |
| **B. 外部二进制 Provider** | Ghidra / IDA / JADX / JEB / adb / apktool / binwalk / 浏览器等分析器本体 | **每个几十 MB ~ 数百 MB，全装约 2GB+** | **你自备**（本文档） | 本文档 |

> 你前面问的"多 G"指的是 **B 类（外部二进制）**。A 类由智能体自动查缺补漏，B 类需要你按下面的方法手动下载安装。

## 下载方式：国内镜像优先 · GitHub 原址备选

国内网络访问 GitHub 与原厂站点常不稳定。本文档所有 **来自 GitHub Releases** 的资源（Ghidra、JADX 等），均支持两种下载方式，**默认走国内镜像，镜像不可用再回退 GitHub 原址**：

| 方式 | 怎么用 | 何时用 |
|---|---|---|
| **① 国内镜像 / 加速（首选）** | 把 `https://github.com/...` 整体替换为社区反代镜像，例如：`https://ghproxy.net/https://github.com/...` 或 `https://mirror.ghproxy.com/...`（镜像地址可能随网络政策变动，以实际可访问为准） | GitHub 直连慢 / 不通时 |
| **② GitHub 原址备选** | 直接用各小节给出的 `github.com` 原始链接 | 镜像失效、或网络本身正常时 |

> **原则：镜像优先、GitHub 兜底。** 各小节标注「GitHub」的条目均已确认此双路可用；
> 商业软件（IDA / JEB / Hopper）无镜像，只能走官网。JDK 另有稳定的国内高校镜像（见 2.1）。

---

## 1. 体积速览（决定你到底要装哪些）

| Provider | 下载体积 | 安装后占用 | 平台 | 授权 | REA 用途 | 关键配置 |
|---|---:|---:|---|---|---|---|
| **Ghidra** | ~543 MB（zip）+ JDK 21 ~200 MB | ~1 GB + 4 GB RAM | Win/macOS/Linux | 免费开源（Apache-2.0 + GPL） | 通用反汇编/反编译（最常用） | 放 `ghidraRun`/`analyzeHeadless` 到 PATH；`open_binary` 用 `provider_id:"ghidra"` |
| **JADX** | ~20–30 MB | 极小 | Win/macOS/Linux（需 Java） | 免费开源 | Android / Dalvik 反编译 | 放 `jadx`/`jadx.bat` 到 PATH |
| **apktool** | ~10 MB（需另装 Java） | 极小 | 全平台（需 Java） | 免费开源 | Android 资源解码 | `REA_APKTOOL_COMMAND` 或 PATH |
| **binwalk / unblob** | 极小（Python 包） | 极小 | 全平台（需 Python） | 免费开源 | 固件 / 打包产物提取 | 装好后 PATH 可用 |
| **adb（platform-tools）** | ~15–30 MB | 极小 | 全平台 | 免费（Google） | Android 设备/包交互 | `REA_ADB_PATH` 指向 `adb`/`adb.exe` |
| **JEB** | 数百 MB | 数百 MB | Win/macOS/Linux | **商业**（PNF Software） | Android/Java 高级分析 | 先启动 JEB MCP，配 `REA_JEB_MCP_URL`（默认 `http://127.0.0.1:8425/mcp`） |
| **IDA Free** | ~100–400 MB（视版本，IDA 9.4 安装包约 411 MB） | ~1 GB | Win/macOS/Linux | 免费版**仅限非商业**、x86/x64、云反编译 | 通用反汇编（高质量） | `open_binary` 用 `provider_id:"ida"`，需先配 IDA MCP |
| **IDA Pro** | 同 Free 量级（商业订阅） | ~1 GB+ | 全平台 | **商业**（Essential/Expert/Ultimate 年订阅） | 全架构反编译/调试 | 同上，需 IDA MCP |
| **Hopper** | ~100–200 MB | 极小 | **仅 macOS** | 商业 | macOS 二进制分析 | `open_binary` 用 `provider_id:"hopper"` |
| **浏览器（Chromium 系）** | ~150 MB（若需另装） | 极小 | 全平台 | 免费 | Web 模块导入 / 原生导入 | `REA_BROWSER_EXECUTABLE` 指向 chromium/chrome 可执行文件 |

> **全装齐 ≈ 2GB+**（Ghidra 543MB + JDK 200MB + IDA 400MB + JEB 数百 MB + Hopper 150MB + 浏览器 150MB + 其余零散）。
> **强烈建议"按目标类型选装"，不要无脑全装**（见第 6 节最小集）。

---

## 2. 各 Provider 下载与安装步骤

### 2.1 Ghidra（最常用，免费，强烈建议首选）

- **下载**（二选一）：
  - **国内镜像（推荐）**：用 `https://ghproxy.net/https://github.com/NationalSecurityAgency/ghidra/releases` 或 `https://mirror.ghproxy.com/https://github.com/NationalSecurityAgency/ghidra/releases` 打开发布页，再下载对应 zip（镜像地址可能变动，失效就换 GitHub 原址）。
  - **GitHub 原址备选**：<https://github.com/NationalSecurityAgency/ghidra/releases>
  - 下载形如 `ghidra_12.1.3_PUBLIC_20260817.zip` 的 **PUBLIC** 资源（当前 12.1.3，约 543 MB）。
  - ⚠️ **不要**下 "Source Code" 那两个（那是源码，不是发布包）。
- **前置：装 JDK 21（64 位，必须 JDK 不是 JRE）**
  - 免费发行版（任选）：
    - 国内镜像（推荐）：<https://mirrors.tuna.tsinghua.edu.cn/Adoptium/21/jdk/x64/windows/>（清华大学 TUNA 镜像，稳定可用；macOS/Linux 同理切目录）或华为云镜像 `https://mirrors.huaweicloud.com/openjdk/`。
    - 原厂备选：<https://adoptium.net/temurin/releases/?version=21>（选 Windows x64 / macOS / Linux 的 `.msi` 或压缩包，安装时勾选 "Add to PATH"）。
  - 验证：`java -version` 应显示 `21.x`。
- **安装**：解压 zip 到**纯英文路径**（如 `C:\Reverse\ghidra`），无安装程序，绿色软件。
- **REA 接入**：确保 `ghidraRun.bat` / `analyzeHeadless` 在 PATH；调用时 `open_binary` 传 `provider_id:"ghidra"`。
- **平台坑**：
  - macOS：解压前先 `xattr -d com.apple.quarantine ghidra_*.zip` 解除 Gatekeeper 隔离，否则原生组件无法运行。
  - 中文/空格路径会导致 Ghidra 启动失败——务必纯英文目录。

### 2.2 JADX（Android / Dalvik 反编译，免费）

- **下载**（二选一）：
  - **国内镜像（推荐）**：`https://ghproxy.net/https://github.com/skylot/jadx/releases` 或 `https://mirror.ghproxy.com/https://github.com/skylot/jadx/releases`。
  - **GitHub 原址备选**：<https://github.com/skylot/jadx/releases>（下 `jadx-1.x.zip`，约 20–30 MB，需本机有 Java）。
- **安装**：解压，把 `bin/jadx`(Linux/macOS) 或 `bin/jadx.bat`(Windows) 所在目录加入 PATH。
- **REA 接入**：PATH 可用即可，Android 类目标 REA 会自动桥接。

### 2.3 apktool（Android 资源解码，免费）

- **下载 / 说明**：<https://apktool.org>（需本机已装 Java）。
- **安装**：按官网把 `apktool.jar` + wrapper 脚本放到 PATH（Windows 用 `apktool.bat`）。
- **REA 接入**：设 `REA_APKTOOL_COMMAND` 为绝对路径，或保证 `apktool` 在 PATH。

### 2.4 binwalk / unblob（固件提取，免费）

- **安装**（Python，推荐虚拟环境）：
  ```bash
  pip install binwalk          # 或 unblob（功能更强）
  ```
- **REA 接入**：PATH 可用即可，固件/打包产物类目标 REA 自动桥接。

### 2.5 adb（Android platform-tools，免费，Google）

- **下载**：<https://developer.android.com/tools/releases/platform-tools>（下 `platform-tools-*.zip`，约 15–30 MB）。
- **安装**：解压，把 `platform-tools/` 加入 PATH。
- **REA 接入**：设 `REA_ADB_PATH`（Windows 指向 `...\platform-tools\adb.exe`），或保证 `adb` 在 PATH。Android 设备/包交互类工具需要。

### 2.6 JEB（商业，Android/Java 高级分析）

- **下载 / 购买**：<https://www.pnfsoftware.com/>
- **REA 接入**：先启动 JEB 并开启其 **MCP 服务**，再设 `REA_JEB_MCP_URL`（默认 `http://127.0.0.1:8425/mcp`）。详见 `config-keys.md`。

### 2.7 IDA Free / IDA Pro（通用反汇编，高质量）

- **IDA Free（免费，非商业）**：
  - 下载：<https://www.hex-rays.com/products/ida/support/download_freeware.shtml>
  - 体积：安装包约 100–400 MB（IDA 9.4 的 `ida-free-pc_94_x64win.exe` 约 411 MB）。
  - 限制：仅 x86/x86-64、云反编译、仅供**非商业**用途、无 IDAPython/C++ SDK。
- **IDA Pro（商业）**：<https://hex-rays.com/>，Essential/Expert/Ultimate 年订阅，全架构反编译与调试。
- **REA 接入**：`open_binary` 传 `provider_id:"ida"`，需先在本机配置好 **IDA MCP**（REA 通过该 MCP 与之通信）。

### 2.8 Hopper（仅 macOS，商业）

- **下载 / 购买**：<https://www.hopperapp.com/>
- **REA 接入**：`open_binary` 传 `provider_id:"hopper"`；macOS 专用 GUI 桥。

### 2.9 浏览器（Web 模块，免费）

- **用途**：REA 的 Web 模块导入 / 原生导入需要 Chromium 系浏览器。
- **REA 接入**：设 `REA_BROWSER_EXECUTABLE` 指向 `chrome` / `chromium` / `msedge` 可执行文件绝对路径；若 PATH 中已能找到也可不设。

---

## 3. 配置键速查（装完后怎么"指"给 REA）

| 配置键 | 对应 Provider | 设置示例 |
|---|---|---|
| （PATH） | Ghidra / JADX / apktool / binwalk / adb（未单独指定时） | 把各自 `bin` 目录加入 PATH |
| `REA_ADB_PATH` | adb | `C:/Android/platform-tools/adb.exe` |
| `REA_APKTOOL_COMMAND` | apktool | `C:/tools/apktool.bat` |
| `REA_JEB_MCP_URL` | JEB | `http://127.0.0.1:8425/mcp`（先启动 JEB MCP） |
| `REA_BROWSER_EXECUTABLE` | 浏览器 | `C:/Program Files/Google/Chrome/Application/chrome.exe` |
| `provider_id`（open_binary 入参） | ghidra / ida / hopper | 见 `config-keys.md` 第 3 节 |

完整键说明见 `references/config-keys.md`。

---

## 4. 安装后验证是否就绪

```bash
node scripts/route.mjs        # 会列出 Node / engine / 各二进制 provider 的就绪情况
```

- 若某 provider 显示"未就绪"，回到本文档对应小节安装，并确认其可执行文件在 PATH 或已配置对应环境变量。
- 也可在 REA 内用 `binary_session`（入参 `{}`）查看 `result.tool_availability`，确认目标 provider 是否可用及其不可用原因。

---

## 5. 路径与环境的铁律（中文环境高频坑）

- **所有 provider 装到纯英文、无空格路径**（如 `C:\Reverse\ghidra`）。中文/空格路径会导致 Ghidra/IDA 启动失败。
- **Ghidra 必须有 JDK 21（JDK 不是 JRE）**，且 `java -version` 为 21.x。
- **Java 类工具**（JADX/apktool/JEB）依赖本机 Java，需先装好 JDK/JRE 并加入 PATH。
- 上述二进制与 Node 依赖**互不替代**：Node 依赖让 `engine/` 能跑起来；二进制 provider 是被 `engine/` 调用的分析器。两者都齐，REA 才能完整工作。

---

## 6. 推荐最小集（按目标类型，避免无脑全装多 G）

| 你的目标 | 只需装 |
|---|---|
| 通用二进制/固件反编译 | **Ghidra**（+JDK 21） |
| Android APK/DEX 分析 | **JADX** + **apktool** + **adb**（可选，连真机时） |
| 固件 / 打包产物提取 | **binwalk / unblob** |
| Windows/Linux 原生 EXE/ELF 高质量分析 | **IDA Free**（非商业）或 **Ghidra** |
| macOS 原生二进制 | **Hopper** |
| Web / 浏览器目标 | 任意 **Chromium 系浏览器** |
| 企业级 Android/Java | **JEB**（商业） |

> 绝大多数中文环境审计场景，**Ghidra + JDK 21** 一个组合就覆盖了 80% 需求，体积约 750MB，远比全装 2GB+ 划算。

---

## 7. 国内镜像 vs GitHub 原址 · 下载地址汇总

下表把本文档所有「来自 GitHub」的下载源集中列出。**统一规则：镜像优先、GitHub 兜底**（镜像地址可能随网络政策变动，失效即换原址）。

| 资源 | 国内镜像（推荐，把 `github.com` 换成前缀） | GitHub 原址备选 | 备注 |
|---|---|---|---|
| **Ghidra** | `https://ghproxy.net/https://github.com/NationalSecurityAgency/ghidra/releases` 或 `https://mirror.ghproxy.com/https://...` | <https://github.com/NationalSecurityAgency/ghidra/releases> | 下 PUBLIC zip（约 543MB） |
| **JADX** | `https://ghproxy.net/https://github.com/skylot/jadx/releases` 或 `https://mirror.ghproxy.com/https://...` | <https://github.com/skylot/jadx/releases> | 约 20–30MB，需 Java |
| **JDK 21（Temurin）** | 清华大学 TUNA：`https://mirrors.tuna.tsinghua.edu.cn/Adoptium/21/jdk/x64/windows/`（macOS/Linux 切目录）；华为云：`https://mirrors.huaweicloud.com/openjdk/` | <https://adoptium.net/temurin/releases/?version=21> | 必须 JDK 非 JRE |
| **apktool** | 无独立镜像，随官网脚本走（体积小） | <https://apktool.org> | 需先装 Java |
| **adb（platform-tools）** | 若无直连可搜 `platform-tools` 的 GitHub 镜像 zip；或经 `ghproxy.net` 中转 Google 链接 | <https://developer.android.com/tools/releases/platform-tools> | Google 官方，约 15–30MB |
| **binwalk / unblob** | `pip install` 走国内 PyPI 镜像（如 `https://pypi.tuna.tsinghua.edu.cn/simple`） | `pip install binwalk` | Python 包，无需二进制下载 |

> 开源加速器前缀常用：`https://ghproxy.net/`、`https://mirror.ghproxy.com/`（任选其一，以实际可访问为准）。
> **商业软件无镜像**：IDA（<https://hex-rays.com>）、JEB（<https://www.pnfsoftware.com/>）、Hopper（<https://www.hopperapp.com/>）只能走官网，按第 2 节链接下载。
> npm 依赖（Node 类）已由 `cn-installer.mjs` / `run-mcp.mjs` 默认走 `https://registry.npmmirror.com` 国内镜像，无需手动处理。
