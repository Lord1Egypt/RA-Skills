import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from solders.hash import Hash
from solders.keypair import Keypair


SCRIPT = Path(__file__).parents[1] / "scripts" / "solana_sign_send.py"
SPEC = importlib.util.spec_from_file_location("swimmer_signer", SCRIPT)
signer = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = signer
SPEC.loader.exec_module(signer)


class SignerPolicyTests(unittest.TestCase):
    def setUp(self):
        self.stock_mint = str(Keypair().pubkey())
        self.keypair = Keypair()
        self.config = signer.WalletConfig(
            keypair=self.keypair,
            rpc_url=signer.PUBLIC_SOLANA_RPC_URL,
            trusted_stock_mints={"AAPL": self.stock_mint},
            max_offer_raw_by_mint={str(signer.SOLANA_USDC_MINT): 25_000_000},
        )
        self.plan = {
            "stock": "AAPL",
            "side": "BUY",
            "order_type": "MARKET",
            "token_pair_name": "USDC-AAPLs",
            "offer_mint": str(signer.SOLANA_USDC_MINT),
            "stock_mint": self.stock_mint,
            "offer_amount_raw": "25000000",
            "request_amount_raw": "0",
        }

    def test_recipient_is_not_accepted_from_plan(self):
        plan = dict(self.plan, recipient=str(Keypair().pubkey()))
        with self.assertRaisesRegex(signer.ValidationError, "unsupported fields"):
            signer._intent(plan, self.config)

    def test_trusted_mint_is_required(self):
        plan = dict(self.plan, stock_mint=str(Keypair().pubkey()))
        with self.assertRaisesRegex(signer.ValidationError, "trusted_stock_mints"):
            signer._intent(plan, self.config)

    def test_offer_cap_is_enforced(self):
        plan = dict(self.plan, offer_amount_raw="25000001")
        with self.assertRaisesRegex(signer.ValidationError, "exceeds"):
            signer._intent(plan, self.config)

    def test_market_zero_discloses_no_minimum(self):
        summary = signer.inspect_plan(self.plan, self.config)
        self.assertTrue(summary["irreversible_transfer"])
        self.assertTrue(summary["execution_amount_unknown"])
        self.assertEqual(summary["on_chain_settlement_guarantee"], "none")
        self.assertIn(str(signer.SVIM_SOLANA_RECIPIENT), summary["authorization_text"])
        self.assertIn("not an atomic swap", summary["warning"])

    def test_limit_requires_positive_request(self):
        plan = dict(self.plan, order_type="LIMIT")
        with self.assertRaisesRegex(signer.ValidationError, "positive integer"):
            signer._intent(plan, self.config)

    def test_confirmation_binds_complete_intent(self):
        first = signer.inspect_plan(self.plan, self.config)["confirmation_id"]
        changed = dict(self.plan, offer_amount_raw="24999999")
        second = signer.inspect_plan(changed, self.config)["confirmation_id"]
        self.assertNotEqual(first, second)

    def test_transaction_has_only_transfer_and_memo(self):
        intent = signer._intent(self.plan, self.config)
        tx = signer._build_order_transaction(intent, self.keypair, Hash.default())
        self.assertEqual(len(tx.message.instructions), 2)
        program_ids = [
            str(tx.message.account_keys[ix.program_id_index])
            for ix in tx.message.instructions
        ]
        self.assertEqual(program_ids, [str(signer.TOKEN_PROGRAM_ID), str(signer.MEMO_PROGRAM_ID)])

    def test_source_has_no_config_path_argument(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn('add_argument("--config"', source)
        self.assertIn('os.open("config.json", common, dir_fd=skill_dir_fd)', source)

    def _config_fixture(self, root: Path, mode: int = 0o600) -> Path:
        directory = root / ".config" / "swimmer-stock-trading"
        directory.mkdir(parents=True)
        directory.chmod(0o700)
        path = directory / "config.json"
        path.write_text(
            json.dumps(
                {
                    "private_key": str(self.keypair),
                    "rpc_url": signer.PUBLIC_SOLANA_RPC_URL,
                    "accepted_custodial_recipient": str(signer.SVIM_SOLANA_RECIPIENT),
                    "trusted_stock_mints": {"AAPL": self.stock_mint},
                    "max_offer_raw_by_mint": {str(signer.SOLANA_USDC_MINT): "25000000"},
                }
            ),
            encoding="utf-8",
        )
        path.chmod(mode)
        return path

    def test_fixed_secure_config_can_load(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._config_fixture(root)
            with mock.patch.object(signer.Path, "home", return_value=root):
                loaded = signer.load_config()
            self.assertEqual(loaded.keypair.pubkey(), self.keypair.pubkey())

    def test_config_requires_exact_0600(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._config_fixture(root, 0o640)
            with mock.patch.object(signer.Path, "home", return_value=root):
                with self.assertRaisesRegex(signer.ValidationError, "exact mode 0600"):
                    signer.load_config()

    def test_config_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            real = self._config_fixture(root)
            moved = root / "real-config.json"
            real.rename(moved)
            os.symlink(moved, real)
            with mock.patch.object(signer.Path, "home", return_value=root):
                with self.assertRaisesRegex(signer.ValidationError, "no-symlink"):
                    signer.load_config()


if __name__ == "__main__":
    unittest.main()
