/**
 * EVVM Payment Adapter Contract Interface
 */

import { ethers, Contract } from 'ethers';

export interface PayViaEVVMWithX402Params {
  from: string;
  to: string;
  toIdentity: string;
  amount: string;
  validAfter: number;
  validBefore: number;
  nonce: string;
  v: number;
  r: string;
  s: string;
  receiptId: string;
  evvmNonce: bigint;
  isAsyncExec: boolean;
  evvmSignature: string;
}

export class EVVMPaymentAdapter {
  private contract: Contract;

  constructor(address: string, signer: ethers.Signer) {
    this.contract = new ethers.Contract(
      address,
      [
        'function payViaEVVMWithX402(address from, address to, string memory toIdentity, uint256 amount, uint256 validAfter, uint256 validBefore, bytes32 nonce, uint8 v, bytes32 r, bytes32 s, string memory receiptId, uint256 evvmNonce, bool isAsyncExec, bytes memory evvmSignature)',
        'function getEVVMPaymentInfo(string memory receiptId) view returns (address from, address to, uint256 amount, uint256 timestamp, bool exists)',
        'function processedPayments(bytes32) view returns (bool)'
      ],
      signer
    );
  }

  async payViaEVVMWithX402(params: PayViaEVVMWithX402Params) {
    return this.contract.payViaEVVMWithX402(
      params.from,
      params.to,
      params.toIdentity,
      params.amount,
      params.validAfter,
      params.validBefore,
      params.nonce,
      params.v,
      params.r,
      params.s,
      params.receiptId,
      params.evvmNonce,
      params.isAsyncExec,
      params.evvmSignature
    );
  }

  async getEVVMPaymentInfo(receiptId: string) {
    return this.contract.getEVVMPaymentInfo(receiptId);
  }

  async isProcessed(nonce: string): Promise<boolean> {
    return this.contract.processedPayments(nonce);
  }
}
