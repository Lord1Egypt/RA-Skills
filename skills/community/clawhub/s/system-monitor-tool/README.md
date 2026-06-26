# System Monitor Skill

System resource monitoring for OpenClaw.

## Features

- ✅ CPU usage and info
- ✅ Memory monitoring
- ✅ Disk space analysis
- ✅ Network status
- ✅ Process listing
- ✅ Temperature (Linux)
- ✅ Watch mode (continuous)

## Usage

### System Overview
```bash
bash skills/system-monitor-1.0.0/scripts/monitor.sh status
```

### CPU
```bash
bash skills/system-monitor-1.0.0/scripts/monitor.sh cpu
```

### Memory
```bash
bash skills/system-monitor-1.0.0/scripts/monitor.sh memory
```

### Disk
```bash
bash skills/system-monitor-1.0.0/scripts/monitor.sh disk
```

### Network
```bash
bash skills/system-monitor-1.0.0/scripts/monitor.sh network
```

### Top Processes
```bash
bash skills/system-monitor-1.0.0/scripts/monitor.sh processes --top 10
```

### Watch Mode
```bash
bash skills/system-monitor-1.0.0/scripts/monitor.sh watch --interval 5
```

## Platform Support

| Feature | Linux | macOS | Windows |
|---------|-------|-------|---------|
| CPU     | ✅    | ✅    | ⚠️ Limited |
| Memory  | ✅    | ✅    | ⚠️ Limited |
| Disk    | ✅    | ✅    | ✅ |
| Network | ✅    | ✅    | ⚠️ Limited |
| Temp    | ✅    | ⚠️ Needs iStats | ❌ |

## License

MIT
