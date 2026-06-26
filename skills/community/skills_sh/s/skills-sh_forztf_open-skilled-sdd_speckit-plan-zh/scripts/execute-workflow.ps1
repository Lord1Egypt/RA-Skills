<#
.SYNOPSIS
    执行完整的 Speckit 计划工作流程
.DESCRIPTION
    协调执行从设置到 Phase 1 完成的整个规划工作流程
.PARAMETER Arguments
    用户提供的参数
#>

param(
    [string]$Arguments = ""
)

# 错误处理设置
$ErrorActionPreference = "Stop"

Write-Host "开始执行 Speckit 计划工作流程..." -ForegroundColor Cyan

try {
    # Phase 0: 设置
    Write-Host "`n=== Phase 0: 环境设置 ===" -ForegroundColor Yellow

    $SetupResult = & (Join-Path $PSScriptRoot "setup-plan.ps1") -Json
    $Config = $SetupResult | ConvertFrom-Json

    Write-Host "✓ 环境设置完成" -ForegroundColor Green

    # 加载上下文
    Write-Host "`n=== 加载项目上下文 ===" -ForegroundColor Yellow

    if (-not (Test-Path $Config.FEATURE_SPEC)) {
        throw "功能规范文件不存在: $($Config.FEATURE_SPEC)"
    }

    $FeatureSpecContent = Get-Content $Config.FEATURE_SPEC -Raw

    # 检查章程文件
    $ConstitutionPath = Join-Path (Split-Path $Config.FEATURE_SPEC) "memory" "constitution.md"
    if (Test-Path $ConstitutionPath) {
        $ConstitutionContent = Get-Content $ConstitutionPath -Raw
        Write-Host "✓ 章程文件已加载" -ForegroundColor Green
    } else {
        Write-Host "⚠ 未找到章程文件，跳过章程检查" -ForegroundColor Yellow
        $ConstitutionContent = ""
    }

    # Phase 1: 研究阶段
    Write-Host "`n=== Phase 1: 研究和分析 ===" -ForegroundColor Yellow

    # 这里应该调用研究代理或执行研究逻辑
    # 当前版本模拟研究过程

    $ResearchOutputPath = Join-Path $Config.SPECS_DIR "research.md"
    $ResearchContent = @"
# 研究结果

## 决策记录

### 技术选择
基于功能需求分析，确定了以下技术方案：

**决策**: 使用现代技术栈
**理由**: 满足功能需求并保证可维护性
**考虑的替代方案**: 传统方案、新兴方案

## 待澄清项目

以下项目需要进一步澄清：
- [ ] 具体的性能要求
- [ ] 部署环境限制
- [ ] 安全性标准

*生成时间: $(Get-Date)*
"@

    Set-Content -Path $ResearchOutputPath -Value $ResearchContent -Encoding UTF8
    Write-Host "✓ 研究文档已生成: $ResearchOutputPath" -ForegroundColor Green

    # Phase 2: 设计阶段
    Write-Host "`n=== Phase 2: 设计和契约 ===" -ForegroundColor Yellow

    # 创建 contracts 目录
    $ContractsDir = Join-Path $Config.SPECS_DIR "contracts"
    if (-not (Test-Path $ContractsDir)) {
        New-Item -ItemType Directory -Path $ContractsDir -Force | Out-Null
    }

    # 生成数据模型
    $DataModelPath = Join-Path $Config.SPECS_DIR "data-model.md"
    $DataModelContent = @"
# 数据模型

## 实体定义

### 核心实体
- **Entity1**: 主要业务实体
  - id: 唯一标识符
  - name: 名称
  - created_at: 创建时间
  - updated_at: 更新时间

### 关系
- Entity1 与其他实体的关系图

## 验证规则
- 名称必填
- 唯一性约束

*生成时间: $(Get-Date)*
"@

    Set-Content -Path $DataModelPath -Value $DataModelContent -Encoding UTF8
    Write-Host "✓ 数据模型已生成: $DataModelPath" -ForegroundColor Green

    # 生成 API 契约示例
    $ApiContractPath = Join-Path $ContractsDir "api.yaml"
    $ApiContractContent = @"
openapi: 3.0.0
info:
  title: API 规范
  version: 1.0.0

paths:
  /entities:
    get:
      summary: 获取实体列表
      responses:
        '200':
          description: 成功返回列表

    post:
      summary: 创建新实体
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
"@

    Set-Content -Path $ApiContractPath -Value $ApiContractContent -Encoding UTF8
    Write-Host "✓ API 契约已生成: $ApiContractPath" -ForegroundColor Green

    # 生成快速开始指南
    $QuickstartPath = Join-Path $Config.SPECS_DIR "quickstart.md"
    $QuickstartContent = @"
# 快速开始指南

## 项目概述
基于功能规范生成的实施项目。

## 环境要求
- PowerShell 5.1+
- Git
- 相关开发工具

## 开发流程
1. 查看研究文档 (research.md)
2. 理解数据模型 (data-model.md)
3. 参考 API 契约 (/contracts/)
4. 开始实施开发

## 下一步
- 设置开发环境
- 创建初始代码结构
- 实施核心功能

*生成时间: $(Get-Date)*
"@

    Set-Content -Path $QuickstartPath -Value $QuickstartContent -Encoding UTF8
    Write-Host "✓ 快速开始指南已生成: $QuickstartPath" -ForegroundColor Green

    # 更新代理上下文
    Write-Host "`n=== 更新代理上下文 ===" -ForegroundColor Yellow

    & (Join-Path $PSScriptRoot "update-agent-context.ps1") -AgentType claude
    Write-Host "✓ 代理上下文已更新" -ForegroundColor Green

    # 报告完成
    Write-Host "`n=== 工作流程完成 ===" -ForegroundColor Green
    Write-Host "分支: $($Config.BRANCH)" -ForegroundColor White
    Write-Host "规范目录: $($Config.SPECS_DIR)" -ForegroundColor White
    Write-Host "生成的工作件:" -ForegroundColor White
    Write-Host "  - research.md" -ForegroundColor Gray
    Write-Host "  - data-model.md" -ForegroundColor Gray
    Write-Host "  - /contracts/api.yaml" -ForegroundColor Gray
    Write-Host "  - quickstart.md" -ForegroundColor Gray

    Write-Host "`n✅ Speckit 计划工作流程执行完成！" -ForegroundColor Green

} catch {
    Write-Host "`n❌ 工作流程执行失败:" -ForegroundColor Red
    Write-Host $Error[0].Exception.Message -ForegroundColor Red
    exit 1
}