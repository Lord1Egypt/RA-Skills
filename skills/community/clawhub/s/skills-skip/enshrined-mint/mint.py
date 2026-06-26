#!/usr/bin/env python3
"""
Enshrined Exchange - Mint/Redeem/Swap/Check Balance
Network: Tempo (Chain 4217)
RPC: https://rpc.moderato.tempo.xyz

Usage:
  Mint:    PRIVATE_KEY=0x... python mint.py mint --amount 100 --source USDC
  Redeem:  PRIVATE_KEY=0x... python mint.py redeem --amount 100 --dest USDC
  Swap:    PRIVATE_KEY=0x... python mint.py swap --amount 100 --from USDC --to USDe
  Balance: PRIVATE_KEY=0x... python mint.py balance

Requirements:
  pip install web3
"""

import os
import sys
import argparse
from decimal import Decimal

from web3 import Web3

RPC = 'https://rpc.moderato.tempo.xyz'
EXCHANGE = Web3.to_checksum_address('0xdec0000000000000000000000000000000000000')

TOKENS = {
    'USDC':   Web3.to_checksum_address('0x20C0000000000000000000000000000000000000'),
    'USDE':    Web3.to_checksum_address('0x20C0000000000000000000000000000000000001'),
    'PATHUSD': Web3.to_checksum_address('0x20C0000000000000000000000000000000000002'),
}

DECIMALS = {'USDC': 6, 'USDE': 18, 'PATHUSD': 18}

EXPLORER = 'https://explorer.tempo.xyz/tx'

EXCHANGE_ABI = [
    {
        'inputs': [
            {'name': 'tokenIn', 'type': 'address'},
            {'name': 'tokenOut', 'type': 'address'},
            {'name': 'amount', 'type': 'uint128'},
            {'name': 'minAmountOut', 'type': 'uint128'},
        ],
        'name': 'swapExactAmountIn',
        'outputs': [{'name': '', 'type': 'uint128'}],
        'stateMutability': 'nonpayable',
        'type': 'function',
    },
    {
        'inputs': [
            {'name': 'user', 'type': 'address'},
            {'name': 'token', 'type': 'address'},
        ],
        'name': 'getBalance',
        'outputs': [{'name': '', 'type': 'uint256'}],
        'stateMutability': 'view',
        'type': 'function',
    },
]

TOKEN_ABI = [
    {
        'inputs': [
            {'name': 'to', 'type': 'address'},
            {'name': 'amount', 'type': 'uint256'},
        ],
        'name': 'mint',
        'outputs': [{'name': '', 'type': 'bool'}],
        'stateMutability': 'nonpayable',
        'type': 'function',
    },
    {
        'inputs': [
            {'name': 'to', 'type': 'address'},
            {'name': 'amount', 'type': 'uint256'},
        ],
        'name': 'redeem',
        'outputs': [{'name': '', 'type': 'bool'}],
        'stateMutability': 'nonpayable',
        'type': 'function',
    },
    {
        'inputs': [{'name': 'account', 'type': 'address'}],
        'name': 'balanceOf',
        'outputs': [{'name': '', 'type': 'uint256'}],
        'stateMutability': 'view',
        'type': 'function',
    },
    {
        'inputs': [
            {'name': 'spender', 'type': 'address'},
            {'name': 'amount', 'type': 'uint256'},
        ],
        'name': 'approve',
        'outputs': [{'name': '', 'type': 'bool'}],
        'stateMutability': 'nonpayable',
        'type': 'function',
    },
    {
        'inputs': [
            {'name': 'owner', 'type': 'address'},
            {'name': 'spender', 'type': 'address'},
        ],
        'name': 'allowance',
        'outputs': [{'name': '', 'type': 'uint256'}],
        'stateMutability': 'view',
        'type': 'function',
    },
]


def parse_amount(amount_str, symbol):
    """Convert decimal string to smallest unit (wei/etc)."""
    dec = DECIMALS.get(symbol, 18)
    return int(Decimal(amount_str) * (10 ** dec))


def format_amount(raw_amount, symbol):
    """Convert smallest unit to decimal string."""
    dec = DECIMALS.get(symbol, 18)
    return str(Decimal(raw_amount) / (10 ** dec))


def check_balance(w3, token_addr, wallet_addr, symbol):
    """Get wallet + exchange balance for a token."""
    token = w3.eth.contract(address=token_addr, abi=TOKEN_ABI)
    exchange = w3.eth.contract(address=EXCHANGE, abi=EXCHANGE_ABI)

    wallet_bal = token.functions.balanceOf(wallet_addr).call()
    try:
        exchange_bal = exchange.functions.getBalance(wallet_addr, token_addr).call()
    except Exception:
        exchange_bal = 0

    print(f'  {symbol} (wallet):   {format_amount(wallet_bal, symbol)}')
    print(f'  {symbol} (exchange): {format_amount(exchange_bal, symbol)}')
    return wallet_bal


def action_balance(w3, wallet_addr, token_symbol=None):
    """Show balance for one or all tokens."""
    tokens = [token_symbol.upper()] if token_symbol else TOKENS.keys()
    print('\n📊 Token Balances')
    for t in tokens:
        if t not in TOKENS:
            print(f'  Unknown token: {t}')
            continue
        check_balance(w3, TOKENS[t], wallet_addr, t)


def action_mint(w3, wallet, amount_str, source_token):
    """Mint USDe by depositing source stablecoin."""
    source = source_token.upper()
    if source not in TOKENS:
        raise ValueError(f'Unknown source token: {source}')
    if source == 'USDE':
        raise ValueError('Source must be a stablecoin (USDC, pathUSD), not USDe')

    source_addr = TOKENS[source]
    usde_addr = TOKENS['USDE']
    amount = parse_amount(amount_str, source)

    token_src = w3.eth.contract(address=source_addr, abi=TOKEN_ABI)
    token_usde = w3.eth.contract(address=usde_addr, abi=TOKEN_ABI)

    # Check source balance
    src_bal = token_src.functions.balanceOf(wallet.address).call()
    print(f'\n📋 Step 1: {source} balance check')
    print(f'  {source} balance: {format_amount(src_bal, source)}')
    if src_bal < amount:
        raise ValueError(
            f'Insufficient {source} balance. '
            f'Have {format_amount(src_bal, source)}, need {format_amount(amount, source)}'
        )

    # Approve USDe contract
    current_allow = token_src.functions.allowance(wallet.address, usde_addr).call()
    print(f'\n📋 Step 2: Approve USDe contract to spend {source}')
    if current_allow < amount:
        tx = token_src.functions.approve(usde_addr, 2**256 - 1).build_transaction({
            'from': wallet.address,
            'nonce': w3.eth.get_transaction_count(wallet.address),
            'gas': 100000,
            'gasPrice': w3.eth.gas_price,
        })
        signed = wallet.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f'  ✅ Approval confirmed ({receipt["transactionHash"].hex()})')
    else:
        print('  ✅ Already approved')

    # Mint
    print(f'\n📋 Step 3: Mint {amount_str} USDe')
    tx = token_usde.functions.mint(wallet.address, amount).build_transaction({
        'from': wallet.address,
        'nonce': w3.eth.get_transaction_count(wallet.address),
        'gas': 200000,
        'gasPrice': w3.eth.gas_price,
    })
    signed = wallet.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f'\n✅ MINT SUCCESSFUL')
    print(f'  TX: {EXPLORER}/{tx_hash.hex()}')
    print(f'  Gas used: {receipt["gasUsed"]}')

    # Final balances
    final_src = token_src.functions.balanceOf(wallet.address).call()
    final_usde = token_usde.functions.balanceOf(wallet.address).call()
    print(f'\n📊 Final Balances')
    print(f'  {source}: {format_amount(final_src, source)}')
    print(f'  USDe: {format_amount(final_usde, "USDe")}')


def action_redeem(w3, wallet, amount_str, dest_token):
    """Redeem USDe for destination stablecoin."""
    dest = dest_token.upper()
    if dest not in TOKENS:
        raise ValueError(f'Unknown dest token: {dest}')
    if dest == 'USDE':
        raise ValueError('Dest must be a stablecoin (USDC, pathUSD), not USDe')

    dest_addr = TOKENS[dest]
    usde_addr = TOKENS['USDE']
    amount = parse_amount(amount_str, 'USDE')

    token_usde = w3.eth.contract(address=usde_addr, abi=TOKEN_ABI)
    token_dest = w3.eth.contract(address=dest_addr, abi=TOKEN_ABI)

    # Check USDe balance
    usde_bal = token_usde.functions.balanceOf(wallet.address).call()
    print(f'\n📋 Step 1: USDe balance check')
    print(f'  USDe balance: {format_amount(usde_bal, "USDe")}')
    if usde_bal < amount:
        raise ValueError(
            f'Insufficient USDe balance. '
            f'Have {format_amount(usde_bal, "USDe")}, need {format_amount(amount, "USDe")}'
        )

    # Redeem
    print(f'\n📋 Step 2: Redeem {amount_str} USDe → {dest}')
    tx = token_usde.functions.redeem(wallet.address, amount).build_transaction({
        'from': wallet.address,
        'nonce': w3.eth.get_transaction_count(wallet.address),
        'gas': 200000,
        'gasPrice': w3.eth.gas_price,
    })
    signed = wallet.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f'\n✅ REDEEM SUCCESSFUL')
    print(f'  TX: {EXPLORER}/{tx_hash.hex()}')
    print(f'  Gas used: {receipt["gasUsed"]}')

    # Final balances
    final_usde = token_usde.functions.balanceOf(wallet.address).call()
    final_dest = token_dest.functions.balanceOf(wallet.address).call()
    print(f'\n📊 Final Balances')
    print(f'  USDe: {format_amount(final_usde, "USDe")}')
    print(f'  {dest}: {format_amount(final_dest, dest)}')


def action_swap(w3, wallet, amount_str, from_token, to_token):
    """Swap one stablecoin for another via exchange."""
    src = from_token.upper()
    dst = to_token.upper()

    if src not in TOKENS:
        raise ValueError(f'Unknown from token: {src}')
    if dst not in TOKENS:
        raise ValueError(f'Unknown to token: {dst}')
    if src == dst:
        raise ValueError('From and To cannot be the same')

    src_addr = TOKENS[src]
    dst_addr = TOKENS[dst]
    amount = parse_amount(amount_str, src)

    exchange = w3.eth.contract(address=EXCHANGE, abi=EXCHANGE_ABI)
    token_src = w3.eth.contract(address=src_addr, abi=TOKEN_ABI)

    # Check source balance
    src_bal = token_src.functions.balanceOf(wallet.address).call()
    print(f'\n📋 Step 1: {src} balance check')
    print(f'  {src} balance: {format_amount(src_bal, src)}')
    if src_bal < amount:
        raise ValueError(f'Insufficient {src} balance')

    # Approve exchange
    current_allow = token_src.functions.allowance(wallet.address, EXCHANGE).call()
    print(f'\n📋 Step 2: Approve exchange to spend {src}')
    if current_allow < amount:
        tx = token_src.functions.approve(EXCHANGE, 2**256 - 1).build_transaction({
            'from': wallet.address,
            'nonce': w3.eth.get_transaction_count(wallet.address),
            'gas': 100000,
            'gasPrice': w3.eth.gas_price,
        })
        signed = wallet.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f'  ✅ Approval confirmed ({receipt["transactionHash"].hex()})')
    else:
        print('  ✅ Already approved')

    # Swap
    print(f'\n📋 Step 3: Swap {amount_str} {src} → {dst}')
    tx = exchange.functions.swapExactAmountIn(src_addr, dst_addr, amount, 0).build_transaction({
        'from': wallet.address,
        'nonce': w3.eth.get_transaction_count(wallet.address),
        'gas': 300000,
        'gasPrice': w3.eth.gas_price,
    })
    signed = wallet.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f'\n✅ SWAP SUCCESSFUL')
    print(f'  TX: {EXPLORER}/{tx_hash.hex()}')
    print(f'  Gas used: {receipt["gasUsed"]}')

    # Final balances
    final_src = token_src.functions.balanceOf(wallet.address).call()
    final_dst_bal = exchange.functions.getBalance(wallet.address, dst_addr).call()
    print(f'\n📊 Final Balances')
    print(f'  {src}: {format_amount(final_src, src)}')
    print(f'  {dst} (exchange): {format_amount(final_dst_bal, dst)}')


def main():
    parser = argparse.ArgumentParser(description='Enshrined Exchange - Mint/Redeem/Swap on Tempo')
    parser.add_argument('action', choices=['mint', 'redeem', 'swap', 'balance'],
                        help='Action to perform')
    parser.add_argument('--amount', help='Amount (e.g. 100)')
    parser.add_argument('--source', default='USDC',
                        help='Source token for minting (default: USDC)')
    parser.add_argument('--dest', default='USDC',
                        help='Destination token for redeem (default: USDC)')
    parser.add_argument('--from', dest='from_token', default='USDC',
                        help='From token for swap (default: USDC)')
    parser.add_argument('--to', dest='to_token', default='USDE',
                        help='To token for swap (default: USDe)')
    parser.add_argument('--token', dest='token_symbol',
                        help='Specific token for balance check')

    args = parser.parse_args(sys.argv[1:])

    private_key = os.environ.get('PRIVATE_KEY')
    if not private_key:
        print('❌ PRIVATE_KEY not set\n', file=sys.stderr)
        print('Usage:', file=sys.stderr)
        print('  Mint:    PRIVATE_KEY=0x... python mint.py mint --amount 100 --source USDC', file=sys.stderr)
        print('  Redeem:  PRIVATE_KEY=0x... python mint.py redeem --amount 100 --dest USDC', file=sys.stderr)
        print('  Swap:    PRIVATE_KEY=0x... python mint.py swap --amount 100 --from USDC --to USDe', file=sys.stderr)
        print('  Balance: PRIVATE_KEY=0x... python mint.py balance', file=sys.stderr)
        print('\nTokens: USDC, USDe, pathUSD', file=sys.stderr)
        sys.exit(1)

    w3 = Web3(Web3.HTTPProvider(RPC))
    if not w3.is_connected():
        print('❌ Cannot connect to RPC', file=sys.stderr)
        sys.exit(1)

    wallet = w3.eth.account.from_key(private_key)

    print('')
    print('🔷 ENSHRIINED.EXCHANGE')
    print('═══════════════════════════════════════════════')
    print(f'  Network:  Tempo (Chain 4217)')
    print(f'  RPC:      {RPC}')
    print(f'  Wallet:   {wallet.address}')
    print(f'  Action:   {args.action}')

    try:
        if args.action == 'balance':
            action_balance(w3, wallet.address, args.token_symbol)
        elif args.action == 'mint':
            if not args.amount:
                raise ValueError('--amount required for mint')
            action_mint(w3, wallet, args.amount, args.source)
        elif args.action == 'redeem':
            if not args.amount:
                raise ValueError('--amount required for redeem')
            action_redeem(w3, wallet, args.amount, args.dest)
        elif args.action == 'swap':
            if not args.amount:
                raise ValueError('--amount required for swap')
            action_swap(w3, wallet, args.amount, args.from_token, args.to_token)
    except Exception as err:
        print(f'\n❌ Error: {err}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
