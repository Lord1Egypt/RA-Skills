# 🏃 Weight Tracker - 体重追踪器

可视化减肥进度追踪工具，中英文双语支持。

## 快速开始

### 第一步：初始化配置

```bash
cd weight-tracker/assets
chmod +x setup.sh
./setup.sh
```

按照向导提示设置：
- 选择语言（中文/英文）
- 选择端口（自动检测可用端口）
- 设置减肥目标（起始体重、目标体重、日期）
- 输入第一条体重记录

### 第二步：启动服务

```bash
cd <你解压的目录>
python3 -m http.server 8080
```

> 端口号以你配置为准，这里用 8080 举例

### 第三步：打开页面

浏览器访问：`http://localhost:8080/jianfei.html`

### 第四步：记录体重

每天告诉 AI："今天体重 XX kg"，AI 会自动更新数据。

### 快捷键

- 按 `W` 键：导出数据为 JSON 文件

## 文件说明

| 文件 | 说明 |
|------|------|
| `jianfei.html` | 追踪页面（需通过 HTTP 服务访问） |
| `config.json` | 配置文件（目标、体重、日期、语言） |
| `weight_history.json` | 体重记录数据 |
| `setup.sh` | 初始化向导（仅首次需要运行） |

## 修改配置

### 切换语言

编辑 `config.json`，将 `"language": "zh"` 改为 `"language": "en"`，然后刷新页面。

### 修改减肥目标

直接编辑 `config.json` 中的体重和日期配置。

### 查看/导出数据

在页面按 `W` 键，或直接打开 `weight_history.json` 文件查看。

## 目录结构

```
weight-tracker/
├── README.md           # 本文件
└── assets/
    ├── jianfei.html     # 追踪页面
    ├── config.json      # 配置（可编辑）
    ├── weight_history.json  # 数据（自动更新）
    └── setup.sh         # 初始化向导
```

## 常见问题

**Q: 为什么必须启动 HTTP 服务器？**
A: 页面需要从外部 JSON 文件读取配置和数据，file:// 协议不支持此功能。

**Q: 端口被占用了怎么办？**
A: 编辑 `config.json` 修改 `port` 字段为其他端口，如 8888。

**Q: 如何多人共享数据？**
A: 将 `jianfei.html`、`config.json`、`weight_history.json` 放在局域网共享目录，多人通过 `http://<电脑IP>:<端口>/jianfei.html` 访问。
