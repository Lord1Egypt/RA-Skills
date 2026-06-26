"""Settings screen."""

import webbrowser

from textual import work
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Static, Footer

from redditrank_tui.config import load_api_key, mask_key, API_BASE


class SettingsScreen(Screen):
    BINDINGS = [
        ("escape", "go_back", "Back"),
        ("u", "upgrade", "Upgrade"),
    ]

    def compose(self) -> ComposeResult:
        key = load_api_key() or ""
        masked = mask_key(key) if key else "[#ff003c]Not set[/]"

        with Vertical(id="settings-root"):
            yield Static("[bold #00f0ff]SETTINGS[/]", id="settings-title")
            yield Static("", id="settings-info")
            yield Static(
                "\n  [#00f0ff][u][/] Upgrade plan",
                id="settings-actions",
            )

        yield Footer()

    def on_mount(self) -> None:
        self.load_info()

    @work(exclusive=True)
    async def load_info(self) -> None:
        key = load_api_key() or ""
        masked = mask_key(key) if key else "[#ff003c]Not set[/]"

        info_lines = [
            f"  API Key:    {masked}",
            f"  API Base:   {API_BASE}",
        ]

        # Try to get account info
        if key:
            from redditrank_tui.api import RedditRankAPI
            api = RedditRankAPI(api_key=key)
            try:
                usage = await api.get_usage()
                tier = usage.get("tier", "free")
                email = ""
                # Try validate to get email
                val = await api.validate_key()
                if val.get("valid"):
                    pass  # email not in validate response currently
                info_lines.insert(1, f"  Plan:       {tier.capitalize()}")
            except Exception:
                info_lines.insert(1, "  Plan:       [dim]Unable to fetch[/]")

        self.query_one("#settings-info", Static).update("\n".join(info_lines))

    def action_upgrade(self) -> None:
        webbrowser.open("https://clawagents.dev/reddit-rank")
        self.notify("Opened pricing page in browser")

    def action_go_back(self) -> None:
        self.app.pop_screen()
