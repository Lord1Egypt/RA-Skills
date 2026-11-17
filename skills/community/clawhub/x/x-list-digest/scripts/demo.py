"""Offline synthetic demo; never fetches X or publishes messages."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tests'))
from test_pipeline import PipelineTest
from analyze import enrich
from render import render
from persist import persist
from common import write
if __name__=='__main__':
    output=Path(sys.argv[1] if len(sys.argv)>1 else 'demo-output');output.mkdir(parents=True,exist_ok=True)
    fixture=PipelineTest();fixture.setUp();fixture.meta['list_name']='Offline synthetic demonstration（not realXdata）'
    rows=enrich(fixture.raw,fixture.analysis)
    write(output/'raw.json',fixture.raw);write(output/'enriched.json',rows);write(output/'metadata.json',fixture.meta)
    (output/'report.md').write_text(render(rows,fixture.meta))
    persist(str(output/'digest.db'),rows,fixture.meta,str(output/'raw.json'),str(output/'enriched.json'))
    print(output.resolve()/'report.md')
