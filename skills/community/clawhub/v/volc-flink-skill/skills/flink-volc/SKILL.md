---
name: flink-volc
description: 火山引擎 Flink 版 (volc_flink) CLI 工具环境管理技能，用于安装、升级、诊断与修复本地 `volc_flink`（含虚拟环境/依赖/路径/版本检查）。不负责登录/退出/登录状态检查与账号切换（由 `flink-auth` 负责），也不负责默认项目/TOS 路径等配置项设置（由 `flink-config` 负责）。Use this skill when the user needs CLI/tooling environment work for `volc_flink` (install/upgrade/diagnose/fix local setup). Do NOT use it for login status/login/logout/account switching (use `flink-auth`) or config items like default project/TOS prefix (use `flink-config`). Always trigger only when the request contains a CLI/tooling intent + a concrete tool action/object.
required_binaries:
  - volc_flink
may_access_config_paths:
  - ~/.volc_flink
  - $VOLC_FLINK_CONFIG_DIR
credentials:
  primary: volc_flink_local_config
  optional_env_vars:
    - VOLCENGINE_ACCESS_KEY
    - VOLCENGINE_SECRET_KEY
    - VOLCENGINE_REGION
---

# 火山引擎 Flink 版 (volc_flink) 工具管理技能

用于安装、更新、升级与修复 `volc_flink` 命令行工具环境，这是所有 Flink 相关操作的基础。

安装策略默认优先级：

1. `pipx` 安装独立 CLI 环境
2. Python 虚拟环境（`venv`）
3. 仅在用户明确接受风险且环境允许时，才讨论直接 `pip install`

认证与账号相关（登录/退出/登录状态检查/账号切换）请使用 `flink-auth`。
默认项目、TOS 路径等配置项设置请使用 `flink-config`。

---

## 通用约定（必读）

本技能的基础约定与安全约定统一收敛在：

- `../../COMMON.md`
- `../../COMMON_SECURITY.md`

本技能涉及登录、本地配置目录、账号与工具链初始化等安全敏感操作，必须遵循 `COMMON_SECURITY.md` 中的秘密输入、脱敏展示和安全输出规则。

---

## 🎯 核心功能

### 1. 工具安装与更新

#### 1.1 检测 volc_flink 是否已安装
**在执行任何操作前，先检测 volc_flink 是否已安装！**

**检测步骤**：
```bash
# 检查 volc_flink 是否在 PATH 中
which volc_flink

# 或者检查版本
volc_flink --version
```

**如果未安装，提供安装指引**：

#### 1.2 安装 volc_flink
根据用户的操作系统，提供相应的安装指引。

**Linux / macOS 安装（推荐优先使用 `pipx`）**：

⚠️ **重要说明**：

- 在 root / system Python / externally-managed Python 环境下，直接执行 `pip install` 可能被禁止或不被允许
- 这种场景下，不要优先要求用户创建虚拟环境再手动激活，优先使用 `pipx`
- `volc-flink-cli` 已提供标准 console script：安装后可直接得到 `volc_flink` 命令

**方式 1：使用 pipx 从 PyPI 安装（首选）**：
```bash
# 如果系统未安装 pipx，优先使用操作系统包管理器安装
# macOS (Homebrew)
brew install pipx
pipx ensurepath

# Ubuntu / Debian
sudo apt install -y pipx
pipx ensurepath

# Fedora
sudo dnf install -y pipx
pipx ensurepath

# 使用清华镜像安装 volc-flink-cli
pipx install volc-flink-cli --pip-args="--index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"

# 验证安装
volc_flink --version
```

**方式 2：使用 Python 虚拟环境安装（备选）**：

⚠️ **重要提示**：推荐使用国内镜像源以获得更快的下载速度！

**使用清华镜像源安装（推荐，速度快）**：
```bash
# 创建 Python 虚拟环境
python3 -m venv ~/flink-env

# 激活虚拟环境
source ~/flink-env/bin/activate

# 先更新基础工具
pip install --upgrade pip setuptools wheel -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 使用清华镜像源安装 volc-flink-cli
pip install volc-flink-cli -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 验证安装
volc_flink --version
```

**使用官方 PyPI 源安装**：
```bash
# 创建 Python 虚拟环境
python3 -m venv ~/flink-env

# 激活虚拟环境
source ~/flink-env/bin/activate

# 先更新基础工具
pip install --upgrade pip setuptools wheel

# 使用官方 PyPI 源安装（速度较慢，可能超时）
pip install volc-flink-cli -i https://pypi.org/simple/

# 验证安装
volc_flink --version
```

**其他可用的国内镜像源**：
- 阿里云：`https://mirrors.aliyun.com/pypi/simple/`
- 中科大：`https://pypi.mirrors.ustc.edu.cn/simple/`
- 豆瓣：`https://pypi.douban.com/simple/`

**Windows 安装（优先使用 `pipx`）**：
```bash
# 安装 pipx（如果未安装）
py -m pip install --user pipx
py -m pipx ensurepath

# 安装 volc-flink-cli
pipx install volc-flink-cli --pip-args="--index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"

# 验证安装
volc_flink --version
```

**Windows 虚拟环境安装（备选）**：
```bash
# 创建 Python 虚拟环境
python -m venv %USERPROFILE%\flink-env

# 激活虚拟环境
%USERPROFILE%\flink-env\Scripts\activate

# 安装 volc-flink-cli
pip install volc-flink-cli -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 验证安装
volc_flink --version
```

**升级到最新版本**：
```bash
# pipx 安装用户（推荐）
pipx upgrade volc-flink-cli

# 如果你确实使用的是 venv
source ~/flink-env/bin/activate
pip install --upgrade volc-flink-cli -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

#### 1.3 查看版本信息
```bash
# 查看 volc_flink 版本
volc_flink --version

# 查看详细帮助
volc_flink --help
```

---

### 2. 认证与账号（由 flink-auth 负责）

本技能不负责登录/退出/登录状态检查与账号切换。
当用户的意图是“认证/账号”而不是“工具安装/修复”，应转交给 `flink-auth`。

常见转交场景：
- “我现在登录了吗 / 登录状态是什么”
- “帮我登录 / 退出登录 / 切换账号”
- “登录失败/过期，怎么处理”

在 `flink-auth` 中会优先使用：

```bash
volc_flink login status
```

---

### 3. 配置项设置（由 flink-config 负责）

本技能不负责默认项目、TOS Jar 存储路径等配置项设置。

当用户的意图是“设置/修改配置项”，应转交给 `flink-config`：
- 默认项目：`volc_flink config set-default-project ...`
- TOS Jar 存储路径：`volc_flink config set-tos-jar-prefix ...`

本技能仅在配置相关问题属于“工具环境不可用/版本不匹配/命令不存在”时介入排障。

### 4. 快速入门指引

#### 4.1 完整的首次使用流程（推荐）

**步骤 1：安装 volc_flink（优先 pipx，使用清华镜像源）**
```bash
# 优先安装 pipx
brew install pipx  # macOS
# 或 sudo apt install -y pipx  # Ubuntu / Debian
# 或 sudo dnf install -y pipx  # Fedora

pipx ensurepath
pipx install volc-flink-cli --pip-args="--index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"

# 验证安装
volc_flink --version
```

**步骤 2：认证与登录（转交 flink-auth）**
- `flink-auth` 会优先使用 `volc_flink login status` 检查登录状态

**步骤 3：配置默认项目/TOS 前缀（转交 flink-config）**
- 配置项设置属于 `flink-config` 的职责范围

**步骤 4：开始使用其他 Flink 技能**
- 使用 `flink-catalog` 浏览元数据
- 使用 `flink-sql` 开发 SQL 任务
- 使用 `flink-sre` 进行运维操作

---

#### 4.2 日常使用提示

**如果你使用的是 pipx，日常使用不需要激活虚拟环境**：
```bash
volc_flink --version
```

**只有在你明确使用 venv 安装时，才需要先激活虚拟环境**：
```bash
source ~/flink-env/bin/activate
```

**如果 pipx 环境损坏，可直接重装**：
```bash
pipx reinstall volc-flink-cli
```

**如果虚拟环境损坏，重新创建（仅 venv 安装用户）**：
```bash
# 删除旧的虚拟环境
rm -rf ~/flink-env

# 重新创建并安装
python3 -m venv ~/flink-env
source ~/flink-env/bin/activate
pip install --upgrade pip setuptools wheel -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
pip install volc-flink-cli -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

---

### 5. 多账号管理（高级功能）

虽然 volc_flink 原生不支持多账号切换，但可以通过以下方式实现：

#### 5.1 使用不同的配置目录
```bash
# 为账号 A 设置配置目录
export VOLC_FLINK_CONFIG_DIR=~/.volc_flink/account_a
volc_flink login  # 交互式登录（推荐）

# 为账号 B 设置配置目录
export VOLC_FLINK_CONFIG_DIR=~/.volc_flink/account_b
volc_flink login  # 交互式登录（推荐）

# 切换到账号 A
export VOLC_FLINK_CONFIG_DIR=~/.volc_flink/account_a
```

#### 5.2 使用配置文件备份
```bash
# 不推荐通过拷贝配置文件进行“账号切换”，因为配置目录通常包含凭据信息，复制/覆盖容易误操作与泄露。
# 推荐用 VOLC_FLINK_CONFIG_DIR 为不同账号隔离配置目录（见 5.1）。
:
```

---

## 工具调用顺序

### 首次使用完整流程
1. **检测安装状态** - 检查 volc_flink 是否已安装
2. **安装工具**（如需要）- 提供安装指引
3. **认证与登录** - 转交 `flink-auth`（`volc_flink login status` / `volc_flink login`）
4. **配置默认项目/TOS 前缀** - 转交 `flink-config`
5. **指引用户使用其他技能**

### 日常使用流程
1. **检测工具可用性** - `volc_flink --version`
2. **如需认证/账号操作** - 转交给 `flink-auth`（例如 `volc_flink login status`）
3. **执行具体操作**（调用其他子技能）

### 更新工具流程
1. **检查当前版本** - `volc_flink --version`
2. **识别安装方式** - 优先判断是 `pipx` 还是 `venv`
3. **执行升级** - `pipx upgrade volc-flink-cli` 或在 venv 中 `pip install --upgrade volc-flink-cli`
4. **验证新版本** - `volc_flink --version`

---

## 常用 volc_flink 命令速查

### 工具管理
```bash
# 查看版本
volc_flink --version

# 查看帮助
volc_flink --help

# 安装（首选 pipx）
pipx install volc-flink-cli --pip-args="--index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"

# 升级（pipx）
pipx upgrade volc-flink-cli

# 备选：venv 安装/升级
python3 -m venv ~/flink-env
source ~/flink-env/bin/activate
pip install --upgrade pip setuptools wheel -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
pip install volc-flink-cli -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
pip install --upgrade volc-flink-cli -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

### 登录与认证
```bash
# 登录/退出/登录状态检查/账号切换：请使用 flink-auth
# 例如：
volc_flink login status
```

### 配置管理
配置项查看与设置：请使用 `flink-config`。

### 项目管理
```bash
# 列举项目
volc_flink projects list

# 查看项目详情
volc_flink projects detail <项目名>
```

---

## 输出格式

### 安装检测反馈
```
# 🔧 volc_flink 工具检测

## 📋 检测结果
- **安装状态**: [已安装 / 未安装]
- **版本**: [版本号 / 未知]

## 💡 下一步
[如果已安装：建议用 flink-auth 检查登录状态（volc_flink login status）]
[如果未安装：提供安装指引]
```

### 工具就绪反馈
```
# ✅ volc_flink 工具已就绪

## 💡 下一步
1. 认证与登录：使用 `flink-auth`（优先 `volc_flink login status`）
2. 默认项目与 TOS 前缀配置：使用 `flink-config`
```

### 配置项转交提示
```
# ⚙️ 配置项设置提示

## 💡 可用操作
- 设置默认项目 / TOS Jar 前缀：请使用 `flink-config`
- 登录状态检查 / 登录 / 退出 / 账号切换：请使用 `flink-auth`
```

---

## 错误处理

### 常见错误及处理

#### 错误 1：volc_flink 未安装
**错误信息**：`command not found: volc_flink`

**处理方式**：
- 友好提示："检测到 volc_flink 未安装"
- 提供安装指引：推荐使用清华镜像源安装
- 等待用户安装后重试

#### 错误 2：下载超时或速度慢
**错误信息**：`Connection timed out while downloading` 或下载速度极慢

**处理方式**：
- 提示："网络下载超时或速度过慢"
- 建议：使用国内镜像源（推荐清华镜像源）
- 提供镜像源安装命令

#### 错误 3：缺少构建依赖
**错误信息**：`Could not find a version that satisfies the requirement setuptools>=40.8.0`

**处理方式**：
- 提示："缺少构建依赖工具"
- 先安装基础工具：`pip install --upgrade pip setuptools wheel`
- 然后再安装 volc-flink-cli

#### 错误 4：tos 包构建失败
**错误信息**：`Failed to build 'tos' when installing build dependencies for tos`

**处理方式**：
- 提示："tos 包构建失败"
- 确保已安装 setuptools 和 wheel
- 使用国内镜像源重新安装

#### 错误 5：认证相关错误
当错误与登录状态/权限相关（例如“请先登录”“权限不足”），请转交给 `flink-auth` 处理。

#### 错误 7：虚拟环境问题
**错误信息**：`/root/flink-env/bin/activate: No such file or directory`

**处理方式**：
- 提示："虚拟环境不存在或已损坏"
- 重新创建虚拟环境：`python3 -m venv ~/flink-env`
- 然后重新激活并安装

#### 错误 8：root / system Python 不允许直接 pip install
**错误信息**：`externally-managed-environment` / `This environment is externally managed`

**处理方式**：
- 提示："当前 Python 环境不允许直接 pip install"
- 优先改用 `pipx install volc-flink-cli`
- 如果系统没有 pipx，优先使用操作系统包管理器安装 pipx
- 仅在用户明确要求时，再讨论 `venv` 方案

---

## 注意事项

### 重要：安全提示

⚠️ **关于 AK/SK 的安全**：
1. **不要在聊天中直接粘贴 AK/SK** - 建议使用交互式登录
2. **妥善保管 AK/SK** - 不要泄露给他人
3. **定期轮换 AK/SK** - 提高安全性
4. **使用最小权限原则** - 为 AK/SK 分配最小必要权限

### 通用注意事项

1. **先检测安装状态**：在执行任何操作前，先检测 volc_flink 是否已安装
2. **认证与配置分工**：登录相关请转交 `flink-auth`，默认项目/TOS 前缀请转交 `flink-config`
3. **安装优先级**：默认优先 `pipx`，其次 `venv`，不要先假设用户必须激活虚拟环境
4. **引导用户使用子技能**：这个技能是入口，具体操作引导用户使用对应的子技能
5. **提供清晰的指引**：用用户能理解的语言解释操作步骤
6. **友好的错误处理**：如果操作失败，向用户说明失败原因，并提供解决方案

---

## 🎯 技能总结

### 核心功能
1. ✅ **工具安装与更新** - 安装、升级 volc_flink 工具
2. ✅ **工具自检与修复** - 版本/依赖/虚拟环境/路径问题定位
3. ✅ **快速入门指引** - 完整的首次使用流程（并明确转交 auth/config）

### 与其他技能的关系
- **工具环境基础** - 所有其他 Flink 技能都依赖 `volc_flink` 可用
- **认证分工** - 登录状态/登录/退出/账号切换由 `flink-auth` 负责
- **引导用户** - 本技能负责把“工具环境问题”与“认证问题”分流到正确技能

这个技能是整个 Flink 技能插件的入口和基础！
