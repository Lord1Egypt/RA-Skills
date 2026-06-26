"""
远程视频帧提取服务
支持从远程 URL 按时间/帧号提取视频帧，无需下载完整文件
"""
import requests
import struct
import logging
import os
import tempfile
from typing import Optional, Dict, List

import cv2
import numpy as np

from utils import (
    get_media_source_name,
    is_remote_source,
    prepare_output_path,
    validate_media_source,
    validate_video_url,
)

logger = logging.getLogger(__name__)


class RemoteVideoFrameExtractor:
    """远程视频帧提取器 - 通过解析 MP4 结构实现部分下载"""

    # MP4 Box 类型常量
    BOX_TYPE_MOOV = b'moov'
    BOX_TYPE_TRAK = b'trak'
    BOX_TYPE_MDIA = b'mdia'
    BOX_TYPE_MINF = b'minf'
    BOX_TYPE_STBL = b'stbl'
    BOX_TYPE_STSD = b'stsd'
    BOX_TYPE_STSS = b'stss'
    BOX_TYPE_STCO = b'stco'
    BOX_TYPE_CO64 = b'co64'
    BOX_TYPE_STSZ = b'stsz'
    BOX_TYPE_STSC = b'stsc'

    def __init__(self, video_url: str, timeout: int = 30):
        validate_video_url(video_url)
        self.video_url = video_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

        self.file_size = 0
        self.width = 0
        self.height = 0
        self.codec_type = None
        self.timescale = 0
        self.duration = 0
        self.stts = []
        self.stss = []
        self.stco = []
        self.stsz = []
        self.stsc = []
        self.nal_length_size = 4
        self.vps_sps_pps_nalus = []

        self._init_video_info()

    def _init_video_info(self):
        try:
            self.file_size = self._get_file_size()
            self._find_and_parse_moov()
        except Exception as e:
            logger.error(f"视频信息解析失败: {e}")
            raise

    def _get_file_size(self) -> int:
        response = self.session.head(self.video_url, timeout=self.timeout)
        if 'content-length' in response.headers:
            return int(response.headers['content-length'])
        response = self.session.get(self.video_url, stream=True, timeout=self.timeout)
        return int(response.headers.get('content-length', 0))

    def _download_range(self, start: int, end: int) -> bytes:
        headers = {'Range': f'bytes={start}-{end}'}
        response = self.session.get(self.video_url, headers=headers, timeout=self.timeout)
        if response.status_code in [200, 206]:
            return response.content
        raise Exception(f"HTTP Range 请求失败: {response.status_code}")

    def _find_and_parse_moov(self):
        pos = 0
        probe_size = min(64 * 1024, self.file_size)
        probe_data = self._download_range(0, probe_size - 1)

        while pos < self.file_size:
            if pos + 8 > len(probe_data):
                header_bytes = self._download_range(pos, min(pos + 7, self.file_size - 1))
                if len(header_bytes) < 8:
                    break
            else:
                header_bytes = probe_data[pos:pos + 8]

            box_size = struct.unpack('>I', header_bytes[0:4])[0]
            box_type = header_bytes[4:8]

            if box_size == 1:
                if pos + 16 > len(probe_data):
                    ext_header = self._download_range(pos, min(pos + 15, self.file_size - 1))
                else:
                    ext_header = probe_data[pos:pos + 16]
                if len(ext_header) < 16:
                    break
                box_size = struct.unpack('>Q', ext_header[8:16])[0]

            if box_size == 0:
                box_size = self.file_size - pos

            if box_size < 8:
                break

            if box_type == self.BOX_TYPE_MOOV:
                moov_data = self._download_range(pos, pos + box_size - 1)
                self._parse_moov(moov_data)
                return

            pos += box_size

        tail_size = min(5 * 1024 * 1024, self.file_size)
        tail_data = self._download_range(self.file_size - tail_size, self.file_size - 1)
        tail_base_offset = self.file_size - tail_size

        scan_pos = 0
        while scan_pos < len(tail_data) - 8:
            box_size = struct.unpack('>I', tail_data[scan_pos:scan_pos + 4])[0]
            box_type = tail_data[scan_pos + 4:scan_pos + 8]

            if box_size == 1 and scan_pos + 16 <= len(tail_data):
                box_size = struct.unpack('>Q', tail_data[scan_pos + 8:scan_pos + 16])[0]

            if box_size < 8:
                scan_pos += 1
                continue

            if box_type == self.BOX_TYPE_MOOV:
                actual_offset = tail_base_offset + scan_pos
                moov_data = self._download_range(actual_offset, actual_offset + box_size - 1)
                self._parse_moov(moov_data)
                return

            scan_pos += box_size

        raise Exception("未找到 moov box")

    def _parse_moov(self, moov_data: bytes):
        pos = 8
        while pos < len(moov_data) - 8:
            box_size = struct.unpack('>I', moov_data[pos:pos+4])[0]
            if moov_data[pos+4:pos+8] == self.BOX_TYPE_TRAK:
                self._parse_trak(moov_data[pos:pos+box_size])
            pos += box_size if box_size > 0 else 1

    def _parse_trak(self, trak_data: bytes):
        is_video = False
        mdia_offset, mdia_size = 0, 0
        pos = 8
        while pos < len(trak_data) - 8:
            box_size = struct.unpack('>I', trak_data[pos:pos+4])[0]
            if trak_data[pos+4:pos+8] == self.BOX_TYPE_MDIA:
                mdia_offset, mdia_size = pos, box_size
                m_pos = pos + 8
                while m_pos < pos + box_size - 8:
                    m_size = struct.unpack('>I', trak_data[m_pos:m_pos+4])[0]
                    if trak_data[m_pos+4:m_pos+8] == b'hdlr':
                        if trak_data[m_pos+16:m_pos+20] == b'vide':
                            is_video = True
                        break
                    m_pos += m_size if m_size > 0 else 1
            pos += box_size if box_size > 0 else 1

        if is_video and mdia_size > 0:
            self._parse_mdia(trak_data[mdia_offset:mdia_offset+mdia_size])

    def _parse_mdia(self, mdia_data: bytes):
        pos = 8
        while pos < len(mdia_data) - 8:
            box_size = struct.unpack('>I', mdia_data[pos:pos+4])[0]
            box_type = mdia_data[pos+4:pos+8]

            if box_type == b'mdhd':
                version = mdia_data[pos+8]
                if version == 0:
                    self.timescale = struct.unpack('>I', mdia_data[pos+20:pos+24])[0]
                    self.duration = struct.unpack('>I', mdia_data[pos+24:pos+28])[0]
                else:
                    self.timescale = struct.unpack('>I', mdia_data[pos+28:pos+32])[0]
                    self.duration = struct.unpack('>Q', mdia_data[pos+32:pos+40])[0]

            elif box_type == self.BOX_TYPE_MINF:
                self._parse_minf(mdia_data[pos:pos+box_size])
            pos += box_size if box_size > 0 else 1

    def _parse_minf(self, minf_data: bytes):
        pos = 8
        while pos < len(minf_data) - 8:
            box_size = struct.unpack('>I', minf_data[pos:pos+4])[0]
            if minf_data[pos+4:pos+8] == self.BOX_TYPE_STBL:
                self._parse_stbl(minf_data[pos:pos+box_size])
            pos += box_size if box_size > 0 else 1

    def _parse_stbl(self, stbl_data: bytes):
        pos = 8
        while pos < len(stbl_data) - 8:
            box_size = struct.unpack('>I', stbl_data[pos:pos+4])[0]
            box_type = stbl_data[pos+4:pos+8]

            if box_type == self.BOX_TYPE_STSD:
                self._parse_stsd(stbl_data[pos:pos+box_size])
            elif box_type == self.BOX_TYPE_STSS:
                entry_count = struct.unpack('>I', stbl_data[pos+12:pos+16])[0]
                for i in range(entry_count):
                    self.stss.append(struct.unpack('>I', stbl_data[pos+16+i*4:pos+20+i*4])[0])
            elif box_type == self.BOX_TYPE_STCO:
                entry_count = struct.unpack('>I', stbl_data[pos+12:pos+16])[0]
                for i in range(entry_count):
                    self.stco.append(struct.unpack('>I', stbl_data[pos+16+i*4:pos+20+i*4])[0])
            elif box_type == self.BOX_TYPE_CO64:
                entry_count = struct.unpack('>I', stbl_data[pos+12:pos+16])[0]
                for i in range(entry_count):
                    self.stco.append(struct.unpack('>Q', stbl_data[pos+16+i*8:pos+24+i*8])[0])
            elif box_type == self.BOX_TYPE_STSZ:
                sample_size = struct.unpack('>I', stbl_data[pos+12:pos+16])[0]
                sample_count = struct.unpack('>I', stbl_data[pos+16:pos+20])[0]
                if sample_size == 0:
                    for i in range(sample_count):
                        self.stsz.append(struct.unpack('>I', stbl_data[pos+20+i*4:pos+24+i*4])[0])
                else:
                    self.stsz = [sample_size] * sample_count
            elif box_type == self.BOX_TYPE_STSC:
                entry_count = struct.unpack('>I', stbl_data[pos+12:pos+16])[0]
                for i in range(entry_count):
                    o = pos + 16 + i * 12
                    self.stsc.append({
                        'first_chunk': struct.unpack('>I', stbl_data[o:o+4])[0],
                        'samples_per_chunk': struct.unpack('>I', stbl_data[o+4:o+8])[0]
                    })
            elif box_type == b'stts':
                entry_count = struct.unpack('>I', stbl_data[pos+12:pos+16])[0]
                for i in range(entry_count):
                    count = struct.unpack('>I', stbl_data[pos+16+i*8:pos+20+i*8])[0]
                    delta = struct.unpack('>I', stbl_data[pos+20+i*8:pos+24+i*8])[0]
                    self.stts.append({'count': count, 'delta': delta})

            pos += box_size if box_size > 0 else 1

    def _parse_stsd(self, stsd_data: bytes):
        pos = 16
        while pos < len(stsd_data) - 8:
            box_size = struct.unpack('>I', stsd_data[pos:pos+4])[0]
            box_type = stsd_data[pos+4:pos+8]

            if box_type in [b'avc1', b'hvc1', b'hev1']:
                self.codec_type = 'h264' if box_type == b'avc1' else 'h265'
                self.width = struct.unpack('>H', stsd_data[pos+32:pos+34])[0]
                self.height = struct.unpack('>H', stsd_data[pos+34:pos+36])[0]

                v_pos = pos + 86
                while v_pos < pos + box_size - 8:
                    v_size = struct.unpack('>I', stsd_data[v_pos:v_pos+4])[0]
                    v_type = stsd_data[v_pos+4:v_pos+8]
                    config_data = stsd_data[v_pos+8:v_pos+v_size]
                    if v_type == b'avcC':
                        self._parse_avcc(config_data)
                    elif v_type == b'hvcC':
                        self._parse_hvcc(config_data)
                    v_pos += v_size if v_size > 0 else 1
            pos += box_size if box_size > 0 else 1

    def _parse_avcc(self, data: bytes):
        self.nal_length_size = (data[4] & 0x03) + 1
        pos = 6
        start_code = b'\x00\x00\x00\x01'
        num_sps = data[5] & 0x1F
        for _ in range(num_sps):
            sps_len = struct.unpack('>H', data[pos:pos+2])[0]
            pos += 2
            self.vps_sps_pps_nalus.append(start_code + data[pos:pos+sps_len])
            pos += sps_len
        num_pps = data[pos]
        pos += 1
        for _ in range(num_pps):
            pps_len = struct.unpack('>H', data[pos:pos+2])[0]
            pos += 2
            self.vps_sps_pps_nalus.append(start_code + data[pos:pos+pps_len])
            pos += pps_len

    def _parse_hvcc(self, data: bytes):
        self.nal_length_size = (data[21] & 0x03) + 1
        num_arrays = data[22]
        pos = 23
        start_code = b'\x00\x00\x00\x01'
        for _ in range(num_arrays):
            pos += 1
            num_nalus = struct.unpack('>H', data[pos:pos+2])[0]
            pos += 2
            for _ in range(num_nalus):
                nal_len = struct.unpack('>H', data[pos:pos+2])[0]
                pos += 2
                self.vps_sps_pps_nalus.append(start_code + data[pos:pos+nal_len])
                pos += nal_len

    def get_sample_position(self, sample_number: int) -> Optional[Dict]:
        if not self.stsz or sample_number > len(self.stsz) or sample_number < 1:
            return None
        target_chunk, samples_so_far, first_sample_in_chunk = 1, 0, 1

        for i in range(len(self.stsc)):
            current = self.stsc[i]
            next_chunk = self.stsc[i+1]['first_chunk'] if i+1 < len(self.stsc) else len(self.stco) + 1
            chunks_in_rule = next_chunk - current['first_chunk']
            samples_in_rule = chunks_in_rule * current['samples_per_chunk']

            if samples_so_far + samples_in_rule >= sample_number:
                chunks_to_target = (sample_number - samples_so_far - 1) // current['samples_per_chunk']
                target_chunk = current['first_chunk'] + chunks_to_target
                first_sample_in_chunk = samples_so_far + chunks_to_target * current['samples_per_chunk'] + 1
                break
            samples_so_far += samples_in_rule

        if target_chunk > len(self.stco):
            return None
        offset = self.stco[target_chunk - 1]
        for i in range(first_sample_in_chunk, sample_number):
            offset += self.stsz[i - 1]
        return {'offset': offset, 'size': self.stsz[sample_number - 1]}

    def _get_frame_number_by_time(self, seconds: float) -> int:
        if not self.stts or not self.timescale:
            return max(1, int(seconds * 30.0))

        target_ticks = int(seconds * self.timescale)
        current_ticks = 0
        current_sample = 1

        for entry in self.stts:
            entry_ticks = entry['count'] * entry['delta']
            if current_ticks + entry_ticks > target_ticks:
                ticks_into_entry = target_ticks - current_ticks
                samples_into_entry = ticks_into_entry // entry['delta']
                return current_sample + samples_into_entry

            current_ticks += entry_ticks
            current_sample += entry['count']

        return current_sample - 1 if current_sample > 1 else 1

    def extract_frame_by_time(self, seconds: float) -> Optional[np.ndarray]:
        target_frame = self._get_frame_number_by_time(seconds)
        if self.stsz and target_frame > len(self.stsz):
            target_frame = len(self.stsz)
        target_frame = max(1, target_frame)
        return self.extract_frame(target_frame)

    def extract_frame(self, frame_number: int) -> Optional[np.ndarray]:
        keyframe = frame_number
        if self.stss:
            keyframes = [kf for kf in self.stss if kf <= frame_number]
            keyframe = max(keyframes) if keyframes else self.stss[0]

        sample_infos = []
        min_offset = float('inf')
        max_offset = 0

        for f in range(keyframe, frame_number + 1):
            info = self.get_sample_position(f)
            if not info:
                logger.warning(f"无法获取帧 {f} 的位置信息")
                return None
            sample_infos.append(info)
            min_offset = min(min_offset, info['offset'])
            max_offset = max(max_offset, info['offset'] + info['size'] - 1)

        raw_data = self._download_range(min_offset, max_offset)

        annexb_stream = bytearray()
        for nalu in self.vps_sps_pps_nalus:
            annexb_stream.extend(nalu)

        for info in sample_infos:
            local_offset = info['offset'] - min_offset
            sample_data = raw_data[local_offset : local_offset + info['size']]
            annexb_stream.extend(self._convert_sample_to_annexb(sample_data))

        frames_to_step = frame_number - keyframe + 1
        return self._decode_video_stream(bytes(annexb_stream), frames_to_step)

    def _convert_sample_to_annexb(self, sample_data: bytes) -> bytes:
        result = bytearray()
        pos = 0
        start_code = b'\x00\x00\x00\x01'

        while pos < len(sample_data):
            if pos + self.nal_length_size > len(sample_data):
                break
            if self.nal_length_size == 4:
                nal_len = struct.unpack('>I', sample_data[pos:pos+4])[0]
            elif self.nal_length_size == 2:
                nal_len = struct.unpack('>H', sample_data[pos:pos+2])[0]
            else:
                nal_len = sample_data[pos]

            pos += self.nal_length_size
            if pos + nal_len > len(sample_data):
                break

            result.extend(start_code)
            result.extend(sample_data[pos:pos+nal_len])
            pos += nal_len
        return bytes(result)

    def _decode_video_stream(self, video_data: bytes, target_read_count: int) -> Optional[np.ndarray]:
        if not video_data:
            return None

        ext = '.h265' if self.codec_type == 'h265' else '.h264'
        temp_path = None
        target_frame_img = None

        try:
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as f:
                f.write(video_data)
                temp_path = f.name

            cap = cv2.VideoCapture(temp_path)
            for i in range(target_read_count):
                ret, frame = cap.read()
                if not ret:
                    break
                target_frame_img = frame
            cap.release()
            
            if target_frame_img is not None:
                return cv2.cvtColor(target_frame_img, cv2.COLOR_BGR2RGB)

        except Exception as e:
            logger.error(f"视频流解码失败: {e}")
            return None
        finally:
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)
        return None

    def get_video_info(self) -> Dict:
        duration_sec = self.duration / self.timescale if self.timescale else 0
        total_frames = len(self.stsz) if self.stsz else 0
        fps = round(total_frames / duration_sec, 3) if duration_sec > 0 and total_frames else 30
        return {
            'width': self.width,
            'height': self.height,
            'codec': self.codec_type,
            'fps': fps,
            'duration': duration_sec,
            'total_frames': total_frames
        }


def get_local_video_info(video_path: str) -> Dict:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"无法打开本地视频: {video_path}")

    try:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
        fps = float(cap.get(cv2.CAP_PROP_FPS) or 0)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        duration = total_frames / fps if fps > 0 and total_frames else 0
        return {
            'width': width,
            'height': height,
            'codec': 'unknown',
            'fps': round(fps, 3) if fps > 0 else 0,
            'duration': duration,
            'total_frames': total_frames,
        }
    finally:
        cap.release()


def extract_thumbnail_from_local(
    video_path: str,
    time_seconds: float = None,
    frame_number: int = None
) -> tuple:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None, None

    try:
        if frame_number is not None:
            cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, int(frame_number) - 1))
            used_method = f'frame_{frame_number}'
        else:
            ts = time_seconds if time_seconds is not None else 0
            cap.set(cv2.CAP_PROP_POS_MSEC, max(0, float(ts)) * 1000)
            used_method = f'time_{ts}s'

        ret, frame = cap.read()
        if not ret:
            return None, used_method
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), used_method
    finally:
        cap.release()


def extract_thumbnail_from_url(
    video_url: str,
    time_seconds: float = None,
    frame_number: int = None,
    save_path: str = None,
    resize_width: int = None,
    quality: int = 85,
    overwrite: bool = True,
    media_roots=None
) -> dict:
    """
    从远程视频提取封面（流式，只下载必要部分）
    """
    try:
        video_url = validate_media_source(video_url, media_roots=media_roots)
        save_path = prepare_output_path(
            output_path=save_path,
            default_dir='output/thumbs',
            default_name=get_media_source_name(video_url, fallback='thumbnail'),
            extension='.jpg',
            overwrite=overwrite
        )
    except ValueError as e:
        return {'status': 'error', 'message': str(e)}
    
    if is_remote_source(video_url):
        extractor = RemoteVideoFrameExtractor(video_url, timeout=60)

        if frame_number is not None:
            frame = extractor.extract_frame(frame_number)
            used_method = f'frame_{frame_number}'
        else:
            ts = time_seconds if time_seconds is not None else 0
            frame = extractor.extract_frame_by_time(ts)
            used_method = f'time_{ts}s'
        video_info = extractor.get_video_info()
    else:
        frame, used_method = extract_thumbnail_from_local(video_url, time_seconds, frame_number)
        try:
            video_info = get_local_video_info(video_url)
        except ValueError as e:
            return {'status': 'error', 'message': str(e)}
    
    if frame is None:
        return {'status': 'error', 'message': 'Failed to extract frame'}
    
    video_info['extract_method'] = used_method
    
    result = {
        'status': 'success',
        'video_info': video_info,
        'shape': frame.shape
    }
    
    if resize_width:
        h, w = frame.shape[:2]
        scale = resize_width / w
        new_h = int(h * scale)
        frame_to_save = cv2.resize(frame, (resize_width, new_h))
    else:
        frame_to_save = frame

    bgr_frame = cv2.cvtColor(frame_to_save, cv2.COLOR_RGB2BGR)
    saved = cv2.imwrite(save_path, bgr_frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    if not saved:
        return {'status': 'error', 'message': f'封面保存失败: {save_path}'}
    result['saved_path'] = save_path
    
    return result
