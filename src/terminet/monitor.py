import asyncio
import threading
from textual.containers import HorizontalGroup
from textual.widgets import Button, Input
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
        self.__iface = Input(
            placeholder="Enter your internet interface (e.g., eth0, wlan0)"
        )
        self.__protocol_map = {
            1: "ICMP", 6: "TCP", 17: "UDP", 58: "ICMPv6", 132: "SCTP"
        }

    def compose(self) -> ComposeResult:
        """Create buttons for app."""
        yield self.__iface
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events for starting and stopping app."""
        btn_event = event.button.id
        if btn_event == "start":
            if not self.__running:
                asyncio.create_task(self.start_sniffing())
                self.app.notify("Starting packet capture")
                self.add_class("started")
        elif btn_event == "stop":
            self.__running = False
            self.app.notify("Stopping packet capture")
            self.remove_class("started")

    async def start_sniffing(self) -> None:
        """Start sniffing network packets in seperate thread."""
        self.__running = True
        self.__sniffing_thread = threading.Thread(
            target=self.sniff_packets,
            daemon=True
        )
        self.__sniffing_thread.start()

    def sniff_packets(self) -> None:
        """Sniff packets using Scapy sniff on the interface provided by the user."""
        interface = self.__iface.value.strip()
        try:
            # Use specified interface if provided.
            if interface:
                self.app.notify(f"Sniffing on interface: {interface}")
            else:
                default_interface = "eth0"
                self.app.notify(
                    f"No interface specified, using default {default_interface}")
        except Exception as e:
            self.app.notify(f"Error: ", e)
            self.__running = False
