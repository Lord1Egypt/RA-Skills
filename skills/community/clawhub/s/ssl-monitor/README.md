# SSL 证书查询技能

## 文件结构
```
ssl-monitor/
├── SKILL.md          # 技能定义文件（必需）
└── check-ssl.sh      # 可选：批量检查脚本
```

## 安装

1. 复制 `ssl-monitor/` 文件夹到 OpenClaw 技能目录：
   ```bash
   cp -r ssl-monitor ~/.openclaw/skills/
   ```

2. 重启 OpenClaw Gateway（如果需要）：
   ```bash
   openclaw gateway restart
   ```

## 使用方法

### 直接对话查询
```
查 baidu.com 证书
SSL 证书 example.com
xxx.cn 还有多久过期
```

### 命令行查询
```bash
domain="example.com"
expiry=$(echo | openssl s_client -servername $domain -connect $domain:443 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
expiry_epoch=$(date -d "$expiry" +%s 2>/dev/null)
now_epoch=$(date +%s)
days_left=$(( ($expiry_epoch - $now_epoch) / 86400 ))
echo "$domain: $days_left 天后过期 ($expiry)"
```

### 批量检查
```bash
# 编辑域名列表
nano ssl-domains.txt

# 运行检查
./check-ssl.sh ssl-domains.txt
```

## 依赖

- `openssl`（Linux/macOS 默认已安装）

## 状态说明

| 状态 | 剩余天数 | 说明 |
|------|----------|------|
| 正常 | ≥ 30 天 | 无需操作 |
| 注意 | 7-29 天 | 计划续期 |
| 紧急 | < 7 天 | 立即续期 |

---

**版本：** 1.0
