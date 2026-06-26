#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
import os
import sys
import json
import numpy as np
from pydub import AudioSegment
import tempfile
import signal

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 最大100MB

# 允许的音频格式
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac', 'ogg', 'm4a'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_waveform_data(file_path, num_points=1000):
    """生成音频波形数据"""
    try:
        audio = AudioSegment.from_file(file_path)
        samples = np.array(audio.get_array_of_samples())
        # 合并声道
        if audio.channels == 2:
            samples = samples.reshape((-1, 2)).mean(axis=1)
        # 采样到指定点数
        if len(samples) > num_points:
            samples = samples[::len(samples)//num_points][:num_points]
        # 归一化
        samples = samples / np.max(np.abs(samples))
        return {
            'duration': audio.duration_seconds * 1000,
            'waveform': samples.tolist(),
            'sample_rate': audio.frame_rate
        }
    except Exception as e:
        return {'error': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '没有选择文件'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    if file and allowed_file(file.filename):
        # 保存临时文件
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(temp_path)
        # 生成波形数据
        waveform = get_waveform_data(temp_path)
        # 删除临时文件
        os.unlink(temp_path)
        return jsonify(waveform)
    return jsonify({'error': '不支持的文件格式'}), 400

@app.route('/shutdown', methods=['POST'])
def shutdown():
    """关闭服务"""
    try:
        import sys
        os.kill(os.getpid(), signal.SIGTERM)
        return jsonify({'status': 'success', 'message': '服务已关闭'})
    except:
        try:
            # Windows兼容退出
            os._exit(0)
        except:
            return jsonify({'status': 'error', 'message': '关闭失败，请手动停止服务'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=698, debug=False)
