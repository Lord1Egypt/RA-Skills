# 测试智能家居技能

```bash
# 安装依赖
cd D:\openclaw\workspace\skills\smart-home-unified
npm install

# 测试 CLI
node bin/cli.js --version
node bin/cli.js devices --list
node bin/cli.js scene run "回家模式"
node bin/cli.js automation --list
node bin/cli.js energy --report
```

## 预期输出

```
smart-home-unified v1.0.0

📱 加载设备列表...
客厅主灯 - 小米 - 在线
空调 - 华为 - 在线
窗帘 - HomeKit - 离线

🎬 执行场景：回家模式
✅ 玄关灯已打开
✅ 空调已设置为 26°C
✅ 窗帘已关闭

🤖 自动化列表
1. 晚上自动开灯 - 已启用
2. 离家自动关闭 - 已启用

📊 用电报告
本周用电：50 kWh
预计电费：¥35
节能建议：空调温度调高 1°C，可省电 10%
```

## 下一步

1. 实现各平台真实 API 对接
2. 添加场景编辑器
3. 实现 AI 节能算法
4. 开发手机 App
