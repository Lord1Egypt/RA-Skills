# 短视频多平台批量自动发布器（使用说明）

> 本说明对应实际代码（Playwright 浏览器自动化方案）。

## 一、工具简介
本地运行的短视频批量发布工具，支持 **抖音 / 视频号 / 快手 / B站**，从 Excel 读取发布任务，
自动上传视频、填标题描述、设封面/合集/标签，并按"发布日期"列自动选择**立即发布**或**定时发布**，

## 二、文件结构
```
video_publisher/
├─ video_publisher.py     # 命令行编排入口（读 Excel → 逐平台发布）
├─ publisher_gui.py       # Tkinter 图形界面（一键发布 / 查看状态）
├─ config.example.yaml    # 配置示例（复制为 config.yaml 后填写）
├─ run.bat               # Windows 一键启动（需改 Python 路径）
├─ requirements.txt      # 依赖
├─ core/                 # 配置/Excel/日志/常量
├─ browser/              # 各平台发布器 + 浏览器单例
└─ 各平台发布界面/        # 各平台发布页 UI 参考
```

## 三、前置准备
1. Python 3.8+（推荐 3.10），加入 PATH
2. 安装依赖：`pip install -r requirements.txt`
3. 安装浏览器：`playwright install chromium`

## 四、配置（必做）
```bash
cp config.example.yaml config.yaml
```
编辑 `config.yaml`：
- `content_types`：列表，每项一个类型。默认 `key: custom` 项的 `input_dir`=视频根目录、`excel_file`=任务 Excel 路径、`collection`=合集名（留空=不指定）
- 新增类型：复制一个 `- key: ...` 块，无需改代码
- `platforms`：开启要用的平台（true/false）

视频目录约定：每个视频一个子目录，内含 `xxx.mp4` 与封面 `0_cover_350.png`（横）/ `0_cover_300.png`（竖）。

## 五、Excel 任务表结构
| 列名 | 含义 |
|------|------|
| 序号 | 视频序号 |
| 名称 | 视频名称（用于匹配文件） |
| 标题 | 发布标题 |
| 描述 | 发布文案 |
| 视频草稿 | 源就绪标记（✓ 才参与发布） |
| 视频完成 | 视频就绪标记（✓ 才参与发布） |
| 发布日期 | `YYYY-MM-DD HH:MM`；未来=定时，过去/空=立即 |
| 抖音/视频号/快手/B站 | 各平台状态（空/□=待发，✓=已发） |

## 六、首次登录
运行 `python publisher_gui.py`，首次各平台会在浏览器标签页要求**手动扫码/登录一次**，
登录态存入 `browser_cache`，后续复用，无需重复登录。建议先拿 1–2 条试发。

## 七、命令行发布
```bash
python video_publisher.py --content-type custom ^
  --excel-path "视频列表.xlsx" --input-dir "视频根目录" ^
  --platforms "抖音,快手,B站"
```

## 八、常见问题
- **浏览器卡死**：发布中勿重复点击；UI 不实时响应属正常
- **登录失效**：删除 `browser_cache` 重新登录
- **找不到视频**：检查 `input_dir` 与文件命名（序号+名称）
- **某平台失败**：多为该平台 UI 改版，需跟进修复对应 `browser/{平台}_pub.py`

## 九、注意事项
1. 纯本地运行，不上传任何数据
2. 发布前先试发 1–2 条确认配置
3. 浏览器自动化发布可能触发平台风控，建议小批量、模拟人工节奏
4. 平台 UI 改版可能导致某平台失效，需维护更新
