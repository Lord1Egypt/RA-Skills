#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import SearchListingOptimizer, handle


def test_platform_detection_amazon():
    opt = SearchListingOptimizer('Amazon A9 listing audit for skincare product')
    assert opt.platform == 'Amazon'


def test_platform_detection_xiaohongshu():
    opt = SearchListingOptimizer('Xiaohongshu SEO audit for skincare brand')
    assert opt.platform == 'Xiaohongshu'


def test_goal_detection_new_listing():
    opt = SearchListingOptimizer('New skincare product listing on Amazon')
    assert opt.goal == 'New Listing'


def test_goal_detection_conversion():
    opt = SearchListingOptimizer('Improve conversion on our Amazon listing with high traffic but low sales')
    assert opt.goal == 'Conversion Improvement'


def test_render_contains_sections():
    output = handle('Audit our Amazon skincare listing for A9 visibility')
    assert output.startswith('# Search Listing Optimization Brief')
    assert '## Listing Attribute Scorecard' in output
    assert '## Keyword Strategy Angles' in output
    assert '## Prioritized Action List' in output


def test_dict_input_supported():
    output = handle({
        'platform': 'Amazon',
        'product': 'skincare serum',
        'goal': 'Visibility Boost',
        'listing': 'Need title and bullet optimization'
    })
    assert '# Search Listing Optimization Brief' in output
    assert 'Amazon' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
