---
name: sentinel-downloader
description: Download Sentinel satellite imagery (Sentinel-1/2/5P) via STAC API with cloud cover filtering and batch download support | 基于 STAC API 下载哨兵卫星影像 (Sentinel-1/2/5P)，支持云量过滤和批量下载
version: 1.0.1
author: ruiduobao
license: MIT-0
---

# Sentinel Downloader | 哨兵卫星影像下载器

Download Sentinel satellite imagery via STAC (SpatioTemporal Asset Catalog) API.

基于 STAC (SpatioTemporal Asset Catalog) API 下载哨兵系列卫星影像。

---

## Install Dependencies | 安装依赖

```bash
pip install pystac-client requests
```

---

## Usage | 使用方法

### Search Sentinel-2 Imagery | 搜索 Sentinel-2 影像

```bash
./sentinel-download.sh --bbox 116.0 39.0 117.0 40.0 --start-date 2024-01-01 --end-date 2024-12-31
```

### Search with Cloud Cover Filter | 搜索并限制云量

```bash
./sentinel-download.sh --bbox 116.0 39.0 117.0 40.0 --max-cloud-cover 10
```

### Search and Download | 搜索并下载

```bash
./sentinel-download.sh --bbox 116.0 39.0 117.0 40.0 --download --output-dir ./data
```

---

## Supported Missions | 支持的卫星任务

| Mission | Description | Data Type |
|---------|-------------|-----------|
| 任务 | 说明 | 数据类型 |
| Sentinel-1 | SAR Radar Imagery / SAR 雷达影像 | All-weather monitoring / 全天候地表监测 |
| Sentinel-2 | Multispectral Optical / 多光谱光学影像 | Land observation, 10m resolution / 陆地观测，10m 分辨率 |
| Sentinel-5P | Atmospheric Monitoring / 大气成分监测 | Air quality, ozone / 空气质量、臭氧等 |

---

## Parameters | 参数说明

| Parameter | Description | Required |
|-----------|-------------|----------|
| 参数 | 说明 | 必填 |
| --bbox | Geographic extent [minLon minLat maxLon maxLat] / 地理范围 | Yes / 是 |
| --start-date | Start date YYYY-MM-DD / 开始日期 | Yes / 是 |
| --end-date | End date YYYY-MM-DD / 结束日期 | Yes / 是 |
| --mission | Satellite mission (sentinel-1/2/5p) / 卫星任务 | No / 否 |
| --max-cloud-cover | Max cloud cover percentage / 最大云量百分比 | No / 否 |
| --download | Download imagery / 是否下载 | No / 否 |

---

## Example Output | 输出示例

```
正在搜索 sentinel-2 影像...
  找到 3 个结果

[1] S2A_MSIL2A_20241227T031141_R075_T50TNK
    时间：2024-12-27
    云量：0.4%
    平台：Sentinel-2A
```

---

## STAC API Endpoints | STAC API 端点

| Name | URL |
|------|-----|
| Microsoft Planetary Computer | https://planetarycomputer.microsoft.com/api/stac/v1 |
| AWS Earth Search | https://earth-search.aws.element84.com/v1 |

---

## License | 许可证

MIT-0 - Free to use, modify, and redistribute. No attribution required.