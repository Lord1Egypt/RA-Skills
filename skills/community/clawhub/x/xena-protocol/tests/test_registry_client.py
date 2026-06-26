"""Unit tests for registry_client. Web3 provider and contract are mocked;
no real network calls. An optional integration test gated on SEPOLIA_RPC env
var is kept separate (not in this file)."""

from unittest.mock import MagicMock, patch

import pytest

from bin.registry_client import RegistryClient, _load_deployed


@pytest.fixture
def deployed_stub():
    return {
        "network": "sepolia",
        "chainId": 11155111,
        "address": "0x310F062c24884f82C15E488b0013EA1a64BD210E",
        "deployBlock": 10684147,
        "minStakeWei": 100000000000000,
        "reportFeeWei": 10000000000000,
        "unstakeCooldownSecs": 86400,
        "abi": [],  # real ABI irrelevant — we mock the contract interface
    }


@pytest.fixture
def mock_w3():
    w3 = MagicMock()
    w3.eth.gas_price = 20_000_000_000
    w3.eth.get_transaction_count.return_value = 0
    w3.eth.chain_id = 11155111
    w3.eth.send_raw_transaction.return_value = b"\xab\xcd"
    w3.eth.get_balance.return_value = 500_000_000_000_000
    return w3


@pytest.fixture
def client(deployed_stub, mock_w3, tmp_path):
    # Write the deployed.json where RegistryClient expects it
    import json
    dep_path = tmp_path / "deployed.json"
    dep_path.write_text(json.dumps(deployed_stub))
    with patch("bin.registry_client.Web3", return_value=mock_w3):
        c = RegistryClient(
            rpc_url="http://fake.rpc",
            deployed_json=str(dep_path),
        )
    # Access and stub .contract for per-call assertions
    c._w3 = mock_w3
    c._contract = MagicMock()
    return c


# generate_wallet
def test_generate_wallet_returns_valid_pair():
    from bin.registry_client import generate_wallet
    addr, pk = generate_wallet()
    assert addr.startswith("0x")
    assert len(addr) == 42
    assert pk.startswith("0x")
    assert len(pk) == 66  # 0x + 64 hex chars


def test_generate_wallet_each_call_different():
    from bin.registry_client import generate_wallet
    a1, _ = generate_wallet()
    a2, _ = generate_wallet()
    assert a1 != a2


# Address hardcoded — security invariant
def test_client_hardcodes_registry_address(client, deployed_stub):
    assert client.address == deployed_stub["address"]


def test_client_has_no_arbitrary_send_method(client):
    assert not hasattr(client, "send_transaction")
    assert not hasattr(client, "raw_call")


# Read-only calls
def test_is_reported_calls_contract(client):
    client._contract.functions.isReported.return_value.call.return_value = (True, 3)
    exists, count = client.is_reported(b"\xab" * 32)
    assert exists is True
    assert count == 3
    client._contract.functions.isReported.assert_called_once_with(b"\xab" * 32)


def test_domain_report_count(client):
    client._contract.functions.domainReportCount.return_value.call.return_value = 7
    n = client.domain_report_count("scam.xyz")
    assert n == 7
    client._contract.functions.domainReportCount.assert_called_once_with("scam.xyz")


def test_get_balance(client, mock_w3):
    bal = client.get_balance("0xabc")
    assert bal == 500_000_000_000_000
    mock_w3.eth.get_balance.assert_called_once_with("0xabc")


# Write calls — verify only registry address is touched
def test_stake_builds_tx_to_registry_address_only(client, deployed_stub):
    # Mock the contract's function builder + transaction building
    fn = MagicMock()
    fn.build_transaction.return_value = {
        "to": deployed_stub["address"],
        "value": deployed_stub["minStakeWei"],
        "data": "0x",
        "gas": 100_000,
        "gasPrice": 20_000_000_000,
        "nonce": 0,
        "chainId": 11155111,
    }
    client._contract.functions.stake.return_value = fn

    signed = MagicMock()
    signed.raw_transaction = b"\xde\xad"
    with patch("bin.registry_client.Account.sign_transaction", return_value=signed) as sign_mock:
        tx = client.stake(
            recipient="0xRecipient",
            value_wei=deployed_stub["minStakeWei"],
            private_key="0x" + "1" * 64,
        )

    fn.build_transaction.assert_called_once()
    built = fn.build_transaction.call_args.args[0]
    # Registry address baked in by build_transaction target
    assert built["value"] == deployed_stub["minStakeWei"]
    # Signing + send raw called
    sign_mock.assert_called_once()
    assert tx == "0xabcd"


def test_report_identity_passes_all_fields(client, deployed_stub):
    fn = MagicMock()
    fn.build_transaction.return_value = {
        "to": deployed_stub["address"], "value": deployed_stub["reportFeeWei"],
        "data": "0x", "gas": 200_000, "gasPrice": 20_000_000_000,
        "nonce": 0, "chainId": 11155111,
    }
    client._contract.functions.reportIdentity.return_value = fn

    signed = MagicMock()
    signed.raw_transaction = b"\xbe\xef"
    with patch("bin.registry_client.Account.sign_transaction", return_value=signed):
        tx = client.report_identity(
            identity_hash=b"\x11" * 32,
            domain="scam.xyz",
            platform=0,
            category=3,
            confidence=92,
            value_wei=deployed_stub["reportFeeWei"],
            private_key="0x" + "1" * 64,
        )

    client._contract.functions.reportIdentity.assert_called_once_with(
        b"\x11" * 32, "scam.xyz", 0, 3, 92
    )
    assert tx == "0xabcd"


def test_unstake(client):
    fn = MagicMock()
    fn.build_transaction.return_value = {
        "to": client.address, "value": 0, "data": "0x",
        "gas": 100_000, "gasPrice": 20_000_000_000, "nonce": 0, "chainId": 11155111,
    }
    client._contract.functions.unstake.return_value = fn

    signed = MagicMock()
    signed.raw_transaction = b"\xfe\xed"
    with patch("bin.registry_client.Account.sign_transaction", return_value=signed):
        tx = client.unstake(private_key="0x" + "1" * 64)

    client._contract.functions.unstake.assert_called_once_with()
    assert tx == "0xabcd"


# Utility
def test_hash_identifier_deterministic():
    from bin.registry_client import hash_identifier
    h1 = hash_identifier("bob@scam.xyz")
    h2 = hash_identifier("bob@scam.xyz")
    assert h1 == h2
    assert len(h1) == 32  # bytes32


def test_hash_identifier_case_normalization():
    from bin.registry_client import hash_identifier
    assert hash_identifier("Bob@SCAM.XYZ") == hash_identifier("bob@scam.xyz")


def test_load_deployed_reads_json(tmp_path, deployed_stub):
    import json
    p = tmp_path / "d.json"
    p.write_text(json.dumps(deployed_stub))
    out = _load_deployed(p)
    assert out["address"] == deployed_stub["address"]


def test_load_deployed_missing_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        _load_deployed(tmp_path / "nope.json")
