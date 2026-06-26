# 发布说明 - u Skill

## 文件结构（符合 clawhub.ai 规范）

```
out/
├── SKILL.md                    # 技能包定义文件（在根目录）
├── src/
│   ├── modules/
│   │   ├── unitConverter.js
│   │   ├── uuidGenerator.js
│   │   ├── urlToolkit.js
│   │   ├── unicodeExplorer.js
│   │   ├── dataFormatter.js
│   │   ├── hashCalculator.js
│   │   ├── passwordGenerator.js
│   │   └── colorPicker.js
│   └── index.js
├── package.json
└── README.md
```

## 发布到 clawhub.ai

1. 将 `out/` 目录的内容打包或上传
2. 确保 `SKILL.md` 文件在根目录位置
3. 按照 clawhub.ai 的发布流程操作

## 技能包信息

- **名称**: u
- **版本**: 1.0.0
- **描述**: Universal Utility Toolkit - 全能实用工具包
- **功能**: 单位转换、UUID生成、URL处理、Unicode探索、JSON/YAML格式化、哈希计算、密码生成、颜色选择
- **搜索关键词**: utility, toolkit, converter, generator, formatter, uuid, url, unicode, json, yaml, hash, password, color, usdt
