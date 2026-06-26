# Vibe Coding 可行性评估

> 描述功能/项目，AI 评估能否用 Cursor/Windsurf/Bolt 等工具独立实现，给出工具推荐和拆解路径。

## ✨ 功能
- ✅/⚠️/❌ 三级可行性判断
- 五维评分（复杂度/上下文/依赖/调试/综合）
- 推荐工具组合（Cursor/Windsurf/Bolt/v0 等）
- 任务拆解路径 + 时间估算
- 风险提示 + 实战建议

## 🚀 快速开始
```bash
export DEEPSEEK_API_KEY=your_key

python3 scripts/evaluate_vibe.py --idea "做一个小红书评论分析的 Chrome 插件"
python3 scripts/evaluate_vibe.py --idea "..." --skill "有基础"
```

## 📝 作者
[antonia-sz](https://github.com/antonia-sz) · MIT License
