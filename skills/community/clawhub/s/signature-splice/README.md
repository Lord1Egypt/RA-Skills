# signature-splice

> 把若干张**手写 / 电子签名图片**，经预处理（去背景、去截图边框、紧裁、透明化）后，
> **按指定顺序均匀**插入 PDF 的目标区域（报名表 / 承诺书 / 审批单 / 合同等），并在插入后**渲染自查**。

跨 Windows / Linux / macOS。依赖 `PyMuPDF`、`Pillow`、`numpy`、`scipy`。

## 它解决什么

表单常要多人手写签名。每人给的签名来源杂乱——白底照片、透明 PNG、"墨迹只在 alpha 通道"的 PNG、
甚至带灰框的截图——直接贴进 PDF 会**大小不一、带白块/灰框、位置对不齐、顺序错乱**。
本 skill 把这件事做成一条**可复现的流水线**：一切具体参数（PDF、签名图、顺序、目标区域、布局）
都由命令行传入，脚本内**零硬编码**。

## 工作流（固定 4 步）

```
① 采集规范命名 → ② preprocess（归一化）→ ③ locate + insert（定位 + 按序均匀）→ ④ render + verify（自查）
```

核心思想：**先把每张签名归一化成同一种干净形态**（透明底、紧裁到墨迹、纯黑），再排版；
这样不同来源的签名才能放进同一行而不突兀。

## 能力

| 能力 | 脚本 |
|------|------|
| 签名归一化（透明底·紧裁·纯黑；去截图边框、自适应阈值、去噪） | `scripts/preprocess_signatures.py` |
| 由锚点文本自动定位插入区域（合并矢量框 → 取含锚点行的最小框 → 其下方空白） | `scripts/locate_anchor.py` |
| 按顺序、均匀插入（等分网格 + 等比缩放；可选姓名标注 / 调试框） | `scripts/insert_signatures.py` |
| 渲染 PDF 供肉眼自查（支持 `--crop` 局部放大） | `scripts/render_pdf.py` |
| 校验签字版与原稿（页数 / 正文文本一致 / 嵌入图） | `scripts/verify_merge.py` |
| 生成签名预览拼图 | `scripts/contact_sheet.py` |
| 图像诊断（极性、截图边框线、包围盒） | `scripts/inspect_signatures.py` |

## 用法

```bash
SK="<skill>/scripts"

# ② 预处理 → 透明底·紧裁·纯黑
python "$SK/preprocess_signatures.py" --input raw_signatures/ --outdir clean/

# ③ 定位（可先确认区域）并按名单顺序插入
python "$SK/locate_anchor.py" --pdf form.pdf --anchor "（签名）" --no-frames
python "$SK/insert_signatures.py" --pdf form.pdf --input clean/ \
       --anchor "（签名）" --order "甲,乙,丙,丁" --out signed.pdf

# ④ 自查
python "$SK/render_pdf.py"   --pdf signed.pdf --outdir png/ --dpi 220 --crop 38,145,575,250
python "$SK/verify_merge.py" --original form.pdf --signed signed.pdf
```

- **顺序**：`--order "甲,乙,丙,丁"` 或 `--order-file names.txt`（按子串匹配文件名重排）。
- **区域**：`--anchor "（签名）"` 自动定位，或 `--box` / `--rect` 显式指定。
- **布局**：`--rows` / `--cols` / `--cell-fill`。
- 所有脚本 `argparse` 参数化、stdout 输出 JSON、支持多文件输入与显式输出路径。

## 设计原则

- **归一化优先**：先统一签名形态，再谈排版。
- **数据驱动定位**：不给表单写死坐标；由锚点文字 + 页面矢量框推导。
- **零硬编码**：路径 / 名单 / 坐标 / 阈值全部参数化，换机可移植。
- **先预演后执行**：变更类操作默认预演，`--apply` 才落盘；输出 stdout JSON。

## License

MIT
