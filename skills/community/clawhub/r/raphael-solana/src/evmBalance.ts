// EVM balance checking for native and ERC-20 tokens on Polygon
import { ethers } from "ethers"
import { loadEvmWallet } from "./evmWallet.ts"

const POLYGON_RPC =
  process.env["POLYGON_RPC_URL"] ??
  "https://polygon-rpc.com"

const USDC_ADDRESS = "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359" // Native USDC on Polygon

const ERC20_ABI = [
  "function balanceOf(address owner) public view returns (uint256)",
  "function decimals() public view returns (uint8)",
  "function symbol() public view returns (string)",
]

export type EvmBalance = {
  walletName: string
  address: string
  nativeBalance: {
    wei: string
    matic: string
  }
  tokenBalances: Array<{
    token: string
    address: string
    raw: string
    decimals: number
    formatted: string
    symbol: string
  }>
}

/**
 * Get native (MATIC) balance for an EVM wallet
 */
export const getNativeBalance = async (walletName: string): Promise<{ wei: string; matic: string }> => {
  const wallet = await loadEvmWallet(walletName)
  const provider = new ethers.JsonRpcProvider(POLYGON_RPC)
  const wei = await provider.getBalance(wallet.address)
  return {
    wei: wei.toString(),
    matic: ethers.formatEther(wei),
  }
}

/**
 * Get ERC-20 token balance for an EVM wallet
 */
export const getTokenBalance = async (
  walletName: string,
  tokenAddress: string,
): Promise<{ raw: string; formatted: string; decimals: number; symbol: string }> => {
  const wallet = await loadEvmWallet(walletName)
  const provider = new ethers.JsonRpcProvider(POLYGON_RPC)
  const contract = new ethers.Contract(tokenAddress, ERC20_ABI, provider)

  const [balance, decimals, symbol] = await Promise.all([
    contract.balanceOf(wallet.address),
    contract.decimals(),
    contract.symbol(),
  ])

  return {
    raw: balance.toString(),
    formatted: ethers.formatUnits(balance, decimals),
    decimals,
    symbol,
  }
}

/**
 * Get USDC balance
 */
export const getUsdcBalance = async (walletName: string): Promise<{ formatted: string; decimals: number }> => {
  const wallet = await loadEvmWallet(walletName)
  const provider = new ethers.JsonRpcProvider(POLYGON_RPC)

  const contract = new ethers.Contract(USDC_ADDRESS, ERC20_ABI, provider)
  const balance = await contract.balanceOf(wallet.address)
  const decimals = await contract.decimals()
  return {
    formatted: ethers.formatUnits(balance, decimals),
    decimals,
  }
}

/**
 * Get full balance summary for a wallet (native + USDC)
 */
export const getEvmBalance = async (walletName: string): Promise<EvmBalance> => {
  const wallet = await loadEvmWallet(walletName)
  const native = await getNativeBalance(walletName)
  const usdc = await getTokenBalance(walletName, USDC_ADDRESS)

  return {
    walletName,
    address: wallet.address,
    nativeBalance: native,
    tokenBalances: [
      {
        token: "USDC",
        address: USDC_ADDRESS,
        raw: usdc.raw,
        decimals: usdc.decimals,
        formatted: usdc.formatted,
        symbol: usdc.symbol || "USDC",
      },
    ],
  }
}
