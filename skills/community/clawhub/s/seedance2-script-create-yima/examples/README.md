# 广告技能示例库

本目录包含18个行业广告示例，展示如何使用Advertising Skill生成符合广告法的Seedance视频提示词。

## 示例覆盖行业

### FMCG快消品 (4个)
- `beauty_skincare.md` - 美妆护肤产品
- `fmcg_beauty.md` - FMCG美容产品
- `fmcg_food.md` - FMCG食品饮料
- `fmcg_daily.md` - FMCG日用品

### 电子产品 (2个)
- `electronics_auto.md` - 电子汽车产品
- `electronics_mobile.md` - 手机数码产品

### 时尚家居 (3个)
- `fashion_home.md` - 时尚家居产品
- `fashion_apparel.md` - 服装鞋包
- `home_furniture.md` - 家具产品

### 其他行业 (9个)
- `food_beverage.md` - 食品饮料
- `pet_services.md` - 宠物服务
- `special_industries.md` - 特殊行业
- `maternity_baby.md` - 母婴产品
- `health_device.md` - 健康设备
- `pet_food.md` - 宠物食品
- `service_food.md` - 餐饮服务
- `realestate_residential.md` - 住宅地产
- `auto_vehicle.md` - 汽车产品

## 示例结构

每个示例文件包含：
1. **用户需求** - 原始用户输入
2. **Skill输出** - 完整的广告提示词结构
3. **合规声明** - 广告法合规检查结果
4. **视频规格** - 时长、比例、风格定义
5. **分镜脚本** - 详细的视频分镜
6. **Seedance提示词** - 可直接使用的生成提示词
7. **图片生成提示词** - 配套的图片生成提示词

## 使用方法

### 1. 学习模板
```markdown
# 查看特定行业的广告风格
cat examples/fmcg_beauty.md
```

### 2. 复制结构
```markdown
# 使用示例作为模板创建新广告
# 替换产品信息和风格描述
```

### 3. 验证合规
```markdown
# 检查示例中的合规标注
grep "合规声明" examples/*.md
```

## 最佳实践

### 风格选择
- **9秒视频**：适合简单产品展示，节奏明快
- **15秒视频**：适合功能演示，信息量适中
- **30秒视频**：适合故事叙述，情感共鸣

### 比例选择
- **9:16**：竖屏视频，适合移动端和短视频平台
- **16:9**：横屏视频，适合网页和电视广告
- **1:1**：方形视频，适合社交媒体

### 行业适配
- 每个行业都有独特的视觉风格和合规要求
- 参考对应行业的示例来确保风格一致性
- 注意特殊行业的强制标注要求

**涉及Reference**：
- `@ref_elec_mobile`（手机数码）
- `@ref_elec_appliance`（家电）
- `@ref_auto_vehicle`（汽车整车）

---

### 5. 服装和家居 (`fashion_home.md`)
- 运动瑜伽服广告（12秒）
- 钻石项链广告（9秒）
- 北欧沙发广告（15秒）
- 床上四件套广告（12秒）
- 智能灯具广告（9秒）

**涉及Reference**：
- `@ref_fashion_apparel`（服装鞋包）
- `@ref_fashion_jewelry`（珠宝配饰）
- `@ref_home_furniture`（家具）
- `@ref_home_textile`（家纺）
- `@ref_home_decor`（家装建材）

---

### 6. 宠物和服务行业 (`pet_services.md`)
- 猫粮广告（12秒）
- 智能猫砂盆广告（15秒）
- 火锅店广告（15秒）
- 海边度假酒店广告（12秒）
- 婴儿奶粉广告（15秒）

**涉及Reference**：
- `@ref_pet_food`（宠物食品）
- `@ref_pet_supplies`（宠物用品）
- `@ref_service_food`（餐饮服务）
- `@ref_service_travel`（旅游酒店）
- `@ref_maternity_baby`（母婴用品）

---

## Reference 索引速查

### 分类模板 Reference

| 行业 | Reference ID | 示例文件 |
|-----|--------------|---------|
| 食品饮料 | `@ref_fmcg_food` | food_beverage.md, fmcg_food.md |
| 美妆护肤 | `@ref_fmcg_beauty` | beauty_skincare.md, fmcg_beauty.md |
| 日用家清 | `@ref_fmcg_daily` | fmcg_daily.md |
| 手机数码 | `@ref_elec_mobile` | electronics_auto.md, electronics_mobile.md |
| 家电 | `@ref_elec_appliance` | electronics_auto.md |
| 电脑办公 | `@ref_elec_computer` | - |
| 服装鞋包 | `@ref_fashion_apparel` | fashion_home.md, fashion_apparel.md |
| 珠宝配饰 | `@ref_fashion_jewelry` | fashion_home.md |
| 家具 | `@ref_home_furniture` | fashion_home.md, home_furniture.md |
| 家纺 | `@ref_home_textile` | fashion_home.md |
| 家装建材 | `@ref_home_decor` | fashion_home.md |
| 汽车整车 | `@ref_auto_vehicle` | electronics_auto.md, auto_vehicle.md |
| 汽车用品 | `@ref_auto_accessory` | - |
| 母婴用品 | `@ref_maternity_baby` | pet_services.md, maternity_baby.md |
| 童装童鞋 | `@ref_maternity_kids` | - |
| 保健食品 | `@ref_health_supplement` | special_industries.md |
| 医疗器械 | `@ref_health_device` | health_device.md |
| 宠物食品 | `@ref_pet_food` | pet_services.md, pet_food.md |
| 宠物用品 | `@ref_pet_supplies` | pet_services.md |
| 餐饮服务 | `@ref_service_food` | pet_services.md, service_food.md |
| 教育培训 | `@ref_service_edu` | special_industries.md |
| 旅游酒店 | `@ref_service_travel` | pet_services.md |
| 金融服务 | `@ref_service_finance` | special_industries.md |
| 住宅房产 | `@ref_realestate_residential` | special_industries.md, realestate_residential.md |
| 商业地产 | `@ref_realestate_commercial` | - |

### 合规检查 Reference

| Reference | 用途 |
|-----------|-----|
| `@ref_compliance_check` | 违禁词检查、强制标注、合规替换 |

### 脚本结构 Reference

| Reference | 用途 |
|-----------|-----|
| `@ref_script_structure` | 脚本基础结构模板 |
| `@script_{分类}_{时长}_{版本}` | 具体广告脚本 |

---

## 使用建议

1. **查找相似案例**：根据产品所属行业，查看对应示例文件
2. **参考输出格式**：每个示例包含完整的Skill输出格式
3. **合规要点**：特殊行业示例包含强制标注要求
4. **提示词结构**：参考Seedance生成提示词的写法

---

## 扩展示例

**已完成示例** (v2.0.0):
- 医疗器械广告 (health_device.md)
- 电脑办公设备广告 (electronics_mobile.md 部分覆盖)
- 童装童鞋广告 (maternity_baby.md 部分覆盖)
- 汽车用品广告 (auto_vehicle.md)
- 商业地产广告 (待补充)
- 更多服务类广告 (service_food.md)

**进行中示例**:
- 商业地产广告
- 教育科技广告
- 跨境电商广告

**计划中示例**:
- 更多母婴细分行业
- 宠物用品细分
- 旅游服务细分
- 金融科技广告
