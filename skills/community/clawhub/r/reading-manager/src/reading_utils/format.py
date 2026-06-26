"""
格式化工具
"""
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


def format_datetime(dt_str: str) -> str:
    """格式化日期时间"""
    if not dt_str:
        return "-"
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return dt_str


def format_date(dt_str: str) -> str:
    """格式化日期"""
    if not dt_str:
        return "-"
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except:
        return dt_str


def format_authors(authors: list) -> str:
    """格式化作者列表"""
    if not authors:
        return "未知作者"
    return ", ".join(authors)


def format_pages(current: int, total: int) -> str:
    """格式化页码显示"""
    if not current or not total:
        return "-"
    percent = current / total * 100
    return f"{current}/{total} ({percent:.1f}%)"


def format_duration(minutes: int) -> str:
    """格式化时长"""
    if not minutes:
        return "-"
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0:
        return f"{hours}小时{mins}分钟"
    return f"{mins}分钟"


def print_book_table(books: list, title: str = "书籍列表"):
    """打印书籍表格"""
    if not books:
        console.print("[yellow]暂无书籍[/yellow]")
        return
    
    table = Table(title=title, box=box.ROUNDED)
    table.add_column("ID", style="cyan", width=4)
    table.add_column("书名", style="green", width=30)
    table.add_column("作者", width=20)
    table.add_column("状态", width=8)
    table.add_column("进度", width=12)
    table.add_column("评分", width=6)
    
    status_map = {
        "want": "[yellow]想读[/yellow]",
        "reading": "[blue]在读[/blue]",
        "finished": "[green]已读[/green]",
    }
    
    for book in books:
        status = status_map.get(book.get("status"), book.get("status"))
        progress = "-"
        if book.get("page_count"):
            progress = f"0/{book['page_count']}"
        
        rating = "⭐" * book.get("rating", 0) if book.get("rating") else "-"
        
        table.add_row(
            str(book.get("id")),
            book.get("title", "-")[:30],
            format_authors(book.get("authors", []))[:20],
            status,
            progress,
            rating,
        )
    
    console.print(table)


def print_book_detail(book: dict):
    """打印书籍详情"""
    if not book:
        console.print("[red]书籍不存在[/red]")
        return
    
    status_map = {
        "want": "想读",
        "reading": "在读",
        "finished": "已读",
    }
    
    content = f"""
[bold cyan]📚 {book.get('title', '未命名')}[/bold cyan]

[bold]作者:[/bold] {format_authors(book.get('authors', []))}
[bold]出版社:[/bold] {book.get('publisher') or '-'}
[bold]出版日期:[/bold] {book.get('published_date') or '-'}
[bold]页数:[/bold] {book.get('page_count') or '-'}
[bold]ISBN:[/bold] {book.get('isbn13') or book.get('isbn10') or '-'}
[bold]状态:[/bold] {status_map.get(book.get('status'), book.get('status'))}
[bold]评分:[/bold] {'⭐' * book.get('rating', 0) if book.get('rating') else '-'}

[bold]简介:[/bold]
{book.get('description') or '暂无简介'}
    """.strip()
    
    console.print(Panel(content, box=box.ROUNDED))


def print_note_table(notes: list, title: str = "笔记列表"):
    """打印笔记表格"""
    if not notes:
        console.print("[yellow]暂无笔记[/yellow]")
        return
    
    table = Table(title=title, box=box.ROUNDED)
    table.add_column("ID", style="cyan", width=4)
    table.add_column("内容", width=50)
    table.add_column("页码", width=6)
    table.add_column("类型", width=8)
    table.add_column("标签", width=15)
    
    type_map = {
        "note": "笔记",
        "highlight": "高亮",
    }
    
    for note in notes:
        tags = ", ".join(note.get("tags", []))[:15] if note.get("tags") else "-"
        content = note.get("content", "")[:50] + "..." if len(note.get("content", "")) > 50 else note.get("content", "")
        
        table.add_row(
            str(note.get("id")),
            content,
            str(note.get("page")) if note.get("page") else "-",
            type_map.get(note.get("note_type"), note.get("note_type")),
            tags,
        )
    
    console.print(table)


def print_progress_bar(current: int, total: int, width: int = 30) -> str:
    """打印进度条"""
    if not total:
        return "[grey]无进度数据[/grey]"
    
    percent = min(100, current / total * 100)
    filled = int(width * percent / 100)
    bar = "█" * filled + "░" * (width - filled)
    
    color = "green" if percent >= 100 else "blue" if percent >= 50 else "yellow"
    return f"[{color}]{bar}[/{color}] {percent:.1f}%"
