#!/usr/bin/env python3
"""
Reading Manager CLI - 阅读管家命令行工具
"""
import click
from rich.console import Console
from rich.panel import Panel
from rich import box

from reading_database import (
    init_database, get_db_path,
    add_book, get_book, list_books, update_book, delete_book, search_books, get_stats,
    add_progress, get_latest_progress, get_progress_history, get_total_reading_time,
    add_note, get_notes, search_notes_by_tag, search_notes, get_all_tags,
    create_list, get_list, list_lists, add_book_to_list, remove_book_from_list, get_list_books,
    set_goal, get_goal_progress, get_yearly_stats, list_goals,
)
from reading_api import search_google_books, search_by_isbn_google
from reading_utils import (
    print_book_table, print_book_detail, print_note_table, print_progress_bar,
    format_authors, format_datetime, format_duration,
)

console = Console()


# 初始化数据库
init_database()


@click.group()
@click.version_option(version="1.0.0", prog_name="reading")
def cli():
    """阅读管家 - 个人阅读管理系统"""


# ========== 书籍管理命令 ==========
@cli.group()
def book():
    """书籍管理"""
    pass


@book.command()
@click.option("--title", "-t", help="书名")
@click.option("--author", "-a", help="作者")
@click.option("--isbn", "-i", help="ISBN")
@click.option("--url", "-u", help="文章 URL")
@click.option("--pages", "-p", type=int, help="总页数")
@click.option("--type", "-T", "source_type", default="book", help="类型: book, article, paper")
def add(title, author, isbn, url, pages, source_type):
    """添加书籍或文章"""
    data = {"source_type": source_type}
    
    if isbn:
        console.print(f"[blue]正在通过 ISBN {isbn} 搜索书籍信息...[/blue]")
        book_info = search_by_isbn_google(isbn)
        if book_info:
            data.update(book_info)
            console.print(f"[green]✓ 找到书籍: {book_info.get('title')}[/green]")
        else:
            data["isbn13"] = isbn
            console.print("[yellow]⚠ 未找到书籍信息，请手动输入[/yellow]")
    
    if title:
        data["title"] = title
    if author:
        data["authors"] = [author]
    if pages:
        data["page_count"] = pages
    if url:
        data["source_url"] = url
    
    if not data.get("title"):
        data["title"] = click.prompt("请输入书名")
    
    book_id = add_book(data)
    console.print(f"[green]✓ 书籍已添加 (ID: {book_id})[/green]")


@book.command()
@click.option("--status", "-s", type=click.Choice(["want", "reading", "finished"]), help="按状态筛选")
@click.option("--limit", "-l", type=int, default=20, help="显示数量")
def list(status, limit):
    """列出书籍"""
    books = list_books(status=status, limit=limit)
    title = "书籍列表"
    if status:
        status_names = {"want": "想读", "reading": "在读", "finished": "已读"}
        title = f"{status_names.get(status)}列表"
    print_book_table(books, title)


@book.command()
@click.argument("book_id", type=int)
def show(book_id):
    """查看书籍详情"""
    book = get_book(book_id)
    print_book_detail(book)
    
    # 显示最新进度
    progress = get_latest_progress(book_id)
    if progress:
        console.print(f"\n[bold]当前进度:[/bold]")
        console.print(f"  页码: {progress.get('current_page')}/{progress.get('total_pages')}")
        console.print(f"  {print_progress_bar(progress.get('current_page', 0), progress.get('total_pages', 0))}")


@book.command()
@click.argument("book_id", type=int)
@click.option("--status", "-s", type=click.Choice(["want", "reading", "finished"]))
@click.option("--rating", "-r", type=int, help="评分 1-5")
def update(book_id, status, rating):
    """更新书籍信息"""
    data = {}
    if status:
        data["status"] = status
    if rating:
        data["rating"] = rating
    
    update_book(book_id, data)
    console.print(f"[green]✓ 书籍已更新[/green]")


@book.command()
@click.argument("book_id", type=int)
@click.confirmation_option(prompt="确定要删除这本书吗？")
def delete(book_id):
    """删除书籍"""
    delete_book(book_id)
    console.print(f"[green]✓ 书籍已删除[/green]")


@book.command()
@click.argument("keyword")
def search(keyword):
    """搜索书籍"""
    books = search_books(keyword)
    print_book_table(books, f"搜索 '{keyword}' 的结果")


# ========== 阅读进度命令 ==========
@cli.group()
def progress():
    """阅读进度管理"""
    pass


@progress.command("update")
@click.argument("book_id", type=int)
@click.option("--page", "-p", type=int, help="当前页码")
@click.option("--percent", "-P", type=float, help="阅读百分比")
@click.option("--minutes", "-m", type=int, default=0, help="阅读时长(分钟)")
@click.option("--notes", "-n", help="备注")
def update_progress(book_id, page, percent, minutes, notes):
    """更新阅读进度"""
    add_progress(book_id, current_page=page, percent=percent, 
                 minutes_read=minutes, notes=notes)
    console.print(f"[green]✓ 阅读进度已更新[/green]")


@progress.command("show")
@click.argument("book_id", type=int)
def show_progress(book_id):
    """查看阅读进度"""
    progress = get_latest_progress(book_id)
    book = get_book(book_id)
    
    if not progress:
        console.print("[yellow]暂无阅读进度记录[/yellow]")
        return
    
    console.print(f"\n[bold cyan]📖 {book.get('title')}[/bold cyan]")
    console.print(f"当前页: {progress.get('current_page')}/{progress.get('total_pages')}")
    console.print(f"进度: {print_progress_bar(progress.get('current_page', 0), progress.get('total_pages', 0))}")
    console.print(f"总阅读时长: {format_duration(get_total_reading_time(book_id))}")


@progress.command("history")
@click.argument("book_id", type=int)
@click.option("--limit", "-l", type=int, default=10)
def progress_history(book_id, limit):
    """查看阅读历史"""
    history = get_progress_history(book_id, limit)
    if not history:
        console.print("[yellow]暂无阅读历史[/yellow]")
        return
    
    console.print(f"\n[bold]阅读历史:[/bold]")
    for h in history:
        console.print(f"  {format_datetime(h.get('recorded_at'))} - "
                     f"页 {h.get('current_page')}, "
                     f"时长 {h.get('minutes_read')}分钟")


# ========== 笔记管理命令 ==========
@cli.group()
def note():
    """笔记管理"""
    pass


@note.command("add")
@click.argument("book_id", type=int)
@click.option("--content", "-c", required=True, help="笔记内容")
@click.option("--page", "-p", type=int, help="页码")
@click.option("--tags", "-t", help="标签(逗号分隔)")
def add_note_cmd(book_id, content, page, tags):
    """添加笔记"""
    tag_list = [t.strip() for t in tags.split(",")] if tags else []
    note_id = add_note(book_id, content=content, page=page, note_type="note", tags=tag_list)
    console.print(f"[green]✓ 笔记已添加 (ID: {note_id})[/green]")


@note.command("highlight")
@click.argument("book_id", type=int)
@click.option("--content", "-c", required=True, help="高亮内容")
@click.option("--page", "-p", type=int, help="页码")
@click.option("--color", "-C", default="yellow", help="高亮颜色")
def add_highlight(book_id, content, page, color):
    """添加高亮"""
    note_id = add_note(book_id, content=content, page=page, 
                       note_type="highlight", highlight_color=color)
    console.print(f"[green]✓ 高亮已添加 (ID: {note_id})[/green]")


@note.command("list")
@click.argument("book_id", type=int, required=False)
@click.option("--type", "-t", type=click.Choice(["note", "highlight"]), help="笔记类型")
def list_notes(book_id, type):
    """列出笔记"""
    notes = get_notes(book_id=book_id, note_type=type, limit=50)
    print_note_table(notes)


@note.command("search")
@click.option("--tag", "-t", help="按标签搜索")
@click.option("--keyword", "-k", help="按关键词搜索")
def search_notes_cmd(tag, keyword):
    """搜索笔记"""
    if tag:
        notes = search_notes_by_tag(tag)
    elif keyword:
        notes = search_notes(keyword)
    else:
        console.print("[red]请提供 --tag 或 --keyword 参数[/red]")
        return
    
    print_note_table(notes, f"搜索结果")


@note.command("tags")
def list_tags():
    """列出所有标签"""
    tags = get_all_tags()
    if tags:
        console.print(f"[bold]所有标签:[/bold] {', '.join(tags)}")
    else:
        console.print("[yellow]暂无标签[/yellow]")


# ========== 书单管理命令 ==========
@cli.group()
def list_cmd():
    """书单管理"""
    pass


@list_cmd.command("create")
@click.argument("name")
@click.option("--description", "-d", help="书单描述")
def create_list_cmd(name, description):
    """创建书单"""
    list_id = create_list(name, description)
    console.print(f"[green]✓ 书单已创建 (ID: {list_id})[/green]")


@list_cmd.command("show")
def show_lists():
    """列出所有书单"""
    lists = list_lists()
    if not lists:
        console.print("[yellow]暂无书单[/yellow]")
        return
    
    console.print(f"\n[bold]我的书单:[/bold]")
    for lst in lists:
        console.print(f"  [{lst.get('id')}] {lst.get('name')} - {lst.get('description') or '无描述'}")
        console.print(f"      包含 {len(lst.get('book_ids', []))} 本书")


@list_cmd.command("add-book")
@click.argument("list_name")
@click.argument("book_id", type=int)
def add_to_list(list_name, book_id):
    """添加书籍到书单"""
    lst = get_list(name=list_name)
    if not lst:
        console.print(f"[red]书单 '{list_name}' 不存在[/red]")
        return
    
    add_book_to_list(lst.get("id"), book_id)
    console.print(f"[green]✓ 书籍已添加到书单[/green]")


@list_cmd.command("remove-book")
@click.argument("list_name")
@click.argument("book_id", type=int)
def remove_from_list(list_name, book_id):
    """从书单移除书籍"""
    lst = get_list(name=list_name)
    if not lst:
        console.print(f"[red]书单 '{list_name}' 不存在[/red]")
        return
    
    remove_book_from_list(lst.get("id"), book_id)
    console.print(f"[green]✓ 书籍已从书单移除[/green]")


# ========== 阅读目标命令 ==========
@cli.group()
def goal():
    """阅读目标管理"""
    pass


@goal.command("set-yearly")
@click.argument("target", type=int)
def set_yearly_goal(target):
    """设置年度阅读目标"""
    from datetime import datetime
    year = datetime.now().year
    set_goal(year, target)
    console.print(f"[green]✓ {year} 年阅读目标已设置为 {target} 本[/green]")


@goal.command("set-monthly")
@click.argument("target", type=int)
def set_monthly_goal(target):
    """设置月度阅读目标"""
    from datetime import datetime
    now = datetime.now()
    set_goal(now.year, target, now.month)
    console.print(f"[green]✓ {now.year}年{now.month}月阅读目标已设置为 {target} 本[/green]")


@goal.command("status")
def goal_status():
    """查看目标进度"""
    from datetime import datetime
    now = datetime.now()
    
    # 年度目标
    yearly = get_goal_progress(now.year)
    if yearly:
        console.print(f"\n[bold cyan]📅 {now.year} 年度目标[/bold cyan]")
        console.print(f"  目标: {yearly['target']} 本")
        console.print(f"  已完成: {yearly['completed']} 本")
        console.print(f"  进度: {print_progress_bar(yearly['completed'], yearly['target'])}")
    
    # 月度目标
    monthly = get_goal_progress(now.year, now.month)
    if monthly:
        console.print(f"\n[bold cyan]📆 {now.month} 月度目标[/bold cyan]")
        console.print(f"  目标: {monthly['target']} 本")
        console.print(f"  已完成: {monthly['completed']} 本")
        console.print(f"  进度: {print_progress_bar(monthly['completed'], monthly['target'])}")


@goal.command("stats")
@click.argument("year", type=int, required=False)
def goal_stats(year):
    """查看年度统计"""
    from datetime import datetime
    if not year:
        year = datetime.now().year
    
    stats = get_yearly_stats(year)
    console.print(f"\n[bold cyan]📊 {year} 年阅读统计[/bold cyan]")
    console.print(f"  总完成: {stats['total_finished']} 本")
    
    if stats.get('monthly_breakdown'):
        console.print(f"\n[bold]月度分布:[/bold]")
        for month, count in sorted(stats['monthly_breakdown'].items()):
            console.print(f"  {month}月: {count} 本")


# ========== 报告命令 ==========
@cli.group()
def report():
    """阅读报告"""
    pass


@report.command("stats")
def report_stats():
    """阅读统计概览"""
    stats = get_stats()
    
    content = f"""
[bold cyan]📚 阅读统计[/bold cyan]

总书籍数: {stats['total']}
  • 想读: {stats['want']} 本
  • 在读: {stats['reading']} 本
  • 已读: {stats['finished']} 本

本月完成: {stats['finished_this_month']} 本
    """.strip()
    
    console.print(Panel(content, box=box.ROUNDED))


# ========== 数据管理命令 ==========
@cli.group()
def data():
    """数据管理"""
    pass


@data.command("path")
def data_path():
    """查看数据库路径"""
    console.print(f"数据库路径: {get_db_path()}")


# 主入口
@click.group()
@click.version_option(version="1.0.0")
def main():
    """阅读管家 - 个人阅读管理系统"""
    pass


# 自定义帮助命令
@main.command()
def help():
    """显示帮助信息"""
    console.print(Panel.fit(
        "[bold cyan]📚 阅读管家[/bold cyan]\n\n"
        "命令:\n"
        "  [green]reading book[/green]      书籍管理\n"
        "  [green]reading progress[/green] 阅读进度\n"
        "  [green]reading note[/green]     笔记管理\n"
        "  [green]reading list[/green]     书单管理\n"
        "  [green]reading goal[/green]     阅读目标\n"
        "  [green]reading report[/green]   阅读报告\n\n"
        "使用 [yellow]reading --help[/yellow] 查看帮助",
        box=box.ROUNDED
    ))


# 注册子命令
main.add_command(book)
main.add_command(progress)
main.add_command(note)
main.add_command(list_cmd, name="list")
main.add_command(goal)
main.add_command(report)
main.add_command(data)


if __name__ == "__main__":
    main()
