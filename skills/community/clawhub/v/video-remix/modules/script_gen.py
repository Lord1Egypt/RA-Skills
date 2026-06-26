"""
Script generator using LLM for creating voiceover scripts
"""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ScriptStyle(Enum):
    """Voiceover script styles"""
    PROFESSIONAL = "professional"      # 专业正式
    CASUAL = "casual"                  # 轻松随意
    ENTHUSIASTIC = "enthusiastic"      # 热情洋溢
    CALM = "calm"                      # 平静温和
    HUMOROUS = "humorous"              # 幽默风趣


@dataclass
class ScriptSegment:
    """Generated script for a video segment"""
    original_start: float
    original_end: float
    original_text: str
    script_text: str
    estimated_duration: float  # Estimated speaking duration
    style: str


@dataclass
class ScriptResult:
    """Complete script generation result"""
    success: bool
    segments: List[ScriptSegment]
    full_script: str
    total_duration: float
    error: Optional[str] = None


class ScriptGenerator:
    """Generate voiceover scripts using LLM"""
    
    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4o-mini",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        style: ScriptStyle = ScriptStyle.PROFESSIONAL,
        language: str = "zh"
    ):
        """
        Initialize script generator
        
        Args:
            provider: LLM provider (openai, anthropic, local)
            model: Model name
            api_key: API key
            base_url: Custom API base URL
            style: Voiceover style
            language: Output language (zh for Chinese)
        """
        self.provider = provider
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.style = style
        self.language = language
    
    def generate(
        self,
        analysis_path: Path,
        transcription_path: Optional[Path] = None
    ) -> ScriptResult:
        """
        Generate voiceover script from analysis
        
        Args:
            analysis_path: Path to analysis JSON
            transcription_path: Path to transcription (optional, for context)
        
        Returns:
            ScriptResult with generated scripts
        """
        try:
            print(f"✍️  Generating scripts...")
            print(f"   Style: {self.style.value}, Model: {self.model}")
            
            # Load analysis
            with open(analysis_path, "r", encoding="utf-8") as f:
                analysis_data = json.load(f)
            
            segments_data = analysis_data.get("segments", [])
            if not segments_data:
                return ScriptResult(
                    success=False,
                    segments=[],
                    full_script="",
                    total_duration=0,
                    error="No segments found in analysis"
                )
            
            # Load transcription for additional context
            trans_context = ""
            if transcription_path and transcription_path.exists():
                with open(transcription_path, "r", encoding="utf-8") as f:
                    trans_data = json.load(f)
                    trans_context = trans_data.get("full_text", "")
            
            # Generate scripts for each segment
            script_segments = []
            full_scripts = []
            total_duration = 0
            
            for seg_data in segments_data:
                script_seg = self._generate_segment_script(
                    seg_data,
                    trans_context
                )
                
                if script_seg:
                    script_segments.append(script_seg)
                    full_scripts.append(script_seg.script_text)
                    total_duration += script_seg.estimated_duration
            
            # Combine into full script
            full_script = "\n\n".join(full_scripts)
            
            print(f"✅ Script generation complete: {len(script_segments)} segments")
            
            return ScriptResult(
                success=True,
                segments=script_segments,
                full_script=full_script,
                total_duration=total_duration
            )
            
        except Exception as e:
            return ScriptResult(
                success=False,
                segments=[],
                full_script="",
                total_duration=0,
                error=str(e)
            )
    
    def _generate_segment_script(
        self,
        seg_data: Dict[str, Any],
        context: str
    ) -> Optional[ScriptSegment]:
        """Generate script for a single segment"""
        try:
            original_text = seg_data.get("text", "")
            summary = seg_data.get("summary", "")
            keywords = seg_data.get("keywords", [])
            seg_type = seg_data.get("segment_type", "other")
            
            # Build prompt
            prompt = self._build_prompt(
                original_text=original_text,
                summary=summary,
                keywords=keywords,
                seg_type=seg_type,
                context=context
            )
            
            # Call LLM
            script_text = self._call_llm(prompt)
            
            if not script_text:
                return None
            
            # Estimate duration (Chinese: ~4 characters per second)
            char_count = len(script_text.replace(" ", ""))
            estimated_duration = char_count / 4.0
            
            return ScriptSegment(
                original_start=seg_data.get("start", 0),
                original_end=seg_data.get("end", 0),
                original_text=original_text,
                script_text=script_text,
                estimated_duration=estimated_duration,
                style=self.style.value
            )
            
        except Exception as e:
            print(f"Error generating script for segment: {e}")
            return None
    
    def _build_prompt(
        self,
        original_text: str,
        summary: str,
        keywords: List[str],
        seg_type: str,
        context: str
    ) -> str:
        """Build LLM prompt for script generation"""
        
        style_instructions = {
            ScriptStyle.PROFESSIONAL: "专业、正式、清晰",
            ScriptStyle.CASUAL: "轻松、自然、像朋友聊天",
            ScriptStyle.ENTHUSIASTIC: "热情、有感染力、积极向上",
            ScriptStyle.CALM: "平静、温和、舒缓",
            ScriptStyle.HUMOROUS: "幽默、风趣、有趣",
        }
        
        style_desc = style_instructions.get(self.style, "专业、清晰")
        
        prompt = f"""你是一位专业的视频配音文案创作者。请根据以下内容，为视频片段生成一段配音文案。

【要求】
- 风格：{style_desc}
- 语言：中文
- 长度：30-100 字左右
- 要自然流畅，适合朗读
- 保持原意但重新组织语言

【视频片段信息】
内容摘要：{summary}
关键词：{', '.join(keywords)}
片段类型：{seg_type}

【原始内容】
{original_text[:500]}

请只输出配音文案，不要其他说明："""
        
        return prompt
    
    def _call_llm(self, prompt: str) -> str:
        """Call LLM API to generate script"""
        
        if self.provider == "openai" or self.provider == "compatible":
            return self._call_openai(prompt)
        elif self.provider == "anthropic":
            return self._call_anthropic(prompt)
        elif self.provider == "local":
            return self._call_local(prompt)
        else:
            # Fallback: return simplified original text
            print("⚠️  No LLM configured, using original text")
            return prompt.split("【原始内容】")[-1].strip()[:100]
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI or compatible API"""
        try:
            from openai import OpenAI
            
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的视频配音文案创作者。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except ImportError:
            print("⚠️  OpenAI library not installed: pip install openai")
            return ""
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return ""
    
    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API"""
        try:
            from anthropic import Anthropic
            
            client = Anthropic(api_key=self.api_key)
            
            response = client.messages.create(
                model=self.model or "claude-3-haiku-20240307",
                max_tokens=200,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text.strip()
            
        except ImportError:
            print("⚠️  Anthropic library not installed: pip install anthropic")
            return ""
        except Exception as e:
            print(f"Anthropic API error: {e}")
            return ""
    
    def _call_local(self, prompt: str) -> str:
        """Call local LLM (Ollama, etc.)"""
        try:
            import requests
            
            # Default to Ollama
            url = self.base_url or "http://localhost:11434/api/generate"
            
            payload = {
                "model": self.model or "qwen2.5:7b",
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            return data.get("response", "").strip()
            
        except Exception as e:
            print(f"Local LLM error: {e}")
            return ""
    
    def save_script(self, result: ScriptResult, output_path: Path):
        """Save script to file"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save full script as text
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.full_script)
        
        # Save detailed JSON
        json_path = output_path.with_suffix(".json")
        data = {
            "success": result.success,
            "total_duration": result.total_duration,
            "style": self.style.value,
            "segments": [
                {
                    "original_start": seg.original_start,
                    "original_end": seg.original_end,
                    "original_text": seg.original_text,
                    "script_text": seg.script_text,
                    "estimated_duration": seg.estimated_duration
                }
                for seg in result.segments
            ]
        }
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Saved script: {output_path}")


if __name__ == "__main__":
    import sys
    import os
    
    # Example usage
    if len(sys.argv) > 1:
        generator = ScriptGenerator(
            provider="openai",
            api_key=os.getenv("OPENAI_API_KEY"),
            style=ScriptStyle.PROFESSIONAL
        )
        result = generator.generate(Path(sys.argv[1]))
        print(f"Success: {result.success}")
        print(f"Segments: {len(result.segments)}")
        print(f"Total duration: {result.total_duration:.1f}s")
        if result.segments:
            print(f"\nFirst segment script:\n{result.segments[0].script_text}")
