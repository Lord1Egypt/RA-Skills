# 微信公众号自动发布技能

一键发布文章到微信公众号草稿箱，支持 Markdown/HTML 格式，自动美化排版。

## 功能特性

✅ **核心功能**
- 一键发布到草稿箱
- Markdown/HTML 自动转换
- 自动上传封面图
- 美化排版样式
- 中文编码修复（UTF-8）

✅ **技术优势**
- 解决 Unicode 转义问题
- 支持长文章（50000 字以内）
- 自动图片压缩

## 配置

### 1. 获取微信公众号配置

登录微信公众平台：https://mp.weixin.qq.com

**路径:** 设置与开发 → 基本配置

**需要:**
- `APPID` (公众号 ID)
- `APPSECRET` (应用密钥)

### 2. 设置环境变量

```bash
WECHAT_APPID=你的 APPID
WECHAT_APPSECRET=你的 APPSECRET
```

## 使用方法

### 方式 1: 命令行发布

```bash
python scripts/wechat_publish.py \
  --article "article.md" \
  --cover "cover.jpg" \
  --title "文章标题"
```

### 方式 2: Python 代码

```python
from wechat_publish import WeChatPublisher

publisher = WeChatPublisher(
    appid="你的 APPID",
    appsecret="你的 APPSECRET"
)

result = publisher.publish(
    article_path="article.md",
    cover_path="cover.jpg",
    title="文章标题"
)
```

## 脚本说明

### wechat_publish.py

主发布脚本，支持多种选项：

```bash
# 基本用法
python wechat_publish.py --article article.md --cover cover.jpg --title "标题"

# 指定摘要
python wechat_publish.py \
  --article article.md \
  --cover cover.jpg \
  --title "标题" \
  --digest "摘要"
```

## 常见问题

### Q1: Token 获取失败？

**原因:** IP 白名单未配置

**解决:**
1. 登录 mp.weixin.qq.com
2. 设置与开发 → 基本配置 → IP 白名单
3. 添加你的公网 IP

### Q2: 中文乱码？

**解决:** 脚本已自动处理 UTF-8 编码

### Q3: 图片上传失败？

**原因:** 图片格式不支持或太大

**解决:**
- 格式：JPG/PNG
- 大小：<10MB
- 尺寸：建议 1200x630px

## 最佳实践

### 封面图选择

- **尺寸:** 1200x630px (2.35:1)
- **格式:** JPG/PNG
- **大小:** <10MB

### 发布时间

**最佳时间:**
- 工作日：20:00-22:00
- 周末：10:00-12:00

## 更新日志

### v3.1.2 (2026-03-13)
- ✅ 精简代码，减少 token 使用
- ✅ 优化文件结构
- ✅ 清理私人信息

### v3.1.1 (2026-03-13)
- ✅ 手机阅读优化
- ✅ 代码块优化
- ✅ 表格样式优化

### v3.1.0 (2026-03-13)
- ✅ 官网配图自动下载
- ✅ 智能过滤图片

---

*版本：v3.1.2*  
*最后更新：2026-03-13*  
*作者：Robotqu*
