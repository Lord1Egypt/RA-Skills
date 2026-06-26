import { ethers } from 'ethers';
import { NetworkName, createProvider, getNetworkConfig } from './provider.js';

const MARKETPLACE_ABI = [
  'constructor(uint256 feeBps, address feeRecipient)',
  'function list(address nftContract, uint256 tokenId, uint256 price) returns (uint256 listingId)',
  'function buy(uint256 listingId) payable',
  'function cancel(uint256 listingId)',
  'function getListing(uint256 listingId) view returns (address seller, address nftContract, uint256 tokenId, uint256 price, bool active)',
  'function getActiveListingCount() view returns (uint256)',
  'function nextListingId() view returns (uint256)',
  'function owner() view returns (address)',
  'function feeRecipient() view returns (address)',
  'function feeBps() view returns (uint256)',
  'function setFee(uint256 feeBps, address feeRecipient)',
  'event Listed(uint256 indexed listingId, address indexed seller, address nftContract, uint256 tokenId, uint256 price)',
  'event Sold(uint256 indexed listingId, address indexed buyer, address indexed seller, uint256 price)',
  'event Cancelled(uint256 indexed listingId)',
  'event FeeUpdated(uint256 newFeeBps, address newFeeRecipient)',
];

const ERC721_APPROVE_ABI = [
  'function approve(address to, uint256 tokenId)',
  'function setApprovalForAll(address operator, bool approved)',
  'function getApproved(uint256 tokenId) view returns (address)',
  'function isApprovedForAll(address owner, address operator) view returns (bool)',
  'function ownerOf(uint256 tokenId) view returns (address)',
];

/**
 * Pre-compiled NFTMarketplace bytecode (Solidity 0.8.34, evmVersion: paris, optimizer: 200 runs).
 * Constructor: (uint256 feeBps, address feeRecipient)
 * feeBps: platform fee in basis points (200 = 2%, max 1000 = 10%)
 * feeRecipient: address that receives fees (address(0) defaults to deployer)
 */
const MARKETPLACE_DEPLOY_BYTECODE = '0x608060405234801561001057600080fd5b50604051610def380380610def83398101604081905261002f916100ca565b6103e88211156100745760405162461bcd60e51b815260206004820152600c60248201526b0cccaca40e8dede40d0d2ced60a31b604482015260640160405180910390fd5b600280546001600160a01b0319163317905560048290556001600160a01b038116156100a057806100a2565b335b600380546001600160a01b0319166001600160a01b0392909216919091179055506101079050565b600080604083850312156100dd57600080fd5b825160208401519092506001600160a01b03811681146100fc57600080fd5b809150509250929050565b610cd9806101166000396000f3fe60806040526004361061009c5760003560e01c80638da5cb5b116100645780638da5cb5b146101ca578063aaccf1ec146101ea578063b4f2e8b814610200578063d96a094a14610220578063dda342bb14610233578063de74e57b1461025357600080fd5b8063107a274a146100a157806324a9d8531461013757806340e58ee51461015b578063469048401461017d57806377420844146101b5575b600080fd5b3480156100ad57600080fd5b506100fd6100bc366004610b46565b6000908152600160208190526040909120805491810154600282015460038301546004909301546001600160a01b0394851695949092169390929160ff1690565b604080516001600160a01b0396871681529590941660208601529284019190915260608301521515608082015260a0015b60405180910390f35b34801561014357600080fd5b5061014d60045481565b60405190815260200161012e565b34801561016757600080fd5b5061017b610176366004610b46565b6102ad565b005b34801561018957600080fd5b5060035461019d906001600160a01b031681565b6040516001600160a01b03909116815260200161012e565b3480156101c157600080fd5b5061014d610382565b3480156101d657600080fd5b5060025461019d906001600160a01b031681565b3480156101f657600080fd5b5061014d60005481565b34801561020c57600080fd5b5061017b61021b366004610b77565b6103c4565b61017b61022e366004610b46565b6104c4565b34801561023f57600080fd5b5061014d61024e366004610ba7565b610847565b34801561025f57600080fd5b506100fd61026e366004610b46565b6001602081905260009182526040909120805491810154600282015460038301546004909301546001600160a01b039485169490921692909160ff1685565b6000818152600160205260409020600481015460ff166103015760405162461bcd60e51b815260206004820152600a6024820152696e6f742061637469766560b01b60448201526064015b60405180910390fd5b80546001600160a01b031633146103475760405162461bcd60e51b815260206004820152600a6024820152693737ba1039b2b63632b960b11b60448201526064016102f8565b60048101805460ff1916905560405182907fc41d93b8bfbf9fd7cf5bfe271fd649ab6a6fec0ea101c23b82a2a28eca2533a990600090a25050565b6000805b6000548110156103c05760008181526001602052604090206004015460ff16156103b857816103b481610bf2565b9250505b600101610386565b5090565b6002546001600160a01b0316331461040a5760405162461bcd60e51b81526020600482015260096024820152683737ba1037bbb732b960b91b60448201526064016102f8565b6103e882111561044b5760405162461bcd60e51b815260206004820152600c60248201526b0cccaca40e8dede40d0d2ced60a31b60448201526064016102f8565b60048290556001600160a01b0381161561047b57600380546001600160a01b0319166001600160a01b0383161790555b600354604080518481526001600160a01b0390921660208301527f7cfad8b150be9751a5386cc4e0f549618032ff63d14fab4f77cd4b0aaaedc242910160405180910390a15050565b6000818152600160205260409020600481015460ff166105135760405162461bcd60e51b815260206004820152600a6024820152696e6f742061637469766560b01b60448201526064016102f8565b806003015434101561055e5760405162461bcd60e51b81526020600482015260146024820152731a5b9cdd59999a58da595b9d081c185e5b595b9d60621b60448201526064016102f8565b6004818101805460ff191690556001820154825460028401546040516323b872dd60e01b81526001600160a01b0392831694810194909452336024850152604484015216906323b872dd90606401600060405180830381600087803b1580156105c657600080fd5b505af11580156105da573d6000803e3d6000fd5b50505050600061271060045483600301546105f59190610c0b565b6105ff9190610c28565b905060008183600301546106139190610c4a565b83546040519192506000916001600160a01b039091169083908381818185875af1925050503d8060008114610664576040519150601f19603f3d011682016040523d82523d6000602084013e610669565b606091505b50509050806106b25760405162461bcd60e51b81526020600482015260156024820152741cd95b1b195c881c185e5b595b9d0819985a5b1959605a1b60448201526064016102f8565b8215610752576003546040516000916001600160a01b03169085908381818185875af1925050503d8060008114610705576040519150601f19603f3d011682016040523d82523d6000602084013e61070a565b606091505b50509050806107505760405162461bcd60e51b8152602060048201526012602482015271199959481c185e5b595b9d0819985a5b195960721b60448201526064016102f8565b505b83600301543411156107f657600384015460009033906107729034610c4a565b604051600081818185875af1925050503d80600081146107ae576040519150601f19603f3d011682016040523d82523d6000602084013e6107b3565b606091505b50509050806107f45760405162461bcd60e51b815260206004820152600d60248201526c1c99599d5b990819985a5b1959609a1b60448201526064016102f8565b505b835460038501546040519081526001600160a01b0390911690339087907f23f50d55776d8003622a982ade45a6c7f083116c8dbbcd980f59942f440badb19060200160405180910390a45050505050565b60008082116108855760405162461bcd60e51b815260206004820152600a6024820152697a65726f20707269636560b01b60448201526064016102f8565b6040516331a9108f60e11b815260048101849052849033906001600160a01b03831690636352211e90602401602060405180830381865afa1580156108ce573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906108f29190610c5d565b6001600160a01b0316146109345760405162461bcd60e51b81526020600482015260096024820152683737ba1037bbb732b960b91b60448201526064016102f8565b60405163020604bf60e21b81526004810185905230906001600160a01b0383169063081812fc90602401602060405180830381865afa15801561097b573d6000803e3d6000fd5b505050506040513d601f19601f8201168201806040525081019061099f9190610c5d565b6001600160a01b03161480610a1d575060405163e985e9c560e01b81523360048201523060248201526001600160a01b0382169063e985e9c590604401602060405180830381865afa1580156109f9573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190610a1d9190610c81565b610a585760405162461bcd60e51b815260206004820152600c60248201526b1b9bdd08185c1c1c9bdd995960a21b60448201526064016102f8565b600080549080610a6783610bf2565b909155506040805160a081018252338082526001600160a01b0389811660208085018281528587018c815260608088018d8152600160808a0181815260008d81528288528c90209a518b54908a166001600160a01b0319918216178c559551918b0180549290991691909516179096559051600288015593516003870155516004909501805495151560ff1990961695909517909455845190815292830189905292820187905292945084917f723f73331eaee88eec7fc68ef60ab6ed15e4b90d0472b55eb92fa43910bab6dd910160405180910390a3509392505050565b600060208284031215610b5857600080fd5b5035919050565b6001600160a01b0381168114610b7457600080fd5b50565b60008060408385031215610b8a57600080fd5b823591506020830135610b9c81610b5f565b809150509250929050565b600080600060608486031215610bbc57600080fd5b8335610bc781610b5f565b95602085013595506040909401359392505050565b634e487b7160e01b600052601160045260246000fd5b600060018201610c0457610c04610bdc565b5060010190565b8082028115828204841417610c2257610c22610bdc565b92915050565b600082610c4557634e487b7160e01b600052601260045260246000fd5b500490565b81810381811115610c2257610c22610bdc565b600060208284031215610c6f57600080fd5b8151610c7a81610b5f565b9392505050565b600060208284031215610c9357600080fd5b81518015158114610c7a57600080fdfea26469706673582212202badec8e56b93f0c3da3254186ca776ad6c42038b0eef22927feed805157e6f164736f6c63430008220033';

/**
 * Solidity source code for the NFTMarketplace contract.
 */
export const MARKETPLACE_SOURCE_CODE = `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC721 {
    function ownerOf(uint256 tokenId) external view returns (address);
    function transferFrom(address from, address to, uint256 tokenId) external;
    function getApproved(uint256 tokenId) external view returns (address);
    function isApprovedForAll(address owner, address operator) external view returns (bool);
}

contract NFTMarketplace {
    struct Listing {
        address seller;
        address nftContract;
        uint256 tokenId;
        uint256 price;
        bool active;
    }

    uint256 public nextListingId;
    mapping(uint256 => Listing) public listings;

    address public owner;
    address public feeRecipient;
    uint256 public feeBps; // basis points (200 = 2%, max 1000 = 10%)

    event Listed(uint256 indexed listingId, address indexed seller, address nftContract, uint256 tokenId, uint256 price);
    event Sold(uint256 indexed listingId, address indexed buyer, address indexed seller, uint256 price);
    event Cancelled(uint256 indexed listingId);
    event FeeUpdated(uint256 newFeeBps, address newFeeRecipient);

    constructor(uint256 _feeBps, address _feeRecipient) {
        require(_feeBps <= 1000, "fee too high");
        owner = msg.sender;
        feeBps = _feeBps;
        feeRecipient = _feeRecipient == address(0) ? msg.sender : _feeRecipient;
    }

    modifier onlyOwner() { require(msg.sender == owner, "not owner"); _; }

    function setFee(uint256 _feeBps, address _feeRecipient) external onlyOwner {
        require(_feeBps <= 1000, "fee too high");
        feeBps = _feeBps;
        if (_feeRecipient != address(0)) feeRecipient = _feeRecipient;
        emit FeeUpdated(_feeBps, feeRecipient);
    }

    function list(address nftContract, uint256 tokenId, uint256 price) external returns (uint256 listingId) {
        require(price > 0, "zero price");
        IERC721 nft = IERC721(nftContract);
        require(nft.ownerOf(tokenId) == msg.sender, "not owner");
        require(
            nft.getApproved(tokenId) == address(this) || nft.isApprovedForAll(msg.sender, address(this)),
            "not approved"
        );
        listingId = nextListingId++;
        listings[listingId] = Listing(msg.sender, nftContract, tokenId, price, true);
        emit Listed(listingId, msg.sender, nftContract, tokenId, price);
    }

    function buy(uint256 listingId) external payable {
        Listing storage l = listings[listingId];
        require(l.active, "not active");
        require(msg.value >= l.price, "insufficient payment");
        l.active = false;
        IERC721(l.nftContract).transferFrom(l.seller, msg.sender, l.tokenId);
        uint256 fee = (l.price * feeBps) / 10000;
        uint256 sellerAmount = l.price - fee;
        (bool ok, ) = l.seller.call{value: sellerAmount}("");
        require(ok, "seller payment failed");
        if (fee > 0) {
            (bool feeOk, ) = feeRecipient.call{value: fee}("");
            require(feeOk, "fee payment failed");
        }
        if (msg.value > l.price) {
            (bool refundOk, ) = msg.sender.call{value: msg.value - l.price}("");
            require(refundOk, "refund failed");
        }
        emit Sold(listingId, msg.sender, l.seller, l.price);
    }

    function cancel(uint256 listingId) external {
        Listing storage l = listings[listingId];
        require(l.active, "not active");
        require(l.seller == msg.sender, "not seller");
        l.active = false;
        emit Cancelled(listingId);
    }

    function getListing(uint256 listingId) external view returns (
        address seller, address nftContract, uint256 tokenId, uint256 price, bool active
    ) {
        Listing storage l = listings[listingId];
        return (l.seller, l.nftContract, l.tokenId, l.price, l.active);
    }

    function getActiveListingCount() external view returns (uint256 count) {
        for (uint256 i = 0; i < nextListingId; i++) {
            if (listings[i].active) count++;
        }
    }
}
`;

export interface MarketplaceDeployResult {
  marketplaceAddress: string;
  txHash: string;
  explorerUrl: string;
}

export interface ListingInfo {
  listingId: number;
  seller: string;
  nftContract: string;
  tokenId: number;
  price: string;
  active: boolean;
}

export interface ListNFTResult {
  listingId: string;
  nftContract: string;
  tokenId: number;
  price: string;
  txHash: string;
  explorerUrl: string;
}

export interface BuyNFTResult {
  listingId: number;
  price: string;
  txHash: string;
  explorerUrl: string;
}

/**
 * QFCMarketplace — Simple NFT marketplace on QFC.
 * List, buy, and cancel NFT listings. Payment in native QFC.
 */
export class QFCMarketplace {
  private provider: ethers.JsonRpcProvider;
  private networkConfig;

  constructor(network: NetworkName = 'testnet') {
    this.networkConfig = getNetworkConfig(network);
    this.provider = createProvider(network);
  }

  private async waitForReceipt(
    txHash: string,
    timeoutMs: number = 120_000,
  ): Promise<{ status: string; contractAddress: string; blockNumber: string; gasUsed: string; logs: Array<{ topics: string[]; data: string }> }> {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      await new Promise((r) => setTimeout(r, 3000));
      const raw = await this.provider.send('eth_getTransactionReceipt', [txHash]);
      if (raw) return raw;
    }
    throw new Error(`Transaction ${txHash} not confirmed after ${timeoutMs / 1000}s`);
  }

  /**
   * Deploy a new NFT marketplace contract with configurable platform fee.
   * @param signer - wallet to deploy from (becomes owner)
   * @param feeBps - platform fee in basis points (default 200 = 2%, max 1000 = 10%, 0 = no fee)
   * @param feeRecipient - address that receives fees (default: deployer address)
   */
  async deploy(
    signer: ethers.Wallet,
    feeBps: number = 200,
    feeRecipient?: string,
  ): Promise<MarketplaceDeployResult> {
    const connected = signer.connect(this.provider);
    const factory = new ethers.ContractFactory(MARKETPLACE_ABI, MARKETPLACE_DEPLOY_BYTECODE, connected);
    const deployTx = await factory.getDeployTransaction(
      feeBps,
      feeRecipient ?? ethers.ZeroAddress,
    );
    deployTx.gasLimit = 1_500_000n;

    const tx = await connected.sendTransaction(deployTx);
    const receipt = await this.waitForReceipt(tx.hash);

    if (receipt.status !== '0x1') {
      throw new Error(`Marketplace deployment reverted (tx: ${tx.hash})`);
    }

    // Best-effort verification
    try {
      const constructorArgs = ethers.AbiCoder.defaultAbiCoder()
        .encode(['uint256', 'address'], [feeBps, feeRecipient ?? ethers.ZeroAddress])
        .slice(2);
      const verifyUrl = `${this.networkConfig.explorerUrl}/api/contracts/verify`;
      await fetch(verifyUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          address: receipt.contractAddress,
          sourceCode: MARKETPLACE_SOURCE_CODE,
          compilerVersion: 'v0.8.34+commit.1c8745a5',
          evmVersion: 'paris',
          optimizationRuns: 200,
          constructorArgs,
        }),
      });
    } catch {
      // Explorer unavailable
    }

    return {
      marketplaceAddress: receipt.contractAddress,
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/contract/${receipt.contractAddress}`,
    };
  }

  /**
   * List an NFT for sale. Auto-approves the marketplace if needed.
   * @param marketplace - marketplace contract address
   * @param nftContract - ERC-721 contract address
   * @param tokenId - token ID to list
   * @param priceQFC - price in native QFC (human-readable, e.g. "5.0")
   * @param signer - NFT owner
   */
  async listNFT(
    marketplace: string,
    nftContract: string,
    tokenId: number,
    priceQFC: string,
    signer: ethers.Wallet,
  ): Promise<ListNFTResult> {
    const connected = signer.connect(this.provider);
    const nft = new ethers.Contract(nftContract, ERC721_APPROVE_ABI, connected);

    // Auto-approve marketplace if not already
    const approved = await nft.getApproved(tokenId);
    const approvedForAll = await nft.isApprovedForAll(connected.address, marketplace);
    if (approved.toLowerCase() !== marketplace.toLowerCase() && !approvedForAll) {
      const approveTx = await nft.approve(marketplace, tokenId);
      const approveReceipt = await this.waitForReceipt(approveTx.hash);
      if (approveReceipt.status !== '0x1') {
        throw new Error(`NFT approval failed (tx: ${approveTx.hash})`);
      }
    }

    const price = ethers.parseEther(priceQFC);
    const mp = new ethers.Contract(marketplace, MARKETPLACE_ABI, connected);
    const txData = await mp.list.populateTransaction(nftContract, tokenId, price);
    txData.gasLimit = 300_000n;
    const tx = await connected.sendTransaction(txData);
    const receipt = await this.waitForReceipt(tx.hash);

    if (receipt.status !== '0x1') {
      throw new Error(`Listing failed (tx: ${tx.hash})`);
    }

    // Parse listing ID from event logs
    const listedTopic = ethers.id('Listed(uint256,address,address,uint256,uint256)');
    const log = receipt.logs?.find((l: { topics: string[] }) => l.topics[0] === listedTopic);
    const listingId = log ? BigInt(log.topics[1]).toString() : '0';

    return {
      listingId,
      nftContract,
      tokenId,
      price: priceQFC,
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${tx.hash}`,
    };
  }

  /**
   * Buy a listed NFT. Sends native QFC as payment.
   */
  async buyNFT(
    marketplace: string,
    listingId: number,
    signer: ethers.Wallet,
  ): Promise<BuyNFTResult> {
    const connected = signer.connect(this.provider);
    const mp = new ethers.Contract(marketplace, MARKETPLACE_ABI, this.provider);

    const [, , , price, active] = await mp.getListing(listingId);
    if (!active) throw new Error(`Listing ${listingId} is not active`);

    const mpConnected = new ethers.Contract(marketplace, MARKETPLACE_ABI, connected);
    const txData = await mpConnected.buy.populateTransaction(listingId);
    txData.value = price;
    txData.gasLimit = 300_000n;
    const tx = await connected.sendTransaction(txData);
    const receipt = await this.waitForReceipt(tx.hash);

    if (receipt.status !== '0x1') {
      throw new Error(`Purchase failed (tx: ${tx.hash})`);
    }

    return {
      listingId,
      price: ethers.formatEther(price),
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${tx.hash}`,
    };
  }

  /**
   * Cancel an active listing (seller only).
   */
  async cancelListing(
    marketplace: string,
    listingId: number,
    signer: ethers.Wallet,
  ): Promise<{ txHash: string; explorerUrl: string }> {
    const connected = signer.connect(this.provider);
    const mp = new ethers.Contract(marketplace, MARKETPLACE_ABI, connected);
    const txData = await mp.cancel.populateTransaction(listingId);
    txData.gasLimit = 100_000n;
    const tx = await connected.sendTransaction(txData);
    const receipt = await this.waitForReceipt(tx.hash);

    if (receipt.status !== '0x1') {
      throw new Error(`Cancel failed (tx: ${tx.hash})`);
    }

    return {
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${tx.hash}`,
    };
  }

  /**
   * Get a specific listing by ID.
   */
  async getListing(marketplace: string, listingId: number): Promise<ListingInfo> {
    const mp = new ethers.Contract(marketplace, MARKETPLACE_ABI, this.provider);
    const [seller, nftContract, tokenId, price, active] = await mp.getListing(listingId);
    return {
      listingId,
      seller,
      nftContract,
      tokenId: Number(tokenId),
      price: ethers.formatEther(price),
      active,
    };
  }

  /**
   * Get all active listings.
   */
  async getListings(marketplace: string): Promise<ListingInfo[]> {
    const mp = new ethers.Contract(marketplace, MARKETPLACE_ABI, this.provider);
    const nextId = await mp.nextListingId();
    const total = Number(nextId);
    const listings: ListingInfo[] = [];

    for (let i = 0; i < total; i++) {
      const [seller, nftContract, tokenId, price, active] = await mp.getListing(i);
      if (active) {
        listings.push({
          listingId: i,
          seller,
          nftContract,
          tokenId: Number(tokenId),
          price: ethers.formatEther(price),
          active: true,
        });
      }
    }

    return listings;
  }

  /**
   * Get active listings filtered by NFT collection.
   */
  async getListingsByCollection(marketplace: string, nftContract: string): Promise<ListingInfo[]> {
    const all = await this.getListings(marketplace);
    return all.filter((l) => l.nftContract.toLowerCase() === nftContract.toLowerCase());
  }

  /**
   * Get marketplace fee info.
   */
  async getFeeInfo(marketplace: string): Promise<{ feeBps: number; feePercent: string; feeRecipient: string; owner: string }> {
    const mp = new ethers.Contract(marketplace, MARKETPLACE_ABI, this.provider);
    const [feeBps, recipient, owner] = await Promise.all([
      mp.feeBps(),
      mp.feeRecipient(),
      mp.owner(),
    ]);
    return {
      feeBps: Number(feeBps),
      feePercent: `${Number(feeBps) / 100}%`,
      feeRecipient: recipient,
      owner,
    };
  }

  /**
   * Update marketplace fee (owner only).
   * @param marketplace - marketplace contract address
   * @param feeBps - new fee in basis points (max 1000 = 10%)
   * @param feeRecipient - new fee recipient (optional, pass undefined to keep current)
   * @param signer - marketplace owner wallet
   */
  async setFee(
    marketplace: string,
    feeBps: number,
    signer: ethers.Wallet,
    feeRecipient?: string,
  ): Promise<{ txHash: string; explorerUrl: string }> {
    const connected = signer.connect(this.provider);
    const mp = new ethers.Contract(marketplace, MARKETPLACE_ABI, connected);
    const txData = await mp.setFee.populateTransaction(feeBps, feeRecipient ?? ethers.ZeroAddress);
    txData.gasLimit = 100_000n;
    const tx = await connected.sendTransaction(txData);
    const receipt = await this.waitForReceipt(tx.hash);

    if (receipt.status !== '0x1') {
      throw new Error(`setFee failed (tx: ${tx.hash})`);
    }

    return {
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${tx.hash}`,
    };
  }
}
