# 安装指南

> **平台要求**：此 Skill 仅支持 Linux（CentOS/RHEL 等）

## 前提条件

- Python >= 3.9
- pip（Python 包管理器）
- Terraform >= 1.0

---

## 安装依赖

```bash
# 进入 skill 目录
cd {baseDir}

# 安装 Python 依赖
pip3 install -r requirements.txt
```

### 验证安装

```bash
# 测试运行
python3 {baseDir}/main.py --help
```

---

## 安装 Terraform

### CentOS/RHEL 7/8/9

```bash
# 安装 yum-utils
sudo yum install -y yum-utils

# 添加 HashiCorp 仓库
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo

# 安装 Terraform
sudo yum -y install terraform

# 验证
terraform --version
```

### CentOS/RHEL（手动安装）

如果 yum 方式有问题，可手动安装：

```bash
# 下载（替换版本号为最新）
TERRAFORM_VERSION="1.7.0"
wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# 解压
unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# 移动到 PATH
sudo mv terraform /usr/local/bin/

# 验证
terraform --version
```

### Ubuntu/Debian

```bash
# 添加 HashiCorp GPG key
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

# 添加仓库
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

# 安装
sudo apt update && sudo apt install terraform
```

---

## Python 依赖

tc-migrate 需要以下 Python 包：

```
tencentcloud-sdk-python>=3.0.0   # 腾讯云 SDK
click>=8.0.0                      # CLI 框架
pyyaml>=6.0                       # YAML 解析
rich>=13.0.0                      # 终端美化
pydantic>=2.0.0                   # 数据验证
```

---

## 常见安装问题

### pip install 报权限错误

```bash
# 使用 --user 安装到用户目录
pip3 install --user -r requirements.txt

# 或使用 sudo（不推荐）
sudo pip3 install -r requirements.txt
```

### Python 版本不对

CentOS 7 默认 Python 2.7，需安装 Python 3.9+：

```bash
# CentOS 7 安装 Python 3.9
sudo yum install -y python39 python39-pip

# 使用 python3.9 替代 python3
python3.9 {baseDir}/main.py --help
```

### Terraform 初始化失败

```bash
# 清除缓存重试
rm -rf .terraform .terraform.lock.hcl
terraform init
```

---

## 虚拟环境（推荐）

为避免依赖冲突，建议使用虚拟环境：

```bash
# 创建虚拟环境
cd {baseDir}
python3 -m venv .venv

# 激活
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 验证
python3 main.py --help
```
