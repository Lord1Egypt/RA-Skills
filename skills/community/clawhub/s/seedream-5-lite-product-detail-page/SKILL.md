---
name: seedream-5-lite-product-detail-page
description: "使用 Seedream 5.0 Lite 按购买者问题阶梯生成详情页模块，依次回答是什么、适不适合、如何工作、如何使用和会收到什么。Use this skill for Seedream 5 Lite product detail page、商品详情页、PDP、Amazon A+、淘宝天猫京东抖店 Shopify 商品页、卖点图、结构图、步骤图、规格图和电商长图；通过 AI Hive 逐模块生成。"
---

# Seedream 5.0 Lite 商品详情页

固定使用 `public_model_seedream_5_0_lite`。将详情页拆成购买问题，而不是固定模板：这是什么、为什么与我有关、如何工作、如何使用、尺寸是否合适、盒内有什么、有哪些限制。每个模块只回答一个问题。

## 问题阶梯

为每个问题记录批准答案、证据、视觉任务、商品锁定项、文字留白、比例与下一模块。没有证据的问题不得通过生成图片“补答案”；数字、认证、评价和对比需来自批准资料并后期排版。

## 场景与代码

### 1. 这是什么：首屏模块

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-monitor-stand.png \
  --prompt '生成显示器增高架详情页首屏底图：保持参考产品长度、支脚、抽屉、材质和Logo，置于整洁办公桌，右侧留产品定位与一句利益点区域，不生成文字、尺寸、承重、人物、显示器品牌或不存在的接口' \
  --param aspect_ratio=16:9
```

### 2. 适不适合：使用人群场景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-baby-carrier.png \
  --prompt '制作婴儿背带适用场景底图：保持产品肩带、扣具、腰带、颜色和Logo，由已授权成年人按批准方式佩戴，使用无可识别面部的模特，右侧留适用范围说明区域；不生成年龄体重数字、医疗主张、不安全姿势或额外配件' \
  --param aspect_ratio=16:9
```

### 3. 如何工作：结构解释

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-desk-hub.png \
  --prompt '生成桌面扩展坞结构解释底图：主体外观、端口数量、顺序、Logo和颜色完全依据参考图，周围放大显示三个已存在端口的局部，留标签空位；不生成文字、内部芯片、传输速度、认证、发光效果或不存在的接口' \
  --param aspect_ratio=16:9
```

### 4. 如何使用：四步流程

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-coffee-grinder.png \
  --prompt '制作手摇磨豆机四步图底图：加豆、盖好、转动手柄、取出咖啡粉，产品结构、刻度、颜色和手柄形状不变，四格相机角度统一，每格留步骤文字区；不生成文字、时间数字、电机、危险手势或额外工具' \
  --param aspect_ratio=16:9
```

### 5. 会收到什么：装箱模块

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-projector-box.png \
  --prompt '生成投影仪装箱清单底图：只展示参考资料确认包含的投影仪、遥控器、电源线和说明书，各出现一次，俯拍整齐排列，右侧留清单文字区；保持产品和配件外观，不生成文字、HDMI线、支架、幕布、赠品或平台Logo' \
  --param aspect_ratio=16:9
```

## 页面验收

- 问题顺序符合实际购买决策，没有两个模块回答同一问题。
- 同一 SKU 在所有模块中的结构、颜色、Logo和配件一致。
- 每个答案都有批准来源，图片不替代检测与法规证据。
- 移动端裁切、文字区和信息密度逐模块检查。
- 最终文字在设计工具中排版并逐项校对。

## 助手边界

脚本固定使用 Seedream 5.0 Lite 图片模型，可提交纯文字任务或上传用户指定图片，查询价格并保存输出。带 Key 请求仅发送到 `https://ai-hive.iclip.cn/api`，不支持自定义地址，也没有聊天、视频、账户或余额接口。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name seedream-5-lite-product-detail-page
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

人物、规格、装箱、评价、效果与认证必须使用授权且可追溯资料。
