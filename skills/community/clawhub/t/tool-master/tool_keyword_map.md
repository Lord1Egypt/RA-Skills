# 工具-关键词映射表

## 格式说明
```
工具类型:工具名称 | 关键词1,关键词2,关键词3 | 命令示例 | 优先级(1-10)
```
## 优先级说明
- 10: 最常用,最核心的工具
- 9-8: 常用工具
- 7-6: 一般工具
- 5-4: 较少使用的工具
- 3-1: 特殊用途工具

## 文件/目录操作类

### 目录结构查看
bash:tree | 目录,目录结构,树形结构,文件夹结构 | tree -a | 8  
bash:ls | 列表,文件列表,查看文件,目录内容 | ls -la | 9  
bash:find | 查找,搜索文件,定位文件,文件查找 | find . -name "*.py" | 8  
rust:exa | 增强ls,文件列表,现代ls | exa -la | 8  
  
### 文件信息统计  
bash:wc | 统计,行数,字数,字符数,文件大小 | wc -l file.txt | 7  
bash:du | 大小,磁盘使用,目录大小,空间占用 | du -sh . | 8  
bash:file | 文件类型,文件格式,检测类型 | file document.pdf | 6  
  
### 文件内容查看  
bash:cat | 查看,显示,文件内容,全文 | cat file.txt | 7  
bash:head | 头部,前几行,开头 | head -20 file.txt | 6  
bash:tail | 尾部,后几行,结尾,日志 | tail -f log.txt | 7  
bash:less | 浏览,分页查看,大文件 | less large_file.txt | 6  
rust:bat | 代码查看,语法高亮,cat替代 | bat file.rs | 8  
  
### 文件搜索  
bash:grep | 搜索,查找文本,匹配,模式 | grep "error" log.txt | 9  
bash:ack | 代码搜索,快速搜索,ack搜索 | ack "function" | 7  
bash:rg | 快速搜索,ripgrep,高性能搜索 | rg "pattern" | 8  
rust:ripgrep (rg) | 快速搜索,代码搜索,高性能搜索 | rg "pattern" | 9  
rust:fd-find (fd) | 文件查找,替代find,快速查找 | fd "*.rs" | 8  
  
### 文件操作  
bash:cp | 复制,拷贝,备份文件 | cp source.txt dest.txt | 8  
bash:mv | 移动,重命名,改名 | mv old.txt new.txt | 8  
bash:rm | 删除,移除,清理 | rm file.txt | 9  
bash:touch | 创建,新建文件,空文件 | touch newfile.txt | 6  
bash:diff | 比较,文件差异,文本比较 | diff file1.txt file2.txt | 7  
bash:diff -u | 详细比较,统一格式差异 | diff -u file1.txt file2.txt | 7  
  
## 系统信息类  
  
### 系统状态  
bash:date | 时间,日期,当前时间,时间戳 | date '+%Y-%m-%d %H:%M:%S' | 7  
bash:uptime | 运行时间,系统运行,开机时间 | uptime | 6  
bash:whoami | 用户,当前用户,登录用户 | whoami | 5  
bash:uname | 系统信息,内核,操作系统 | uname -a | 6  
  
### 进程管理  
bash:ps | 进程,运行进程,查看进程 | ps aux | 8  
bash:top | 监控,系统监控,资源使用 | top | 7  
bash:htop | 增强监控,交互式监控 | htop | 7  
bash:kill | 终止,结束进程,杀死进程 | kill -9 PID | 8  
  
### 网络相关  
bash:ping | 网络测试,连通性,ping测试 | ping google.com | 7  
bash:curl | 下载,网络请求,API调用,获取网页 | curl -O https://example.com/file.txt | 8  
bash:wget | 下载文件,网页下载 | wget https://example.com/file.txt | 7  
bash:netstat | 网络连接,端口,监听端口 | netstat -tulpn | 7  
bash:ss | 套接字统计,网络连接 | ss -tulpn | 7  
  
### 磁盘空间  
bash:df | 磁盘空间,文件系统,可用空间 | df -h | 7  
bash:du | 目录大小,磁盘使用 | du -sh directory/ | 8  
  
## 文本处理类  
  
### 文本编辑  
bash:sed | 替换,编辑,文本替换,批量替换 | sed 's/old/new/g' file.txt | 8  
bash:awk | 处理,分析,提取,格式化,报表 | awk '{print $1}' file.txt | 8  
bash:cut | 切割,提取列,字段提取 | cut -d',' -f1 file.csv | 7  
bash:sort | 排序,排列,顺序 | sort file.txt | 7  
bash:uniq | 去重,唯一值,重复项 | sort file.txt | uniq | 7  
bash:vim | 编辑,文本编辑器,修改文件,代码编辑 | vim file.txt | 8  
bash:vimdiff | 比较,差异对比,文件比较,可视化比较 | vimdiff file1.txt file2.txt | 7  
  
### 文本转换  
bash:tr | 转换,字符替换,大小写转换 | tr 'a-z' 'A-Z' < file.txt | 6  
bash:iconv | 编码转换,字符集转换 | iconv -f UTF-8 -t GBK file.txt | 5  
  
## Python工具类  
  
### 文件处理  
python:文件统计 | 统计,分析文件,文件信息,行数统计 | python3 -c "import os; print(len(open('file.txt').readlines()))" | 7  
python:JSON处理 | JSON,解析,格式化,提取 | python3 -c "import json; data=json.load(open('data.json')); print(data['key'])" | 8  
python:CSV处理 | CSV,表格,数据处理,分析 | python3 -c "import csv; with open('data.csv') as f: reader=csv.reader(f); print(list(reader))" | 8  
  
### 数据处理  
python:数据清洗 | 清洗,清理数据,预处理 | python3 -c "import pandas as pd; df=pd.read_csv('data.csv'); print(df.head())" | 7  
python:数据分析 | 分析,统计,计算,汇总 | python3 -c "import numpy as np; data=[1,2,3]; print(np.mean(data))" | 7  
python:数据可视化 | 图表,图形,可视化,绘图 | python3 -c "import matplotlib.pyplot as plt; plt.plot([1,2,3]); plt.show()" | 6  
  
### 网络请求  
python:API调用 | API,接口,请求,获取数据 | python3 -c "import requests; r=requests.get('https://api.example.com'); print(r.json())" | 8  
python:网页抓取 | 抓取,爬虫,网页内容,提取 | python3 -c "import requests; from bs4 import BeautifulSoup; r=requests.get('https://example.com'); soup=BeautifulSoup(r.text); print(soup.title)" | 7  
  
### 系统操作  
python:文件操作 | 批量处理,文件操作,自动化 | python3 -c "import os; for f in os.listdir('.'): print(f)" | 7  
python:进程管理 | 子进程,执行命令,系统调用 | python3 -c "import subprocess; result=subprocess.run(['ls','-la'], capture_output=True); print(result.stdout.decode())" | 7  
  
## 开发工具类  
  
### 版本控制  
bash:git status | Git状态,版本状态,变更状态 | git status | 8  
bash:git log | 提交历史,版本历史,变更记录 | git log --oneline | 7  
bash:git diff | 差异,比较,变更内容 | git diff HEAD~1 | 7  
bash:git log --graph | 图形化分支,分支图,可视化历史 | git log --oneline --graph --all | 8  
bash:git diff HEAD~1 | 比较提交,查看变更,两次提交差异 | git diff HEAD~1 HEAD -- filename | 8  
bash:git difftool --tool=vimdiff | 图形化比较,并排显示,vimdiff差异 | git difftool --tool=vimdiff HEAD~1 HEAD -- file | 7  
bash:vimdiff <(git show) | 进程替换比较,灵活版本对比 | vimdiff <(git show HEAD~1:file) <(git show HEAD:file) | 7  
bash:gvimdiff | 图形对比,可视化差异,gvim比较 | gvimdiff file1 file2 | 6  
bash:git remote add | 首次关联远程,添加origin,新建远程 | git remote add origin git@github.com:user/repo.git | 8  
bash:git remote set-url | 修改远程地址,切换SSH,已有远程改URL | git remote set-url origin git@github.com:user/repo.git | 8  
bash:ssh-keygen | 生成SSH密钥,免密登录 | ssh-keygen -t ed25519 -C "email@example.com" | 8  
bash:git config | 配置用户名邮箱,全局设置 | git config --global user.name "Your Name" | 8  
bash:git init | 初始化仓库,创建git | git init | 8  
bash:git add | 添加,暂存,准备提交 | git add file.txt | 8  
bash:git commit | 提交,保存变更,版本提交 | git commit -m "message" | 8  
bash:git push | 推送,上传,同步远程 | git push origin main | 8  
bash:git pull | 拉取,更新,获取最新 | git pull origin main | 8  
  
### Rust 开发  
rust:cargo build | Rust编译,构建项目,编译Rust | ~/.cargo/bin/cargo build | 8  
rust:cargo run | 运行Rust程序,执行项目 | ~/.cargo/bin/cargo run | 8  
rust:cargo test | Rust测试,单元测试 | ~/.cargo/bin/cargo test | 7  
rust:cargo check | 快速检查,语法检查 | ~/.cargo/bin/cargo check | 7  
rust:cargo clippy | Rust代码检查,静态分析 | ~/.cargo/bin/cargo clippy | 7  
rust:cargo fmt | Rust代码格式化 | ~/.cargo/bin/cargo fmt | 6  
rust:cargo new | 创建Rust项目,新建项目 | ~/.cargo/bin/cargo new project_name | 8  
rust:cargo add | 添加Rust依赖,安装库 | ~/.cargo/bin/cargo add serde | 8  
rust:cargo update | 更新Rust依赖 | ~/.cargo/bin/cargo update | 7  
rust:cargo doc | 生成Rust文档 | ~/.cargo/bin/cargo doc --open | 6  
rust:cargo search | 搜索Rust库,查找第三方库 | ~/.cargo/bin/cargo search "http client" | 7  
rust:cargo info | 查看库信息,依赖详情 | ~/.cargo/bin/cargo info serde | 7  
rust:cargo add | 添加Rust依赖,安装库 | ~/.cargo/bin/cargo add serde | 8  
rust:cargo tree | 查看依赖树,依赖关系 | ~/.cargo/bin/cargo tree | 6  
rust:cargo new --bin | 创建二进制项目,可执行程序 | ~/.cargo/bin/cargo new project-name --bin | 8  
rust:cargo new --lib | 创建库项目,Rust库 | ~/.cargo/bin/cargo new project-name --lib | 8  
rust:cargo workspace | 创建工作区,多项目管理 | 创建Cargo.toml定义[workspace] | 7  
  
### 代码分析  
bash:flake8 | Python检查,代码规范,语法检查 | flake8 myfile.py | 7  
bash:pylint | Python代码质量,静态分析 | pylint myfile.py | 6  
bash:mypy | Python类型检查,类型提示 | mypy myfile.py | 6  
  
### 构建测试  
bash:make | 编译,构建,Makefile | make | 7  
bash:cmake | CMake构建,跨平台构建 | cmake . && make | 6  
bash:pytest | Python测试,单元测试 | pytest tests/ | 7  
  
## 数据库类  
  
### SQLite  
bash:sqlite3 | SQLite数据库,查询,数据库操作 | sqlite3 database.db "SELECT * FROM table;" | 7  
  
### PostgreSQL  
bash:psql | PostgreSQL,数据库查询,SQL | psql -U user -d database -c "SELECT * FROM table;" | 6  
  
### MySQL  
bash:mysql | MySQL数据库,查询,管理 | mysql -u user -p database -e "SELECT * FROM table;" | 6  
  
## 压缩归档类  
  
### 压缩解压  
bash:tar | 打包,归档,压缩文件 | tar -czf archive.tar.gz directory/ | 8  
bash:gzip | 压缩,GZ压缩,解压 | gzip file.txt | 7  
bash:gunzip | 解压,GZ解压 | gunzip file.txt.gz | 7  
bash:zip | ZIP压缩,打包 | zip archive.zip file1.txt file2.txt | 7  
bash:unzip | ZIP解压,提取 | unzip archive.zip | 7  
  
## 权限管理类  
  
### 文件权限  
bash:chmod | 权限,修改权限,执行权限 | chmod +x script.sh | 8  
bash:chown | 所有者,修改所有者 | chown user:group file.txt | 7  
bash:chgrp | 用户组,修改组 | chgrp group file.txt | 6  
  
### 用户管理  
bash:who | 登录用户,在线用户 | who | 5  
bash:w | 用户活动,登录信息 | w | 5  
bash:id | 用户ID,组ID,身份信息 | id | 5  
  
## 监控调试类  
  
### 系统监控  
bash:vmstat | 虚拟内存,系统性能 | vmstat 1 | 6  
bash:iostat | IO统计,磁盘IO | iostat 1 | 6  
bash:mpstat | CPU统计,处理器性能 | mpstat 1 | 6  
  
### 日志查看  
bash:journalctl | 系统日志,服务日志 | journalctl -u service-name | 7  
bash:dmesg | 内核日志,系统消息 | dmesg | 6  
  
## OpenClaw 工具类  
  
### 系统状态  
openclaw:status | OpenClaw状态,系统状态,健康检查,状态检查 | openclaw status | 9  
openclaw:doctor | 诊断,问题诊断,健康诊断,系统诊断 | openclaw doctor | 8  
openclaw:version | 版本,版本检查,OpenClaw版本 | openclaw --version | 7  
  
### Gateway管理  
openclaw:gateway status | Gateway状态,网关状态,服务状态 | openclaw gateway status | 8  
openclaw:gateway start | 启动Gateway,启动服务,启动网关 | openclaw gateway start | 8  
openclaw:gateway stop | 停止Gateway,停止服务,停止网关 | openclaw gateway stop | 8  
openclaw:gateway restart | 重启Gateway,重启服务,重启网关 | openclaw gateway restart | 8  
  
### 会话管理  
openclaw:sessions list | 会话列表,查看会话,活动会话 | openclaw sessions list | 7  
openclaw:sessions history | 会话历史,消息历史,聊天历史 | openclaw sessions history <sessionKey> | 6  
  
### 技能管理  
openclaw:skills list | 技能列表,查看技能,可用技能 | openclaw skills list | 7  
openclaw:skills install | 安装技能,添加技能,下载技能 | openclaw skills install <skill-name> | 7  
openclaw:skills uninstall | 卸载技能,移除技能,删除技能 | openclaw skills uninstall <skill-name> | 6  
  
### 配置管理  
openclaw:config get | 获取配置,查看配置,读取配置 | openclaw config get <key> | 7  
openclaw:config set | 设置配置,修改配置,更新配置 | openclaw config set <key> <value> | 7  
openclaw:config list | 配置列表,所有配置,查看所有配置 | openclaw config list | 6  
  
### 模型管理  
openclaw:models list | 模型列表,可用模型,查看模型 | openclaw models list | 7  
openclaw:models set | 设置模型,切换模型,更改模型 | openclaw models set <model-alias> | 7  
  
### 消息发送  
openclaw:message send | 发送消息,消息发送,通知发送 | openclaw message send --channel webchat --message "Hello" | 6  
  
### 备份恢复  
openclaw:backup create | 创建备份,备份数据,数据备份 | openclaw backup create | 6  
openclaw:backup restore | 恢复备份,数据恢复,还原备份 | openclaw backup restore <backup-file> | 6  
  
### 系统事件  
openclaw:system heartbeat | 心跳,系统心跳,保持活动 | openclaw system heartbeat | 5  
openclaw:system wake | 唤醒,系统唤醒,发送唤醒事件 | openclaw system wake "任务提醒" | 5  
  
## 其他实用工具  
  
### 计算器  
bash:bc | 计算,数学计算,计算器 | echo "5 + 3" | bc | 6  
bash:expr | 表达式计算,算术 | expr 5 + 3 | 5  
  
### 编码转换  
bash:base64 | Base64编码,解码 | echo "hello" | base64 | 6  
bash:md5sum | MD5校验,哈希值 | md5sum file.txt | 6  
bash:sha256sum | SHA256校验,安全哈希 | sha256sum file.txt | 6  
  
### 时间相关  
bash:sleep | 等待,暂停,延时 | sleep 5 | 5  
bash:time | 计时,执行时间,性能测试 | time command | 6  
