# OCR 模型文件

## 说明

本目录**不包含模型文件**。模型文件在首次运行时自动下载。

## 为什么模型文件不在此目录？

1. **文件较大**: 3 个模型文件共 ~13MB
2. **官方管理**: `rapidocr-onnxruntime` 包会自动下载和管理
3. **版本控制**: 避免大文件进入代码仓库
4. **自动更新**: 依赖包可以获取最新模型版本

## 模型文件信息

首次运行 `rapidocr_minimal.py` 时，会自动下载以下模型到**本地缓存目录**：

| 模型 | 大小 | 用途 |
|------|------|------|
| ch_PP-OCRv3_det_infer.onnx | 2.3 MB | 文字检测（Detection） |
| ch_PP-OCRv3_rec_infer.onnx | 10.2 MB | 文字识别（Recognition） |
| ch_ppocr_mobile_v2.0_cls_infer.onnx | 0.6 MB | 文字方向分类（Classification） |

**总计**: ~13 MB

## 模型存储位置

模型文件存储在用户目录的缓存文件夹，而非技能目录：

- **Windows**: `C:\Users\<用户名>\.rapidocr\`
- **Linux**: `~/.rapidocr/`
- **macOS**: `~/.rapidocr/`

## 模型来源

- **项目**: PaddleOCR (Baidu)
- **许可**: Apache 2.0
- **版本**: PP-OCRv3（轻量级中文版）
- **GitHub**: https://github.com/PaddlePaddle/PaddleOCR

## 如何预下载模型？

如果你需要在离线环境使用，可以：

1. 在有网络的环境运行一次技能
2. 模型会自动下载到本地缓存
3. 复制缓存目录到目标机器

或者：

```bash
# 手动预下载
python -c "from rapidocr_onnxruntime import RapidOCR; RapidOCR()"
```

---

**最后更新**: 2026-03-13  
**版本**: 1.3.0
