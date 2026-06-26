# 图片理解API服务部署指南

## 一、环境准备

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export TENCENT_SECRET_ID="你的腾讯云SecretId"
export TENCENT_SECRET_KEY="你的腾讯云SecretKey"
export TENCENT_CI_BUCKET="your-bucket-12345"  # BucketName-APPID格式
export TENCENT_CI_REGION="ap-guangzhou"        # 存储桶区域
export IMAGE_API_KEY="自定义API密钥"            # 客户端调用时的验证密码
export PORT=8901

# 可选：通义千问VL（升级图片理解能力）
export DASHSCOPE_API_KEY="你的通义千问API Key"
```

## 二、启动服务

```bash
# 开发模式
python3 server.py

# 生产模式
gunicorn -w 4 -b 0.0.0.0:8901 server:app --timeout 120
```

## 三、接口说明

### POST /api/analyze
接收图片文件，返回识别结果。

请求：
- Header: `X-API-Key: 你的密钥`
- Body: `file` (图片文件) + `model` (可选: ci|qwen, 默认ci)

响应：
```json
{
  "status": "ok",
  "model": "ci",
  "description": "图片内容识别: 表格, 表单\n\n图片中的文字内容:\n用户名\n密码\n登录",
  "labels": [{"name": "表格", "confidence": 85, "category": "物品", "sub_category": "办公用品"}],
  "ocr_text": "用户名\n密码\n登录",
  "ocr_line_count": 3,
  "confidence": 85
}
```

### GET /api/health
健康检查，返回服务状态和可用provider。

## 四、腾讯云数据万象配置

1. 开通腾讯云COS（对象存储）
2. 创建存储桶（用于临时上传图片）
3. 开通数据万象服务（绑定存储桶）
4. 获取SecretId和SecretKey（访问管理→API密钥）
5. 购买内容识别资源包（可选，按量计费也可）

## 五、安全建议

- 生产环境必须使用HTTPS（Nginx反向代理+SSL证书）
- API Key设置强密码
- 限制IP白名单（Nginx层）
- 资源包用完后自动按量计费，注意监控
