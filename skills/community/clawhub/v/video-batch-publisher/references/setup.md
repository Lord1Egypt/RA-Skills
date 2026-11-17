# 安装与首次登录指南

> 适用：拿到 `scripts/video_publisher/` 后，在 Windows 上配置并首次运行。

## 一、环境准备
1. 安装 Python 3.8+（推荐 3.10），勾选"Add to PATH"
2. 安装依赖：
   ```bash
   cd scripts/video_publisher
   pip install -r requirements.txt
   playwright install chromium
   ```

## 二、配置（首次必做）
1. 复制示例配置并改名：
   ```bash
   cp config.example.yaml config.yaml
   ```
2. 编辑 `config.yaml`：
   - `content_types` 是列表，每个类型一项。默认 `key: custom` 那一项：
     - `input_dir` → 你的视频根目录（放视频与封面子目录）
     - `excel_file` → 你的任务 Excel 绝对路径
     - `collection` → 发布时归入的合集名（留空=不指定合集）
     - `ai_label` → 是否勾选「AI生成内容」声明（抖音/视频号/快手/B站 按各自 UI 勾选；`true`=勾选，`false`=不勾选）。可按内容类型分别设置，关闭后发布不再勾选 AI 声明
   - 要新增内容类型：复制一个 `- key: ...` 块即可，无需改代码
   - `platforms` → 打开你要用的平台（true/false）
   - `excel.require_draft_finished` / `excel.require_video_finished` → 是否要求对应列标记 ✓ 才发布（通用用户设 `false`；接 自家流水线设 `true`）
   - `system.browser.debug_keep_browser` → 发布完成后是否保留浏览器进程（默认 `false` 自动关闭；排查问题时临时设 `true`）
3. 视频目录约定：每个视频一个子目录，内含 `xxx.mp4` 与封面 `0_cover_350.png`（横）/ `0_cover_300.png`（竖）

## 三、Excel 任务表结构（当前版本要求）
| 列名 | 含义 |
|------|------|
| 序号 | 视频序号 |
| 名称 | 视频名称（用于匹配文件） |
| 标题 | 发布标题 |
| 描述 | 发布文案 |
| 视频草稿 | **可选** 源就绪标记（仅当 `excel.require_draft_finished: true` 时作为发布前置条件） |
| 视频完成 | **可选** 视频就绪标记（仅当 `excel.require_video_finished: true` 时作为发布前置条件） |
| 发布日期 | `YYYY-MM-DD HH:MM`；未来=定时，过去/空=立即 |
| 抖音/视频号/快手/B站 | 各平台发布状态（空/□=待发，✓=已发） |

> ℹ️ `视频草稿`/`视频完成` 两列**现已可选**：默认（`config.example.yaml`）不要求这两列，纯本地用户可直接用；
> 若你接了 自家流水线，把 `excel.require_draft_finished` / `excel.require_video_finished` 改成 `true`，
> 即可恢复"双列 ✓ 才发布"的过滤（缺列时自动跳过，不会报错）。

## 四、首次登录
1. 运行 `python publisher_gui.py` 打开图形界面
2. 点"一键发布" → 工具为每个平台打开浏览器标签页
3. **首次需手动扫码/账号登录**（抖音/视频号等），登录态存入 `browser_cache`
4. 登录完成后关闭界面，之后运行会复用登录态，无需重复登录
5. 建议先拿 1–2 条视频试发，确认配置无误

## 五、命令行发布
```bash
python video_publisher.py ^
  --content-type custom ^
  --excel-path "你的视频列表.xlsx" ^
  --input-dir "视频根目录" ^
  --platforms "抖音,快手,B站"
```

## 六、常见问题
- **浏览器闪退/卡死**：发布中勿重复点击；UI 不实时响应属正常
- **授权/登录失效**：删除 `browser_cache` 重新登录
- **找不到视频文件**：检查 `input_dir` 与文件名命名规则（序号+名称）
- **某平台发布失败**：多为该平台 UI 改版，需跟进修复对应 `browser/{平台}_pub.py`
