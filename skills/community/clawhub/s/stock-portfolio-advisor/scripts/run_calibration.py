"""One command: build historical panel, validate candidate weights, optionally activate."""
import argparse
from pathlib import Path
from build_backtest_dataset import build
from calibrate_weights import calibrate, write_summary
from weight_registry import read_json, write_json, read_registry, activate, DEFAULT_PATH


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest',required=True);p.add_argument('--as-of',required=True);p.add_argument('--output-dir',required=True)
    p.add_argument('--config');p.add_argument('--strategy');p.add_argument('--profiles',help='Comma-separated profiles')
    p.add_argument('--weights-file',default=str(DEFAULT_PATH));p.add_argument('--apply',action='store_true')
    a=p.parse_args()
    try:
        manifest=Path(a.manifest);out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
        dataset=build(read_json(manifest),manifest.parent)
        write_json(out/'dataset.json',dataset)
        report=calibrate(dataset,a.as_of,read_registry(a.weights_file),read_json(a.config) if a.config else None,
                         read_json(a.strategy) if a.strategy else None,a.profiles.split(',') if a.profiles else None)
        write_json(out/'calibration.json',report)
        status={'status':'review_only'}
        if a.apply:
            if dataset['synthetic']:
                status={'status':'refused','reason':'Synthetic results cannot activate production weights'}
            else:status=activate(report,a.weights_file)
        write_json(out/'activation.json',status)
        write_summary(out/'calibration.md',report,status)
        print('[OK] '+str(status)+'; summary='+str(out/'calibration.md'))
        return 2 if status['status']=='refused' else 0
    except (ValueError,KeyError,TypeError,OSError) as exc:p.error(str(exc))


if __name__=='__main__':raise SystemExit(main())
