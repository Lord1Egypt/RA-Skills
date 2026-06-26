# VLAN Linux 客户端管理技能

用于管理 VLAN.CN 虚拟组网 Linux 客户端的安装、配置和日常操作。

## 触发条件

当用户询问以下相关内容时触发：
- VLAN.CN Linux 客户端安装
- vlancli 命令使用
- 组网连接/断开
- 登录/账号管理
- 服务控制（启动/停止/重启）
- 网络诊断和调试

## 系统要求

### 支持的发行版
- Ubuntu: 18.04 及以上
- Debian: 10 及以上
- CentOS: 7 及以上
- Fedora: 30 及以上
- Arch Linux

## 核心命令参考

### 安装命令
```bash
curl -kfsSL http://dl.vlan.cn/vlan2.0/linux/install.sh | sh
```

### 基础用法
```bash
vlancli [options] command
```

**常用选项:**
| 选项 | 说明 |
|------|------|
| `-b, --batch` | 非交互模式 (静默执行) |
| `-c, --config=DIR` | 指定配置文件目录 |
| `-d, --loglevel=num` | 日志级别 (1:Info, 2:Debug, 3:Trace) |
| `--help` | 显示帮助信息 |

### 账号登录

**方式一：登录码登录（推荐）**
```bash
vlancli login login_code_dRGulkXga4ia1zf38kekc6hi
```
优势：无需每次输入密码，登录码有效期 30 分钟自动刷新

**方式二：用户名密码登录**
```bash
vlancli login <用户名> <密码> [服务器地址]
# 示例
vlancli login myuser mypassword
```

### 连接组网流程
```bash
# 1. 启动服务
vlancli start

# 2. 获取组列表
vlancli getvlanlist

# 3. 连接至指定组
vlancli connect <VlanID>
```

### 服务控制
| 动作 | 命令 | 说明 |
|------|------|------|
| 启动 | `vlancli start` | 启动后台服务 |
| 停止 | `vlancli stop` | 停止后台服务 |
| 重启 | `vlancli restart` | 重启后台服务 |
| 状态 | `vlancli status` | 查看后台服务运行状态 |

### 组网管理
| 功能 | 命令 | 说明 |
|------|------|------|
| 查看组列表 | `vlancli getvlanlist` | 显示已加入的虚拟网组 |
| 连接组 | `vlancli connect <VlanID>` | 连接指定组 |
| 断开连接 | `vlancli disconnect <VlanID>` | 断开与指定组的连接 |
| 查看节点 | `vlancli getnodelist <VlanID>` | 查看组内在线节点列表 |
| 加入组 | `vlancli joinvlan <VlanID>` | 加入新的虚拟网组 |
| 退出组 | `vlancli quitvlan <VlanID>` | 退出已加入的虚拟网组 |

### 调试与诊断
| 功能 | 命令 | 说明 |
|------|------|------|
| 本机信息 | `vlancli info` | 查看客户端运行状态及本机信息 |
| 调试日志 | `vlancli debug <Level>` | 设置日志级别 (1-3) |
| KCP 加速 | `vlancli usekcp <NodeID> <1\|0>` | 开启 (1) 或关闭 (0) 指定节点的 KCP 加速 |
| 导出节点 | `vlancli dump edges` | 查看所有已知的边缘节点信息 |
| 导出路径 | `vlancli dump paths` | 查看网络路径及延迟信息 |

## 使用示例

### 示例 1: 首次安装和配置
用户：如何在 Linux 上安装 VLAN 客户端？

回复：
```bash
# 使用官方一键安装脚本
curl -kfsSL http://dl.vlan.cn/vlan2.0/linux/install.sh | sh

# 安装完成后，使用登录码登录（推荐）
vlancli login <你的登录码>

# 启动服务
vlancli start

# 查看可用组网
vlancli getvlanlist

# 连接到组网
vlancli connect <组网 ID>
```

### 示例 2: 日常连接
用户：帮我连接到 VLAN 组网

回复：
```bash
# 检查服务状态
vlancli status

# 如果未启动，先启动服务
vlancli start

# 查看可用组网
vlancli getvlanlist

# 连接到指定组网（替换 <ID> 为实际组网 ID）
vlancli connect <ID>

# 验证连接
vlancli info
```

### 示例 3: 故障排查
用户：VLAN 连接不上，怎么排查？

回复：
```bash
# 1. 检查服务状态
vlancli status

# 2. 查看本机信息和连接状态
vlancli info

# 3. 提高日志级别进行调试
vlancli debug 3

# 4. 查看网络路径和延迟
vlancli dump paths

# 5. 查看边缘节点信息
vlancli dump edges

# 6. 尝试重启服务
vlancli restart
```

## 注意事项

1. **登录安全**：推荐使用登录码方式，避免在命令行历史中留下密码
2. **登录码有效期**：登录码仅 30 分钟有效，超时需重新生成
3. **权限要求**：部分命令可能需要 sudo 权限
4. **防火墙**：确保系统防火墙允许 VLAN 客户端的网络流量
5. **网络依赖**：客户端需要能访问 api.vlan.cn 服务器

## 常见问题

### Q: 登录后提示认证失败？
A: 检查登录码是否过期（30 分钟有效期），或用户名密码是否正确

### Q: 连接组网后无法访问资源？
A: 
1. 检查 `vlancli status` 确认服务运行正常
2. 使用 `vlancli info` 查看本机获取的 IP 地址
3. 检查防火墙规则
4. 尝试 `vlancli dump paths` 查看网络路径

### Q: 如何完全卸载？
A: 运行安装脚本时添加卸载参数，或手动删除：
```bash
# 停止服务
vlancli stop

# 删除客户端文件（具体路径参考安装文档）
sudo rm -rf /usr/local/vlan
```

---

**技能版本**: 1.0  
**最后更新**: 2026-03-18  
**适用客户端**: VLAN.CN Linux Client v2.0
