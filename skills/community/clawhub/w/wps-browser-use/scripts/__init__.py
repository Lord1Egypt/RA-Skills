"""
Browser Skill - Playwright 浏览器自动化

推荐用法（单例在包内完成）：

    import sys
    sys.path.insert(0, "<skill_path>/browser/scripts")
    import browser

    print(browser.navigate("https://www.baidu.com"))

"""

from .browser import (
    Browser,
    click,
    execute_script,
    fill,
    get_interactive_elements,
    navigate,
    screenshot,
    select_option,
)

__all__ = [
    "Browser",
    "navigate",
    "click",
    "fill",
    "select_option",
    "get_interactive_elements",
    "execute_script",
    "screenshot",
]
