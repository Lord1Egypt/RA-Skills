from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# 从「项目根」读取 .env：完整仓库为 app/core → parents[2]；技能包内为 code/app/core → 与 SKILL.md 同级的 parents[3]
_this_file = Path(__file__).resolve()
_skill_pack_root = _this_file.parents[3] / "code" / "app" / "core" / "settings.py"
if _skill_pack_root.resolve() == _this_file.resolve():
    _PROJECT_ROOT = _this_file.parents[3]
else:
    _PROJECT_ROOT = _this_file.parents[2]
_ENV_FILE = _PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    app_name: str = "VideoToText"
    app_env: str = "dev"
    request_timeout_seconds: int = 20
    sessdata: str = Field(default="", validation_alias=AliasChoices("SESSDATA", "sessdata"))
    bilibili_session_token: str = Field(
        default="", validation_alias=AliasChoices("BILIBILI_SESSION_TOKEN", "bilibili_session_token")
    )
    bili_jct: str = Field(
        default="",
        validation_alias=AliasChoices("BILI_JCT", "bili_jct"),
    )
    dede_user_id: str = Field(
        default="",
        validation_alias=AliasChoices("DEDEUSERID", "DedeUserID", "dede_user_id"),
    )
    dede_user_id_ckmd5: str = Field(
        default="",
        validation_alias=AliasChoices("DEDEUSERID__CKMD5", "DedeUserID__ckMd5", "dede_user_id_ckmd5"),
    )
    bilibili_min_interval_seconds: float = 0.8
    bilibili_max_retries: int = 3
    bilibili_backoff_base_seconds: float = 0.8
    # 是否开启时长/标题匹配与多轮采样（false=只取第一条可用轨道，更快，由调用方自行判断质量）
    bilibili_subtitle_validate: bool = False
    # 多轮采样会放大接口抖动（每轮最优可能不同）；稳定优先用 1，接口飘时再加大
    bilibili_subtitle_sample_rounds: int = 1
    bilibili_player_subtitle_empty_retries: int = 5
    bilibili_player_subtitle_empty_retry_sleep_seconds: float = 1.0
    bilibili_subtitle_sample_round_sleep_seconds: float = 1.0
    # 长视频：若最后一条字幕结束时间远早于视频时长，多半是 AI 半截/乱序，丢弃该次结果
    bilibili_subtitle_min_coverage_ratio: float = 0.2
    bilibili_subtitle_min_duration_for_coverage_check_seconds: float = 120.0
    # 超长视频：字幕条数过少也视为不可靠
    bilibili_subtitle_long_video_min_duration_seconds: float = 600.0
    bilibili_subtitle_long_video_min_body_lines: int = 40
    # 标题与字幕正文的汉字二元组命中率下限（防止 AI 串台到无关内容）
    bilibili_subtitle_min_title_match_score: float = 0.05
    bilibili_subtitle_relaxed_title_match_score: float = 0.03
    bilibili_subtitle_min_title_chars_for_match: int = 6
    # lan 为 ai-* 时标题二元组命中率下限（高于普通阈值，减轻 AI 串台/无关正文）
    bilibili_subtitle_ai_min_title_match: float = Field(
        default=0.10,
        validation_alias=AliasChoices(
            "BILIBILI_SUBTITLE_AI_MIN_TITLE_MATCH", "bilibili_subtitle_ai_min_title_match"
        ),
    )
    # validate=false 时仍对 AI 轨道做标题 sanity，不通过则试下一条轨道（避免首条 AI 乱码/外文）
    bilibili_subtitle_ai_sanity_when_validate_off: bool = Field(
        default=True,
        validation_alias=AliasChoices(
            "BILIBILI_SUBTITLE_AI_SANITY_WHEN_VALIDATE_OFF",
            "bilibili_subtitle_ai_sanity_when_validate_off",
        ),
    )

    # 本地 ASR（faster-whisper）：无官方字幕时使用；默认关闭以免 CI/无依赖环境报错
    local_asr_enabled: bool = Field(default=False, validation_alias=AliasChoices("LOCAL_ASR_ENABLED", "local_asr_enabled"))
    # 无可用字幕正文时（0 条轨道或有轨道但下载/校验失败）走本机转写；与 LOCAL_ASR_ENABLED 二选一即可
    local_asr_when_subtitle_fails: bool = Field(
        default=True,
        validation_alias=AliasChoices(
            "LOCAL_ASR_WHEN_SUBTITLE_FAILS", "local_asr_when_subtitle_fails"
        ),
    )
    local_asr_model: str = Field(
        default="small",
        validation_alias=AliasChoices("LOCAL_ASR_MODEL", "local_asr_model"),
    )
    # 速度档位：balanced(默认) / fast（更快，精度略降）
    local_asr_speed_profile: str = Field(
        default="balanced",
        validation_alias=AliasChoices("LOCAL_ASR_SPEED_PROFILE", "local_asr_speed_profile"),
    )
    local_asr_device: str = Field(
        default="cpu",
        validation_alias=AliasChoices("LOCAL_ASR_DEVICE", "local_asr_device"),
    )
    # 留空则 cpu 用 int8，cuda 用 float16
    local_asr_compute_type: str = Field(
        default="",
        validation_alias=AliasChoices("LOCAL_ASR_COMPUTE_TYPE", "local_asr_compute_type"),
    )
    local_asr_language: str = Field(
        default="zh",
        validation_alias=AliasChoices("LOCAL_ASR_LANGUAGE", "local_asr_language"),
    )
    # Whisper 无「简体/繁体」独立开关；对 zh 解码传入 initial_prompt 可偏向简体中文书写。
    # 留空表示不注入提示词。
    local_asr_initial_prompt: str = Field(
        default="以下语音为普通话内容，请使用简体中文书写。",
        validation_alias=AliasChoices(
            "LOCAL_ASR_INITIAL_PROMPT", "local_asr_initial_prompt"
        ),
    )
    local_asr_beam_size: int = Field(default=5, validation_alias=AliasChoices("LOCAL_ASR_BEAM_SIZE", "local_asr_beam_size"))
    local_asr_vad_filter: bool = Field(
        default=True,
        validation_alias=AliasChoices("LOCAL_ASR_VAD_FILTER", "local_asr_vad_filter"),
    )
    # 0 表示沿用后端默认；可按机器核心数调大
    local_asr_cpu_threads: int = Field(
        default=0,
        validation_alias=AliasChoices("LOCAL_ASR_CPU_THREADS", "local_asr_cpu_threads"),
    )
    # 0 表示沿用后端默认；I/O 与预处理并发
    local_asr_num_workers: int = Field(
        default=0,
        validation_alias=AliasChoices("LOCAL_ASR_NUM_WORKERS", "local_asr_num_workers"),
    )
    # 0 表示不限制
    local_asr_max_duration_seconds: float = Field(
        default=0.0,
        validation_alias=AliasChoices("LOCAL_ASR_MAX_DURATION_SECONDS", "local_asr_max_duration_seconds"),
    )
    local_asr_max_download_mb: int = Field(
        default=512,
        validation_alias=AliasChoices("LOCAL_ASR_MAX_DOWNLOAD_MB", "local_asr_max_download_mb"),
    )
    local_asr_download_timeout_seconds: int = Field(
        default=600,
        validation_alias=AliasChoices("LOCAL_ASR_DOWNLOAD_TIMEOUT_SECONDS", "local_asr_download_timeout_seconds"),
    )
    # 文本总结（优先 LLM，失败时回退本地摘要）
    summary_enabled: bool = Field(
        default=True,
        validation_alias=AliasChoices("SUMMARY_ENABLED", "summary_enabled"),
    )
    summary_llm_base_url: str = Field(
        default="",
        validation_alias=AliasChoices(
            "SUMMARY_LLM_BASE_URL",
            "summary_llm_base_url",
            # 与其它工具/Cursor 里常见的 OpenAI 兼容配置对齐
            "OPENAI_BASE_URL",
            "openai_base_url",
        ),
    )
    # 若填写完整 URL，则优先使用（不再与 BASE_URL 拼接）。火山方舟 OpenAI 兼容一般为 .../api/v3/chat/completions
    summary_llm_chat_completions_url: str = Field(
        default="",
        validation_alias=AliasChoices(
            "SUMMARY_LLM_CHAT_COMPLETIONS_URL",
            "summary_llm_chat_completions_url",
            "OPENAI_CHAT_COMPLETIONS_URL",
            "openai_chat_completions_url",
        ),
    )
    summary_llm_api_key: str = Field(
        default="",
        validation_alias=AliasChoices(
            "SUMMARY_LLM_API_KEY",
            "summary_llm_api_key",
            "OPENAI_API_KEY",
            "openai_api_key",
        ),
    )
    summary_llm_model: str = Field(
        default="",
        validation_alias=AliasChoices(
            "SUMMARY_LLM_MODEL",
            "summary_llm_model",
            "OPENAI_MODEL",
            "openai_model",
        ),
    )
    summary_llm_timeout_seconds: int = Field(
        default=120,
        validation_alias=AliasChoices(
            "SUMMARY_LLM_TIMEOUT_SECONDS", "summary_llm_timeout_seconds"
        ),
    )
    summary_llm_temperature: float = Field(
        default=0.2,
        validation_alias=AliasChoices("SUMMARY_LLM_TEMPERATURE", "summary_llm_temperature"),
    )

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE) if _ENV_FILE.is_file() else ".env",
        env_file_encoding="utf-8",
        # 避免系统/IDE 里被设成空字符串的环境变量覆盖 .env 里的 SUMMARY_LLM_* / OPENAI_*
        env_ignore_empty=True,
    )


settings = Settings()
