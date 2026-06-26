# product-image-generator 配置文件

# ===== 默认 API：Nano Banana（备用方案）=====
NANO_BANANA_API_KEY = "sk-6fe41fd597614d2686f6d0685b4bd232"
NANO_BANANA_ENDPOINT = "https://grsai.dakka.com.cn"
NANO_BANANA_MODEL = "nano-banana-pro"
NANO_BANANA_TIMEOUT = 120  # 超时时间（秒）
NANO_BANANA_MAX_RETRIES = 3  # 最大重试次数

# ===== 备用 API：火山引擎即梦（需充值）=====
VOLCENGINE_API_KEY = "eaf6834a-9459-4e05-9512-9d317408df60"
VOLCENGINE_ENDPOINT = "https://ark.cn-beijing.volces.com/api/v3"
VOLCENGINE_MODEL = "doubao-seedream-5-0-260128"

# 默认使用 Nano Banana
DEFAULT_API = "nano-banana"  # 可选：nano-banana | volcengine

# 默认生成配置
DEFAULT_SIZE = "1024x1024"
DEFAULT_NUM_IMAGES = 1

# 图片输出目录
OUTPUT_DIR = "./output"

# 支持的尺寸
SUPPORTED_SIZES = [
    "1024x1024",  # 1K
    "2048x2048",  # 2K
    "1024x576",   # 16:9
    "576x1024",   # 9:16
    "768x1024",   # 3:4
    "1024x768",   # 4:3
]
