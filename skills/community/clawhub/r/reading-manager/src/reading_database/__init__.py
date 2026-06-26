"""
数据库模块
"""
from .connection import init_database, get_db_path
from .books import (
    add_book, get_book, list_books, update_book, delete_book, 
    search_books, get_stats
)
from .progress import (
    add_progress, get_latest_progress, get_progress_history, 
    get_total_reading_time
)
from .notes import (
    add_note, get_notes, search_notes_by_tag, search_notes, get_all_tags
)
from .lists import (
    create_list, get_list, list_lists, add_book_to_list, 
    remove_book_from_list, get_list_books
)
from .goals import (
    set_goal, get_goal_progress, get_yearly_stats, list_goals
)
