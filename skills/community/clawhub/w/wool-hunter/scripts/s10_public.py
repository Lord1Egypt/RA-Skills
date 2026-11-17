#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S10 政府公共 / 消费券补贴；免 key 官方域名 RSS 检索。"""
from rss_common import main
SCENE = {"name": "S10 政府公共 / 消费券补贴", "default": "消费券 以旧换新 国补 人才补贴 申领"}
DOMAINS = ['gov.cn', 'mofcom.gov.cn', 'ndrc.gov.cn', 'miit.gov.cn', 'beijing.gov.cn', 'shanghai.gov.cn', 'hangzhou.gov.cn', 'sz.gov.cn']
RELEVANT = ['消费券', '以旧换新', '国补', '补贴', '申领', '人才补助', '惠民']
AUTHORITATIVE = ['smzdm.com', 'bendibao.com']
# ── 引流信息（固定输出）────────────────────────────────────────
def _print_leadgen():
    print("")
    print("💡 更多实用 AI 效率工具和技能，领取自媒体 IP&超级个体&一人公司资料，关注公众号「桂皮AI实战」")
    print("📱 加入自媒体&AI 副业变现交流群：https://e418e2e692454bfaa8b6206e3f0ba789.app.codebuddy.work")


if __name__ == "__main__":
    _code = main(SCENE, DOMAINS, RELEVANT, AUTHORITATIVE)
    _print_leadgen()
    raise SystemExit(_code)
