"""
XHS Expert - CLI入口
命令行工具入口，支持所有核心操作
"""

import asyncio
import json
import sys
from pathlib import Path

import click

# 添加包路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.xhs_client import XHSClient, XHSClientConfig
from scripts.cookie_manager import CookieManager, check_login_status, login_with_browser
from scripts.feed_collector import FeedCollector, CollectConfig
from scripts.interaction_handler import InteractionHandler, BatchInteractionHandler
from dataclasses import asdict


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """🐾 XHS Expert - 小红书运营专家技能"""
    pass


# ============== 认证命令 ==============

@cli.group("auth")
def auth_group():
    """认证管理"""
    pass


@auth_group.command("status")
def auth_status():
    """检查登录状态"""
    status = check_login_status()

    if status.get("logged_in"):
        click.echo(f"✅ 已登录 (Profile: {status.get('profile', 'default')})")
        click.echo(f"   Cookie有效期: {status.get('age_days', '?')}天")
    else:
        click.echo(f"❌ 未登录: {status.get('reason', '未知原因')}")
        click.echo("")
        click.echo("提示: 运行 `xhs auth login` 进行登录")


@auth_group.command("login")
@click.option("--profile", default="default", help="Profile名称")
@click.option("--headless", is_flag=True, help="无头模式")
def auth_login(profile, headless):
    """浏览器扫码登录"""
    click.echo(f"正在启动浏览器 (Profile: {profile})...")

    async def run():
        result = await login_with_browser(profile=profile, headless=headless)
        if result.get("success"):
            click.echo(f"✅ 登录成功 (Profile: {result.get('profile')})")
        else:
            click.echo(f"❌ 登录失败: {result.get('error')}")
            sys.exit(1)

    asyncio.run(run())


# ============== 内容发现命令 ==============

@cli.group("explore")
def explore_group():
    """内容发现"""
    pass


@explore_group.command("search")
@click.option("--keyword", "-k", required=True, help="搜索关键词")
@click.option("--max", "-m", default=20, help="最大笔记数")
@click.option("--sort", "-s", default="general",
              type=click.Choice(["general", "time", "time_like"]),
              help="排序方式")
@click.option("--output", "-o", type=click.Path(), help="输出文件路径")
def explore_search(keyword, max, sort, output):
    """搜索笔记"""
    async def run():
        client = XHSClient()
        await client.load_cookies()

        collector = FeedCollector(
            client,
            config=CollectConfig(
                keyword=keyword,
                max_notes=max,
                sort=sort
            )
        )

        click.echo(f"正在搜索: {keyword}")
        notes = await collector.collect_search()

        if output:
            path = collector.save_to_file(Path(output))
            click.echo(f"✅ 已保存到: {path}")
        else:
            summary = collector.get_summary()
            click.echo(f"\n=== 搜索结果 ===")
            click.echo(f"共找到 {summary['total']} 篇笔记")
            click.echo(f"总点赞: {summary.get('total_likes', 0)}")
            click.echo(f"总收藏: {summary.get('total_collects', 0)}")
            click.echo("")

            for note in notes[:10]:
                click.echo(f"📝 {note.title or '(无标题)'}")
                click.echo(f"   ID: {note.note_id}")
                click.echo(f"   作者: {note.user_nickname}")
                click.echo(f"   点赞: {note.like_count} | 收藏: {note.collect_count} | 评论: {note.comment_count}")
                click.echo("")

        await client.close()

    asyncio.run(run())


@explore_group.command("detail")
@click.option("--note-id", "-n", required=True, help="笔记ID")
@click.option("--xsec-token", "-t", default="", help="XSEC Token")
@click.option("--include-comments/--no-comments", default=True, help="包含评论")
def explore_detail(note_id, xsec_token, include_comments):
    """获取笔记详情"""
    async def run():
        client = XHSClient()
        await client.load_cookies()

        collector = FeedCollector(client)
        result = await collector.collect_detail(note_id, xsec_token, include_comments)

        if not result:
            click.echo("❌ 获取详情失败")
            sys.exit(1)

        note = result.get("note")
        comments = result.get("comments", [])

        click.echo(f"\n=== 笔记详情 ===")
        click.echo(f"标题: {note.title or '(无标题)'}")
        click.echo(f"ID: {note.note_id}")
        click.echo(f"作者: {note.user_nickname} ({note.user_id})")
        click.echo(f"内容: {note.desc[:200]}..." if note.desc else "内容: (无)")
        click.echo(f"点赞: {note.like_count} | 收藏: {note.collect_count} | 评论: {note.comment_count}")
        click.echo(f"标签: {', '.join(note.tags) if note.tags else '无'}")

        if comments:
            click.echo(f"\n=== 评论 ({len(comments)}) ===")
            for c in comments[:5]:
                click.echo(f"  💬 {c.user_nickname}: {c.content[:50]}...")
                if c.sub_comments:
                    for sub in c.sub_comments[:2]:
                        click.echo(f"    ↳ {sub.user_nickname}: {sub.content[:50]}...")

        await client.close()

    asyncio.run(run())


# ============== 互动命令 ==============

@cli.group("interact")
def interact_group():
    """社交互动"""
    pass


@interact_group.command("like")
@click.option("--note-id", "-n", required=True, help="笔记ID")
@click.option("--action", "-a", default="add",
              type=click.Choice(["add", "remove"]),
              help="操作: add点赞, remove取消")
def interact_like(note_id, action):
    """点赞/取消点赞"""
    async def run():
        client = XHSClient()
        await client.load_cookies()

        handler = InteractionHandler(client)
        result = await handler.like(note_id, action)

        emoji = "✅" if result.result.value == "success" else "❌"
        click.echo(f"{emoji} {result.message}")

        await client.close()

    asyncio.run(run())


@interact_group.command("collect")
@click.option("--note-id", "-n", required=True, help="笔记ID")
@click.option("--action", "-a", default="add",
              type=click.Choice(["add", "remove"]),
              help="操作: add收藏, remove取消")
def interact_collect(note_id, action):
    """收藏/取消收藏"""
    async def run():
        client = XHSClient()
        await client.load_cookies()

        handler = InteractionHandler(client)
        result = await handler.collect(note_id, action=action)

        emoji = "✅" if result.result.value == "success" else "❌"
        click.echo(f"{emoji} {result.message}")

        await client.close()

    asyncio.run(run())


@interact_group.command("comment")
@click.option("--note-id", "-n", required=True, help="笔记ID")
@click.option("--content", "-c", required=True, help="评论内容")
def interact_comment(note_id, content):
    """发表评论"""
    async def run():
        client = XHSClient()
        await client.load_cookies()

        handler = InteractionHandler(client)
        result = await handler.comment(note_id, content)

        emoji = "✅" if result.result.value == "success" else "❌"
        click.echo(f"{emoji} {result.message}")

        await client.close()

    asyncio.run(run())


@interact_group.command("follow")
@click.option("--user-id", "-u", required=True, help="用户ID")
@click.option("--action", "-a", default="add",
              type=click.Choice(["add", "remove"]),
              help="操作: add关注, remove取消")
def interact_follow(user_id, action):
    """关注/取消关注用户"""
    async def run():
        client = XHSClient()
        await client.load_cookies()

        handler = InteractionHandler(client)
        if action == "add":
            result = await handler.follow(user_id)
        else:
            result = await handler.unfollow(user_id)

        emoji = "✅" if result.result.value == "success" else "❌"
        click.echo(f"{emoji} {result.message}")

        await client.close()

    asyncio.run(run())


@interact_group.command("batch-like")
@click.option("--note-ids", "-n", required=True, help="笔记ID列表，逗号分隔")
@click.option("--delay", "-d", default=2.0, type=float, help="操作间隔（秒）")
def interact_batch_like(note_ids, delay):
    """批量点赞"""
    note_list = [n.strip() for n in note_ids.split(",") if n.strip()]

    async def run():
        client = XHSClient()
        await client.load_cookies()

        handler = InteractionHandler(client)
        batch = BatchInteractionHandler(handler, delay=delay)

        click.echo(f"开始批量点赞 {len(note_list)} 篇笔记...")

        results = await batch.batch_like(note_list)
        summary = batch.summarize_results(results)

        click.echo(f"\n=== 批量操作结果 ===")
        click.echo(f"总计: {summary['total']}")
        click.echo(f"成功: {summary['success']} ✅")
        click.echo(f"失败: {summary['failed']} ❌")
        click.echo(f"成功率: {summary['success_rate']}")

        await client.close()

    asyncio.run(run())


# ============== 数据查询命令 ==============

@cli.group("data")
def data_group():
    """数据查询"""
    pass


@data_group.command("stats")
def data_stats():
    """查看本地数据统计"""
    from scripts.state_parser import NoteCard

    data_dir = Path.home() / ".config" / "xiaohongshu" / "data"

    if not data_dir.exists():
        click.echo("暂无本地数据")
        return

    files = list(data_dir.glob("*.json"))

    if not files:
        click.echo("暂无本地数据")
        return

    total_notes = 0
    total_likes = 0

    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
                if isinstance(data, list):
                    total_notes += len(data)
                    for item in data:
                        if isinstance(item, dict):
                            total_likes += item.get("like_count", 0)
        except Exception:
            continue

    click.echo(f"\n=== 本地数据统计 ===")
    click.echo(f"文件数: {len(files)}")
    click.echo(f"笔记数: {total_notes}")
    click.echo(f"总点赞: {total_likes}")


# ============== 主入口 ==============

def main():
    """CLI主入口"""
    if len(sys.argv) == 1:
        click.echo("🐾 XHS Expert - 小红书运营专家技能")
        click.echo("")
        click.echo("用法:")
        click.echo("  xhs auth status          检查登录状态")
        click.echo("  xhs auth login            扫码登录")
        click.echo("  xhs explore search -k xxx 搜索笔记")
        click.echo("  xhs explore detail -n xxx 获取笔记详情")
        click.echo("  xhs interact like -n xxx  点赞")
        click.echo("  xhs interact comment -n xxx -c xxx  评论")
        click.echo("  xhs data stats            本地数据统计")
        click.echo("")
        click.echo("完整帮助: xhs --help")
        return

    cli()


if __name__ == "__main__":
    main()
