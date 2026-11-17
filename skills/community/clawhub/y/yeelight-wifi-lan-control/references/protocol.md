# WiFi Protocol Reference

Source: [Yeelight WiFi Light Inter-Operation Specification](https://www.yeelight.com/download/Yeelight_Inter-Operation_Spec.pdf), 23 pages, inspected 2026-08-14, SHA-256 `9f454a97ca4730ac7fe97990862bb9ad1b7f2b94aa2b0b2726a13961f1586bd2`.

## Transport

- Discovery: UDP multicast `239.255.255.250:1982`, CRLF M-SEARCH with `ST: wifi_bulb`.
- Control: TCP JSON messages terminated by `\r\n`, normally port `55443`.
- Replies correlate by integer `id`; notifications use `method: "props"`.
- Device limits: four simultaneous TCP connections, 60 commands/minute per normal
  connection, 144 LAN commands/minute total.

## Methods

The catalog contains all 35 unique methods: `get_prop`; foreground absolute,
toggle/default, flow/scene, timer, adjust, music, and name methods; background
counterparts; `dev_toggle`; and foreground/background relative adjustment methods.
Only advertised `support` tokens enable an operation.

## Common Values

- CT: 1700..6500 K. RGB command: 0..16777215. HSV hue: 0..359, saturation: 0..100.
- Brightness: 1..100. Effects: `sudden` or `smooth`; smooth duration >=30 ms.
- Flow duration >=50 ms; modes 1 RGB, 2 CT, 7 sleep; brightness -1 or 1..100.
- Flow stop action: 0 restore, 1 keep, 2 power off; loop count 0 means forever.
- Scene classes: `color`, `hsv`, `ct`, `cf`, `auto_delay_off`.
- Relative percentages: -100..100. Device name: at most 64 bytes.

The PDF has known inconsistencies: optional fourth power mode, the
`auto_dealy_off` prose typo, an RGB lower-bound mismatch, and malformed examples.
The runtime follows the catalog's explicit command rules and tests these differences.
