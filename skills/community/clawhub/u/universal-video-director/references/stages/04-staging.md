# 子技能 04 · 场面调度与站位 staging
**来源**：shuohao novel-staging（开场站位、朝向、锚定物、群演，8 道门禁，产出可直接复制进分镜的开场站位句），ai-short-drama-from-zero 的 04A 场景空间模型和 180° 关系轴线，Toonflow 的 3D 白模预演。

## 目标
分镜之前，先定好每场戏谁在哪、朝哪、坐着还是站着，以及两人之间的关系轴线。

## 方法
1. 根据剧本和场景空镜图，为每场的每个角色确定：
   - anchor：站或坐在哪个物体旁边
   - side
   - posture
   - facing
   - xy（可选，俯视坐标）
2. **axis**：对话双方连一条关系轴线。后面分镜的同场镜头默认不越轴。
3. 没有场景图时，标 `provisional:true`，表示站位是暂定的。
4. **blocking_sentence**：每场写一句开场站位描述，分镜阶段要**原样**复制进这场戏的第一个 segment。
5. 不能两个人坐在同一个锚点的同一侧；场景里出现的角色都必须安排位置。
6. **道具也要定位**（会说话的物件、关键证物）：写 `kind:"prop"`，posture 从下面三个里选：
   - `placed`：放在某处
   - `held`：被人拿着
   - `concealed`：藏着，比如藏在袖子里
   藏在人身上的，side 写 `on_person`。道具误用人物姿态会报 PROP_POSTURE 警告，角色误用道具姿态会报 CHAR_POSTURE 错误。
7. 轴线一般连两个人。只有人和物件对峙的独角戏，才把物件设为轴线端点（AXIS_PROP 警告提示确认）。

## 常见错误码
CHAR_NOT_PLACED、AXIS_REF、SEAT_CONFLICT、BLOCKING_NOT_COPIED（由分镜阶段触发）
