#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os
import logging

import zmq

logger = logging.getLogger("relay")

if not logger.hasHandlers():
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(asctime)s: %(levelname)s] %(message)s"))
    logger.addHandler(handler)

try:
    INTERNAL_PORT = int(os.getenv("INTERNAL_SOCKET_PORT"))
except Exception:
    INTERNAL_PORT = 5000
try:
    SOCKET_PORT = int(os.getenv("SOCKET_PORT"))
except Exception:
    SOCKET_PORT = 6000
try:
    EVENTS = os.getenv("EVENTS").split(",")
except Exception:
    EVENTS = []
    logger.error(f"unable to parse events list. Defaulting to {EVENTS}")


def main():
    context = zmq.Context()

    public_uri = f"tcp://*:{SOCKET_PORT}"
    logger.info(f"binding to {public_uri}")
    public_server = context.socket(zmq.PUB)
    public_server.bind(public_uri)

    private_uri = f"tcp://*:{INTERNAL_PORT}"
    logger.info(f"binding to {private_uri}")
    private_server = context.socket(zmq.SUB)
    private_server.bind(private_uri)
    for event in EVENTS:
        logger.debug(f"subscribing to topic `{event}`")
        private_server.setsockopt_string(zmq.SUBSCRIBE, event)

    while True:
        received_string = private_server.recv_string()
        logger.info(f"[FORWARDING] {received_string}")
        public_server.send_string(received_string)


if __name__ == "__main__":
    main()
