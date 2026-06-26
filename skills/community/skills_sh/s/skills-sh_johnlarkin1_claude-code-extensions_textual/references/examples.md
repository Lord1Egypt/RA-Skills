# Textual Complete Examples

## Table of Contents
- [Calculator App](#calculator-app)
- [Animated Sidebar](#animated-sidebar)
- [Async Data Fetching](#async-data-fetching)
- [Multi-Screen App](#multi-screen-app)
- [Data Table App](#data-table-app)

## Calculator App

### calculator.py
```python
from decimal import Decimal
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import var
from textual.widgets import Button, Digits

class CalculatorApp(App):
    CSS_PATH = "calculator.tcss"

    numbers = var("0")
    left = var(Decimal("0"))
    operator = var("plus")

    def watch_numbers(self, value: str) -> None:
        self.query_one("#numbers", Digits).update(value)

    def compose(self) -> ComposeResult:
        with Container(id="calculator"):
            yield Digits(id="numbers")
            yield Button("AC", id="ac", variant="primary")
            yield Button("7", id="number-7", classes="number")
            yield Button("8", id="number-8", classes="number")
            yield Button("9", id="number-9", classes="number")
            yield Button("+", id="plus", variant="warning")
            yield Button("4", id="number-4", classes="number")
            yield Button("5", id="number-5", classes="number")
            yield Button("6", id="number-6", classes="number")
            yield Button("-", id="minus", variant="warning")
            yield Button("1", id="number-1", classes="number")
            yield Button("2", id="number-2", classes="number")
            yield Button("3", id="number-3", classes="number")
            yield Button("=", id="equals", variant="warning")
            yield Button("0", id="number-0", classes="number")

    @on(Button.Pressed, ".number")
    def number_pressed(self, event: Button.Pressed) -> None:
        number = event.button.id.partition("-")[-1]
        self.numbers = self.numbers.lstrip("0") + number

    @on(Button.Pressed, "#ac")
    def clear(self) -> None:
        self.numbers = "0"
        self.left = Decimal("0")

    @on(Button.Pressed, "#plus,#minus")
    def operator_pressed(self, event: Button.Pressed) -> None:
        self.left = Decimal(self.numbers)
        self.operator = event.button.id
        self.numbers = "0"

    @on(Button.Pressed, "#equals")
    def equals_pressed(self) -> None:
        right = Decimal(self.numbers)
        if self.operator == "plus":
            result = self.left + right
        else:
            result = self.left - right
        self.numbers = str(result)

if __name__ == "__main__":
    CalculatorApp().run()
```

### calculator.tcss
```css
#calculator {
    layout: grid;
    grid-size: 4;
    grid-gutter: 1 2;
}

#numbers {
    column-span: 4;
    height: 3;
    background: $panel;
    content-align: right middle;
}

#number-0 {
    column-span: 2;
}

Button {
    width: 100%;
    height: 100%;
}
```

## Animated Sidebar

```python
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Footer, Label, Button

class Sidebar(Widget):
    DEFAULT_CSS = """
    Sidebar {
        width: 30;
        layer: sidebar;
        dock: left;
        offset-x: -100%;
        background: $primary;
        transition: offset 200ms;
        padding: 1;

        &.-visible {
            offset-x: 0;
        }
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("Sidebar Content")
        yield Button("Option 1")
        yield Button("Option 2")
        yield Button("Option 3")

class SidebarApp(App):
    CSS = """
    Screen {
        layers: base sidebar;
    }
    #main {
        padding: 2;
    }
    """

    BINDINGS = [("s", "toggle_sidebar", "Toggle Sidebar")]

    show_sidebar = reactive(False)

    def compose(self) -> ComposeResult:
        yield Sidebar()
        with Vertical(id="main"):
            yield Label("Press 's' to toggle sidebar")
        yield Footer()

    def action_toggle_sidebar(self) -> None:
        self.show_sidebar = not self.show_sidebar

    def watch_show_sidebar(self, show: bool) -> None:
        self.query_one(Sidebar).set_class(show, "-visible")

if __name__ == "__main__":
    SidebarApp().run()
```

## Async Data Fetching

```python
from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Input, Static, Header, Footer
from textual.containers import VerticalScroll
import httpx

class WeatherApp(App):
    CSS = """
    #weather {
        height: 1fr;
        padding: 1;
        background: $surface;
    }
    Input {
        margin: 1;
    }
    """

    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Enter city name and press Enter")
        with VerticalScroll():
            yield Static("Enter a city to fetch weather", id="weather")
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.value:
            self.query_one("#weather").update("Loading...")
            self.fetch_weather(event.value)

    @work(exclusive=True)
    async def fetch_weather(self, city: str) -> None:
        url = f"https://wttr.in/{city}?format=3"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                weather = response.text
        except Exception as e:
            weather = f"Error: {e}"

        if city == self.query_one(Input).value:
            self.query_one("#weather").update(weather)

if __name__ == "__main__":
    WeatherApp().run()
```

## Multi-Screen App

```python
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Static, Header, Footer, Input
from textual.containers import Vertical, Center

class WelcomeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            with Vertical():
                yield Static("Welcome to My App", classes="title")
                yield Button("Start", id="start", variant="primary")
                yield Button("Settings", id="settings")
                yield Button("Quit", id="quit", variant="error")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            self.app.push_screen("main")
        elif event.button.id == "settings":
            self.app.push_screen("settings")
        elif event.button.id == "quit":
            self.app.exit()

class MainScreen(Screen):
    BINDINGS = [("escape", "go_back", "Back")]

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Static("Main Application Content")
            yield Static("Press ESC to go back")
        yield Footer()

    def action_go_back(self) -> None:
        self.app.pop_screen()

class SettingsScreen(Screen):
    BINDINGS = [("escape", "go_back", "Back")]

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Static("Settings")
            yield Input(placeholder="Username")
            yield Input(placeholder="Email")
            yield Button("Save", variant="primary")
        yield Footer()

    def action_go_back(self) -> None:
        self.app.pop_screen()

class MultiScreenApp(App):
    CSS = """
    .title {
        text-style: bold;
        text-align: center;
        padding: 1;
    }
    Button {
        margin: 1;
        width: 20;
    }
    """

    SCREENS = {
        "welcome": WelcomeScreen,
        "main": MainScreen,
        "settings": SettingsScreen,
    }

    def on_mount(self) -> None:
        self.push_screen("welcome")

if __name__ == "__main__":
    MultiScreenApp().run()
```

## Data Table App

```python
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Header, Footer, Static
from textual.containers import Vertical

ROWS = [
    ("Alice", "alice@example.com", "Admin"),
    ("Bob", "bob@example.com", "User"),
    ("Charlie", "charlie@example.com", "User"),
    ("Diana", "diana@example.com", "Moderator"),
    ("Eve", "eve@example.com", "User"),
]

class DataTableApp(App):
    CSS = """
    DataTable {
        height: 1fr;
    }
    #status {
        height: 1;
        background: $surface;
        padding: 0 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("a", "add_row", "Add Row"),
        ("d", "delete_row", "Delete Row"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable()
        yield Static("Select a row", id="status")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Name", "Email", "Role")
        table.add_rows(ROWS)
        table.cursor_type = "row"

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        row_data = event.data_table.get_row(event.row_key)
        self.query_one("#status").update(f"Selected: {row_data[0]}")

    def action_add_row(self) -> None:
        table = self.query_one(DataTable)
        table.add_row("New User", "new@example.com", "User")

    def action_delete_row(self) -> None:
        table = self.query_one(DataTable)
        if table.row_count > 0:
            row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
            table.remove_row(row_key)

if __name__ == "__main__":
    DataTableApp().run()
```
