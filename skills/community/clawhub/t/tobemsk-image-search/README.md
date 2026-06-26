# image-search

本地图片语义搜索工具 - 基于 CLIP 模型实现中英文图片内容的语义理解检索，类似小米相册 AI 搜索。

## 功能特性

- 🔍 **语义搜索**：用自然语言搜索图片，支持中英文关键词
- 🇨🇳 **中文支持**：基于 Chinese-CLIP 模型，精准理解中文语义
- 🔄 **增量更新**：新增图片后只需更新新图片，无需全量重建
- 💾 **本地存储**：所有数据存储在本地，保护隐私
- 🖥️ **老硬件友好**：支持 CPU 运行，8GB+ 内存即可

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

> 首次运行会自动下载 CLIP 模型（约 400MB）

### 2. 首次建库（约 2 小时）

```bash
python scripts/scan.py
```

扫描 C:\ D:\ E:\ F:\ 四个盘符，提取所有图片特征建立索引。

### 3. 搜索图片

```bash
python scripts/search.py 塔
python scripts/search.py "日落海滩"
```

搜索结果自动保存到桌面。

### 4. 增量更新（后续使用）

```bash
python scripts/update.py
```

自动扫描新增图片，只处理新图片，快速完成。

## 使用 Windows 快捷方式

双击 `启动.bat`，按菜单操作即可。

## 项目结构

```
image-search/
├── SKILL.md              # 技能说明
├── requirements.txt      # Python 依赖
├── 启动.bat              # Windows 快捷启动
└── scripts/
    ├── config.py         # 配置文件
    ├── scan.py           # 全量建库
    ├── update.py         # 增量更新
    └── search.py         # 搜索图片
```

## 配置说明

编辑 `scripts/config.py` 自定义扫描行为：

```python
# 扫描的根目录，留空则自动检测所有盘
SCAN_ROOTS = []

# 排除的目录
EXCLUDE_DIRS = {"Windows", "Program Files", "$RECYCLE.BIN", ...}

# 批处理大小，内存不足可调小
BATCH_SIZE = 4
```

## 系统要求

- **系统**: Windows 10/11
- **Python**: 3.8+
- **内存**: 建议 8GB 以上
- **存储**: 需要约 1GB 空间存储索引

## 技术原理

1. **特征提取**：使用 `OFA-Sys/chinese-clip-vit-base-patch16` 模型将图片转换为 512 维向量
2. **向量存储**：使用 FAISS 向量数据库存储和检索
3. **语义搜索**：将搜索词转换为向量，在向量空间中找最相似的图片

## 常见问题

**Q: 内存不足？**  
A: 减小 `config.py` 中的 `BATCH_SIZE`（如改为 2）

**Q: 模型下载失败？**  
A: 脚本已自动设置镜像源 `hf-mirror.com`，确保网络畅通

**Q: 想重建索引？**  
A: 删除 `image_db/` 目录，重新运行 `scan.py`

## License

MIT