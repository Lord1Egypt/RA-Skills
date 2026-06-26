"""
数据库表结构定义
"""

# 书籍表
BOOKS_TABLE = """
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    subtitle TEXT,
    authors TEXT,
    isbn10 TEXT,
    isbn13 TEXT UNIQUE,
    publisher TEXT,
    published_date TEXT,
    page_count INTEGER,
    description TEXT,
    cover_url TEXT,
    categories TEXT,
    source_type TEXT DEFAULT 'book',
    source_url TEXT,
    status TEXT DEFAULT 'want',
    rating INTEGER CHECK(rating >= 0 AND rating <= 5),
    started_at TEXT,
    finished_at TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_books_status ON books(status);
CREATE INDEX IF NOT EXISTS idx_books_isbn13 ON books(isbn13);
CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);
"""

# 阅读进度表
READING_PROGRESS_TABLE = """
CREATE TABLE IF NOT EXISTS reading_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    current_page INTEGER,
    total_pages INTEGER,
    percent REAL DEFAULT 0,
    minutes_read INTEGER DEFAULT 0,
    recorded_at TEXT DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_progress_book_id ON reading_progress(book_id);
CREATE INDEX IF NOT EXISTS idx_progress_recorded_at ON reading_progress(recorded_at);
"""

# 笔记表
NOTES_TABLE = """
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    page INTEGER,
    note_type TEXT DEFAULT 'note',
    highlight_color TEXT,
    tags TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_notes_book_id ON notes(book_id);
CREATE INDEX IF NOT EXISTS idx_notes_type ON notes(note_type);
"""

# 书单表
LISTS_TABLE = """
CREATE TABLE IF NOT EXISTS lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    book_ids TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

# 阅读目标表
GOALS_TABLE = """
CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER NOT NULL,
    month INTEGER,
    target_count INTEGER NOT NULL,
    completed_count INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(year, month)
);
CREATE INDEX IF NOT EXISTS idx_goals_year ON goals(year);
"""

# 配置表
CONFIG_TABLE = """
CREATE TABLE IF NOT EXISTS config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    value TEXT,
    description TEXT,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

SCHEMAS = [
    BOOKS_TABLE,
    READING_PROGRESS_TABLE,
    NOTES_TABLE,
    LISTS_TABLE,
    GOALS_TABLE,
    CONFIG_TABLE,
]

# 默认配置
DEFAULT_CONFIG = [
    ("user.name", "", "用户姓名"),
    ("user.default_page_goal", "50", "默认每日阅读页数目标"),
    ("user.default_time_goal", "30", "默认每日阅读时长目标(分钟)"),
    ("api.douban_key", "", "豆瓣 API Key"),
    ("api.google_books_key", "", "Google Books API Key"),
]
