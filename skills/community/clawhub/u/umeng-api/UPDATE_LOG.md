# umeng-api 技能更新日志

## 2026-03-31 - 添加配置文件支持

### 更新内容

1. **新增 `umeng_config.py` 模块**
   - 支持从 `umeng-config.json` 配置文件读取认证信息
   - 支持多种字段名（`apiKey`/`api_key`/`UMENG_API_KEY`）
   - 提供 `get_umeng_credentials()` 函数，按优先级获取认证信息
   - 提供 `save_config()` 函数用于保存配置

2. **更新 `umeng_get_outlier_points.py`**
   - 集成 `umeng_config` 模块
   - 认证信息获取优先级：参数 > 配置文件 > 环境变量
   - 改进错误提示，明确告知用户如何配置

3. **更新 `aop/__init__.py`**
   - 添加 `_load_umeng_config()` 函数
   - 修改 `get_default_appinfo()` 自动从配置文件或环境变量加载认证信息
   - 保持向后兼容，支持手动 `set_default_appinfo()`

4. **更新 `SKILL.md` 文档**
   - 详细说明三种认证配置方式
   - 添加配置文件示例和安全提示
   - 更新代码示例，展示自动加载认证信息

5. **新增示例文件**
   - `umeng-config.json.example` - 配置文件模板

6. **更新 `TOOLS.md`**
   - 添加友盟 API 配置说明

### 认证信息优先级

从高到低：
1. 代码中直接传入的参数（`api_key`, `api_security`）
2. `umeng-config.json` 配置文件
3. 环境变量（`UMENG_API_KEY`, `UMENG_API_SECURITY`）

### 配置文件位置

按以下顺序查找：
1. 当前工作目录 (`./umeng-config.json`)
2. 用户主目录 (`~/umeng-config.json`)
3. 技能目录 (`<skill-dir>/umeng-config.json`)

### 安全建议

- 将 `umeng-config.json` 添加到 `.gitignore`
- 设置文件权限：`chmod 600 umeng-config.json`
- 不要将认证信息硬编码到代码中

### 向后兼容性

所有更新保持向后兼容：
- 原有的环境变量方式继续有效
- 原有的 `set_default_appinfo()` 方式继续有效
- 现有代码无需修改即可使用新的配置文件功能
