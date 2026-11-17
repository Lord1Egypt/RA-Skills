# 源代码文档格式规范

## 总体要求

- 提交源程序的前 30 页和后 30 页（共 60 页）
- 如果总代码量不足 60 页，提交全部代码
- 每页不少于 50 行有效代码（去除空行和纯注释行）
- 文件格式：PDF
- 单个文件建议 ≤ 10MB

## 页眉规范

```
格式：软件全称 V{版本号}
示例：鱼探AI——智能钓鱼助手软件 V1.0
位置：页面顶部居中
字体：宋体，小五号
```

## 页脚规范

```
格式：第 X 页 / 共 Y 页
示例：第 1 页 / 共 60 页
位置：页面底部居中
字体：宋体，小五号
```

## 代码内容规范

### 必须包含的内容
- ✅ 核心业务逻辑代码
- ✅ 主要功能模块实现
- ✅ 自定义类/函数/方法
- ✅ 有代表性的算法实现

### 必须排除的内容
- ❌ 空行（减少有效行数统计）
- ❌ 纯注释行（只含注释不含代码的行）
- ❌ 第三方库代码（如 node_modules、vendor）
- ❌ 开源框架代码（如 React、Vue 源码）
- ❌ 自动生成的模板代码（如 create-react-app 脚手架代码）
- ❌ 配置文件（如 package.json、.env、webpack.config.js，除非是软件核心配置）
- ❌ 硬编码的敏感信息（数据库密码、API 密钥、Token 等）

### 注释处理
- 保留行内注释（代码和注释在同一行），如：`int count = 0; // 初始化计数器`
- 去除纯注释行（整行只有注释），如：`// 这是初始化函数`

## 代码格式规范

### 字体和排版
- 字体：宋体（中文）/ Times New Roman 或 Consolas（英文代码）
- 字号：五号或小五号（9-10pt）
- 行距：单倍行距
- 左侧添加连续行号（如 1-3000）

### 页边距
- 上：2.5cm，下：2.5cm
- 左：3.0cm（留装订边），右：2.0cm

## 不同编程语言的处理

### Web 前端（HTML/CSS/JS）
- 提交核心 JS/TS 业务逻辑
- 排除 node_modules、框架源码
- 可提交自定义组件代码

### 后端（Java/Python/Go/PHP）
- 提交 Service/Controller/Model 层代码
- 排除框架自动生成的 CRUD 代码
- Python 排除 `__pycache__` 和 venv

### 微信小程序
- 提交核心页面 JS 逻辑和自定义组件
- 排除微信原生 API 调用样板代码
- 排除第三方 UI 库

### APP（Android/iOS）
- 提交核心 Activity/ViewController 代码
- 排除 Gradle/Pod 配置文件
- 排除第三方 SDK 集成代码

## 代码量不足的处理方案

如果有效代码量不足 3000 行（60 页 × 50 行）：

1. **合并文件**：将多个逻辑相关的短文件合并到同一页
2. **补充单元测试代码**：如项目有测试代码，可纳入
3. **提交全部代码**：不足 60 页时提交全部有效代码即可，无需凑数

⚠️ 切勿：
- 复制开源代码充数（2026 年查重系统会检测）
- 重复提交相同代码段落
- 添加无用代码填充行数

## 格式化流程（供 Agent 执行）

```
1. 读取源代码目录
2. 遍历文件，分类：核心代码 / 排除文件
3. 对核心代码文件：
   a. 去除纯空行
   b. 去除纯注释行
   c. 保留行内注释
   d. 统计有效行数
4. 合并所有有效代码行
5. 按 50 行/页分页
6. 每页添加页眉页脚
7. 取前 30 页 + 后 30 页（或全部）
8. 输出格式化文本
```

## 示例

### 输入代码
```python
# 用户管理模块
# 作者：张三

def add_user(name, email):  # 添加用户
    if not name:  # 检查名称
        return False
    # 创建用户记录
    user = User(name=name, email=email)
    user.save()
    return True

# 删除用户
def delete_user(user_id):
    user = User.get(id=user_id)
    user.delete()
```

### 处理后（有效行数 = 5）
```python
def add_user(name, email):  # 添加用户
    if not name:  # 检查名称
        return False
    user = User(name=name, email=email)
    user.save()
    return True
def delete_user(user_id):
    user = User.get(id=user_id)
    user.delete()
```

（纯注释行 `# 用户管理模块`、`# 作者：张三`、`# 创建用户记录`、`# 删除用户` 被去除；行内注释保留。）
