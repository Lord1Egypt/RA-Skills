#!/usr/bin/env python3
"""
WorldClim BioClimatic Variables Extractor
从WorldClim GeoTIFF文件中根据经纬度提取生物气候变量
"""

import argparse
import os
import sys
import urllib.request
import zipfile

import pandas as pd
import rasterio

# WorldClim 2.1 下载配置
WORLCLIM_BASE_URL = "https://geodata.ucdavis.edu/climate/worldclim/2_1/base"
BIO_ZIP_URL = f"{WORLCLIM_BASE_URL}/wc2.1_{{res}}_bio.zip"

# 分辨率对应的像素大小说明
RES_INFO = {
    "10m": {"desc": "10 arc-minutes (~18.5 km)", "zip_size_mb": 48},
    "5m": {"desc": "5 arc-minutes (~9.3 km)", "zip_size_mb": 170},
    "2.5m": {"desc": "2.5 arc-minutes (~4.6 km)", "zip_size_mb": 650},
}

# BIO变量名称映射
BIO_NAMES = {
    1: "年均温 (Annual Mean Temperature)",
    2: "昼夜温差月均值 (Mean Diurnal Range)",
    3: "等温性 (Isothermality)",
    4: "温度季节性 (Temperature Seasonality)",
    5: "最暖月最高温 (Max Temperature of Warmest Month)",
    6: "最冷月最低温 (Min Temperature of Coldest Month)",
    7: "年温度范围 (Temperature Annual Range)",
    8: "最湿季均温 (Mean Temperature of Wettest Quarter)",
    9: "最干季均温 (Mean Temperature of Driest Quarter)",
    10: "最暖季均温 (Mean Temperature of Warmest Quarter)",
    11: "最冷季均温 (Mean Temperature of Coldest Quarter)",
    12: "年降水量 (Annual Precipitation)",
    13: "最湿月降水量 (Precipitation of Wettest Month)",
    14: "最干月降水量 (Precipitation of Driest Month)",
    15: "降水季节性 (Precipitation Seasonality)",
    16: "最湿季降水量 (Precipitation of Wettest Quarter)",
    17: "最干季降水量 (Precipitation of Driest Quarter)",
    18: "最暖季降水量 (Precipitation of Warmest Quarter)",
    19: "最冷季降水量 (Precipitation of Coldest Quarter)",
}


def download_worldclim(resolution, cache_dir):
    """下载并解压WorldClim生物气候数据"""
    zip_path = os.path.join(cache_dir, f"wc2.1_{resolution}_bio.zip")
    if os.path.exists(cache_dir):
        # 检查是否已存在所有19个tif文件
        existing = [f for f in os.listdir(cache_dir) if f.startswith(f"wc2.1_{resolution}_bio_") and f.endswith(".tif")]
        if len(existing) == 19:
            print(f"[INFO] 已存在 {resolution} 分辨率数据，跳过下载")
            return cache_dir

    os.makedirs(cache_dir, exist_ok=True)
    url = BIO_ZIP_URL.format(res=resolution)
    print(f"[INFO] 正在下载 WorldClim {resolution} 分辨率数据...")
    print(f"[INFO] 来源: {url}")
    print(f"[INFO] 预计大小: ~{RES_INFO[resolution]['zip_size_mb']} MB")

    try:
        urllib.request.urlretrieve(url, zip_path)
    except Exception as e:
        print(f"[ERROR] 下载失败: {e}")
        print(f"[HINT] 请手动下载 {url} 并解压到 {cache_dir}")
        sys.exit(1)

    print(f"[INFO] 解压中...")
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(cache_dir)
    os.remove(zip_path)
    print(f"[INFO] 完成，数据保存在: {cache_dir}")
    return cache_dir


def extract_values(tif_path, coords):
    """从单个tif文件中提取坐标值"""
    with rasterio.open(tif_path) as src:
        values = list(src.sample(coords))
    return [v[0] for v in values]


def build_column_name(bio_num, res):
    """构建输出列名"""
    bio_name = BIO_NAMES.get(bio_num, f"BIO{bio_num}")
    # 简化列名
    if bio_num == 1:
        return "年均温度_C"
    elif bio_num == 12:
        return "年降水量_mm"
    else:
        return f"BIO{bio_num}"


def process(input_path, lon_col, lat_col, output_path, bios, resolution, cache_dir):
    """主处理流程"""
    # 1. 读取输入
    if input_path.endswith(".csv"):
        df = pd.read_csv(input_path)
    else:
        df = pd.read_excel(input_path)

    n_total = len(df)
    print(f"[INFO] 读取 {n_total} 行数据")

    # 2. 清洗坐标（先去除隐藏空格/特殊Unicode空白字符，再转数值）
    import unicodedata
    def clean_numeric(series):
        if series.dtype == object:
            # 去除常见Unicode空白字符（包括\xa0不间断空格等）
            series = series.astype(str).str.replace(r'\s+', '', regex=True)
            series = series.str.replace(r'[\u00A0\u2000-\u200F\u202F\u205F\u3000]', '', regex=True)
        return pd.to_numeric(series, errors="coerce")

    df[lon_col] = clean_numeric(df[lon_col])
    df[lat_col] = clean_numeric(df[lat_col])
    df_valid = df.dropna(subset=[lon_col, lat_col]).copy()
    n_valid = len(df_valid)
    if n_valid < n_total:
        print(f"[WARN] 剔除 {n_total - n_valid} 行无效坐标，剩余 {n_valid} 行")

    coords = list(zip(df_valid[lon_col].astype(float), df_valid[lat_col].astype(float)))

    # 3. 确保数据存在
    data_dir = download_worldclim(resolution, cache_dir)

    # 4. 提取每个BIO变量
    for bio_num in bios:
        tif_name = f"wc2.1_{resolution}_bio_{bio_num}.tif"
        tif_path = os.path.join(data_dir, tif_name)
        if not os.path.exists(tif_path):
            print(f"[WARN] 文件不存在: {tif_path}，跳过 BIO{bio_num}")
            continue

        col_name = build_column_name(bio_num, resolution)
        print(f"[INFO] 提取 {col_name} ...")
        values = extract_values(tif_path, coords)
        df_valid[col_name] = values

        # 基本统计
        vmin, vmax = min(values), max(values)
        print(f"       范围: {vmin:.2f} ~ {vmax:.2f}")

    # 5. 保存结果
    if output_path.endswith(".csv"):
        df_valid.to_csv(output_path, index=False)
    else:
        df_valid.to_excel(output_path, index=False)
    print(f"[INFO] 结果保存至: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="从WorldClim GeoTIFF提取生物气候变量",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  # 提取年均温和年降水（默认）
  python extract_worldclim.py -i coords.xlsx -o result.xlsx

  # 提取全部19个BIO变量
  python extract_worldclim.py -i coords.xlsx -o result.xlsx --bios 1-19

  # 提取特定变量，2.5m分辨率
  python extract_worldclim.py -i coords.csv -o result.xlsx --bios 1,5,6,12,13 --res 2.5m

BIO变量说明:
  温度类 (°C): BIO1-BIO11
  降水类 (mm): BIO12-BIO19
"""
    )
    parser.add_argument("-i", "--input", required=True, help="输入文件 (.xlsx 或 .csv)，需含经纬度列")
    parser.add_argument("-o", "--output", required=True, help="输出文件 (.xlsx 或 .csv)")
    parser.add_argument("--lon", default="经度", help="经度列名 (默认: 经度)")
    parser.add_argument("--lat", default="纬度", help="纬度列名 (默认: 纬度)")
    parser.add_argument(
        "--bios",
        default="1,12",
        help="要提取的BIO变量编号，逗号分隔或范围如 1-19 (默认: 1,12 即年均温+年降水)"
    )
    parser.add_argument("--res", default="10m", choices=["10m", "5m", "2.5m"], help="空间分辨率 (默认: 10m)")
    parser.add_argument("--cache", default="./worldclim_data", help="WorldClim数据缓存目录")

    args = parser.parse_args()

    # 解析bios参数
    bios = []
    for part in args.bios.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            bios.extend(range(int(start), int(end) + 1))
        else:
            bios.append(int(part))
    bios = sorted(set(bios))

    process(
        input_path=args.input,
        lon_col=args.lon,
        lat_col=args.lat,
        output_path=args.output,
        bios=bios,
        resolution=args.res,
        cache_dir=args.cache,
    )


if __name__ == "__main__":
    main()
