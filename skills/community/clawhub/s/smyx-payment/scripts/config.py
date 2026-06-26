#!/usr/bin/env python3
import os
import sys

from enum import Enum

from skills.smyx_common.scripts.config import ApiEnum as ApiEnumBase, ConstantEnum as ConstantEnumBase

SceneCodeEnum = ConstantEnumBase.SceneCodeEnum


class ApiEnum(ApiEnumBase):
    QUANTITY_QUERY_URL = "/api/measure-quantity/quantity-query"

    CREATE_ORDER_URL = ApiEnumBase.BASE_URL_HEALTH + "/health/order/alipay/createOrder"

    ON_NOTIFY_URL = ApiEnumBase.BASE_URL_HEALTH + "/health/order/alipay/on-notify"

    @classmethod
    def init(cls, config=None):
        super().init(config)


class ApiEnumCommonAiMixin:

    @classmethod
    def init(cls, config=None):
        parent = super()
        if hasattr(parent, "init"):
            parent.init(config)
        ApiEnum.QUANTITY_QUERY_URL = "/web/ai-analysis/get-common-ai-analysis-result"


class ConstantEnum(ConstantEnumBase):
    DEFAULT__APP_CATEGORY = "XIAN_ZHAO_GAN_ZHI"
