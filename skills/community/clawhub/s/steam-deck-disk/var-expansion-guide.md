# Steam Deck /var 分区扩容指南

## 方案选择

### 方案 A：调整分区大小（推荐，一劳永逸）

**风险：** 中等，需要重启，建议先备份重要数据

**步骤：**

1. **备份当前状态**
```bash
sudo sfdisk -d /dev/nvme0n1 > ~/nvme-partitions-backup.txt
```

2. **进入桌面模式，关闭所有应用**

3. **使用 GParted 调整分区**
```bash
sudo pacman -S gparted
sudo gparted
```
- 缩小 /home 分区（nvme0n1p8）
- 扩大 /var 分区（nvme0n1p7）
- 建议给 /var 分配 2-5GB

4. **或者使用命令行（高级用户）**
```bash
# 卸载 /var（需要在救援模式）
sudo umount /var

# 调整分区大小
sudo growpart /dev/nvme0n1 7

# 调整文件系统
sudo resize2fs /dev/nvme0n1p7
```

### 方案 B：创建 systemd mount 覆盖（安全，无需重启）

将 /var 下剩余的小目录也绑定到 /home：

```bash
# 创建目标目录
sudo mkdir -p /home/var-extended/{lib,cache,spool,opt}

# 停止相关服务
sudo systemctl stop systemd-journald

# 移动现有数据
sudo rsync -av /var/lib/ /home/var-extended/lib/
sudo rsync -av /var/cache/ /home/var-extended/cache/

# 创建 systemd mount 单元
sudo tee /etc/systemd/system/var-lib.mount <<EOF
[Unit]
Description=Bind mount /var/lib to /home

[Mount]
What=/home/var-extended/lib
Where=/var/lib
Type=none
Options=bind

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable var-lib.mount
sudo systemctl start var-lib.mount
```

### 方案 C：使用 SteamOS 内置工具（最安全）

SteamOS 3.6+ 提供了分区管理工具：

```bash
# 检查是否有更新
sudo steamos-atomupd check

# 使用官方分区调整脚本（如果有）
sudo steamos-partition-manager --expand-var
```

## 推荐操作

**我建议方案 A**，因为：
1. 一劳永逸，不需要复杂的 bind mount
2. /home 有 195GB 空闲，分出 5GB 给 /var 完全没问题
3. SteamOS 的 ext4 分区支持在线调整

**分配建议：**
- /var: 5GB（足够系统使用）
- /home: 保持 238GB（仍然充裕）

## 执行前准备

1. 备份分区表：`sudo sfdisk -d /dev/nvme0n1 > backup.txt`
2. 确保电量 >50% 或连接电源
3. 关闭所有应用和游戏

## 验证扩容后状态

```bash
df -h /var
lsblk -f | grep nvme
```
