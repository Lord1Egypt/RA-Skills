# 元链 yotta-chain — 检测规则参考

> 每条规则的触发逻辑、严重度与修复指引。用于人工复核与教学。

## 严重度

`info < low < medium < high`。`scan` 默认 `--gate=info`（任何发现即退出 1），CI 可 `--gate high` 收紧。

## 一、依赖混淆（dependency confusion）

依赖混淆：攻击者把「只应存在于私有仓库的包名」发布到公共仓库（npm / PyPI），利用解析优先级让受害者装到恶意包。本引擎**纯本地**用「仓库配置 vs 实际解析来源」给强信号。

### confusion_scope_registry（high）

- 触发：`.npmrc` 为某 scope 配置了私有仓库（`@scope:registry=...`），但 package-lock.json 里该 scope 的包 `resolved` 指向其它（公共）仓库主机。
- 含义：私有包名本应从私有仓库解析，实际却可能被公共仓库的同名攻击者包抢占。
- 示例：

  ```
  # .npmrc
  @corp:registry=https://npm.corp.example.com/
  # package-lock.json
  "node_modules/@corp/secret": { "resolved": "https://registry.npmjs.org/@corp/secret.tgz" }
  ```

- 修复：核对 resolved 是否应指向私有仓库；用正确的私有仓库重新 `npm install` 并检查锁文件 resolved 主机；把 `.npmrc` 提交入库（或用 CI 注入）。

### confusion_mixed_registry（high）

- 触发：同一包名在锁文件里被解析自多个不同仓库主机（如顶层来自公共 registry，嵌套来自公司镜像）。
- 含义：同一依赖来源不一致，可能是镜像污染或被替换。
- 修复：统一到单一可信仓库；删除不一致条目后重新安装。

### confusion_suspicious_registry（medium）

- 触发：仓库 / 索引地址为 `http://`（非 TLS）、IP 字面量（如 `http://192.168.1.5/...`）、本机地址（localhost / 127.0.0.1）。
- 含义：非 HTTPS 或指向内网 / 本机的仓库可被中间人篡改，或指向开发环境残留。
- 修复：改用 HTTPS 域名仓库；删除开发期残留地址。

### confusion_extra_index（medium）

- 触发：pip 同时配置 `--index-url`（私有）与 `--extra-index-url`（公共，如 PyPI）；或 poetry 源标记 `secondary = true`；或 Pipfile 同时列出公共 PyPI 与私有源。
- 含义：公共仓库成为回退源——私有包名只要在公共仓库出现同名包，就可能被抢占（依赖混淆经典场景）。
- 修复：只保留单一可信源；私有包确保只在私有源解析；poetry 把私有源设为 `default` 并关闭 PyPI 回退；pip 用 `--index-url` 单一私有源 + 显式 `--extra-index-url` 白名单。

### confusion_registry_mismatch（medium）

- 触发：项目配置了私有默认仓库（`.npmrc registry=` 或 package.json publishConfig），但锁文件里包从公共仓库（registry.npmjs.org）解析。
- 含义：配置与锁定来源不一致，私有包名可能从公共仓库被抢占。
- 修复：核对默认仓库配置与锁文件生成时机；重新安装生成锁文件。

## 二、lockfile 一致性

### lockfile_missing_entry（high）

- 触发：清单（package.json / pyproject.toml / Pipfile）声明了依赖，锁文件里却没有。
- 修复：`npm install` / `poetry lock` / `pipenv lock` 重新生成锁文件；若锁文件被手工删条目需还原。

### lockfile_range_unsatisfied（high）

- 触发：锁文件版本不满足清单声明的版本范围（npm semver / PEP 440 语义）。
- 示例：`"lodash": "^5.0.0"` 但锁文件锁定 `4.17.21`。
- 修复：声明与锁定必须一致；升级或回退后重新生成锁文件。

### lockfile_dangling_ref（high）

- 触发：锁文件里某包依赖的包名不存在于锁文件包列表（依赖图断裂）。
- 修复：重新生成锁文件；手工编辑锁文件会破坏依赖图。

### lockfile_duplicate_conflict（high）

- 触发：同名同版本存在多个不同 `resolved` / `integrity` 来源。
- 含义：同一版本解析到不同 tarball，存在被替换风险。
- 修复：统一来源；核对 integrity 是否与官方一致。

### lockfile_root_mismatch（medium）

- 触发：锁文件根 `name` / `version` 与清单不一致。
- 修复：锁文件与清单应对应同一项目；复制 / 改名后需重新生成。

### lockfile_integrity_missing（medium）

- 触发：package-lock.json（v2/v3）条目缺 `integrity`、poetry.lock `files` 为空、Pipfile.lock 条目缺 `hashes`。
- 含义：缺少完整性校验，安装无法防篡改。
- 修复：重新生成锁文件（npm / poetry / pipenv 均会写入哈希）。

## 三、卫生

### missing_lockfile（medium）

- 触发：声明了依赖但没有锁文件（package.json 无 package-lock.json / npm-shrinkwrap.json / yarn.lock / pnpm-lock.yaml / bun.lock；pyproject.toml 或 Pipfile 无 poetry.lock / uv.lock / Pipfile.lock）。
- 修复：提交锁文件并使用 `npm ci` / `yarn install --immutable` / `pnpm install --frozen-lockfile` / `uv sync --locked` / `poetry install --locked` / `pipenv install --deploy` 保证可复现。

### unpinned（low / medium）

- 触发：npm 依赖为 `*` / `latest` / 未指定；requirements.txt 无版本约束；Maven 依赖未声明 `<version>` 且不在 dependencyManagement（medium）。
- 修复：给出精确或收窄范围并配合锁文件。

### snapshot（low）

- 触发：Maven 依赖使用 `-SNAPSHOT` 版本。
- 修复：发布物改用 release 版本。

## 四、typo-squat

### typosquat（low）

- 触发：依赖名与内置知名 npm / PyPI 包列表编辑距离 ≤ 2（含转置），如 `lodassh`→lodash、`requets`→requests。
- 含义：拼写仿冒包是供应链投毒常见手法，需人工确认包名与来源。
- 修复：核对包名拼写与发布者；用精确版本 + 完整性哈希；可配置私有仓库白名单。
- 说明：内置列表是常用包子集，未覆盖 ≠ 安全；本规则只做提示，不自动判定恶意。

## 五、版本范围语义

- **npm semver**：`^` `~` `>=` `<=` `>` `<` `=`、x 范围（`1.x` / `1.2.x`）、`*`、`||` 或、连字符范围（`1.2.3 - 2.3.4`）、预发布规则（预发布版本默认不满足不含预发布的比较器）。
- **PEP 440**：`==` `!=` `>=` `<=` `>` `<` `~=` `===`、逗号 AND、`||` 或、`==1.2.*` 通配；`~=1.2` = `>=1.2,==1.2.*`。

## 六、已知限制（v0.1.4）

- 不做在线 CVE 比对（那是 snyk / trivy / npm audit 的地盘）。
- 依赖混淆为本地近似：真正确认「私有包名被公共仓库抢占」需要在线核对，引擎给强信号供人工复核。
- `yarn.lock` / `pnpm-lock.yaml` / `bun.lock` / `uv.lock` 做基础一致性解析；`bun.lockb` 只识别不深度解析，`go.mod` / `Cargo.lock` 未支持。
- 只扫描给定目录（不递归子目录 monorepo）；`-r` 递归的 requirements 会跟随（深度 ≤ 5）。
- 不读用户级 `.npmrc` / `pip.conf`（只读项目内配置），避免触碰项目外数据。

## 七、输出语义

- `scannedFiles`：本次实际读取的依赖清单 / 锁文件，用于证明扫描输入。
- `files`：本次产生 finding 的文件；干净扫描可以为空，不代表没有读取输入。
