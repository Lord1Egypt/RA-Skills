# 腾讯云COS API 参考

## 安装

```bash
pip install -U cos-python-sdk-v5
```

## 初始化

```python
from qcloud_cos import CosConfig, CosS3Client
import os

secret_id = os.environ['COS_SECRET_ID']
secret_key = os.environ['COS_SECRET_KEY']
region = 'ap-beijing'

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
client = CosS3Client(config)
```

## 核心API

### 上传文件

**简单上传（文件流）**：
```python
with open('picture.jpg', 'rb') as fp:
    response = client.put_object(
        Bucket='examplebucket-1250000000',
        Body=fp,
        Key='picture.jpg'
    )
```

**高级上传（自动分块）**：
```python
response = client.upload_file(
    Bucket='examplebucket-1250000000',
    LocalFilePath='local.txt',
    Key='picture.jpg',
    PartSize=1,
    MAXThread=10
)
```

### 下载文件

```python
response = client.get_object(
    Bucket='examplebucket-1250000000',
    Key='picture.jpg'
)
response['Body'].get_stream_to_file('output.txt')
```

### 列举对象

```python
response = client.list_objects(
    Bucket='examplebucket-1250000000',
    Prefix='2024/01/',
    MaxKeys=100
)
```

### 删除对象

```python
response = client.delete_object(
    Bucket='examplebucket-1250000000',
    Key='picture.jpg'
)
```

## 地域对照表

| 地域 | Region值 |
|------|----------|
| 北京 | ap-beijing |
| 上海 | ap-shanghai |
| 广州 | ap-guangzhou |
| 成都 | ap-chengdu |
| 重庆 | ap-chongqing |
| 香港 | ap-hongkong |
| 新加坡 | ap-singapore |
| 东京 | ap-tokyo |
| 硅谷 | na-siliconvalley |
| 弗吉尼亚 | na-ashburn |

## 文件大小限制

| 操作 | 限制 |
|------|------|
| 简单上传 | 5GB |
| 分块上传 | 50TB |
| 单个对象键 | 850字节 |
| 分块大小 | 1MB - 50GB |
