"""History screen: past discover sessions."""

from textual import work
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Static, DataTable, Footer


class HistoryScreen(Screen):
    BINDINGS = [
        ("escape", "go_back", "Back"),
    ]

    def __init__(self):
        super().__init__()
        self._sessions: list[dict] = []

    def compose(self) -> ComposeResult:
        with Vertical(id="hist-root"):
            yield Static("[bold #00f0ff]HISTORY[/]", id="hist-title")
            yield DataTable(id="hist-table", cursor_type="row")

        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#hist-table", DataTable)
        table.add_columns("Date", "Query", "Threads", "Status")
        self.load_history()

    @work(exclusive=True)
    async def load_history(self) -> None:
        from redditrank_tui.api import RedditRankAPI
        api = RedditRankAPI()

        try:
            data = await api.list_sessions(limit=50)
            self._sessions = data.get("sessions", [])

            table = self.query_one("#hist-table", DataTable)
            table.clear()

            for s in self._sessions:
                date = s.get("created_at", "")[:10]
                query = s.get("keyword") or s.get("product_url") or s.get("product_description", "")
                if len(query) > 45:
                    query = query[:42] + "..."
                threads = str(s.get("threads_found", 0))
                table.add_row(date, query, threads, "done", key=s.get("id", ""))

        except Exception as e:
            table = self.query_one("#hist-table", DataTable)
            table.add_row("", f"Error: {e}", "", "")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        session_id = str(event.row_key.value) if event.row_key else None
        if session_id:
            from redditrank_tui.screens.threads import ThreadBrowserScreen
            self.app.push_screen(ThreadBrowserScreen(session_id=session_id))

    def action_go_back(self) -> None:
        self.app.pop_screen()
