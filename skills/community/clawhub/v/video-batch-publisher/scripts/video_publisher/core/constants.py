# ====================== 全局常量定义 ======================
# 修改这里即可全局生效，无需逐个文件修改

# ---------------------- Excel 列名常量 ----------------------
COL_SN = "序号"
COL_NAME = "名称"
COL_TITLE = "标题"
COL_DESCRIPTION = "描述"
COL_DRAFT_FINISHED = "视频草稿"      # 源/草稿就绪标记列（默认名，可在 config.yaml 覆盖为任意列名）
COL_VIDEO_FINISHED = "视频完成"      # 视频制作完成标记列（默认名，可在 config.yaml 覆盖）
COL_PUBLISH_DATE = "发布日期"
COL_NOTE = "备注"

# ---------------------- 平台相关常量 ----------------------
PLATFORM_LIST = ["快手", "视频号", "抖音", "B站"]

PLATFORM_DISPLAY_NAME = {
    "快手": "快手",
    "视频号": "视频号",
    "抖音": "抖音",
    "B站": "B站"
}

# ---------------------- 状态标识常量 ----------------------
STATUS_PENDING = "□"
STATUS_SUCCESS = "✓"
STATUS_FAILED = "❌"

# ---------------------- 日期格式常量 ----------------------
PUBLISH_TIME_FORMAT = "%Y-%m-%d %H:%M"

# ---------------------- 浏览器配置常量 ----------------------
BROWSER_PROFILE_DIR = "./browser_profile"

# ---------------------- Excel 必须存在的列 ----------------------
# 注意：视频草稿 / 视频完成 为「可选」列，仅当配置要求时才作为发布前置条件，
# 故不列入 REQUIRED_COLUMNS（列名可在 config.yaml 的 excel 段自定义，兼容任意叫法）
REQUIRED_COLUMNS = [
    COL_SN,
    COL_NAME,
    COL_PUBLISH_DATE,
] + PLATFORM_LIST

# ====================== 导出所有常量 ======================
__all__ = [
    'COL_SN', 'COL_NAME', 'COL_TITLE', 'COL_DESCRIPTION',
    'COL_DRAFT_FINISHED', 'COL_VIDEO_FINISHED',
    'COL_PUBLISH_DATE', 'COL_NOTE',
    'PLATFORM_LIST', 'PLATFORM_DISPLAY_NAME',
    'STATUS_PENDING', 'STATUS_SUCCESS', 'STATUS_FAILED',
    'PUBLISH_TIME_FORMAT', 'REQUIRED_COLUMNS',
    'BROWSER_PROFILE_DIR'
]
