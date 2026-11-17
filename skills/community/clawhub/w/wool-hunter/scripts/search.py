# /// script
# requires-python = ">=3.11"
# dependencies = ["aiohttp", "argparse"]
# ///
"""
全网优惠券搜索 — 通过扣子 Bot 聚合淘宝/京东/拼多多/抖音/快手/1688/苏宁/唯品会等主流电商平台优惠券。
"""
import os
import json
import sys
import asyncio
import argparse
import aiohttp

CONFIG_PATH = os.path.expanduser("~/.coupon_search_config.json")


def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"❌ 配置文件不存在: {CONFIG_PATH}", file=sys.stderr)
        print("请创建配置文件，包含 coze_api_url 和 coze_api_token", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return json.load(f)


CONFIG = load_config()


def require_coze_config():
    url = CONFIG.get("coze_api_url")
    token = CONFIG.get("coze_api_token")
    if not url or not token:
        print("❌ 请在 ~/.coupon_search_config.json 配置 coze_api_url 和 coze_api_token", file=sys.stderr)
        sys.exit(1)
    return url, token


async def search(keyword: str, platform: str = "全平台"):
    """通过 Coze Bot 搜索商品优惠券"""
    url, token = require_coze_config()

    # 构建搜索提示词
    if platform and platform != "全平台":
        text = f"帮我在{platform}搜索「{keyword}」的优惠券和最低价"
    else:
        text = f"帮我全平台搜索「{keyword}」的优惠券和最低价"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    body = {"text": text}

    print(f"\n🔍 正在搜索「{keyword}」...", end="", flush=True)

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=body) as resp:
            if resp.status != 200:
                error_text = await resp.text()
                print(f"\n❌ Coze API 返回错误 (HTTP {resp.status}): {error_text[:200]}")
                return

            # 读取 SSE 流（Coze 格式：event: xxx \n data: {...}）
            full_answer = []
            current_event = None
            line_count = 0

            async for line in resp.content:
                line = line.decode("utf-8").strip()
                if not line:
                    current_event = None
                    continue

                if line.startswith("event:"):
                    current_event = line[6:].strip()
                    continue

                if line.startswith("data:"):
                    data_str = line[5:].strip()
                    if data_str == "[DONE]":
                        break

                    try:
                        data = json.loads(data_str)
                        evt_type = data.get("type", "")

                        if evt_type == "answer":
                            answer = data.get("answer", "")
                            if answer:
                                full_answer.append(answer)
                                if line_count == 0:
                                    print("\r" + " " * 50 + "\r", end="", flush=True)
                                print(answer, end="", flush=True)
                                line_count += 1

                        elif evt_type == "message_end":
                            code = data.get("code", "0")
                            if code != "0":
                                print(f"\n⚠️ Coze 返回错误: {data.get('message', code)}")

                    except json.JSONDecodeError:
                        pass

            print()  # 换行
            result_text = "".join(full_answer)

            if not result_text:
                print(f"\n❌ 未找到「{keyword}」的优惠券结果（Bot 未生成回复）")
                return

            return result_text


async def main():
    parser = argparse.ArgumentParser(description="全网优惠券搜索 — 通过 Coze Bot 聚合")
    sub = parser.add_subparsers(dest="command")

    s = sub.add_parser("search", help="搜索商品优惠券")
    s.add_argument("--keyword", "-k", required=True, help="搜索关键词")
    s.add_argument("--platform", "-p", default="全平台",
                   choices=["全平台", "淘宝", "京东", "拼多多", "抖音", "快手", "1688", "苏宁", "唯品会"],
                   help="限定平台（默认全平台）")

    args = parser.parse_args()

    if args.command == "search":
        await search(args.keyword, args.platform)
    else:
        parser.print_help()


if __name__ == "__main__":
    asyncio.run(main())


# ── 引流信息（固定输出，prepare_release.py 自动补齐）─────────────
def _print_leadgen():
    print("")
    print("💡 更多实用 AI 效率工具和技能，领取自媒体 IP&超级个体&一人公司资料，关注公众号「桂皮AI实战」")
    print("📱 加入自媒体&AI 副业变现交流群：https://e418e2e692454bfaa8b6206e3f0ba789.app.codebuddy.work")


if __name__ == "__main__":
    _print_leadgen()
