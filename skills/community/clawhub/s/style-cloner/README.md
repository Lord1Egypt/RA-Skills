# 文章风格克隆助手

> 提供参考文章 + 原始素材，AI 分析写作风格并改写，输出3个强度版本。

## ✨ 功能

- **风格精准分析**：语言风格、句式偏好、开头结尾套路、高频词汇
- **三强度版本**：60% / 80% / 100% 风格克隆，总有一款合适
- **多平台适配**：小红书 / 公众号 / 知乎 / LinkedIn 各平台风格优化
- **迭代优化**：对结果提出修改意见，继续打磨

## 🚀 使用方式

### 作为 OpenClaw Skill 使用

```
参考文章：
[粘贴1-5篇你想模仿的文章]

---

原始素材：
[你想改写的内容]
```

### 作为 CLI 工具使用

```bash
export DEEPSEEK_API_KEY=your_key_here

# 基本用法
python3 scripts/clone_style.py \
  --refs "参考文章内容" \
  --content "原始素材内容"

# 完整参数
python3 scripts/clone_style.py \
  --refs /path/to/reference.txt \
  --content /path/to/draft.md \
  --intensity 80 \       # 风格强度 0-100，默认80
  --length 1500 \        # 目标字数
  --platform "小红书" \  # 目标平台
  --output ~/result.md   # 输出文件
```

## 📊 分析维度

| 维度 | 示例 |
|------|------|
| 语言风格 | 口语化、亲切感强、多用第一人称 |
| 句式特点 | 短句为主，善用破折号和感叹号 |
| 开头套路 | 常以一个反问句开头引发共鸣 |
| 结尾套路 | 以「你觉得呢？」等互动句结尾 |
| 特色词汇 | 「真的」「其实」「说真的」 |

## 📦 环境要求

- Python 3.8+
- 无需额外依赖（只用标准库）
- 设置 `DEEPSEEK_API_KEY` 或 `OPENAI_API_KEY` 环境变量

## 📝 作者

[antonia-sz](https://github.com/antonia-sz) · Powered by OpenClaw

## 📄 License

MIT
