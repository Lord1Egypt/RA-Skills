# 车辆年检沿途路线规划器

## 快速开始

### 1. 安装依赖

无需额外依赖，仅需 Python 3 标准库。

### 2. 准备高德 API Key

前往 [高德开放平台](https://console.amap.com/dev/key/app) 申请 **Web服务** 类型的 Key。

### 3. 准备检测站列表

CSV 格式，包含 `name` 和 `address` 两列。可从 [122.gov.cn](https://122.gov.cn/) 获取。

本仓库已附带 `stations_shanghai.csv`（上海120家检测站）作为示例。

### 4. 运行

```bash
python3 planner.py \
  --amap-key YOUR_AMAP_KEY \
  --home "你的家庭地址" \
  --company "你的公司地址" \
  --depart 07:30 \
  --inspect-min 45 \
  --city 上海 \
  --stations-file stations_shanghai.csv \
  --top-n 5
```

### 5. 输出

Markdown 格式的出行方案，包含 Top N 排名总览表和每个方案的详细时间轴 + 导航明细。

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| `--amap-key` | ✅ | — | 高德Web服务API Key |
| `--home` | ✅ | — | 出发地地址 |
| `--company` | ✅ | — | 目的地地址 |
| `--stations-file` | ✅ | — | 检测站CSV文件 |
| `--depart` | ❌ | 07:30 | 出发时间 |
| `--inspect-min` | ❌ | 45 | 办事耗时（分钟） |
| `--city` | ❌ | 上海 | 城市名 |
| `--top-n` | ❌ | 5 | 输出前N名 |

## 安全须知

- **API Key 由用户运行时通过 `--amap-key` 参数传入，不会持久化存储。**
- 请勿将 API Key 写入任何文件或提交到版本控制。
- 本工具不收集、不上传任何用户数据。
