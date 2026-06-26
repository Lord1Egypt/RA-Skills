# 智能提示构建器 (Smart Prompt Builder)

根据语料库检索结果生成优化的写作提示，支持多种场景和上下文注入。

## 功能特性

- ✅ **4种写作场景**: 描写(description)、对话(dialogue)、动作(action)、情感(emotion)
- ✅ **Voice Profile注入**: 从YAML文件加载风格配置
- ✅ **上下文注入**: 支持前文摘要、角色状态、当前场景
- ✅ **语料库集成**: 自动格式化检索结果
- ✅ **结构化输出**: 系统提示 + 用户提示 + 约束条件
- ✅ **富文本渲染**: 使用rich库美化终端输出
- ✅ **文件导出**: 支持纯文本格式导出
- ✅ **完整错误处理**: 友好的错误提示

## 安装依赖

```bash
pip install -r scripts/requirements.txt
```

## 使用方法

### 基本用法

```bash
# 描写场景
python scripts/build_prompt.py --scene-type description \
  --context '{"scene": "雨中的街道"}'

# 对话场景
python scripts/build_prompt.py --scene-type dialogue \
  --context '{"characters": {"主角": "侦探"}}'
```

### 使用Voice Profile

创建 `style.yml` 配置文件：

```yaml
voice_tags:
  - 温柔
  - 叙事性
  - 略带忧伤

speed: 0.9
tone: 亲切的讲述者语气
emotional_predisposition: 0.3
```

使用配置：

```bash
python scripts/build_prompt.py --scene-type description \
  --style-file assets/style.yml \
  --context '{"scene": "森林"}'
```

### 集成语料库检索

```bash
python scripts/build_prompt.py --scene-type dialogue \
  --corpus-results '[{
    "title": "咖啡馆对话",
    "content": "林风：这咖啡真香。苏雨：specialty豆子，刚到货。",
    "relevance_score": 0.92
  }, {
    "title": "对话节奏",
    "content": "注意停顿和动作描写",
    "relevance_score": 0.85
  }]'
```

### 完整示例

```bash
python scripts/build_prompt.py --scene-type action \
  --context '{
    "summary": "主角被敌人包围",
    "characters": {"主角": "重伤", "敌人": "5人"},
    "scene": "废弃工厂"
  }' \
  --style-file style.yml \
  --corpus-results '[{"title": "打斗场景", "content": "...", "relevance_score": 0.9}]' \
  --output prompt.txt
```

### 导出文件

```bash
# 输出到文件（纯文本格式）
python scripts/build_prompt.py --scene-type emotion \
  --output output/prompt.txt
```

## CLI参数

| 参数 | 必需 | 说明 | 示例 |
|------|------|------|------|
| `--scene-type` | ✅ | 场景类型 | `description`, `dialogue`, `action`, `emotion` |
| `--context` | ❌ | 上下文信息(JSON) | `{"scene": "森林"}` |
| `--style-file` | ❌ | Voice Profile文件 | `style.yml` |
| `--corpus-results` | ❌ | 语料库结果(JSON) | `[{"title": "...", "content": "..."}]` |
| `--output` | ❌ | 输出文件路径 | `prompt.txt` |

## 上下文支持字段

```json
{
  "summary": "前文摘要",
  "characters": {
    "角色名": "状态描述"
  },
  "scene": "当前场景",
  "previous_output": "前文输出"
}
```

## 语料库结果格式

```json
[
  {
    "title": "结果标题",
    "content": "检索内容",
    "relevance_score": 0.95
  }
]
```

## Voice Profile配置

```yaml
voice_tags: ["风格标签1", "风格标签2"]
speed: 0.9          # 语速 (0.5-2.0)
tone: "语气描述"
emotional_predisposition: 0.3  # 情感倾向 (-1.0 到 1.0)
```

## 场景约束

### description (描写)
- 使用五感描写法（视觉、听觉、嗅觉、味觉、触觉）
- 包含至少3个具体的细节描写
- 使用比喻或拟人手法增强表现力
- 保持描写节奏的层次感

### dialogue (对话)
- 对话需符合角色身份和性格特征
- 每段对话不超过3轮
- 包含非语言动作描述（动作、表情）
- 使用口语化表达，避免书面腔

### action (动作)
- 使用短句增强节奏感
- 动作描写需连贯有序
- 包含细节（手部动作、表情变化等）
- 适当使用动词强化表现力

### emotion (情感)
- 将抽象情感转化为具体意象
- 描写身体反应（心跳、温度、手势等）
- 避免直接陈述情感词语
- 展现情感的层次变化

## 输出格式

### 终端输出（富文本）
- 蓝色面板：系统提示
- 绿色面板：用户提示
- 黄色面板：约束条件
- 表格：元数据

### 文件输出（纯文本）
```
============================================================
【系统提示】
============================================================
...

============================================================
【用户提示】
============================================================
...

============================================================
【约束条件】
============================================================
• ...

============================================================
【元数据】
============================================================
```

## 错误处理

- ✅ 无效的scene-type：显示可用选项
- ✅ 缺失的style文件：友好的错误提示
- ✅ 无效的JSON格式：显示解析错误
- ✅ 文件不存在：显示路径错误

## 许可证

MIT License
