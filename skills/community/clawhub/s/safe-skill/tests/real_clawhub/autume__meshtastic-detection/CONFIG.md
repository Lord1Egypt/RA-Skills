# Meshtastic Detection Configuration

## Device

```yaml
# 使用 ls /dev/cu.usb* 查看实际路径
serial_port: /dev/cu.usbmodem1CDBD4A896441
```

## Storage

```yaml
data_dir: ./data
```

## Notification

```yaml
notification:
  channel: "feishu"
  monitor_interval_ms: 60000
```

All `DETECTION_SENSOR_APP` events are high-priority alerts. No rules needed — every detection triggers an immediate notification.
