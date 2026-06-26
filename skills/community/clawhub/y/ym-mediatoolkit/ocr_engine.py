import importlib.util


def is_ocr_available() -> bool:
    return importlib.util.find_spec('paddleocr') is not None


def recognize_frame_texts(
    video_source: str,
    sample_interval_sec: float = 1.0,
    crop_bottom_ratio: float = 0.35,
) -> dict:
    if not is_ocr_available():
        return {
            'status': 'error',
            'message': '缺少 OCR 依赖: paddleocr。请运行: pip install -r requirements.txt',
            'code': 'missing_ocr_dependency',
        }

    try:
        import cv2
        from paddleocr import PaddleOCR
    except Exception as e:
        return {
            'status': 'error',
            'message': f'OCR 引擎加载失败: {e}',
            'code': 'ocr_engine_error',
        }

    try:
        ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
        cap = cv2.VideoCapture(video_source)
        if not cap.isOpened():
            return {'status': 'error', 'message': '无法打开视频进行 OCR', 'code': 'ocr_video_open_failed'}

        fps = float(cap.get(cv2.CAP_PROP_FPS) or 25)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        duration_sec = total_frames / fps if fps > 0 and total_frames else 0
        interval = max(0.2, float(sample_interval_sec))
        captions = []
        timestamp = 0.0

        while timestamp <= duration_sec or (not captions and timestamp == 0):
            cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
            ok, frame = cap.read()
            if not ok:
                break

            height = frame.shape[0]
            crop_start = int(height * (1 - max(0.05, min(1.0, crop_bottom_ratio))))
            region = frame[crop_start:height, :]
            ocr_result = ocr.ocr(region, cls=True)
            texts = []
            scores = []
            for line_group in ocr_result or []:
                for item in line_group or []:
                    if len(item) < 2:
                        continue
                    text, score = item[1]
                    text = (text or '').strip()
                    if text:
                        texts.append(text)
                        scores.append(float(score or 0))
            caption_text = ' '.join(texts).strip()
            if caption_text:
                start_us = int(timestamp * 1_000_000)
                end_us = int((timestamp + interval) * 1_000_000)
                captions.append({
                    'captionTxt': caption_text,
                    'startTimeUs': start_us,
                    'endTimeUs': max(end_us, start_us + 1),
                    'source': 'ocr',
                    'confidence': round(sum(scores) / len(scores), 4) if scores else 0,
                })
            timestamp += interval

        cap.release()
        return {
            'status': 'success',
            'captions': captions,
            'engine': 'paddleocr',
            'sampleIntervalSec': interval,
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e), 'code': 'ocr_failed'}
