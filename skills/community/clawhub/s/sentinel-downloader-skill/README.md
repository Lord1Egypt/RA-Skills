# Sentinel Downloader

基于 STAC (SpatioTemporal Asset Catalog) API 下载哨兵系列卫星影像的工具。

## 快速开始

### 1. 安装依赖

```bash
cd /home/admin/skills/sentinel-downloader
pip3 install requests pystac-client geopandas
```

### 2. 使用示例

```bash
# 搜索北京地区的 Sentinel-2 影像
./sentinel-download.sh --bbox 116.0 39.0 117.0 40.0 --start-date 2024-01-01 --end-date 2024-12-31

# 搜索云量小于 10% 的影像
./sentinel-download.sh --bbox 116.0 39.0 117.0 40.0 --start-date 2024-01-01 --end-date 2024-12-31 --max-cloud-cover 10

# 搜索并下载
./sentinel-download.sh --bbox 116.0 39.0 117.0 40.0 --start-date 2024-01-01 --end-date 2024-12-31 --download --output-dir ./data

# 使用 Microsoft Planetary Computer API
./sentinel-download.sh --stac-api https://planetarycomputer.microsoft.com/api/stac/v1 --bbox 116.0 39.0 117.0 40.0 --start-date 2024-01-01 --end-date 2024-12-31
```

## 支持的卫星任务

| 任务 | 说明 | 数据类型 |
|------|------|----------|
| Sentinel-1 | SAR 雷达影像 | 全天候地表监测 |
| Sentinel-2 | 多光谱光学影像 | 陆地观测，10m 分辨率 |
| Sentinel-5P | 大气成分监测 | 空气质量、臭氧等 |

## 参数说明

| 参数 | 说明 | 必填 |
|------|------|------|
| `--bbox` | 地理范围 [minLon minLat maxLon maxLat] | 是 |
| `--start-date` | 开始日期 YYYY-MM-DD | 是 |
| `--end-date` | 结束日期 YYYY-MM-DD | 是 |
| `--mission` | 卫星任务 (sentinel-1/2/5p) | 否 |
| `--max-cloud-cover` | 最大云量百分比 | 否 |
| `--stac-api` | STAC API 端点 | 否 |
| `--output-dir` | 输出目录 | 否 |
| `--limit` | 最大结果数 | 否 |
| `--download` | 是否下载 | 否 |

## 常用地理范围参考

| 地区 | BBOX |
|------|------|
| 北京 | 115.4 39.4 117.5 41.1 |
| 上海 | 120.5 30.4 122.1 31.9 |
| 广州 | 112.6 22.3 114.1 23.9 |
| 深圳 | 113.7 22.4 114.6 22.8 |

## STAC API 端点

| 名称 | URL | 说明 |
|------|-----|------|
| AWS Earth Search | https://earth-search.aws.element84.com/v0 | 亚马逊云托管 |
| Microsoft PC | https://planetarycomputer.microsoft.com/api/stac/v1 | 微软行星计算机 |
| Sentinel Hub | https://services.sentinel-hub.com/api/v1/catalog | 哨兵中心 |

## 输出说明

搜索结果包含：
- 产品 ID
- 获取时间
- 云量信息
- 地理范围
- 下载链接

下载的文件保存在指定输出目录，按产品 ID 组织子目录。

## 注意事项

1. 下载大量数据需要稳定的网络连接
2. 部分数据源可能需要注册认证
3. 建议先用小 limit 值测试搜索
4. 下载前建议预览结果确认覆盖范围

## 许可证

MIT License
