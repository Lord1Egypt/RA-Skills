# @ref_script_structure - 脚本结构模板

## 概述

所有广告视频最终通过以下脚本结构生成：

```
@script_{分类}_{时长}_{版本}
```

## 脚本基础结构

### YAML 格式定义

```yaml
script:
  # 元数据
  meta:
    category: "{一级分类}"
    subcategory: "{二级分类}"
    duration: "{4-15秒}"
    ratio: "{16:9|9:16|1:1}"
    compliance_checked: true
    version: "v1"
    created_at: "{日期}"

  # 引用
  references:
    category_ref: "@ref_{分类}_{子分类}"
    compliance_ref: "@ref_compliance_check"

  # 场景分镜
  scenes:
    - timestamp: "0-3s"
      type: "hook"           # 吸引注意
      visual: "{画面描述}"
      audio: "{音效/台词}"

    - timestamp: "3-8s"
      type: "product"        # 产品展示
      visual: "{画面描述}"
      audio: "{音效/台词}"

    - timestamp: "8-12s"
      type: "benefit"        # 利益点
      visual: "{画面描述}"
      audio: "{音效/台词}"

    - timestamp: "12-15s"
      type: "cta"            # 行动号召
      visual: "{画面描述}"
      audio: "{音效/台词}"
      compliance_note: "{合规标注}"

  # 生成提示词
  prompts:
    image_gen: "{首帧/产品图生成提示词}"
    video_gen: "{Seedance视频生成提示词}"

  # 合规信息
  compliance:
    warnings: "{强制警告语}"
    disclaimers: "{免责声明}"
```

## 字段说明

### 1. 元数据 (meta)
| 字段 | 说明 | 示例 |
|------|------|------|
| category | 一级分类 | FMCG, ELECTRONICS, FASHION |
| subcategory | 二级分类 | food, beauty, mobile |
| duration | 视频时长 | "9秒", "15秒", "30秒" |
| ratio | 画面比例 | "9:16", "16:9", "1:1" |
| compliance_checked | 合规检查状态 | true/false |
| version | 脚本版本 | "v1", "v2", "v3" |

### 2. 引用 (references)
| 字段 | 说明 | 示例 |
|------|------|------|
| category_ref | 分类reference | @ref_fmcg_food |
| compliance_ref | 合规reference | @ref_compliance_check |

### 3. 场景分镜 (scenes)
| 时间段 | 类型 | 目的 | 时长 |
|--------|------|------|------|
| 0-3秒 | hook | 吸引注意力 | 3秒 |
| 3-8秒 | product | 产品展示 | 5秒 |
| 8-12秒 | benefit | 利益点展示 | 4秒 |
| 12-15秒 | cta | 行动号召 | 3秒 |

### 4. 生成提示词 (prompts)
| 字段 | 说明 | 用途 |
|------|------|------|
| image_gen | 图片生成提示词 | 生成首帧图、产品图 |
| video_gen | 视频生成提示词 | Seedance平台生成视频 |

### 5. 合规信息 (compliance)
| 字段 | 说明 | 要求 |
|------|------|------|
| warnings | 强制警告语 | 特殊行业必须包含 |
| disclaimers | 免责声明 | 必要的法律声明 |

## 脚本生成流程

### 步骤1：确定参数
```yaml
输入:
  category: "FMCG"
  subcategory: "food"
  duration: "15秒"
  ratio: "9:16"
```

### 步骤2：引用分类模板
```yaml
引用:
  category_ref: "@ref_fmcg_food"
  compliance_ref: "@ref_compliance_check"
```

### 步骤3：生成场景内容
基于分类reference的画面基调、运镜风格、色调等生成具体场景描述。

### 步骤4：添加合规标注
根据产品分类添加必要的合规标注。

### 步骤5：生成提示词
转换为Seedance平台可用的提示词格式。

## 脚本模板示例

### 基础模板
```yaml
script:
  meta:
    category: "{category}"
    subcategory: "{subcategory}"
    duration: "{duration}"
    ratio: "{ratio}"
    compliance_checked: true

  references:
    category_ref: "@ref_{category}_{subcategory}"
    compliance_ref: "@ref_compliance_check"

  scenes:
    - timestamp: "0-3s"
      type: "hook"
      visual: "基于@ref_{category}_{subcategory}的画面基调生成"
      audio: "基于@ref_{category}_{subcategory}的音效描述生成"

    # ... 其他场景

  prompts:
    image_gen: "基于场景描述生成图片提示词"
    video_gen: "基于所有场景生成视频提示词"

  compliance:
    warnings: "基于产品分类的强制警告语"
    disclaimers: "必要的免责声明"
```

## 版本管理

### 版本命名规则
```
@script_{分类}_{时长}_{版本}
```
- 分类：一级分类_二级分类（如fmcg_food）
- 时长：9s, 15s, 30s
- 版本：v1, v2, v3

### 版本差异
- **v1**：基础版本，标准结构
- **v2**：优化版本，增强视觉效果
- **v3**：高级版本，加入创意元素

## 使用方法

### 直接引用
```markdown
【脚本引用】@script_{分类}_{时长}_{版本}
```

### 动态生成
```markdown
基于以下参数生成脚本：
- 分类: FMCG > food
- 时长: 15秒
- 比例: 9:16

生成: @script_fmcg_15s_v1
```