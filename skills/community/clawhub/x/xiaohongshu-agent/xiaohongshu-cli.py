#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书 (Xiaohongshu/RED) CLI 工具
让 AI Agent 控制小红书！支持发布笔记、搜索内容、获取用户信息等。

⚠️ 风险警告：
- 可能触发风控导致账号被限制甚至封禁
- 使用需谨慎，建议仅用于学习/测试
"""

import click
import json
import sys
import os
from datetime import datetime

try:
    from xhs import XhsClient
except ImportError:
    print("❌ 错误：未安装 xhs 库")
    print("请运行：pip3 install xhs --break-system-packages")
    sys.exit(1)


def get_client(cookie: str = None):
    """获取客户端实例"""
    if not cookie:
        # 从环境变量读取
        cookie = os.environ.get('XHS_COOKIE', '')
    
    if not cookie:
        click.echo("❌ 错误：未提供 Cookie")
        click.echo("请使用 --cookie 参数或设置 XHS_COOKIE 环境变量")
        sys.exit(1)
    
    return XhsClient(cookie=cookie)


@click.group()
@click.option('--cookie', '-c', default=None, help='小红书 Cookie')
@click.option('--json-output', '-j', is_flag=True, help='JSON 格式输出')
@click.pass_context
def cli(ctx, cookie, json_output):
    """📕 小红书 CLI 工具 - 让 AI Agent 控制小红书
    
    ⚠️ 风险警告：
    - 可能触发风控导致账号被限制甚至封禁
    - 使用需谨慎，建议仅用于学习/测试
    """
    ctx.ensure_object(dict)
    ctx.obj['client'] = get_client(cookie)
    ctx.obj['json_output'] = json_output


@cli.group()
@click.pass_context
def note(ctx):
    """笔记相关操作"""
    pass


@note.command('search')
@click.option('--keyword', '-k', required=True, help='搜索关键词')
@click.option('--limit', '-l', default=10, help='返回数量（默认 10）')
@click.pass_context
def note_search(ctx, keyword, limit):
    """搜索笔记"""
    client = ctx.obj['client']
    json_output = ctx.obj['json_output']
    
    try:
        result = client.search_note(keyword, limit=limit)
        
        if json_output:
            click.echo(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            click.echo(f"\n📕 搜索结果：{keyword}\n")
            for i, note in enumerate(result, 1):
                title = note.get('title', '无标题')
                author = note.get('user', {}).get('nickname', '未知')
                likes = note.get('likes', 0)
                click.echo(f"{i}. {title}")
                click.echo(f"   作者：{author} | 👍 {likes}")
                click.echo()
    except Exception as e:
        click.echo(f"❌ 错误：{str(e)}", err=True)
        sys.exit(1)


@note.command('info')
@click.option('--note-id', '-n', required=True, help='笔记 ID')
@click.option('--xsec-token', '-t', required=True, help='XSEC Token')
@click.pass_context
def note_info(ctx, note_id, xsec_token):
    """获取笔记详情"""
    client = ctx.obj['client']
    json_output = ctx.obj['json_output']
    
    try:
        result = client.get_note(note_id, xsec_token)
        
        if json_output:
            click.echo(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            click.echo(f"\n📕 笔记详情\n")
            click.echo(f"标题：{result.get('title', '无标题')}")
            click.echo(f"作者：{result.get('user', {}).get('nickname', '未知')}")
            click.echo(f"描述：{result.get('desc', '')[:200]}...")
            click.echo(f"👍 {result.get('likes', 0)} | 💬 {result.get('comments', 0)} | ⭐ {result.get('collects', 0)}")
    except Exception as e:
        click.echo(f"❌ 错误：{str(e)}", err=True)
        sys.exit(1)


@note.command('publish')
@click.option('--title', '-t', required=True, help='笔记标题')
@click.option('--content', '-c', required=True, help='笔记内容')
@click.option('--image-paths', '-i', multiple=True, help='图片路径（可多个）')
@click.option('--topics', multiple=True, help='话题标签（可多个）')
@click.pass_context
def note_publish(ctx, title, content, image_paths, topics):
    """发布笔记"""
    client = ctx.obj['client']
    json_output = ctx.obj['json_output']
    
    try:
        # 上传图片（如果有）
        image_infos = []
        if image_paths:
            for img_path in image_paths:
                if os.path.exists(img_path):
                    # 这里需要调用上传 API
                    click.echo(f"📷 准备上传图片：{img_path}")
        
        # 发布笔记
        result = client.create_note(
            title=title,
            desc=content,
            image_infos=image_infos if image_infos else None,
            topics=list(topics) if topics else None
        )
        
        if json_output:
            click.echo(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            click.echo(f"✅ 笔记发布成功！")
            click.echo(f"标题：{title}")
    except Exception as e:
        click.echo(f"❌ 错误：{str(e)}", err=True)
        sys.exit(1)


@note.command('delete')
@click.option('--note-id', '-n', required=True, help='笔记 ID')
@click.pass_context
def note_delete(ctx, note_id):
    """删除笔记"""
    client = ctx.obj['client']
    
    try:
        result = client.delete_note(note_id)
        click.echo(f"✅ 笔记已删除：{note_id}")
    except Exception as e:
        click.echo(f"❌ 错误：{str(e)}", err=True)
        sys.exit(1)


@cli.group()
@click.pass_context
def user(ctx):
    """用户相关操作"""
    pass


@user.command('info')
@click.option('--user-id', '-u', required=True, help='用户 ID')
@click.pass_context
def user_info(ctx, user_id):
    """获取用户信息"""
    client = ctx.obj['client']
    json_output = ctx.obj['json_output']
    
    try:
        result = client.get_user_info(user_id)
        
        if json_output:
            click.echo(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            click.echo(f"\n👤 用户信息\n")
            click.echo(f"昵称：{result.get('nickname', '未知')}")
            click.echo(f"ID: {user_id}")
            click.echo(f"简介：{result.get('desc', '无')}")
            click.echo(f"👥 粉丝：{result.get('followers', 0)} | 关注：{result.get('following', 0)}")
            click.echo(f"📕 笔记：{result.get('notes_count', 0)}")
    except Exception as e:
        click.echo(f"❌ 错误：{str(e)}", err=True)
        sys.exit(1)


@user.command('current')
@click.pass_context
def user_current(ctx):
    """获取当前登录用户信息"""
    client = ctx.obj['client']
    json_output = ctx.obj['json_output']
    
    try:
        result = client.get_current_user()
        
        if json_output:
            click.echo(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            click.echo(f"\n👤 当前用户\n")
            click.echo(f"昵称：{result.get('nickname', '未知')}")
            click.echo(f"ID: {result.get('user_id', '未知')}")
    except Exception as e:
        click.echo(f"❌ 错误：{str(e)}", err=True)
        sys.exit(1)


@user.command('notes')
@click.option('--user-id', '-u', required=True, help='用户 ID')
@click.option('--limit', '-l', default=10, help='返回数量（默认 10）')
@click.pass_context
def user_notes(ctx, user_id, limit):
    """获取用户笔记列表"""
    client = ctx.obj['client']
    json_output = ctx.obj['json_output']
    
    try:
        result = client.get_user_notes(user_id, limit=limit)
        
        if json_output:
            click.echo(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            click.echo(f"\n📕 用户笔记：{user_id}\n")
            for i, note in enumerate(result, 1):
                title = note.get('title', '无标题')
                likes = note.get('likes', 0)
                click.echo(f"{i}. {title} | 👍 {likes}")
    except Exception as e:
        click.echo(f"❌ 错误：{str(e)}", err=True)
        sys.exit(1)


@cli.group()
@click.pass_context
def comment(ctx):
    """评论相关操作"""
    pass


@comment.command('list')
@click.option('--note-id', '-n', required=True, help='笔记 ID')
@click.option('--xsec-token', '-t', required=True, help='XSEC Token')
@click.option('--limit', '-l', default=20, help='返回数量（默认 20）')
@click.pass_context
def comment_list(ctx, note_id, xsec_token, limit):
    """获取评论列表"""
    client = ctx.obj['client']
    json_output = ctx.obj['json_output']
    
    try:
        result = client.get_note_comments(note_id, xsec_token)
        comments = result.get('comments', [])[:limit]
        
        if json_output:
            click.echo(json.dumps({'comments': comments}, ensure_ascii=False, indent=2))
        else:
            click.echo(f"\n💬 评论列表\n")
            for i, c in enumerate(comments, 1):
                user = c.get('user', {})
                content = c.get('content', '')
                likes = c.get('likes', 0)
                click.echo(f"{i}. {user.get('nickname', '未知')}: {content[:50]}... | 👍 {likes}")
    except Exception as e:
        click.echo(f"❌ 错误：{str(e)}", err=True)
        sys.exit(1)


@comment.command('post')
@click.option('--note-id', '-n', required=True, help='笔记 ID')
@click.option('--content', '-c', required=True, help='评论内容')
@click.pass_context
def comment_post(ctx, note_id, content):
    """发布评论"""
    client = ctx.obj['client']
    
    try:
        result = client.create_comment(note_id, content)
        click.echo(f"✅ 评论发布成功！")
    except Exception as e:
        click.echo(f"❌ 错误：{str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def feed(ctx):
    """获取首页推荐"""
    client = ctx.obj['client']
    json_output = ctx.obj['json_output']
    
    try:
        result = client.get_home_feed()
        
        if json_output:
            click.echo(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            click.echo(f"\n🏠 首页推荐\n")
            for i, note in enumerate(result[:10], 1):
                title = note.get('title', '无标题')
                author = note.get('user', {}).get('nickname', '未知')
                click.echo(f"{i}. {title} - {author}")
    except Exception as e:
        click.echo(f"❌ 错误：{str(e)}", err=True)
        sys.exit(1)


@cli.command()
def version():
    """显示版本信息"""
    click.echo("📕 小红书 CLI 工具 v1.0.0")
    click.echo("⚠️ 风险警告：可能触发风控导致账号限制")
    click.echo("使用 xhs 库版本:", end=" ")
    try:
        import xhs
        click.echo(xhs.__version__)
    except:
        click.echo("unknown")


if __name__ == '__main__':
    cli()
