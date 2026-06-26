#!/bin/bash
# Termaid 批量渲染脚本
# 自动将 Mermaid 图表批量渲染为终端友好的格式

set -e

# 配置
INPUT_DIR="./mermaid-diagrams"
OUTPUT_DIR="./rendered-diagrams"
THEME="phosphor"
FORMAT="txt"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查输入目录
if [ ! -d "$INPUT_DIR" ]; then
    echo -e "${YELLOW}⚠️  输入目录不存在，创建示例目录...${NC}"
    mkdir -p "$INPUT_DIR"
    
    # 创建示例文件
    cat > "$INPUT_DIR/architecture.mmd" << 'EOF'
graph TB
    subgraph "前端"
        UI[用户界面]
        Component[Web组件]
        State[状态管理]
    end
    
    subgraph "后端"
        API[API网关]
        Service[业务服务]
        DB[数据库]
    end
    
    UI --> API
    Component --> API
    State --> API
    API --> Service
    Service --> DB
EOF
    
    cat > "$INPUT_DIR/workflow.mmd" << 'EOF'
graph TD
    Start([开始]) --> Input{输入数据}
    Input -->|有效| Process[处理]
    Input -->|无效| Error[错误]
    Process --> Output([完成])
EOF
    
    echo -e "${GREEN}✅ 已创建示例目录和文件${NC}"
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

echo -e "${BLUE}🚀 Termaid 批量渲染开始${NC}"
echo "输入目录: $INPUT_DIR"
echo "输出目录: $OUTPUT_DIR"
echo "使用主题: $THEME"
echo ""

# 统计变量
total_files=0
success_count=0
error_count=0

# 遍历所有 .mmd 文件
for input_file in "$INPUT_DIR"/*.mmd; do
    if [ -f "$input_file" ]; then
        total_files=$((total_files + 1))
        filename=$(basename "$input_file")
        output_file="$OUTPUT_DIR/${filename%.mmd}.$FORMAT"
        
        echo -e "${BLUE}📄 处理: $filename${NC}"
        
        # 获取文件大小
        file_size=$(wc -c < "$input_file")
        echo "  大小: ${file_size} bytes"
        
        # 提取图表类型（简单检测）
        first_line=$(head -1 "$input_file" | tr '[:upper:]' '[:lower:]')
        if echo "$first_line" | grep -q "graph"; then
            chart_type="流程图"
        elif echo "$first_line" | grep -q "sequence"; then
            chart_type="序列图"
        elif echo "$first_line" | grep -q "class"; then
            chart_type="类图"
        elif echo "$first_line" | grep -q "er"; then
            chart_type="ER图"
        elif echo "$first_line" | grep -q "state"; then
            chart_type="状态图"
        elif echo "$first_line" | grep -q "block"; then
            chart_type="块图"
        elif echo "$first_line" | grep -q "git"; then
            chart_type="Git图"
        elif echo "$first_line" | grep -q "pie"; then
            chart_type="饼图"
        elif echo "$first_line" | grep -q "treemap"; then
            chart_type="树状图"
        else
            chart_type="未知类型"
        fi
        echo "  类型: $chart_type"
        
        # 渲染图表
        echo -n "  渲染..."
        if termaid "$input_file" --theme "$THEME" > "$output_file" 2>/dev/null; then
            success_count=$((success_count + 1))
            
            # 检查渲染结果
            output_size=$(wc -c < "$output_file")
            if [ $output_size -gt 10 ]; then
                echo -e " ${GREEN}成功 ✅${NC}"
                echo "  输出: $output_file (${output_size} bytes)"
                
                # 显示预览
                echo "  预览:"
                head -5 "$output_file" | sed 's/^/      /'
            else
                echo -e " ${YELLOW}警告 ⚠️ (输出过小)${NC}"
                error_count=$((error_count + 1))
            fi
        else
            echo -e " ${RED}失败 ❌${NC}"
            error_count=$((error_count + 1))
            rm -f "$output_file" 2>/dev/null || true
        fi
        
        echo ""
    fi
done

# 生成汇总报告
echo -e "${BLUE}📊 渲染汇总${NC}"
echo "=========================="
echo "总文件数: $total_files"
echo -e "成功: ${GREEN}$success_count${NC}"
echo -e "失败: ${RED}$error_count${NC}"
echo ""

if [ $total_files -eq 0 ]; then
    echo -e "${YELLOW}⚠️  没有找到 Mermaid 文件 (.mmd)${NC}"
    echo ""
    echo "使用方法:"
    echo "1. 将 Mermaid 文件放入 $INPUT_DIR/"
    echo "2. 运行此脚本"
    echo "3. 查看 $OUTPUT_DIR/ 中的渲染结果"
    exit 0
fi

# 创建索引文件
INDEX_FILE="$OUTPUT_DIR/INDEX.md"
cat > "$INDEX_FILE" << EOF
# Termaid 渲染结果索引

**渲染时间**: $(date)  
**输入目录**: $INPUT_DIR  
**输出目录**: $OUTPUT_DIR  
**主题**: $THEME  
**格式**: $FORMAT  

## 文件列表

EOF

# 添加文件列表到索引
for input_file in "$INPUT_DIR"/*.mmd; do
    if [ -f "$input_file" ]; then
        filename=$(basename "$input_file")
        base_name="${filename%.mmd}"
        output_file="$base_name.$FORMAT"
        
        # 获取源文件信息
        source_size=$(wc -c < "$input_file")
        source_lines=$(wc -l < "$input_file")
        
        # 获取渲染文件信息
        rendered_file="$OUTPUT_DIR/$output_file"
        if [ -f "$rendered_file" ]; then
            rendered_size=$(wc -c < "$rendered_file")
            rendered_lines=$(wc -l < "$rendered_file")
            status="✅ 已渲染"
        else
            rendered_size="N/A"
            rendered_lines="N/A"
            status="❌ 失败"
        fi
        
        cat >> "$INDEX_FILE" << EOF
### $base_name

- **源文件**: \`$filename\` ($source_size bytes, $source_lines lines)
- **渲染文件**: \`$output_file\` ($rendered_size bytes, $rendered_lines lines)
- **状态**: $status

\`\`\`bash
# 查看渲染结果
cat "$OUTPUT_DIR/$output_file" | head -20
\`\`\`

EOF
    fi
done

# 添加使用说明
cat >> "$INDEX_FILE" << 'EOF'

## 使用说明

### 查看特定图表
```bash
# 查看流程图
cat rendered-diagrams/architecture.txt

# 带行号查看
cat -n rendered-diagrams/workflow.txt
```

### 批量操作
```bash
# 统计所有渲染文件
wc -l rendered-diagrams/*.txt

# 查找最大的图表
ls -la rendered-diagrams/*.txt | sort -k5 -n -r | head -5
```

### 重新渲染
```bash
# 单个文件重新渲染
termaid mermaid-diagrams/architecture.mmd --theme neon > rendered-diagrams/architecture.txt

# 全部重新渲染
bash batch-render.sh
```

## 故障排除

### 常见问题

1. **渲染失败**
   ```bash
   # 检查 Mermaid 语法
   # 确保文件以正确的图表类型开头
   ```

2. **输出空白**
   ```bash
   # 检查文件编码
   file -i your-file.mmd
   
   # 尝试 ASCII 模式
   termaid your-file.mmd --ascii
   ```

3. **颜色不显示**
   ```bash
   # 确保安装了 rich 扩展
   pip install termaid[rich]
   
   # 或使用 ASCII 模式
   termaid --ascii your-file.mmd
   ```

## 支持的图表类型

1. ✅ 流程图 (`graph`)
2. ✅ 序列图 (`sequenceDiagram`)
3. ✅ 类图 (`classDiagram`)
4. ✅ ER 图 (`erDiagram`)
5. ✅ 状态图 (`stateDiagram-v2`)
6. ✅ 块图 (`block-beta`)
7. ✅ Git 图 (`gitGraph`)
8. ✅ 饼图 (`pie`)
9. ✅ 树状图 (`treemap-beta`)

---
*自动生成于 $(date)*
EOF

echo -e "${GREEN}✅ 渲染完成！${NC}"
echo "索引文件: $INDEX_FILE"
echo ""
echo "🎯 下一步操作:"
echo "1. 查看渲染结果: ls -la $OUTPUT_DIR/"
echo "2. 查看索引文件: cat $INDEX_FILE | head -30"
echo "3. 测试渲染文件: cat $OUTPUT_DIR/*.txt | head -5"
echo ""
echo "🔧 配置选项:"
echo "  修改脚本开头的 THEME 变量使用不同主题"
echo "  修改 INPUT_DIR 和 OUTPUT_DIR 变量指定目录"
echo ""
echo "💡 提示:"
echo "  - 支持的主题: default, terra, neon, mono, amber, phosphor"
echo "  - 添加 --ascii 参数为纯 ASCII 输出"
echo "  - 添加 --tui 参数为交互式界面"