# 翻译引擎模板

## 新增翻译引擎步骤

```python
# 1. 在 config.py 的 CLOUD_MODELS 中添加配置
"新模型名称": {
    "base_url": "https://api.xxx.com/v1",
    "model": "model-name",
    "env_key": "XXX_API_KEY"
}

# 2. 在 translator.py 的 TranslatorModule 中实现
elif self.engine == "new_engine":
    try:
        response = new_engine_client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": text}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"    [新引擎错误] {e}")
        return text
```

## 引擎配置要求

- 必须支持 OpenAI 兼容的 chat.completions 接口
- 或使用独立 SDK 封装为统一接口
- 错误处理必须返回原文作为 fallback
