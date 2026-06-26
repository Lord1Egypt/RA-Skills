# 项目结构规范

## 目录结构

```
Xtranslate/
├── SKILL.md                  # 核心指令 + 元数据
├── README.md                 # 项目说明（可选）
├── requirements.txt          # Python依赖
├── Xtranslate.spec           # PyInstaller打包配置
│
├── src/                      # 源代码目录
│   ├── __init__.py
│   ├── config.py             # 全局配置
│   ├── main.py               # CLI入口
│   ├── gui.py                # GUI入口
│   ├── translator.py         # 翻译引擎
│   ├── file_handler.py       # 文件处理器
│   ├── analyzer.py           # 文本分析
│   ├── formatter.py          # 排版优化
│   ├── cad_handler.py        # CAD处理
│   ├── crypto_utils.py       # 加密工具
│   └── ...
│
├── templates/                # 代码模板
│   ├── module.py.md
│   └── translator_engine.py.md
│
├── examples/                 # 代码示例
│   ├── good.md
│   └── anti-pattern.md
│
├── references/               # 规范参考
│   ├── naming-convention.md
│   └── project-structure.md
│
├── scripts/                  # 辅助脚本
│   └── check-deps.py
│
├── build/                    # 构建输出
├── dist/                     # 分发文件
├── output/                   # 翻译结果输出
└── tmp/                      # 临时文件
```

## 模块组织原则

1. **单一职责**: 每个模块只负责一类功能
   - `file_handler.py` - 文件读写
   - `translator.py` - 翻译逻辑
   - `analyzer.py` - 文本分析

2. **依赖方向**: 底层模块不依赖上层模块
   ```
   gui.py → main.py → translator.py → config.py
   ```

3. **配置集中**: 所有配置项集中在 `config.py`

4. **工具独立**: 通用工具（如加密）放在独立模块
