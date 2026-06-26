# Reading Manager - 阅读管家

个人阅读管理系统，帮助记录书籍、跟踪阅读进度、管理笔记并生成阅读报告。

## 快速开始

```bash
# 安装
cd ~/.openclaw/workspace/skills/reading-manager
pip install -e .

# 初始化数据库
reading data path

# 添加一本书
reading book add --title "深入理解计算机系统" --author "Randal E. Bryant" --pages 800

# 查看书籍列表
reading book list

# 更新阅读进度
reading progress update 1 --page 150

# 添加笔记
reading note add 1 --content "内存层次结构的重要性" --page 120 --tags "important,memory"

# 查看阅读统计
reading report stats
```

## 示例数据

```bash
# 添加示例书籍
reading book add --title "Python编程：从入门到实践" --author "Eric Matthes" --pages 500
reading book add --title "算法导论" --author "Thomas H. Cormen" --pages 1300
reading book add --title "设计模式" --author "GoF" --pages 400

# 添加文章
reading book add --title "如何高效学习" --url "https://example.com/learning" --type article

# 创建书单
reading list create "技术书单" --description "编程技术相关书籍"
reading list add-book "技术书单" 1
reading list add-book "技术书单" 2

# 设置年度目标
reading goal set-yearly 24
```

## 测试命令

```bash
# 测试书籍管理
reading book list
reading book show 1
reading book search Python

# 测试进度管理
reading progress show 1
reading progress history 1

# 测试笔记管理
reading note list
reading note tags

# 测试书单
reading list show

# 测试目标
reading goal status
```
