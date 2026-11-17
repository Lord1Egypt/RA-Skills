"""Offline tests for query-intel."""
import json
import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
INTEL = os.path.join(HERE, '..', 'intel.py')


def run(*args):
    r = subprocess.run([sys.executable, INTEL] + list(args),
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return r.stdout


def test_all():
    sb = json.loads(run('stepback', 'Qwen3 embedding reranker pricing'))
    assert 'principle' in sb and len(sb['sub_questions']) >= 2, sb
    dc = json.loads(run('decompose', 'compare BM25 and dense retrieval'))
    assert len(dc['steps']) >= 3, dc
    g1 = json.loads(run('gate', 'Qwen3 reranker pricing 2026'))
    assert g1['decision'] == 'retrieve', g1
    g2 = json.loads(run('gate', 'capital of France', '--conf', '0.95'))
    assert g2['decision'] == 'skip', g2
    ol = json.loads(run('outline', 'unified orchestration'))
    assert any('Breakthrough' in s['h'] for s in ol['sections']), ol
    print('test_all PASS')


if __name__ == '__main__':
    test_all()
