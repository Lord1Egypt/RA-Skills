# 视频总结模板

## 用途

此模板用于生成视频总结的 Markdown 文档，由 `analyze-subtitles-ai.py` 脚本调用。

## 模板变量

| 变量 | 说明 | 来源 |
|------|------|------|
| `{title}` | 视频标题 | 元数据 |
| `{tags}` | 标签列表 | AI 生成 |
| `{author}` | UP 主名称 | 元数据 |
| `{thumbnail}` | 封面图 URL | 元数据 |
| `{note}` | 100-200 字概述 | AI 生成 |
| `{video_url}` | 视频链接 | 元数据 |
| `{duration}` | 视频时长 | 元数据 |
| `{uploader}` | UP 主 | 元数据 |
| `{subtitle_source}` | 字幕来源 | 元数据 |
| `{key_points}` | 核心要点 | AI 生成 |
| `{concepts}` | 关键概念 | AI 生成 |
| `{warnings}` | 注意事项 | AI 生成 |
| `{screenshots}` | 视频帧截图 | OSS 上传结果 |
| `{summary}` | 最终总结 | AI 生成 |
| `{timestamp}` | 生成时间 | 自动生成 |
| `{version}` | 技能版本 | 硬编码 |

## 修改模板

直接编辑 `summary.md` 文件即可修改输出格式。

**示例：添加新章节**

```markdown
## 📚 关键概念

{concepts}

## 🎯 核心要点

{key_points}

## 🆕 新增章节

这里是新章节内容...

```

## 测试模板修改

```bash
# 处理一个视频测试新模板
./scripts/video-summarize.sh "视频 URL" /tmp/test-output

# 查看生成的总结
cat /tmp/test-output/summary.md
```

## 注意事项

1. **保留变量名** - `{xxx}` 格式的变量不要删除，否则对应内容不会显示
2. **Markdown 格式** - 保持标准 Markdown 语法，确保 Notion 兼容
3. **变量位置** - 变量可以放在模板任意位置，按逻辑组织即可

---

**版本:** v1.0.13  
**最后更新:** 2026-04-06
