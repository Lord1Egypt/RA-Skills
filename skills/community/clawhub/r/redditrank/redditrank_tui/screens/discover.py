"""Discover screen: input + SSE pipeline progress."""

from textual import work
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Static, Input, Button, Footer, RadioButton, RadioSet


class DiscoverScreen(Screen):
    BINDINGS = [
        ("escape", "go_back", "Back"),
    ]

    def __init__(self):
        super().__init__()
        self._mode = "url"  # url or desc
        self._running = False

    def compose(self) -> ComposeResult:
        with Vertical(id="disc-root"):
            yield Static("[bold #00f0ff]NEW DISCOVER[/]", id="disc-title")

            with Horizontal(id="disc-mode"):
                yield RadioSet(
                    RadioButton("Paste URL", value=True, id="radio-url"),
                    RadioButton("Describe product", id="radio-desc"),
                    id="disc-radios",
                )

            yield Input(
                placeholder="https://yourproduct.com",
                id="disc-input",
            )

            with Horizontal(id="disc-actions"):
                yield Button("Run Discover", variant="primary", id="btn-discover")

            yield Static("", id="disc-pipeline")

        yield Footer()

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        inp = self.query_one("#disc-input", Input)
        if event.pressed.id == "radio-url":
            self._mode = "url"
            inp.placeholder = "https://yourproduct.com"
        else:
            self._mode = "desc"
            inp.placeholder = "Describe what your product does..."

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-discover" and not self._running:
            self.run_discover()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if not self._running:
            self.run_discover()

    @work(exclusive=True)
    async def run_discover(self) -> None:
        value = self.query_one("#disc-input", Input).value.strip()
        if not value:
            self.notify("Enter a URL or description", severity="warning")
            return

        self._running = True
        pipeline = self.query_one("#disc-pipeline", Static)
        btn = self.query_one("#btn-discover", Button)
        btn.disabled = True

        steps = {
            "scan": "Scanning...",
            "market": "Understanding market position...",
            "keywords": "Generating keywords...",
            "google": "Searching Google for Reddit threads...",
            "reddit": "Scanning Reddit for fresh conversations...",
            "rank": "Ranking opportunities...",
        }
        step_status: dict[str, str] = {k: "pending" for k in steps}
        keywords_found: list[str] = []
        analysis_info = ""
        google_count = 0
        reddit_count = 0
        final_data: dict | None = None

        def render_pipeline() -> str:
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

                # Extra info after certain steps
                if sid == "market" and st == "done" and analysis_info:
                    lines.append(f"    [#b967ff]{analysis_info}[/]")
                if sid == "keywords" and st != "pending" and keywords_found:
                    kw_str = ", ".join(keywords_found[:8])
                    lines.append(f"    [#00f0ff]{kw_str}[/]")
                if sid == "google" and st in ("active", "done"):
                    lines.append(f"    [dim]({google_count} found)[/]")
                if sid == "reddit" and st in ("active", "done"):
                    lines.append(f"    [dim]({reddit_count} found)[/]")

            return "\n".join(lines)

        pipeline.update(render_pipeline())

        from redditrank_tui.api import RedditRankAPI
        api = RedditRankAPI()

        try:
            kwargs = {}
            if self._mode == "url":
                kwargs["product_url"] = value
            else:
                kwargs["product_description"] = value

            async for event_type, data in api.discover_stream(**kwargs):
                if event_type == "step":
                    sid = data.get("id", "")
                    if sid in step_status:
                        # Mark all prior steps as done
                        found = False
                        for k in steps:
                            if k == sid:
                                found = True
                                step_status[k] = "active"
                            elif not found:
                                step_status[k] = "done"
                        pipeline.update(render_pipeline())

                elif event_type == "analysis":
                    name = data.get("product_name", "")
                    liner = data.get("one_liner", "")
                    analysis_info = f"{name}: {liner}" if name else ""
                    step_status["market"] = "done"
                    pipeline.update(render_pipeline())

                elif event_type == "keywords":
                    keywords_found = data.get("keywords", [])
                    step_status["keywords"] = "done"
                    pipeline.update(render_pipeline())

                elif event_type == "google":
                    threads = data.get("threads", [])
                    google_count = len(threads)
                    step_status["google"] = "done"
                    pipeline.update(render_pipeline())

                elif event_type == "reddit":
                    threads = data.get("threads", [])
                    reddit_count = len(threads)
                    step_status["reddit"] = "done"
                    pipeline.update(render_pipeline())

                elif event_type == "done":
                    for k in step_status:
                        step_status[k] = "done"
                    pipeline.update(render_pipeline())
                    final_data = data
                    break

                elif event_type == "error":
                    err = data.get("error", "Discovery failed")
                    pipeline.update(render_pipeline() + f"\n\n  [#ff003c]Error: {err}[/]")
                    self._running = False
                    btn.disabled = False
                    return

        except Exception as e:
            pipeline.update(render_pipeline() + f"\n\n  [#ff003c]Error: {e}[/]")
            self._running = False
            btn.disabled = False
            return

        self._running = False
        btn.disabled = False

        if final_data:
            # Combine google + reddit threads
            g_threads = final_data.get("google_threads", [])
            r_threads = final_data.get("reddit_threads", [])
            all_threads = g_threads + r_threads

            if all_threads:
                from redditrank_tui.screens.threads import ThreadBrowserScreen
                self.app.push_screen(
                    ThreadBrowserScreen(
                        threads=all_threads,
                        product_name=analysis_info.split(":")[0].strip() if analysis_info else "",
                        product_url=value if self._mode == "url" else "",
                        product_description=value if self._mode == "desc" else "",
                    )
                )
            else:
                pipeline.update(
                    render_pipeline() + "\n\n  [dim]No threads found. Try a different product.[/]"
                )

    def action_go_back(self) -> None:
        if not self._running:
            self.app.pop_screen()
