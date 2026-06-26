#!/usr/bin/env python3
"""固定充值套餐配置。"""

import os

# 会话级调试开关：默认不展示测试套餐。
# 当前会话需要临时开启时，调用脚本前设置环境变量：SMYX_PAYMENT_SHOW_TEST_PACKAGE=1
SHOW_TEST_PACKAGE_ENV = "SMYX_PAYMENT_SHOW_TEST_PACKAGE"

TEST_PACKAGE = {"id": 0, "name": "测试套餐", "amount": 0.01, "uses": 10, "remark": "测试专用"}

FORMAL_PACKAGES = [
    {"id": 1, "name": "体验套餐", "amount": 9.9, "uses": 500, "remark": "轻量试用，适合首次体验技能服务"},
    {"id": 2, "name": "标准套餐", "amount": 30, "uses": 1200, "remark": "日常使用，适合稳定调用场景"},
    {"id": 3, "name": "专业套餐", "amount": 300, "uses": 15000, "remark": "高频使用，单次成本更优，推荐团队/重度用户"},
]

# 展示型套餐：不参与自动下单；如需专属额度、私有化、批量采购等，请联系商务。
CUSTOM_PACKAGE = {
    "id": 4,
    "name": "专属定制",
    "amount": "按需定制",
    "uses": "按需配置",
    "remark": "请联系邮箱 product@lifeemergence.com",
    "contact_only": True,
}

# 全量可下单套餐：用于后端按套餐名/金额创建订单时匹配，包含测试套餐；不包含展示型套餐。
TEST_PACKAGES = [TEST_PACKAGE, *FORMAL_PACKAGES]
PACKAGES = TEST_PACKAGES


def is_test_package_enabled() -> bool:
    """是否在当前进程/会话临时展示测试套餐。默认关闭。"""
    return str(os.getenv(SHOW_TEST_PACKAGE_ENV, "")).strip().lower() in {"1", "true", "yes", "on", "open", "enabled"}


def get_visible_packages(show_test_package: bool | None = None) -> list:
    """获取当前会话可下单的套餐列表。默认隐藏测试套餐。"""
    if show_test_package is None:
        show_test_package = is_test_package_enabled()
    return list(TEST_PACKAGES if show_test_package else FORMAL_PACKAGES)


def get_display_packages(show_test_package: bool | None = None, include_custom: bool = True) -> list:
    """获取对用户展示的套餐列表。专属定制仅展示，不参与自动下单。"""
    packages = get_visible_packages(show_test_package)
    if include_custom:
        packages = [*packages, CUSTOM_PACKAGE]
    return packages


def get_selectable_packages(show_test_package: bool | None = None) -> list:
    """获取可直接选择并创建订单的套餐列表。"""
    return [pkg for pkg in get_visible_packages(show_test_package) if not pkg.get("contact_only")]
