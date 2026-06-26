# Call AIDA App - 使用示例

## 目录

1. [基础使用](#基础使用)
2. [与 OpenClaw Agent 集成](#与-openclaw-agent-集成)
3. [错误处理示例](#错误处理示例)
4. [高级用法](#高级用法)

## 基础使用

### 示例 1：最简单的调用

```bash
# 通过命令行参数
python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py \
  --appid "your-app-id" \
  --inputs '{"question": "Hello"}'
```

**响应示例：**
```json
{
  "success": true,
  "message": "调用成功",
  "data": {
    "answer": "你好！有什么我可以帮助的吗？"
  },
  "raw_answer": "{\"answer\": \"你好！有什么我可以帮助的吗？\"}"
}
```

### 示例 2：带查询的调用

```bash
python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py \
  --appid "my-app-123" \
  --query "Please analyze this code" \
  --inputs '{"code": "print(\"Hello World\")"}'
```

### 示例 3：通过 stdin 调用（推荐）

```bash
cat << 'EOF' | python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py
{
  "appid": "doc-processor",
  "query": "Please summarize",
  "inputs": {
    "document": "这是一份关于 AI 的文档...",
    "language": "zh-CN"
  }
}
EOF
```

### 示例 4：使用环境变量

```bash
# 设置环境变量
export AIDA_APPID="text-classifier"
export AIDA_INPUTS='{"text": "This product is amazing!", "task": "sentiment"}'
export AIDA_QUERY="Classify sentiment"
export AIDA_USER="user@example.com"

# 调用脚本
python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py
```

## 与 OpenClaw Agent 集成

### 在 Agent 任务中使用

假设你有一个 OpenClaw Agent，需要调用 AI 搭应用来处理用户输入：

```yaml
# agent-config.yaml
agents:
  - name: "document-analyzer"
    description: "文档分析 Agent"
    tools:
      - type: "external"
        name: "call_aida_app"
        command: "python3"
        args: ["~/.openclaw/skills/call-aida-app/call_aida_app.py"]
        input_mode: "stdin"  # 使用 stdin 传入参数
```

### Agent 中的脚本片段

```python
import json
import subprocess

def call_aida_from_agent(appid: str, inputs: dict, query: str = ""):
    """
    从 Agent 中调用 AIDA 技能

    Args:
        appid: AIDA 应用 ID
        inputs: 输入参数
        query: 可选的查询文本

    Returns:
        解析后的响应数据
    """
    payload = {
        "appid": appid,
        "inputs": inputs,
        "query": query
    }

    result = subprocess.run(
        ["python3", "~/.openclaw/skills/call-aida-app/call_aida_app.py"],
        input=json.dumps(payload),
        capture_output=True,
        text=True
    )

    response = json.loads(result.stdout)
    if response["success"]:
        return response["data"]
    else:
        raise Exception(f"AIDA 调用失败: {response['message']}")

# 使用示例
try:
    result = call_aida_from_agent(
        appid="document-qa",
        inputs={"document": "...", "question": "What is...?"},
        query="Answer the question"
    )
    print(result)
except Exception as e:
    print(f"错误: {e}")
```

## 错误处理示例

### 示例 1：处理参数缺失

```bash
$ python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py

# 输出
{
  "success": false,
  "message": "缺少必要参数。请通过以下方式之一传入：\n1. stdin JSON: ...\n2. 命令行: ...\n3. 环境变量: ...",
  "data": null
}
```

### 示例 2：处理 HTTP 错误

```bash
$ python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py \
  --appid "invalid-app" \
  --inputs '{}'

# 输出
{
  "success": false,
  "message": "HTTP 错误 401: Server Error",
  "data": {
    "status_code": 401,
    "error_body": "{\"code\":\"invalid param\",\"message\":\"API密钥校验失败\"}"
  }
}
```

### 示例 3：Python 中的错误处理

```python
import json
import subprocess

def safe_call_aida(appid: str, inputs: dict):
    """安全的 AIDA 调用，包含完整的错误处理"""
    try:
        payload = {"appid": appid, "inputs": inputs}

        result = subprocess.run(
            ["python3", "~/.openclaw/skills/call-aida-app/call_aida_app.py"],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=130  # 比脚本的 120 秒稍长
        )

        response = json.loads(result.stdout)

        if not response["success"]:
            error_msg = response.get("message", "未知错误")
            error_data = response.get("data", {})

            if isinstance(error_data, dict):
                status_code = error_data.get("status_code")
                if status_code == 401:
                    print("认证失败，检查 appid")
                elif status_code == 500:
                    print("服务端错误")
                    print(f"详情: {error_data.get('error_body')}")

            return None, error_msg

        return response.get("data"), None

    except subprocess.TimeoutExpired:
        return None, "脚本执行超时"
    except json.JSONDecodeError:
        return None, "响应格式不是有效 JSON"
    except Exception as e:
        return None, f"未预期的错误: {str(e)}"

# 使用
data, error = safe_call_aida("my-app", {"key": "value"})
if error:
    print(f"调用失败: {error}")
else:
    print(f"调用成功: {data}")
```

## 高级用法

### 示例 1：链式调用

将一个应用的输出作为另一个应用的输入：

```bash
#!/bin/bash

# 第一步：使用应用1进行文本预处理
RESULT1=$(python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py \
  --appid "text-preprocessor" \
  --inputs '{"text": "原始文本"}')

# 提取结果
PROCESSED=$(echo "$RESULT1" | jq -r '.data.processed_text')

# 第二步：使用应用2进行分析
RESULT2=$(python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py \
  --appid "text-analyzer" \
  --inputs "{\"text\": \"$PROCESSED\"}")

echo "$RESULT2" | jq '.'
```

### 示例 2：批量处理

```bash
#!/bin/bash

# 批量处理多个文档
DOCUMENTS=("doc1" "doc2" "doc3")

for doc in "${DOCUMENTS[@]}"; do
    echo "处理 $doc..."

    RESULT=$(python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py \
      --appid "batch-processor" \
      --inputs "{\"document_id\": \"$doc\"}")

    # 检查是否成功
    if echo "$RESULT" | jq -e '.success' > /dev/null; then
        echo "✓ $doc 处理成功"
        echo "$RESULT" | jq '.data' >> output.jsonl
    else
        echo "✗ $doc 处理失败"
        echo "$RESULT" | jq '.message' >> errors.log
    fi
done
```

### 示例 3：条件调用

```bash
#!/bin/bash

# 根据输入类型选择不同的应用
detect_and_process() {
    local input_type=$1
    local content=$2

    case $input_type in
        "text")
            APP_ID="text-processor"
            ;;
        "code")
            APP_ID="code-analyzer"
            ;;
        "image")
            APP_ID="image-processor"
            ;;
        *)
            echo "未知类型: $input_type"
            return 1
            ;;
    esac

    python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py \
      --appid "$APP_ID" \
      --inputs "{\"content\": \"$content\", \"type\": \"$input_type\"}"
}

# 使用
detect_and_process "text" "这是一些文本"
```

### 示例 4：与 jq 结合进行数据处理

```bash
# 调用应用并使用 jq 提取特定字段
python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py \
  --appid "data-extractor" \
  --inputs '{"source": "webpage"}' | \
  jq '{
    success: .success,
    message: .message,
    result: .data.extracted_data,
    confidence: .data.confidence
  }'

# 如果成功，只输出数据部分
python3 ~/.openclaw/skills/call-aida-app/call_aida_app.py \
  --appid "my-app" \
  --inputs '{}' | \
  jq 'if .success then .data else empty end'
```

### 示例 5：日志记录和监控

```python
import json
import subprocess
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    filename='aida_calls.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def logged_call_aida(appid: str, inputs: dict, user: str = ""):
    """带日志的 AIDA 调用"""
    start_time = datetime.now()

    payload = {
        "appid": appid,
        "inputs": inputs,
        "user": user or "default"
    }

    try:
        result = subprocess.run(
            ["python3", "~/.openclaw/skills/call-aida-app/call_aida_app.py"],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=130
        )

        response = json.loads(result.stdout)
        duration = (datetime.now() - start_time).total_seconds()

        # 记录调用
        logging.info(
            f"AIDA 调用 - appid={appid}, "
            f"success={response['success']}, "
            f"duration={duration}s, "
            f"message={response['message']}"
        )

        return response

    except Exception as e:
        logging.error(f"AIDA 调用异常 - appid={appid}, error={str(e)}")
        raise

# 使用
result = logged_call_aida("my-app", {"key": "value"}, "user@example.com")
```

## 总结

这个技能提供了灵活的方式来调用 AI 搭应用。根据你的使用场景选择合适的调用方式：

- **stdin 方式**：最灵活，推荐用于 OpenClaw 集成
- **命令行参数**：快速测试和简单脚本
- **环境变量**：适合 CI/CD 流程
- **Python 集成**：复杂逻辑和错误处理

需要帮助？查看 `SKILL.md` 获取完整文档。

