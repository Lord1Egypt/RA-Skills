# system_cmd 技能使用示例

## 基本用法

### 1. 查看帮助
```
/system_cmd help
```
或
```
/system_cmd
```

**输出示例**:
```
📋 **system_cmd 技能帮助**

**用法**: /system_cmd <命令名>

**支持的命令**:
- **ipconfig**: 查看网络接口配置和IP地址
- **tasklist**: 查看当前运行的进程列表
- **netstat**: 查看所有网络连接和监听端口
- **systeminfo**: 查看详细的系统信息

**示例**:
- `/system_cmd ipconfig` - 查看IP配置
- `/system_cmd tasklist` - 查看进程列表
- `/system_cmd netstat` - 查看网络连接
- `/system_cmd systeminfo` - 查看系统信息
```

### 2. 查看IP配置
```
/system_cmd ipconfig
```

**输出示例**:
```
📊 IPCONFIG 命令执行结果
==================================================
Windows IP Configuration

   Host Name . . . . . . . . . . . . : DESKTOP-QQFI8LR
   Primary Dns Suffix  . . . . . . . : 
   Node Type . . . . . . . . . . . . : Hybrid
   IP Routing Enabled. . . . . . . . : No
   WINS Proxy Enabled. . . . . . . . : No

Ethernet adapter Ethernet0:

   Connection-specific DNS Suffix  . : 
   Description . . . . . . . . . . . : Intel(R) Ethernet Connection (7) I219-LM
   Physical Address. . . . . . . . . : 00-0C-29-XX-XX-XX
   DHCP Enabled. . . . . . . . . . . : Yes
   Autoconfiguration Enabled . . . . : Yes
   Link-local IPv6 Address . . . . . : fe80::xxxx:xxxx:xxxx:xxxx%12(Preferred)
   IPv4 Address. . . . . . . . . . . : 192.168.1.100(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Lease Obtained. . . . . . . . . . : 2026年4月8日 21:30:15
   Lease Expires . . . . . . . . . . : 2026年4月9日 21:30:15
   Default Gateway . . . . . . . . . : 192.168.1.1
   DHCP Server . . . . . . . . . . . : 192.168.1.1
   DHCPv6 IAID . . . . . . . . . . . : 123456789
   DHCPv6 Client DUID. . . . . . . . : 00-01-00-01-XX-XX-XX-XX-XX-XX-XX-XX
   DNS Servers . . . . . . . . . . . : 192.168.1.1
                                       8.8.8.8
   NetBIOS over Tcpip. . . . . . . . : Enabled
==================================================
✅ 命令执行完成
```

### 3. 查看进程列表
```
/system_cmd tasklist
```

**输出示例**:
```
📊 TASKLIST 命令执行结果
==================================================
Image Name                     PID Session Name        Session#    Mem Usage
========================= ======== ================ =========== ============
System Idle Process              0 Services                   0          8 K
System                           4 Services                   0      1,028 K
Registry                       136 Services                   0     68,864 K
smss.exe                       528 Services                   0      1,056 K
csrss.exe                      788 Services                   0      3,888 K
wininit.exe                    880 Services                   0      3,680 K
...
==================================================
✅ 命令执行完成
```

### 4. 查看网络连接
```
/system_cmd netstat
```

**输出示例**:
```
📊 NETSTAT 命令执行结果
==================================================
Active Connections

  Proto  Local Address          Foreign Address        State
  TCP    0.0.0.0:135            0.0.0.0:0              LISTENING
  TCP    0.0.0.0:445            0.0.0.0:0              LISTENING
  TCP    0.0.0.0:5040           0.0.0.0:0              LISTENING
  TCP    0.0.0.0:7680           0.0.0.0:0              LISTENING
  TCP    0.0.0.0:49664          0.0.0.0:0              LISTENING
  TCP    0.0.0.0:49665          0.0.0.0:0              LISTENING
  TCP    0.0.0.0:49666          0.0.0.0:0              LISTENING
  TCP    0.0.0.0:49667          0.0.0.0:0              LISTENING
  TCP    0.0.0.0:49668          0.0.0.0:0              LISTENING
  TCP    127.0.0.1:49667        127.0.0.1:49668        ESTABLISHED
  TCP    127.0.0.1:49668        127.0.0.1:49667        ESTABLISHED
  TCP    192.168.1.100:139      0.0.0.0:0              LISTENING
  TCP    192.168.1.100:5040     192.168.1.50:56708     ESTABLISHED
==================================================
✅ 命令执行完成
```

### 5. 查看系统信息
```
/system_cmd systeminfo
```

**输出示例**:
```
📊 SYSTEMINFO 命令执行结果
==================================================
Host Name:                     DESKTOP-QQFI8LR
OS Name:                       Microsoft Windows 11 专业版
OS Version:                    10.0.26100 N/A Build 26100
OS Manufacturer:               Microsoft Corporation
OS Configuration:              Standalone Workstation
OS Build Type:                 Multiprocessor Free
Registered Owner:              Administrator
Registered Organization:       
Product ID:                    00330-80000-00000-AAOEM
Original Install Date:         2026/3/22, 20:15:32
System Boot Time:              2026/4/8, 8:30:15
System Manufacturer:           VMware, Inc.
System Model:                  VMware Virtual Platform
System Type:                   x64-based PC
Processor(s):                  1 Processor(s) Installed.
                               [01]: Intel64 Family 6 Model 85 Stepping 7 GenuineIntel ~2300 Mhz
BIOS Version:                  VMware, Inc. VMW71.00V.21805430.B64.2405220206, 2024/5/22
Windows Directory:             C:\Windows
System Directory:              C:\Windows\system32
Boot Device:                   \Device\HarddiskVolume1
System Locale:                 zh-cn;Chinese (China)
Input Locale:                  zh-cn;Chinese (China)
Time Zone:                     (UTC+08:00) Beijing, Chongqing, Hong Kong, Urumqi
Total Physical Memory:         8,192 MB
Available Physical Memory:     4,096 MB
Virtual Memory: Max Size:      9,216 MB
Virtual Memory: Available:     5,120 MB
Virtual Memory: In Use:        4,096 MB
Page File Location(s):         C:\pagefile.sys
Domain:                        WORKGROUP
Logon Server:                  \\DESKTOP-QQFI8LR
Hotfix(s):                     3 Hotfix(s) Installed.
                               [01]: KB5044033
                               [02]: KB5044284
                               [03]: KB5044286
Network Card(s):               1 NIC(s) Installed.
                               [01]: Intel(R) Ethernet Connection (7) I219-LM
                                     Connection Name: Ethernet0
                                     DHCP Enabled:    Yes
                                     DHCP Server:     192.168.1.1
                                     IP address(es)
                                     [01]: 192.168.1.100
                                     [02]: fe80::xxxx:xxxx:xxxx:xxxx
Hyper-V Requirements:          A hypervisor has been detected. Features required for Hyper-V will not be displayed.
==================================================
✅ 命令执行完成
```

## 错误处理示例

### 1. 无效命令
```
/system_cmd invalidcmd
```

**输出示例**:
```
❌ 错误: 不支持的命令: invalidcmd
支持的命令: ipconfig, tasklist, netstat, systeminfo

📋 **system_cmd 技能帮助**
...
```

### 2. 命令执行失败
如果命令需要管理员权限或其他原因失败：

**输出示例**:
```
❌ 错误: 执行 systeminfo 时出错: Command failed: powershell -Command "& {chcp 65001 > $null; systeminfo}"
可能需要管理员权限。

📋 **system_cmd 技能帮助**
...
```

## 使用技巧

### 1. 快速诊断网络问题
```
/system_cmd ipconfig
/system_cmd netstat
```
结合使用可以快速查看网络配置和连接状态。

### 2. 系统性能检查
```
/system_cmd tasklist
```
查看哪些进程占用资源较多。

### 3. 系统信息收集
```
/system_cmd systeminfo
```
获取完整的系统配置信息，用于故障排除或记录。

### 4. 批量检查
可以依次执行多个命令进行系统健康检查：
1. `ipconfig` - 检查网络配置
2. `tasklist` - 检查进程状态
3. `netstat` - 检查网络连接
4. `systeminfo` - 检查系统信息

## 注意事项

1. **执行时间**: `systeminfo` 命令可能需要较长时间（5-10秒）
2. **输出大小**: `tasklist` 和 `netstat` 可能输出大量数据
3. **权限要求**: 某些命令可能需要管理员权限才能获取完整信息
4. **编码处理**: 技能已处理中文编码问题，确保输出正常显示