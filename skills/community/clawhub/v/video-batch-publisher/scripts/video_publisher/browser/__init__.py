from .browser_singleton import (
    init_browser,
    get_page,
    get_platform_page,
    get_context,
    get_browser,
    new_page,
    close_browser,
    wait_for_element,
    wait_for_element_visible,
    wait_for_element_hidden,
    wait_for_navigation,
    select_option_by_text,
    handle_modal_dialog,
    take_screenshot,
    browser_singleton
)

from .douyin_pub import create_publisher as create_douyin_publisher
from .bilibili_pub import create_publisher as create_bilibili_publisher
from .kuaishou_pub import create_publisher as create_kuaishou_publisher
from .weixin_pub import create_publisher as create_weixin_publisher
from .xiaohongshu_pub import create_publisher as create_xiaohongshu_publisher

__all__ = [
    'init_browser',
    'get_page',
    'get_platform_page',
    'get_context',
    'get_browser',
    'new_page',
    'close_browser',
    'wait_for_element',
    'wait_for_element_visible',
    'wait_for_element_hidden',
    'wait_for_navigation',
    'select_option_by_text',
    'handle_modal_dialog',
    'take_screenshot',
    'browser_singleton',
    'create_douyin_publisher',
    'create_bilibili_publisher',
    'create_kuaishou_publisher',
    'create_weixin_publisher',
    'create_xiaohongshu_publisher'
]