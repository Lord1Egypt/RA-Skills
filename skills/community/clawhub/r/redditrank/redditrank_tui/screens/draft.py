"""Draft generation screen with SSE pipeline progress."""

import webbrowser

from textual import work
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Static, Button, Footer


class DraftScreen(Screen):
    BINDINGS = [
        ("escape", "go_back", "Close"),
        ("c", "copy_draft", "Copy"),
        ("o", "open_thread", "Open Thread"),
        ("r", "regenerate", "Regenerate"),
    ]

    def __init__(
        self,
        thread: dict,
        product_name: str = "",
        product_url: str = "",
        product_description: str = "",
    ):
        super().__init__()
        self._thread = thread
        self._product_name = product_name
        self._product_url = product_url
        self._product_description = product_description
        self._draft_text = ""
        self._phase = "loading"  # loading | done

    def compose(self) -> ComposeResult:
        title = self._thread.get("title", "")
        if len(title) > 60:
            title = title[:57] + "..."
        sub = self._thread.get("subreddit", "")

        with Vertical(id="draft-root"):
            yield Static(
                f"[bold #ff4500]GENERATING REPLY[/]\n"
                f"[bold]{title}[/]\n"
                f"[dim]r/{sub}[/]",
                id="draft-header",
            )
            yield Static("", id="draft-pipeline")
            yield Static("", id="draft-result")

            with Horizontal(id="draft-actions"):
                yield Button("Copy Draft", variant="primary", id="btn-copy", disabled=True)
                yield Button("Open Thread", id="btn-open", disabled=True)
                yield Button("Regenerate", id="btn-regen", disabled=True)
                yield Button("Close", id="btn-close")

        yield Footer()

    def on_mount(self) -> None:
        self.generate_draft()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-copy":
            self.action_copy_draft()
        elif event.button.id == "btn-open":
            self.action_open_thread()
        elif event.button.id == "btn-regen":
            self.action_regenerate()
        elif event.button.id == "btn-close":
            self.action_go_back()

    @work(exclusive=True)
    async def generate_draft(self) -> None:
        pipeline = self.query_one("#draft-pipeline", Static)
        result_widget = self.query_one("#draft-result", Static)

        steps = {
            "fetch": "Fetching thread context...",
            "category": "Detecting category...",
            "fit": "Scoring product fit...",
            "draft": "Drafting reply...",
            "qa": "Running QA pipeline...",
        }
        step_status: dict[str, str] = {k: "pending" for k in steps}
        extra_info: dict[str, str] = {}

        def render() -> str:
            lines = []
            for sid, label in steps.items():
                st = step_status[sid]
                if st == "done":
                    icon = "[#39ff14]✓[/]"
                    text = f"[#39ff14]{label}[/]"
                elif st == "active":
                    icon = "[#ff4500]●[/]"
                    text = f"[bold]{label}[/]"
                else:
                    icon = "[dim]○[/]"
                    text = f"[dim]{label}[/]"
                lines.append(f"  {icon} {text}")
                if sid in extra_info:
                    lines.append(f"    [#b967ff]{extra_info[sid]}[/]")
            return "\n".join(lines)

        pipeline.update(render())

        from redditrank_tui.api import RedditRankAPI
        api = RedditRankAPI()

        try:
            async for event_type, data in api.draft_stream(
                thread_url=self._thread.get("url", ""),
                product_name=self._product_name,
                product_url=self._product_url,
                product_description=self._product_description,
            ):
                if event_type == "step":
                    sid = data.get("id", "")
                    if sid in step_status:
                        found = False
                        for k in steps:
                            if k == sid:
                                found = True
                                step_status[k] = "active"
                            elif not found:
                                step_status[k] = "done"
                        pipeline.update(render())

                elif event_type == "thread":
                    step_status["fetch"] = "done"
                    pipeline.update(render())

                elif event_type == "category":
                    cat = data.get("category", "")
                    extra_info["category"] = cat
                    step_status["category"] = "done"
                    pipeline.update(render())

                elif event_type == "fit":
                    score = data.get("score", 0)
                    mode = data.get("mode", "")
                    mode_label = "product mention" if mode == "product_drop" else "value only"
                    extra_info["fit"] = f"fit {score}/10 · {mode_label}"
                    step_status["fit"] = "done"
                    pipeline.update(render())

                elif event_type == "draft_preview":
                    step_status["draft"] = "done"
                    pipeline.update(render())

                elif event_type == "qa":
                    composite = data.get("composite", 0)
                    verdict = data.get("verdict", "")
                    attempts = data.get("attempts", 1)
                    info = f"QA {composite}/10 · {verdict}"
                    if attempts > 1:
                        info += f" · revised {attempts - 1}x"
                    extra_info["qa"] = info
                    step_status["qa"] = "done"
                    pipeline.update(render())

                elif event_type == "done":
                    for k in step_status:
                        step_status[k] = "done"
                    pipeline.update(render())

                    self._draft_text = data.get("draft", "")
                    mode = data.get("mode", "")
                    fit = data.get("fit_score", 0)
                    qa = data.get("qa", {})
                    composite = qa.get("composite", 0)
                    word_count = len(self._draft_text.split())
                    mode_label = "product mention" if mode == "product_drop" else "value only"

                    result_widget.update(
                        f"\n[bold #00f0ff]Draft Ready[/] · "
                        f"[dim]{mode_label} · fit {fit}/10 · QA {composite}/10 · "
                        f"{word_count} words[/]\n\n"
                        f"{self._draft_text}"
                    )

                    self._phase = "done"
                    self.query_one("#btn-copy", Button).disabled = False
                    self.query_one("#btn-open", Button).disabled = False
                    self.query_one("#btn-regen", Button).disabled = False

                    self.query_one("#draft-header", Static).update(
                        f"[bold #39ff14]AI DRAFT READY[/]\n"
                        f"[bold]{self._thread.get('title', '')[:60]}[/]\n"
                        f"[dim]r/{self._thread.get('subreddit', '')}[/]"
                    )
                    break

                elif event_type == "error":
                    err = data.get("error", "Draft failed")
                    pipeline.update(render() + f"\n\n  [#ff003c]Error: {err}[/]")
                    self.query_one("#btn-close", Button).disabled = False
                    return

        except Exception as e:
            pipeline.update(f"  [#ff003c]Error: {e}[/]")

    def action_copy_draft(self) -> None:
        if self._draft_text:
            import pyperclip
            try:
                pyperclip.copy(self._draft_text)
                self.notify("Copied to clipboard!", severity="information")
            except Exception:
                self.notify("Copy failed. Install pyperclip or xclip.", severity="warning")

    def action_open_thread(self) -> None:
        url = self._thread.get("url", "")
        if url:
            webbrowser.open(url)
            self.notify("Opened in browser")

    def action_regenerate(self) -> None:
        if self._phase == "done":
            self._phase = "loading"
            self._draft_text = ""
            self.query_one("#draft-result", Static).update("")
            self.query_one("#btn-copy", Button).disabled = True
            self.query_one("#btn-regen", Button).disabled = True
            self.query_one("#draft-header", Static).update(
                f"[bold #ff4500]REGENERATING...[/]\n"
                f"[bold]{self._thread.get('title', '')[:60]}[/]\n"
                f"[dim]r/{self._thread.get('subreddit', '')}[/]"
            )
            self.generate_draft()

    def action_go_back(self) -> None:
        self.app.pop_screen()
