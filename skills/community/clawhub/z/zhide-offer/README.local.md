# zhide-offer 本地接入说明

## 已安装位置

`~/.openclaw/skills/zhide-offer`

## 配置 API Key

二选一：

### 方式 1：环境变量（推荐）

```bash
export ZHIDE_OFFER_KEY='ofk_your_key_here'
```

### 方式 2：本地配置文件

复制模板并填写：

```bash
cp ~/.openclaw/skills/zhide-offer/scripts/config.json.template ~/.openclaw/skills/zhide-offer/scripts/config.json
```

然后把 `zhideOfferKey` 改成真实 key。

## 可用脚本

```bash
node ~/.openclaw/skills/zhide-offer/scripts/jobs_search.js 数据产品经理
node ~/.openclaw/skills/zhide-offer/scripts/jobs_get.js <岗位ID>
node ~/.openclaw/skills/zhide-offer/scripts/interviews_search.js 产品经理 --company 字节跳动 --tag 校招 --limit 5
node ~/.openclaw/skills/zhide-offer/scripts/interviews_get.js <面经ID>
```

## 快捷入口

直接用 skill 自带包装命令就行：

```bash
bash ~/.openclaw/skills/zhide-offer/scripts/zhide_offer.sh jobs-search 产品经理 --size 3
bash ~/.openclaw/skills/zhide-offer/scripts/zhide_offer.sh job-get <岗位ID>
bash ~/.openclaw/skills/zhide-offer/scripts/zhide_offer.sh interviews-search 产品经理 --limit 2
bash ~/.openclaw/skills/zhide-offer/scripts/zhide_offer.sh interview-get <面经ID>
bash ~/.openclaw/skills/zhide-offer/scripts/zhide_offer.sh quota
```

## 说明

这个包本质上是“技能说明 + Node 查询脚本”，不是带 tool schema 的 OpenClaw 原生扩展。
当前已经完成本地安装落位，可直接在本机通过这些脚本调用。
发布到市场时不要携带真实 `scripts/config.json`，公开版本只保留模板或占位值。
如果要进一步变成完全原生的 OpenClaw 一等工具，还需要额外封装 tool 接口或 MCP bridge。
