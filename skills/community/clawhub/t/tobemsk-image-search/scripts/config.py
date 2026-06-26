import os
import sys

# 自动设置 HuggingFace 缓存目录
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ.setdefault('HF_HOME', os.path.join(os.path.expanduser('~'), '.cache', 'huggingface'))

# ==================== 扫描配置 ====================
# 使用说明：
# 1. config.py - 修改扫描目录和参数
# 2. scan.py   - 建库/更新索引（首次运行或新增图片后）
# 3. search.py - 搜索图片，例如: python search.py 猫

# 要扫描的根目录列表（会递归扫描所有子目录）
# 留空列表则自动检测所有可用盘
SCAN_ROOTS = []  # 自动检测所有盘（全盘扫描）

# 排除的目录（扫描时会跳过，减少无用图片）
EXCLUDE_DIRS = {
    "Windows", "Program Files", "Program Files (x86)", "ProgramData",
    "$RECYCLE.BIN", "System Volume Information", "node_modules",
    ".git", "AppData", ".cache", "OneDrive", "百度云", "微信备份",
}

# 排除的文件名包含这些关键词的
EXCLUDE_KEYWORDS = ["thumbs.db", ".ds_store", "desktop.ini", "node_modules"]

# ==================== 图片格式 ====================
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tiff', '.tif', '.heic', '.heif'}

# ==================== 模型配置 ====================
# 中文CLIP模型（支持中文搜索）
MODEL_NAME = "OFA-Sys/chinese-clip-vit-base-patch16"

# 批处理大小（CPU建议4-8，内存不足改为2或4）
BATCH_SIZE = 4

# ==================== 存储配置 ====================
# 使用脚本所在目录作为基准
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

DB_DIR = os.path.join(BASE_DIR, "image_db")
SCAN_LOG = os.path.join(DB_DIR, "scan_log.json")
INDEX_FILE = os.path.join(DB_DIR, "image.index")
IMAGE_LIST_FILE = os.path.join(DB_DIR, "image_list.pkl")
EMBEDDINGS_FILE = os.path.join(DB_DIR, "embeddings.npy")

# 确保数据库目录存在
os.makedirs(DB_DIR, exist_ok=True)