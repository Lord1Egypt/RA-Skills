# wechat-miniprogram-dev - 微信小程序开发技能

_版本：V1.0 | 创建时间：2026-03-08 | 状态：已上线_

---

## 📋 技能描述

微信小程序开发、调试、部署全流程技能，包含测试号限制、模拟模式、常见问题解决方案。

**核心能力：**
- 小程序项目初始化
- 测试号配置与限制处理
- 模拟模式开发（无需云开发）
- 语音识别与正则表达式匹配
- 常见问题诊断与修复

---

## 🎯 触发词

- "编译小程序"
- "开发小程序"
- "小程序测试"
- "微信开发者工具"
- "小程序调试"

---

## 🚀 工作流程

### **Step 1: 项目初始化**

```powershell
# 检查项目结构
Get-ChildItem -Path "miniprogram-项目名" -Recurse -File

# 验证文件完整性
- app.js (云开发初始化)
- app.json (页面配置)
- project.config.json (AppID 配置)
- pages/index/index.js (主逻辑)
- pages/index/index.wxml (页面结构)
- pages/index/index.wxss (样式)
```

### **Step 2: 测试号配置**

**测试号限制：**
- ❌ 云开发控制台按钮灰色（不可用）
- ❌ 无法上传云函数
- ❌ 无法调用真实云数据库
- ✅ 可以编译运行
- ✅ 可以开发界面
- ✅ 可以使用模拟数据

**AppID 配置：**
```json
// project.config.json
{
  "appid": "wx3b2270e4bfe955ee",  // 测试号
  "projectname": "voice-redpacket",
  "cloudfunctionRoot": "cloudfunctions/"
}
```

### **Step 3: 模拟模式开发**

**语音识别模拟：**
```javascript
// pages/index/index.js
recognizeVoice(filePath) {
  const that = this;
  
  wx.showLoading({ title: '识别中...' });

  setTimeout(() => {
    wx.hideLoading();
    
    // 模拟识别结果
    const mockText = '给老婆发 520 红包，祝她生日快乐';
    
    console.log('模拟识别结果:', mockText);
    that.setData({ voiceText: mockText });
    
    // 解析语音指令
    that.parseVoiceCommand(mockText);
    
    wx.showToast({ title: '模拟识别成功', icon: 'success' });
  }, 1000);
}
```

**发送红包模拟：**
```javascript
sendRedPacket() {
  const that = this;
  const { redPacket } = this.data;

  wx.showLoading({ title: '发送中...' });

  setTimeout(() => {
    wx.hideLoading();
    
    console.log('模拟发送成功:', redPacket);
    that.generateRedPacketCard(redPacket);
    
    wx.showToast({ title: '发送成功', icon: 'success' });
    
    that.setData({ redPacket: null, voiceText: '' });
    
    // 添加模拟记录
    const mockRecord = {
      _id: 'mock_' + Date.now(),
      recipient: redPacket.recipient,
      amount: redPacket.amount,
      message: redPacket.message,
      createTime: new Date().toISOString()
    };
    
    that.setData({ 
      recentRecords: [mockRecord, ...that.data.recentRecords]
    });
  }, 500);
}
```

**记录列表模拟：**
```javascript
loadRecentRecords() {
  const that = this;
  
  const mockRecords = [
    {
      _id: 'mock_1',
      recipient: '老婆',
      amount: 520,
      message: '我爱你~',
      createTime: new Date().toISOString()
    },
    {
      _id: 'mock_2',
      recipient: '老妈',
      amount: 200,
      message: '母亲节快乐',
      createTime: new Date(Date.now() - 86400000).toISOString()
    }
  ];
  
  that.setData({ recentRecords: mockRecords });
}
```

### **Step 4: 语音指令解析（含坑点修复）**

**⚠️ 踩过的坑：**

#### **坑 1：空格导致正则匹配失败**

**问题现象：**
```
模拟识别结果：给老婆发 520 红包，祝她生日快乐
文本长度：18
字符码：[32473, 32769, 23110, 21457, 32, 53, 50, 48, 32, ...]
                                     ↑↑
                                   空格空格
正则 1 匹配结果：null
```

**解决方案：**
```javascript
parseVoiceCommand(text) {
  const that = this;
  
  // ✅ 先去除所有空格和标点符号
  const cleanText = text.replace(/[\s,.!?.,]/g, '');
  console.log('清理后文本:', cleanText);
  
  // ✅ 用清理后的文本匹配关键词
  if (cleanText.includes('老婆') && cleanText.includes('红包')) {
    // 提取金额
    const amountMatch = cleanText.match(/(\d+)/);
    const amount = amountMatch ? parseInt(amountMatch[1]) : 520;
    
    // 提取祝福语
    const lastCommaIndex = text.lastIndexOf(',');
    const message = lastCommaIndex > 0 
      ? text.substring(lastCommaIndex + 1).trim() 
      : '恭喜发财，大吉大利';
    
    // ✅ 使用 that.setData 并添加回调
    that.setData({
      redPacket: {
        recipient: '老婆',
        amount: amount,
        message: message
      }
    }, function() {
      console.log('setData 回调执行，redPacket:', that.data.redPacket);
      wx.showToast({ title: '解析成功', icon: 'success' });
    });
    
    that.setData({ isRecording: false });
    return;
  }
}
```

#### **坑 2：setData 不触发页面刷新**

**问题现象：**
- 控制台显示「redPacket 已设置」
- 界面不显示红包预览
- wx:if 条件始终为 false

**解决方案：**
```javascript
// ❌ 错误写法
this.setData({
  redPacket: { recipient: '老婆', amount: 520 }
});

// ✅ 正确写法
const that = this;  // 保存 this 引用
that.setData({
  redPacket: { recipient: '老婆', amount: 520 }
}, function() {
  // 回调函数确保数据已设置
  console.log('setData 回调执行');
});
```

#### **坑 3：正则表达式不支持空格**

**错误示例：**
```javascript
// ❌ 不支持空格
const pattern = /给 (.+?) 发 (\d+) 红包/;
```

**正确示例：**
```javascript
// ✅ 支持空格
const pattern = /给\s*(.+?)\s*发\s*(\d+)\s*红包/;

// ✅ 或者先清理空格
const cleanText = text.replace(/\s+/g, '');
const pattern = /给 (.+?) 发 (\d+) 红包/;
```

### **Step 5: WXML 页面结构**

**红包预览区域：**
```xml
<!-- 红包预览区域 -->
<view class="preview-section">
  <view class="preview-title">红包预览</view>
  <view class="red-packet-card" wx:if="{{redPacket}}">
    <view class="amount">¥{{redPacket.amount}}</view>
    <view class="recipient">给：{{redPacket.recipient}}</view>
    <view class="message">{{redPacket.message}}</view>
    <button class="send-btn" bindtap="sendRedPacket">发送红包</button>
  </view>
  <view wx:else style="padding: 40rpx; text-align: center; color: #999;">
    请先点击「点击说话」按钮，说出红包指令
  </view>
</view>
```

**临时测试按钮：**
```xml
<!-- 测试按钮（临时） -->
<view class="test-section" style="margin-top: 20rpx; text-align: center;">
  <button wx:if="{{redPacket}}" 
          bindtap="sendRedPacket" 
          style="background: #ff6b6b; color: white; font-size: 32rpx; padding: 20rpx 40rpx; border-radius: 10rpx;">
    🧧 测试：发送红包
  </button>
</view>
```

### **Step 6: 编译调试**

**编译步骤：**
1. 点击微信开发者工具顶部「编译」按钮
2. 查看小程序界面是否正常显示
3. 点击「点击说话」按钮测试录音
4. 查看控制台日志

**调试日志：**
```javascript
// 关键日志点
console.log('模拟识别结果:', mockText);
console.log('文本长度:', mockText.length);
console.log('清理后文本:', cleanText);
console.log('关键词检查:', { hasRedPacket, hasLaopo, hasLiWanyu });
console.log('解析成功:', { recipient, amount, message });
console.log('setData 回调执行，redPacket:', that.data.redPacket);
```

**预期日志：**
```
模拟识别结果：你好你好给我。老婆，李婉瑜发一个红包，祝他节日快乐！
文本长度：23
清理后文本：你好你好给我老婆李婉瑜发一个红包祝他节日快乐
关键词检查：{hasRedPacket: true, hasLaopo: true, hasLiWanyu: true}
✅ 匹配到红包指令
解析成功：{recipient: "李婉瑜", amount: 520, message: "祝他节日快乐！"}
setData 回调执行，redPacket: {recipient: "李婉瑜", amount: 520, message: "祝他节日快乐！"}
```

---

## 📁 项目结构

```
miniprogram-voice-redpacket/
├── app.js                          # 云开发初始化
├── app.json                        # 页面配置
├── app.wxss                        # 全局样式
├── project.config.json             # AppID 配置
├── package.json                    # 项目信息
├── cloudfunctions/                 # 云函数（测试号不可用）
│   ├── createRedPacket/index.js    # 创建红包
│   ├── getRedPackets/index.js      # 获取红包列表
│   └── recognizeVoice/index.js     # 语音识别
├── pages/
│   ├── index/                      # 首页
│   │   ├── index.js                # 主逻辑（含模拟模式）
│   │   ├── index.wxml              # 页面结构
│   │   ├── index.wxss              # 样式
│   │   └── index.json              # 页面配置
│   └── records/                    # 记录页
└── DEPLOY.md                       # 部署指南
```

---

## ⚠️ 常见坑点总结

### **坑 1：测试号云开发限制**
- **现象**：云开发控制台按钮灰色
- **原因**：测试号不支持云开发控制台
- **解决**：使用模拟模式开发界面，正式号再部署云函数

### **坑 2：空格导致正则匹配失败**
- **现象**：控制台显示「未匹配到红包指令」
- **原因**：语音识别结果包含空格
- **解决**：先 `text.replace(/[\s,.!?.,]/g, '')` 清理空格和标点

### **坑 3：setData 不刷新页面**
- **现象**：数据已设置但界面不更新
- **原因**：`this` 指向问题或缺少回调
- **解决**：用 `const that = this` 保存引用，添加回调函数

### **坑 4：正则表达式不支持空格**
- **现象**：正则匹配返回 null
- **原因**：正则没考虑空格
- **解决**：用 `\s*` 匹配空格，或先清理空格

### **坑 5：wx:if 条件不生效**
- **现象**：预览区域不显示
- **原因**：数据未设置或条件判断错误
- **解决**：添加 `wx:else` 分支显示提示，检查 setData 回调

---

## 🎯 最佳实践

### **1. 模拟模式开发流程**
1. 测试号编译运行
2. 模拟数据测试流程
3. 验证 UI/UX 设计
4. 正式号部署云函数

### **2. 语音指令解析**
1. 清理空格和标点
2. 关键词匹配优先
3. 正则表达式兜底
4. 添加详细调试日志

### **3. setData 使用**
1. 保存 `this` 引用：`const that = this`
2. 添加回调函数确认数据设置
3. 控制台日志验证

### **4. 调试日志**
1. 文本长度和字符码
2. 清理后文本
3. 关键词检查结果
4. setData 回调执行

---

## 🚀 使用说明

### **开发小程序**
```
编译小程序 [voice-redpacket]
```

### **测试流程**
```
测试小程序流程 [voice-redpacket]
```

### **诊断问题**
```
小程序诊断 [问题描述]
```

### **部署云函数**
```
部署云函数 [voice-redpacket]
```

---

## 📝 版本记录

| 版本号 | 修改时间 | 修改内容 | 修改人 |
|--------|----------|----------|--------|
| V1.0 | 2026-03-08 19:30 | 初始版本，包含测试号开发全流程和坑点总结 | 阿福 |

---

_本技能由阿福开发，基于语音发红包小程序实战经验总结_
