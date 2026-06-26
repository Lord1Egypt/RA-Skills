#!/usr/bin/env python3

import os
import sys
from datetime import datetime

from .config import ApiEnum, ConstantEnum
from skills.smyx_common.scripts.api_service import ApiService as ApiServiceBase
from skills.smyx_common.scripts import DatetimeUtil


class ApiService(ApiServiceBase):

    def __init__(self):
        super().__init__()

    def on_pay_notify(self, *args, **argss):
        # params = argss.setdefault("params", {})
        # scene_code and params.setdefault("sceneCode", scene_code)
        data = (args[0] if len(args) > 0 else None) or {}
        user_id = data.get("userId")
        total_amount = float(data.get("total_amount"))
        data.update({
            # "account": phone_number,
            "total_amount": total_amount,
            "userId": f"SKILL-USER:{user_id}",
            "sceneCode": "ALL-SKILL",
            "bizTag": str(datetime.now().year)
        })

        result = self.http_post(ApiEnum.ON_NOTIFY_URL, *args, **argss)

        return result

    def quantity_query(self, *args, **argss):
        data = (args[0] if len(args) > 0 else None) or {}
        user_id = data.get("userId")
        new_user = self.get_user_by_username(user_id)
        new_user_id = new_user.username if new_user else user_id
        data.update({
            # "account": phone_number,
            "userId": f"SKILL-USER:{new_user_id}",
            "sceneCode": "ALL-SKILL",
            "bizTag": str(datetime.now().year)
        })

        result = self.http_post(ApiEnum.QUANTITY_QUERY_URL, *args, **argss)

        # 解析返回结果（根据实际 API 调整）
        if result:
            account_info = {
                "phoneNumber": new_user_id,
                "totalRecharged": result.get("totalQuantity", 0),
                "balance": result.get("balance", 0),
                "remainingUses": result.get("remainingUses", 0),
                "usedCount": result.get("usedQuantity", 0),
                "isInsufficient": result.get("isInsufficient", False)
            }
            account_info["remainingUses"] = account_info["balance"] = account_info["totalRecharged"] - account_info[
                "usedCount"] if account_info[
                                    "totalRecharged"] > \
                                account_info[
                                    "usedCount"] else 0
            account_info["isInsufficient"] = account_info["remainingUses"] <= 0
        else:
            account_info = None

        return account_info

    def create_order(self, *args, **argss):
        # params = argss.setdefault("params", {})
        # scene_code and params.setdefault("sceneCode", scene_code)
        data = (args[0] if len(args) > 0 else None) or {}
        # user_id = data.get("userId")

        # promotion_id = "open_claw_promotion_" + data["promotionId"]
        amount = int(float(data.get("amount")) * 100)
        open_id = data.get("openId")
        new_user = self.get_user_by_username(open_id)
        new_open_id = new_user.username if new_user else open_id

        data.update({
            "amount": amount,
            "memberType": 1,
            "openId": new_open_id
        })

        # ✅ 修复：传递更新后的 data，而不是原始 args
        result = self.http_post(ApiEnum.CREATE_ORDER_URL, data)

        return result

    def notify_order(self, *args, **argss):
        # params = argss.setdefault("params", {})
        # scene_code and params.setdefault("sceneCode", scene_code)
        data = (args[0] if len(args) > 0 else None) or {}
        # user_id = data.get("userId")

        # promotion_id = "open_claw_promotion_" + data["promotionId"]
        # amount = int(float(data.get("amount")) * 100)
        data.update({
            "trade_status": "TRADE_SUCCESS",
            # "out_trade_no": "HY26043015320751568234",
            "trade_no": DatetimeUtil.now_str(),
            "total_amount": data.get("amount")
        })

        # ✅ 修复：传递更新后的 data，而不是原始 args
        result = self.http_post(ApiEnum.ON_NOTIFY_URL, *args, **argss)

        return result
