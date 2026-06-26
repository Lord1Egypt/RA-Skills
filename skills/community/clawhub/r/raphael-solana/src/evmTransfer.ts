// EVM token transfers on Polygon — MATIC (native) and ERC-20 tokens
import { ethers } from "ethers"
import { loadEvmWallet } from "./evmWallet.ts"

const POLYGON_RPC = process.env["POLYGON_RPC_URL"] ?? "https://polygon-rpc.com"

const ERC20_ABI = [
  "function transfer(address to, uint256 amount) returns (bool)",
  "function decimals() public view returns (uint8)",
  "function symbol() public view returns (string)",
]

export type EvmTransferResult = {
  from: string
  to: string
  amount: string
  token: string
  txHash: string
  explorerUrl: string
}

export const transferMatic = async (
  walletName: string,
  toAddress: string,
  amountMatic: number,
): Promise<EvmTransferResult> => {
  const wallet = await loadEvmWallet(walletName)
  const provider = new ethers.JsonRpcProvider(POLYGON_RPC)
  const signer = wallet.connect(provider)

  const value = ethers.parseEther(amountMatic.toString())
  const tx = await signer.sendTransaction({ to: toAddress, value })
  await tx.wait()

  return {
    from: wallet.address,
    to: toAddress,
    amount: amountMatic.toString(),
    token: "MATIC",
    txHash: tx.hash,
    explorerUrl: `https://polygonscan.com/tx/${tx.hash}`,
  }
}

export const transferErc20 = async (
  walletName: string,
  toAddress: string,
  tokenAddress: string,
  amount: number,
): Promise<EvmTransferResult> => {
  const wallet = await loadEvmWallet(walletName)
  const provider = new ethers.JsonRpcProvider(POLYGON_RPC)
  const signer = wallet.connect(provider)

  const contract = new ethers.Contract(tokenAddress, ERC20_ABI, signer)
  const [decimals, symbol]: [number, string] = await Promise.all([
    contract.decimals(),
    contract.symbol(),
  ])
  const rawAmount = ethers.parseUnits(amount.toString(), decimals)

  const tx = await contract.transfer(toAddress, rawAmount)
  await tx.wait()

  return {
    from: wallet.address,
    to: toAddress,
    amount: amount.toString(),
    token: symbol,
    txHash: tx.hash,
    explorerUrl: `https://polygonscan.com/tx/${tx.hash}`,
  }
}
