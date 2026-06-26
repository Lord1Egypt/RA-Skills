# 数据源配置参考

## 千里马招标网

### 基本信息
- **官网**: https://vip.qianlima.com
- **登录页**: https://vip.qianlima.com/login
- **搜索页**: https://vip.qianlima.com/business-opportunity/bidding-info

### API 接口
```
POST https://vip.qianlima.com/rest/service/website/search/solr/tender
Content-Type: application/json

{
  "T": 时间戳,
  "newAreas": "4",  // 甘肃省
  "keywords": "安防",
  "currentPage": 1,
  "numPerPage": 20
}
```

### 响应字段
```javascript
{
  "code": 200,
  "data": {
    "data": [
      {
        "contentid": "唯一ID",
        "popTitle": "标题",
        "areaName": "地区",
        "updateTime": "发布时间",
        "tenderAmountNumber": "金额数字",
        "tenderAmountUnit": "金额单位",
        "noticeSegmentTypeName": "公告类型",
        "tenderees": "招标单位",
        "agent": "代理机构",
        "url": "详情链接"
      }
    ]
  }
}
```

## 中项网 (vip.ccpc360.com)

### 基本信息
- **官网**: https://vip.ccpc360.com
- **搜索页**: https://vip.ccpc360.com/#/projectQuery/bidding
- **状态**: ✅ 已打通，每日自动采集

### 技术方案
- **登录方式**: Chrome CDP + Cookie复用
- **采集方式**: Playwright浏览器自动化
- **去重机制**: 标题+地区联合去重
- **合并策略**: 与千里马数据合并存储

### 关键词列表
```javascript
['安防', '监控', '智能化', '弱电', '门禁', '报警', '视频监控', 
 '智慧安防', '楼宇对讲', '停车场管理', '电子巡更', '入侵报警', 
 '门禁系统', '监控系统', '安防监控', '智能安防']
```

### 数据字段
```javascript
{
  title: "项目名称",
  area: "地区",
  unit: "招标单位",
  agent: "招标代理",
  date: "发布时间",
  keyword: "匹配关键词",
  source: "zhongxiang"
}
```

### 注意事项
- ⚠️ 需要Chrome保持开启（--remote-debugging-port=9222）
- ⚠️ Cookie有效期约7天，需定期重新登录
- ⚠️ 网站有115层营销弹窗，需先清理才能操作

## 甘肃政府采购网

### 基本信息
- **官网**: http://www.ccgp-gansu.gov.cn
- **状态**: ⏳ 待攻克（反爬机制复杂）

### 待研究
- 页面结构
- 反爬机制
- 数据接口

## 其他地区扩展

### 青海省
- 青海政府采购网

### 宁夏
- 宁夏政府采购网

### 新疆
- 新疆政府采购网
