from textual.containers import HorizontalGroup
from textual.widgets import Button
from scapy.all import IP, TCP, UDP, sniff
from network_table import NetworkTable
from textual.app import ComposeResult


class Monitor(HorizontalGroup):
    """Class for maintaining textual buttons and handling the necessities
       for reading network data."""

    def __init__(self, network_table: NetworkTable):
        super().__init__()
        self.__network_table = network_table
        self.__sniffing_thread = None
        self.__running = False
        self.__protocol_map = {
            1: "ICMP", 6: "TCP", 17: "UDP", 58: "ICMPv6", 132: "SCTP"
        }

    def compose(self) -> ComposeResult:
        """Create buttons for app."""
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events for starting and stopping app."""
        btn_event = event.button.id
        if btn_event == "start":
            if not self.__running:
                self.__running = True
                self.app.notify("Starting packet capture")
                self.add_class("started")
        elif btn_event == "stop":
            self.__running = False
            self.app.notify("Stopping packet capture")
            self.remove_class("started")
