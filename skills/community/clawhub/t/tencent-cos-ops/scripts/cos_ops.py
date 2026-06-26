#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云COS对象存储操作脚本
功能：上传本地文件到COS指定目录，按月管理文件

依赖：pip install -U cos-python-sdk-v5

环境变量：
  COS_SECRET_ID - 腾讯云SecretId
  COS_SECRET_KEY - 腾讯云SecretKey
  COS_REGION - COS地域，如ap-beijing
  COS_BUCKET - COS Bucket名称
"""

import os
import sys
import argparse
from datetime import datetime
from qcloud_cos import CosConfig, CosS3Client


def get_cos_client():
    """初始化COS客户端"""
    secret_id = os.environ.get('COS_SECRET_ID')
    secret_key = os.environ.get('COS_SECRET_KEY')
    region = os.environ.get('COS_REGION', 'ap-beijing')

    if not secret_id or not secret_key:
        raise ValueError("请设置环境变量 COS_SECRET_ID 和 COS_SECRET_KEY")

    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    return CosS3Client(config)


def get_monthly_prefix():
    """获取当前月份的文件夹前缀，格式：YYYY/MM/"""
    now = datetime.now()
    return f"{now.year}/{now.month:02d}/"


def upload_file(local_file_path, cos_key=None, bucket=None):
    """
    上传本地文件到COS

    Args:
        local_file_path: 本地文件路径
        cos_key: COS中的对象键，若为None则使用月份前缀+文件名
        bucket: COS Bucket名称，若为None则使用环境变量COS_BUCKET

    Returns:
        dict: 上传响应
    """
    if not os.path.exists(local_file_path):
        raise FileNotFoundError(f"文件不存在: {local_file_path}")

    client = get_cos_client()
    bucket = bucket or os.environ.get('COS_BUCKET')

    if not bucket:
        raise ValueError("请设置环境变量COS_BUCKET或传入bucket参数")

    # 确定COS中的对象键
    if cos_key is None:
        filename = os.path.basename(local_file_path)
        prefix = get_monthly_prefix()
        cos_key = f"{prefix}{filename}"
    elif not cos_key.endswith('/'):
        # 如果cos_key是目录路径，添加文件名
        filename = os.path.basename(local_file_path)
        cos_key = f"{cos_key.rstrip('/')}/{filename}"

    print(f"上传文件: {local_file_path}")
    print(f"到Bucket: {bucket}")
    print(f"对象键: {cos_key}")

    # 使用高级上传接口（自动选择简单上传或分块上传）
    with open(local_file_path, 'rb') as fp:
        response = client.put_object(
            Bucket=bucket,
            Body=fp,
            Key=cos_key,
            EnableMD5=False
        )

    print(f"上传成功，ETag: {response.get('ETag', 'N/A')}")
    return response


def upload_file_advanced(local_file_path, cos_key=None, bucket=None, part_size=1, max_threads=10):
    """
    使用高级上传接口上传大文件

    Args:
        local_file_path: 本地文件路径
        cos_key: COS中的对象键
        bucket: COS Bucket名称
        part_size: 分块大小(MB)，默认1MB
        max_threads: 最大并发线程数，默认10

    Returns:
        dict: 上传响应
    """
    if not os.path.exists(local_file_path):
        raise FileNotFoundError(f"文件不存在: {local_file_path}")

    client = get_cos_client()
    bucket = bucket or os.environ.get('COS_BUCKET')

    if not bucket:
        raise ValueError("请设置环境变量COS_BUCKET或传入bucket参数")

    # 确定COS中的对象键
    if cos_key is None:
        filename = os.path.basename(local_file_path)
        prefix = get_monthly_prefix()
        cos_key = f"{prefix}{filename}"
    elif not cos_key.endswith('/'):
        filename = os.path.basename(local_file_path)
        cos_key = f"{cos_key.rstrip('/')}/{filename}"

    print(f"高级上传文件: {local_file_path}")
    print(f"到Bucket: {bucket}")
    print(f"对象键: {cos_key}")

    # 高级上传接口，自动选择简单上传或分块上传
    response = client.upload_file(
        Bucket=bucket,
        LocalFilePath=local_file_path,
        Key=cos_key,
        PartSize=part_size,
        MAXThread=max_threads
    )

    print(f"上传成功，ETag: {response.get('ETag', 'N/A')}")
    return response


def download_file(cos_key, local_file_path, bucket=None):
    """
    从COS下载文件到本地

    Args:
        cos_key: COS中的对象键
        local_file_path: 本地保存路径
        bucket: COS Bucket名称

    Returns:
        dict: 下载响应
    """
    client = get_cos_client()
    bucket = bucket or os.environ.get('COS_BUCKET')

    if not bucket:
        raise ValueError("请设置环境变量COS_BUCKET或传入bucket参数")

    print(f"下载文件: {cos_key}")
    print(f"从Bucket: {bucket}")
    print(f"到本地: {local_file_path}")

    response = client.get_object(
        Bucket=bucket,
        Key=cos_key,
    )
    response['Body'].get_stream_to_file(local_file_path)

    print(f"下载成功")
    return response


def list_objects(prefix='', bucket=None, max_items=100):
    """
    列出COS中的对象

    Args:
        prefix: 对象键前缀，用于筛选
        bucket: COS Bucket名称
        max_items: 最大返回数量

    Returns:
        dict: 列表响应
    """
    client = get_cos_client()
    bucket = bucket or os.environ.get('COS_BUCKET')

    if not bucket:
        raise ValueError("请设置环境变量COS_BUCKET或传入bucket参数")

    print(f"列出Bucket: {bucket} 前缀: {prefix}")

    response = client.list_objects(
        Bucket=bucket,
        Prefix=prefix,
        MaxKeys=max_items
    )

    if 'Contents' in response:
        print(f"找到 {len(response['Contents'])} 个对象:")
        for obj in response['Contents']:
            print(f"  - {obj['Key']} ({obj.get('Size', 'N/A')} bytes, {obj.get('LastModified', 'N/A')})")
    else:
        print("没有找到对象")

    return response


def delete_object(cos_key, bucket=None):
    """
    删除COS中的对象

    Args:
        cos_key: COS中的对象键
        bucket: COS Bucket名称

    Returns:
        dict: 删除响应
    """
    client = get_cos_client()
    bucket = bucket or os.environ.get('COS_BUCKET')

    if not bucket:
        raise ValueError("请设置环境变量COS_BUCKET或传入bucket参数")

    print(f"删除对象: {cos_key} 从Bucket: {bucket}")

    response = client.delete_object(
        Bucket=bucket,
        Key=cos_key
    )

    print(f"删除成功")
    return response


def main():
    parser = argparse.ArgumentParser(description='腾讯云COS对象存储操作工具')
    subparsers = parser.add_subparsers(dest='command', help='支持的命令')

    # 上传命令
    upload_parser = subparsers.add_parser('upload', help='上传文件到COS')
    upload_parser.add_argument('local_file', help='本地文件路径')
    upload_parser.add_argument('--key', '-k', help='COS对象键，默认为月份前缀+文件名')
    upload_parser.add_argument('--bucket', '-b', help='COS Bucket名称')
    upload_parser.add_argument('--advanced', '-a', action='store_true', help='使用高级上传接口')
    upload_parser.add_argument('--part-size', '-p', type=int, default=1, help='分块大小(MB)，高级上传用')
    upload_parser.add_argument('--threads', '-t', type=int, default=10, help='最大并发线程数')

    # 下载命令
    download_parser = subparsers.add_parser('download', help='从COS下载文件')
    download_parser.add_argument('cos_key', help='COS对象键')
    download_parser.add_argument('local_file', help='本地保存路径')
    download_parser.add_argument('--bucket', '-b', help='COS Bucket名称')

    # 列表命令
    list_parser = subparsers.add_parser('list', help='列出COS中的对象')
    list_parser.add_argument('--prefix', '-p', default='', help='对象键前缀')
    list_parser.add_argument('--bucket', '-b', help='COS Bucket名称')
    list_parser.add_argument('--max', '-m', type=int, default=100, help='最大返回数量')

    # 删除命令
    delete_parser = subparsers.add_parser('delete', help='删除COS中的对象')
    delete_parser.add_argument('cos_key', help='COS对象键')
    delete_parser.add_argument('--bucket', '-b', help='COS Bucket名称')

    args = parser.parse_args()

    if args.command == 'upload':
        if args.advanced:
            upload_file_advanced(
                args.local_file,
                cos_key=args.key,
                bucket=args.bucket,
                part_size=args.part_size,
                max_threads=args.threads
            )
        else:
            upload_file(
                args.local_file,
                cos_key=args.key,
                bucket=args.bucket
            )
    elif args.command == 'download':
        download_file(args.cos_key, args.local_file, bucket=args.bucket)
    elif args.command == 'list':
        list_objects(prefix=args.prefix, bucket=args.bucket, max_items=args.max)
    elif args.command == 'delete':
        delete_object(args.cos_key, bucket=args.bucket)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
