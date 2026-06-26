# 微信公众号 API 参考

## 基础信息

- **API 域名**: `https://api.weixin.qq.com`
- **Access Token**: 每次调用前重新获取，有效期 7200 秒
- **必需前提**: 调用 IP 已在 mp.weixin.qq.com 后台加入白名单

## 核心 API 端点

| 功能 | 方法 | URL | 说明 |
|------|------|-----|------|
| 获取 Access Token | GET | `/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}` | 返回 `{access_token, expires_in}` |
| 上传永久图片素材 | POST | `/cgi-bin/material/add_material?access_token={token}&type=image` | multipart/form-data，< 2MB |
| 上传临时图片素材 | POST | `/cgi-bin/media/upload?access_token={token}&type=image` | multipart/form-data，< 2MB，3天有效期 |
| 上传临时 thumb 素材 | POST | `/cgi-bin/media/upload?access_token={token}&type=thumb` | **< 64KB**，3天有效期 |
| 新增草稿 | POST | `/cgi-bin/draft/add?access_token={token}` | JSON body，草稿接口**只接受永久素材 media_id** |

## 草稿接口 media_id 规则（关键）

```
草稿 thumb_media_id 必须是永久素材！
不能用 /media/upload?type=thumb 返回的临时 media_id
```

草稿支持的封面图类型：`image` 类型永久素材（add_material）。

## PowerShell multipart 上传模板

```powershell
$token = "..."
$filePath = "C:\path\to\cover.png"
$boundary = [guid]::NewGuid().ToString("N")
$fileBytes = [System.IO.File]::ReadAllBytes($filePath)
$fileName = [System.IO.Path]::GetFileName($filePath)

$header = "--$boundary`r`nContent-Disposition: form-data; name=`"media`"; filename=`"$fileName`"`r`nContent-Type: image/png`r`n`r`n"
$footer = "`r`n--$boundary--`r`n"
$binHeader = [System.Text.Encoding]::UTF8.GetBytes($header)
$binFooter = [System.Text.Encoding]::UTF8.GetBytes($footer)

$memStream = New-Object System.IO.MemoryStream
$memStream.Write($binHeader, 0, $binHeader.Length)
$memStream.Write($fileBytes, 0, $fileBytes.Length)
$memStream.Write($binFooter, 0, $binFooter.Length)
$body = $memStream.ToArray()
$memStream.Close()

$url = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=$token&type=image"
$resp = Invoke-WebRequest -Uri $url -Method POST -Body $body -ContentType "multipart/form-data; boundary=$boundary"
$resp.Content
```

## Access Token 刷新时机

- Token 有效期 2 小时
- 建议每次写草稿前重新获取，不要复用超过 30 分钟的 token
- 返回 errcode 40001 时立即重新获取

## 草稿 JSON 结构

```json
{
  "articles": [{
    "title": "文章标题",
    "author": "作者名（可选）",
    "digest": "摘要（可选，不超过54字）",
    "content": "<p>HTML正文...</p>",
    "content_source_url": "",
    "thumb_media_id": "永久素材 media_id",
    "need_open_comment": 1,
    "only_fans_can_comment": 0
  }]
}
```

## 错误码速查

| errcode | errmsg | 含义 | 解决方案 |
|---------|--------|------|---------|
| 40164 | invalid ip hint | IP不在白名单 | mp后台添加 112.8.202.216 |
| 40006 | size limit | media 尺寸超限 | 压缩图片 |
| 40007 | invalid media_id | 无效 media_id | 用 add_material 永久素材接口 |
| 40013 | invalid appid | appid 不合法 | 检查 wechat_credentials.json |
| 40001 | invalid credential | access_token 无效/过期 | 重新获取 token |
| 41006 | media_id missing | 缺少 thumb_media_id | 确保封面图已上传 |
| 44001 | empty content | 空内容 | 检查 Markdown 内容 |
