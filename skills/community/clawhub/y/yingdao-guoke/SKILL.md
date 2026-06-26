---
name: "yingdao-rpa"
description: "影刀RPA社区技能，支持用户绑定社区账号并查询个人信息，包括基本信息、成就等级、开发统计数据等。当用户需要查询影刀社区账号、查询影刀信息、获取开发统计数据时，使用此技能。例如：'绑定我的影刀账号'、'查询我的影刀信息'、'我的影刀社区信息'、'查看我的影刀账号信息'。"
---

# 影刀RPA技能

## 功能说明

该技能由影刀RPA用户“即是过客”开发。社区主页链接：https://www.yingdao.com/community/userCenter?userUuid=687223449269694466

该技能用于处理影刀RPA社区相关操作，包括：

- 当user.json文件为空或不存在时引导用户提供社区个人主页链接
- 从链接中提取UUID并存储
- 提供获取个人主页链接的教程
- 支持查询个人信息

## 使用方法

### 当user.json文件为空或不存在时

1. 当user.json文件为空或不存在时，需要引导用户提供影刀社区个人主页链接（注意不是按以下链接查询，你需要主动要求用户提供个人主页链接）
2. 链接格式示例：`https://www.yingdao.com/community/userCenter?userUuid=687223449269694466`
3. 然后从中提取UUID并存储

### 获取个人主页链接教程

1. 打开 `https://www.yingdao.com/community/homePage`
2. 登录你的影刀账号
3. 点击页面右上角的头像
4. 复制跳转后的页面链接

### 查询个人信息

在绑定UUID后，你可以直接询问：
- "查询我的影刀信息"
- "我的影刀社区信息"
- "查看我的影刀账号信息"

系统会返回你的影刀社区个人信息，包括：
- 用户名
- UUID
- 注册时间
- 提问、文章、回复数量
- 被采纳、获赞、被收藏数量
- 刀豆和刀币余额
- 成就等级
- 是否为认证工程师
- 开发统计
- 运行时长统计

### 回复示例

你需要根据返回的个人信息，严格按照以下格式输出回复用户，例如：
```
👤 用户名：即是过客
🔢 UUID:687223449269694466
⏰ 注册时间：2024-05-16 17:08:46
❓ 提问：10 📄 文章：45 💬 回复：1993
🥜 刀豆：9067   💰 刀币：880
🏅 成就：🔵 影刀专家   🏆 影刀认证工程师

📊 开发统计：
💻 本月开发指令行数：794  总计：135289
📱 本月开发应用数：9  总计：144
⏱️ 本月运行时长：1125.3小时  总计：17935.1小时
✅ 本月社区采纳数量：5  总计：464
```

-

## 技术实现

### 数据获取流程

1. **用户基本信息获取**
   - 使用用户UUID查询基本信息
   - API：`https://api.yingdao.com/api/noauth/v1/sns/forum/user/query?userUuid={uuid}`
   - 从返回的`data.achieveLevel.personalHomePageLink`中提取personalId，如果不存在则无需查询开发统计数据，直接返回基本信息并告诉用户未绑定成就。
   - personalId是链接的最后一部分，例如：`https://www.yingdao.com/achievement/user/773705612499406848`中的`773705612499406848`

2. **开发统计数据获取**
   - 使用personalId查询开发统计数据
   - API：`https://api.yingdao.com/api/eco/noauth/v1/achieve/info/query/appSnsData?personalId={personalId}`
   - 返回数据结构：
     ```json
     {
       "appDevelopStat": {
         "developBlockStat": {
           "monthStatList": [{"statDate": "202603", "statVal": 794}],
           "totalStatVal": 135289
         },
         "developAppStat": {
           "monthStatList": [{"statDate": "202603", "statVal": 9}],
           "totalStatVal": 144
         },
         "ownerAppRunTimeStat": {
           "monthStatList": [{"statDate": "202603", "statVal": 4051199}],
           "totalStatVal": 64566190
         }
       },
       "snsStat": {
         "acceptedStat": {
           "monthStatList": [{"statDate": "202603", "statVal": 5}],
           "totalStatVal": 464
         }
       }
     }
     ```

### 数据字段说明

- `developBlockStat`：开发指令行数统计
  - `monthStatList[0].statVal`：本月开发指令行数
  - `totalStatVal`：总计开发指令行数

- `developAppStat`：开发应用数统计
  - `monthStatList[0].statVal`：本月开发应用数
  - `totalStatVal`：总计开发应用数

- `ownerAppRunTimeStat`：运行时长统计
  - `monthStatList[0].statVal`：本月运行时长（秒）
  - `totalStatVal`：总计运行时长（秒）
  - 需要转换为小时：`statVal / 3600`

- `acceptedStat`：社区采纳统计
  - `monthStatList[0].statVal`：本月社区采纳数量
  - `totalStatVal`：总计社区采纳数量

### 数据处理逻辑

1. 首次查询时，从用户信息中提取personalId并存储
2. 后续查询时，直接使用存储的personalId获取开发统计数据
3. 运行时长需要从秒转换为小时，保留一位小数
4. 所有统计数据都显示本月和总计两个数值

## 注意事项

- 请确保提供的链接格式正确，包含userUuid参数
- 绑定后，系统会记住你的UUID，下次查询时无需重复提供
- 如果查询失败，请检查你的网络连接或稍后重试
- 开发统计数据需要personalId，首次查询后会自动绑定

# 声明
该技能仅用于学习和研究，不涉及任何商业用途。
您可以基于该技能进行修改和扩展，以满足您的特定需求，但请确保遵守影刀RPA社区的使用条款和政策。否则产生的任何问题，我们不承担任何责任。