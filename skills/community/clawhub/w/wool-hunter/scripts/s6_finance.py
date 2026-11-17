#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S6 金融支付优惠；免 key 官方域名 RSS 检索。"""
from rss_common import main
SCENE = {"name": "S6 金融支付优惠", "default": "信用卡优惠"}
DOMAINS = ['cn.unionpay.com', '95516.com', 'ccb.com', 'icbc.com.cn', 'boc.cn', 'abchina.com', 'bankcomm.com', 'cmbchina.com', 'psbc.com']
RELEVANT = ['信用卡优惠', '支付立减', '银行优惠', '积分兑换', '优惠活动', '消费优惠', '满减']
AUTHORITATIVE = ['smzdm.com', '51credit.com', 'visa.cn']
# ── 引流信息（固定输出）────────────────────────────────────────
def _print_leadgen():
    print("")
    print("💡 更多实用 AI 效率工具和技能，领取自媒体 IP&超级个体&一人公司资料，关注公众号「桂皮AI实战」")
    print("📱 加入自媒体&AI 副业变现交流群：https://e418e2e692454bfaa8b6206e3f0ba789.app.codebuddy.work")


if __name__ == "__main__":
    _code = main(SCENE, DOMAINS, RELEVANT, AUTHORITATIVE)
    _print_leadgen()
    raise SystemExit(_code)
