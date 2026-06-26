# 语音发红包小程序 🧧🎤

一个可以通过语音控制发送红包的微信小程序 MVP 版本。

---

## 📱 功能特性

- ✅ 语音识别输入
- ✅ 智能解析红包指令（金额 + 收款人 + 祝福语）
- ✅ 红包预览确认
- ✅ 红包记录管理
- ✅ 云开发集成

---

## 🛠️ 技术栈

- **前端**：微信小程序原生开发
- **后端**：微信云开发（CloudBase）
- **语音识别**：腾讯云语音识别 API（待集成）
- **数据库**：云开发数据库

---

## 📁 项目结构

```
miniprogram-voice-redpacket/
├── app.js                      # 小程序入口
├── app.json                    # 小程序配置
├── app.wxss                    # 全局样式
├── project.config.json         # 项目配置
├── pages/
│   ├── index/                  # 首页（语音发红包）
│   │   ├── index.js
│   │   ├── index.wxml
│   │   ├── index.wxss
│   │   └── index.json
│   └── record/                 # 记录页
│       ├── record.js
│       ├── record.wxml
│       ├── record.wxss
│       └── record.json
└── cloudfunctions/
    ├── createRedPacket/        # 创建红包云函数
    ├── getRedPackets/          # 查询红包云函数
    └── recognizeVoice/         # 语音识别云函数
```

---

## 🚀 快速开始

### 1️⃣ 导入项目

1. 打开微信开发者工具
2. 导入项目：选择 `miniprogram-voice-redpacket` 文件夹
3. 填入你的小程序 AppID

### 2️⃣ 配置云开发

1. 打开 `app.js`
2. 修改云开发环境 ID：
```javascript
wx.cloud.init({
  env: 'card-native-2gvohkdhd8a64b2d'  // 你的环境 ID
});
```

### 3️⃣ 上传云函数

在微信开发者工具中：
1. 右键点击 `cloudfunctions` 文件夹
2. 选择「上传并部署：云端安装依赖」
3. 等待上传完成

### 4️⃣ 创建数据库

1. 打开云开发控制台
2. 创建集合：`red_packets`
3. 设置权限：仅创建者可读写

### 5️⃣ 编译运行

点击编译按钮，即可在模拟器中查看效果！

---

## 🎤 语音指令示例

- "给老婆发 520 红包，祝她生日快乐"
- "发 200 块红包给爸爸，生日快乐"
- "给张三发个 100 元红包，恭喜发财"

---

## 📝 数据库结构

**集合名：** `red_packets`

```json
{
  "_id": "自动生成",
  "_openid": "用户 openid",
  "recipient": "收款人",
  "amount": 520,
  "message": "祝福语",
  "status": "sent",
  "createTime": "服务器时间"
}
```

---

## ⚠️ 注意事项

### 当前版本（MVP）
- ✅ 语音识别使用模拟结果
- ✅ 红包记录保存到数据库
- ❌ 暂未集成真实微信支付
- ❌ 暂未集成真实红包发送

### 下一步
1. 集成腾讯云语音识别 API
2. 申请微信支付权限
3. 实现真实红包发送
4. 优化 UI/UX

---

## 📞 开发环境

- **微信开发者工具**：最新版
- **基础库版本**：2.19.4+
- **云开发环境**：card-native-2gvohkdhd8a64b2d（体验版）

---

## 🎯 开发计划

- [ ] 集成真实语音识别 API
- [ ] 实现微信支付对接
- [ ] 红包分享功能
- [ ] 成就系统
- [ ] 邀请好友功能

---

_Created by 阿福 & Xiabi | 2026-03-08_
