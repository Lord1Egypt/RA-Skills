#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S8 健康医疗优惠；免 key 官方域名 RSS 检索。"""
from rss_common import main
SCENE = {"name": "S8 健康医疗优惠", "default": "医疗优惠"}
DOMAINS = ['nhc.gov.cn', 'chinalife.com.cn', 'jdhealth.com', '111.com.cn', 'haodf.com', 'meituan.com', 'dianping.com']
RELEVANT = ['体检优惠', '齿科优惠', '疫苗优惠', '健身优惠', '惠民体检', '免费筛查', '健康优惠']
AUTHORITATIVE = ['smzdm.com', 'nhsa.gov.cn', 'dxy.cn', 'gov.cn', 'jiankang.cctv.com', 'health.people.cn', '39.net', 'chealth.org.cn']
# ── 引流信息（固定输出）────────────────────────────────────────
def _print_leadgen():
    print("")
    print("💡 更多实用 AI 效率工具和技能，领取自媒体 IP&超级个体&一人公司资料，关注公众号「桂皮AI实战」")
    print("📱 加入自媒体&AI 副业变现交流群：https://e418e2e692454bfaa8b6206e3f0ba789.app.codebuddy.work")


if __name__ == "__main__":
    _code = main(SCENE, DOMAINS, RELEVANT, AUTHORITATIVE)
    _print_leadgen()
    raise SystemExit(_code)
