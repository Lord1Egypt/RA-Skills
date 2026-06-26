#!/bin/bash
set -e  # 遇错退出
set -u  # 未定义变量报错
set -o pipefail  # 管道命令失败检测

# 自媒体写作助手 - 项目结构初始化脚本
# 用途：自动创建新项目的标准目录结构

echo "📝 自媒体写作助手 - 项目结构初始化"
echo "======================================"
echo ""

# 检查项目名称参数
if [ -z "$1" ]; then
    echo "❌ 请提供项目名称"
    echo "用法: ./创建项目结构.sh \"项目名称\""
    echo ""
    echo "示例:"
    echo "  ./创建项目结构.sh \"Claude Code 评测\""
    exit 1
fi

PROJECT_NAME="$1"

# 验证项目名称（避免特殊字符）
if [[ "$PROJECT_NAME" =~ [/\\:\*\?\"\<\>\|] ]]; then
    echo "❌ 项目名称包含非法字符: / \\ : * ? \" < > |"
    echo "请使用合法的项目名称"
    exit 1
fi

DATE=$(date +%Y.%m.%d)
PROJECT_DIR="$DATE $PROJECT_NAME"

echo "项目名称：$PROJECT_NAME"
echo "创建日期：$DATE"
echo ""

# 检查是否已存在
if [ -d "$PROJECT_DIR" ]; then
    echo "⚠️  项目目录已存在：$PROJECT_DIR"
    echo ""
    read -p "是否继续？（将在现有目录中创建子文件夹）(y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 已取消"
        exit 1
    fi
fi

# 创建项目主目录
mkdir -p "$PROJECT_DIR"
echo "✅ 创建项目目录：$PROJECT_DIR"

# 创建子目录
mkdir -p "$PROJECT_DIR/_briefs"
mkdir -p "$PROJECT_DIR/_协作文档"
mkdir -p "$PROJECT_DIR/images"
echo "✅ 创建子目录：_briefs, _协作文档, images"

# 复制 brief 模板
BRIEF_FILE="$PROJECT_DIR/_briefs/$DATE $PROJECT_NAME-brief.md"

if [ -f "references/brief-template.md" ]; then
    cp "references/brief-template.md" "$BRIEF_FILE"
    echo "✅ 创建 brief 文件：$BRIEF_FILE"
else
    # 如果模板不存在，创建一个空文件
    cat > "$BRIEF_FILE" << EOF
# 项目 Brief

**创建日期**：$DATE
**项目名称**：$PROJECT_NAME
**目标平台**：□ 公众号 □ 视频逐字稿 □ 小红书 □ 其他

## 一、基本信息

### 创作目标
（你想达成什么效果？）

### 核心主题
（这篇文章/视频的核心是什么？）

### 目标受众
（谁会看这篇文章/视频？）

### 核心价值
（读者/观众能获得什么？）

## 二、内容要求

### 关键信息点
（必须包含的信息）

### 风格要求
- □ 洞察口语化
- □ 干货感强
- □ 爆款结构化
- □ 其他：________

### 特殊要求
（有什么特别需要注意的？）

## 三、参考资料

### 相关链接
（可以参考的文章、视频、产品文档等）

### 背景资料
（需要搜索的主题、关键词）

### 竞品参考
（类似主题的优秀案例）

## 四、交付标准

### 字数/时长要求
- 公众号：____ 字
- 视频逐字稿：____ 分钟
- 小红书：____ 字

### 配图需求
- □ 不需要
- □ 封面图（16:9）
- □ 核心概念图
- □ 案例/截图

### 交付时间
- 初稿：____
- 定稿：____

## 五、协作事项

### 需要测试的产品/工具
- □ 无
- □ 有：_______________

### 需要配图的内容
- □ 无
- □ 有：_______________

### 其他协作需求
___________________
___________________
___________________

## 六、备注

（其他需要说明的事项）
EOF
    echo "✅ 创建 brief 文件：$BRIEF_FILE"
fi

# 创建项目说明文件
cat > "$PROJECT_DIR/项目说明.md" << EOF
# $PROJECT_NAME

**创建日期**：$DATE
**状态**：进行中

## 项目信息

- **Brief 文件**：\`./_briefs/$DATE $PROJECT_NAME-brief.md\`
- **知识库**：\`./_knowledge_base/\`
- **协作文档**：\`./_协作文档/\`
- **配图**：\`./images/\`

## 进度跟踪

- [ ] Brief 确认
- [ ] 信息搜索
- [ ] 选题讨论
- [ ] 风格学习
- [ ] 创作初稿
- [ ] 第一遍审校（内容）
- [ ] 第二遍审校（降AI味）
- [ ] 第三遍审校（细节）
- [ ] 配图建议
- [ ] 定稿发布

## 备注
EOF

echo "✅ 创建项目说明文件"
echo ""
echo "🎉 项目结构创建完成！"
echo ""
echo "📂 项目目录：$PROJECT_DIR"
echo "📄 Brief 文件：$BRIEF_FILE"
echo ""
echo "💡 下一步："
echo "   1. cd \"$PROJECT_DIR\""