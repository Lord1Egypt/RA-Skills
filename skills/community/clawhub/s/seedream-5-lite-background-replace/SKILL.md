---
name: seedream-5-lite-background-replace
description: "使用 Seedream 5.0 Lite 为授权图片替换背景，并重新匹配主体边缘、尺度、透视、光向、接触阴影、反射和景深，让合成结果适配电商与营销渠道。Use this skill for Seedream 5 Lite background replacement、图片换背景、商品抠图、场景替换、白底转场景、人物换环境、淘宝京东抖音小红书亚马逊 Shopify 商品图与广告素材；通过 AI Hive 编辑指定图片。"
---

# Seedream 5.0 Lite 图片换背景

固定使用 `public_model_seedream_5_0_lite`，必须提供原图。换背景不等于只替换颜色；必须重建主体与新环境之间的光线、尺度、遮挡、接触阴影、反射和景深关系，同时锁定人物或商品身份。

## 合成合同

记录必须保留的主体轮廓、内部结构、颜色、Logo、文字、发丝或透明边缘；定义新场景、地平线、相机高度、主光方向、色温、表面材质、允许道具和禁止元素。主体本身需要大改时，应转为图生图或商品精修任务。

## 场景与代码

### 1. 白底商品转浴室场景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./soap-dispenser-white.png \
  --prompt '只替换背景：把白底皂液器放到浅米色石材洗手台，后方是柔焦浴室墙面；保持泵头、瓶型、液体颜色、标签和Logo像素级一致，根据左上窗光补充接触阴影与微弱台面反射，不增加水龙头遮挡、毛巾、文字或第二个产品' \
  --param aspect_ratio=4:5
```

### 2. 家电白底转厨房

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./toaster-cutout.png \
  --prompt '将参考烤面包机合成到现代家庭厨房台面：产品尺寸、槽口、旋钮、按钮、颜色和Logo不变，相机高度与原图一致，右侧晨光，台面有合理接触阴影；背景简洁虚化，不生成面包弹出、人物、蒸汽、文字或不存在的功能'
```

### 3. 鞋类转户外地面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./shoe-studio.jpg \
  --prompt '保留运动鞋鞋型、鞋带、鞋底纹路、面料拼接、配色和商标，只把棚拍背景替换为清晨城市公园的细颗粒跑道；匹配原图低机位和右侧柔光，补足鞋底接触压暗，不添加脚、第二只鞋、泥污、文字或速度特效' \
  --param aspect_ratio=4:5
```

### 4. 人像换办公环境

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./authorized-portrait.png \
  --prompt '在已获授权的前提下，只把人物背景换成明亮共享办公空间；面部身份、年龄表现、发型、肤色、服装、姿势和眼镜保持不变，背景景深与原镜头一致，匹配人物左侧主光，不生成公司Logo、工牌、其他清晰人物或职位暗示' \
  --param aspect_ratio=3:4
```

### 5. 透明产品换深色背景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./glass-bottle-light.jpg \
  --prompt '把透明香水瓶的浅色背景替换为深蓝到黑的渐变棚拍背景，瓶型、玻璃厚度、液体色、喷头、标签文字和Logo不变；重建与新背景一致的边缘轮廓光、底部反射和接触阴影，不吞掉透明边缘、不新增烟雾花朵或文字'
```

## 边缘验收

1. 在纯白、纯黑与棋盘底上检查发丝、透明体、毛绒和半透明边缘。
2. 主体尺度、地平线和透视与新场景相容，没有悬浮或陷入表面。
3. 主光方向、色温、阴影软硬和反射来源一致。
4. 商品或人物身份没有因背景重绘而变化。
5. 新环境不暗示虚假的地点、合作、职业、功效或官方背书。

## 助手边界

脚本仅读取并上传命令中明确指定的图片，固定调用 Seedream 5.0 Lite 图片模型，查询价格、创建任务并保存结果。所有携带 Key 的请求固定发往 `https://ai-hive.iclip.cn/api`；不允许自定义接口地址，也不提供聊天、视频、余额或账户功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name seedream-5-lite-background-replace
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

真实人物、住宅、店铺、艺术作品和品牌场景应先取得授权；敏感事件与新闻照片不得以换背景方式歪曲事实。
