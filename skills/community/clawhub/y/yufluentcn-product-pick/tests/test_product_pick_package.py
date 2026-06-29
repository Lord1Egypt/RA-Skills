"""yufluentcn-product-pick 技能包测试。"""

from __future__ import annotations

import importlib.util
import sys
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SKILLS_SHARED = ROOT.parent / "_shared"


def _load_run_module():
    """加载 run.py（与 CLI 相同：scripts → bootstrap → _shared）。"""
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    import bootstrap

    bootstrap.ensure_cloud_client_path(SCRIPTS / "run.py")
    spec = importlib.util.spec_from_file_location("product_pick_run", SCRIPTS / "run.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_product_pick_package_layout():
    assert (ROOT / "SKILL.md").is_file()
    assert (SCRIPTS / "run.py").is_file()
    assert (SKILLS_SHARED / "yufluent_api.py").is_file()
    assert (ROOT / "requirements.txt").is_file()


def test_bootstrap_finds_monorepo_shared():
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    import bootstrap

    resolved = bootstrap.ensure_cloud_client_path(SCRIPTS / "run.py")
    assert resolved.is_dir()
    assert (resolved / "yufluent_api.py").is_file()


def test_build_payload_inline_candidates():
    run = _load_run_module()
    args = Namespace(
        niche="  便携榨汁杯  ",
        product_candidates="platform,title\namazon,A",
        platforms="amazon,tiktok",
        data_source="manual",
        unit_cost=None,
        target_margin=None,
        max_capital=None,
        risk_constraints=None,
        message=None,
        context=None,
        discover=False,
        discover_source=None,
        lang="en",
    )
    payload = run.build_payload(args, product_candidates="platform,title\namazon,A")
    assert payload["niche"] == "便携榨汁杯"
    assert payload["product_candidates"] == "platform,title\namazon,A"
    assert payload["platforms"] == "amazon,tiktok"
    assert payload["data_source"] == "manual"
    assert payload["platform"] == "multi"
    assert payload["lang"] == "en"
    assert "unit_cost" not in payload


def test_build_payload_optional_fields_and_file_candidates(tmp_path: Path):
    run = _load_run_module()
    data_file = tmp_path / "market.txt"
    data_file.write_text("platform,bsr\namazon,#1200", encoding="utf-8")
    args = Namespace(
        niche="榨汁杯",
        product_candidates=str(data_file),
        platforms="amazon,tiktok,aliexpress",
        data_source="browser_extract",
        unit_cost=" ¥35 ",
        target_margin="30%",
        max_capital="50000",
        risk_constraints="避免侵权",
        message="老板要看",
        context="Q2 备货",
        discover=False,
        discover_source=None,
        lang="zh",
    )
    payload = run.build_payload(
        args,
        product_candidates="platform,bsr\namazon,#1200",
    )
    assert payload["unit_cost"] == "¥35"
    assert payload["max_capital"] == "50000"
    assert payload["message"] == "老板要看"
    assert payload["context"] == "Q2 备货"


def test_read_text_arg_nonexistent_path_is_literal():
    _load_run_module()
    from cloud_cli import read_text_arg

    literal = "./not-a-real-file.csv"
    assert read_text_arg(literal) == literal


def test_read_text_arg_empty_string():
    _load_run_module()
    from cloud_cli import read_text_arg

    assert read_text_arg("") == ""
    assert read_text_arg("   ") == ""


def test_main_success_calls_run_skill_with_payload():
    run = _load_run_module()
    fake = {"formatted_text": '{"verdict":"go"}', "run_id": "hr_test", "model_used": "m1"}

    with patch.object(run, "run_skill", return_value=fake) as mock_run:
        code = run.main(
            [
                "--niche",
                "榨汁杯",
                "--product-candidates",
                "platform,title\namazon,X",
                "--data-source",
                "manual",
            ]
        )

    assert code == 0
    mock_run.assert_called_once()
    skill_id, payload = mock_run.call_args[0][0], mock_run.call_args[0][1]
    assert skill_id == "product-pick"
    assert payload["niche"] == "榨汁杯"
    assert payload["data_source"] == "manual"


def test_main_api_error_exit_codes():
    run = _load_run_module()
    from yufluent_api import YufluentApiError

    argv = ["--niche", "x", "--product-candidates", "a,b", "--data-source", "manual"]

    with patch.object(run, "run_skill", side_effect=YufluentApiError("unauthorized", status=401)):
        assert run.main(argv) == 1

    with patch.object(run, "run_skill", side_effect=YufluentApiError("payment required", status=402)):
        assert run.main(argv) == 2


def test_main_writes_output_file(tmp_path: Path, capsys):
    run = _load_run_module()
    out_path = tmp_path / "report.json"
    fake = {"formatted_text": '{"summary":"ok"}', "run_id": "hr_out"}

    with patch.object(run, "run_skill", return_value=fake):
        code = run.main(
            [
                "--niche",
                "榨汁杯",
                "--product-candidates",
                "data",
                "--output",
                str(out_path),
            ]
        )

    assert code == 0
    assert out_path.read_text(encoding="utf-8") == '{"summary":"ok"}'
    assert "Saved to" in capsys.readouterr().err


def test_main_missing_required_args_exits():
    run = _load_run_module()
    with pytest.raises(SystemExit):
        run.main(["--niche", "only-niche"])


def test_validate_discover_requires_source():
    run = _load_run_module()
    parser = run.build_parser()
    with pytest.raises(SystemExit):
        run.validate_args(parser, parser.parse_args(["--niche", "榨汁杯", "--discover"]))


def test_build_payload_discover_mode():
    run = _load_run_module()
    args = Namespace(
        niche="榨汁杯",
        discover=True,
        discover_source="amazon_serp",
        data_source="manual",
        platforms="amazon",
        unit_cost=None,
        target_margin=None,
        max_capital=None,
        risk_constraints=None,
        message=None,
        context=None,
        lang="zh",
    )
    payload = run.build_payload(
        args,
        product_candidates="platform,asin\namazon,B0TEST1234",
    )
    assert payload["data_source"] == "browser_extract"
    assert payload["discover_source"] == "amazon_serp"


def test_main_discover_mode_calls_browser_then_skill():
    run = _load_run_module()
    fake = {"formatted_text": "{}", "run_id": "hr_disc", "model_used": "m1"}
    csv_data = "platform,asin,title\namazon,B0X"

    with patch.object(run, "discover_candidates", return_value=csv_data) as mock_disc, patch.object(
        run, "run_skill", return_value=fake
    ) as mock_run:
        code = run.main(
            [
                "--niche",
                "榨汁杯",
                "--discover",
                "--discover-source",
                "amazon_serp",
                "--search-query",
                "portable juicer",
                "--max-candidates",
                "5",
            ]
        )

    assert code == 0
    mock_disc.assert_called_once_with(
        "amazon_serp",
        "portable juicer",
        max_candidates=5,
        browser_url=None,
    )
    assert mock_run.call_args[0][1]["product_candidates"] == csv_data
    assert mock_run.call_args[0][1]["data_source"] == "browser_extract"


def test_main_discover_error_returns_3():
    run = _load_run_module()
    from discover import DiscoverError

    with patch.object(run, "discover_candidates", side_effect=DiscoverError("browser down")):
        code = run.main(
            [
                "--niche",
                "x",
                "--discover",
                "--discover-source",
                "amazon_bs",
            ]
        )
    assert code == 3


def test_discover_resolve_urls():
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    import discover

    assert "amazon.com/s?" in discover.amazon_search_url("juicer")
    assert "exact-aware-popularity-rank" in discover.amazon_bs_search_url("juicer")
    assert "tiktok.com/shop/search" in discover.tiktok_shop_search_url("juicer")


def test_discover_amazon_with_mock_browser():
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    import discover

    serp = {
        "schema": "amazon_serp",
        "data": {
            "query_results": [
                {
                    "rank": 1,
                    "asin": "B0AAA11111",
                    "title": "Juicer A",
                    "price": "$19.99",
                    "rating": "4.5",
                    "sponsored": False,
                }
            ]
        },
    }
    listing = {
        "schema": "amazon_listing",
        "url": "https://www.amazon.com/dp/B0AAA11111",
        "data": {
            "asin": "B0AAA11111",
            "title": "Juicer A",
            "price": "$19.99",
            "rating": "4.5",
            "review_count": "900",
            "bsr": "#850",
        },
    }

    with patch.object(discover, "browser_open") as mock_open, patch.object(
        discover, "browser_extract"
    ) as mock_extract:
        mock_open.side_effect = [{"tab_id": "t1"}, {"tab_id": "t2"}]
        mock_extract.side_effect = [serp, listing]

        table = discover.discover_candidates(
            "amazon_serp",
            "juicer",
            max_candidates=1,
            browser_url="http://browser.test",
        )

    assert "B0AAA11111" in table
    assert "amazon_serp" in table
    assert "#850" in table

