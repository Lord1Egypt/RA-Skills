#!/bin/bash
# Spring Boot测试覆盖率检查脚本

set -e  # 遇到错误退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 覆盖率阈值
LINE_COVERAGE_THRESHOLD=85
BRANCH_COVERAGE_THRESHOLD=80
METHOD_COVERAGE_THRESHOLD=90
CLASS_COVERAGE_THRESHOLD=95

print_header() {
    echo -e "\n${BLUE}=========================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}=========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_prerequisites() {
    print_header "检查环境依赖"
    
    # 检查Maven
    if ! command -v mvn &> /dev/null; then
        print_error "Maven未安装"
        exit 1
    fi
    print_success "Maven已安装: $(mvn --version | head -1)"
    
    # 检查Java
    if ! command -v java &> /dev/null; then
        print_error "Java未安装"
        exit 1
    fi
    print_success "Java已安装: $(java -version 2>&1 | head -1)"
    
    # 检查项目根目录
    if [ ! -f "pom.xml" ]; then
        print_error "当前目录不是Maven项目根目录"
        exit 1
    fi
    print_success "Maven项目检测成功"
}

run_tests() {
    print_header "运行测试"
    
    echo "清理并运行测试..."
    mvn clean test
    
    if [ $? -eq 0 ]; then
        print_success "测试运行成功"
    else
        print_error "测试运行失败"
        exit 1
    fi
}

generate_coverage_report() {
    print_header "生成覆盖率报告"
    
    echo "生成JaCoCo覆盖率报告..."
    mvn jacoco:report
    
    if [ $? -eq 0 ]; then
        print_success "覆盖率报告生成成功"
    else
        print_error "覆盖率报告生成失败"
        exit 1
    fi
}

check_coverage_thresholds() {
    print_header "检查覆盖率阈值"
    
    local jacoco_xml="target/site/jacoco/jacoco.xml"
    
    if [ ! -f "$jacoco_xml" ]; then
        print_error "覆盖率报告文件不存在: $jacoco_xml"
        exit 1
    fi
    
    # 解析JaCoCo XML文件
    echo "解析覆盖率数据..."
    
    # 提取覆盖率数据
    local line_coverage=$(xmlstarlet sel -t -v "//counter[@type='LINE']/@covered" -o "/" -v "//counter[@type='LINE']/@missed" "$jacoco_xml" 2>/dev/null | bc -l 2>/dev/null || echo "0")
    local branch_coverage=$(xmlstarlet sel -t -v "//counter[@type='BRANCH']/@covered" -o "/" -v "//counter[@type='BRANCH']/@missed" "$jacoco_xml" 2>/dev/null | bc -l 2>/dev/null || echo "0")
    local method_coverage=$(xmlstarlet sel -t -v "//counter[@type='METHOD']/@covered" -o "/" -v "//counter[@type='METHOD']/@missed" "$jacoco_xml" 2>/dev/null | bc -l 2>/dev/null || echo "0")
    local class_coverage=$(xmlstarlet sel -t -v "//counter[@type='CLASS']/@covered" -o "/" -v "//counter[@type='CLASS']/@missed" "$jacoco_xml" 2>/dev/null | bc -l 2>/dev/null || echo "0")
    
    # 计算百分比
    line_coverage=$(echo "scale=2; $line_coverage * 100" | bc)
    branch_coverage=$(echo "scale=2; $branch_coverage * 100" | bc)
    method_coverage=$(echo "scale=2; $method_coverage * 100" | bc)
    class_coverage=$(echo "scale=2; $class_coverage * 100" | bc)
    
    # 显示覆盖率
    echo -e "\n${BLUE}📊 当前覆盖率:${NC}"
    echo "  行覆盖率:    $line_coverage%"
    echo "  分支覆盖率:  $branch_coverage%"
    echo "  方法覆盖率:  $method_coverage%"
    echo "  类覆盖率:    $class_coverage%"
    
    # 检查阈值
    local passed=true
    
    if (( $(echo "$line_coverage < $LINE_COVERAGE_THRESHOLD" | bc -l) )); then
        print_warning "行覆盖率低于阈值: $line_coverage% < ${LINE_COVERAGE_THRESHOLD}%"
        passed=false
    else
        print_success "行覆盖率达标: $line_coverage% >= ${LINE_COVERAGE_THRESHOLD}%"
    fi
    
    if (( $(echo "$branch_coverage < $BRANCH_COVERAGE_THRESHOLD" | bc -l) )); then
        print_warning "分支覆盖率低于阈值: $branch_coverage% < ${BRANCH_COVERAGE_THRESHOLD}%"
        passed=false
    else
        print_success "分支覆盖率达标: $branch_coverage% >= ${BRANCH_COVERAGE_THRESHOLD}%"
    fi
    
    if (( $(echo "$method_coverage < $METHOD_COVERAGE_THRESHOLD" | bc -l) )); then
        print_warning "方法覆盖率低于阈值: $method_coverage% < ${METHOD_COVERAGE_THRESHOLD}%"
        passed=false
    else
        print_success "方法覆盖率达标: $method_coverage% >= ${METHOD_COVERAGE_THRESHOLD}%"
    fi
    
    if (( $(echo "$class_coverage < $CLASS_COVERAGE_THRESHOLD" | bc -l) )); then
        print_warning "类覆盖率低于阈值: $class_coverage% < ${CLASS_COVERAGE_THRESHOLD}%"
        passed=false
    else
        print_success "类覆盖率达标: $class_coverage% >= ${CLASS_COVERAGE_THRESHOLD}%"
    fi
    
    if [ "$passed" = true ]; then
        print_success "所有覆盖率指标均达标！"
        return 0
    else
        print_error "部分覆盖率指标未达标"
        return 1
    fi
}

analyze_test_categories() {
    print_header "分析测试类别"
    
    local test_dir="src/test/java"
    
    if [ ! -d "$test_dir" ]; then
        print_warning "测试目录不存在: $test_dir"
        return
    fi
    
    # 统计各种测试类型
    local unit_tests=0
    local integration_tests=0
    local controller_tests=0
    local service_tests=0
    local repository_tests=0
    local exception_tests=0
    local boundary_tests=0
    
    # 查找Java测试文件
    while IFS= read -r file; do
        local filename=$(basename "$file")
        local content=$(cat "$file" 2>/dev/null || echo "")
        
        # 分类统计
        if [[ "$filename" == *IntegrationTest* ]] || [[ "$filename" == *IT.java ]]; then
            ((integration_tests++))
        elif [[ "$filename" == *ControllerTest* ]]; then
            ((controller_tests++))
        elif [[ "$filename" == *ServiceTest* ]]; then
            ((service_tests++))
        elif [[ "$filename" == *RepositoryTest* ]] || [[ "$filename" == *MapperTest* ]]; then
            ((repository_tests++))
        else
            ((unit_tests++))
        fi
        
        # 内容分析
        if [[ "$content" == *assertThrows* ]] || [[ "$content" == *Exception* ]]; then
            ((exception_tests++))
        fi
        
        if [[ "$content" == *boundary* ]] || [[ "$content" == *Boundary* ]]; then
            ((boundary_tests++))
        fi
        
    done < <(find "$test_dir" -name "*.java" -type f)
    
    # 显示统计结果
    echo -e "\n${BLUE}📋 测试类别统计:${NC}"
    echo "  单元测试:      $unit_tests"
    echo "  集成测试:      $integration_tests"
    echo "  Controller测试: $controller_tests"
    echo "  Service测试:    $service_tests"
    echo "  Repository测试: $repository_tests"
    echo "  异常测试:      $exception_tests"
    echo "  边界测试:      $boundary_tests"
    
    # 检查是否缺少重要测试类型
    if [ $controller_tests -eq 0 ]; then
        print_warning "缺少Controller层测试"
    fi
    
    if [ $service_tests -eq 0 ]; then
        print_warning "缺少Service层测试"
    fi
    
    if [ $repository_tests -eq 0 ]; then
        print_warning "缺少Repository/Mapper层测试"
    fi
    
    if [ $exception_tests -eq 0 ]; then
        print_warning "缺少异常处理测试"
    fi
    
    if [ $boundary_tests -eq 0 ]; then
        print_warning "缺少边界值测试"
    fi
}

check_test_quality() {
    print_header "检查测试质量"
    
    local issues=0
    
    # 检查测试命名规范
    echo "检查测试命名规范..."
    local bad_names=$(find src/test/java -name "*.java" -type f -exec grep -l "test[^A-Z]" {} \; 2>/dev/null || true)
    
    if [ -n "$bad_names" ]; then
        print_warning "发现不符合命名规范的测试文件:"
        echo "$bad_names" | while read -r file; do
            echo "  - $file"
        done
        ((issues++))
    else
        print_success "测试命名规范良好"
    fi
    
    # 检查测试方法长度
    echo "检查测试方法长度..."
    local long_methods=$(find src/test/java -name "*.java" -type f -exec awk '
        BEGIN { in_method=0; line_count=0; method_name="" }
        /@Test/ { in_method=1; line_count=0; method_name=""; next }
        /public void test/ && in_method==0 { 
            in_method=1; 
            line_count=0; 
            method_name=$0; 
            next 
        }
        in_method && /^\s*}[[:space:]]*$/ { 
            if (line_count > 50) {
                print FILENAME ":" method_name " - " line_count "行"
            }
            in_method=0; 
            line_count=0; 
            method_name=""; 
            next 
        }
        in_method { line_count++ }
    ' {} \; 2>/dev/null || true)
    
    if [ -n "$long_methods" ]; then
        print_warning "发现过长的测试方法:"
        echo "$long_methods" | head -5 | while read -r line; do
            echo "  - $line"
        done
        ((issues++))
    else
        print_success "测试方法长度合适"
    fi
    
    # 检查断言使用
    echo "检查断言使用..."
    local no_assertions=$(find src/test/java -name "*.java" -type f -exec grep -l "@Test" {} \; | xargs grep -L "assert\|verify\|expect" 2>/dev/null || true)
    
    if [ -n "$no_assertions" ]; then
        print_warning "发现没有断言的测试方法:"
        echo "$no_assertions" | while read -r file; do
            echo "  - $file"
        done
        ((issues++))
    else
        print_success "所有测试都有断言"
    fi
    
    if [ $issues -eq 0 ]; then
        print_success "测试质量检查通过"
    else
        print_warning "发现 $issues 个测试质量问题"
    fi
}

generate_summary() {
    print_header "测试覆盖率检查总结"
    
    echo -e "${BLUE}🏁 检查完成!${NC}"
    echo ""
    echo "📁 覆盖率报告位置:"
    echo "  - HTML报告: target/site/jacoco/index.html"
    echo "  - XML报告:  target/site/jacoco/jacoco.xml"
    echo ""
    echo "📈 覆盖率阈值:"
    echo "  - 行覆盖率:    ${LINE_COVERAGE_THRESHOLD}%"
    echo "  - 分支覆盖率:  ${BRANCH_COVERAGE_THRESHOLD}%"
    echo "  - 方法覆盖率:  ${METHOD_COVERAGE_THRESHOLD}%"
    echo "  - 类覆盖率:    ${CLASS_COVERAGE_THRESHOLD}%"
    echo ""
    echo "💡 建议:"
    echo "  1. 定期运行覆盖率检查"
    echo "  2. 添加缺失的测试类别"
    echo "  3. 优化测试代码质量"
    echo "  4. 集成到CI/CD流程"
}

main() {
    print_header "Spring Boot测试覆盖率检查"
    
    echo "项目: $(basename $(pwd))"
    echo "时间: $(date)"
    echo ""
    
    # 执行检查步骤
    check_prerequisites
    run_tests
    generate_coverage_report
    check_coverage_thresholds
    analyze_test_categories
    check_test_quality
    generate_summary
    
    print_header "✅ 检查完成"
}

# 执行主函数
main "$@"