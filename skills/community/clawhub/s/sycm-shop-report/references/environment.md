> **适用范围**：本技能仅服务中国大陆天猫 / 淘宝商家，数据源限定生意参谋 MCP。
> **默认中文输出与 Asia/Shanghai 时区**是这一垂直领域的合理默认（生意参谋字段、千牛入口、类目命名都是中文语境），**不是策略强加**——若你的团队需要英文或别的时区，请自行改 SKILL.md 里字体、cron `tz` 与 narrative 文案。

# 环境依赖自检与安装

开工前按此清单自检；缺什么装什么。

## 1. Node.js + docx
```bash
node -v                                   # 需要 Node 18+
node -e "require.resolve('docx')"         # 不报错即已装
```
缺失时全局安装：`npm i -g docx`（技能脚本用 docx@9.x）。
运行 docx 脚本要能让 Node 找到全局包：
```bash
# Windows（全局包通常在 %APPDATA%\npm\node_modules）
NODE_PATH="%APPDATA%\npm\node_modules" node scripts/build_daily_report.js
# macOS / Linux
NODE_PATH="$(npm root -g)" node scripts/build_daily_report.js
```
先 `npm root -g` 确认全局 node_modules 路径，再把它赋给 `NODE_PATH`。

## 2. Python + matplotlib
```bash
python -c "import matplotlib; print(matplotlib.__version__)"   # 需要 3.7+
```
缺失时：`pip install matplotlib`。

### 中文字体（关键，否则图表中文变方框）
脚本默认 `Microsoft YaHei`（Windows 自带）。查可用中文字体：
```bash
python -c "import matplotlib.font_manager as fm; print(sorted({f.name for f in fm.fontManager.ttflist if any(k in f.name for k in ['Hei','YaHei','SimHei','Song','Noto Sans CJK','Source Han','PingFang','WenQuanYi'])}))"
```
- Windows：`Microsoft YaHei` / `SimHei`
- macOS：`PingFang SC` / `Heiti SC`
- Linux：`Noto Sans CJK SC` / `WenQuanYi Zen Hei`（无则 `apt install fonts-noto-cjk`）
把选定的字体名写进 JSON 的 `font` 字段即可，脚本会读它。

## 3. 生意参谋 MCP
确认 `taobao-open-platform` MCP 已连接（能列出 `mcp__taobao-open-platform__openAtpSycm*` 工具）。未连接时提示用户在千问办公里启用淘宝/生意参谋连接器，本技能无法取数。

## 4. 校验工具（可选但推荐）
OOXML 校验脚本随 `docx` 技能提供：
```bash
PYTHONUTF8=1 python "<skills>/docx/toolkit/ooxml/audit.py" 输出.docx
```
Windows 上 Python 默认 GBK，务必加 `PYTHONUTF8=1`，否则中文 XML 会报 codec 错。
本机若无 LibreOffice，就不做逐页渲染，改为：audit 通过 + 解压 docx 后 grep 关键数字逐项复核。

## 5. 输出目录
JSON 里 `output_dir` 必须是可写目录。图表输出到 `output_dir/charts_subdir`。路径用正斜杠 `/` 或转义反斜杠 `\\`。

## 常见坑
- `Cannot find module 'docx'` → 没设 `NODE_PATH`，见上。
- 图表中文方框 → `font` 字段填了系统没有的字体，换成上面查到的可用字体。
- `audit.py` 报 `'gbk' codec can't decode` → 没加 `PYTHONUTF8=1`。
- Git Bash 的 `/tmp` 与 Python 路径不一致 → 测试时用系统原生临时目录的绝对路径。
