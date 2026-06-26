---
name: rpm
category: packaging
description: "🚨 RPM 打包通用规范。任何涉及 spec 文件编写/修改、rpmbuild、rpmlint、宏展开、依赖管理、构建系统模板（Autotools/CMake/Meson/Python）的场景，都必须读取此技能获取规范，绝不凭训练记忆编写 spec。适用于所有 RPM 发行版。"
version: 4.0.0
metadata: {"openclaw":{"requires":{"skills":[]}}}
---

# RPM 包管理技能 — 你的 RPM 打包规范唯一来源

> ⚠️ **核心规则：**
> 
> **RPM 打包规范非常细致且经常更新。你的训练记忆中的 spec 格式、宏用法、构建指令可能过时或不完整。**
> 
> **因此：任何涉及 RPM 打包的场景，都必须读取此技能获取最新规范。绝不凭记忆编写。**

## 🚨 触发规则 — 遇到以下任何情况，立即读取此技能

| 如果你要做… | 你应该… | 禁止行为 |
|---|---|---|
| 编写/修改 spec 文件 | ✅ 读取此技能 | ❌ 凭记忆写 spec 模板 |
| 检查 spec 文件问题 | ✅ 读取此技能 | ❌ 自己判断格式是否正确 |
| 使用 rpmbuild/mock 构建 | ✅ 读取此技能 | ❌ 凭记忆写构建命令 |
| 处理依赖关系 | ✅ 读取此技能 | ❌ 凭记忆写 Requires/BuildRequires |
| 展开/调试 RPM 宏 | ✅ 读取此技能 | ❌ 凭记忆猜测宏展开结果 |
| 选择构建系统指令 | ✅ 读取此技能 | ❌ 凭记忆写 %build/%install 指令 |
| 运行 rpmlint 检查 | ✅ 读取此技能 | ❌ 自己判断 lint 错误 |
| 包升级/更新版本 | ✅ 读取此技能 | ❌ 凭记忆写升级流程 |
| openEuler 专项打包 | ✅ 同时读取 `openeuler-rpm` | ❌ 只用此技能（openEuler 有特殊规则） |

### 快速自检

当你要编写或修改**任何 spec 文件、执行 RPM 构建命令、处理 RPM 依赖**时，问自己：

> "我确定这个 spec 格式/宏/构建指令是正确的吗？还是我在凭记忆猜？"

如果不确定 → **读取此技能**。如果是 openEuler 打包 → **同时读取 `openeuler-rpm`**。

---

## 📋 核心功能

### 1. Spec 文件分析与优化
- ✅ 自动检测 spec 文件问题
- ✅ 提供优化建议
- ✅ 符合官方打包指南
- ✅ RPMLint 集成

### 2. 多构建系统支持
| 构建系统 | Prep | Build | Install |
|---------|------|-------|---------|
| Autotools | `%autosetup -p1` | `%configure` | `%make_install` |
| CMake | `%autosetup -p1` | `%cmake` | `%cmake_install` |
| Meson | `%autosetup -p1` | `%meson` | `%ninja_install` |
| Python | `%autosetup -p1 -n %{name}-%{version}` | `%pyproject_build_wheel` | `%pyproject_make_binary` |
| Node.js | `%autosetup -p1 -n package` | `npm install` |手动安装|

### 3. 自动化构建
- 本地构建 | `rpmbuild -ba`
- Mock 构建 | `mock --rebuild`
- OBS 构建 | `osc build`

### 4. 包验证与测试
- RPMLint 集成
- 签名验证
- 文件完整性检查
- 运行时测试

### 5. 依赖管理
- 自动依赖生成
- 依赖解析
- 依赖冲突检测
- 反向依赖查询

### 6. 宏系统深入理解
- 宏定义与展开
- 宏调试
- 宏文档查询

---

## 📝 Spec 文件标准结构

```spec
Name:           mypackage
Version:        1.0.0
Release:        0%{?dist}
Summary:        Package summary

License:        MIT
URL:            https://example.com
Source0:        https://github.com/%{url}/releases/download/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
Requires:       glibc >= 2.17

%description
Detailed package description.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%check
make test

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}

%changelog
* Thu Apr 16 2026 Your Name <your@email.com> - 1.0.0-1
- Update to 1.0.0
- Fix build issues
```

---

## 🔧 常用命令

### RPM 查询
```bash
rpm -qa                    # 所有已安装包
rpm -qi package           # 包信息
rpm -ql package           # 文件列表
rpm -qR package           # 依赖
rpm -qf /path/to/file     # 文件归属
```

### 构建命令
```bash
rpmbuild -ba spec         # 构建 SRPM+RPM
rpmbuild -bs spec         # 仅构建 SRPM
rpmbuild -bb spec         # 仅构建 RPM
mock -r fedora-39-x86_64 --rebuild src.rpm
osc build                 # OBS 构建
```

### 验证命令
```bash
rpmlint spec              # 检查 spec 文件
rpmlint rpm               # 检查 RPM
rpm -V package            # 验证包
rpm -Va                   # 验证所有包
```

### 宏管理
```bash
rpm --showrc              # 查看所有宏
rpm --eval '%{name}'      # 展开宏
rpmspec -E spec           # 检查 spec 宏
```

---

## 🎯 工作流

### 新包构建流程
```
1. 创建 spec → rpmdev-newspec -o mypackage.spec
2. 编辑 spec → 填写元数据、依赖、构建指令
3. 本地构建 → rpmbuild -ba mypackage.spec
4. 质量检查 → rpmlint mypackage.spec
5. 修正问题 → 根据 RPMLint 报告修改
6. Mock 构建 → mock --rebuild src.rpm (可选)
7. OBS 构建 → osc build (如需要)
```

### 升级现有包流程
```
1. 检查新版本 → curl -s https://example.com/releases | grep mypackage
2. 更新 Source0 → %update_source_url mypackage.spec
3. 更新 Version → sed -i "s/^Version:.*/Version:/new/" mypackage.spec
4. 更新 Release → Release: 1%{?dist}
5. 更新 changelog → 添加新条目
6. 重建构建 → rpmbuild -ba mypackage.spec
7. 验证功能 → rpm -e && rpm -ivh package.rpm
```

---

## 🔍 RPMLint 常见错误

| 错误 | 说明 | 修复方法 |
|------|------|----------|
| `invalid-license` | License 不在标准列表 | 参考 SPDX License List |
| `no-description` | 缺少 %description | 添加描述 |
| `spurious-executable-permission` | 文件有执行权限但不是脚本 | 移除执行位或添加 `%{_bindir}` |
| `summary-not-capitalized` | Summary 首字母未大写 | 大写首字母 |
| `wrong-file-end-of-line-encoding` | 文件编码问题 | 用 UTF-8 保存 |

---

## 🏗️ 构建系统模板

### Autotools
```spec
BuildRequires: autoconf automake libtool
%prep: %autosetup -p1
%build: %configure && %make_build
%install: %make_install
```

### CMake
```spec
BuildRequires: cmake
%prep: %autosetup -p1
%build: %cmake && %cmake_build
%install: %cmake_install
```

### Meson
```spec
BuildRequires: meson ninja-build
%prep: %autosetup -p1
%build: %meson && %ninja_build
%install: %ninja_install
```

### Python
```spec
BuildRequires: python3-devel python3-setuptools
%prep: %autosetup -p1 -n %{name}-%{version}
%build: %pyproject_build_wheel && %pyproject_install
%install: %pyproject_make_binary
```

### Node.js
```spec
BuildRequires: nodejs npm
%prep: %autosetup -p1 -n package
%build: npm install --production=false && npm run build
%install: mkdir -p %{buildroot}%{_datadir}/%{name} && cp -r . %{buildroot}%{_datadir}/%{name}/
```

---

## 🔄 宏参考

| 宏 | 路径 |
|---|------|
| `%{_bindir}` | /usr/bin |
| `%{_libdir}` | /usr/lib[64] |
| `%{_datadir}` | /usr/share |
| `%{_sysconfdir}` | /etc |
| `%{_docdir}` | /usr/share/doc |
| `%{_mandir}` | /usr/share/man |
| `%{_topdir}` | ~/rpmbuild |

---

## 📋 最佳实践

### Spec 文件编写
- ✅ 使用 `%autosetup` 而非手动 `%setup`
- ✅ 使用 `%{_bindir}` 等标准宏
- ✅ 提供详细的 changelog 条目
- ✅ 优先使用标准构建系统宏
- ✅ 运行 `rpmlint` 检查

### 构建优化
- ✅ 使用并行构建 `make %{?_smp_mflags}`
- ✅ 使用 mock 或 OBS 进行干净构建
- ✅ 明确声明所有依赖
- ✅ 使用 `%{?dist}` 区分发行版
- ✅ 避免 `AutoReq: no`

### 质量控制
- ✅ 运行 `rpmlint` 检查 spec
- ✅ 验证签名和校验和
- ✅ 测试安装/卸载
- ✅ 检查依赖完整性
- ✅ 验证文件权限

---

## 📋 依赖技能

本技能可与以下技能配合使用：

| 技能 | 用途 |
|------|------|
| `openeuler-rpm` | openEuler 专项打包规范 |
| `koji` | Koji 构建系统集成 |

---

_版本: 4.0.0 | 作者: OS Build Agent_
