# WeChat Look - 微信文章阅读工具

一个专门为 OpenClaw 设计的微信文章读取技能，能够自动处理URL规范化并提取文章内容。

## 快速开始

### 安装

```bash
# 从本地目录安装
openclaw skill install ./skills/wechat-look

# 使用完整路径
openclaw skill install ~/.openclaw/workspace/skills/wechat-look
```

### 使用示例

在 OpenClaw 对话中：

```
读取微信文章 https://mp.weixin.qq.com/s/D7vSSNGCQFT4NAdY6loPWA
```

或者：

```
帮我读这篇文章：https://mp.weixin.qq.com/s/S3AF2BKqRYcxHaI8uZ71BA
```

## 功能特性

✅ **智能URL处理**
- 自动检测微信文章URL
- 自动添加`scene=1`参数绕过验证码
- 正确处理现有查询参数

✅ **内容提取**
- 从HTML中提取纯文本内容
- 保留文章标题和作者信息
- 提供结构化输出格式

✅ **错误处理**
- 友好的错误提示
- 网络异常重试机制
- 无效URL检测

## 技术实现

### Python 核心逻辑

```python
def normalize_wechat_url(url):
    """规范化微信文章URL"""
    if not url.startswith('https://mp.weixin.qq.com/s/'):
        return url
    
    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
    
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    params['scene'] = ['1']
    
    new_query = urlencode(params, doseq=True)
    new_url = urlunparse((
        parsed.scheme, parsed.netloc, parsed.path,
        parsed.params, new_query, parsed.fragment
    ))
    
    return new_url
```

### 工作流程

1. **输入验证**: 检查URL格式
2. **URL规范化**: 添加`scene=1`参数
3. **内容获取**: 使用浏览器工具读取页面
4. **文本提取**: 从HTML中提取正文内容
5. **结果格式化**: 返回结构化数据

## 测试用例

```python
# 测试用例
test_urls = [
    "https://mp.weixin.qq.com/s/D7vSSNGCQFT4NAdY6loPWA",
    "https://mp.weixin.qq.com/s/S3AF2BKqRYcxHaI8uZ71BA?param=value",
    "https://example.com/not-wechat"  # 非微信URL
]

# 预期结果
# URL 1 -> https://mp.weixin.qq.com/s/D7vSSNGCQFT4NAdY6loPWA?scene=1
# URL 2 -> https://mp.weixin.qq.com/s/S3AF2BKqRYcxHaI8uZ71BA?param=value&scene=1
# URL 3 -> https://example.com/not-wechat (保持不变)
```

## 注意事项

⚠️ **访问限制**: 微信有访问频率限制，请合理使用

⚠️ **安全规范**: 所有外部内容标记为未信任源

⚠️ **验证码**: 确保URL包含正确的`scene=1`参数

## 故障排除

### Q: 遇到验证码怎么办？
A: 确保URL正确包含`scene=1`参数，格式为`?scene=1`而不是`&scene=1`

### Q: 无法获取文章内容？
A: 检查网络连接，确认URL有效，等待页面完全加载

### Q: 提取的内容不完整？
A: 某些文章内容可能需要JavaScript渲染，当前版本可能无法完全捕获动态内容

## 贡献指南

欢迎提交Issue和Pull Request来改进这个技能！

1. 遵循OpenClaw技能开发规范
2. 添加适当的测试用例
3. 更新文档和示例