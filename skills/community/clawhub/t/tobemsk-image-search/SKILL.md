---
name: image-search
description: 本地图片语义搜索工具，基于 CLIP 模型实现中英文图片内容的语义理解检索，类似小米相册 AI 搜索功能。使用场景：(1) 用户想用自然语言搜索本地图片 (2) 用户需要搜索中文关键词相关的图片 (3) 用户提到"搜图片"、"找图片"、"图片搜索"、"AI相册"等关键词
---

# 本地图片语义搜索工具

基于 CLIP 模型的全盘中英文图片语义搜索工具，支持中文关键词检索。

## 项目结构

```
image-search/
├── SKILL.md              # 本说明文件
├── requirements.txt      # Python 依赖
└── scripts/
    ├── scan.py           # 首次全量建库（约2小时）
    ├── update.py         # 增量更新（只处理新增图片）
    ├── search.py         # 搜索图片
    └── config.py         # 配置文件
```

## 快速开始

### 第一步：安装依赖

```bash
pip install -r requirements.txt
```

**注意**：首次运行会**自动下载 CLIP 模型**（约 400MB），请确保网络畅通。模型会缓存到 `~/.cache/huggingface/`。

### 第二步：首次建库（只需一次）

```bash
python scripts/scan.py
```

- 扫描 C:\ D:\ E:\ F:\ 四个盘符的所有图片
- 提取图片特征并建立向量索引
- **耗时约 2 小时**（取决于图片数量）
- 完成后索引保存在 `image_db/` 目录

### 第三步：搜索图片

```bash
python scripts/search.py 关键词
```

支持中英文关键词，例如：
```bash
python scripts/search.py 塔
python scripts/search.py 猫
python scripts/search.py sunset
python scripts/search.py 建筑 红色
```

搜索结果保存到桌面 `搜索结果_关键词.txt`，包含图片路径和相似度分数。

### 增量更新（后续使用）

每次新增图片后，运行增量更新：

```bash
python scripts/update.py
```

- 自动扫描四个盘符
- 找出新增图片（不在索引中的）
- **只对新图片提取特征**，几分钟完成
- 追加到现有索引

## 工作原理

1. **特征提取**：使用 `OFA-Sys/chinese-clip-vit-base-patch16` 模型将图片转换为 512 维向量
2. **向量存储**：使用 FAISS 向量数据库存储和检索
3. **语义搜索**：将搜索词转换为向量，在向量空间中找最相似的图片

## 配置修改

编辑 `scripts/config.py`：

```python
SCAN_ROOTS = ["C:\\", "D:\\", "E:\\", "F:\\"]  # 扫描的根目录
EXCLUDE_DIRS = ["$RECYCLE.BIN", "System Volume Information", ".cache"]  # 排除的目录
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}  # 支持的图片格式
MODEL_NAME = "OFA-Sys/chinese-clip-vit-base-patch16"  # CLIP 模型
BATCH_SIZE = 16  # 批处理大小，内存不足可调小
```

## 硬件要求

- **CPU**: i5-4590（已验证可用）
- **内存**: 建议 8GB 以上
- **显卡**: 可用 GPU 加速（如 GTX 750 Ti），不用也能跑
- **硬盘**: 需要约 1GB 空间存储索引

## 常见问题

**Q: 内存不足怎么办？**
A: 减小 `config.py` 中的 `BATCH_SIZE`（如改为 4 或 8）

**Q: 模型下载失败？**
A: 国内网络可能需要设置镜像源：
```bash
set HF_ENDPOINT=https://hf-mirror.com
```

**Q: 如何完全重建索引？**
A: 删除 `image_db/` 目录，然后重新运行 `scan.py`