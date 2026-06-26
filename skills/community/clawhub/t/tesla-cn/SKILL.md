---
name: tesla-cn
description: 面向中国特斯拉车主的远程控制技能，基于特斯拉官方车队 API（Fleet API）实现，使用简单、体验自然。
author: Libin
---

## Tesla CN Skill

面向中国特斯拉车主的远程控制技能，基于特斯拉官方车队 API（Fleet API）实现，使用简单、体验自然。

## Setup

### Requirements

- Node.js 18 或更高版本（内置 `fetch`）
- 一个在 `https://tesla.dhuar.com` 获取的 `apiKey`

> `{baseDir}` 通常为当前 workspace 根目录，例如 `/home/robin/.openclaw/workspace`。

### apiKey 存放位置（推荐）

默认会从当前用户主目录下的 `~/.tesla_cn.json` 读取 `apiKey`。  
配置文件示例内容：

```json
{
  "apiKey": "YOUR_API_KEY"
}
```

- Linux / macOS：路径形如 `/home/<user>/.tesla_cn.json` 或 `/Users/<user>/.tesla_cn.json`
- Windows：路径形如 `C:\Users\<User>\.tesla_cn.json`（内部仍使用用户主目录自动解析）

> 如果同时在命令行参数中传入 `apiKey=...`，**命令行参数优先**，会覆盖配置文件中的值。

### 一键初始化配置文件

你可以使用随技能附带的脚本来创建或更新 `~/.tesla_cn.json`：

```bash
node {baseDir}/skills/tesla-cn/scripts/init-tesla-config.js \
  apiKey="YOUR_API_KEY"
```

成功后会在当前用户主目录生成/更新 `~/.tesla_cn.json`，之后使用下面的命令时可以省略 `apiKey` 参数。

### 参数格式

- 第 1 个参数：`type=...`（`endpoints` / `commands` / `endpoints/commands`）
- 第 2 个参数：`name=...`
- 第 3 个及之后：可选 `vin=...`、`data='{"key":"value"}'`

## Commands

```bash
# 车辆列表（GET /api/1/vehicles）
node {baseDir}/skills/tesla-cn/scripts/tesla-command.js \
  type=endpoints \
  name=list

# 车辆详情（GET /api/1/vehicles/{vin}）
node {baseDir}/skills/tesla-cn/scripts/tesla-command.js \
  type=endpoints \
  name=vehicle \
  vin="YOUR_VIN"

# 车辆实时状态（GET /api/1/vehicles/{vin}/vehicle_data）
node {baseDir}/skills/tesla-cn/scripts/tesla-command.js \
  type=endpoints \
  name=vehicle_data \
  vin="YOUR_VIN"

# 车辆允许的驾驶员列表（GET /api/1/vehicles/{vin}/drivers）
node {baseDir}/skills/tesla-cn/scripts/tesla-command.js \
  type=endpoints \
  name=drivers \
  vin="YOUR_VIN"

# 车辆订阅资格（GET /api/1/dx/vehicles/subscriptions/eligibility?vin={vin}）
node {baseDir}/skills/tesla-cn/scripts/tesla-command.js \
  type=endpoints \
  name=eligible_subscriptions \
  vin="YOUR_VIN"

# 车辆保修信息（GET /api/1/dx/warranty/details）
node {baseDir}/skills/tesla-cn/scripts/tesla-command.js \
  type=endpoints \
  name=warranty_details

# fleet_status：多个车辆的聚合状态（POST /api/1/vehicles/fleet_status）
node {baseDir}/skills/tesla-cn/scripts/tesla-command.js \
  type=endpoints \
  name=fleet_status \
  data='{"vins":["VIN1","VIN2"]}'

# 唤醒车辆（POST /api/1/vehicles/{vin}/wake_up）
node {baseDir}/skills/tesla-cn/scripts/tesla-command.js \
  type=endpoints \
  name=wake_up \
  vin="YOUR_VIN"

# 开启车内空调（POST /api/1/vehicles/{vin}/command/auto_conditioning_start）
node {baseDir}/skills/tesla-cn/scripts/tesla-command.js \
  type=commands \
  name=auto_conditioning_start \
  vin="YOUR_VIN"

# 关闭车内空调（POST /api/1/vehicles/{vin}/command/auto_conditioning_stop）
node {baseDir}/skills/tesla-cn/scripts/tesla-command.js \
  type=commands \
  name=auto_conditioning_stop \
  vin="YOUR_VIN"

# 闪灯（POST /api/1/vehicles/{vin}/command/flash_lights）
node {baseDir}/skills/tesla-cn/scripts/tesla-command.js \
  type=commands \
  name=flash_lights \
  vin="YOUR_VIN"

# 车门上锁（POST /api/1/vehicles/{vin}/command/door_lock）
node {baseDir}/skills/tesla-cn/scripts/tesla-command.js \
  type=commands \
  name=door_lock \
  vin="YOUR_VIN"

# 打开充电口盖（POST /api/1/vehicles/{vin}/command/charge_port_door_open）
node {baseDir}/skills/tesla-cn/scripts/tesla-command.js \
  type=commands \
  name=charge_port_door_open \
  vin="YOUR_VIN"

# 关闭充电口盖（POST /api/1/vehicles/{vin}/command/charge_port_door_close）
node {baseDir}/skills/tesla-cn/scripts/tesla-command.js \
  type=commands \
  name=charge_port_door_close \
  vin="YOUR_VIN"

# 前备箱 / 后备箱（POST /api/1/vehicles/{vin}/command/actuate_trunk）
# which_trunk 可为 "front" 或 "rear"
node {baseDir}/skills/tesla-cn/scripts/tesla-command.js \
  type=commands \
  name=actuate_trunk \
  vin="YOUR_VIN" \
  data='{"which_trunk":"front"}'

node {baseDir}/skills/tesla-cn/scripts/tesla-command.js \
  type=commands \
  name=actuate_trunk \
  vin="YOUR_VIN" \
  data='{"which_trunk":"rear"}'

# 鸣笛（POST /api/1/vehicles/{vin}/command/honk_horn）
node {baseDir}/skills/tesla-cn/scripts/tesla-command.js \
  type=commands \
  name=honk_horn \
  vin="YOUR_VIN"

# 远程外放声音（POST /api/1/vehicles/{vin}/command/remote_boombox）
# 声音 ID 示例：
# 0    → 随机放屁
# 2000 → 定位哔声
node {baseDir}/skills/tesla-cn/scripts/tesla-command.js \
  type=commands \
  name=remote_boombox \
  vin="YOUR_VIN" \
  data='{"sound":2000}'
```

## Safety

- 这是对 Tesla 车辆的远程控制，建议先使用 `list` 命令确认连接与权限，再尝试 `commands`。
- 避免在不确认环境安全的情况下对真实车辆执行 `door_lock` / `actuate_trunk` 等操作。
- `honk_horn`、`remote_boombox` 等命令可能对周围造成骚扰，建议在安全、合规的环境中谨慎使用。

## Privacy

- 不要将你的 `apiKey`、VIN 或包含位置信息的原始响应输出提交到 git 仓库。
- 如需分享日志，建议先手动脱敏（去掉 `apiKey`、VIN、地理位置等字段）。


