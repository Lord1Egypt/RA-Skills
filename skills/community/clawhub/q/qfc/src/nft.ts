import { ethers } from 'ethers';
import { NetworkName, createProvider, getNetworkConfig } from './provider.js';

const ERC721_ABI = [
  'function name() view returns (string)',
  'function symbol() view returns (string)',
  'function owner() view returns (address)',
  'function totalSupply() view returns (uint256)',
  'function tokenURI(uint256 tokenId) view returns (string)',
  'function ownerOf(uint256 tokenId) view returns (address)',
  'function balanceOf(address owner) view returns (uint256)',
  'function transferFrom(address from, address to, uint256 tokenId)',
  'function approve(address to, uint256 tokenId)',
  'function mint(address to, string uri)',
];

const ERC721_DEPLOY_ABI = [
  'constructor(string name, string symbol)',
  ...ERC721_ABI,
  'event Transfer(address indexed from, address indexed to, uint256 indexed tokenId)',
  'event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId)',
];

/**
 * Solidity source code for the pre-compiled ERC-721 NFT contract.
 * Compile settings: Solidity 0.8.34, evmVersion: paris, optimizer: 200 runs.
 */
export const ERC721_SOURCE_CODE = `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleNFT {
    string public name;
    string public symbol;
    address public owner;
    uint256 public totalSupply;

    mapping(uint256 => address) private _owners;
    mapping(address => uint256) private _balances;
    mapping(uint256 => address) private _tokenApprovals;
    mapping(uint256 => string) private _tokenURIs;

    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);

    modifier onlyOwner() {
        require(msg.sender == owner, "not owner");
        _;
    }

    constructor(string memory _name, string memory _symbol) {
        name = _name;
        symbol = _symbol;
        owner = msg.sender;
    }

    function mint(address to, string memory uri) external onlyOwner {
        uint256 tokenId = totalSupply;
        totalSupply++;
        _owners[tokenId] = to;
        _balances[to]++;
        _tokenURIs[tokenId] = uri;
        emit Transfer(address(0), to, tokenId);
    }

    function tokenURI(uint256 tokenId) external view returns (string memory) {
        require(_owners[tokenId] != address(0), "nonexistent token");
        return _tokenURIs[tokenId];
    }

    function ownerOf(uint256 tokenId) external view returns (address) {
        address tokenOwner = _owners[tokenId];
        require(tokenOwner != address(0), "nonexistent token");
        return tokenOwner;
    }

    function balanceOf(address _owner) external view returns (uint256) {
        require(_owner != address(0), "zero address");
        return _balances[_owner];
    }

    function approve(address to, uint256 tokenId) external {
        address tokenOwner = _owners[tokenId];
        require(msg.sender == tokenOwner, "not token owner");
        _tokenApprovals[tokenId] = to;
        emit Approval(tokenOwner, to, tokenId);
    }

    function transferFrom(address from, address to, uint256 tokenId) external {
        address tokenOwner = _owners[tokenId];
        require(tokenOwner == from, "not owner");
        require(
            msg.sender == tokenOwner || _tokenApprovals[tokenId] == msg.sender,
            "not authorized"
        );
        _tokenApprovals[tokenId] = address(0);
        _balances[from]--;
        _balances[to]++;
        _owners[tokenId] = to;
        emit Transfer(from, to, tokenId);
    }
}
`;

/**
 * Pre-compiled ERC-721 bytecode (Solidity 0.8.34, evmVersion: paris, optimizer: 200 runs).
 * Constructor: (string name, string symbol)
 */
const ERC721_DEPLOY_BYTECODE = '0x608060405234801561001057600080fd5b50604051610dbf380380610dbf83398101604081905261002f9161011b565b600061003b838261021a565b506001610048828261021a565b5050600280546001600160a01b03191633179055506102dc565b634e487b7160e01b600052604160045260246000fd5b600082601f83011261008957600080fd5b81516001600160401b038111156100a2576100a2610062565b604051601f8201601f19908116603f011681016001600160401b03811182821017156100d0576100d0610062565b6040528181528382016020018510156100e857600080fd5b60005b82811015610107576020818601810151838301820152016100eb565b506000918101602001919091529392505050565b6000806040838503121561012e57600080fd5b82516001600160401b0381111561014457600080fd5b61015085828601610078565b602085015190935090506001600160401b0381111561016e57600080fd5b61017a85828601610078565b9150509250929050565b600181811c9082168061019857607f821691505b6020821081036101b857634e487b7160e01b600052602260045260246000fd5b50919050565b601f821115610215578282111561021557806000526020600020601f840160051c60208510156101ec575060005b90810190601f840160051c0360005b81811015610211576000838201556001016101fb565b5050505b505050565b81516001600160401b0381111561023357610233610062565b610247816102418454610184565b846101be565b6020601f82116001811461027b57600083156102635750848201515b600019600385901b1c1916600184901b1784556102d5565b600084815260208120601f198516915b828110156102ab578785015182556020948501946001909201910161028b565b50848210156102c95786840151600019600387901b60f8161c191681555b505060018360011b0184555b5050505050565b610ad4806102eb6000396000f3fe608060405234801561001057600080fd5b506004361061009e5760003560e01c806370a082311161006657806370a082311461012b5780638da5cb5b1461013e57806395d89b4114610151578063c87b56dd14610159578063d0def5211461016c57600080fd5b806306fdde03146100a3578063095ea7b3146100c157806318160ddd146100d657806323b872dd146100ed5780636352211e14610100575b600080fd5b6100ab61017f565b6040516100b89190610713565b60405180910390f35b6100d46100cf36600461077d565b61020d565b005b6100df60035481565b6040519081526020016100b8565b6100d46100fb3660046107a7565b6102c7565b61011361010e3660046107e4565b610451565b6040516001600160a01b0390911681526020016100b8565b6100df6101393660046107fd565b6104b0565b600254610113906001600160a01b031681565b6100ab610513565b6100ab6101673660046107e4565b610520565b6100d461017a366004610835565b610619565b6000805461018c906108ff565b80601f01602080910402602001604051908101604052809291908181526020018280546101b8906108ff565b80156102055780601f106101da57610100808354040283529160200191610205565b820191906000526020600020905b8154815290600101906020018083116101e857829003601f168201915b505050505081565b6000818152600460205260409020546001600160a01b031633811461026b5760405162461bcd60e51b815260206004820152600f60248201526e3737ba103a37b5b2b71037bbb732b960891b60448201526064015b60405180910390fd5b60008281526006602052604080822080546001600160a01b0319166001600160a01b0387811691821790925591518593918516917f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b92591a4505050565b6000818152600460205260409020546001600160a01b03908116908416811461031e5760405162461bcd60e51b81526020600482015260096024820152683737ba1037bbb732b960b91b6044820152606401610262565b336001600160a01b038216148061034b57506000828152600660205260409020546001600160a01b031633145b6103885760405162461bcd60e51b815260206004820152600e60248201526d1b9bdd08185d5d1a1bdc9a5e995960921b6044820152606401610262565b600082815260066020908152604080832080546001600160a01b03191690556001600160a01b0387168352600590915281208054916103c68361094f565b90915550506001600160a01b03831660009081526005602052604081208054916103ef83610966565b909155505060008281526004602052604080822080546001600160a01b0319166001600160a01b0387811691821790925591518593918816917fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef91a450505050565b6000818152600460205260408120546001600160a01b0316806104aa5760405162461bcd60e51b81526020600482015260116024820152703737b732bc34b9ba32b73a103a37b5b2b760791b6044820152606401610262565b92915050565b60006001600160a01b0382166104f75760405162461bcd60e51b815260206004820152600c60248201526b7a65726f206164647265737360a01b6044820152606401610262565b506001600160a01b031660009081526005602052604090205490565b6001805461018c906108ff565b6000818152600460205260409020546060906001600160a01b031661057b5760405162461bcd60e51b81526020600482015260116024820152703737b732bc34b9ba32b73a103a37b5b2b760791b6044820152606401610262565b60008281526007602052604090208054610594906108ff565b80601f01602080910402602001604051908101604052809291908181526020018280546105c0906108ff565b801561060d5780601f106105e25761010080835404028352916020019161060d565b820191906000526020600020905b8154815290600101906020018083116105f057829003601f168201915b50505050509050919050565b6002546001600160a01b0316331461065f5760405162461bcd60e51b81526020600482015260096024820152683737ba1037bbb732b960b91b6044820152606401610262565b60038054908190600061067183610966565b9091555050600081815260046020908152604080832080546001600160a01b0319166001600160a01b0388169081179091558352600590915281208054916106b883610966565b909155505060008181526007602052604090206106d583826109db565b5060405181906001600160a01b038516906000907fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef908290a4505050565b602081526000825180602084015260005b818110156107415760208186018101516040868401015201610724565b506000604082850101526040601f19601f83011684010191505092915050565b80356001600160a01b038116811461077857600080fd5b919050565b6000806040838503121561079057600080fd5b61079983610761565b946020939093013593505050565b6000806000606084860312156107bc57600080fd5b6107c584610761565b92506107d360208501610761565b929592945050506040919091013590565b6000602082840312156107f657600080fd5b5035919050565b60006020828403121561080f57600080fd5b61081882610761565b9392505050565b634e487b7160e01b600052604160045260246000fd5b6000806040838503121561084857600080fd5b61085183610761565b9150602083013567ffffffffffffffff81111561086d57600080fd5b8301601f8101851361087e57600080fd5b803567ffffffffffffffff8111156108985761089861081f565b604051601f8201601f19908116603f0116810167ffffffffffffffff811182821017156108c7576108c761081f565b6040528181528282016020018710156108df57600080fd5b816020840160208301376000602083830101528093505050509250929050565b600181811c9082168061091357607f821691505b60208210810361093357634e487b7160e01b600052602260045260246000fd5b50919050565b634e487b7160e01b600052601160045260246000fd5b60008161095e5761095e610939565b506000190190565b60006001820161097857610978610939565b5060010190565b601f8211156109d657828211156109d657806000526020600020601f840160051c60208510156109ad575060005b90810190601f840160051c0360005b818110156109d2576000838201556001016109bc565b5050505b505050565b815167ffffffffffffffff8111156109f5576109f561081f565b610a0981610a0384546108ff565b8461097f565b6020601f821160018114610a3d5760008315610a255750848201515b600019600385901b1c1916600184901b178455610a97565b600084815260208120601f198516915b82811015610a6d5787850151825560209485019460019092019101610a4d565b5084821015610a8b5786840151600019600387901b60f8161c191681555b505060018360011b0184555b505050505056fea2646970667358221220afd2cd4d691cc4f94bd096b37f0f56f8a85a98a63ea6d72d56bfa39950ea3c0d64736f6c63430008220033';

export interface NFTDeployResult {
  contractAddress: string;
  txHash: string;
  explorerUrl: string;
  name: string;
  symbol: string;
  verified?: boolean;
}

export interface NFTMintResult {
  txHash: string;
  tokenId: string;
  explorerUrl: string;
}

export interface NFTInfo {
  contractAddress: string;
  name: string;
  symbol: string;
  totalSupply: string;
}

/**
 * QFCNFT — ERC-721 NFT operations on QFC.
 */
export class QFCNFT {
  private provider: ethers.JsonRpcProvider;
  private networkConfig;

  constructor(network: NetworkName = 'testnet') {
    this.networkConfig = getNetworkConfig(network);
    this.provider = createProvider(network);
  }

  /** Poll for transaction receipt via raw RPC (avoids ethers.js log-parsing issues on QFC) */
  private async waitForReceipt(
    txHash: string,
    timeoutMs: number = 120_000,
  ): Promise<{ status: string; contractAddress: string; blockNumber: string; gasUsed: string }> {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      await new Promise((r) => setTimeout(r, 3000));
      const raw = await this.provider.send('eth_getTransactionReceipt', [txHash]);
      if (raw) return raw;
    }
    throw new Error(`Transaction ${txHash} not confirmed after ${timeoutMs / 1000}s`);
  }

  /**
   * Deploy a new ERC-721 NFT contract on QFC.
   * Uses a pre-compiled contract (Solidity 0.8.34, Paris EVM, optimizer 200 runs).
   *
   * @param name - collection name (e.g. "My NFT Collection")
   * @param symbol - collection symbol (e.g. "MNFT")
   * @param signer - wallet to deploy from (pays gas, becomes owner)
   */
  async deploy(
    name: string,
    symbol: string,
    signer: ethers.Wallet,
  ): Promise<NFTDeployResult> {
    const connected = signer.connect(this.provider);
    const factory = new ethers.ContractFactory(ERC721_DEPLOY_ABI, ERC721_DEPLOY_BYTECODE, connected);

    const deployTx = await factory.getDeployTransaction(name, symbol);
    deployTx.gasLimit = 1_500_000n;

    const tx = await connected.sendTransaction(deployTx);
    const receipt = await this.waitForReceipt(tx.hash);

    if (receipt.status !== '0x1') {
      throw new Error(`Deploy transaction reverted (tx: ${tx.hash})`);
    }

    const result: NFTDeployResult = {
      contractAddress: receipt.contractAddress,
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/contract/${receipt.contractAddress}`,
      name,
      symbol,
    };

    // Auto-verify on explorer (best-effort)
    try {
      const abiCoder = ethers.AbiCoder.defaultAbiCoder();
      const constructorArgs = abiCoder.encode(
        ['string', 'string'],
        [name, symbol],
      ).slice(2); // remove 0x prefix

      const verifyResponse = await fetch(
        `${this.networkConfig.explorerUrl}/api/contracts/verify`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            address: receipt.contractAddress,
            sourceCode: ERC721_SOURCE_CODE,
            compilerVersion: 'v0.8.34',
            evmVersion: 'paris',
            optimizationRuns: 200,
            constructorArgs,
          }),
        },
      );
      const verifyData = await verifyResponse.json();
      result.verified = verifyData.ok && verifyData.data?.verified;
    } catch {
      result.verified = false;
    }

    return result;
  }

  /**
   * Mint a new NFT to the specified address.
   * @param contractAddress - NFT contract address
   * @param to - recipient address
   * @param uri - token metadata URI
   * @param signer - contract owner wallet
   */
  async mint(
    contractAddress: string,
    to: string,
    uri: string,
    signer: ethers.Wallet,
  ): Promise<NFTMintResult> {
    const connected = signer.connect(this.provider);
    const contract = new ethers.Contract(contractAddress, ERC721_ABI, connected);

    // Get current totalSupply before minting (this will be the new tokenId)
    const totalSupplyBefore = await contract.totalSupply();
    const tokenId = totalSupplyBefore.toString();

    const tx = await contract.mint(to, uri);
    const receipt = await this.waitForReceipt(tx.hash);

    if (receipt.status !== '0x1') {
      throw new Error(`Mint transaction reverted (tx: ${tx.hash})`);
    }

    return {
      txHash: tx.hash,
      tokenId,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${tx.hash}`,
    };
  }

  /**
   * Query the owner of a specific NFT token.
   * @param contractAddress - NFT contract address
   * @param tokenId - token ID to query
   */
  async ownerOf(contractAddress: string, tokenId: string): Promise<string> {
    const contract = new ethers.Contract(contractAddress, ERC721_ABI, this.provider);
    return contract.ownerOf(tokenId);
  }

  /**
   * Query the metadata URI for a specific NFT token.
   * @param contractAddress - NFT contract address
   * @param tokenId - token ID to query
   */
  async getTokenURI(contractAddress: string, tokenId: string): Promise<string> {
    const contract = new ethers.Contract(contractAddress, ERC721_ABI, this.provider);
    return contract.tokenURI(tokenId);
  }

  /**
   * Query the number of NFTs owned by an address.
   * @param contractAddress - NFT contract address
   * @param owner - address to query
   */
  async balanceOf(contractAddress: string, owner: string): Promise<string> {
    const contract = new ethers.Contract(contractAddress, ERC721_ABI, this.provider);
    const balance = await contract.balanceOf(owner);
    return balance.toString();
  }

  /**
   * Transfer an NFT from one address to another.
   * @param contractAddress - NFT contract address
   * @param from - current owner address
   * @param to - recipient address
   * @param tokenId - token ID to transfer
   * @param signer - wallet to sign the transaction (must be owner or approved)
   */
  async transfer(
    contractAddress: string,
    from: string,
    to: string,
    tokenId: string,
    signer: ethers.Wallet,
  ): Promise<{ txHash: string; explorerUrl: string }> {
    const connected = signer.connect(this.provider);
    const contract = new ethers.Contract(contractAddress, ERC721_ABI, connected);
    const tx = await contract.transferFrom(from, to, tokenId);
    const receipt = await this.waitForReceipt(tx.hash);

    if (receipt.status !== '0x1') {
      throw new Error(`Transfer transaction reverted (tx: ${tx.hash})`);
    }

    return {
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${tx.hash}`,
    };
  }
}
