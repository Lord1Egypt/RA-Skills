# eNSP Skill

> AI-powered eNSP topology file generator for Huawei network simulation.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This is an AI Agent Skill that generates native `.topo` files for [eNSP (Enterprise Network Simulation Platform)](https://support.huawei.com/enterprise/en/cloud-computing/ensp-pid-21602604), allowing you to quickly create network topology diagrams using natural language.

## Features

- **AI-Powered** - Describe your network in plain English, get a ready-to-use topology
- **Full Device Support** - Routers, switches, PCs, Cloud, wireless devices
- **Flexible Connections** - Ethernet (Copper), Serial, Auto-detect cables
- **Rich Annotations** - Area boxes, text labels, network segment annotations
- **Official Examples** - Pre-built topologies for RIP, OSPF, BGP and more

## Quick Start

1. Describe your network topology to the AI
2. Receive a `.topo` file
3. Open in eNSP and start simulating

## Supported Devices

| Category | Models |
|----------|--------|
| Routers | AR1220, AR2220 |
| Switches | S5700 |
| Endpoints | PC, Laptop, MCS, Server |
| Cloud | Cloud, AC6005, AP6050, STA |

## Project Structure

```
ensp-skills/
├── SKILL.md                    # AI Agent skill definition
├── references/
│   └── topo-reference.md       # .topo file format reference
├── examples/
│   ├── 1-1RIPv1&v2.topo        # RIP topology example
│   ├── 2-1Single-Area OSPF.topo
│   └── Multi-Area OSPF.topo
├── DEVELOPMENT.md               # Development notes
└── README.md
```

## Usage Example

```
User: Create a simple OSPF topology with 3 routers connected in a triangle
Agent: Generates ospf-triangle.topo
User: Opens in eNSP, configures OSPF, runs simulation
```

## License

MIT License
