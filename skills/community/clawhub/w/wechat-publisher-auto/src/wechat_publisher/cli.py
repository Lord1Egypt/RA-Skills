"""
CLI 入口 - 支持多账号
"""

import asyncio
import re
from pathlib import Path
from typing import Optional

import httpx
from PIL import Image, ImageDraw
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
import typer

from .config import settings, WeChatAccount
from .converter import WeChatStyleConverter
from .humanizer import Humanizer
from .platforms import WeChatPlatform, PublishRequest

app = typer.Typer(
    name="wechat-publish-pro",
    help="微信公众号文章发布工具",
)
console = Console()


def select_account() -> WeChatAccount:
    """让用户选择要使用的账号"""
    settings.load()
    account_names = settings.get_account_names()
    
    if not account_names:
        raise RuntimeError("未配置任何微信公众号账号，请先使用 config add-account 添加账号")
    
    # 只有一个账号，直接使用
    if len(account_names) == 1:
        account_key = account_names[0]
        console.print(f"[cyan]使用账号: {settings.get_account(account_key).name}[/cyan]")
        return settings.get_account(account_key)
    
    # 多个账号，让用户选择
    default_key = settings.get_default_account() or account_names[0]
    choices = [settings.get_account(k).name for k in account_names]
    choice_map = dict(zip(account_names, choices))
    
    # 显示账号列表
    console.print("[cyan]可用账号:[/cyan]")
    for i, key in enumerate(account_names, 1):
        acc = settings.get_account(key)
        marker = " (默认)" if key == default_key else ""
        console.print(f"  {i}. {acc.name}{marker}")
    
    # 提示选择
    choice = Prompt.ask(
        "\n选择要使用的账号",
        default=str(account_names.index(default_key) + 1),
        show_choices=False
    )
    
    # 解析选择
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(account_names):
            account_key = account_names[idx]
        else:
            account_key = default_key
    except ValueError:
        account_key = default_key
    
    account = settings.get_account(account_key)
    console.print(f"[green]使用账号: {account.name}[/green]\n")
    return account


def create_wechat_platform(account: WeChatAccount) -> WeChatPlatform:
    """创建微信平台实例"""
    if not account.app_id or not account.app_secret:
        raise RuntimeError(f"账号 '{account.name}' 未配置 app_id 或 app_secret")
    return WeChatPlatform(
        app_id=account.app_id,
        app_secret=account.app_secret,
    )


async def humanize_html_content(content: str, intensity: str = "medium") -> tuple[str, bool]:
    """
    对 HTML 内容进行去痕处理

    Returns:
        tuple[处理后的内容, 是否进行了去痕处理]
    """
    settings.load()
    if not settings.is_ai_configured():
        return content, False

    # 简单处理：从 HTML 中提取纯文本进行处理
    # 移除 HTML 标签获取纯文本
    text_content = re.sub(r'<[^>]+>', '\n', content)
    text_content = re.sub(r'\n+', '\n', text_content).strip()

    if not text_content:
        return content, False

    console.print(f"[cyan]正在使用 AI 去痕处理...[/cyan]")

    humanizer = Humanizer(
        api_key=settings.ai.api_key,
        provider=settings.ai.provider,
        base_url=settings.ai.base_url,
        model=settings.ai.model,
    )

    try:
        result = await humanizer.humanize(text_content, intensity=intensity)

        if result.changes:
            console.print(f"[yellow]去痕变化:[/yellow]")
            for change in result.changes[:3]:
                console.print(f"  - {change}")

        # 将去痕后的文本重新包装成简单 HTML
        humanized_html = f"<p>来源: AI整理</p>\n" + result.humanized.replace("\n\n", "</p><p>").replace("\n", "<br>")
        humanized_html = f"<div>{humanized_html}</div>"

        return humanized_html, True
    except Exception as e:
        console.print(f"[yellow]AI 去痕失败: {e}，使用原文发布[/yellow]")
        return content, False
    finally:
        await humanizer.close()


# 配置命令组
config_app = typer.Typer(help="配置管理")
app.add_typer(config_app, name="config")


@config_app.command("init")
def config_init() -> None:
    """初始化配置文件"""
    settings.save()
    console.print(f"[green]配置文件已创建: {settings.get_config_file()}[/green]")


@config_app.command("show")
def config_show() -> None:
    """显示当前配置"""
    settings.load()

    table = Table(title="配置信息")
    table.add_column("配置项", style="cyan")
    table.add_column("值", style="green")

    table.add_row("配置文件", str(settings.get_config_file()))
    
    # 显示账号列表
    account_names = settings.get_account_names()
    if account_names:
        table.add_row("微信公众号账号", f"共 {len(account_names)} 个")
        default_key = settings.get_default_account()
        for key in account_names:
            acc = settings.get_account(key)
            marker = " (默认)" if key == default_key else ""
            table.add_row(f"  - {key}", f"{acc.name}{marker}")
    else:
        table.add_row("微信公众号账号", "[red]未配置[/red]")
    
    table.add_row("AI Provider", settings.ai.provider or "[red]未配置[/red]")
    table.add_row("AI Model", settings.ai.model or "[red]未配置[/red]")

    console.print(table)


@config_app.command("add-account")
def config_add_account(
    key: str = typer.Argument(..., help="账号标识（如: personal, work）"),
    name: str = typer.Option(..., "--name", "-n", help="账号显示名称"),
    app_id: str = typer.Option(..., "--app-id", help="微信公众号 AppID"),
    app_secret: str = typer.Option(..., "--app-secret", help="微信公众号 AppSecret"),
) -> None:
    """添加微信公众号账号
    
    示例:
        wechat-publish-pro config add-account personal --name "个人公众号" --app-id xxx --app-secret xxx
    """
    settings.load()
    settings.add_account(key, name, app_id, app_secret)
    settings.save()
    console.print(f"[green]已添加账号: {name} (key: {key})[/green]")


@config_app.command("remove-account")
def config_remove_account(
    key: str = typer.Argument(..., help="账号标识"),
) -> None:
    """删除微信公众号账号"""
    settings.load()
    if key not in settings.get_account_names():
        console.print(f"[red]账号 {key} 不存在[/red]")
        raise typer.Exit(1)
    
    name = settings.get_account(key).name
    settings.remove_account(key)
    settings.save()
    console.print(f"[green]已删除账号: {name}[/green]")


@config_app.command("set-default")
def config_set_default(
    key: str = typer.Argument(..., help="账号标识"),
) -> None:
    """设置默认账号"""
    settings.load()
    if key not in settings.get_account_names():
        console.print(f"[red]账号 {key} 不存在[/red]")
        raise typer.Exit(1)
    
    settings.set_default_account(key)
    settings.save()
    console.print(f"[green]已设置默认账号: {settings.get_account(key).name}[/green]")


@config_app.command("set")
def config_set(
    key: str = typer.Argument(..., help="配置键，格式: section.key"),
    value: str = typer.Argument(..., help="配置值"),
) -> None:
    """设置配置项

    示例:
        wechat-publish-pro config set ai.api_key your_api_key
        wechat-publish-pro config set ai.provider qwen
    """
    settings.load()

    parts = key.split(".")
    if len(parts) != 2:
        console.print("[red]错误: 配置键格式应为 section.key[/red]")
        raise typer.Exit(1)

    section, subkey = parts

    if section == "ai":
        if subkey == "provider":
            settings.ai.provider = value
        elif subkey == "api_key":
            settings.ai.api_key = value
        elif subkey == "base_url":
            settings.ai.base_url = value
        elif subkey == "model":
            settings.ai.model = value
        else:
            console.print(f"[red]未知配置项: {key}[/red]")
            raise typer.Exit(1)
    elif section == "wechat":
        console.print("[yellow]提示: 微信账号请使用 add-account 命令添加[/yellow]")
        raise typer.Exit(1)
    else:
        console.print(f"[red]未知配置节: {section}[/red]")
        raise typer.Exit(1)

    settings.save()
    console.print(f"[green]已设置 {key}[/green]")


# 转换命令
@app.command()
def convert(
    file: Path = typer.Argument(..., help="Markdown 文件路径", exists=True),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="输出 HTML 文件路径"),
    theme: str = typer.Option(None, "--theme", help="主题名称 (green/blue/purple/orange/simple/default)"),
    title: Optional[str] = typer.Option(None, "--title", "-t", help="文章标题（默认从文件名提取）"),
) -> None:
    """将 Markdown 转换为微信公众号格式的 HTML

    支持多种精美主题，自动处理代码高亮、列表、表格等元素。
    """
    # 默认使用绿色主题
    if theme is None:
        theme = "green"
    
    if not file.exists():
        console.print(f"[red]文件不存在: {file}[/red]")
        raise typer.Exit(1)

    # 读取 Markdown 内容
    markdown_content = file.read_text(encoding="utf-8")

    # 解析 frontmatter 并移除
    article_title = title
    frontmatter_cover = None
    
    fm_match = re.match(r'^---\n(.*?)\n---\n', markdown_content, re.DOTALL)
    if fm_match:
        fm_content = fm_match.group(1)
        # 移除 frontmatter
        markdown_content = markdown_content[fm_match.end():]
        
        # 提取标题
        if not article_title:
            title_match = re.search(r'^title:\s*(.+?)\s*$', fm_content, re.MULTILINE)
            if title_match:
                article_title = title_match.group(1).strip().strip('"\'')
        
        # 提取封面
        cover_match = re.search(r'^cover:\s*(.+?)\s*$', fm_content, re.MULTILINE)
        if cover_match:
            frontmatter_cover = cover_match.group(1).strip().strip('"\'')
        
        # 如果 frontmatter 有 title，移除正文中的第一个 H1（避免重复）
        if article_title:
            markdown_content = re.sub(r'^#\s+.+$', '', markdown_content, count=1, flags=re.MULTILINE)
            markdown_content = markdown_content.lstrip('\n')
    else:
        # 没有 frontmatter，尝试从第一个 # 标题提取
        if not article_title:
            h1_match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
            if h1_match:
                article_title = h1_match.group(1).strip()

    console.print(f"[cyan]转换 Markdown → HTML[/cyan]")
    console.print(f"[cyan]输入文件: {file}[/cyan]")
    if article_title:
        console.print(f"[cyan]标题: {article_title}[/cyan]")
    if frontmatter_cover:
        console.print(f"[cyan]封面: {frontmatter_cover}[/cyan]")
    console.print(f"[cyan]主题: {theme}[/cyan]")

    # 转换
    try:
        converter = WeChatStyleConverter(theme=theme)
        html_content = converter.convert(markdown_content, title=article_title)
    except Exception as e:
        console.print(f"[red]转换失败: {e}[/red]")
        raise typer.Exit(1)

    # 确定输出文件
    if output:
        output_path = output
    else:
        output_path = file.with_suffix('.html')

    output_path.write_text(html_content, encoding="utf-8")
    console.print(f"[green]转换完成: {output_path}[/green]")


# 发布命令
@app.command()
def publish(
    file: Path = typer.Argument(..., help="HTML 文件路径", exists=True),
    title: Optional[str] = typer.Option(None, "--title", "-t", help="文章标题（默认从文件名提取）"),
    cover: Optional[str] = typer.Option(None, "--cover", "-c", help="封面图片路径"),
    author: Optional[str] = typer.Option(None, "--author", "-a", help="作者"),
    account: Optional[str] = typer.Option(None, "--account", help="指定账号标识（不指定则交互选择）"),
    humanize: bool = typer.Option(True, "--humanize/--no-humanize", help="发布前自动 AI 去痕（默认启用）"),
    intensity: str = typer.Option("medium", "--intensity", "-i", help="去痕强度 (light/medium/heavy)"),
) -> None:
    """发布 HTML 文件到微信公众号草稿箱

    发布前会自动使用 AI 去痕处理，让文章读起来更自然。
    """
    if not file.exists():
        console.print(f"[red]文件不存在: {file}[/red]")
        raise typer.Exit(1)

    # 读取 HTML 内容
    html_content = file.read_text(encoding="utf-8")

    # 确定标题
    article_title = title or file.stem
    if not title:
        # 尝试从 HTML 中提取标题
        title_match = re.search(r"<h1[^>]*>([^<]+)</h1>", html_content)
        if title_match:
            article_title = title_match.group(1)
        else:
            title_match = re.search(r"<title>([^<]+)</title>", html_content)
            if title_match:
                article_title = title_match.group(1)

    console.print(f"[cyan]发布 HTML 文件: {file}[/cyan]")
    console.print(f"[cyan]标题: {article_title}[/cyan]")

    # 选择账号
    if account:
        # 指定账号
        settings.load()
        acc = settings.get_account(account)
        if not acc:
            console.print(f"[red]账号 {account} 不存在[/red]")
            raise typer.Exit(1)
        console.print(f"[cyan]使用账号: {acc.name}[/cyan]\n")
    else:
        # 交互选择
        acc = select_account()

    # AI 去痕处理
    if humanize:
        html_content, was_humanized = asyncio.run(humanize_html_content(html_content, intensity))
        if was_humanized:
            console.print(f"[green]AI 去痕完成[/green]")
        else:
            console.print(f"[yellow]跳过 AI 去痕（未配置 AI）[/yellow]")

    # 发布到平台
    try:
        wechat = create_wechat_platform(acc)
    except RuntimeError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    request = PublishRequest(
        title=article_title,
        content=html_content,
        cover=cover,
        author=author,
    )

    result = asyncio.run(wechat.publish(request))

    if result.success:
        console.print(f"[green]发布到 {acc.name} 成功！[/green]")
        if result.media_id:
            console.print(f"  Media ID: {result.media_id}")
        if result.article_url:
            console.print(f"  URL: {result.article_url}")
    else:
        console.print(f"[red]发布到 {acc.name} 失败: {result.message}[/red]")
        raise typer.Exit(1)


# 测试命令
@app.command()
def test(
    account: Optional[str] = typer.Option(None, "--account", help="指定账号标识"),
) -> None:
    """测试微信公众号连接"""
    if account:
        settings.load()
        acc = settings.get_account(account)
        if not acc:
            console.print(f"[red]账号 {account} 不存在[/red]")
            raise typer.Exit(1)
        console.print(f"[cyan]测试账号: {acc.name}[/cyan]\n")
    else:
        acc = select_account()

    try:
        wechat = create_wechat_platform(acc)
    except RuntimeError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    console.print(f"[cyan]测试 {acc.name} 连接...[/cyan]")

    result = asyncio.run(wechat.validate_credentials())

    if result:
        console.print(f"[green]{acc.name} 连接成功！[/green]")
    else:
        console.print(f"[red]{acc.name} 连接失败[/red]")
        raise typer.Exit(1)


# 上传图片命令
@app.command()
def upload_image(
    file: Path = typer.Argument(..., help="图片文件路径", exists=True),
    account: Optional[str] = typer.Option(None, "--account", help="指定账号标识"),
) -> None:
    """上传图片到微信素材库"""
    if account:
        settings.load()
        acc = settings.get_account(account)
        if not acc:
            console.print(f"[red]账号 {account} 不存在[/red]")
            raise typer.Exit(1)
        console.print(f"[cyan]使用账号: {acc.name}[/cyan]\n")
    else:
        acc = select_account()

    try:
        wechat = create_wechat_platform(acc)
    except RuntimeError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    console.print(f"[cyan]上传图片: {file}[/cyan]")

    result = asyncio.run(wechat.upload_image(str(file)))

    if result.success:
        console.print(f"[green]图片上传成功！[/green]")
        if result.media_id:
            console.print(f"  Media ID: {result.media_id}")
        if result.url:
            console.print(f"  URL: {result.url}")
    else:
        console.print(f"[red]图片上传失败: {result.message}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
