---
name: unit-converter
description: "常用单位换算：长度/重量/温度/速度/存储/面积/体积，支持中英文单位名。纯本地计算，无网络依赖。"
homepage: ""
metadata:
  {
    "openclaw":
      {
        "emoji": "📐",
        "install":
          [
            {
              "id": "python3",
              "kind": "apt",
              "formula": "python3",
              "bins": ["python3"],
              "label": "Install python3",
            },
          ],
      },
  }
---

# unit-converter.sh 单位换算

常用单位即时换算，**纯本地计算**，支持中英文单位写法。

## 用法

```bash
unit-converter.sh length 1 km m       # 长度: 1千米 = ?米
unit-converter.sh weight 5 kg g       # 重量: 5千克 = ?克
unit-converter.sh temp 100 c f        # 温度: 100°C = ?°F
unit-converter.sh speed 60 kmh mph    # 速度: 60 km/h = ? mph
unit-converter.sh data 1 GB MB        # 存储: 1GB = ?MB
unit-converter.sh area 1 ha m2        # 面积: 1公顷 = ?平方米
unit-converter.sh volume 1 L ml       # 体积: 1升 = ?毫升
unit-converter.sh --help              # 帮助
```

## 支持类别

- 📏 length: mm / cm / m / km / in / ft / yd / mile
- ⚖️ weight: mg / g / kg / t / oz / lb
- 🌡️ temp: c ↔ f（摄氏 ↔ 华氏）
- 🚗 speed: kmh / mph / ms / knot
- 💾 data: b / kb / mb / gb / tb
- 🗺️ area: m2 / km2 / ha / acre / ft2
- 🧪 volume: ml / l / m3 / gal / cup

## 特点

- 🔒 完全本地计算，无网络请求
- 🇨🇳 支持中英文单位名（如 kg=千克、m=米）
- ⚡ 即时结果，适合日常快速换算
