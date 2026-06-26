"""Dashboard screen: usage stats and recent activity."""

from textual import work
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, Container
from textual.screen import Screen
from textual.widgets import Static, DataTable, Footer, ProgressBar, LoadingIndicator


class DashboardScreen(Screen):
    BINDINGS = [
        ("n", "new_discover", "New Discover"),
        ("h", "history", "History"),
        ("s", "settings", "Settings"),
        ("q", "quit", "Quit"),
        ("?", "help", "Help"),
    ]

    def __init__(self):
        super().__init__()
        self._usage_data: dict = {}
        self._sessions: list = []

    def compose(self) -> ComposeResult:
        with Vertical(id="dash-root"):
            yield Static(
                "[bold #00f0ff]REDDITRANK[/] [dim]v1.0[/]",
                id="dash-title",
            )

            with Horizontal(id="dash-panels"):
                # Left: usage + quick start
                with Vertical(id="dash-left"):
                    yield Static("[bold]Quick Start[/]", classes="section-title")
                    yield Static(
                        "  [#00f0ff][n][/] New Discover\n"
                        "  [#00f0ff][h][/] View History",
                        id="dash-quickstart",
                    )
                    yield Static("", id="dash-spacer-1")
                    yield Static("[bold]API Usage Today[/]", classes="section-title")
                    yield Static("Loading...", id="dash-usage")
                    yield Static("", id="dash-plan")

                # Right: recent sessions
                with Vertical(id="dash-right"):
                    yield Static("[bold]Recent Activity[/]", classes="section-title")
                    yield DataTable(id="dash-sessions", cursor_type="row")

        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#dash-sessions", DataTable)
        table.add_columns("When", "Query", "Threads", "Drafts")
        self.load_data()

    @work(exclusive=True)
    async def load_data(self) -> None:
        from redditrank_tui.api import RedditRankAPI
        api = RedditRankAPI()

        # Fetch usage
        try:
            usage = await api.get_usage()
            self._usage_data = usage
            today = usage.get("today", {})
            limits = usage.get("limits", {})
            tier = usage.get("tier", "free")

            disc_used = today.get("discovers", 0)
            disc_limit = limits.get("discovers_per_day", 10)
            draft_used = today.get("drafts", 0)
            draft_limit = limits.get("drafts_per_day", 5)

            disc_bar = _progress_bar(disc_used, disc_limit)
            draft_bar = _progress_bar(draft_used, draft_limit)

            self.query_one("#dash-usage", Static).update(
                f"  Discovers: {disc_bar} {disc_used}/{disc_limit}\n"
                f"  Drafts:    {draft_bar} {draft_used}/{draft_limit}"
            )
            self.query_one("#dash-plan", Static).update(
                f"\n  Plan: [bold]{tier.capitalize()}[/]"
            )
        except Exception as e:
            self.query_one("#dash-usage", Static).update(f"  [#ff003c]Error: {e}[/]")

        # Fetch recent sessions
        try:
            data = await api.list_sessions(limit=10)
            sessions = data.get("sessions", [])
            self._sessions = sessions

            table = self.query_one("#dash-sessions", DataTable)
            table.clear()
            for s in sessions:
                when = _relative_time(s.get("created_at", ""))
                query = s.get("keyword") or s.get("product_url") or s.get("product_description", "")
                if len(query) > 35:
                    query = query[:32] + "..."
                threads = str(s.get("threads_found", 0))
                # Draft count not in session list, show "-"
                table.add_row(when, query, threads, "-", key=s.get("id", ""))
        except Exception as e:
            self.query_one("#dash-sessions", DataTable).add_row("", f"Error: {e}", "", "")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Drill into a session's threads."""
        session_id = str(event.row_key.value) if event.row_key else None
        if session_id:
            from redditrank_tui.screens.threads import ThreadBrowserScreen
            self.app.push_screen(ThreadBrowserScreen(session_id=session_id))

    def action_new_discover(self) -> None:
        from redditrank_tui.screens.discover import DiscoverScreen
        self.app.push_screen(DiscoverScreen())

    def action_history(self) -> None:
        from redditrank_tui.screens.history import HistoryScreen
        self.app.push_screen(HistoryScreen())

    def action_settings(self) -> None:
        from redditrank_tui.screens.settings import SettingsScreen
        self.app.push_screen(SettingsScreen())

    def action_help(self) -> None:
        self.notify(
            "[n] New discover  [h] History  [s] Settings  [q] Quit",
            title="Hotkeys",
        )

    def action_quit(self) -> None:
        self.app.exit()


def _progress_bar(used: int, limit: int, width: int = 20) -> str:
    """ASCII progress bar."""
    if limit <= 0:
        return "[dim]N/A[/]"
    ratio = min(used / limit, 1.0)
    filled = int(ratio * width)
    empty = width - filled
    color = "#39ff14" if ratio < 0.7 else "#f9f002" if ratio < 0.9 else "#ff003c"
    return f"[{color}]{'█' * filled}{'░' * empty}[/]"


def _relative_time(iso: str) -> str:
    """Convert ISO timestamp to relative time string."""
    if not iso:
        return ""
    from datetime import datetime, timezone
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        delta = now - dt
        hours = delta.total_seconds() / 3600
        if hours < 1:
            return "just now"
        if hours < 24:
            return f"{int(hours)}h ago"
        days = int(hours / 24)
        if days == 1:
            return "yesterday"
        if days < 7:
            return f"{days}d ago"
        return f"{days // 7}w ago"
    except Exception:
        return iso[:10]
