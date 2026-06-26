# 标签范围与风险等级参考

## labels 标签定义

| 标签 | 含义 |
|------|------|
| system_suggest_0 | No match.（无匹配场景） |
| system_suggest_1 | Someone appears.（有人出现） |
| system_suggest_2 | Multiple people appear.（多人出现） |
| system_suggest_3 | Child or infant appears.（儿童或婴儿出现） |
| system_suggest_4 | Elderly person appears.（老人出现） |
| system_suggest_5 | Animal appears.（动物出现） |
| system_suggest_6 | Suspicious behavior detected.（可疑行为） |
| system_suggest_7 | Person lying down.（有人躺卧） |
| system_suggest_8 | Person running.（有人在跑） |
| system_suggest_9 | Person climbing.（有人在攀爬） |
| system_suggest_10 | Fall detected.（检测到摔倒） |
| system_suggest_11 | Delivery person detected.（检测到快递员/外卖员） |
| system_suggest_12 | Family interaction.（家人互动） |
| system_suggest_13 | Household chore.（做家务） |
| system_suggest_14 | Package/parcel detected.（检测到快递包裹） |

## risk.level 风险等级定义

| 等级 | 含义 | 典型场景 |
|------|------|----------|
| none | 无风险 | 正常日常活动，家人互动，做家务 |
| low | 低风险 | 可疑但不确定的行为，非危险区域的攀爬 |
| medium | 中风险 | 儿童靠近窗户/阳台边缘，老人独处出现异常姿态 |
| high | 高风险 | 摔倒，儿童攀爬窗户/围栏，陌生人闯入 |

## 数据集类别要求

### 物体（每物体50条）
- 人：婴儿，儿童，老人，男成人，女成人，快递员、外卖员
- 动物：猫，狗
- 物体：快递盒，扫地机器人、吸尘器、床、桌子、椅子、凳子、沙发、门、窗帘、冰箱、洗衣机、其他家具

### 行为动作（每动作35条）
- 人的动作：躺卧，下蹲，爬行，攀爬，追逐、弯腰，徘徊，快速跑，吃饭、看电视、聊天、家人互动（拥抱、递东西、打闹、追逐）、做家务（扫地、拖地、擦桌子、洗菜、切菜、做饭、洗衣服、取出衣服、晾衣服、收衣服）
- 儿童婴儿动作：翻身、爬行、蹒跚学步、玩玩具、吃饭、吃手、摔倒，儿童/婴儿爬窗户，围栏
- 老人动作：浇花、看电视、看报纸、打太极、静坐、静卧、走动、普通活动
- 动物的动作：进食，饮水，猫抓挠家居，跑酷，跳跃，追尾巴，歪头杀，守在门口、攀爬围栏/窗户、撕咬、其他事件

### 环境（每环境30条）
- 室内：客厅/厨房/卫生间/阳台/门口/庭院/超市/书房/办公室/走廊
- 户外：停车场/花园/池塘/果园/农田/蔬菜大棚/鸡圈/羊圈/牛圈
