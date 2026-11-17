# templates/quad-exact —— 四刊合璧 1:1 全复刻构建模板（v2.14）

从 40 页真实交付（四本 NG 参照刊 × 每刊 10 页 → 《先发影响力》）直接参数化的可运行模板，
不是伪代码。整条管线：**选页配额 → 逐页建模 → 覆盖式替换 → 分级局部降级 → 零偏差验收 → PPTX → 细节体检**。

## 1. 文件

| 文件 | 作用 |
|---|---|
| `build.example.py` | 主构建脚本，五个 stage 全在，含自动回退与三报告输出 |
| `config.example.json` | 配置示例，复制成 `config.json` 改路径即可 |

## 2. 运行

```bash
cp -r templates/quad-exact/ <project>/scripts/
cp <project>/scripts/quad-exact/config.example.json <project>/scripts/quad-exact/config.json
# 改 config.json：journals / book_stream / 三个 marker / 两个 4K 池
python3 <project>/scripts/quad-exact/build.example.py --config <project>/scripts/quad-exact/config.json
```

也可用环境变量：`QUAD_CONFIG=/path/config.json python3 build.example.py`。

依赖：PyMuPDF、numpy、Pillow、python-pptx；`engine_dir` 需能 import 到
`exact_replication.build_page_models / verify`（技能不内附该引擎，从既有项目复用或自备同签名实现）。

## 3. 配置键

| 键 | 必须 | 说明 |
|---|---|---|
| `journals[]` | ✅ | `{label, path}`，数组顺序即轮转顺序 |
| `per_journal` | | 每刊取页数，默认 10；四刊 → 40 页 |
| `book_stream` | ✅ | 书稿纯文本（PDF 先抽文本，勿带页眉页脚） |
| `body_start_marker` / `body_end_marker` | 建议 | 正文起止锚点。**剥错会把版权页/电子书定价/献词当正文**（实战踩过） |
| `photo4k` / `fig4k` | ✅ | 4K 摄影池 / 4K 科研图池 |
| `engine_dir` | ✅ | `exact_replication.py` 所在目录 |
| `project_dir` | | 产出落到 `<project_dir>/delivery`、`assets` |
| `font_cjk` | | CJK 字体文件，默认 macOS STHeiti |
| `out_pdf` / `out_pptx` | | 输出名 |

## 4. 输出（`<project_dir>/delivery/`）

- `四刊版式全复刻_*.pdf` / `*.pptx`（40 页，宽高继承底版）
- `零偏差验收.json` + `零偏差验收_round1/2/3.json`（每轮回退可追溯）
- `全复刻构建报告.json`（`stats` / `page_modes` / `degraded_pages` / `content_audit` / `optimization[]` / `page_manifest`）
- 细节体检由 `scripts/detail_audit.py` 单独产出 `细节体检.json`（本模板不内联，避免双份口径）

## 5. 交付门槛

1. `verdict=PASS` 且 `worst_outside_change_ratio=0.0`，未改动页 100% 相同；
2. 40/40 页有改动、零回退页（靠分级降级，不靠整页放弃）；
3. `detail_audit.py` 八门 D1–D8 全 PASS；
4. PDF 页数与画布逐页等于底版；PPTX 零越界；
5. 三份报告口径一致（同一轮 `verify` + 同一轮 `detail_audit`）。

## 6. 已知边界（如实披露，勿掩盖）

- **含透明层的页面**插大图会引发 PyMuPDF 亚像素合成抖动 → 该页降为「仅中文、原刊图保留」，
  不整页回退（实战 P28/P32/P40）。
- **满版信息图的竖排标注**（bbox 宽 <10pt）横排中文落不进 → 按设计层不可变契约保护原刊图，
  该页无中文是正确结果而非缺陷。
- 覆盖色必须是**采样中位色精确值**；量化到 1/8 会产生肉眼可见色块（15.1% 槽位命中）。
- 文字色必须走 WCAG 相对亮度择优 + 纯黑兜底；二值阈值在中灰底会失读。

方法论与全部踩坑见 `references/exact-content-engineering.md`、`references/visual-detail-qa.md`。
