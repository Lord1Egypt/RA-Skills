---
name: universal-beijing-resort
display_name: 北京环球影城游园助手
description: 零配置即装即用，提供7项游园工具，含实时排队查询和智能推荐下一步，基于themeparks.wiki实时数据与本地预设数据。
tags: [环球影城, 北京环球影城, 游园, 排队, 路线规划, 演出, 餐厅, 门票, Universal, 主题乐园, 亲子游, 哈利波特, 变形金刚]
tools:
  - name: universal_ticket
    description: 查询北京环球影城门票价格和优速通价格
    parameters:
      - name: date
        type: string
        description: 游览日期，格式YYYY-MM-DD
        required: false
      - name: query
        type: string
        description: 查询关键词如2成人1儿童
        required: false
  - name: universal_wait_times
    description: 查询北京环球影城游乐设施实时排队等待时间
    parameters:
      - name: query
        type: string
        description: 筛选条件如刺激项目、室内项目、变形金刚
        required: false
  - name: universal_show_schedule
    description: 查询北京环球影城园区演出场次时间及观赏建议
    parameters:
      - name: date
        type: string
        description: 日期YYYY-MM-DD
        required: false
      - name: query
        type: string
        description: 筛选条件如必看、水世界
        required: false
  - name: universal_smart_next
    description: 根据当前情况智能推荐北京环球影城最佳下一步游玩项目
    parameters:
      - name: query
        type: string
        description: 自然语言描述如带5岁孩子、亲子游、刺激路线
        required: false
  - name: universal_route
    description: 规划北京环球影城一日游完整路线
    parameters:
      - name: query
        type: string
        description: 路线类型如亲子一日游、刺激路线、带5岁孩子
        required: false
  - name: universal_schedule
    description: 查询北京环球影城近期营业时间
    parameters:
      - name: days
        type: integer
        description: 查询天数，默认7，最多14
        required: false
  - name: universal_dining
    description: 查询北京环球影城园区餐厅和美食推荐
    parameters:
      - name: query
        type: string
        description: 筛选条件如哈利波特餐厅、便宜的小食、烤肉
        required: false
---

# 北京环球影城游园助手

零配置即装即用，提供7项游园工具，含实时排队查询和智能推荐下一步，基于themeparks.wiki实时数据与本地预设数据。专注北京环球影城，支持自然语言输入，自动识别意图调用对应工具。

## 能做什么

- **实时排队**：查询各设施当前等待时间（实时数据，含单人通道等待时间）
- **智能推荐**：基于同行人年龄、偏好和当前排队，推荐最适合的下一个项目
- **路线规划**：生成亲子/刺激/均衡三种风格的一日游路线
- **演出时间**：查询必看演出场次、最佳观赏位置、建议到场时间
- **营业时间**：查询近14天开闭园时间（themeparks.wiki实时数据）
- **餐厅推荐**：按区域/菜系/价格筛选园区餐厅
- **门票价格**：查询淡季/平季/旺季/特定日票价和优速通价格

## 不能做什么

- 不能在线购票或预约（请通过北京环球影城官方App购票）
- 不能查询酒店预订信息（可搭配酒店搜索技能使用）
- 实时排队数据依赖第三方API，偶有延迟属于正常

## 使用示例

1. "环球影城排队情况怎么样"
2. "带5岁孩子去环球影城，推荐路线"
3. "今天有什么演出"
4. "推荐下一步玩什么"
5. "环球影城门票多少钱"
6. "园区有什么吃的"

## 注意事项

- 排队等待时间为实时数据，仅供参考，实际以园区公告为准
- 营业时间可能因节假日、特殊活动调整，请以官方公告为准
- 门票价格仅供参考，以官方实时价格为准
- 身高限制是硬门槛，带小孩时需特别注意
- **数据流向**：实时排队和营业时间查询通过themeparks.wiki公开API获取，API不存储用户数据；其余功能为本地内置数据

## 使用提示

- 霸天虎过山车和哈利·波特禁忌之旅全天排队最长，建议开园首冲
- 带小孩优先选"亲子路线"，避免排队超过40分钟的刺激项目
- 霍格沃茨城堡夜间魔法秀需提前30分钟占位，最佳位置在城堡正前方
- 错峰就餐：11点前或14点后人少，黄油啤酒必喝
- 出园后可在城市大道用餐（无需门票），全聚德、哈根达斯等可选
