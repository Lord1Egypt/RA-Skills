#!/usr/bin/env python3
"""评分CLI：python score_engine.py --input metrics.json --output result.json [--prev old.json]"""
import argparse
import json
from pathlib import Path
from value_model import VERSION, evaluate, compute_delta, template
from weight_registry import read_registry, read_json


def main():
    parser = argparse.ArgumentParser(description=f'A股价值评分引擎 {VERSION}')
    parser.add_argument('--input')
    parser.add_argument('--output')
    parser.add_argument('--prev')
    parser.add_argument('--weights-file',help='可选权重注册表；默认config/weights.json')
    parser.add_argument('--template',action='store_true')
    args = parser.parse_args()
    if args.template:
        result = template()
    else:
        if not args.input:
            parser.error('需要--input或--template')
        try:
            override = None
            warning = None
            if args.weights_file:
                try:
                    override = read_registry(args.weights_file)
                except (ValueError, OSError, TypeError):
                    override = {'schema_version':1, 'releases':[]}
                    warning = '指定权重文件无效，回退内置权重'
            result = evaluate(read_json(args.input),registry=override)
            if warning: result['weight_warnings'].append(warning)
            if args.prev:
                result = compute_delta(result,read_json(args.prev))
        except (ValueError,TypeError) as exc:
            parser.error(str(exc))
    output = json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)
    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(output,encoding='utf-8')
        print(f'[OK] {target}')
    else:
        print(output)


if __name__=='__main__':
    main()
