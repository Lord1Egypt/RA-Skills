# UOS/deepin 应用打包规范

UOS/deepin 应用基于统信打包规范，使用 deb 格式，所有应用文件必须安装到 `/opt/apps/${appid}/` 目录下。

## 核心规则

### 1. 应用标识（appid）

必须使用**倒置域名**规则，支持小写字母和点号。**包名（Package）必须与 appid 完全一致，且仅支持小写字母。**

```
org.deepin.browser
cn.i4.i4tools
com.example.myapp
```

### 2. 目录结构（重要）

```
${appid}/                          ← 直接作为打包根目录，不要有 data/opt 前缀
├── DEBIAN/                        # 打包根目录下的 DEBIAN/（不是 data/DEBIAN/）
│   ├── control
│   ├── postinst
│   ├── prerm
│   ├── postrm
│   ├── preinst
│   └── copyright                  # 版权文件不动
├── opt/apps/${appid}/             ← 打包根目录下创建 opt/，不是 data/opt/
│   ├── entries/                  # 资源映射到系统目录（DDE 自动处理）
│   │   ├── applications/        # desktop → /usr/share/applications/
│   │   │   └── ${appid}.desktop
│   │   ├── icons/                # 图标 → /usr/share/icons/
│   │   │   └── hicolor/scalable/apps/${appid}.svg
│   │   └── ...
│   ├── files/                    # 应用主体文件（原包内容放这里）
│   │   ├── bin/
│   │   ├── lib/
│   │   ├── run.sh
│   │   └── resources/
│   └── info                      # 应用描述文件（JSON，DDE 解析后自动配置映射）
```

**⚠️ 关键教训：**
- `dpkg-deb` 打包时，`DEBIAN/` 和 `opt/` 必须**直接位于打包根目录**，不能套一层 `data/` 再放 opt
- 正确：`./opt/apps/${appid}/...`；错误：`./data/opt/apps/${appid}/...`（会导致文件装到 `/data/opt/...`）
- 打包命令在 repack 目录的**父目录**执行：`dpkg-deb --build ${repack_dir} ${output}.deb`

### 3. info 文件（必需）

info 文件是 UOS 打包的**核心文件**，由 DDE 桌面环境解析后**自动配置** entries 到系统目录的映射（无需手动写 postinst 创建 symlink）。

路径：`opt/apps/${appid}/info`

```json
{
    "appid": "cn.i4.i4tools",
    "name": "i4Tools",
    "version": "3.09.002",
    "arch": ["amd64"],
    "permissions": {
        "autostart": false,
        "notification": true,
        "trayicon": true,
        "clipboard": true,
        "account": false,
        "bluetooth": false,
        "camera": false,
        "audio_record": false,
        "installed_apps": false
    },
    "support-plugins": [],
    "plugins": []
}
```

**字段说明：**

| 字段 | 说明 | 要求 |
|------|------|------|
| appid | 应用唯一标识 | 必填，必须与包名一致 |
| name | 应用默认名称 | 必填 |
| version | 版本号 | 必填，格式 `{MAJOR}.{MINOR}.{PATCH}`，纯数字 |
| arch | 支持的架构 | 必填，支持：amd64, arm64, loongarch64, mips64el, sw_64 |
| permissions | 沙箱权限 | 布尔值，默认 false |
| support-plugins | 支持的插件类型 | 可选 |
| plugins | 实现的插件类型 | 可选 |

### 4. Desktop Entry 文件

路径：`opt/apps/${appid}/entries/applications/${appid}.desktop`
编码：**必须 UTF-8**（其他编码会导致中文乱码）

```ini
[Desktop Entry]
Version=3.09.002
Type=Application
Name=i4Tools
Name[zh_CN]=爱思助手
Comment=苹果设备管理工具
Comment[zh_CN]=苹果设备管理工具
GenericName=i4Tools
GenericName[zh_CN]=爱思助手
Exec=/opt/apps/cn.i4.i4tools/files/run.sh
Icon=/opt/apps/cn.i4.i4tools/files/resources/logo.png
Terminal=false
Categories=utils
Keywords=i4Tools;i4
StartupNotify=true
```

**必填字段：** `[Desktop Entry]`、`Name`、`Exec`、`Icon`、`Type`、`Terminal`、`StartupNotify`

**Icon 路径注意：** 如果图标在 entries/ 下但 logo 资源在 files/ 下，应使用 `files/resources/logo.png` 的绝对路径，或将图标文件放入 `files/resources/` 后在 desktop 中引用。

**Categories 可选值：**

| 值 | 启动器分类 |
|---|-----------|
| Network | 网络应用 |
| Chat | 社交沟通 |
| Audio | 音乐欣赏 |
| AudioVideo | 视频播放 |
| Graphics | 图形图像 |
| Game | 游戏娱乐 |
| Office | 办公学习 |
| Reading | 阅读翻译 |
| Development | 编程开发 |
| System | 系统管理 |
| utils | 工具类（未在上表时归为"其他应用"） |

### 5. 图标

矢量格式（推荐 SVG）：
```
opt/apps/${appid}/entries/icons/hicolor/scalable/apps/${appid}.svg
```

非矢量格式（PNG，分辨率 16/24/32/48/128/256/512）：
```
opt/apps/${appid}/entries/icons/hicolor/24x24/apps/${appid}.png
opt/apps/${appid}/entries/icons/hicolor/48x48/apps/${appid}.png
opt/apps/${appid}/entries/icons/hicolor/128x128/apps/${appid}.png
```

### 6. 文件系统权限

- **系统目录**：只读，不依赖其内容
- **应用数据目录**：使用 XDG 环境变量

| 环境变量 | 路径 |
|----------|------|
| `$XDG_DATA_HOME` | `~/.local/share` |
| `$XDG_CONFIG_HOME` | `~/.config` |
| `$XDG_CACHE_HOME` | `~/.cache` |

应用数据路径：`$XDG_DATA_HOME/${appid}`（例：`~/.local/share/org.deepin.browser`）

**禁止直接写入 `$HOME`！**

### 7. DEBIAN 钩子脚本规范

#### 7.1 版权/归属信息不动

以下内容属于版权/归属信息，**不要修改**：
- `DEBIAN/copyright` 文件
- `DEBIAN/control` 中的 `Maintainer` 字段
- 原包自带的业务逻辑（如 udev 规则内容）

#### 7.2 可以修改的部分

- `DEBIAN/control` 中的 `Package`（包名，需与 appid 一致）
- `DEBIAN/control` 中的 `Breaks`/`Replaces`（防冲突）
- 所有维护脚本的功能逻辑（修复 bug、适配 UOS 环境）
- desktop 文件、info 文件的内容

#### 7.3 rm -rf 命令规范

```bash
# ✅ 正确（带引号）
rm -rf "$INSTALL_DIR/tmp"

# ❌ 错误（未引用变量，重定向不受 sudo 影响）
sudo echo xxx > /lib/udev/rules.d/xxx  # 重定向不在 sudo 作用域
# 正确做法：
printf '%s\n' "content" | sudo tee /lib/udev/rules.d/xxx > /dev/null
```

#### 7.4 sudo 与重定向

在脚本中，`sudo` **不影响重定向**（`>`、`>>`）。如果需要 sudo 写入文件，使用 `tee`：

```bash
# 错误
sudo echo "rule" > /path/file

# 正确
printf '%s\n' "rule" | sudo tee /path/file > /dev/null
```

#### 7.5 UOS 无 sudo 环境适配

UOS/统信环境下，普通用户可以直接写入 `/lib/udev/rules.d/` 等目录。可以通过 `/etc/os-release` 检测：

```bash
if [ -f /etc/os-release ]; then
    . /etc/os-release
    case "$ID" in
        uos|uniontech|deepin)
            # UOS：直接写入，无需 sudo
            printf '%s\n' "$CONTENT" > /path/file
            ;;
        *)
            # 其他系统：使用 sudo
            printf '%s\n' "$CONTENT" | sudo tee /path/file > /dev/null
            ;;
    esac
fi
```

#### 7.6 shellcheck 检查

```bash
sudo apt install shellcheck
shellcheck DEBIAN/postinst DEBIAN/prerm DEBIAN/postrm DEBIAN/preinst
```

## 完整打包流程

### Step 1：分析原始 deb 包

```bash
dpkg-deb -I original.deb          # 查看包信息
dpkg-deb -x original.deb /tmp/orig/  # 解压数据
dpkg-deb -e original.deb /tmp/orig/DEBIAN  # 解压控制信息
```

### Step 2：建立 UOS 规范目录结构

```bash
APPID="cn.i4.i4tools"
mkdir -p ${APPID}/opt/apps/${APPID}/{entries/applications,entries/icons/hicolor/scalable/apps,files}
```

### Step 3：迁移文件

- **应用主体（原包 opt/ 下的内容）** → `opt/apps/${APPID}/files/`
- **desktop 文件** → `opt/apps/${APPID}/entries/applications/${APPID}.desktop`
- **图标** → `opt/apps/${APPID}/entries/icons/hicolor/scalable/apps/${APPID}.svg`
- **创建 info 文件** → `opt/apps/${APPID}/info`

### Step 4：更新 desktop 文件

- `Exec` 路径改为 `files/` 下的实际路径
- `Icon` 路径指向 `files/resources/` 下的图标
- 确认 `StartupNotify=true`
- 确保编码为 UTF-8

### Step 5：编写/更新 DEBIAN 脚本

- `preinst`：安装前清理旧目录（如有）、写入 udev 规则（用 tee 不用 echo+重定向）
- `postinst`：写入 udev 规则（UOS 检测）、触发 udev reload
- `prerm`：移除 desktop 链接（如有）
- `postrm`：卸载后清理 udev 规则
- **不要删除或修改 copyright 文件**

### Step 6：写 control 文件

```
Package: ${APPID}
Version: x.x.x
Section: utils
Priority: optional
Architecture: amd64
Maintainer: <保持原样，不动>
Breaks: ${APPID}
Replaces: ${APPID}
Description: 应用描述
```

### Step 7：打包

```bash
# 在 repack 目录的**父目录**执行
# 目录结构应为：
#   repack/
#   ├── DEBIAN/
#   ├── opt/
#   └── usr/ （如需要）
# 不要有 data/ 前缀

dpkg-deb --build repack/ output_${VERSION}_amd64.deb
```

### Step 8：验证

```bash
dpkg-deb -I output.deb                      # 检查 control
dpkg-deb -c output.deb | head -30           # 检查归档路径（应为 ./opt/...，不是 ./data/opt/...）
sudo dpkg -i output.deb                      # 安装测试
dpkg -L ${APPID} | grep -E "(entries|info)"  # 检查文件列表
ls /opt/apps/${APPID}/                       # 确认目录存在
ls /usr/share/applications/ | grep ${APPID}  # 确认 desktop 软链接
ls /usr/share/icons/.../${APPID}.svg         # 确认 icon 软链接
cat /lib/udev/rules.d/38-${APPID}.rules      # 确认 udev 规则
shellcheck DEBIAN/postinst DEBIAN/prerm DEBIAN/postrm DEBIAN/preinst
```

## 支持的 CPU 架构

| 架构 | CPU 系列 |
|------|---------|
| amd64 | x86: 海光、兆芯、Intel、AMD |
| arm64 | ARM64: 飞腾、鲲鹏、海思麒麟、瑞芯微 |
| loongarch64 | 龙芯 3A5000/3B5000+ |
| mips64el | 龙芯 3A4000/3A3000 及更早 |
| sw_64 | 申威 CPU |

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| 文件装到 `/data/opt/...` | 打包根目录内嵌套了 `data/` 层 | 打包时 `DEBIAN/` 和 `opt/` 直接在 repack 根目录下 |
| 快捷方式不显示 | Exec 路径无效 / desktop 编码非 UTF-8 | 检查路径；保存为 UTF-8；确认 StartupNotify=true |
| 图标不显示 | Icon 路径错误 | 使用 `files/resources/logo.png` 或确认 entries 下图标路径 |
| DDE 未自动映射 entries | 缺少 info 文件 | 必须有 `opt/apps/${appid}/info` 文件 |
| udev 规则无效 | sudo echo 重定向不生效 | 使用 `tee` 而非 `echo + 重定向` |
| info 文件无效 | JSON 格式错误 | 严格 JSON 格式，注意字段名拼写 |
| 中文乱码 | desktop 文件非 UTF-8 编码 | 保存为 UTF-8 编码 |
| shellcheck 报错 | 脚本语法问题 | SC2024（sudo 重定向）、SC2129（多次重定向） |
| 维护脚本执行失败 | 权限不够 / 路径问题 | UOS 下 `/etc/os-release` 检测判断是否需要 sudo |
