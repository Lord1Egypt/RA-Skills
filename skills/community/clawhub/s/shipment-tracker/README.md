# Shipment Tracker

[![ClawHub](https://img.shields.io/badge/ClawHub-shipment--tracker-blue)](https://clawhub.ai/pfrederiksen/shipment-tracker)
[![Version](https://img.shields.io/badge/version-1.0.0-green)]()

An [OpenClaw](https://openclaw.ai) skill for tracking packages across multiple carriers. Auto-detects carrier from tracking number patterns and checks delivery status using a hybrid approach (direct HTTP + browser-use fallback).

## Features

- 📦 **Multi-carrier** — USPS, UPS, FedEx, DHL, Amazon, OnTrac, LaserShip
- 🔍 **Auto-detection** — identifies carrier from tracking number pattern
- 🔗 **Tracking URLs** — generates correct tracking page link per carrier
- 🌐 **Hybrid status** — tries direct HTTP first, recommends browser-use for JS-heavy sites
- 📋 **Markdown format** — reads shipments from a simple markdown table
- 🔒 **Clean security** — no subprocess, no shell, no file writes, stdlib only

## Installation

```bash
clawhub install shipment-tracker
```

## Usage

```bash
# Check all active shipments
python3 scripts/shipment_tracker.py memory/shipments.md

# JSON output
python3 scripts/shipment_tracker.py memory/shipments.md --format json

# Detect carrier from tracking number
python3 scripts/shipment_tracker.py --detect 1Z999AA10123456784
```

## Requirements

- Python 3.10+
- Outbound HTTPS to carrier tracking sites
- browser-use (optional, for full tracking on JS-heavy sites)

## License

MIT

## Links

- [ClawHub](https://clawhub.ai/pfrederiksen/shipment-tracker)
- [OpenClaw](https://openclaw.ai)
