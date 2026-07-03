<#
Tavily Search 工具脚本
#>

param(
    [Parameter(Position=0)]
    [string]$Command,
    [Parameter(Position=1)]
    [string]$Query,
    [string]$ApiKey,
    [int]$MaxResults = 5,
    [int]$MaxPages = 10,
    [int]$Count = 5,
    [string]$Format = "text",
    [string]$SearchDepth = "basic",
    [switch]$IncludeImages,
    [switch]$IncludeRawContent
)

$configPath = Join-Path $PSScriptRoot "config.json"

# 配置API密钥
if ($Command -eq "config") {
    if (-not $ApiKey) {
        Write-Host "❌ 请提供API密钥: tavily config --api-key tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" -ForegroundColor Red
        exit 1
    }
    $config = @{ api_key = $ApiKey }
    $config | ConvertTo-Json | Out-File $configPath -Encoding utf8
    Write-Host "✅ API密钥已保存到: $configPath" -ForegroundColor Green
    exit 0
}

# 检查配置
if (-not (Test-Path $configPath)) {
    Write-Host "❌ 未配置API密钥，请先执行: tavily config --api-key <your-tavily-api-key>" -ForegroundColor Red
    Write-Host "ℹ️  密钥可以在 https://tavily.com/ 免费申请"
    exit 1
}
$config = Get-Content $configPath | ConvertFrom-Json
$apiKey = $config.api_key
$apiUrl = "https://api.tavily.com/search"

# 搜索功能
if ($Command -eq "search" -or $Command -eq "research" -or $Command -eq "image") {
    if (-not $Query) {
        Write-Host "❌ 请提供搜索关键词: tavily search <关键词>" -ForegroundColor Red
        exit 1
    }

    $body = @{
        api_key = $apiKey
        query = $Query
        max_results = $MaxResults
        search_depth = if ($Command -eq "research") { "advanced" } else { $SearchDepth }
        include_answer = $true
        include_images = if ($Command -eq "image" -or $IncludeImages) { $true } else { $false }
        include_raw_content = $IncludeRawContent
    }

    try {
        Write-Host "🔍 正在搜索: $Query..." -ForegroundColor Cyan
        $response = Invoke-WebRequest -Uri $apiUrl -Method Post -Body ($body | ConvertTo-Json) -ContentType "application/json" -ErrorAction Stop
        $result = $response.Content | ConvertFrom-Json

        if ($Format -eq "json") {
            Write-Output $result | ConvertTo-Json -Depth 10
            exit 0
        }

        # 文本格式输出
        Write-Host "`n📝 搜索结果: " -ForegroundColor Green
        Write-Host "----------------------------------------"
        Write-Host "💡 答案: $($result.answer)`n"

        if ($Command -eq "image" -and $result.images) {
            Write-Host "🖼️  相关图片: " -ForegroundColor Green
            for ($i=0; $i -lt [Math]::Min($Count, $result.images.Count); $i++) {
                Write-Host "   $($i+1). $($result.images[$i])"
            }
            Write-Host ""
        }

        Write-Host "📄 来源详情: " -ForegroundColor Green
        for ($i=0; $i -lt $result.results.Count; $i++) {
            $item = $result.results[$i]
            Write-Host "   $($i+1). $($item.title)"
            Write-Host "      🔗 $($item.url)"
            $pubDate = if ($item.published_date) { $item.published_date } else { "未知" }
            Write-Host "      📅 $pubDate"
            $contentPreview = $item.content.Substring(0, [Math]::Min(150, $item.content.Length))
            Write-Host "      💬 $contentPreview...`n"
        }

        Write-Host "⏱️  响应时间: $($result.response_time)s"
    }
    catch {
        Write-Host "❌ 搜索失败: $_" -ForegroundColor Red
        exit 1
    }
    exit 0
}

# 帮助信息
Write-Host "Tavily Search v1.0.0" -ForegroundColor Cyan
Write-Host "用法: tavily <命令> [参数]`n"
Write-Host "命令列表:"
Write-Host "  config    配置API密钥: tavily config --api-key <your-api-key>"
Write-Host "  search    基础搜索: tavily search <关键词> [--max-results 5] [--format text/json]"
Write-Host "  research  深度研究: tavily research <关键词> [--max-pages 10]"
Write-Host "  image     图片搜索: tavily image <关键词> [--count 5]`n"
Write-Host "示例:"
Write-Host "  tavily search '2026年AI最新进展'"
Write-Host "  tavily research '企业AI安全建设方案'"
Write-Host "  tavily image 'AI硬件产品' --count 10"
