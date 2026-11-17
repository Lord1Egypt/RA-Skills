---
name: seedance-2-5-ecommerce-video
description: "使用 Seedance 2.5 为电商 Listing、PDP 和详情页生成可追溯的模块短片，让每个槽位只回答一个购买问题：随箱清单、尺寸、兼容性、安装、使用步骤、材质、SKU变体或功能证据。Use this skill for Seedance 2.5 ecommerce video、电商视频、商品主图视频、详情页视频、Amazon Product Video、Listing、PDP、淘宝天猫京东、抖音商城、小红书、TikTok Shop、Shopify、Temu、Shopee；也适合比较可灵 Kling、即梦 Dreamina、海螺 Hailuo、Vidu、Runway、Pika、Sora、Veo、美图 MOKI 与剪映 CapCut。通过 AI Hive 调用。"
---

# Seedance 2.5 电商视频

把详情页视频拆成可独立验收的 Listing 槽位：一个短片只回答一个购买问题，并绑定 SKU 主档、事实来源、平台规则和后期文字地图。无动作参考时固定调用 `public_model_seedance_2_5_i2v`；提供批准动作样片时调用 `public_model_seedance_2_5_r2v`。真实商品图优先于动作参考。

这个 Skill 不负责情绪带货、整支品牌宣传片或多平台裁切；对应需求分别由带货节拍、产品宣传片镜头包和社媒版本矩阵处理。

## 模块选择

| 模块 | 回答的问题 | 强制信息 |
|---|---|---|
| `in-box` | 包装内到底有什么 | `included-count` |
| `dimension` | 相对尺寸和使用空间如何 | 批准尺寸来源 |
| `compatibility` | 能与什么真实设备配合 | `compatibility-basis` |
| `assembly / use-step / care` | 某一个步骤如何完成 | 步骤编号与总数 |
| `material` | 材质与表面细节是什么 | 材质 QC 来源 |
| `variant` | SKU 之间真正有什么差别 | 每个 SKU 的批准图 |
| `feature-proof` | 一个批准功能如何被看见 | 测试或说明书来源 |

可灵、即梦、海螺、Vidu、Runway、Pika、Sora、Veo、美图 MOKI、剪映以及电商平台名称只用于搜索、比较与迁移，不代表官方合作。平台规则可能变化，发布前应复核当前政策。

## 场景与代码

每条命令都可追加 `--preview`，先查看模型、商品素材职责和完整事实任务，不上传、不计费。

### 1. Amazon 随箱清单

```bash
python3 "$SKILL_PATH/scripts/listing_clips.py" clip \
  --listing-id amz-deskstand-us --slot-id in-box-01 --platform amazon --module in-box \
  --delivery "Amazon Product Video 16:9，7秒" --shopper "担心配件不全的桌面办公用户" \
  --shopper-question "包装里实际包含哪些部件" \
  --visual-answer "未开封包装切到全部批准部件平铺，每件只出现一次" \
  --sku-record "Stand S2黑色SKU，美区量产包装V4" \
  --product-source /path/to/box-qc.jpg /path/to/all-parts-qc.jpg \
  --product-role "包装、标签和SKU事实" "支架、底座、螺钉包与说明卡数量事实" \
  --fact "随箱包含1个支架、1个底座、1包批准螺钉和1张说明卡" \
  --fact-source "Stand S2美区BOM-2026-08与包装QC" --included-count "四类内容，各出现一次" \
  --start-state "封闭包装居中" --action "包装移出后四类内容按QC顺序平铺出现" \
  --end-state "所有内容完整可见并稳定停留" --camera "固定俯拍，不变焦" \
  --continuity-lock "黑色S2 SKU" --continuity-lock "部件数量不变" \
  --continuity-lock "螺钉包保持密封" --continuity-lock "包装标签不变" --continuity-lock "比例和颜色不变" \
  --overlay-map "右侧留给后期英文清单，画面内不生成文字" \
  --policy-guard "不把包装、道具或重复影像误表示为赠品" \
  --reject "不增加工具、手机、备用零件、尺寸、徽章、价格或五星评价" \
  --param aspect_ratio=16:9 --param duration=7
```

### 2. 天猫尺寸与空间关系

```bash
python3 "$SKILL_PATH/scripts/listing_clips.py" clip \
  --listing-id tmall-storage-r3 --slot-id dimension-02 --platform tmall --module dimension \
  --delivery "天猫详情页16:9，6秒" --shopper "担心收纳架放不进橱柜的家庭用户" \
  --shopper-question "批准样品与标准测试柜的相对空间如何" \
  --visual-answer "收纳架一次推入品牌批准测试柜，展示门板和层架余量" \
  --sku-record "Storage R3三层白色SKU，量产尺寸记录DR-31" \
  --product-source /path/to/rack-qc.jpg /path/to/test-cabinet-qc.jpg \
  --product-role "三层结构、连接件和白色事实" "批准测试柜、层板和相对尺度事实" \
  --fact "展示该量产样品在批准测试柜中的真实相对关系，具体尺寸后期标注" \
  --fact-source "R3尺寸报告DR-31与测试柜校准记录CB-08" \
  --start-state "收纳架和测试柜完整并列" --action "将收纳架一次平稳推入柜内并关到半门" \
  --end-state "柜门半开，三层和四角余量可见" --camera "正面固定中景后轻移到45度" \
  --continuity-lock "始终为三层白色R3" --continuity-lock "层高和连接件不变" \
  --continuity-lock "测试柜比例不变" --continuity-lock "不增加收纳物" --continuity-lock "透视与地面水平" \
  --overlay-map "左下留给后期毫米尺寸线，画面不自动生数字" \
  --policy-guard "不据此承诺适配所有橱柜，尺寸须由买家复核" \
  --reject "不生成尺寸、容量结论、箭头、竞品、额外层架或夸张伸缩"
```

### 3. 京东接口兼容性

```bash
python3 "$SKILL_PATH/scripts/listing_clips.py" clip \
  --listing-id jd-hub-h8 --slot-id compatibility-03 --platform jd --module compatibility \
  --delivery "京东商品视频16:9，8秒" --shopper "需要确认接口连接关系的笔记本用户" \
  --shopper-question "H8如何与批准测试笔记本和显示器连接" \
  --visual-answer "按批准连接图完成三次插接，端口和线缆清楚可见" \
  --sku-record "Hub H8深灰SKU，CN版端口布局V7" \
  --product-source /path/to/hub-ports.jpg /path/to/approved-setup.jpg \
  --product-role "H8端口数量、顺序和Logo事实" "批准笔记本、显示器与线缆连接事实" \
  --fact "只展示H8与指定测试设备按V7连接图的物理连接" \
  --fact-source "H8 CN说明书V7第4页" --compatibility-basis "品牌实验室测试设备清单CL-19" \
  --start-state "H8、三根批准线缆和测试设备均未连接" \
  --action "依次连接上行线、显示器线和电源线，每次只插一个端口" \
  --end-state "三根线已连接，全部端口仍可辨" --camera "固定桌面45度近景，插接时不切镜" \
  --continuity-lock "H8端口顺序不变" --continuity-lock "线缆数量和接口头不变" \
  --continuity-lock "设备型号外观不变" --continuity-lock "连接顺序不变" --continuity-lock "桌面和手连续" \
  --overlay-map "顶部留给后期设备名称和兼容性限定" \
  --policy-guard "不从物理连接推导性能、协议、分辨率或所有设备兼容承诺" \
  --reject "不生成端口、屏幕内容、传输速度、认证、无线连接或额外设备"
```

### 4. TikTok Shop 安装步骤

```bash
python3 "$SKILL_PATH/scripts/listing_clips.py" clip \
  --listing-id tts-filter-f2 --slot-id assembly-02 --platform tiktok-shop --module assembly \
  --delivery "TikTok Shop 9:16，6秒" --shopper "购买后需要安装滤芯的用户" \
  --shopper-question "第二步如何把滤芯正确锁入壶盖" \
  --visual-answer "只展示对齐标记、插入和顺时针锁定的第二步" \
  --sku-record "Filter F2白色壶与蓝色滤芯，安装指南V5" \
  --product-source /path/to/filter-parts.jpg /path/to/lock-mark-qc.jpg \
  --product-role "壶盖、滤芯、颜色和数量事实" "对齐标记与锁定终点事实" \
  --motion-reference /path/to/approved-step2-motion.mp4 \
  --fact "滤芯按标记对齐后顺时针旋转到批准锁定位置" --fact-source "F2安装指南V5第2步" \
  --step-number 2 --step-total 4 --start-state "滤芯位于壶盖上方且标记未对齐" \
  --action "按参考动作完成对齐、插入和一次顺时针旋转" \
  --end-state "滤芯停在批准锁定位置，标记可见" --camera "顶部近景固定，手不遮挡标记" \
  --continuity-lock "白壶蓝滤芯SKU" --continuity-lock "滤芯结构不变" \
  --continuity-lock "标记形状和位置不变" --continuity-lock "只旋转一次" --continuity-lock "手和桌面连续" \
  --overlay-map "左侧留给后期Step 2与箭头，不自动生成" \
  --policy-guard "这是单一步骤演示，发布时必须与完整四步说明共同呈现" \
  --reject "不跳过对齐、不逆时针、不增加零件、水、文字、特效或完成提示" \
  --param aspect_ratio=9:16 --param duration=6
```

### 5. Shopify 材质细节

```bash
python3 "$SKILL_PATH/scripts/listing_clips.py" clip \
  --listing-id shopify-wallet-w1 --slot-id material-05 --platform shopify --module material \
  --delivery "Shopify PDP 4:5，5秒" --shopper "在意真实皮纹与缝线的消费者" \
  --shopper-question "批准样品的表面纹理和边油细节是什么样" \
  --visual-answer "微距展示皮纹、缝线、边油与金属扣，不演示未批准耐久性能" \
  --sku-record "Wallet W1栗棕SKU，材料样本M-22" \
  --product-source /path/to/wallet-front.jpg /path/to/material-macro.jpg \
  --product-role "钱包结构、Logo和栗棕色事实" "批准皮纹、缝线、边油与金属表面事实" \
  --fact "展示量产样品可见材料细节，不推导材质等级或寿命" --fact-source "W1材料QC M-22" \
  --start-state "钱包45度完整近景" --action "焦点从皮纹缓慢移动到缝线和边油" \
  --end-state "金属扣与边油同框稳定停留" --camera "100mm微距横移，只做一次焦点转移" \
  --continuity-lock "栗棕色不变" --continuity-lock "皮纹不磨平" --continuity-lock "缝线数量与走向不变" \
  --continuity-lock "Logo和金属扣不变" --continuity-lock "原使用痕迹不删除" \
  --overlay-map "顶部20%留给后期材料名称" --policy-guard "材料名称和成分以批准规格表为准" \
  --reject "不生成皮革等级、耐磨测试、火焰、水滴、放大结构图或奢侈品类比"
```

### 6. 淘宝 SKU 变体区分

```bash
python3 "$SKILL_PATH/scripts/listing_clips.py" clip \
  --listing-id taobao-bottle-b6 --slot-id variant-06 --platform taobao --module variant \
  --delivery "淘宝详情页1:1，6秒" --shopper "需要区分三个批准颜色SKU的用户" \
  --shopper-question "黑、白、薄荷绿三个SKU在外观上如何区分" \
  --visual-answer "三个SKU按同一角度依次出现，每次只显示一个，最后并列" \
  --sku-record "Bottle B6黑、白、薄荷绿三个量产SKU，结构完全相同" \
  --product-source /path/to/black.jpg /path/to/white.jpg /path/to/mint.jpg \
  --product-role "黑色SKU事实" "白色SKU事实" "薄荷绿SKU事实" \
  --fact "三个SKU只在批准颜色上不同" --fact-source "B6 SKU主档V9与三色QC" \
  --start-state "黑色SKU正面居中" --action "黑、白、薄荷绿按顺序淡切，最后三者等距并列" \
  --end-state "三色SKU同角度同尺寸并列" --camera "相机、焦段和光线固定" \
  --continuity-lock "三者结构完全一致" --continuity-lock "Logo位置一致" --continuity-lock "容量和瓶盖一致" \
  --continuity-lock "颜色只来自各自QC" --continuity-lock "每个SKU只出现一次" \
  --overlay-map "下方留给后期颜色名和SKU编号" --policy-guard "不得暗示颜色对应不同功能或容量" \
  --reject "不混色、不新增色号、不改变结构、瓶盖、Logo、容量、背景或光线"
```

## 验收

逐帧核对 SKU、数量、尺寸关系、接口、材质、颜色、步骤和兼容性；确认每段只回答一个购买问题。检查动作参考是否只贡献动作，而没有带入错误商品。关闭后期文字层复看，画面本身不能出现乱码、虚构数字或平台 UI。最后按目标平台验证比例、时长、自动播放、循环、静音观看与政策限制，并保存 `listing-id / slot-id / fact-source / taskId`。

## 首次使用

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/listing_clips.py" auth --api-key sk-api-你的密钥
python3 "$SKILL_PATH/scripts/listing_clips.py" status --task-id <taskId>
```

API Key 也可放入 `AI_HIVE_API_KEY` 或 `~/.ai-hive/config.json`。默认路由 `COST_FIRST`，支持其他路由、多个 `--param key=value`、`--no-download` 和自定义输出目录。超时后查询原任务，避免重复提交。
