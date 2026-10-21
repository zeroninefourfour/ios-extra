#!/usr/bin/env python3
"""Non-root UDP log listener for sweet USB Ethernet (192.168.7.1:5140)."""
import os
import socket
import sys
import time

def main():
    log_path = sys.argv[1] if len(sys.argv) > 1 else "sweet-live.log"
    os.makedirs(os.path.dirname(os.path.abspath(log_path)), exist_ok=True)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 5140))
    sock.settimeout(2.0)
    print(f"Listening on UDP 5140 -> {log_path}...", flush=True)

    with open(log_path, "ab", buffering=0) as f:
        start_time = time.monotonic()
        while True:
            try:
                data, addr = sock.recvfrom(65535)
                f.write(data)
                text = data.decode('utf-8', errors='replace')
                for line in text.splitlines():
                    if any(tag in line for tag in ("SWEET", "panic", "SweetBattery", "AppleCLCD", "IOLog")):
                        print(line, flush=True)
            except socket.timeout:
                if time.monotonic() - start_time > 86400:
                    break
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    main()
