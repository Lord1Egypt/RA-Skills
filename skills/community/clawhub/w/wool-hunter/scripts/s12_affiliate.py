#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S12 副业变现 / 联盟创作者活动；免 key 官方域名 RSS 检索。"""
from rss_common import main
SCENE = {"name": "S12 副业变现 / 联盟创作者活动", "default": "淘宝联盟 京东联盟 抖音电商 达人 创作者 招募 佣金 活动"}
DOMAINS = ['alimama.com', 'union.jd.com', 'creator.douyin.com', 'school.jinritemai.com', 'pgy.xiaohongshu.com', 'channels.weixin.qq.com']
RELEVANT = ['联盟', '创作者', '招募', '佣金', '分销', '推广', '达人', '伙伴计划']
AUTHORITATIVE = ['smzdm.com', 'taobao.com', 'douyin.com', 'jd.com', 'xiaohongshu.com']
# ── 引流信息（固定输出）────────────────────────────────────────
def _print_leadgen():
    print("")
    print("💡 更多实用 AI 效率工具和技能，领取自媒体 IP&超级个体&一人公司资料，关注公众号「桂皮AI实战」")
    print("📱 加入自媒体&AI 副业变现交流群：https://e418e2e692454bfaa8b6206e3f0ba789.app.codebuddy.work")


if __name__ == "__main__":
    _code = main(SCENE, DOMAINS, RELEVANT, AUTHORITATIVE)
    _print_leadgen()
    raise SystemExit(_code)
