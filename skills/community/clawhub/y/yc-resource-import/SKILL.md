---
name: yc-resource-import
description: |
  全球旅游资源全自动解析入库技能。
  支持本地文件 / Google Drive / 百度网盘自动拉取合同；
  支持 PDF / Word / 图片PDF / 扫描件 / 拍照图片全格式解析；
  自动识别8大资源类型 → 按锁死标准字段抽取 → 公开信息自动补齐 → 敏感信息脱敏 → 合规校验 → 输出标准CSV并追加到生产库；
  不编造、不脑补、不乱填、字段与表头100%对齐生产环境。
  触发词：资源入库、解析入库、旅游资源、CSV入库、合同解析、资源协议导入。
compatibility: Python 3.8+, PyMuPDF, python-docx, pdfplumber, csv, redis（可选）
---

# 全球旅游资源解析入库技能 V2.0（最终锁字段版）
## 【全局强约束：字段永久锁死，禁止任何改动】
你必须严格绑定以下8类资源固定字段体系，**字段名、数量、顺序永久固定**，不允许：新增字段、删除字段、改名字段、调整顺序、合并字段、编造内容。
识别资源类型后，只加载对应字段列表，按顺序填空，缺则留空。

-------------------------------------------------------------------------------
# 【1】酒店 固定字段（42个，顺序锁死）
contract_id,hotelnameen,hotelnamecn,star_rating,region_en,region_cn,address,phone,email,website,gps_longitude,gps_latitude,Zone ID,Hotel Number,Company Name,room_type,area_sqm,max_occupancy,bed_type,room_amenities,facilities,unique_features,priceidrlow_season,priceidrhigh_season,priceidrpeak_season,pricecnylow_season,pricecnyhigh_season,pricecnypeak_season,breakfast_policy,children_policy,extrabedpolicy,cancellation_policy,checkintime,checkouttime,deposit_policy,payment_terms,validity_start,validity_end,data_source,data_quality,last_updated,notes,tags_audience,tags_style,tags_feature

# 【2】车辆 固定字段（36个，顺序锁死）
vehiclemodelen,vehiclemodelcn,vehicle_type,seats,capacity,luggage_capacity,air_condition,driver_language,services_included,driver_experience,vehicle_condition,Company Name,priceidrhalf_day,priceidrdaily13,priceidrdaily4,Priceidrdaily5,Priceidrdaily6,Priceidrdaily7,Priceidrdaily8,pricecnyhalf_day,pricecnydaily13,pricecnydaily47,Pricecnydaily5,Pricecnydaily6,Pricecnydaily7,Pricecnydaily8,service_hours,overtimefeeidr,overtimefeecny,outofareafeeidr,fuel_policy,toll_policy,parking_policy,validity_start,validity_end,data_source,data_quality,last_updated,notes,tags_audience,tags_style,tags_feature

# 【3】景点 固定字段（40个，顺序锁死）
Attraction ID,attractionnameen,attractionnamecn,attraction_type,category,region_en,region_cn,address,website,gps_longitude,gps_latitude,Zone ID,opening_hours,closing_days,duration_required,bestvisittime,priceidradult,priceidrchild,priceidrinfant,pricecnyadult,pricecnychild,pricecnyinfant,special_requirements,booking_info,transport_info,description,highlights,photos_allowed,guided_tour,wheelchair_access,parking_available,restaurantonsite,restroom_available,souvenir_shop,validity_start,validity_end,data_source,data_quality,last_updated,notes,tags_audience,tags_style,tags_feature

# 【4】活动 固定字段（42个，顺序锁死）
activity_id,activitynameen,activitynamecn,activity_type,category,region_en,region_cn,gps_longitude,gps_latitude,Zone ID,Company Name,location,address,phone,email,website,duration_hours,difficulty_level,age_restriction,health_requirements,physical_demand,besttimeof_day,Opening Hours,Recommended Time,Best Time to Visit,seasonal_availability,groupsizemin,groupsizemax,priceidradult,priceidrchild,priceidrinfant,pricecnyadult,pricecnychild,pricecnyinfant,inclusions,instructor_language,equipment_provided,insurance_included,weather_dependency,booking_required,cancellation_policy,description,highlights,safety_notes,whattobring,photos_allowed,videoserviceavailable,validity_start,validity_end,data_source,data_quality,last_updated,notes,tags_audience,tags_style,tags_feature

# 【5】SPA 固定字段（33个，顺序锁死）
spa_id,spanameen,spanamecn,spa_type,category,region_en,region_cn,address,phone,email,website,gps_longitude,gps_latitude,Zone ID,SPA Shop Name,opening_hours,closing_days,duration_hours,Treatments info,priceidr60min,priceidr90min,priceidr120min,pricecny60min,pricecny90min,pricecny120min,inclusions,room_type,products_used,booking_required,cancellation_policy,shower_facilities,locker_rooms,validity_start,validity_end,data_source,data_quality,last_updated,notes,tags_audience,tags_style,tags_feature

# 【6】俱乐部 固定字段（35个，顺序锁死）
club_id,clubnameen,clubnamecn,club_type,category,region_en,region_cn,address,Zone ID,Company Name,phone,email,website,gps_longitude,gps_latitude,opening_hours,closing_days,age_restriction,dress_code,entry_requirements,coverchargeidr_adult,coverchargeidr_female,coverchargeidr_couple,coverchargecny_adult,coverchargecny_female,coverchargecny_couple,tablebookingrequired,minimumspendingidr,minimumspendingcny,features,music_style,dj_schedule,special_events,parking_available,vip_rooms,bottle_service,food_available,description,highlights,safety_notes,validity_start,validity_end,data_source,data_quality,last_updated,notes,tags_audience,tags_style,tags_feature

# 【7】餐厅 固定字段（38个，顺序锁死）
restaurant_id,restaurantnameen,restaurantnamecn,restaurant_type,category,region_en,region_cn,address,Zone ID,Company Name,phone,email,website,gps_longitude,gps_latitude,opening_hours,closing_days,cuisine_type,seating_capacity,outdoor_seating,beach_front,sunset_view,signature_dishes,special_offers,private_dining,Package1,Menu 1,averagepriceidrperperson,averagepricecnyperperson,Package2,Menu 2,reservation_required,advancebookingdays,cancellation_policy,free_parking,wheelchair_accessible,children_menu,halal_food,payment_methods,service_charge,tax,description,highlights,special_notes,validity_start,validity_end,data_source,data_quality,last_updated,notes,tags_audience,tags_style,tags_feature

# 【8】下午茶 固定字段（32个，顺序锁死）
afternoonteaid,afternoonteaname_en,afternoonteaname_cn,afternoonteatype,category,region_en,region_cn,address,Zone ID,Company Name,phone,email,website,gps_longitude,gps_latitude,opening_hours,closing_days,teatimehours,capacity,menu_type,tea_selection,cake_selection,special_combinations,priceidrsetfortwo,priceidrper_person,pricecnysetfortwo,pricecnyper_person,reservations_required,advancebookingdays,cancellation_policy,beach_view,sunset_view,pool_access,signature_treats,special_offers,private_area,free_parking,wheelchair_accessible,children_friendly,payment_methods,service_charge,tax,description,highlights,special_notes,validity_start,validity_end,data_source,data_quality,last_updated,notes,tags_audience,tags_style,tags_feature
-------------------------------------------------------------------------------

## 一、触发识别与路径提取
从用户输入动态提取以下变量，禁止硬编码：
1. 云盘URL：Google Drive / 百度网盘 / 其他网盘
2. 本地文件路径
3. 模型文件路径（生产CSV所在目录）
4. 目标输出路径（解析结果存放目录）
未指定路径时，必须提示用户补充。

## 一（附）、网盘自动识别与技能匹配规则（必须遵守）
根据用户提供的网盘URL自动匹配对应技能：
| 网盘类型 | URL特征 | 所需技能 | 安装命令 |
|---------|---------|---------|---------|
| Google Drive | drive.google.com | google-drive | `openclaw skills install google-drive` |
| 百度网盘 | pan.baidu.com | baidu-netdisk | `openclaw skills install baidu-netdisk` |
| 阿里云盘 | aliyundrive.com / alipan.com | aliyundrive | `openclaw skills install aliyundrive` |
| OneDrive | onedrive.live.com | onedrive | `openclaw skills install onedrive` |
| Dropbox | dropbox.com | dropbox | `openclaw skills install dropbox` |

**执行流程：**
1. 识别URL中的网盘类型
2. 检查对应技能是否已安装
3. 未安装 → 提示用户执行安装命令
4. 已安装 → 使用该技能拉取文件
5. 技能安装后仍无法访问 → 提示用户创建分享链接或使用本地文件

## 二、依赖检查
执行前必须检查：
- google-drive、Bbaidu-netdisk-storage 技能
- pdfplumber、python-docx、PyMuPDF
缺失时返回安装指引，终止执行。

## 三、文件拉取与预处理
1. 云盘文件：自动下载 PDF/Word/图片类合同，过滤无关文件
2. 本地文件：直接读取
3. 图片PDF/扫描件/拍照图：自动OCR转文本，notes标注「来源=OCR识别」
4. 云端文件先下载到本地临时目录，再解析
5. 支持批量10+文件，任务队列串行处理，不崩溃

## 四、资源类型自动识别（无需人工指定）
按以下维度判定，输出固定8类：
酒店、车辆、景点、活动、SPA、俱乐部、餐厅、下午茶
判定依据：
- 文件名/标题关键词
- 正文特征词（房型、门票、租车、按摩、冲浪等）
- 价格结构（按晚/按天/按人次/按分钟）
- 条款模式（入住退房、超时费、时长、套餐）

## 五、三层标签体系（强制使用官方标准）
### 人群标签（所有资源通用）
家庭、亲子、情侣、商务、蜜月、年轻人、老年人、单身
### 风格标签（所有资源通用）
豪华、经济型、浪漫、休闲、刺激、度假村、商务、自然、文化
### 特色标签（严格按8类官方标签库生成，不编造）
必须从《巴厘岛旅游资源_8类特色标签快速查阅表_V4.0》中选取，只选匹配项，用英文逗号分隔。

## 六、Zone ID 自动匹配（官方规则）
按地区自动映射：
- Zone-S1：努沙杜瓦、金巴兰、乌鲁瓦图
- Zone-S2：库塔、水明漾、长谷、萨努尔
- Zone-C1：乌布、德格拉朗、嘉利维
- Zone-W1：贝都古、汉达拉、贾蒂卢维
- Zone-E1：帕当拜、阿曼、天堂之门
- Zone-N1：京打马尼、罗威纳、塞库普
- Zone-OFF：佩妮达、蓝梦岛、吉利群岛
无法匹配时填：未知

## 七、字段抽取与补齐规则（核心）
1. 按锁死字段列表**按顺序抽取**，不增、不减、不改、不乱序
2. 优先级：合同原文 > 公开网络查询 > 留空
3. 【自动补齐白名单】仅公开信息可联网查询补齐：
   address、region_en、region_cn、gps_longitude、gps_latitude、website、phone、email、opening_hours
4. 价格、政策、合同条款、有效期、标签：**只使用合同内容，禁止补齐**
5. 补齐记录必须在notes标注：[自动补齐]xxx / [缺失]xxx
6. 无内容必须留空，禁止填写：无、NULL、未提供、合同未提供

## 八、多房型解析规则（酒店专用）
1. 每个房型单独一行
2. 基础信息全部复制
3. 房型、面积、价格、床型单独填写
4. 政策、标签全行一致

## 九、敏感信息自动脱敏（强制执行）
- 手机号：138****1234
- 身份证号：1101********1234
- 银行卡/对公账户：6222****1234
- 其他隐私信息一律打码，不显示原文

## 十、合规与质量校验（官方评分体系）
1. 合同有效期校验：
   - 已过期 → notes：合同已过期
   - 30天内到期 → notes：合同即将到期
2. 必备字段缺失 → notes：核心信息缺失，需人工复核
3. 价格异常/冲突 → notes：条款异常，请人工核对
4. 数据质量自动评分（官方标准）：
   - 合约价：90分
   - 官网价：70分
   - 未知来源：0分
   完整+时效+审核通过：+10~15分

## 十一、CSV输出路径与格式
用户可指定任意输出路径，自动按资源类型分文件夹：
/output/酒店、/output/车辆、/output/景点 ...
编码：
- 酒店：utf-8-sig
- 其他7类：gbk

## 十二、数据库导入规则
1. 8类资源对应8张表
2. 字段与CSV完全一致
3. 追加写入，不覆盖
4. 重复ID自动跳过
5. 支持 MySQL / PostgreSQL

## 十三、依赖缺失处理
- 缺云盘技能：提示执行 openclaw skills install xxx
- 缺Python库：提示 pip install pdfplumber python-docx PyMuPDF
- 路径不存在：自动创建

## 十四、执行完成标准回复（必须原样返回）
✅ 资源解析入库完成
━━━━━━━━━━━━━━━━━━━━
解析文件：xxx.pdf、xxx.docx
成功解析：N 条数据
资源类型：酒店×N | 车辆×N | 景点×N | 活动×N | SPA×N | 俱乐部×N | 餐厅×N | 下午茶×N
输出CSV路径：/xxx/xxx/xxx/
数据库入库状态：已完成 / 未开启
清理状态：原始文件已归档，临时文件已删除

## 十五、文件处理规则
### 15.1 输出目录结构规范（强制执行）
```
目标输出路径/
├── 📄 hotel_contracts_final.csv      # CSV文件放在根目录
├── 📄 restaurant_contracts_final.csv
├── 📄 spa_contracts_final.csv
├── 📄 [其他资源类型]_contracts_final.csv
└── 📑 contracts/                      # PDF/Word原始合同放入子文件夹
    ├── xxx_Hotel_Contract.pdf
    ├── xxx_Restaurant_Contract.pdf
    └── ...
```
**规则：**
- CSV输出文件必须放在目标路径根目录
- 原始PDF/Word合同文件必须放入 `contracts/` 子文件夹
- `data_source` 字段值格式：`contracts/文件名.pdf`
- 禁止将PDF与CSV放在同一级目录

### 15.2 归档规则
1. 云盘下载原始合同 → 放入 `contracts/` 子文件夹
2. 中间临时文件 → 自动删除
3. 最终CSV → 永久保留在用户指定目录根目录
4. 重复文件自动跳过，不覆盖

## 十六、绝对禁止行为
- 不编造任何合同信息
- 不脑补价格、政策、条款、标签
- 不新增/删除/改名字段
- 不打乱字段顺序
- 不输出解释、表格、代码块，只输出纯CSV
- 不修改合同真实内容