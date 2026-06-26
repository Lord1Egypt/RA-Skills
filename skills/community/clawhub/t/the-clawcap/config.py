"""
全局配置模块
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- Gemini API ---
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

# 模型选择 (Gemini 3.1 系列，2026年3月最新)
VLM_MODEL: str = "gemini-3.1-pro-preview"                 # 阶段一：视觉指纹提取（纯文本分析）
IMAGEN_MODEL: str = "gemini-3.1-flash-image-preview"       # 阶段三：图像编辑 (Nano Banana 2)

# --- 图像处理 ---
MIN_IMAGE_SIZE: int = 256       # 最小输入分辨率 (px)
MAX_IMAGE_SIZE: int = 2048      # 最大输入分辨率 (px)
OUTPUT_SIZE: int = 1024         # 默认输出分辨率 (px)

# --- 系统限制 ---
API_TIMEOUT_MS: int = 25000     # 全流程超时阈值 (ms)
MAX_RETRIES: int = 2            # 生图重试次数

# --- Mask 生成参数 ---
MASK_EXPAND_RATIO: float = 0.35   # Mask 向头顶上方延展的比例 (相对于头部高度)
MASK_FEATHER_PX: int = 12         # Mask 边缘羽化像素数
