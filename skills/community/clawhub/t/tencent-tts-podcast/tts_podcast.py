# -*- coding: utf-8 -*-
"""
Tencent TTS Podcast Generator
Convert text to podcast audio using Tencent Cloud TTS service
Supports both short and long text processing with automatic chunking
"""

import os
import uuid
import hashlib
import hmac
import json
import sys
import time
import base64
import requests
import wave
from datetime import datetime

# Tencent Cloud TTS single request max character limit (tested stable at ~150 chars)
MAX_TEXT_LENGTH = 150

# Speech rate configuration: characters per minute (for duration estimation)
CHARS_PER_MINUTE = 240  # ~240 chars/minute

# Maximum supported duration (minutes)
MAX_DURATION_MINUTES = 30

# Default concurrent configuration
DEFAULT_MAX_WORKERS = 3

# Long text optimization: chunk size (adjustable, larger = fewer requests but may timeout)
LONG_TEXT_CHUNK_SIZE = 140  # Slightly less than MAX_TEXT_LENGTH for safety margin

# Short text optimization: single request timeout (seconds)
SHORT_TEXT_TIMEOUT = 30

# Long text optimization: single chunk timeout (seconds)
LONG_TEXT_TIMEOUT = 60

# Enable automatic retry
ENABLE_RETRY = True
MAX_RETRY_COUNT = 2

# Voice type mappings
VOICE_TYPES = {
    # Basic voices
    "0": "普通女声",
    "1": "普通男声",
    "5": "情感女声",
    "6": "情感男声",
    # Featured voices
    "1000": "智障少女",
    "1001": "阳光少年",
    "1002": "温柔淑女",
    "1003": "成熟青年",
    "1004": "严厉管事",
    "1005": "亲和女声",
    "1006": "甜美女声",
    "1007": "磁性男声",
    "1008": "播音主播",
    # Customer service voices
    "101001": "客服女声",
    "101005": "售前客服",
    "101007": "售后客服",
    "101008": "亲和客服",
    # Tencent featured voices
    "502006": "小旭",
    "502007": "小巴",
    "502008": "思驰",
    "502009": "思佳",
    "502010": "思悦",
    "502011": "小宁",
    "502012": "小杨",
    "502013": "云扬",
    "502014": "云飞",
}


def get_voice_list() -> dict:
    """Get available voice types"""
    return VOICE_TYPES


def get_voice_name(voice_type: str) -> str:
    """Get voice name by voice type ID"""
    return VOICE_TYPES.get(str(voice_type), "Unknown")


def split_text(text: str, max_length: int = None, preserve_paragraphs: bool = True) -> list:
    """
    Split text into multiple chunks while maintaining semantic integrity
    
    Args:
        text: Text to split
        max_length: Max characters per chunk, defaults to LONG_TEXT_CHUNK_SIZE
        preserve_paragraphs: Whether to preserve paragraph boundaries
    
    Returns:
        List of text chunks
    """
    import re
    
    if max_length is None:
        max_length = LONG_TEXT_CHUNK_SIZE
    
    # Clean text
    text = text.replace('\r\n', '\n').strip()
    
    # Return directly if text is short
    if len(text) <= max_length:
        return [text] if text else []
    
    # Split by paragraphs
    paragraphs = text.split('\n')
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            if preserve_paragraphs and current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""
            continue
            
        # If single paragraph exceeds limit, split by sentences
        if len(para) > max_length:
            # Save current accumulated content first
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""
            
            # Split by sentences (support multiple punctuation marks)
            sentences = re.split(r'([。！？；.!?;])', para)
            temp_chunk = ""
            for i in range(0, len(sentences), 2):
                sent = sentences[i].strip()
                punct = sentences[i+1] if i+1 < len(sentences) else ""
                full_sent = sent + punct
                
                if not sent:
                    continue
                    
                if len(temp_chunk) + len(full_sent) <= max_length:
                    temp_chunk += full_sent
                else:
                    if temp_chunk:
                        chunks.append(temp_chunk)
                    # If single sentence is too long, force truncate at semantic boundaries
                    if len(full_sent) > max_length:
                        # Try to truncate at comma
                        sub_sentences = re.split(r'([，,])', full_sent)
                        sub_chunk = ""
                        for j in range(0, len(sub_sentences), 2):
                            sub_sent = sub_sentences[j]
                            sub_punct = sub_sentences[j+1] if j+1 < len(sub_sentences) else ""
                            full_sub = sub_sent + sub_punct
                            
                            if len(sub_chunk) + len(full_sub) <= max_length:
                                sub_chunk += full_sub
                            else:
                                if sub_chunk:
                                    chunks.append(sub_chunk)
                                sub_chunk = full_sub
                        if sub_chunk:
                            # If still too long, force truncate
                            if len(sub_chunk) > max_length:
                                chunks.append(sub_chunk[:max_length])
                                temp_chunk = sub_chunk[max_length:]
                            else:
                                temp_chunk = sub_chunk
                    else:
                        temp_chunk = full_sent
            if temp_chunk:
                chunks.append(temp_chunk)
        else:
            # Check if adding current paragraph exceeds limit
            separator = "\n" if current_chunk else ""
            if len(current_chunk) + len(separator) + len(para) <= max_length:
                current_chunk = current_chunk + separator + para if current_chunk else para
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = para
    
    # Save last chunk
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks


def estimate_duration(text_length: int) -> float:
    """Estimate audio duration in minutes"""
    return text_length / CHARS_PER_MINUTE


def validate_text_length(text: str) -> tuple[bool, str]:
    """Validate if text length is within supported range"""
    text_length = len(text)
    estimated_minutes = estimate_duration(text_length)
    
    if estimated_minutes > MAX_DURATION_MINUTES:
        max_chars = MAX_DURATION_MINUTES * CHARS_PER_MINUTE
        return False, f"Text too long (~{estimated_minutes:.1f} minutes), max supported is {MAX_DURATION_MINUTES} minutes (~{max_chars} chars)"
    
    return True, f"Estimated duration: ~{estimated_minutes:.1f} minutes"


def sign(key: bytes, msg: str) -> bytes:
    """Calculate HMAC-SHA256 signature"""
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def tts_request(secret_id: str, secret_key: str, text: str, voice_type: str, 
                timeout: int = None, enable_retry: bool = None, max_retries: int = None) -> bytes:
    """
    Send single TTS request and return audio data
    
    Args:
        secret_id: Tencent Cloud SecretId
        secret_key: Tencent Cloud SecretKey
        text: Text to convert
        voice_type: Voice type ID
        timeout: Request timeout in seconds, uses config default if None
        enable_retry: Whether to enable retry, uses config default if None
        max_retries: Max retry count, uses config default if None
    
    Returns:
        Audio data (bytes)
    """
    # Use defaults
    if timeout is None:
        timeout = LONG_TEXT_TIMEOUT if len(text) > MAX_TEXT_LENGTH else SHORT_TEXT_TIMEOUT
    if enable_retry is None:
        enable_retry = ENABLE_RETRY
    if max_retries is None:
        max_retries = MAX_RETRY_COUNT
    
    service = "tts"
    host = "tts.tencentcloudapi.com"
    version = "2019-08-23"
    action = "TextToVoice"
    endpoint = "https://tts.tencentcloudapi.com"
    algorithm = "TC3-HMAC-SHA256"
    
    last_error = None
    retry_count = 0
    
    while retry_count <= max_retries if enable_retry else 0:
        try:
            timestamp = int(time.time())
            date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
            
            payload = json.dumps({"Text": text, "SessionId": str(uuid.uuid4()), "VoiceType": voice_type})
            
            # Step 1: Build canonical request
            http_request_method = "POST"
            canonical_uri = "/"
            canonical_querystring = ""
            ct = "application/json; charset=utf-8"
            canonical_headers = "content-type:%s\nhost:%s\nx-tc-action:%s\n" % (ct, host, action.lower())
            signed_headers = "content-type;host;x-tc-action"
            hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
            canonical_request = (http_request_method + "\n" +
                                canonical_uri + "\n" +
                                canonical_querystring + "\n" +
                                canonical_headers + "\n" +
                                signed_headers + "\n" +
                                hashed_request_payload)

            # Step 2: Build string to sign
            credential_scope = date + "/" + service + "/" + "tc3_request"
            hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
            string_to_sign = (algorithm + "\n" +
                            str(timestamp) + "\n" +
                            credential_scope + "\n" +
                            hashed_canonical_request)

            # Step 3: Calculate signature
            secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
            secret_service = sign(secret_date, service)
            secret_signing = sign(secret_service, "tc3_request")
            signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

            # Step 4: Build Authorization header
            authorization = (algorithm + " " +
                            "Credential=" + secret_id + "/" + credential_scope + ", " +
                            "SignedHeaders=" + signed_headers + ", " +
                            "Signature=" + signature)

            # Step 5: Build and send request
            headers = {
                "Authorization": authorization,
                "Content-Type": "application/json; charset=utf-8",
                "Host": host,
                "X-TC-Action": action,
                "X-TC-Timestamp": str(timestamp),
                "X-TC-Version": version
            }

            resp = requests.post(endpoint, headers=headers, data=payload.encode('utf-8'), timeout=timeout)
            resp.raise_for_status()
            response_data = resp.content.decode('utf-8', errors='replace')
            response_json = json.loads(response_data)
            
            if 'Error' in response_json.get('Response', {}):
                error_info = response_json['Response']['Error']
                raise Exception(f"{error_info.get('Code', 'Unknown')} - {error_info.get('Message', 'Unknown error')}")
            
            if 'Audio' not in response_json.get('Response', {}):
                raise Exception("Audio field not found in response")
            
            audio_base64 = response_json['Response']['Audio']
            return base64.b64decode(audio_base64)
            
        except Exception as e:
            last_error = e
            retry_count += 1
            if enable_retry and retry_count <= max_retries:
                wait_time = 2 ** retry_count  # Exponential backoff
                print(f"[WARN] TTS request failed, retrying in {wait_time}s ({retry_count}/{max_retries}): {str(e)}")
                time.sleep(wait_time)
            else:
                break
    
    raise last_error if last_error else Exception("TTS request failed")


def combine_wav_files(file_paths: list, output_path: str) -> None:
    """Combine multiple WAV files into one"""
    if not file_paths:
        raise Exception("No audio files to combine")
    
    # Read first file as reference
    with wave.open(file_paths[0], 'rb') as ref_wav:
        n_channels = ref_wav.getnchannels()
        sampwidth = ref_wav.getsampwidth()
        framerate = ref_wav.getframerate()
    
    # Collect all audio data
    all_data = []
    for fp in file_paths:
        with wave.open(fp, 'rb') as wav:
            # Verify parameters match
            if wav.getnchannels() != n_channels or wav.getsampwidth() != sampwidth or wav.getframerate() != framerate:
                raise Exception(f"WAV parameters mismatch: {fp}")
            frames = wav.readframes(wav.getnframes())
            # Remove WAV header, keep only data
            data_start = 44  # Standard WAV header size
            if len(frames) > data_start:
                all_data.append(frames[data_start:])
            else:
                all_data.append(frames)
    
    # Write combined WAV file
    with wave.open(output_path, 'wb') as out_wav:
        out_wav.setnchannels(n_channels)
        out_wav.setsampwidth(sampwidth)
        out_wav.setframerate(framerate)
        out_wav.writeframes(b''.join(all_data))


def process_chunk(args: tuple) -> tuple:
    """Process single chunk (for concurrent execution)"""
    idx, chunk, secret_id, secret_key, voice_type, base_session_id, timeout = args
    try:
        audio_data = tts_request(secret_id, secret_key, chunk, voice_type, timeout=timeout)
        temp_file = f"temp_tts_{base_session_id}_{idx}.wav"
        with open(temp_file, 'wb') as f:
            f.write(audio_data)
        return (idx, temp_file, None)
    except Exception as e:
        return (idx, None, str(e))


def tts_main(params: dict) -> dict:
    """
    Tencent Cloud TTS main function (supports long text auto-chunking, 10+ minute audio)
    
    Args:
        params: Dictionary containing:
            - Text: Text to convert
            - VoiceType: Voice type ID
            - secret_id: Tencent Cloud SecretId
            - secret_key: Tencent Cloud SecretKey
            - max_workers: Concurrent threads (default 3, long text: 3-5, short text: 1-2)
            - chunk_size: Chunk size (default LONG_TEXT_CHUNK_SIZE)
            - timeout: Request timeout in seconds (short: 30, long: 60)
            - enable_retry: Enable auto retry (default True)
            - max_retries: Max retry count (default 2)
            - preserve_paragraphs: Preserve paragraph boundaries when chunking (default True)
    
    Returns:
        Dictionary with Code, Msg, filename, duration
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    secret_id = params.get('secret_id', '')
    secret_key = params.get('secret_key', '')
    
    # Get optimization parameters
    max_workers = params.get('max_workers', DEFAULT_MAX_WORKERS)
    chunk_size = params.get('chunk_size', LONG_TEXT_CHUNK_SIZE)
    timeout = params.get('timeout', None)
    enable_retry = params.get('enable_retry', ENABLE_RETRY)
    max_retries = params.get('max_retries', MAX_RETRY_COUNT)
    preserve_paragraphs = params.get('preserve_paragraphs', True)

    if not secret_id or not secret_key:
        return {"Code": 1, "Msg": "Missing Tencent Cloud credentials (secret_id or secret_key)", "filename": None, "duration": 0}

    Text = params.get('Text', '')
    VoiceType = params.get('VoiceType', '')

    if not Text:
        return {"Code": 1, "Msg": "Text cannot be empty", "filename": None, "duration": 0}

    if not VoiceType:
        return {"Code": 1, "Msg": "VoiceType cannot be empty", "filename": None, "duration": 0}
    
    # Validate text length
    valid, msg = validate_text_length(Text)
    if not valid:
        return {"Code": 1, "Msg": msg, "filename": None, "duration": 0}

    text_len = len(Text)
    is_long_text = text_len > MAX_TEXT_LENGTH
    estimated_duration = estimate_duration(text_len)
    
    if timeout is None:
        timeout = LONG_TEXT_TIMEOUT if is_long_text else SHORT_TEXT_TIMEOUT

    # Long text chunking
    if is_long_text:
        chunks = split_text(Text, max_length=chunk_size, preserve_paragraphs=preserve_paragraphs)
        total_chunks = len(chunks)
        
        print(f"[INFO] Text length {text_len} chars, estimated duration {estimated_duration:.1f} minutes")
        print(f"[INFO] Split into {total_chunks} chunks, concurrency: {max_workers}")
        
        temp_files = [None] * total_chunks
        base_session_id = str(uuid.uuid4())
        
        try:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(
                        process_chunk, 
                        (i, chunk, secret_id, secret_key, VoiceType, base_session_id, timeout)
                    ): i for i, chunk in enumerate(chunks)
                }
                
                completed = 0
                for future in as_completed(futures):
                    idx, temp_file, error = future.result()
                    if error:
                        raise Exception(f"Chunk {idx+1} failed: {error}")
                    temp_files[idx] = temp_file
                    completed += 1
                    print(f"[INFO] Completed {completed}/{total_chunks} chunks")
            
            final_filename = f"tts_output_{base_session_id[:8]}.wav"
            combine_wav_files(temp_files, final_filename)
            
            for tf in temp_files:
                try:
                    if tf and os.path.exists(tf):
                        os.remove(tf)
                except:
                    pass
            
            return {
                "Code": 0,
                "Msg": f"success ({total_chunks} chunks, estimated {estimated_duration:.1f} minutes)",
                "filename": final_filename,
                "duration": estimated_duration
            }
            
        except Exception as e:
            for tf in temp_files:
                try:
                    if tf and os.path.exists(tf):
                        os.remove(tf)
                except:
                    pass
            return {"Code": 1, "Msg": f"TTS generation error: {str(e)}", "filename": None, "duration": 0}
    else:
        # Short text direct processing
        try:
            audio_data = tts_request(secret_id, secret_key, Text, VoiceType, 
                                     timeout=timeout, enable_retry=enable_retry, max_retries=max_retries)
            SessionId = str(uuid.uuid4())
            filename = f"tts_output_{SessionId[:8]}.wav"
            
            with open(filename, 'wb') as f:
                f.write(audio_data)
            
            return {
                "Code": 0,
                "Msg": "success",
                "filename": filename,
                "duration": estimated_duration
            }
        except Exception as err:
            return {"Code": 1, "Msg": f"TTS generation error: {str(err)}", "filename": None, "duration": 0}


def _upload_to_cos(local_path: str, object_key: str, secret_id: str, secret_key: str, 
                   bucket_name: str = "ti-aoi", app_id: str = "1257195185", 
                   region: str = "ap-guangzhou") -> str:
    """Upload file to Tencent Cloud COS"""
    try:
        from qcloud_cos import CosConfig, CosS3Client
    except ImportError:
        # Try to install
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "cos-python-sdk-v5", "-q"])
        from qcloud_cos import CosConfig, CosS3Client

    cfg = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    cli = CosS3Client(cfg)

    bucket_full = f"{bucket_name}-{app_id}"
    from mimetypes import guess_type
    mime, _ = guess_type(local_path)
    content_type = mime or "audio/wav"

    cli.put_object_from_local_file(
        Bucket=bucket_full,
        LocalFilePath=local_path,
        Key=object_key,
        ContentType=content_type
    )
    try:
        cli.put_object_acl(Bucket=bucket_full, Key=object_key, ACL="public-read")
    except:
        pass

    return f"https://{bucket_full}.cos.{region}.myqcloud.com/{object_key}"


def main(params: dict) -> dict:
    """
    Main function - Generate podcast audio and upload to COS
    
    Args:
        params: Dictionary containing:
            - Text: Text content to convert
            - VoiceType: Voice type ID
            - secret_id: Tencent Cloud TTS SecretId (optional, uses cos credentials if not provided)
            - secret_key: Tencent Cloud TTS SecretKey (optional, uses cos credentials if not provided)
            - cos_secret_id: Tencent Cloud COS SecretId
            - cos_secret_key: Tencent Cloud COS SecretKey
            - bucket_name: COS Bucket name (default: ti-aoi)
            - app_id: COS App ID (default: 1257195185)
            - region: COS region (default: ap-guangzhou)
    
    Returns:
        Dictionary with Code, Msg, AudioUrl
    """
    try:
        # Core parameters
        Text = params.get('Text', '')
        VoiceType = params.get('VoiceType', '')
        VoiceName = params.get('VoiceName', '')
        
        # If VoiceName provided, convert to VoiceType
        if VoiceName and not VoiceType:
            reverse_voice_map = {v: k for k, v in VOICE_TYPES.items()}
            if VoiceName in reverse_voice_map:
                VoiceType = reverse_voice_map[VoiceName]
            else:
                return {
                    "Code": 1,
                    "Msg": f"Voice not found: {VoiceName}, available: {', '.join(VOICE_TYPES.values())}",
                    "AudioUrl": ""
                }
        
        # Ensure VoiceType is integer
        if VoiceType:
            try:
                VoiceType = int(VoiceType)
            except (ValueError, TypeError):
                return {
                    "Code": 1,
                    "Msg": f"VoiceType must be a number: {VoiceType}",
                    "AudioUrl": ""
                }
        
        # Credentials - prefer separate TTS credentials, fallback to COS credentials
        cos_secret_id = params.get("cos_secret_id", "").strip()
        cos_secret_key = params.get("cos_secret_key", "").strip()
        tts_secret_id = params.get("secret_id", "").strip() or cos_secret_id
        tts_secret_key = params.get("secret_key", "").strip() or cos_secret_key
        
        # COS configuration
        bucket_name = params.get("bucket_name", "ti-aoi")
        app_id = params.get("app_id", "1257195185")
        region = params.get("region", "ap-guangzhou")
        
        # Whether to upload to COS (default False, only generate local audio)
        upload_cos = params.get("upload_cos", False)
        if isinstance(upload_cos, str):
            upload_cos = upload_cos.lower() in ('true', '1', 'yes')

        if not Text:
            return {
                "Code": 1,
                "Msg": "Text cannot be empty",
                "AudioUrl": ""
            }

        if not VoiceType:
            return {
                "Code": 1,
                "Msg": "VoiceType cannot be empty",
                "AudioUrl": "",
                "VoiceTypes": VOICE_TYPES
            }

        if not tts_secret_id or not tts_secret_key:
            return {
                "Code": 1,
                "Msg": "Missing Tencent Cloud credentials (secret_id or secret_key)",
                "AudioUrl": ""
            }
        
        if not cos_secret_id or not cos_secret_key:
            cos_secret_id = tts_secret_id
            cos_secret_key = tts_secret_key

        # Request TTS generation
        tts_result = tts_main({
            "Text": Text, 
            "VoiceType": VoiceType, 
            "secret_id": tts_secret_id, 
            "secret_key": tts_secret_key
        })
        
        # Check TTS result
        if tts_result["Code"] != 0:
            return {
                "Code": tts_result["Code"],
                "Msg": tts_result["Msg"],
                "AudioUrl": ""
            }
        
        filename = tts_result["filename"]

        # Upload to COS if requested
        if upload_cos:
            try:
                object_key = f"podcast/{filename}"
                audio_url = _upload_to_cos(
                    filename, object_key, 
                    cos_secret_id, cos_secret_key,
                    bucket_name, app_id, region
                )
            except Exception as e:
                # Clean up local file
                try:
                    if os.path.exists(filename):
                        os.remove(filename)
                except:
                    pass
                return {
                    "Code": 2,
                    "Msg": f"COS upload error: {str(e)}",
                    "AudioUrl": ""
                }

            # Clean up local file
            try:
                if os.path.exists(filename):
                    os.remove(filename)
            except:
                pass

            return {
                "Code": 0,
                "Msg": "success",
                "AudioUrl": audio_url
            }
        else:
            # Return local file path
            return {
                "Code": 0,
                "Msg": "success",
                "AudioUrl": filename
            }

    except Exception as e:
        return {
            "Code": 3,
            "Msg": f"Processing error: {str(e)}",
            "AudioUrl": ""
        }


if __name__ == "__main__":
    # Example usage - credentials should be set via environment variables
    import os
    secret_id = os.environ.get("TENCENT_TTS_SECRET_ID", "YOUR_SECRET_ID_HERE")
    secret_key = os.environ.get("TENCENT_TTS_SECRET_KEY", "YOUR_SECRET_KEY_HERE")
    
    result = main({
        "Text": "Hello, welcome to the podcast!",
        "VoiceType": 502006,
        "secret_id": secret_id,
        "secret_key": secret_key
    })
    print(json.dumps(result, ensure_ascii=False, indent=2))
