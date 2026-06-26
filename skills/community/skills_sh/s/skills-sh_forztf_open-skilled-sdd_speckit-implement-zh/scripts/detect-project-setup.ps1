# 项目设置检测脚本
function Test-IsGitRepo {
    $result = git rev-parse --git-dir 2>$null
    return $LASTEXITCODE -eq 0
}

function Test-DockerExists {
    return (Test-Path "Dockerfile*") -or (Test-Path "*.dockerfile")
}

function Test-EslintExists {
    return (Test-Path ".eslintrc*") -or (Test-Path "eslint.config.*")
}

function Test-PrettierExists {
    return (Test-Path ".prettierrc*")
}

function Test-NpmExists {
    return (Test-Path ".npmrc") -or (Test-Path "package.json")
}

function Test-TerraformExists {
    return (Test-Path "*.tf")
}

function Test-HelmExists {
    return (Test-Path "Chart.yaml") -or (Test-Path "charts/**")
}

function Get-TechStackFromPlan {
    if (-not (Test-Path "plan.md")) {
        return @()
    }

    $planContent = Get-Content "plan.md" -Raw

    $techStack = @()
    if ($planContent -match "node|javascript|typescript|npm|yarn") {
        $techStack += "Node.js"
    }
    if ($planContent -match "python|pip|conda|virtualenv") {
        $techStack += "Python"
    }
    if ($planContent -match "java|maven|gradle") {
        $techStack += "Java"
    }
    if ($planContent -match "c#|\.net|dotnet") {
        $techStack += "C#"
    }
    if ($planContent -match "golang|go") {
        $techStack += "Go"
    }
    if ($planContent -match "ruby|rails|bundler") {
        $techStack += "Ruby"
    }
    if ($planContent -match "php|composer") {
        $techStack += "PHP"
    }
    if ($planContent -match "rust|cargo") {
        $techStack += "Rust"
    }
    if ($planContent -match "kotlin") {
        $techStack += "Kotlin"
    }
    if ($planContent -match "c\+\+") {
        $techStack += "C++"
    }
    if ($planContent -match "c[^+]|gcc|clang") {
        $techStack += "C"
    }
    if ($planContent -match "swift") {
        $techStack += "Swift"
    }
    if ($planContent -match "r|cran") {
        $techStack += "R"
    }

    return $techStack
}

# 主检测逻辑
$projectSetup = @{
    IsGitRepo = Test-IsGitRepo
    HasDocker = Test-DockerExists
    HasEslint = Test-EslintExists
    HasPrettier = Test-PrettierExists
    HasNpm = Test-NpmExists
    HasTerraform = Test-TerraformExists
    HasHelm = Test-HelmExists
    TechStack = Get-TechStackFromPlan
}

# 输出 JSON 结果
$projectSetup | ConvertTo-Json -Depth 10