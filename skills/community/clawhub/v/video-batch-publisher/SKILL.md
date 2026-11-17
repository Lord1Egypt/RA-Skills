---
name: video-batch-publisher
display_name: 短视频多平台批量自动发布器
description: "一套本地运行的短视频批量发布工具，支持抖音/视频号/快手/B站多平台，从 Excel 读取任务，自动上传视频、填标题描述、设封面/合集/标签、按发布日期选择立即或定时发布。运行全程不修改你的 Excel，发布结果实时显示在界面与日志。当用户需要批量自动发视频、多平台一键发布、自媒体矩阵发布、把 video_publisher 打包成可交付产品时启用。"
---

# 短视频多平台批量自动发布器（免费上架，付费支持另议）

> 本 Skill 即产品本体。**安装后，按 `references/setup.md` 配置一次，即可用 GUI 或命令行批量发布。**

## 它解决什么
自媒体矩阵运营最耗时的环节是"把同一个视频挨个平台手动传、填、定时"。本工具把这一环自动化：
- 一个 Excel 管所有待发视频 + 各平台发布状态
- 一键批量上传到多个平台
- 自动填标题/描述/封面/合集/标签
- 按"发布日期"列自动判断**立即发布**或**定时发布**
- 运行全程**不修改你的 Excel**（发布结果实时显示在界面与运行日志，方便你手动记录或二次处理）

## 支持平台与能力
见 `references/capability-matrix.md`。一句话：**抖音/视频号/快手/B站** 四项已启用，
各平台均支持上传、封面、标题描述、合集、定时；B站/视频号额外支持草稿、标签。

## 技术形态
- **Playwright 浏览器自动化**（非平台开放 API，无需申请开发者资质）
- 首次运行在浏览器里**手动扫码/登录一次**，登录态保存在本地 `browser_cache`，后续复用
- Python 3.8+ + Tkinter GUI（Windows 原生），亦可用命令行 `video_publisher.py` 跑
- 纯本地运行，不上传任何数据

## 上手（简版，详见 setup.md）
```bash
cd scripts/video_publisher
pip install -r requirements.txt
playwright install chromium
cp config.example.yaml config.yaml   # 改 input_dir / excel_file 为你自己的路径
python publisher_gui.py              # 首次登录各平台，之后点"一键发布"
```

## 本 Skill 被 AI 调用时如何工作
安装本 Skill 后，AI 应按以下方式帮助用户使用工具（工具本体是本地 Python 程序，AI 不直接"代发"，而是引导用户跑程序）：

1. **首次部署**：读取 `references/setup.md`，指导用户 `pip install -r requirements.txt` → `playwright install chromium` → `cp config.example.yaml config.yaml` 并改路径。
2. **配置 Excel**：按 setup.md 的表结构准备好任务表（含 序号/名称/标题/描述/视频草稿/视频完成/发布日期/各平台 列）。
3. **启动发布**：让用户运行 `python publisher_gui.py`（图形界面一键发布）或 `python video_publisher.py --content-type custom --excel-path ... --input-dir ... --platforms "抖音,快手,B站"`。
4. **首次登录**：提示用户首次需在弹出的浏览器标签页手动扫码/登录各平台，登录态会存入 `browser_cache` 复用。
5. **排障**：发布失败先看 `logs/`，多为平台 UI 改版导致对应 `browser/{平台}_pub.py` 需更新；找不到视频检查 `input_dir` 与命名。

> 注意：AI 不能直接替用户登录或绕过平台风控；自动化发布有封号风险，须提示用户小批量、模拟人工节奏。

## 重要边界（务必读）
1. **浏览器自动化 ≠ 官方 API**：平台改版（UI/选择器变动）可能导致某平台失效，需跟进修复。
2. **账号风险**：用自动化发布违反部分平台 ToS（尤其 B站/视频号），有封号可能；建议小批量、模拟人工节奏。
3. **Excel 列结构有约定**：当前要求含 `序号/名称/标题/描述/视频草稿/视频完成/发布日期/各平台` 列（详见 setup.md）。
4. **B站批量修复待实机验证**：第 2 个视频起的过渡态修复已写代码，但需真实登录环境跑一遍确认。

## 授权与付费（详情见 evaluation.md）
- 当前上架版：**免费使用**，完整功能（抖音/视频号/快手/B站 4 平台）直接可用
- 商业授权 / 优先支持 / 定制开发：价格另议，联系作者
- 定制服务（站外）：新增平台 / 改造 Excel 结构 / 一对一部署

## 参考资料
- `references/evaluation.md` — 上架就绪度评估 + 必须修复项 + 定价模型
- `references/capability-matrix.md` — 各平台能力明细
- `references/packaging-plan.md` — 实际上架步骤 + 店铺文案
- `references/setup.md` — 安装与首次登录
- 商业授权 / 付费支持：另议（联系作者）
