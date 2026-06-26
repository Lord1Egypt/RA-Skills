"""打印机驱动搜索与下载公共函数"""

import os
import re
import requests
from datetime import date


def search_drivers(keyword):
    """搜索打印机驱动，返回驱动列表"""
    url = "https://www.chinauos.com/driver-api/v1/driver/query/list"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Referer": "https://www.chinauos.com/resource/download-drivers",
        "Accept": "application/json"
    }
    params = {
        "keyword": keyword,
        "source": "2",
        "pageIndex": "1",
        "pageSize": "20"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("result") and data.get("data"):
            return data["data"]["list"]
        else:
            print(f"未找到相关结果: {data.get('msg')}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"搜索出错: {e}")
        return []


def download_driver(driver_info, download_dir="."):
    """根据 driver_info 下载驱动，返回 (success, filepath)"""
    deb_id = driver_info.get('deb_id')
    driver_id = driver_info.get('driver_id')

    if not deb_id or not driver_id:
        print("错误：缺少必要的下载参数 (deb_id 或 driver_id)")
        return False, None

    download_api = f"https://www.chinauos.com/driver-api/v1/driver/download?deb_id={deb_id}&driver_id={driver_id}"

    package = driver_info.get('package', 'unknown')
    model = driver_info.get('model', 'unknown')
    arch = driver_info.get('arch', 'unknown')
    version = driver_info.get('version', 'unknown')

    print(f"\n开始下载驱动...")
    print(f"  型号：{model}")
    print(f"  包名：{package}")
    print(f"  架构：{arch}")
    print(f"  版本：{version}")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "Referer": "https://www.chinauos.com/resource/download-drivers"
        }

        resp = requests.get(download_api, headers=headers, timeout=10)
        resp.raise_for_status()
        result_data = resp.json()

        if not result_data.get('result'):
            print(f"API返回错误: {result_data.get('msg')}")
            return False, None

        actual_url = result_data['data']['url']

        file_resp = requests.get(actual_url, headers=headers, stream=True, timeout=60)
        file_resp.raise_for_status()

        filename = f"{package}_{version}_{arch}.deb"
        filepath = os.path.join(download_dir, filename)

        total_size = int(file_resp.headers.get('content-length', 0))
        if total_size > 0:
            print(f"文件大小：{total_size / 1024 / 1024:.2f} MB")

        downloaded_size = 0

        with open(filepath, 'wb') as f:
            for chunk in file_resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)

                    if total_size > 0:
                        percent = (downloaded_size / total_size) * 100
                        print(f"\r进度：{percent:.1f}% ({downloaded_size / 1024 / 1024:.2f} MB / {total_size / 1024 / 1024:.2f} MB)", end='', flush=True)

        print("\n")
        print(f"下载完成！")
        print(f"文件保存位置：{os.path.abspath(filepath)}")
        print(f"文件大小：{downloaded_size / 1024 / 1024:.2f} MB")

        return True, filepath

    except requests.exceptions.HTTPError as e:
        print(f"HTTP 错误：{e}")
        return False, None
    except requests.exceptions.ConnectionError as e:
        print(f"连接错误：{e}")
        return False, None
    except requests.exceptions.Timeout:
        print("下载超时，请检查网络连接。")
        return False, None
    except Exception as e:
        print(f"下载失败：{e}")
        return False, None


def build_download_dir(base_dir, model_name):
    """构造下载目录: <base_dir>/printer_driver_YYYYMMDD/<model_name>/"""
    date_str = date.today().strftime("%Y%m%d")
    safe_model = re.sub(r'[\\/:*?"<>|]', '_', model_name).replace(' ', '_')
    dir_path = os.path.join(base_dir, f"printer_driver_{date_str}", safe_model)
    os.makedirs(dir_path, exist_ok=True)
    return dir_path


def display_driver_list(drivers):
    """以表格形式显示驱动列表"""
    header = f"\n{'序号':<4} | {'架构':<10} | {'驱动型号 (Model)':<50} | {'版本 (Version)':<15} | {'包名 (Package)'}"
    print(header)
    print("-" * 120)

    for idx, item in enumerate(drivers):
        package = item.get('package', 'N/A')
        arch = item.get('arch', 'N/A')
        model = item.get('model', 'N/A')[:50]
        version = item.get('version', 'N/A')
        print(f"{idx + 1:<4} | {arch:<10} | {model:<50} | {version:<15} | {package}")


def select_drivers(drivers, preferred_arch="amd64"):
    """选择要下载的驱动列表：
    1. 始终包含所有 all 架构驱动
    2. 包含所有匹配 preferred_arch 的驱动
    不够 3 个则有多少下载多少
    """
    if not drivers:
        return []

    all_arch = [d for d in drivers if d.get('arch') == 'all']
    preferred = [d for d in drivers if d.get('arch') == preferred_arch]

    return all_arch + preferred
