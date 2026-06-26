# 广告脚本生成工具

自动生成广告脚本的工具，支持多种模板和自定义参数。

## 功能特性

- 基于模板的脚本生成
- 自定义参数支持
- 批量生成能力
- 预览和验证功能

## 使用方法

### 基本生成

```bash
python script_generator.py --category "electronics" --duration 15 --ratio "9:16" --style "科技现代"
```

### 使用自定义参数

```bash
python script_generator.py --template elec_15s_v1 --params '{"brand": "小米", "product": "手机"}'
```

### 批量生成

```bash
python script_generator.py --batch config.json --output generated_scripts/
```

## 参数说明

### 核心参数
- `--category`: 产品类别 (electronics, fmcg, health, etc.)
- `--duration`: 视频时长 (9, 15, 30秒)
- `--ratio`: 视频比例 (9:16, 16:9, 1:1)
- `--style`: 广告风格描述

### 自定义参数
- `--template`: 指定模板文件
- `--params`: JSON格式的自定义参数
- `--brand`: 品牌名称
- `--product`: 产品名称

### 输出控制
- `--output`: 输出目录
- `--preview`: 预览模式，不生成文件
- `--validate`: 生成后验证脚本

## 生成流程

1. **参数解析**: 解析用户输入的参数
2. **模板选择**: 根据类别和时长选择最合适的模板
3. **参数替换**: 将自定义参数应用到模板中
4. **合规检查**: 自动添加合规标注
5. **格式验证**: 验证生成的脚本格式正确性

## 模板系统

### 模板结构
```yaml
template:
  name: "电子产品15秒模板"
  category: "electronics"
  duration: 15
  ratio: "9:16"

parameters:
  brand: "{{brand}}"
  product: "{{product}}"
  style: "{{style}}"

script:
  scenes:
    - time: "0-3秒"
      description: "{{brand}} {{product}}展示，{{style}}风格"
      audio: "科技BGM，界面音效"
```

### 变量替换
支持以下变量：
- `{{brand}}`: 品牌名称
- `{{product}}`: 产品名称
- `{{style}}`: 风格描述
- `{{duration}}`: 视频时长
- `{{ratio}}`: 视频比例

## 批量配置

batch_config.json 示例：

```json
{
  "jobs": [
    {
      "id": "xiaomi_phone_15s",
      "category": "electronics",
      "duration": 15,
      "ratio": "9:16",
      "params": {
        "brand": "小米",
        "product": "智能手机",
        "style": "科技现代"
      }
    },
    {
      "id": "cocacola_drink_9s",
      "category": "fmcg",
      "duration": 9,
      "ratio": "9:16",
      "params": {
        "brand": "可口可乐",
        "product": "汽水饮料",
        "style": "清凉解渴"
      }
    }
  ],
  "output_dir": "generated_scripts",
  "validate_output": true
}
```

## 输出格式

生成的脚本文件包含：

- 完整的广告视频提示词
- Seedance生成提示词
- 图片生成提示词
- 合规声明和标注

## 依赖项

- Python 3.8+
- Jinja2 (模板引擎)
- PyYAML

## 安装

```bash
pip install Jinja2 PyYAML
```

## 示例

```python
from script_generator import ScriptGenerator

generator = ScriptGenerator()

# 生成单个脚本
script = generator.generate(
    category="electronics",
    duration=15,
    brand="小米",
    product="智能手机",
    style="科技现代"
)

print(script['seedance_prompt'])
print(script['image_prompt'])
```