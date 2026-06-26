import requests
from typing import List, Optional, Tuple
from datetime import datetime
from urllib.parse import quote
from book_manager import Book


class LibraryScraper:
    """图书馆网站爬虫基类"""

    def __init__(self, config: dict):
        self.config = config
        self.base_url = config.get("base_url", "")
        self.search_url = config.get("search_url", "")
        self.timeout = config.get("timeout", 30)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Referer": "https://www.szlib.org.cn/opac/",
            }
        )
        # 先访问搜索页面建立 session
        self._init_session()

    def _init_session(self):
        """初始化 session，访问搜索页面"""
        try:
            self.session.get("https://www.szlib.org.cn/opac/", timeout=self.timeout)
        except Exception as e:
            print(f"初始化 session 失败: {e}")

    def search_book(self, book: Book) -> Tuple[bool, List[str], str]:
        """
        搜索书籍并返回可借状态和馆藏位置
        返回: (是否可借, 馆藏位置列表, 最后检查时间)
        """
        raise NotImplementedError("子类必须实现 search_book 方法")

    def update_book_status(self, book: Book) -> Tuple[Book, bool]:
        """更新书籍状态"""
        available, locations, check_time = self.search_book(book)
        status_changed = book.available != available
        book.available = available
        book.locations = locations
        book.last_checked = check_time
        return book, status_changed


class ShenzhenLibraryScraper(LibraryScraper):
    """深圳图书馆爬虫"""

    def __init__(self, config: dict):
        super().__init__(config)
        self.api_base = "https://www.szlib.org.cn/api/opacservice"

    def search_book(self, book: Book) -> Tuple[bool, List[str], str]:
        """搜索深圳图书馆书籍"""
        check_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        keyword = book.isbn or book.title or f"{book.author} {book.title}"

        if not keyword:
            return False, [], check_time

        try:
            print(f"正在搜索: {keyword}")

            # 第一步：搜索书籍
            record_id, table_name = self._search_book_by_keyword(keyword)
            if not record_id:
                print(f"未找到书籍: {keyword}")
                return False, [], check_time

            print(f"找到书籍，recordId: {record_id}, tableName: {table_name}")

            # 第二步：获取馆藏信息
            locations = self._get_holding_info(record_id, table_name)
            available = len(locations) > 0

            return available, locations, check_time

        except requests.RequestException as e:
            print(f"搜索失败: {e}")
            return False, [], check_time

    def _search_book_by_keyword(
        self, keyword: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """通过关键词搜索书籍"""
        try:
            encoded_keyword = quote(keyword)
            url = (
                f"{self.api_base}/getQueryResult?"
                f"v_index=title&"
                f"v_value={encoded_keyword}&"
                f"library=all&"
                f"v_tablearray=bibliosm,serbibm,apabibibm,mmbibm,&"
                f"cirtype=&"
                f"sortfield=ptitle&"
                f"sorttype=desc&"
                f"pageNum=10&"
                f"v_page=1&"
                f"v_startpubyear=&"
                f"v_endpubyear=&"
                f"v_secondquery=&"
                f"client_id=t1"
            )

            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            if data.get("data"):
                docs = data["data"].get("docs", [])
                if docs:
                    first_doc = docs[0]
                    record_id = first_doc.get("recordid")
                    table_name = first_doc.get("tablename")
                    return str(record_id) if record_id else None, table_name

            return None, None

        except Exception as e:
            print(f"搜索书籍时出错: {e}")
            return None, None

    def _get_holding_info(self, record_id: str, table_name: str) -> List[str]:
        """获取馆藏信息"""
        locations = []
        try:
            url = f"{self.api_base}/getpreholding"
            params = {
                "metaTable": table_name,
                "metaId": record_id,
                "library": "all",
                "client_id": "t1",
            }

            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            can_loan_list = data.get("CanLoanBook", [])
            for loan_info in can_loan_list:
                record_list = loan_info.get("recordList", [])
                for record in record_list:
                    location = record.get("local", "")
                    if location and location not in locations:
                        locations.append(location)

            return locations

        except Exception as e:
            print(f"获取馆藏信息时出错: {e}")
            return locations
