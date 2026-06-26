#!/bin/bash
# vuln-analysis-hub 决策路由脚本
# 根据输入类型自动选择分析路径

INPUT="$1"

if [ -z "$INPUT" ]; then
  echo "用法: $0 <输入内容>"
  echo ""
  echo "输入类型自动判断:"
  echo "  CVE 编号      → 走 CVE 深度分析流程"
  echo "  二进制路径    → 走 IDA 逆向 + 静态分析流程"
  echo "  内核源码路径  → 走 kernel-vuln-discover 流程"
  echo "  故障描述      → 走 internet-failure-analysis-expert 流程"
  exit 1
fi

echo "[+] vuln-analysis-hub 输入路由"
echo ""

# 判断输入类型
if echo "$INPUT" | grep -qE "^CVE-\d{4}-\d{4,}"; then
  echo "[→] 检测为：CVE 编号 → cve-lookup"
  echo ""
  echo "执行流程:"
  echo "  1. cve-lookup: NVD/MITRE/GitHub Advisory 多源查询"
  echo "  2. internet-failure-analysis-expert: 时间线 + 根因 + 建议"
  echo "  3. 输出: CVE-Reports/CVE-YYYY-XXXX.md"

elif echo "$INPUT" | grep -qE "\.(exe|dll|so|elf|macho|apk|sys)$"; then
  echo "[→] 检测为：二进制文件 → ida-reverse + binary-exploitation-tools"
  echo ""
  echo "执行流程:"
  echo "  1. start.ps1: 启动 IDA HTTP 服务器"
  echo "  2. open.ps1: 打开二进制文件"
  echo "  3. ida-reverse: 概况 → 反编译 → 函数分析 → 漏洞定位"
  echo "  4. trailofbits-security: 静态分析（CodeQL/Semgrep）"
  echo "  5. binary-exploitation-tools: PoC 构建 + 偏移计算"
  echo "  6. 输出: 漏洞报告 + 概念性 PoC"

elif echo "$INPUT" | grep -qE "(kernel|linux|io_uring|netfilter|overlayfs|bpf)"; then
  echo "[→] 检测为：内核/驱动源码 → kernel-vuln-discover + kernel-cve-tracker"
  echo ""
  echo "执行流程:"
  echo "  1. kernel-cve-tracker: 批量查询已有 CVE"
  echo "  2. kernel-vuln-discover:"
  echo "     Phase 1: 攻击面枚举"
  echo "     Phase 2: CVE 模式扫描（8 种已知模式）"
  echo "     Phase 3: Fuzzing（syzkaller/trinity）"
  echo "     Phase 4: 静态审计（Coccinelle/semgrep）"
  echo "     Phase 5: PoC 生成 + 漏洞报告"
  echo "  3. trailofbits-security: CodeQL/Semgrep 驱动/内核审计"
  echo "  4. 输出: 漏洞发现报告 + PoC"

elif echo "$INPUT" | grep -qE "(故障|宕机|outage|incident|post-mortem|分析|事件)"; then
  echo "[→] 检测为：故障/事件描述 → internet-failure-analysis-expert"
  echo ""
  echo "执行流程:"
  echo "  1. 识别输入类型（CVE 模式 / 通用模式）"
  echo "  2. 获取官方故障报告"
  echo "  3. 拆解时间线 + 关键事件节点"
  echo "  4. 分析导火索 + 连环故障"
  echo "  5. 识别根本原因（人/组织因素）"
  echo "  6. 生成技术 + 管理改进建议"
  echo "  7. 输出: 完整故障分析报告"

else
  echo "[→] 无法明确判断类型，请用户提供更明确的信息："
  echo ""
  echo "支持的输入类型："
  echo "  • CVE 编号（如 CVE-2024-3094）"
  echo "  • 二进制文件路径（如 sample.exe、lib.so）"
  echo "  • 内核/驱动源码目录"
  echo "  • 故障描述（如 Facebook 宕机、阿里云故障）"
fi