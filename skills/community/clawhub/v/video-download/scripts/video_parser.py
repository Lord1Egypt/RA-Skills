import sys
import os
import glob
import yt_dlp
from faster_whisper import WhisperModel
import json
import tqdm

COMMON_SUBTITLE_EXTENSIONS = (
    "srt",
    "vtt",
    "ass",
    "ssa",
    "lrc",
    "sub",
    "sbv",
    "ttml",
    "dfxp",
    "json",
    "txt",
)


def find_existing_subtitles(video_folder: str, audio_filename: str) -> list:
    """查找已存在的字幕文件，支持 video.ext 和 video.<lang>.ext 格式"""
    subtitle_candidates = glob.glob(os.path.join(video_folder, f"{audio_filename}.*"))
    existing_subtitles = []
    for candidate in subtitle_candidates:
        basename = os.path.basename(candidate)
        if not basename.startswith(f"{audio_filename}."):
            continue
        suffix_parts = basename[len(audio_filename) + 1:].split(".")
        if suffix_parts and suffix_parts[-1].lower() in COMMON_SUBTITLE_EXTENSIONS:
            existing_subtitles.append(candidate)
    return sorted(existing_subtitles)


def extract_audio(video_path: str) -> str:
    """从视频中提取音频"""
    import ffmpeg

    audio_path = os.path.splitext(video_path)[0] + '.wav'
    stream = ffmpeg.input(video_path)
    stream = ffmpeg.output(stream, audio_path, acodec='pcm_s16le', ar=16000)
    ffmpeg.run(stream, overwrite_output=True, quiet=True)
    return audio_path


def transcribe_audio(audio_path: str, model: WhisperModel) -> dict:
    """使用Faster Whisper转录音频

    Args:
        audio_path: 音频文件路径
        model: Faster Whisper模型
    """

    # 获取转录结果和信息
    result, info = model.transcribe(audio=audio_path)

    # 收集所有片段，带进度条
    segments = []
    with tqdm.tqdm(total=info.duration, unit="seconds", desc="Transcribing") as pbar:
        for segment in result:
            segments.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text
            })
            pbar.update(segment.end - pbar.n)

    # 获取完整文本
    text = "".join([seg["text"] for seg in segments])

    return {
        "text": text,
        "segments": segments
    }


def save_subtitle(audio_path: str, result: dict, output_folder: str, subtitle_format: str = 'txt'):
    """保存字幕文件

    Args:
        audio_path: 音频文件路径
        result: Faster Whisper 转录结果
        output_folder: 输出目录
        subtitle_format: 字幕格式，支持: txt, srt, vtt, json
    """
    # 获取不带扩展名的音频文件名
    audio_filename = os.path.splitext(os.path.basename(audio_path))[0]
    output_path = os.path.join(output_folder, f"{audio_filename}.{subtitle_format.lower()}")

    if subtitle_format.lower() == 'txt':
        # 纯文本格式：直接保存所有文本
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result['text'].strip())

    elif subtitle_format.lower() == 'json':
        # JSON格式
        import json
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    elif subtitle_format.lower() == 'srt':
        # SRT格式
        with open(output_path, 'w', encoding='utf-8') as f:
            for idx, seg in enumerate(result['segments'], 1):
                # SRT时间格式: HH:MM:SS,mmm
                start_time = format_srt_time(seg['start'])
                end_time = format_srt_time(seg['end'])
                # 清理文本，去除多余空格
                text = seg['text'].strip()
                f.write(f"{idx}\n{start_time} --> {end_time}\n{text}\n\n")

    elif subtitle_format.lower() == 'vtt':
        # VTT格式
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("WEBVTT\n\n")
            for seg in result['segments']:
                # VTT时间格式: HH:MM:SS.mmm
                start_time = format_vtt_time(seg['start'])
                end_time = format_vtt_time(seg['end'])
                # 清理文本，去除多余空格
                text = seg['text'].strip()
                f.write(f"{start_time} --> {end_time}\n{text}\n\n")

    return output_path


def format_srt_time(seconds: float) -> str:
    """将秒数转换为SRT时间格式 HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def format_vtt_time(seconds: float) -> str:
    """将秒数转换为VTT时间格式 HH:MM:SS.mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def choose_subtitle_language_and_format(subtitle_map: dict) -> tuple:
    """从字幕信息中选择语言与格式：英文优先，其次中文；格式优先txt。"""
    if not subtitle_map:
        return None, None

    normalized = {}
    for lang, tracks in subtitle_map.items():
        if not tracks:
            continue
        exts = []
        for track in tracks:
            ext = (track.get("ext") or "").lower()
            if ext:
                exts.append(ext)
        if exts:
            normalized[lang] = exts

    if not normalized:
        return None, None

    def pick_format(exts: list) -> str:
        if "txt" in exts:
            return "txt"
        if "srt" in exts:
            return "srt"
        if "vtt" in exts:
            return "vtt"
        return exts[0]

    english_candidates = {"en", "en-us", "en-gb", "english"}
    chinese_candidates = {"zh", "zh-cn", "zh-hans", "zh-hant", "zh-tw", "chinese"}

    def normalize_lang(lang: str) -> str:
        return lang.lower().replace("_", "-")

    for lang in normalized:
        lang_norm = normalize_lang(lang)
        if lang_norm in english_candidates or lang_norm.startswith("en-"):
            return lang, pick_format(normalized[lang])

    for lang in normalized:
        lang_norm = normalize_lang(lang)
        if lang_norm in chinese_candidates or lang_norm.startswith("zh-"):
            return lang, pick_format(normalized[lang])

    fallback_lang = next(iter(normalized.keys()))
    return fallback_lang, pick_format(normalized[fallback_lang])


def download_subtitle(json_input: str) -> dict:
    """仅下载字幕：onlysubtitle=true 时使用。"""
    try:
        params = json.loads(json_input)
    except json.JSONDecodeError as e:
        return {"success": False, "message": f"JSON解析失败: {str(e)}", "results": []}

    urls = params.get("urls", [])
    output_path = params.get("output", "./downloads")
    onlysubtitle = params.get("onlysubtitle", False)
    cookie = params.get("cookie", "")
    cookiesfrombrowser = params.get("cookiesfrombrowser", "")
    cookiefile = params.get("cookiefile", "")

    if not urls:
        return {"success": False, "message": "URL列表为空", "results": []}
    if not onlysubtitle:
        return {"success": False, "message": "onlysubtitle=false，不执行仅字幕下载逻辑", "results": []}

    os.makedirs(output_path, exist_ok=True)

    results = []
    success_count = 0

    base_opts = {"format": "bestvideo+bestaudio/best"}
    if cookie:
        base_opts["http_headers"] = {"Cookie": cookie}
    if cookiesfrombrowser:
        base_opts["cookiesfrombrowser"] = (cookiesfrombrowser,)
    if cookiefile:
        base_opts["cookiefile"] = cookiefile

    for idx, url in enumerate(urls, 1):
        try:
            with yt_dlp.YoutubeDL(base_opts) as ydl_probe:
                info = ydl_probe.extract_info(url, download=False)

            video_title = info.get("title", f"video_{idx}")
            safe_title = "".join(c for c in video_title if c.isalnum() or c in (" ", "-", "_")).strip() or f"video_{idx}"
            video_folder = os.path.join(output_path, safe_title)
            os.makedirs(video_folder, exist_ok=True)

            subtitle_map = {}
            subtitle_map.update(info.get("subtitles") or {})
            subtitle_map.update(info.get("automatic_captions") or {})
            selected_lang, selected_format = choose_subtitle_language_and_format(subtitle_map)

            if not selected_lang or not selected_format:
                results.append({
                    "url": url,
                    "success": False,
                    "subtitle_path": None,
                    "error": "未找到可用字幕"
                })
                continue

            download_opts = dict(base_opts)
            download_opts.update({
                "outtmpl": f"{video_folder}/%(title)s.%(ext)s",
                "skip_download": True,
                "writesubtitles": True,
                "writeautomaticsub": True,
                "subtitleslangs": [selected_lang],
                "subtitlesformat": selected_format
            })

            with yt_dlp.YoutubeDL(download_opts) as ydl_download:
                ydl_download.download([url])
                video_path = ydl_download.prepare_filename(info)

            subtitle_base = os.path.splitext(os.path.basename(video_path))[0]
            subtitle_files = find_existing_subtitles(video_folder, subtitle_base)
            if subtitle_files:
                success_count += 1
                results.append({
                    "url": url,
                    "success": True,
                    "subtitle_path": subtitle_files[0],
                    "error": None
                })
            else:
                results.append({
                    "url": url,
                    "success": False,
                    "subtitle_path": None,
                    "error": "字幕下载执行完成，但未找到字幕文件"
                })
        except Exception as e:
            results.append({
                "url": url,
                "success": False,
                "subtitle_path": None,
                "error": str(e)
            })

    overall_success = success_count > 0
    return {
        "success": overall_success,
        "message": f"仅字幕下载完成：成功 {success_count}/{len(urls)}",
        "results": results
    }


def download_videos(json_input: str) -> dict:
    """
    下载视频并转录

    Args:
        json_input: JSON字符串，支持以下参数:
            - urls: 视频URL列表 (必须)
            - output: 下载保存路径 (默认: "./downloads")
            - model: Faster Whisper模型名称 (默认: "small")
            - transcribe: 是否进行转录 (默认: True)
            - subtitle_format: 字幕格式，支持: txt, srt, vtt, json (默认: "txt")
            - download_subtitle: 是否下载视频自带字幕 (默认: False)
            - overwrite_subtitle: 是否覆盖已存在的字幕文件 (默认: True)
            - cookie: 可选，下载请求使用的 Cookie 字符串 (默认: "")
            - cookiesfrombrowser: 可选，从浏览器读取 cookies (默认: "")
            - cookiefile: 可选，Netscape 格式 cookie 文件路径 (默认: "")

    Returns:
        结果字典
    """
    try:
        params = json.loads(json_input)
    except json.JSONDecodeError as e:
        return {"success": False, "message": f"JSON解析失败: {str(e)}", "downloaded": [], "transcripts": []}

    urls = params.get("urls", [])
    output_path = params.get("output", "./downloads")
    model_name = params.get("model", "small")
    transcribe = params.get("transcribe", True)  # 是否进行转录
    subtitle_format = params.get("subtitle_format", "txt")  # 字幕格式
    download_subtitle = params.get("download_subtitle", False)  # 是否下载视频自带字幕
    overwrite_subtitle = params.get("overwrite_subtitle", True)  # 是否覆盖已存在的字幕文件
    cookie = params.get("cookie", "")  # 下载请求 Cookie
    cookiesfrombrowser = params.get("cookiesfrombrowser", "")  # 从浏览器读取 cookies
    cookiefile = params.get("cookiefile", "")  # cookie 文件路径

    if not urls:
        return {"success": False, "message": "URL列表为空", "downloaded": [], "transcripts": []}

    os.makedirs(output_path, exist_ok=True)

    downloaded = []
    video_list = []  # 存储下载后的视频信息，用于后续转录

    # ========== 第一步：下载所有视频 ==========
    print("=" * 50)
    print("开始下载视频...")
    print("=" * 50)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
    }

    if cookie:
        ydl_opts['http_headers'] = {
            'Cookie': cookie
        }
    if cookiesfrombrowser:
        ydl_opts['cookiesfrombrowser'] = (cookiesfrombrowser,)
    if cookiefile:
        ydl_opts['cookiefile'] = cookiefile

    language = 'en'
    # 如果需要下载视频自带的字幕
    if download_subtitle:
        ydl_opts['writesubtitles'] = True
        ydl_opts['writeautomaticsub'] = True
        ydl_opts['subtitleslangs'] = [language]
        ydl_opts['subtitlesformat'] = subtitle_format

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for idx, url in enumerate(urls):
            try:
                # 先获取视频信息，确定文件夹名称
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', f'video_{idx + 1}')
                # 清理文件名中的非法字符
                safe_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).strip()
                video_folder = os.path.join(output_path, safe_title)
                os.makedirs(video_folder, exist_ok=True)

                # 检查视频是否已存在
                video_path = ydl.prepare_filename(info)
                if os.path.exists(video_path):
                    print(f"[{video_title}] 文件已存在，跳过下载")
                    downloaded.append(url)
                    video_list.append({
                        "title": video_title,
                        "url": url,
                        "video_path": video_path,
                        "video_folder": video_folder
                    })
                    print(f"[{video_title}] 已添加到转录队列")
                    continue

                # 下载视频到对应文件夹
                ydl_opts['outtmpl'] = f'{video_folder}/%(title)s.%(ext)s'
                ydl_opts['progress_hooks'] = [lambda d, t=video_title: print_progress(d, t)]

                def print_progress(d, title):
                    if d['status'] == 'downloading':
                        total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                        downloaded_bytes = d.get('downloaded_bytes', 0)
                        speed = d.get('speed', 0)

                        # 格式化文件大小
                        def format_size(bytes_val):
                            if bytes_val >= 1024 * 1024 * 1024:
                                return f"{bytes_val / 1024 / 1024 / 1024:.2f} GB"
                            elif bytes_val >= 1024 * 1024:
                                return f"{bytes_val / 1024 / 1024:.2f} MB"
                            elif bytes_val >= 1024:
                                return f"{bytes_val / 1024:.2f} KB"
                            else:
                                return f"{bytes_val} B"

                        speed_str = f"{speed / 1024 / 1024:.2f} MB/s" if speed else "N/A"
                        if total > 0:
                            percent = downloaded_bytes / total * 100
                            print(f"\r[{title}] {format_size(downloaded_bytes)} / {format_size(total)} ({percent:.1f}%) | 速度: {speed_str}", end='', flush=True)
                        else:
                            # 没有总大小时，只显示已下载大小和速度
                            print(f"\r[{title}] 已下载: {format_size(downloaded_bytes)} | 速度: {speed_str}", end='', flush=True)
                    elif d['status'] == 'finished':
                        total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)

                        def format_size(bytes_val):
                            if bytes_val >= 1024 * 1024 * 1024:
                                return f"{bytes_val / 1024 / 1024 / 1024:.2f} GB"
                            elif bytes_val >= 1024 * 1024:
                                return f"{bytes_val / 1024 / 1024:.2f} MB"
                            elif bytes_val >= 1024:
                                return f"{bytes_val / 1024:.2f} KB"
                            else:
                                return f"{bytes_val} B"

                        print(f"\n[{title}] 下载完成! 文件大小: {format_size(total)}")

                with yt_dlp.YoutubeDL(ydl_opts) as ydl_video:
                    ydl_video.download([url])
                    video_path = ydl_video.prepare_filename(info)

                if os.path.exists(video_path):
                    downloaded.append(url)
                    video_list.append({
                        "title": video_title,
                        "url": url,
                        "video_path": video_path,
                        "video_folder": video_folder
                    })
                    print(f"[{video_title}] 已添加到转录队列")
            except Exception as e:
                print(f"下载失败 {url}: {str(e)}")

    # ========== 第二步：转录所有视频 ==========
    if not transcribe:
        # 不需要转录，只下载视频
        print("\n" + "=" * 50)
        print("视频下载完成 (跳过转录)")
        print("=" * 50)
        return {
            "success": True,
            "message": f"成功下载 {len(downloaded)} 个视频 (跳过转录)",
            "downloaded": downloaded,
            "transcripts": []
        }

    if not video_list:
        return {
            "success": False,
            "message": "未下载到任何视频，程序退出",
            "downloaded": downloaded,
            "transcripts": []
        }

    transcripts = []
    pending_video_list = []
    if not overwrite_subtitle:
        for idx, video_info in enumerate(video_list):
            video_title = video_info["title"]
            url = video_info["url"]
            video_path = video_info["video_path"]
            video_folder = video_info["video_folder"]
            audio_filename = os.path.splitext(os.path.basename(video_path))[0]
            existing_subtitles = find_existing_subtitles(video_folder, audio_filename)
            if existing_subtitles:
                subtitle_preview = ", ".join(os.path.basename(path) for path in existing_subtitles)
                print(f"\n[{idx + 1}/{len(video_list)}] 检测到已存在字幕文件，跳过转录: {video_title}")
                print(f"[{idx + 1}/{len(video_list)}] 已存在字幕: {subtitle_preview}")
                transcripts.append({
                    "title": video_title,
                    "url": url,
                    "transcript": existing_subtitles[0],
                    "format": subtitle_format
                })
            else:
                pending_video_list.append(video_info)
    else:
        pending_video_list = video_list

    if not pending_video_list:
        print("\n无需转录：所有视频均已存在字幕文件")
        return {
            "success": True,
            "message": f"成功下载 {len(downloaded)} 个视频，跳过 {len(transcripts)} 个转录（字幕已存在）",
            "downloaded": downloaded,
            "transcripts": transcripts
        }

    print("\n" + "=" * 50)
    print(f"视频下载完成，开始转录 {len(pending_video_list)} 个视频...")
    print("=" * 50)

    # 使用 Faster Whisper 加载模型
    # device: "auto" 自动选择 CUDA 或 CPU
    # compute_type: "auto" 自动选择最佳精度 (float16 for CUDA, int8 for CPU)
    model = WhisperModel(model_name, device="auto", compute_type="auto")
    for idx, video_info in enumerate(pending_video_list):
        video_title = video_info["title"]
        url = video_info["url"]
        video_path = video_info["video_path"]
        video_folder = video_info["video_folder"]

        print(f"\n[{idx + 1}/{len(pending_video_list)}] 正在提取音频: {video_title}")
        try:
            audio_path = extract_audio(video_path)
            print(f"[{idx + 1}/{len(pending_video_list)}] 正在转录: {video_title}")

            transcript = transcribe_audio(audio_path, model)
            print()  # 换行

            # 保存字幕文件
            print(f"[{idx + 1}/{len(pending_video_list)}] 正在保存字幕文件...")
            transcript_filename = save_subtitle(audio_path, transcript, video_folder, subtitle_format)
            print(f"[{idx + 1}/{len(pending_video_list)}] 字幕文件已保存")

            transcripts.append({
                "title": video_title,
                "url": url,
                "transcript": transcript_filename,
                "format": subtitle_format
            })
            print(f"[{idx + 1}/{len(pending_video_list)}] 转录完成: {video_title}")
        except Exception as e:
            print(f"转录失败 {video_title}: {str(e)}")
            transcripts.append({
                "title": video_title,
                "url": url,
                "transcript": None,
                "error": str(e)
            })

    return {
        "success": True,
        "message": f"成功下载 {len(downloaded)} 个视频，完成 {len([t for t in transcripts if t.get('transcript')])} 个转录",
        "downloaded": downloaded,
        "transcripts": transcripts
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python video_parser.py '<JSON字符串>'")
        print()
        print("参数说明:")
        print("  urls: 视频URL列表 (必须)")
        print("  output: 下载保存路径 (默认: './downloads')")
        print("  model: Faster Whisper模型 (默认: 'small', 可选: tiny/base/small/medium/large/large-v2/large-v3/turbo)")
        print("  transcribe: 是否转录 (默认: True)")
        print("  subtitle_format: 字幕格式 (默认: 'txt', 可选: txt/srt/vtt/json)")
        print("  download_subtitle: 是否下载视频自带字幕 (默认: False)")
        print("  onlysubtitle: 是否仅下载字幕 (默认: False)")
        print("  overwrite_subtitle: 是否覆盖已存在的字幕文件 (默认: True)")
        print("  cookie: 下载请求 Cookie 字符串 (默认: '')")
        print("  cookiesfrombrowser: 从浏览器读取 cookies (默认: '')")
        print("  cookiefile: Netscape 格式 cookie 文件路径 (默认: '')")
        print()
        print('示例1 - 下载并转录: python video_parser.py \'{"urls":["URL"],"output":"./downloads"}\'')
        print('示例2 - 只下载不转录: python video_parser.py \'{"urls":["URL"],"output":"./downloads","transcribe":false}\'')
        print('示例3 - 生成SRT字幕: python video_parser.py \'{"urls":["URL"],"output":"./downloads","subtitle_format":"srt"}\'')
        print('示例4 - 下载视频自带字幕: python video_parser.py \'{"urls":["URL"],"output":"./downloads","download_subtitle":true}\'')
        print('示例5 - 不覆盖已有字幕: python video_parser.py \'{"urls":["URL"],"overwrite_subtitle":false}\'')
        print('示例6 - 携带 Cookie 下载: python video_parser.py \'{"urls":["URL"],"cookie":"sid=xxx; token=yyy"}\'')
        print('示例7 - 从浏览器读取 cookies: python video_parser.py \'{"urls":["URL"],"cookiesfrombrowser":"chrome"}\'')
        print('示例8 - 使用 cookie 文件下载: python video_parser.py \'{"urls":["URL"],"cookiefile":"/path/to/cookies.txt"}\'')
        print('示例9 - 仅下载字幕: python video_parser.py \'{"urls":["URL"],"output":"./downloads","onlysubtitle":true}\'')
        sys.exit(1)

    json_input = ''.join(sys.argv[1:])
    try:
        cli_params = json.loads(json_input)
    except json.JSONDecodeError:
        cli_params = {}

    if cli_params.get("onlysubtitle", False):
        subtitle_result = download_subtitle(json_input)
        failed_urls = [
            item.get("url")
            for item in subtitle_result.get("results", [])
            if item.get("url") and (
                not item.get("subtitle_path") or not os.path.exists(item.get("subtitle_path"))
            )
        ]

        if failed_urls:
            fallback_params = dict(cli_params)
            fallback_params["urls"] = failed_urls
            fallback_params["onlysubtitle"] = False
            fallback_result = download_videos(json.dumps(fallback_params, ensure_ascii=False))
            result = {
                "success": subtitle_result.get("success", False) or fallback_result.get("success", False),
                "message": (
                    f"{subtitle_result.get('message', '')}；"
                    f"未下载到字幕的链接已回退到视频下载流程：{fallback_result.get('message', '')}"
                ),
                "results": subtitle_result.get("results", []),
                "fallback": fallback_result
            }
        else:
            result = subtitle_result
    else:
        result = download_videos(json_input)

    print(result['message'])
    if 'results' in result:
        print(result['results'])
        if 'fallback' in result:
            print(result['fallback'].get('transcripts', []))
    else:
        print(result['transcripts'])
