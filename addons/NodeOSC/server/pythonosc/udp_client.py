"""Client to send OSC datagrams to an OSC server via UDP."""

from collections.abc import Iterable
import socket

from .osc_message_builder import OscMessageBuilder
from pythonosc import osc_message

from typing import Union


class UDPClient(object):
    """OSC client to send OscMessages or OscBundles via UDP."""

    def __init__(self, address: str, port: int, allow_broadcast: bool = False):
        """Initialize the client.

        As this is UDP it will not actually make any attempt to connect to the
        given server at ip:port until the send() method is called.
        """
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setblocking(0)
        if allow_broadcast:
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._address = address
        self._port = port

    def send(self, content: osc_message.OscMessage) -> None:
        """Sends an OscBundle or OscMessage to the server."""
        self._sock.sendto(content.dgram, (self._address, self._port))


class SimpleUDPClient(UDPClient):
    """Simple OSC client with a `send_message` method."""

    def send_message(self, address: str, value: Union[int, float, bytes, str, bool, tuple, list]) -> None:
        """Compose an OSC message and send it."""
        builder = OscMessageBuilder(address=address)
        if not isinstance(value, Iterable) or isinstance(value, (str, bytes)):
            values = [value]
        else:
            values = value
        for val in values:
            builder.add_arg(val)
        msg = builder.build()
        self.send(msg)
