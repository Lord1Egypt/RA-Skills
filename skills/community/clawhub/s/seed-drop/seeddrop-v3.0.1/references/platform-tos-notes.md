# 平台服务条款关键摘要

## B站

- 搜索接口: `api.bilibili.com/x/web-interface/wbi/search`
- 评论接口: `api.bilibili.com/x/v2/reply/add`（需 CSRF=bili_jct）
- 搜索频率建议 ≤30 次/小时
- 评论频率建议 ≤50 条/天
- 重复内容会被自动过滤
- 对服务器 IP 无特殊限制

## 百度贴吧

- BDUSS 有效期 6 个月+，非常稳定
- Cookie-Editor 导出的是 BDUSS_BFESS（不可用），必须从网络请求头获取 BDUSS
- 回帖需先获取 tbs token
- 回帖频率建议 ≤30 条/天
- 重复内容会被系统删除
- STOKEN 用于写操作验证

## 知乎

- 搜索接口: `zhihu.com/api/v4/search_v3`
- 回答需要 x-zse-96 签名（当前用 browser 模式绕过）
- z_c0 有效期约 30 天
- 对服务器 IP 有限制，高频访问触发验证码
- 回答/评论有内容审核

## 小红书

- 无公开写入 API，回复操作通过浏览器模拟
- 搜索接口: `edith.xiaohongshu.com/api/sns/web/v1/search/notes`（需 X-s/X-t 签名）
- Cookie 有效期极短: ~12 小时
- 多层反爬: Header + 行为指纹 + 设备ID + WASM
- 强烈建议配合 SocialVault 自动续期
- 评论区不允许外部链接
- 请求间隔不低于 3 秒
