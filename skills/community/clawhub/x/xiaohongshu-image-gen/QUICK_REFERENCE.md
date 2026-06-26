# 快速参考 - xiaohongshu-image-gen

## 一图胜千言

```bash
# 家装（默认）
xiaohongshu-image-gen --prompt "现代简约客厅，白色沙发+原木茶几"

# 美食
xiaohongshu-image-gen --prompt "精致日式拉面，热气腾腾" --style "美食"

# 穿搭
xiaohongshu-image-gen --prompt "春夏季轻盈连衣裙，INS风街拍" --style "穿搭"

# 旅行
xiaohongshu-image-gen --prompt "洱海日落，风景如画" --style "旅行" --size "9:16"
```

## 常见问题

**Q: 没有 API Key 怎么办？**
A: 系统会自动降级使用本地 `image-generate` 技能，无需配置。

**Q: 图片生成失败？**
A: 检查 API Key 是否正确，或本地 image-generate 技能是否已安装。

**Q: 如何批量生成？**
A: 使用 shell 脚本循环调用，或配合 `social-publisher` 使用。

## 文件位置

- 安装目录: `~/.openclaw/skills/xiaohongshu-image-gen/`
- 主程序: `source/xiaohongshu_image_gen.py`
- 依赖: `requirements.txt`

## 更多信息

详见 [README.md](README.md) 和 [SKILL.md](SKILL.md)