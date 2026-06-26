#!/usr/bin/env python3
"""
Sentinel Satellite Image Downloader
基于 STAC API 下载哨兵卫星影像
"""

import argparse
import json
import os
import sys
import requests
from datetime import datetime
from typing import List, Dict, Optional, Any
from urllib.parse import urljoin

# 默认 STAC API 端点
DEFAULT_STAC_APIS = {
    'sentinel-1': 'https://planetarycomputer.microsoft.com/api/stac/v1',
    'sentinel-2': 'https://planetarycomputer.microsoft.com/api/stac/v1',
    'sentinel-5p': 'https://planetarycomputer.microsoft.com/api/stac/v1',
}

# 各任务的集合 ID (Microsoft Planetary Computer)
COLLECTION_IDS = {
    'sentinel-1': 'sentinel-1-grd',
    'sentinel-2': 'sentinel-2-l2a',
    'sentinel-5p': 'sentinel-5p-l2-netcdf',
}

# 各任务的产品类型
PRODUCT_TYPES = {
    'sentinel-1': 'GRD',  # 地面距离产品
    'sentinel-2': 'L1C',  # 顶层大气产品
    'sentinel-5p': 'L2',  # 二级产品
}


class SentinelDownloader:
    """哨兵卫星影像下载器"""

    def __init__(self, stac_api: Optional[str] = None, mission: str = 'sentinel-2'):
        """
        初始化下载器

        Args:
            stac_api: STAC API 端点 URL
            mission: 任务类型 (sentinel-1, sentinel-2, sentinel-5p)
        """
        self.mission = mission.lower()
        if stac_api:
            self.stac_api = stac_api.rstrip('/')
        else:
            self.stac_api = DEFAULT_STAC_APIS.get(self.mission, DEFAULT_STAC_APIS['sentinel-2']).rstrip('/')

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Sentinel-Downloader/1.0'
        })

    def search(
        self,
        bbox: List[float],
        start_date: str,
        end_date: str,
        max_cloud_cover: float = 100,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        搜索哨兵影像

        Args:
            bbox: 地理范围 [minLon, minLat, maxLon, maxLat]
            start_date: 开始日期 YYYY-MM-DD
            end_date: 结束日期 YYYY-MM-DD
            max_cloud_cover: 最大云量百分比
            limit: 最大返回结果数

        Returns:
            搜索结果列表
        """
        # 构建 STAC 搜索请求
        search_url = f"{self.stac_api}/search"

        # 构建查询条件
        query = {
            "collections": [COLLECTION_IDS.get(self.mission, COLLECTION_IDS['sentinel-2'])],
            "bbox": bbox,
            "datetime": f"{start_date}T00:00:00Z/{end_date}T23:59:59Z",
            "limit": limit,
        }

        # 添加云量过滤 (仅 Sentinel-2)
        if self.mission == 'sentinel-2' and max_cloud_cover < 100:
            query["query"] = {
                "eo:cloud_cover": {
                    "lte": max_cloud_cover
                }
            }

        print(f"正在搜索 {self.mission} 影像...")
        print(f"  STAC API: {self.stac_api}")
        print(f"  地理范围：{bbox}")
        print(f"  时间范围：{start_date} 至 {end_date}")
        print(f"  最大云量：{max_cloud_cover}%")
        print(f"  限制数量：{limit}")

        try:
            response = self.session.post(search_url, json=query, timeout=60)
            response.raise_for_status()
            data = response.json()

            features = data.get('features', [])
            print(f"  找到 {len(features)} 个结果")

            return self._parse_results(features)

        except requests.exceptions.RequestException as e:
            print(f"搜索失败：{e}")
            return []

    def _parse_results(self, features: List[Dict]) -> List[Dict[str, Any]]:
        """解析 STAC 搜索结果"""
        results = []

        for feature in features:
            properties = feature.get('properties', {})
            assets = feature.get('assets', {})
            links = feature.get('links', [])

            # 提取关键信息
            result = {
                'id': feature.get('id', ''),
                'datetime': properties.get('datetime', ''),
                'cloud_cover': properties.get('eo:cloud_cover', properties.get('cloud_cover', 0)),
                'platform': properties.get('platform', ''),
                'instruments': properties.get('instruments', []),
                'bbox': feature.get('bbox', []),
                'assets': self._extract_assets(assets),
                'self_link': self._find_self_link(links),
            }

            results.append(result)

        return results

    def _extract_assets(self, assets: Dict) -> Dict[str, str]:
        """提取可用的数据资源链接"""
        extracted = {}

        for key, asset in assets.items():
            href = asset.get('href', '')
            asset_type = asset.get('type', '')

            # 提取主要的数据链接
            if any(x in key.lower() for x in ['data', 'image', 'download', 'safe']):
                extracted[key] = href
            elif 'thumbnail' in key.lower():
                extracted['thumbnail'] = href

        return extracted

    def _find_self_link(self, links: List[Dict]) -> Optional[str]:
        """查找自引用链接"""
        for link in links:
            if link.get('rel') == 'self':
                return link.get('href')
        return None

    def download(
        self,
        items: List[Dict[str, Any]],
        output_dir: str,
        asset_keys: Optional[List[str]] = None
    ) -> List[str]:
        """
        下载影像文件

        Args:
            items: 搜索结果的物品列表
            output_dir: 输出目录
            asset_keys: 要下载的资产键列表

        Returns:
            已下载文件路径列表
        """
        downloaded = []

        for item in items:
            print(f"\n下载产品：{item['id']}")

            assets = item.get('assets', {})
            if not assets:
                print("  没有可用的下载链接")
                continue

            # 确定要下载的资产
            if asset_keys:
                keys_to_download = [k for k in asset_keys if k in assets]
            else:
                # 默认下载主要数据文件
                keys_to_download = list(assets.keys())

            # 创建输出目录
            item_dir = os.path.join(output_dir, item['id'])
            os.makedirs(item_dir, exist_ok=True)

            for key in keys_to_download:
                href = assets[key]
                if not href:
                    continue

                filename = self._get_filename_from_url(href, key)
                filepath = os.path.join(item_dir, filename)

                if os.path.exists(filepath):
                    print(f"  跳过 (已存在): {filename}")
                    continue

                print(f"  下载：{filename}...")
                if self._download_file(href, filepath):
                    downloaded.append(filepath)
                else:
                    print(f"  下载失败：{filename}")

        return downloaded

    def _get_filename_from_url(self, url: str, default_key: str) -> str:
        """从 URL 提取文件名"""
        # 尝试从 URL 获取文件名
        if '?' in url:
            url = url.split('?')[0]
        filename = os.path.basename(url)

        if filename:
            return filename

        # 回退到使用资产键
        ext = os.path.splitext(url)[1] or '.tif'
        return f"{default_key}{ext}"

    def _download_file(self, url: str, filepath: str) -> bool:
        """下载单个文件"""
        try:
            response = self.session.get(url, stream=True, timeout=300)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        # 显示进度
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"    进度：{progress:.1f}%", end='\r')

            print(f"    完成：{downloaded / 1024 / 1024:.1f} MB")
            return True

        except requests.exceptions.RequestException as e:
            print(f"    错误：{e}")
            if os.path.exists(filepath):
                os.remove(filepath)
            return False


def format_output(results: List[Dict], format_type: str = 'table') -> str:
    """格式化输出结果"""
    if format_type == 'json':
        return json.dumps(results, indent=2, ensure_ascii=False)

    # 表格格式
    if not results:
        return "未找到符合条件的影像"

    output = []
    output.append(f"\n找到 {len(results)} 个影像产品:\n")
    output.append("-" * 100)

    for i, item in enumerate(results, 1):
        output.append(f"[{i}] {item['id']}")
        output.append(f"    时间：{item['datetime']}")
        output.append(f"    云量：{item['cloud_cover']:.1f}%")
        output.append(f"    平台：{item['platform']}")
        output.append(f"    范围：[{', '.join(f'{x:.2f}' for x in item['bbox'])}]")

        if item.get('assets'):
            assets = list(item['assets'].keys())
            output.append(f"    资源：{', '.join(assets[:5])}{'...' if len(assets) > 5 else ''}")

        output.append("")

    output.append("-" * 100)
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description='哨兵卫星影像下载器 (基于 STAC API)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 搜索 Sentinel-2 影像
  %(prog)s --bbox 116.0 39.0 117.0 40.0 --start-date 2024-01-01 --end-date 2024-12-31

  # 搜索并限制云量
  %(prog)s --bbox 116.0 39.0 117.0 40.0 --max-cloud-cover 10 --mission sentinel-2

  # 搜索并下载
  %(prog)s --bbox 116.0 39.0 117.0 40.0 --download --output-dir ./sentinel_data

  # 使用自定义 STAC API
  %(prog)s --stac-api https://planetarycomputer.microsoft.com/api/stac/v1 --bbox 116.0 39.0 117.0 40.0
        """
    )

    parser.add_argument('--bbox', type=float, nargs=4, required=True,
                        metavar=('MIN_LON', 'MIN_LAT', 'MAX_LON', 'MAX_LAT'),
                        help='地理范围 [最小经度 最小纬度 最大经度 最大纬度]')
    parser.add_argument('--start-date', type=str, required=True,
                        help='开始日期 (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, required=True,
                        help='结束日期 (YYYY-MM-DD)')
    parser.add_argument('--mission', type=str, default='sentinel-2',
                        choices=['sentinel-1', 'sentinel-2', 'sentinel-5p'],
                        help='卫星任务类型 (默认：sentinel-2)')
    parser.add_argument('--max-cloud-cover', type=float, default=100,
                        help='最大云量百分比 (0-100, 默认：100)')
    parser.add_argument('--stac-api', type=str, default=None,
                        help='STAC API 端点 URL')
    parser.add_argument('--output-dir', type=str, default='./sentinel_output',
                        help='输出目录 (默认：./sentinel_output)')
    parser.add_argument('--limit', type=int, default=10,
                        help='最大搜索结果数 (默认：10)')
    parser.add_argument('--download', action='store_true',
                        help='是否下载影像文件')
    parser.add_argument('--output-format', type=str, default='table',
                        choices=['table', 'json'],
                        help='输出格式 (默认：table)')

    args = parser.parse_args()

    # 验证日期格式
    try:
        datetime.strptime(args.start_date, '%Y-%m-%d')
        datetime.strptime(args.end_date, '%Y-%m-%d')
    except ValueError as e:
        print(f"日期格式错误，请使用 YYYY-MM-DD 格式：{e}")
        sys.exit(1)

    # 创建下载器
    downloader = SentinelDownloader(
        stac_api=args.stac_api,
        mission=args.mission
    )

    # 搜索影像
    results = downloader.search(
        bbox=args.bbox,
        start_date=args.start_date,
        end_date=args.end_date,
        max_cloud_cover=args.max_cloud_cover,
        limit=args.limit
    )

    if not results:
        print("\n未找到符合条件的影像")
        sys.exit(0)

    # 输出结果
    print(format_output(results, args.output_format))

    # 下载
    if args.download:
        print(f"\n开始下载，输出目录：{args.output_dir}")
        os.makedirs(args.output_dir, exist_ok=True)

        downloaded = downloader.download(results, args.output_dir)

        print(f"\n下载完成！共下载 {len(downloaded)} 个文件")
        if downloaded:
            print("已下载文件:")
            for f in downloaded[:10]:
                print(f"  - {f}")
            if len(downloaded) > 10:
                print(f"  ... 还有 {len(downloaded) - 10} 个文件")


if __name__ == '__main__':
    main()
