"""Thread browser: table + detail preview."""

import webbrowser

from textual import work
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Static, DataTable, Footer


class ThreadBrowserScreen(Screen):
    BINDINGS = [
        ("escape", "go_back", "Back"),
        ("d", "draft_reply", "Draft Reply"),
        ("o", "open_browser", "Open in Browser"),
    ]

    def __init__(
        self,
        threads: list[dict] | None = None,
        session_id: str | None = None,
        product_name: str = "",
        product_url: str = "",
        product_description: str = "",
    ):
        super().__init__()
        self._threads = threads or []
        self._session_id = session_id
        self._product_name = product_name
        self._product_url = product_url
        self._product_description = product_description
        self._selected_idx = 0

    def compose(self) -> ComposeResult:
        count = len(self._threads)
        title = f"[bold #00f0ff]{count} THREADS FOUND[/]" if count else "[bold #00f0ff]THREADS[/]"

        with Vertical(id="threads-root"):
            yield Static(title, id="threads-title")
            yield DataTable(id="threads-table", cursor_type="row")
            yield Static("", id="threads-preview")

        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#threads-table", DataTable)
        table.add_columns("Src", "Subreddit", "Title", "Opp", "Age", "Pts", "Comments")

        if self._session_id and not self._threads:
            self.load_session()
        else:
            self._populate_table()

    @work(exclusive=True)
    async def load_session(self) -> None:
        from redditrank_tui.api import RedditRankAPI
        api = RedditRankAPI()
        try:
            data = await api.get_session(self._session_id)
            self._threads = data.get("threads", [])
            self._populate_table()
            count = len(self._threads)
            self.query_one("#threads-title", Static).update(
                f"[bold #00f0ff]{count} THREADS[/]"
            )
        except Exception as e:
            self.notify(f"Error loading session: {e}", severity="error")

    def _populate_table(self) -> None:
        table = self.query_one("#threads-table", DataTable)
        table.clear()
        for t in self._threads:
            src = _source_label(t)
            sub = f"r/{t.get('subreddit', '?')}"
            title = t.get("title", "")
            if len(title) > 50:
                title = title[:47] + "..."
            opp = str(round(t.get("opportunity_score", 0), 1))
            age = _age_label(t.get("age_days", 0))
            pts = str(t.get("score", 0))
            comments = str(t.get("num_comments", 0))
            table.add_row(src, sub, title, opp, age, pts, comments)

        if self._threads:
            self._update_preview(0)

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        if event.cursor_row is not None:
            self._selected_idx = event.cursor_row
            self._update_preview(event.cursor_row)

    def _update_preview(self, idx: int) -> None:
        if idx < 0 or idx >= len(self._threads):
            return

        t = self._threads[idx]
        preview = self.query_one("#threads-preview", Static)

        lines = []
        lines.append(
            f"[bold]{t.get('title', '')}[/]\n"
            f"[dim]r/{t.get('subreddit', '')} · {t.get('score', 0)} pts · "
            f"{t.get('num_comments', 0)} comments · {_age_label(t.get('age_days', 0))}[/]"
        )

        selftext = t.get("selftext", "")
        if selftext and selftext != "Title":
            if len(selftext) > 400:
                selftext = selftext[:397] + "..."
            lines.append(f"\n{selftext}")

        top_comments = t.get("top_comments", []) or []
        if top_comments:
            lines.append("\n[bold dim]Top comments:[/]")
            for c in top_comments[:3]:
                author = c.get("author", "?")
                body = c.get("body", "")
                if len(body) > 120:
                    body = body[:117] + "..."
                score = c.get("score", 0)
                lines.append(f"  [#b967ff]u/{author}[/] ({score} pts): {body}")

        if not t.get("is_commentable", True):
            lines.append("\n[#ff003c]Thread is locked[/]")

        preview.update("\n".join(lines))

    def action_draft_reply(self) -> None:
        if not self._threads:
            return
        t = self._threads[self._selected_idx]
        if not t.get("is_commentable", True):
            self.notify("Thread is locked", severity="warning")
            return

        from redditrank_tui.screens.draft import DraftScreen
        self.app.push_screen(DraftScreen(
            thread=t,
            product_name=self._product_name,
            product_url=self._product_url,
            product_description=self._product_description,
        ))

    def action_open_browser(self) -> None:
        if not self._threads:
            return
        url = self._threads[self._selected_idx].get("url", "")
        if url:
            webbrowser.open(url)
            self.notify("Opened in browser")

    def action_go_back(self) -> None:
        self.app.pop_screen()


def _source_label(t: dict) -> str:
    pos = t.get("serp_position")
    if pos:
        return f"G#{pos}"
    return "Fresh"


def _age_label(days: int) -> str:
    if days <= 1:
        return "today"
    if days < 7:
        return f"{days}d"
    if days < 30:
        return f"{days // 7}w"
    return f"{days // 30}mo"
