# blackbird-upload

批量上传 FIT 文件到黑鸟骑行网页版 (https://www.blackbirdsport.com)

## 用途

- 自动上传修改后的 `_GM.fit` 文件到黑鸟骑行平台
- 支持批量上传多个文件
- 自动检测登录状态，支持手动登录

## 依赖

- Python 3.x
- Playwright: `pip install playwright`
- Playwright 浏览器：`playwright install chromium`

## 安装依赖

```bash
# 使用 conda Python
/home/ckboss/anaconda3/bin/pip install playwright
/home/ckboss/anaconda3/bin/playwright install chromium
```

## 使用方法

### 上传单个文件

```bash
cd /home/ckboss/.openclaw/workspace/skills/blackbird-upload/scripts
/home/ckboss/anaconda3/bin/python upload_to_blackbird.py /path/to/ride_GM.fit
```

### 上传整个目录

```bash
/home/ckboss/anaconda3/bin/python upload_to_blackbird.py /home/ckboss/Downloads/onelap-rides-0316-0321/
```

### 上传多个文件（通配符）

```bash
/home/ckboss/anaconda3/bin/python upload_to_blackbird.py /home/ckboss/Downloads/onelap-rides-0316-0321/*_GM.fit
```

## 工作流程

1. **启动浏览器** - 打开黑鸟骑行上传页面
2. **检测登录** - 如果未登录，等待用户手动登录（最长 5 分钟）
3. **上传文件** - 自动选择并上传所有 FIT 文件
4. **等待完成** - 等待上传完成后显示结果

## 注意事项

- **首次运行需要登录** - 脚本会等待你在浏览器中登录黑鸟账号
- **登录状态保持** - 浏览器会保存 cookies，下次运行可能无需重新登录
- **文件命名** - 优先上传 `_GM.fit` 文件（已修改设备 ID 的版本）
- **重复检测** - 黑鸟会自动检测重复文件，避免重复上传

## 完整流程示例

```bash
# 1. 修改 FIT 文件设备 ID
/home/ckboss/anaconda3/bin/python /home/ckboss/.openclaw/workspace/skills/fit-device-id-modifier/scripts/modify_fit.py /path/to/rides/

# 2. 上传到黑鸟
/home/ckboss/anaconda3/bin/python /home/ckboss/.openclaw/workspace/skills/blackbird-upload/scripts/upload_to_blackbird.py /path/to/rides/*_GM.fit
```

## 文件结构

```
skills/blackbird-upload/
├── SKILL.md
└── scripts/
    └── upload_to_blackbird.py
```

## 相关 Skill

- `fit-device-id-modifier` - 修改 FIT 文件设备 ID 为 Garmin Edge 500

## 故障排除

### 浏览器无法启动
```bash
# 重新安装 Playwright 浏览器
/home/ckboss/anaconda3/bin/playwright install chromium
```

### 上传超时
- 检查网络连接
- 确认黑鸟网站可访问
- 尝试减少单次上传的文件数量

### 登录状态失效
- 清除浏览器缓存后重新登录
- 或者使用 `headless=False` 模式手动登录
