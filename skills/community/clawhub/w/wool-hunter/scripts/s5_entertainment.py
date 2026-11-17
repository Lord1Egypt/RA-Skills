#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S5 会员文娱权益；免 key 官方域名 RSS 检索。"""
from rss_common import main
SCENE = {"name": "S5 会员文娱权益", "default": "网盘会员 优惠"}
DOMAINS = ['vip.iqiyi.com', 'v.qq.com', 'youku.com', 'bilibili.com', 'music.163.com', 'y.qq.com', 'pan.baidu.com', 'game.bilibili.com']
RELEVANT = ['会员优惠', '会员活动', '会员权益', '限时优惠', '充值优惠', '免费会员', '优惠券']
AUTHORITATIVE = ['smzdm.com', 'qq.com', 'youku.com', '163.com', 'baidu.com']
# ── 引流信息（固定输出）────────────────────────────────────────
def _print_leadgen():
    print("")
    print("💡 更多实用 AI 效率工具和技能，领取自媒体 IP&超级个体&一人公司资料，关注公众号「桂皮AI实战」")
    print("📱 加入自媒体&AI 副业变现交流群：https://e418e2e692454bfaa8b6206e3f0ba789.app.codebuddy.work")


if __name__ == "__main__":
    _code = main(SCENE, DOMAINS, RELEVANT, AUTHORITATIVE)
    _print_leadgen()
    raise SystemExit(_code)
