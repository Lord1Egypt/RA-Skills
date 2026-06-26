"""First-run onboarding wizard."""

from textual import work
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Static, Input, Button, Label


class OnboardingScreen(ModalScreen[str | None]):
    """Collects API key or runs registration. Returns the API key string or None."""

    BINDINGS = [("escape", "cancel", "Cancel")]

    def compose(self) -> ComposeResult:
        with Vertical(id="onboard-box"):
            yield Static(
                "[bold #00f0ff]REDDITRANK[/]\n"
                "Find Reddit threads ranking on Google.\n"
                "Generate stealth replies that drive traffic.",
                id="onboard-header",
            )
            yield Static("", id="onboard-divider")
            yield Label("Do you have an API key?", id="onboard-prompt")
            with Horizontal(id="onboard-buttons"):
                yield Button("I have a key", variant="primary", id="btn-have-key")
                yield Button("Get one free", variant="default", id="btn-register")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-have-key":
            self.app.push_screen(EnterKeyScreen(), callback=self._on_key)
        elif event.button.id == "btn-register":
            self.app.push_screen(RegisterScreen(), callback=self._on_key)

    def _on_key(self, key: str | None) -> None:
        if key:
            self.dismiss(key)

    def action_cancel(self) -> None:
        self.dismiss(None)


class EnterKeyScreen(ModalScreen[str | None]):
    """Paste an existing API key."""

    BINDINGS = [("escape", "pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        with Vertical(id="key-box"):
            yield Label("Paste your API key:")
            yield Input(placeholder="rr_sk_...", id="key-input", password=True)
            yield Static("", id="key-status")
            with Horizontal(id="key-actions"):
                yield Button("Validate", variant="primary", id="btn-validate")
                yield Button("Back", id="btn-back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-validate":
            self.validate_key()
        elif event.button.id == "btn-back":
            self.dismiss(None)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.validate_key()

    @work(exclusive=True)
    async def validate_key(self) -> None:
        key = self.query_one("#key-input", Input).value.strip()
        if not key:
            self.query_one("#key-status", Static).update("[#ff003c]Enter a key[/]")
            return

        status = self.query_one("#key-status", Static)
        status.update("[#b967ff]Validating...[/]")

        from redditrank_tui.api import RedditRankAPI
        api = RedditRankAPI(api_key=key)
        try:
            result = await api.validate_key()
            if result.get("valid"):
                status.update(f"[#39ff14]Valid! Tier: {result.get('tier', 'free')}[/]")
                from redditrank_tui.config import save_api_key
                save_api_key(key)
                self.dismiss(key)
            else:
                status.update(f"[#ff003c]{result.get('error', 'Invalid key')}[/]")
        except Exception as e:
            status.update(f"[#ff003c]Connection error: {e}[/]")


class RegisterScreen(ModalScreen[str | None]):
    """Email registration flow."""

    BINDINGS = [("escape", "pop_screen", "Back")]

    def __init__(self):
        super().__init__()
        self._email = ""
        self._phase = "email"  # email -> code

    def compose(self) -> ComposeResult:
        with Vertical(id="reg-box"):
            yield Label("Enter your email to get a free API key:", id="reg-label")
            yield Input(placeholder="you@company.com", id="reg-input")
            yield Static("", id="reg-status")
            with Horizontal(id="reg-actions"):
                yield Button("Send Code", variant="primary", id="btn-send")
                yield Button("Back", id="btn-back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-send":
            self.handle_submit()
        elif event.button.id == "btn-back":
            self.dismiss(None)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.handle_submit()

    @work(exclusive=True)
    async def handle_submit(self) -> None:
        inp = self.query_one("#reg-input", Input)
        status = self.query_one("#reg-status", Static)
        value = inp.value.strip()

        from redditrank_tui.api import RedditRankAPI
        api = RedditRankAPI()

        if self._phase == "email":
            if not value or "@" not in value:
                status.update("[#ff003c]Enter a valid email[/]")
                return

            self._email = value.lower()
            status.update("[#b967ff]Sending verification code...[/]")

            try:
                result = await api.register(self._email)
                if result.get("error"):
                    status.update(f"[#ff003c]{result['error']}[/]")
                    return
                status.update("[#39ff14]Code sent! Check your email.[/]")
                self._phase = "code"
                self.query_one("#reg-label", Label).update("Enter the 6-digit code from your email:")
                inp.placeholder = "123456"
                inp.value = ""
                inp.focus()
                self.query_one("#btn-send", Button).label = "Verify"
            except Exception as e:
                status.update(f"[#ff003c]Error: {e}[/]")

        elif self._phase == "code":
            if not value or len(value) != 6:
                status.update("[#ff003c]Enter the 6-digit code[/]")
                return

            status.update("[#b967ff]Verifying...[/]")
            try:
                result = await api.verify(self._email, value)
                if result.get("error"):
                    status.update(f"[#ff003c]{result['error']}[/]")
                    return
                api_key = result.get("api_key", "")
                if api_key:
                    from redditrank_tui.config import save_api_key
                    save_api_key(api_key)
                    status.update("[#39ff14]API key created and saved![/]")
                    self.dismiss(api_key)
                else:
                    status.update("[#ff003c]Unexpected response[/]")
            except Exception as e:
                status.update(f"[#ff003c]Error: {e}[/]")
