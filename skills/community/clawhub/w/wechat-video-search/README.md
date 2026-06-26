# 微信视频号视频搜索技能

## 状态

✅ 技能已创建完成  
⚠️ **需要配置 TikHub Token 权限**

## 403 错误解决方案

测试时发现 API 返回 403 错误：
```
API Token lacks required permissions
```

**原因**：当前的 TikHub Token 缺少视频号搜索 API 的权限。

**解决方法**：
1. 登录 TikHub 用户后台：https://user.tikhub.io/dashboard/api
2. 找到您正在使用的 API Token
3. 编辑 Token 权限，勾选 **WeChat Channels API** 相关权限
4. 保存后重试

## 技能结构

```
wechat-video-search/
├── SKILL.md                      # 技能说明文档
├── skill.json                    # 技能配置
├── _meta.json                    # 元数据
├── README.md                     # 本文件
└── scripts/
    └── wechat_video_search.py    # 搜索脚本
```

## 使用方法

```bash
# 简单搜索
python3 scripts/wechat_video_search.py "餐饮 鸡鸭鹅"

# 输出原始 JSON
python3 scripts/wechat_video_search.py "熟食" --raw
```

## API 端点

- **域名**: https://api.tikhub.dev（中国大陆用户）
- **路径**: /api/v1/wechat_channels/fetch_search_latest
- **方法**: GET
- **参数**: keywords（URL 编码）

## 返回数据示例

```json
{
  "code": 200,
  "data": [
    {
      "video_id": "视频 ID",
      "desc": "视频描述",
      "author": {
        "nickname": "作者昵称"
      },
      "statistics": {
        "play_count": 播放量，
        "digg_count": 点赞数
      },
      "video": {
        "play_addr": {
          "url_list": ["视频下载链接"]
        }
      }
    }
  ]
}
```

## 与抖音搜索的区别

| 特性 | 抖音搜索 | 视频号搜索 |
|------|---------|-----------|
| 域名 | api.tikhub.io | api.tikhub.dev |
| 排序参数 | 支持（综合/点赞/最新） | 暂不支持 |
| 时间筛选 | 支持 | 暂不支持 |
| 返回数据 | 丰富（含分页信息） | 基础（视频列表） |
| 主要用途 | 深度分析 | 快速获取视频链接 |
