"""
Video Merger 单元测试
"""
import os
import tempfile
import pytest
from src.video_merger import VideoMerger

class TestVideoMerger:
    def test_init(self):
        """测试初始化"""
        merger = VideoMerger()
        assert merger is not None

    def test_get_sorted_videos(self, tmpdir):
        """测试视频排序功能"""
        # 创建测试文件
        files = [
            "003_test.mp4",
            "001_test.mp4", 
            "002_test.mp4",
            "10_test.mp4",
            "not_a_video.txt"
        ]
        for f in files:
            tmpdir.join(f).write("")

        merger = VideoMerger()
        sorted_videos = merger.get_sorted_videos(str(tmpdir))
        
        # 验证排序结果
        assert len(sorted_videos) == 4
        assert os.path.basename(sorted_videos[0]) == "001_test.mp4"
        assert os.path.basename(sorted_videos[1]) == "002_test.mp4"
        assert os.path.basename(sorted_videos[2]) == "003_test.mp4"
        assert os.path.basename(sorted_videos[3]) == "10_test.mp4"

    def test_get_sorted_videos_empty(self, tmpdir):
        """测试空目录"""
        merger = VideoMerger()
        with pytest.raises(ValueError):
            merger.get_sorted_videos(str(tmpdir))

    def test_invalid_directory(self):
        """测试无效目录"""
        merger = VideoMerger()
        with pytest.raises(FileNotFoundError):
            merger.get_sorted_videos("/invalid/directory/that/does/not/exist")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
