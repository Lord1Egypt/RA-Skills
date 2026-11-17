"""示例常量（复制到新 skill 时请替换为目标站点与业务字段）。"""

SKILL_SLUG = "example-real-browser-rpa"
LOG_LOGGER_NAME = "openclaw.skill.example_real_browser_rpa"

TARGET_PLATFORM = "target_platform"
LEASE_HOLDER = "example-real-browser-rpa"
LEASE_TTL_SEC = "1800"

DEFAULT_START_URL = "https://example.com"
DEFAULT_MAX_ITEMS = 100
DEFAULT_MAX_SCROLLS = 40
DEFAULT_NO_NEW_ROUNDS_LIMIT = 5
HUMAN_WAIT_TIMEOUT = 180

RESULT_END_TEXT = "没有更多结果了"

# 示例 selector — 复制到新 skill 时按目标站点 DOM 替换
SEARCH_INPUT_SELECTORS = (
    'input[type="search"]',
    'input[name="q"]',
    'input[placeholder*="搜索"]',
)
SEARCH_BUTTON_SELECTOR = 'button:has-text("搜索")'
RESULT_CONTAINER_SELECTOR = "#search-result-container"
RESULT_ITEM_SELECTOR = "[data-result-item]"
SCROLL_CONTAINER_SELECTORS = (
    "#search-result-container",
    ".search-result-scroll",
    ".route-scroll-container",
)
