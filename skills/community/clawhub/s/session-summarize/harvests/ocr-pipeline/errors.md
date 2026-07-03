# OCR-Pipeline 项目专属错误账本

> 文档转换管线：PDF扫描件 → OCR → AI结构化 → 知识库导入
> 创建于: 2026-06-28 | 涉及会话: sess_2f42a5c0

## 工具评测

### OCR引擎对比

| 工具 | 版本 | 中文质量 | 结论 |
|:---|:---|:---:|:---|
| **PaddleOCR** | **2.8.1** | ⭐⭐⭐⭐⭐ | **✅ 首选** |
| EasyOCR | latest | ⭐ | ❌ 中文乱码 |
| Tesseract | 5.x chi_sim | ⭐⭐ | ❌ 中文字间插空格 |
| MinerU | latest | — | ❌ 环境兼容性差 |

### PaddleOCR版本锁定

```
✅ PaddleOCR 2.8.1 + PaddlePaddle 2.6.2 + Python 3.12
❌ PaddleOCR 3.x     → OneDNN bug 崩溃
❌ PaddlePaddle 3.x  → OneDNN bug 崩溃  
❌ Python 3.14       → 无 PaddlePaddle wheel
```

### AI重构引擎对比

| 工具 | 效果 | 成本 | 结论 |
|:---|:---:|:---:|:---|
| **DeepSeek API** (deepseek-chat) | ⭐⭐⭐⭐⭐ | ¥0.06/12万字 | **✅ 首选** |
| 规则脚本 | ⭐⭐ | ¥0 | ❌ 无语义理解能力 |

### SiYuan导入API

| 端点 | 用途 | 坑点 |
|:---|:---|:---|
| `POST /api/filetree/createDocWithMd` | 创建文档 | `title`参数被`custom-sy-title-empty=true`覆盖→事后需`renameDoc` |
| `POST /api/filetree/removeDoc` | 删除文档 | 不清理`recent-doc.json`→需手动清缓存 |
| `POST /api/filetree/renameDoc` | 重命名 | 可用于修复"未命名文档" |

## 错误记录

| 错误类型 | 次数 | 分类 | 涉实体 | 避免规则 |
|---------|:---:|:--:|--------|---------|
| PaddleOCR版本选错 | 2 | ENVR | TOOL:PaddleOCR, SIG:OneDNN | 锁定2.8.1+2.6.2+py3.12 |
| Tesseract中文差 | 1 | KNOW | TOOL:Tesseract | 中文不用Tesseract |
| MinerU装不上 | 1 | ENVR | TOOL:MinerU, SIG:版本冲突 | 放弃，PaddleOCR够用 |
| createDocWithMd标题失效 | 3 | TOOL | TOOL:SiYuanAPI, FILE:.sy | 事后调renameDoc |
| removeDoc残留缓存 | 2 | TOOL | TOOL:SiYuanAPI, FILE:recent-doc.json | 手动清理状态文件 |
| API输出格式不一致 | 2 | TOOL | TOOL:DeepSeek | 处理时考虑`#`/`##`两种标题格式 |

## 完整管线

```
PDF(扫描件) 
  → PaddleOCR 2.8.1 (文本提取)
  → Python 章节按目录拆分
  → DeepSeek API 逐章AI重构(分段/层级/概念高亮/闪卡)
  → Python 组装结构化Markdown
  → SiYuan API createDocWithMd 导入
  → renameDoc 修复标题
  → 清理 recent-doc.json
```

## 下次复用命令

```bash
# OCR转换
/c/Python312/python.exe ocr_paddle_final.py \
  --input "输入.pdf" --output "输出.md"

# AI重构（改 CHAPTERS_DIR 即可复用）
/c/Python312/python.exe api_restructure_continue.py
```
