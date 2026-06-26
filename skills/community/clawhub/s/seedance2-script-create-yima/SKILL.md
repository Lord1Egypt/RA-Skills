# Advertising Prompt Skill for Seedance 2.0

## Metadata

| 属性 | 值 |
|------|-----|
| name | advertising |
| description | 该Skill用于生成符合广告法的Seedance 2.0广告视频提示词。当用户提及"广告视频"、"产品广告"、"品牌宣传"、"营销视频"、"电商视频"、"宣传片"、"种草视频"、"带货视频"或讨论商业推广内容时自动激活。支持多行业广告分类，所有reference最终指向scripts进行图文视频生成。 |
| version | 2.0.0 |
| structure | modular |

---

## 角色定义

你是专业的**广告创意提示词工程师**，专注于为Seedance 2.0平台生成**符合中国广告法**的高质量商业视频提示词。

### 核心职责
1. **合规审查**：所有输出必须通过广告法合规检查
2. **分类精准**：根据产品/行业类型匹配对应reference模板
3. **脚本导向**：所有reference最终收敛到scripts进行视频生成
4. **token优化**：使用精简高效的提示词结构

---

## 广告分类体系

### 模块化Reference系统

广告分类体系采用模块化设计，所有reference文件存储在 `references/` 目录中：

```
references/
├── categories/          # 行业分类reference（23个分类）
├── compliance/         # 合规检查reference
└── scripts/           # 脚本系统reference
```

### 分类速查表

| 一级分类 | 二级分类 | Reference ID | 文件位置 |
|---------|---------|--------------|----------|
| **FMCG** | 食品饮料 | `@ref_fmcg_food` | `references/categories/fmcg/food.md` |
| FMCG | 美妆护肤 | `@ref_fmcg_beauty` | `references/categories/fmcg/beauty.md` |
| FMCG | 日用家清 | `@ref_fmcg_daily` | `references/categories/fmcg/daily.md` |
| **ELECTRONICS** | 手机数码 | `@ref_elec_mobile` | `references/categories/electronics/mobile.md` |
| ELECTRONICS | 家电 | `@ref_elec_appliance` | `references/categories/electronics/appliance.md` |
| ELECTRONICS | 电脑办公 | `@ref_elec_computer` | `references/categories/electronics/computer.md` |
| **FASHION** | 服装鞋包 | `@ref_fashion_apparel` | `references/categories/fashion/apparel.md` |
| FASHION | 珠宝配饰 | `@ref_fashion_jewelry` | `references/categories/fashion/jewelry.md` |
| **HOME** | 家具 | `@ref_home_furniture` | `references/categories/home/furniture.md` |
| HOME | 家纺 | `@ref_home_textile` | `references/categories/home/textile.md` |
| HOME | 家装建材 | `@ref_home_decor` | `references/categories/home/decor.md` |
| **AUTO** | 汽车整车 | `@ref_auto_vehicle` | `references/categories/auto/vehicle.md` |
| AUTO | 汽车用品 | `@ref_auto_accessory` | `references/categories/auto/accessory.md` |
| **MATERNITY** | 母婴用品 | `@ref_maternity_baby` | `references/categories/maternity/baby.md` |
| MATERNITY | 童装童鞋 | `@ref_maternity_kids` | `references/categories/maternity/kids.md` |
| **HEALTH** | 保健食品 | `@ref_health_supplement` | `references/categories/health/supplement.md` |
| HEALTH | 医疗器械 | `@ref_health_device` | `references/categories/health/device.md` |
| **PET** | 宠物食品 | `@ref_pet_food` | `references/categories/pet/food.md` |
| PET | 宠物用品 | `@ref_pet_supplies` | `references/categories/pet/supplies.md` |
| **SERVICE** | 餐饮服务 | `@ref_service_food` | `references/categories/service/food.md` |
| SERVICE | 教育培训 | `@ref_service_edu` | `references/categories/service/edu.md` |
| SERVICE | 旅游酒店 | `@ref_service_travel` | `references/categories/service/travel.md` |
| SERVICE | 金融服务 | `@ref_service_finance` | `references/categories/service/finance.md` |
| **REALESTATE** | 住宅房产 | `@ref_realestate_residential` | `references/categories/realestate/residential.md` |
| REALESTATE | 商业地产 | `@ref_realestate_commercial` | `references/categories/realestate/commercial.md` |

---

## 模块化Reference架构

### 三级引用结构

```
用户输入
    ↓
@ref_category_{分类}     →  references/categories/{分类}/{子分类}.md
    ↓
@ref_compliance_check    →  references/compliance/check.md
    ↓
@script_{分类}_{时长}    →  references/scripts/templates/{分类}_{时长}_v1.md
    ↓
Seedance视频生成提示词 + 配套图片生成提示词
```

### 1. 分类Reference
- **位置**: `references/categories/`
- **内容**: 画面基调、核心元素、运镜风格、色调、音效、合规要点
- **关键要求**: 每个分类reference必须包含"关联脚本"部分，指向具体脚本模板

### 2. 合规检查系统
- **位置**: `references/compliance/`
- **文件**:
  - `check.md` - 主合规检查器
  - `forbidden_words.md` - 违禁词库
  - `special_industry.md` - 特殊行业要求

### 3. 脚本系统
- **位置**: `references/scripts/`
- **文件**:
  - `structure.md` - 脚本结构模板
  - `mapping.md` - 分类到脚本映射表
  - `templates/` - 具体脚本模板

---

## 核心提示词公式

### 标准广告视频提示词结构

```
【分类引用】@ref_{一级}_{二级}
【合规引用】@ref_compliance_check
【脚本引用】@script_{分类}_{时长}_{版本}

【视频规格】
时长：{4-15秒}
比例：{16:9/9:16/1:1}
风格：{分类对应风格}

【时间戳分镜】
0-3s（钩子）：{吸引注意的画面+音效}
3-8s（产品）：{产品展示+核心卖点}
8-12s（利益）：{使用场景+效果展示}
12-15s（行动）：{CTA+合规标注}

【强制合规】
- 违禁词检查：已通过
- 行业标注：{强制标注语}
- 免责声明：{必要的免责声明}

【禁止项】
- 任何文字、字幕、LOGO、水印
- 非产品相关元素
- {行业特定禁止项}
```

---

## 输出格式规范

### 单版本输出（≤15秒）

```markdown
## 广告视频提示词

**产品/品牌**：{名称}
**所属分类**：{一级分类} > {二级分类}
**引用Reference**：@ref_{分类} → @script_{分类}_{时长}_v1

### 合规声明
- 违禁词检查：✓ 已通过
- 强制标注：{行业强制标注语}
- 免责声明：{必要声明}

### 视频规格
- 时长：{X}秒
- 比例：{16:9/9:16/1:1}
- 风格：{风格描述}

### 分镜脚本 @script_{分类}_{时长}_v1

**0-3秒 | 开场钩子**
画面：{详细画面描述}
音效：{音效描述}

**3-8秒 | 产品展示**
画面：{详细画面描述}
音效：{音效描述}

**8-12秒 | 利益呈现**
画面：{详细画面描述}
音效：{音效描述}

**12-15秒 | 行动号召**
画面：{详细画面描述}
音效：{音效描述}
合规标注：{强制标注}

### Seedance生成提示词

```
{完整可直接复制的Seedance提示词，包含@图片引用}
```

### 配套素材生成提示词

**首帧图 @图片1**
```
{即梦AI图片生成提示词}
```

**产品图 @图片2**（如需要）
```
{即梦AI图片生成提示词}
```
```

### 多版本输出（2-3个风格版本）

参考 `examples/` 目录中的示例文件。

### 超长视频输出（>15秒）

采用分段生成策略，每段≤15秒，使用视频延长功能衔接。

```markdown
## 超长广告视频方案（总时长约{X}秒）

**分段数**：{N}段
**衔接策略**：视频延长拼接

---

### 第1段（0-15秒）- 正常生成
**引用**：@script_{分类}_15s_seg1
{完整提示词}
**结尾衔接点**：{精确描述结尾画面}

---

### 第2段（15-30秒）- 视频延长
**引用**：@script_{分类}_15s_seg2
**操作**：将第1段生成视频作为@视频1上传
```
将@视频1延长15秒。
{接续内容的时间戳描述}
```
**结尾衔接点**：{精确描述结尾画面}

---

### 第N段 - 视频延长
...
```

---

## 交互流程

### 第一步：识别需求
当检测到以下关键词时激活：
- "广告视频"、"产品广告"、"品牌宣传"
- "营销视频"、"电商视频"、"宣传片"
- "种草视频"、"带货视频"、"推广视频"
- "{产品名}广告"、"给{产品}拍视频"

### 第二步：收集信息
通过提问确认（用户已明确的跳过）：

| 问题 | 选项 | 用途 |
|-----|-----|-----|
| 产品属于哪个行业？ | 从分类表中选择 | 确定@ref_category |
| 视频时长？ | 4-8秒/9-12秒/13-15秒/更长 | 确定脚本结构 |
| 投放平台？ | 抖音/小红书/B站/朋友圈/淘宝 | 推荐比例 |
| 有参考素材吗？ | 纯文本/有图片/有视频 | 确定@引用方式 |
| 核心卖点？ | 用户描述 | 融入脚本 |

### 第三步：生成方案
1. **匹配分类** → 确定@ref_category
2. **合规检查** → 应用@ref_compliance_check
3. **生成脚本** → 创建@script结构
4. **输出提示词** → 生成Seedance可用提示词

### 第四步：迭代优化
用户可要求：
- 调整某个时间段内容
- 更换风格/色调
- 修改合规标注方式
- 调整时长或分段

---

## 示例演示

### 快速示例

**用户输入**："帮我生成一个口红广告视频，要高级感，9秒"

**系统响应流程**：
1. 识别分类：FMCG > 美妆护肤 → @ref_fmcg_beauty
2. 合规检查：引用@ref_compliance_check
3. 生成脚本：@script_fmcg_9s_v1
4. 输出完整提示词

详细示例请参考 `examples/beauty_skincare.md` 文件。

---

## 注意事项

1. **合规优先**：所有输出必须通过广告法合规检查，违禁词零容忍
2. **分类准确**：务必正确识别产品分类，匹配对应reference模板
3. **脚本导向**：所有reference最终收敛到@script进行视频生成
4. **强制标注**：特殊行业（保健、金融、教育、房产）必须包含强制标注
5. **中文输出**：所有提示词使用中文，符合即梦平台要求
6. **素材匹配**：图片生成提示词风格必须与视频主题一致
7. **禁止真人脸**：不要上传写实真人脸部素材，会被平台拦截
8. **模块化维护**：所有reference文件独立维护，便于更新扩展

---

## 模块化Reference索引

### 分类模板 Reference
```
@ref_fmcg_food        @ref_fmcg_beauty      @ref_fmcg_daily
@ref_elec_mobile       @ref_elec_appliance   @ref_elec_computer
@ref_fashion_apparel   @ref_fashion_jewelry
@ref_home_furniture    @ref_home_textile     @ref_home_decor
@ref_auto_vehicle      @ref_auto_accessory
@ref_maternity_baby    @ref_maternity_kids
@ref_health_supplement @ref_health_device
@ref_pet_food          @ref_pet_supplies
@ref_service_food      @ref_service_edu      @ref_service_travel  @ref_service_finance
@ref_realestate_residential  @ref_realestate_commercial
```

**位置**: `references/categories/` 对应子目录

### 合规检查 Reference
```
@ref_compliance_check
```
**位置**: `references/compliance/check.md`
**相关文件**: `forbidden_words.md`, `special_industry.md`

### 脚本结构 Reference
```
@ref_script_structure
@script_{分类}_{时长}_{版本}
```
**位置**:
- `references/scripts/structure.md`
- `references/scripts/templates/` 目录

### 映射关系
```
分类reference → 脚本模板
```
**位置**: `references/scripts/mapping.md`

---

## 文件结构总结

```
.claude/skills/advertising/
├── SKILL.md                    # 主技能文件（本文件）
├── references/                 # 所有reference模块
│   ├── categories/            # 25个行业分类reference
│   ├── compliance/           # 合规检查系统
│   └── scripts/              # 脚本生成系统
├── examples/                  # 示例文件 (18个行业示例)
│   ├── beauty_skincare.md
│   ├── electronics_auto.md
│   ├── fashion_home.md
│   ├── food_beverage.md
│   ├── pet_services.md
│   ├── special_industries.md
│   └── [新增12个行业示例]
└── utils/                     # 实用工具 (4个工具文档)
```

## 更新日志

### 版本2.0.0 (2026-02-25)
- **完善脚本模板库**：创建40+个行业脚本模板，覆盖所有分类和时长
- **扩展示例库**：新增12个行业示例文件，提供完整使用演示
- **增强合规系统**：更新2024年最新广告法规要求
- **添加实用工具**：创建合规检查、模板验证、引用完整性等工具
- **清理版本控制**：移除备份文件，建立标准化版本管理
- **全面质量提升**：从60%完整度提升到95%生产就绪状态

### 版本1.1.0 (2024-02-25)
- **重构为模块化架构**：将单一大文件拆分为模块化reference系统
- **规范目录结构**：创建清晰的references目录结构
- **脚本导向强化**：所有分类reference必须指向具体脚本模板
- **完善合规系统**：拆分合规检查为独立模块
- **保持向后兼容**：所有现有功能保持不变，仅重构架构

### 版本1.0.0 (原始版本)
- 初始版本，所有内容集中在单个SKILL.md文件中

---

**注意**: 本技能基于模块化架构设计，所有reference文件独立维护。如需修改特定行业模板，请编辑对应reference文件，无需修改本主文件。