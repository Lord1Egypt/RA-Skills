# 虚拟用户 Skill 部署指南

> 详细部署步骤和配置说明

---

## 📋 部署前准备

### 系统要求

- Python 3.8+
- pip 包管理器
- 至少 2GB 可用磁盘空间
- 网络连接（下载向量化模型）

### 检查环境

```bash
# 检查 Python 版本
python3 --version

# 检查 pip
pip3 --version
```

---

## 🚀 快速部署

### 方法 1：使用快速启动脚本（推荐）

```bash
# 进入技能目录
cd virtual_user_skill

# 运行快速启动脚本
./run.sh "用户的问题"
```

脚本会自动：
1. 创建虚拟环境
2. 安装依赖
3. 生成密钥
4. 检查数据文件
5. 运行技能

### 方法 2：手动部署

```bash
# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 初始化密钥
python3 src/encrypt.py

# 4. 准备数据
python3 scripts/prepare_data.py your_data.xlsx

# 5. 运行技能
python3 src/main.py "用户的问题"
```

---

## 📊 数据准备

### 从语雀导出数据

1. 打开语雀文档
2. 点击"导出" → "Excel"
3. 保存为 `scenario_library.xlsx`

### 转换数据格式

```bash
python3 scripts/prepare_data.py scenario_library.xlsx
```

输出文件：
- `data/scenario_library.json.enc` - 加密的场景库
- `data/scenario_embeddings.npy` - 预计算的向量

### 数据字段要求

Excel 应包含以下字段（Sheet1）：

| 字段名 | 必填 | 说明 |
|:---|:---|:---|
| 序号 | 是 | 记录编号 |
| 用户姓名和背景信息 | 是 | 用户画像描述 |
| 用户具体场景 | 是 | 使用场景 |
| 任务 | 是 | 用户任务 |
| 痛点 | 否 | 不满意点 |
| 爽点 | 否 | 满意点 |
| 底层需求 | 是 | 根本需求 |

---

## 🔧 配置选项

### 环境变量

```bash
# 自定义数据目录
export VIRTUAL_USER_DATA_DIR=/path/to/data

# 自定义模型
export VIRTUAL_USER_MODEL_NAME=bge-large-zh-v1.5

# 自动选择模式
export VIRTUAL_USER_AUTO_SELECT=true
```

### 配置文件

编辑 `config.yaml`：

```yaml
defaults:
  user_types_count: 10      # 生成的用户类型数量
  auto_select_count: 3      # 自动选择的数量
  search_top_k: 20          # 搜索场景数量
```

---

## 🧪 测试验证

### 单元测试

```bash
# 安装测试依赖
pip install pytest

# 运行测试
python3 -m pytest tests/ -v
```

### 端到端测试

```bash
# 基本测试
./run.sh "测试问题" --auto

# 查看输出
ls outputs/
```

### 验证清单

- [ ] 依赖安装成功
- [ ] 密钥生成成功（`~/.virtual_user/.key` 存在）
- [ ] 数据文件存在（`data/*.enc` 和 `data/*.npy`）
- [ ] 技能运行无报错
- [ ] 能生成虚拟用户类型
- [ ] 能生成对话回复
- [ ] 能导出报告

---

## 🐛 故障排查

### 问题 1：依赖安装失败

```bash
# 升级 pip
pip install --upgrade pip

# 重试安装
pip install -r requirements.txt
```

### 问题 2：模型下载失败

```bash
# 手动下载模型
# 访问 https://huggingface.co/BAAI/bge-large-zh-v1.5
# 下载到本地后设置环境变量
export SENTENCE_TRANSFORMERS_HOME=/path/to/models
```

### 问题 3：密钥文件权限错误

```bash
# 修复权限
chmod 600 ~/.virtual_user/.key
```

### 问题 4：数据文件不存在

```bash
# 重新生成数据
python3 scripts/prepare_data.py your_data.xlsx
```

---

## 📦 部署到生产环境

### 1. 服务器部署

```bash
# 在服务器上克隆代码
git clone <your-repo-url>
cd virtual_user_skill

# 安装依赖
./run.sh

# 设置为系统服务（可选）
sudo cp virtual_user.service /etc/systemd/system/
sudo systemctl enable virtual_user
sudo systemctl start virtual_user
```

### 2. Docker 部署

创建 `Dockerfile`：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "src/main.py"]
```

构建和运行：

```bash
docker build -t virtual-user-skill .
docker run -v ./data:/app/data virtual-user-skill "用户问题"
```

### 3. API 服务部署

创建 `api.py`：

```python
from flask import Flask, request, jsonify
from src import VirtualUserSkill

app = Flask(__name__)
skill = VirtualUserSkill()

@app.route('/api/interview', methods=['POST'])
def interview():
    data = request.json
    question = data.get('question')
    
    result = skill.run(question, auto_select=True)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

运行：

```bash
pip install flask
python3 api.py
```

---

## 🔐 安全建议

### 密钥管理

- ✅ 密钥保存在 `~/.virtual_user/.key`
- ✅ 文件权限设置为 600
- ❌ 不要提交到 Git
- ❌ 不要分享给他人

### 数据保护

- ✅ 场景库加密存储
- ✅ 运行时解密，不暴露原始数据
- ⚠️ 如需更高级别保护，使用 API 服务模式

### 访问控制

- 在生产环境中添加身份验证
- 限制 API 调用频率
- 记录访问日志

---

## 📞 技术支持

遇到问题？

1. 查看 [SKILL.md](SKILL.md) 常见问题章节
2. 检查日志文件 `logs/*.log`
3. 提交 GitHub Issue
4. 联系作者

---

## 📝 更新维护

### 更新技能

```bash
# 拉取最新代码
git pull

# 重新安装依赖
pip install -r requirements.txt --upgrade

# 重新生成密钥（如需要）
rm ~/.virtual_user/.key
python3 src/encrypt.py
```

### 更新场景库

```bash
# 准备新数据
python3 scripts/prepare_data.py new_data.xlsx

# 备份旧数据
cp data/scenario_library.json.enc data/scenario_library.json.enc.bak

# 替换新数据
mv new_scenario_library.json.enc data/scenario_library.json.enc
```

---

## ✅ 部署完成检查清单

- [ ] 代码已部署到服务器/本地
- [ ] 依赖已安装
- [ ] 密钥已生成
- [ ] 数据已准备
- [ ] 测试通过
- [ ] 配置已优化
- [ ] 监控已设置
- [ ] 备份策略已制定

---

**部署完成！🎉**

开始使用：
```bash
./run.sh "用户预订机票时最关心什么？"
```
