#!/usr/bin/env python3
"""Resolve Z视介 channel/cid to live URL and print channel-aware Markdown."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys

BASE_URL = "https://zmtv.cztv.com/cmsh5-share/prod/cztv-tvLive/index.html?pageId={cid}"

CHANNEL_TO_CID = {
    "浙江卫视": "101",
    "钱江都市": "102",
    "经济生活": "103",
    "教科影视": "104",
    "民生休闲": "106",
    "新闻": "107",
    "少儿频道": "108",
    "浙江国际": "110",
    "好易购": "111",
    "之江纪录": "112",
}

CHANNEL_PROFILES = {
    "浙江卫视": {
        "summary": "中国蓝综合频道，主打头部综艺、晚会活动和热门事件直播。",
        "core": "综艺感强、节奏快，适合直接进直播追热点和看王牌内容。",
        "highlights": "大综艺热度高，逢大型晚会、特别节目和节点活动时更值得直接切入。",
        "programs": ["奔跑吧", "王牌对王牌", "中国蓝特别节目/晚会"],
    },
    "钱江都市": {
        "summary": "都市民生向频道，内容更贴近日常生活、消费服务和本地社会话题。",
        "core": "看城市生活、民生服务和都市资讯时，这个频道更对路。",
        "highlights": "本地生活感强，适合关注帮忙、调查、消费和身边新闻。",
        "programs": ["都市民生栏目", "消费服务内容", "本地新闻资讯"],
    },
    "经济生活": {
        "summary": "偏财经与生活服务的频道，关注消费、理财、行业和实用生活信息。",
        "core": "适合看经济观察、消费趋势和生活服务类内容。",
        "highlights": "信息密度高，适合想看实用资讯和经济生活话题的场景。",
        "programs": ["财经观察", "消费服务节目", "生活资讯内容"],
    },
    "教科影视": {
        "summary": "教育、人文和影视内容并重，兼顾知识性和陪伴式观看。",
        "core": "想看教育、人文专题或影视排播时，可以直接进这个频道。",
        "highlights": "内容相对稳，适合背景陪看，也适合找知识和故事感更强的内容。",
        "programs": ["教育专题", "人文纪实", "影视剧场"],
    },
    "民生休闲": {
        "summary": "聚焦本地民生与休闲生活，整体更轻松，也更贴近城市日常。",
        "core": "适合看本地生活、休闲资讯和民生类陪伴内容。",
        "highlights": "贴近日常，节奏相对轻，适合随手打开看实时节目。",
        "programs": ["民生资讯", "生活服务内容", "休闲陪伴节目"],
    },
    "新闻": {
        "summary": "以新闻和时政资讯为主，适合第一时间看重要消息和直播报道。",
        "core": "想直接跟进新闻现场、时政资讯和突发事件，这个频道最合适。",
        "highlights": "时效性最强，适合在重要节点直接进台获取连续信息流。",
        "programs": ["新闻直播", "时政报道", "深度新闻栏目"],
    },
    "少儿频道": {
        "summary": "面向亲子和少儿内容的频道，偏动画、成长陪伴和启蒙教育。",
        "core": "适合给孩子看动画、益智内容和亲子陪伴节目。",
        "highlights": "内容友好、节奏清晰，适合家庭场景直接打开。",
        "programs": ["动画节目", "益智启蒙内容", "亲子陪伴栏目"],
    },
    "浙江国际": {
        "summary": "偏国际传播与外向型内容，兼顾浙江窗口和对外表达。",
        "core": "适合看国际视角、外宣内容和面向海外受众的节目编排。",
        "highlights": "信息视角更外向，适合关注国际传播和城市形象表达。",
        "programs": ["国际传播内容", "外宣资讯节目", "浙江形象专题"],
    },
    "好易购": {
        "summary": "以电视购物和商品导购为核心，内容聚焦选品、介绍和下单转化。",
        "core": "如果你想看购物导购、商品讲解和促销直播，可以直接进这个频道。",
        "highlights": "导购导向明确，适合带着购买意图直接看。",
        "programs": ["商品导购", "购物直播", "促销讲解内容"],
    },
    "之江纪录": {
        "summary": "偏纪录片和人文纪实，适合看自然、历史、社会和文化故事。",
        "core": "想看更安静、更有信息量的纪实内容，这个频道更匹配。",
        "highlights": "适合沉浸式观看，内容质感和叙事性更强。",
        "programs": ["纪录片", "人文纪实", "自然历史专题"],
    },
}

ALIASES = {
    "浙江卫视": "浙江卫视",
    "浙江卫视频道": "浙江卫视",
    "浙江卫视直播": "浙江卫视",
    "浙江台": "浙江卫视",
    "跑男": "浙江卫视",
    "奔跑吧": "浙江卫视",
    "奔跑吧兄弟": "浙江卫视",
    "跑男直播": "浙江卫视",
    "奔跑吧直播": "浙江卫视",
    "卫视": "浙江卫视",
    "钱江都市": "钱江都市",
    "钱江都市频道": "钱江都市",
    "钱江都市直播": "钱江都市",
    "钱江": "钱江都市",
    "经济生活": "经济生活",
    "经济生活频道": "经济生活",
    "教科影视": "教科影视",
    "教科影视频道": "教科影视",
    "民生休闲": "民生休闲",
    "民生休闲频道": "民生休闲",
    "6频道": "民生休闲",
    "六频道": "民生休闲",
    "新闻": "新闻",
    "新闻频道": "新闻",
    "少儿频道": "少儿频道",
    "少儿直播": "少儿频道",
    "少儿": "少儿频道",
    "浙江国际": "浙江国际",
    "浙江国际频道": "浙江国际",
    "国际": "浙江国际",
    "好易购": "好易购",
    "之江纪录": "之江纪录",
    "之江纪录频道": "之江纪录",
    "纪录": "之江纪录",
}

CID_TO_CHANNEL = {cid:channel for channel, cid in CHANNEL_TO_CID.items()}
SUPPORTED_CIDS = tuple(sorted(CID_TO_CHANNEL.keys()))

ACTION_WORDS = (
    "打开",
    "进入",
    "播放",
    "收看",
    "观看",
    "看",
    "切到",
    "切换到",
    "我要",
    "请",
    "帮我",
)

NOISE_WORDS = (
    "直播间",
    "直播",
    "电视频道",
    "电视台",
    "频道",
    "在线",
)


def normalize(text: str) -> str:
    normalized = text.strip().replace("\u3000", " ").lower()
    normalized = re.sub(r"\s+", "", normalized)
    normalized = re.sub(r"[，,。.!?？:：;；\"'“”‘’【】\[\]\(\)（）\-_/|]+", "", normalized)
    for word in ACTION_WORDS:
        normalized = normalized.replace(word, "")
    for word in NOISE_WORDS:
        normalized = normalized.replace(word, "")
    return normalized


NORMALIZED_ALIAS_LOOKUP = {normalize(alias): channel for alias, channel in ALIASES.items()}


def resolve_by_channel(channel_input: str) -> tuple[str, str]:
    normalized_input = normalize(channel_input)
    channel = NORMALIZED_ALIAS_LOOKUP.get(normalized_input)
    if channel:
        return channel, CHANNEL_TO_CID[channel]

    # Fallback: user input may contain surrounding words, match by contained alias.
    for alias, mapped_channel in sorted(
        NORMALIZED_ALIAS_LOOKUP.items(), key=lambda item: len(item[0]), reverse=True
    ):
        if alias and alias in normalized_input:
            channel = mapped_channel
            break

    if not channel:
        supported = ", ".join(CHANNEL_TO_CID.keys())
        raise ValueError(f"Unknown channel '{channel_input}'. Supported channels: {supported}")
    return channel, CHANNEL_TO_CID[channel]


def resolve_by_cid(cid_input: str) -> tuple[str, str]:
    cid = cid_input.strip()
    if cid not in CID_TO_CHANNEL:
        supported = ", ".join(SUPPORTED_CIDS)
        raise ValueError(f"Unsupported cid '{cid_input}'. Supported cids: {supported}")
    return CID_TO_CHANNEL[cid], cid


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resolve Z视介 channel/cid to live URL.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--channel", help="Channel name, e.g. 浙江卫视")
    group.add_argument("--cid", help="Channel cid, e.g. 101")
    group.add_argument("--list", action="store_true", help="List supported channels and cids")
    parser.add_argument(
        "--open",
        dest="open_page",
        action="store_true",
        default=True,
        help="Open URL in default browser (default: true)",
    )
    parser.add_argument(
        "--no-open",
        dest="open_page",
        action="store_false",
        help="Do not open URL in browser",
    )
    parser.add_argument(
        "--url-only",
        action="store_true",
        help="Print URL only instead of Markdown",
    )
    parser.add_argument("--json", action="store_true", help="Print result in JSON format")
    return parser.parse_args()


def print_channels(json_mode: bool) -> None:
    items = [{"channel": channel, "cid": cid} for channel, cid in CHANNEL_TO_CID.items()]
    if json_mode:
        print(json.dumps({"channels": items}, ensure_ascii=False))
        return
    for item in items:
        print(f"{item['channel']}\t{item['cid']}")


def print_error(message: str, json_mode: bool) -> None:
    if json_mode:
        print(json.dumps({"error": message}, ensure_ascii=False), file=sys.stderr)
        return
    print(f"error={message}", file=sys.stderr)


def try_open_url(url: str) -> None:
    if sys.platform == "darwin":
        cmd = ["open", url]
    elif sys.platform.startswith("linux"):
        if not shutil.which("xdg-open"):
            return
        cmd = ["xdg-open", url]
    elif sys.platform.startswith("win"):
        cmd = ["cmd", "/c", "start", "", url]
    else:
        return

    try:
        subprocess.run(
            cmd,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5,
        )
    except Exception:
        return


def render_markdown(channel: str, url: str) -> str:
    profile = CHANNEL_PROFILES[channel]
    programs = "、".join(profile["programs"])
    return "\n".join(
        [
            f"## {channel}直播",
            "",
            profile["summary"],
            "",
            f"- 核心定位：{profile['core']}",
            f"- 看点：{profile['highlights']}",
            f"- 常见节目/内容：{programs}",
            "",
            f"[点击这里进入{channel}直播]({url})",
        ]
    )


def main() -> int:
    args = parse_args()

    if args.list:
        print_channels(args.json)
        return 0

    try:
        if args.channel:
            channel, cid = resolve_by_channel(args.channel)
        else:
            channel, cid = resolve_by_cid(args.cid or "")
    except ValueError as err:
        print_error(str(err), args.json)
        return 2

    url = BASE_URL.format(cid=cid)
    markdown = render_markdown(channel, url)
    result: dict[str, object] = {
        "channel": channel,
        "cid": cid,
        "url": url,
        "markdown": markdown,
    }

    if args.open_page:
        try_open_url(url)

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        if args.url_only:
            print(result["url"])
        else:
            print(result["markdown"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
