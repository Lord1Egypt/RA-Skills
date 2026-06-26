#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import ReadingProgressTracker, handle


def test_page_progress_extraction():
    tracker = ReadingProgressTracker('I am reading Deep Work on Kindle, page 87, for learning.')
    assert tracker.current_reads[0]['progress'].lower() == 'page 87'
    assert tracker.current_reads[0]['next_stop'] == 'Page 102'


def test_format_detection():
    tracker = ReadingProgressTracker('I am listening to Atomic Habits as an audiobook during walks.')
    assert tracker.current_reads[0]['format'] == 'audiobook'


def test_output_sections():
    output = handle('I am reading The Anxious Generation in print, chapter 3. Idea: attention is trainable.')
    assert output.startswith('# Reading Dashboard')
    assert '## Current Reads' in output
    assert '## Session Note' in output
    assert '## Queue' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
