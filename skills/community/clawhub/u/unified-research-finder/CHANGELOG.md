# 更新日志 / Changelog

## [v1.1.1] — 2026-07-24

### 🚀 数据源扩展

**#4 新增 KipHub 学术 + 学术搜索Pro 镜像，修复烂番薯反爬**

- **现象**：2026-07-24 起，中国 Scholar 镜像站普遍升级反爬策略，原四源全部不可达（dotaindex API 500、烂番薯 403、hk/google 超时）。
- **修复**：
  - 新增 **KipHub学术**（`kiphub.com`，自定义 `paper-summary-wrapper` 解析器）和 **学术搜索Pro**（`googlescholar.pro`，`card-title/card-meta/card-text` 解析器）。
  - 修复烂番薯：URL 中加入 `hl=zh-CN&as_sdt=0,5&btnG=` 固定参数，绕过 403 反爬墙。
  - 底层扩展：SOURCES 新增 `query_param`（如 kiphub 用 `wd`）和 `extra_params` 字段，支持不同镜像的参数约定。
  - 优先级更新为 **kiphub → lanfanshu → scholar_pro → dotaindex → hk → google**。
  - 全部 Scholar 源失败时，提示中明确建议安装 Playwright 并启用 `--browser` 兜底。
- **实测**：kiphub `积雪草` 返回 10 条；scholar_pro 返回 9 条，含标题/作者/年份/摘要/被引；lanfanshu 固定参数后可正常访问。

### 📝 文档更新

- `references/scholar-sources.md`：扩展为 6 源技术参考（新增 kiphub/scholar_pro 解析器说明及字段映射）。
- `SKILL.md`：描述 / 触发词 / 用例 / 未找到提示全部更新为 6 源。
- `README.md`：更新项目简介，反映当前 6 源 Scholar 检索能力。

---

## [v1.1] — 2026-07-24

### 🐛 Bug Fixes

**#1 沙箱环境下 `unified_search.py` 被 SIGKILL（无任何输出）**

- **现象**：在某些受约束的沙箱环境（如 operitAI、WorkBuddy sandbox）中运行 `unified_search.py` 时，进程直接被杀死，不产生 stdout/stderr 任何输出。
- **根因**：旧版使用 `subprocess.run()` 串行执行 PubMed → Scholar。Scholar 需依次尝试 4 个源，每个源 HTTP 超时 25s，全程 2-3 分钟无任何 I/O。沙箱检测到进程长时间零输出后发送 SIGKILL，`print()` 永远走不到。
- **修复**：
  - 两路子进程改用 `concurrent.futures.ThreadPoolExecutor` 并行启动。
  - Scholar 设独立 60s 超时上限（≈ 走完 2-3 个源），超时直接出部分结果，不阻塞输出。
  - 所有 `print()` 后追加 `sys.stdout.flush()`，确保管道/沙箱立刻看到 I/O。
  - 即使 Scholar 超时，PubMed 结果仍正常合并输出。

**#2 operitAI 加载 skill 时三条启动报错**

- **现象**：在 operitAI（Android）加载本 skill 时，控制台出现三条错误：
  1. `tool_name must use packageName:toolName format`
  2. `Tool not found: unified-research-finder:unified_search`
  3. `Tool not found: unified-research-finder:terminal`
- **根因**：operitAI 自动扫描 `scripts/` 目录，试图把每个 `.py` 文件按 `{skill_name}:{script_basename}` 格式注册为工具。由于 SKILL.md 缺少显式 `tools` 声明，注册格式校验失败，后续工具查找全部落空。
- **修复**：在 SKILL.md frontmatter 中新增 `tools` 显式声明：
  ```yaml
  tools:
    - unified_search
    - pubmed_search
    - scholar_search
  ```
  > **微调（同日）**：初版 `tools` 声明带了 `.py` 后缀，operitAI 将其原样拼接为 `:unified_search.py` 导致一条残留报错。去掉后缀后彻底消除。

**#3 中国 Scholar 镜像站集体反爬/宕机，HTTP 方式无法获取结果**

- **现象**：2026-07-24 起，原四源全部不可达——dotaindex API 500、烂番薯 403、hk/google 超时。纯 HTTP（`urllib`）方式全面失效。
- **根因**：镜像站普遍升级反爬策略（CAPTCHA/验证码墙），dotaindex 后端宕机。
- **修复**：
  - 新增两个 Scholar 源：**KipHub学术**（`kiphub.com`）、**学术搜索Pro**（`googlescholar.pro`）。
  - 修复烂番薯：添加 `hl=zh-CN&as_sdt=0,5&btnG=` 固定参数绕过 403 反爬墙。
  - 新增 `query_param` / `extra_params` 源配置字段，支持不同镜像的 URL 参数约定（kiphub 用 `wd` 而非 `q`）。
  - 新增 `parse_kiphub_html()` / `parse_scholarpro_html()` 自定义 HTML 解析器。
  - 优先级更新为：kiphub → lanfanshu → scholar_pro → dotaindex → hk → google。
  - 全部失败时给出明确的 Playwright `--browser` 兜底建议。

### 📝 文档改进

- 更新 `references/scholar-sources.md`：六源技术细节（新增 kiphub/scholar_pro）。
- README.md 项目结构段落地道化。

---

## [v1.0] — 2026-07-22

### ✨ Initial Release

- **PubMed 子系统**：基于 NCBI E-utilities 官方 API（`esearch` + `efetch`），返回真实 PMID/摘要/DOI。
- **Scholar 多源回退**：覆盖灯塔（JSON API，最快最省内存）、烂番薯（HTML 服务端渲染）、Google Scholar 香港镜像、Google Scholar 官方站，按「灯塔 → 烂番薯 → 香港 → 官方」优先级自动回退。
- **双库合并去重**（`unified_search.py`）：同时检索 PubMed + Scholar，以 DOI 或归一化标题为键去重，默认开启。
- **纯标准库**：所有脚本仅用 Python 内置模块，无需 `pip install`，启动快、内存低。
- **开源投稿文件**：MIT-0 License、中英双语 README.md、`.gitignore`。
