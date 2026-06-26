import os
import time
import json
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
from translate import Translator as PyTranslator
import ollama
from config_loader import CONFIG
from crypto_utils import crypto


class PerformanceMonitor:
    """性能监控器 - 统计翻译速度和效率"""
    
    def __init__(self):
        self.start_time = None
        self.total_chars = 0
        self.total_batches = 0
        self.failed_batches = 0
    
    def start(self):
        self.start_time = time.time()
    
    def record_batch(self, char_count, success=True):
        self.total_chars += char_count
        self.total_batches += 1
        if not success:
            self.failed_batches += 1
    
    def report(self):
        elapsed = time.time() - self.start_time if self.start_time else 0
        speed = self.total_chars / elapsed if elapsed > 0 else 0
        print(f"\n    [性能统计] 总字符:{self.total_chars}, 批次:{self.total_batches}, "
              f"耗时:{elapsed:.1f}s, 速度:{speed:.0f}字符/秒")


class BatchOptimizer:
    """智能批次优化器 - 根据文件大小和文本长度自动优化批次参数"""
    
    @staticmethod
    def get_optimal_batch_config(engine, total_items, avg_length=100):
        """
        获取最优批次配置
        
        Args:
            engine: 引擎类型 (cloud/ollama/python)
            total_items: 总文本段数
            avg_length: 平均文本长度
            
        Returns:
            dict: 优化后的批次配置
        """
        opt_cfg = CONFIG.get("BATCH_OPTIMIZATION", {})
        batch_config = CONFIG.get("BATCH_CONFIG", {})
        
        # 调试信息
        if engine == "cloud":
            print(f"    [调试] BATCH_CONFIG keys: {list(batch_config.keys())}")
            print(f"    [调试] cloud config exists: {'cloud' in batch_config}")
            if 'cloud' in batch_config:
                print(f"    [调试] cloud config: {batch_config['cloud']}")
        
        base_cfg = batch_config.get(engine, {"max_len": 10000, "max_count": 10, "concurrent": 1})
        
        if not opt_cfg.get("enabled", True):
            return base_cfg
        
        max_len = base_cfg.get("max_len", 10000)
        max_count = base_cfg.get("max_count", 10)
        concurrent = base_cfg.get("concurrent", 1)
        adaptive = base_cfg.get("adaptive", False)
        
        # 自适应分段：根据平均文本长度调整
        if adaptive and avg_length > 0:
            # 如果单条文本很长，减少批次数量
            if avg_length > 500:
                max_count = max(1, max_count // 2)
                max_len = min(max_len, 5000)  # 增加上限到5000
            # 如果单条文本很短，可以增加批次
            elif avg_length < 100:
                max_count = min(max_count + 2, 20)  # 增加上限
        
        # 根据文件大小动态调整
        if opt_cfg.get("auto_adjust", True):
            small_threshold = opt_cfg.get("small_file_threshold", 50)
            large_threshold = opt_cfg.get("large_file_threshold", 500)
            
            if total_items <= small_threshold:
                # 小文件：增大批次，减少请求次数
                max_count = min(max_count + 10, 100)  # 允许更大批次
            elif total_items >= large_threshold:
                # 大文件：适度减小批次，提高稳定性
                max_count = max(max_count // 2, 5)
        
        return {
            "max_len": max_len,
            "max_count": max_count,
            "concurrent": concurrent
        }

class TranslatorModule:
    def __init__(self, engine="cloud", source_lang='auto', target_lang='zh-CN', keywords=None):
        self.engine = engine
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.keywords = keywords or []
        
        # 初始化不同引擎
        if self.engine == "cloud":
            # 动态从配置库获取当前模型信息
            current_model_name = CONFIG.get("CURRENT_CLOUD_MODEL", "DeepSeek (V3/R1)")
            model_info = CONFIG.get("CLOUD_MODELS", {}).get(current_model_name, CONFIG["CLOUD_MODELS"]["DeepSeek (V3/R1)"])
            
            # 尝试获取对应环境变量的 Key
            env_key_name = model_info.get("env_key", "DEEPSEEK_API_KEY")
            raw_key = os.getenv(env_key_name, CONFIG.get("DEEPSEEK_API_KEY", ""))
            
            # 解密 API Key
            api_key = crypto.decrypt(raw_key)
            
            if not api_key:
                raise ValueError("MISSING_API_KEY")
            
            self.client = OpenAI(
                api_key=api_key,
                base_url=model_info.get("base_url", "https://api.deepseek.com")
            )
            self.model = model_info.get("model", "deepseek-chat")
            
        elif self.engine == "python":
            # 这里的 translate 库不支持多线程批量请求，速度较慢
            self.py_translator = PyTranslator(to_lang=target_lang, from_lang=source_lang if source_lang != 'auto' else 'en')

        elif self.engine == "ollama":
            self.ollama_model = CONFIG.get("OLLAMA_MODEL", "llama3")

    def _get_system_prompt(self):
        system_prompt = f"You are a professional translator. Translate the following text into {self.target_lang}. Keep the original formatting."
        if self.source_lang != "auto":
            system_prompt += f" The source language is {self.source_lang}."
            
        # 增加关键词引导
        if self.keywords:
            terms = ", ".join(self.keywords)
            system_prompt += f" The text is about these key terms: {terms}. Use accurate professional terminology."
            
        return system_prompt

    def translate_text(self, text):
        """翻译单段文本"""
        if not text.strip():
            return ""
        
        if self.engine == "cloud":
            try:
                # 简化提示词，直接翻译
                prompt = f"Translate the following text into {self.target_lang}. Return translation only:\n\n{text}"
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a professional translator. Output translation only, no explanations."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=8192,
                    stream=False
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"    [API 错误] {e}")
                return text

        elif self.engine == "ollama":
            try:
                # 获取 Ollama 的 max_tokens 配置
                ollama_cfg = CONFIG.get("BATCH_CONFIG", {}).get("ollama", {})
                max_tokens = ollama_cfg.get("max_tokens", 10000)
                
                # Ollama 调用选项：关闭推理能力，提高翻译速度
                options = {
                    "temperature": 0.3,           # 适中温度，平衡准确性和创造性
                    "num_predict": max_tokens,    # 限制输出token数
                    "top_p": 0.5,                 # 降低采样多样性
                    "top_k": 10,                  # 限制候选词数量
                }
                
                # 针对 qwen3 模型，添加禁用推理的参数
                if "qwen" in self.ollama_model.lower():
                    # 在提示词中明确禁止推理
                    modified_prompt = text + "\n\n[要求：直接翻译，不要解释，不要推理，只输出译文]"
                else:
                    modified_prompt = text
                
                response = ollama.chat(
                    model=self.ollama_model,
                    messages=[
                        {"role": "system", "content": self._get_system_prompt()},
                        {"role": "user", "content": modified_prompt}
                    ],
                    options=options
                )
                return response['message']['content'].strip()
            except Exception as e:
                print(f"    [Ollama 错误] {e}")
                return text

        elif self.engine == "python":
            try:
                return self.py_translator.translate(text)
            except Exception as e:
                print(f"    [Python 翻译错误] {e}")
                return text

    def translate_list(self, text_list):
        """批量翻译文本列表（智能优化+并发处理：根据文件大小和模型能力自动优化批次）"""
        if not text_list:
            return []

        # 过滤空行并记录原始索引，以便之后还原
        indexed_texts = [(i, text) for i, text in enumerate(text_list) if text.strip()]
        if not indexed_texts:
            return [""] * len(text_list)

        results = [""] * len(text_list)
        total_items = len(indexed_texts)
        
        # 计算平均文本长度
        avg_length = sum(len(text) for _, text in indexed_texts) // total_items if total_items > 0 else 100
        
        # 使用智能批次优化器获取最优配置
        batch_cfg = BatchOptimizer.get_optimal_batch_config(self.engine, total_items, avg_length)
        MAX_LEN = batch_cfg.get("max_len", 10000)
        MAX_COUNT = batch_cfg.get("max_count", 10)
        CONCURRENT = batch_cfg.get("concurrent", 1)
        
        # 性能监控
        monitor = PerformanceMonitor()
        monitor.start()
        
        if CONFIG.get("VERBOSE_OUTPUT", True):
            print(f"    [批次优化] 总段数:{total_items}, 批次大小:{MAX_COUNT}, 并发:{CONCURRENT}")
            print(f"    [配置详情] MAX_LEN={MAX_LEN}, MAX_COUNT={MAX_COUNT}")
        
        # 批处理逻辑仅适用于 AI 模型
        if self.engine in ["cloud", "ollama"]:
            # 1. 构建批次
            batches = []
            batch = []
            batch_indices = []
            current_len = 0

            for idx, text in indexed_texts:
                text_len = len(text)
                # 更合理的批次判断：考虑JSON格式的开销
                estimated_size = current_len + text_len + len(text) // 10  # 估算10%的格式开销
                if estimated_size > MAX_LEN or len(batch) >= MAX_COUNT:
                    if batch:  # 确保不添加空批次
                        batches.append((batch, batch_indices))
                    batch = []
                    batch_indices = []
                    current_len = 0
                
                batch.append(text)
                batch_indices.append(idx)
                current_len += text_len

            if batch:
                batches.append((batch, batch_indices))

            total_batches = len(batches)
            progress_interval = CONFIG.get("BATCH_OPTIMIZATION", {}).get("progress_interval", 10)
            
            # 2. 串行处理所有批次（简化逻辑，避免并发问题）
            for batch_idx, (b, b_idx) in enumerate(batches):
                batch_num = batch_idx + 1
                
                # 显示详细进度
                if CONFIG.get("VERBOSE_OUTPUT", True) or batch_num == 1 or batch_num == total_batches:
                    print(f"    [进度] {batch_num}/{total_batches} 批 ({len(b)}条, {sum(len(t) for t in b)}字符)")
                
                start_time = time.time()
                _, translated_parts, char_count, success = self._process_single_batch(
                    b, b_idx, batch_num, total_batches, progress_interval
                )
                elapsed = time.time() - start_time
                monitor.record_batch(char_count, success)
                
                if translated_parts and len(translated_parts) == len(b_idx):
                    # 批次成功，写入结果
                    for i, part in zip(b_idx, translated_parts):
                        results[i] = part
                    if CONFIG.get("VERBOSE_OUTPUT", True):
                        print(f"    [成功] {elapsed:.1f}s, {char_count/elapsed:.0f}字符/秒")
                else:
                    # 批次失败，逐个翻译
                    print(f"    [降级] 批次失败，逐条翻译 {len(b)} 条...")
                    fail_start = time.time()
                    for i, text in zip(b_idx, b):
                        results[i] = self.translate_text(text)
                    fail_elapsed = time.time() - fail_start
                    print(f"    [完成] 逐条翻译 {len(b)} 条, {fail_elapsed:.1f}s")
            
            monitor.report()
        else:
            # Python 内置引擎，只能逐条处理
            total = len(indexed_texts)
            for idx, (i, text) in enumerate(indexed_texts):
                if CONFIG.get("VERBOSE_OUTPUT", True):
                    print(f"    [进度] {idx+1}/{total}")
                results[i] = self.translate_text(text)

        return results
    
    def _process_single_batch(self, b, b_idx, batch_num, total_batches, progress_interval):
        """处理单个批次，返回 (b_idx, translated_parts, char_count, success)"""
        # 显示进度
        if batch_num == 1 or batch_num % progress_interval == 0 or batch_num == total_batches:
            if CONFIG.get("VERBOSE_OUTPUT", True):
                print(f"    [进度] {batch_num}/{total_batches}")
        
        char_count = sum(len(text) for text in b)
        separator = "###BATCH_SEP###"
        combined_text = f"\n{separator}\n".join(b)
        
        prompt = (
            f"Translate the following {len(b)} texts into {self.target_lang}. "
            f"Maintain the separator '{separator}' between each part exactly. "
            "Do not add any other text or explanation. Return the translations only.\n\n"
            f"{combined_text}"
        )

        try:
            if self.engine == "cloud":
                # 使用 JSON 格式批量翻译
                json_prompt = (
                    f"You are a professional translator. Translate into {self.target_lang}.\n"
                    f"Return ONLY a JSON array of translations, no explanations.\n\n"
                    f"{json.dumps(b, ensure_ascii=False, indent=2)}"
                )
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "Output JSON array only. No markdown, no explanations."},
                        {"role": "user", "content": json_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=8192
                )
                
                # 解析 JSON 响应
                content = response.choices[0].message.content.strip()
                # 移除可能的 markdown 代码块标记
                if content.startswith("```json"):
                    content = content[7:]
                if content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()
                
                translated_list = json.loads(content)
                if isinstance(translated_list, list) and len(translated_list) == len(b):
                    return (b_idx, translated_list, char_count, True)
                else:
                    return (b_idx, None, char_count, False)
                    
            else: # ollama
                # 获取 Ollama 的 max_tokens 配置
                ollama_cfg = CONFIG.get("BATCH_CONFIG", {}).get("ollama", {})
                max_tokens = ollama_cfg.get("max_tokens", 10000)
                
                # Ollama 调用选项：关闭推理能力
                options = {
                    "temperature": 0.1,
                    "num_predict": max_tokens,
                    "top_p": 0.5,
                    "top_k": 10,
                }
                
                # 针对 qwen3 模型禁用推理
                if "qwen" in self.ollama_model.lower():
                    modified_prompt = prompt + "\n\n[要求：直接翻译，不要解释，不要推理，只输出译文]"
                else:
                    modified_prompt = prompt
                
                response = ollama.chat(
                    model=self.ollama_model,
                    messages=[
                        {"role": "system", "content": self._get_system_prompt()},
                        {"role": "user", "content": modified_prompt}
                    ],
                    options=options
                )
                translated_combined = response['message']['content'].strip()
            
            translated_parts = translated_combined.split(separator)
            translated_parts = [p.strip() for p in translated_parts if p.strip()]
            
            # 兜底处理
            if len(translated_parts) == 1 and len(b) > 1:
                lines = [line.strip() for line in translated_combined.split('\n') if line.strip()]
                if len(lines) == len(b):
                    translated_parts = lines
            
            if len(translated_parts) != len(b):
                # 批次失败，返回空让上层逐个翻译
                if CONFIG.get("VERBOSE_OUTPUT", True):
                    print(f"    [警告] 批次结果数量不匹配，期望{len(b)}条，实际{len(translated_parts)}条")
                return (b_idx, None, char_count, False)
            
            return (b_idx, translated_parts, char_count, True)
            
        except Exception as e:
            if CONFIG.get("VERBOSE_OUTPUT", True):
                print(f"    [错误] 批次 {batch_num} 失败: {e}")
            return (b_idx, None, char_count, False)
