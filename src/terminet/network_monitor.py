from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label
from textual.containers import Horizontal
from textual import events


class NetworkMonitorApp(App):
    """Class for setting up textual App."""

    BINDINGS = [("d", "toggle_dark", "Toggle Dark Mode")]
    CSS_PATH = "styles.tcss"

    def compose(self) -> ComposeResult:
        """Create child widgets for App."""
        yield Header()
        with Horizontal(id="footer-outer"):
            with Horizontal(id="footer-inner"):
                yield Footer()
            yield Label("Press 'ctrl-q' to quit application", id="right-label")

    def action_toggle_dark(self) -> None:
        """Switch between light and dark theme."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    NetworkMonitorApp().run()
