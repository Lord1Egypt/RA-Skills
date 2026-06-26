# 微信小程序开发 - 环境信息

## 当前项目配置

- **AppID**: wx637a3fa923864f90
- **云开发环境**: cloudbase-5g2zxj6y510bc574
- **私钥路径**: ./key/private.key
- **小程序根目录**: miniprogram/
- **云函数根目录**: cloudfunctions/

## 已部署的云函数

- getTaskProgress - 获取任务进度
- getHistory - 获取历史记录
- imageCallback - 图像处理回调
- restorePhoto - 照片修复
- addWatermark - 添加水印
- sendSubscribeMessage - 订阅消息
- getUserInfo - 用户信息
- createOrder - 创建订单
- payCallback - 支付回调

## 常用命令

### 部署云函数
```bash
cd /root/.openclaw/workspace-main/weapp-photo-restore
npx miniprogram-ci cloud functions upload --pp ./ --pkp ./key/private.key -r 1 -e cloudbase-5g2zxj6y510bc574 -n 函数名 -p ./cloudfunctions/函数名 --rnpm
```

### 生成预览
```bash
cd /root/.openclaw/workspace-main/weapp-photo-restore/miniprogram
npx miniprogram-ci preview --pp . --pkp ../key/private.key --qr-dest ../preview-qrcode.png --qr-format image --appid wx637a3fa923864f90 -r 1 --enable-qrcode true --uv "1.0.0" --threads 0 --use-cos false
```