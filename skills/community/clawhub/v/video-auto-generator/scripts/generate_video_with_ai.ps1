# generate_video_with_ai.ps1 - AI驱动的视频生成流水线
# 功能：AI生成脚本 → 自动配音+封面+合成
# 使用：.\generate_video_with_ai.ps1 -Topic "你的选题" -Duration 90

param(
    [string]$Topic = "ClawHub赚钱实战：我用AI做了5个技能",
    [int]$Duration = 90,
    [string]$Style = "review",  # review/tutorial/story
    [string]$Voice = "zh-CN-XiaoxiaoNeural",
    [string]$OutputDir = "$env:USERPROFILE\Desktop\video_output"
)

$ErrorActionPreference = "Stop"

Write-Host "`n🚀 AI视频生成流水线启动" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "📋 选题：$Topic"
Write-Host "⏱️  时长：$Duration 秒"
Write-Host "🎨 风格：$Style"
Write-Host "🎤 音色：$Voice"
Write-Host "============================================================`n" -ForegroundColor Cyan

# 创建输出目录
New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
Write-Host "📁 输出目录：$OutputDir`n"

# ========== 第1步：AI生成视频脚本 ==========
Write-Host "📝 第1步：AI生成视频脚本..." -ForegroundColor Yellow

$scriptPrompt = @"
请为以下选题生成一个$Duration秒的视频脚本（风格：$Style）：

选题：$Topic

要求：
1. 按时间轴分镜（每5-10秒一个镜头）
2. 每个镜头包含：画面描述、配音文案、字幕文本
3. 配音文案要口语化，适合TTS合成
4. 总字数控制在$($Duration * 4)字左右（每秒4字）
5. 输出格式为Markdown

示例格式：
### 镜头1（0-5秒）：开场
**画面**：...
**配音**：...
**字幕**：...
"@

# 保存prompt到文件，让AI填写（这里需要先让AI生成内容）
$scriptPath = Join-Path $OutputDir "script.md"

# 这里AI会生成脚本内容（通过QClaw的AI能力）
# 暂时先创建空文件，等待AI填充
$scriptPrompt | Out-File -FilePath "$OutputDir\script_prompt.txt" -Encoding utf8

Write-Host "   ✅ 脚本生成prompt已保存：$OutputDir\script_prompt.txt"
Write-Host "   ⏳ 等待AI生成脚本内容..." -ForegroundColor Yellow

# ========== 第2步：生成配音（需要先有脚本） ==========
# 这里先跳过，等AI生成脚本后再执行

Write-Host "`n⚠️  流水线暂停：需要AI先生成script.md内容" -ForegroundColor Red
Write-Host "请查看 $OutputDir\script_prompt.txt，让AI生成脚本后保存到 $scriptPath`n" -ForegroundColor Yellow

# 输出下一步指令
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "📌 下一步操作：" -ForegroundColor Green
Write-Host "1. 阅读 $OutputDir\script_prompt.txt"
Write-Host "2. 让AI生成完整的视频脚本"
Write-Host "3. 将脚本内容保存到 $scriptPath"
Write-Host "4. 运行第2步：配音生成`n"

# 生成第2步脚本
$step2Script = @"
# 第2步：生成配音 + 封面 + 合成视频
# 在 script.md 生成后运行此脚本

`$env:PYTHONIOENCODING = "utf-8"
`$env:PYTHONUTF8 = "1"

cd "$PSScriptRoot\skills\video-auto-generator\scripts"

# 从 script.md 提取配音文本
`$scriptContent = Get-Content "$OutputDir\script.md" -Encoding utf8 -Raw

# 提取所有**配音**：后面的内容
`$voiceText = (`$scriptContent | Select-String -Pattern "\*\*配音\*\*：(.+)" -AllMatches).Matches | 
    ForEach-Object { `$_.Groups[1].Value } | 
    Join-String -Separator "`n"

# 如果没有提取到，使用标题
if ([string]::IsNullOrWhiteSpace(`$voiceText)) {
    `$voiceText = "$Topic"
}

# 保存配音文本
`$voiceText | Out-File -FilePath "$OutputDir\voice_text.txt" -Encoding utf8

# 生成配音
python -m edge_tts --text "`$(Get-Content "$OutputDir\voice_text.txt" -Encoding utf8 -Raw)" --voice $Voice --write-media "$OutputDir\voice.mp3"

Write-Host "`n✅ 配音已生成：$OutputDir\voice.mp3`n"
"@

$step2Script | Out-File -FilePath "$OutputDir\step2_generate_voice.ps1" -Encoding utf8

Write-Host "✅ 第2步脚本已生成：$OutputDir\step2_generate_voice.ps1`n" -ForegroundColor Green
