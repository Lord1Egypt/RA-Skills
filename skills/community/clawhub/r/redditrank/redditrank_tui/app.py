"""RedditRank TUI — main application."""

from textual.app import App, ComposeResult
from textual.widgets import Footer

from redditrank_tui.theme import cyberpunk
from redditrank_tui.config import load_api_key, save_api_key


class RedditRankApp(App):
    """RedditRank terminal interface."""

    TITLE = "RedditRank"
    SUB_TITLE = "Find Reddit threads. Generate stealth replies."
    CSS_PATH = "redditrank.tcss"

    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self.register_theme(cyberpunk)
        self.theme = "cyberpunk"

        key = load_api_key()
        if key:
            self._launch_dashboard()
        else:
            self._launch_onboarding()

    def _launch_dashboard(self) -> None:
        from redditrank_tui.screens.dashboard import DashboardScreen
        self.push_screen(DashboardScreen())

    def _launch_onboarding(self) -> None:
        from redditrank_tui.screens.onboarding import OnboardingScreen

        def on_result(key: str | None) -> None:
            if key:
                save_api_key(key)
                self._launch_dashboard()
            else:
                self.exit()

        self.push_screen(OnboardingScreen(), callback=on_result)
