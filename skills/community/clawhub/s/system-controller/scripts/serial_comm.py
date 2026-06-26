#!/usr/bin/env python3
"""
Serial Communication - Communicate with Arduino and other serial devices.

Capabilities:
  - List available serial ports
  - Connect to a serial device
  - Send data (text or bytes)
  - Receive data (with timeout)
  - Continuous monitor mode
  - Auto-detect common baud rates

Requirements: pyserial (pip install pyserial)
"""

import sys
import json
import time
import subprocess
import os

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


def check_pyserial():
    """Check if pyserial is installed, install if not."""
    try:
        import serial
        import serial.tools.list_ports
        return True
    except ImportError:
        print("Installing pyserial...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pyserial", "-q"],
            stdout=subprocess.DEVNULL
        )
        try:
            import serial
            return True
        except ImportError:
            return False


def list_ports():
    """List all available serial ports."""
    if not check_pyserial():
        return '{"error":"Failed to install pyserial"}'
    
    import serial.tools.list_ports
    
    ports = []
    for port in serial.tools.list_ports.comports():
        ports.append({
            "device": port.device,
            "description": port.description,
            "hwid": port.hwid,
            "vendor": port.vid if port.vid else None,
            "product": port.pid if port.pid else None,
        })
    
    if not ports:
        return json.dumps({"info": "No serial ports found"}, ensure_ascii=False)
    return json.dumps(ports, indent=2, ensure_ascii=False)


def detect_baud_rate(port, timeout=2):
    """Try to detect the baud rate by testing common rates."""
    if not check_pyserial():
        return "ERROR: pyserial not available"
    
    import serial
    
    common_rates = [9600, 115200, 57600, 38400, 19200, 4800, 2400, 1200]
    
    for rate in common_rates:
        try:
            ser = serial.Serial(port, rate, timeout=timeout)
            ser.write(b'\n')
            time.sleep(0.5)
            response = ser.read(ser.in_waiting or 1)
            ser.close()
            if response:
                return json.dumps({
                    "detected_rate": rate,
                    "response_preview": response.decode('utf-8', errors='replace')[:100]
                })
        except Exception:
            continue
    
    return json.dumps({"detected_rate": 9600, "note": "Could not auto-detect, using default 9600"})


def send_data(port, data, baud_rate=9600, encoding="utf-8", newline=True):
    """Send data to a serial port."""
    if not check_pyserial():
        return "ERROR: pyserial not available"
    
    import serial
    
    try:
        ser = serial.Serial(port, baud_rate, timeout=2)
        payload = (data + '\n').encode(encoding) if newline else data.encode(encoding)
        ser.write(payload)
        ser.flush()
        ser.close()
        return f"OK: Sent {len(payload)} bytes to {port} at {baud_rate} baud"
    except serial.SerialException as e:
        return f"ERROR: {e}"


def receive_data(port, baud_rate=9600, timeout=2, max_bytes=1024, encoding="utf-8"):
    """Receive data from a serial port."""
    if not check_pyserial():
        return "ERROR: pyserial not available"
    
    import serial
    
    try:
        ser = serial.Serial(port, baud_rate, timeout=timeout)
        data = ser.read(max_bytes)
        ser.close()
        
        if data:
            try:
                text = data.decode(encoding)
            except UnicodeDecodeError:
                text = data.hex()
            return json.dumps({
                "bytes_received": len(data),
                "data": text,
                "hex": data.hex()[:200]
            }, ensure_ascii=False)
        else:
            return '{"info":"No data received within timeout"}'
    except serial.SerialException as e:
        return f"ERROR: {e}"


def send_and_receive(port, data, baud_rate=9600, timeout=2, encoding="utf-8"):
    """Send data and wait for response."""
    if not check_pyserial():
        return "ERROR: pyserial not available"
    
    import serial
    
    try:
        ser = serial.Serial(port, baud_rate, timeout=timeout)
        ser.write((data + '\n').encode(encoding))
        ser.flush()
        time.sleep(0.1)
        response = ser.read(ser.in_waiting or 1024)
        ser.close()
        
        try:
            text = response.decode(encoding)
        except UnicodeDecodeError:
            text = response.hex()
        
        return json.dumps({
            "sent": data,
            "received": text,
            "bytes": len(response)
        }, ensure_ascii=False)
    except serial.SerialException as e:
        return f"ERROR: {e}"


def monitor(port, baud_rate=9600, duration=10, encoding="utf-8"):
    """Monitor serial port output for a duration (outputs in real-time)."""
    if not check_pyserial():
        return "ERROR: pyserial not available"
    
    import serial
    
    try:
        ser = serial.Serial(port, baud_rate, timeout=0.1)
        print(f"Monitoring {port} at {baud_rate} baud for {duration}s...")
        print("--- Press Ctrl+C to stop ---")
        
        start = time.time()
        buffer = b""
        while time.time() - start < duration:
            if ser.in_waiting:
                chunk = ser.read(ser.in_waiting)
                buffer += chunk
                try:
                    print(chunk.decode(encoding), end="", flush=True)
                except UnicodeDecodeError:
                    print(chunk.hex(), flush=True)
            time.sleep(0.05)
        
        ser.close()
        print(f"\n--- Monitor ended. Total bytes: {len(buffer)} ---")
        return ""
    except KeyboardInterrupt:
        ser.close()
        print("\n--- Monitor stopped by user ---")
        return ""
    except serial.SerialException as e:
        return f"ERROR: {e}"


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Serial Communication")
    sub = parser.add_subparsers(dest="action")

    p_list = sub.add_parser("list", help="List serial ports")
    
    p_detect = sub.add_parser("detect", help="Detect baud rate")
    p_detect.add_argument("--port", type=str, required=True)
    
    p_send = sub.add_parser("send", help="Send data")
    p_send.add_argument("--port", type=str, required=True)
    p_send.add_argument("--data", type=str, required=True)
    p_send.add_argument("--baud", type=int, default=9600)
    p_send.add_argument("--no-newline", action="store_true")
    
    p_recv = sub.add_parser("receive", help="Receive data")
    p_recv.add_argument("--port", type=str, required=True)
    p_recv.add_argument("--baud", type=int, default=9600)
    p_recv.add_argument("--timeout", type=float, default=2)
    
    p_chat = sub.add_parser("chat", help="Send and receive")
    p_chat.add_argument("--port", type=str, required=True)
    p_chat.add_argument("--data", type=str, required=True)
    p_chat.add_argument("--baud", type=int, default=9600)
    
    p_mon = sub.add_parser("monitor", help="Monitor port")
    p_mon.add_argument("--port", type=str, required=True)
    p_mon.add_argument("--baud", type=int, default=9600)
    p_mon.add_argument("--duration", type=int, default=10)

    args = parser.parse_args()

    if args.action == "list":
        print(list_ports())
    elif args.action == "detect":
        print(detect_baud_rate(args.port))
    elif args.action == "send":
        print(send_data(args.port, args.data, args.baud, newline=not args.no_newline))
    elif args.action == "receive":
        print(receive_data(args.port, args.baud, args.timeout))
    elif args.action == "chat":
        print(send_and_receive(args.port, args.data, args.baud))
    elif args.action == "monitor":
        monitor(args.port, args.baud, args.duration)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
