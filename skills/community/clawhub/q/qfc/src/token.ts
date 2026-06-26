import { ethers } from 'ethers';
import { NetworkName, createProvider, getNetworkConfig } from './provider.js';

const ERC20_ABI = [
  'function name() view returns (string)',
  'function symbol() view returns (string)',
  'function decimals() view returns (uint8)',
  'function totalSupply() view returns (uint256)',
  'function balanceOf(address) view returns (uint256)',
  'function transfer(address to, uint256 amount) returns (bool)',
  'function approve(address spender, uint256 amount) returns (bool)',
  'function allowance(address owner, address spender) view returns (uint256)',
];

const MINTABLE_ABI = [
  ...ERC20_ABI,
  'function owner() view returns (address)',
  'function mint(address to, uint256 amount)',
  'function burn(uint256 amount)',
  'function transferOwnership(address newOwner)',
];

/**
 * Pre-compiled standard ERC-20 bytecode (Solidity 0.8.34, evmVersion: paris, optimizer: 200 runs).
 * Constructor: (string name, string symbol, uint256 initialSupply)
 * Fixed supply, no owner/admin. Mints initialSupply to msg.sender.
 */
const ERC20_DEPLOY_BYTECODE = '0x608060405234801561001057600080fd5b50604051610a0b380380610a0b83398101604081905261002f91610153565b600061003b848261025b565b506001610048838261025b565b506002819055336000818152600360209081526040808320859055518481527fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef910160405180910390a350505061031d565b634e487b7160e01b600052604160045260246000fd5b600082601f8301126100c157600080fd5b81516001600160401b038111156100da576100da61009a565b604051601f8201601f19908116603f011681016001600160401b03811182821017156101085761010861009a565b60405281815283820160200185101561012057600080fd5b60005b8281101561013f57602081860181015183830182015201610123565b506000918101602001919091529392505050565b60008060006060848603121561016857600080fd5b83516001600160401b0381111561017e57600080fd5b61018a868287016100b0565b602086015190945090506001600160401b038111156101a857600080fd5b6101b4868287016100b0565b925050604084015190509250925092565b600181811c908216806101d957607f821691505b6020821081036101f957634e487b7160e01b600052602260045260246000fd5b50919050565b601f821115610256578282111561025657806000526020600020601f840160051c602085101561022d575060005b90810190601f840160051c0360005b818110156102525760008382015560010161023c565b5050505b505050565b81516001600160401b038111156102745761027461009a565b6102888161028284546101c5565b846101ff565b6020601f8211600181146102bc57600083156102a45750848201515b600019600385901b1c1916600184901b178455610316565b600084815260208120601f198516915b828110156102ec57878501518255602094850194600190920191016102cc565b508482101561030a5786840151600019600387901b60f8161c191681555b505060018360011b0184555b5050505050565b6106df8061032c6000396000f3fe608060405234801561001057600080fd5b50600436106100935760003560e01c8063313ce56711610066578063313ce5671461010357806370a082311461011d57806395d89b411461013d578063a9059cbb14610145578063dd62ed3e1461015857600080fd5b806306fdde0314610098578063095ea7b3146100b657806318160ddd146100d957806323b872dd146100f0575b600080fd5b6100a0610183565b6040516100ad919061050d565b60405180910390f35b6100c96100c4366004610577565b610211565b60405190151581526020016100ad565b6100e260025481565b6040519081526020016100ad565b6100c96100fe3660046105a1565b61027e565b61010b601281565b60405160ff90911681526020016100ad565b6100e261012b3660046105de565b60036020526000908152604090205481565b6100a0610424565b6100c9610153366004610577565b610431565b6100e2610166366004610600565b600460209081526000928352604080842090915290825290205481565b6000805461019090610633565b80601f01602080910402602001604051908101604052809291908181526020018280546101bc90610633565b80156102095780601f106101de57610100808354040283529160200191610209565b820191906000526020600020905b8154815290600101906020018083116101ec57829003601f168201915b505050505081565b3360008181526004602090815260408083206001600160a01b038716808552925280832085905551919290917f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b9259061026c9086815260200190565b60405180910390a35060015b92915050565b6001600160a01b03831660009081526004602090815260408083203384529091528120548211156102e25760405162461bcd60e51b8152602060048201526009602482015268616c6c6f77616e636560b81b60448201526064015b60405180910390fd5b6001600160a01b0384166000908152600360205260409020548211156103395760405162461bcd60e51b815260206004820152600c60248201526b1a5b9cdd59999a58da595b9d60a21b60448201526064016102d9565b6001600160a01b03841660009081526004602090815260408083203384529091528120805484929061036c908490610683565b90915550506001600160a01b03841660009081526003602052604081208054849290610399908490610683565b90915550506001600160a01b038316600090815260036020526040812080548492906103c6908490610696565b92505081905550826001600160a01b0316846001600160a01b03167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef8460405161041291815260200190565b60405180910390a35060019392505050565b6001805461019090610633565b3360009081526003602052604081205482111561047f5760405162461bcd60e51b815260206004820152600c60248201526b1a5b9cdd59999a58da595b9d60a21b60448201526064016102d9565b336000908152600360205260408120805484929061049e908490610683565b90915550506001600160a01b038316600090815260036020526040812080548492906104cb908490610696565b90915550506040518281526001600160a01b0384169033907fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef9060200161026c565b602081526000825180602084015260005b8181101561053b576020818601810151604086840101520161051e565b506000604082850101526040601f19601f83011684010191505092915050565b80356001600160a01b038116811461057257600080fd5b919050565b6000806040838503121561058a57600080fd5b6105938361055b565b946020939093013593505050565b6000806000606084860312156105b657600080fd5b6105bf8461055b565b92506105cd6020850161055b565b929592945050506040919091013590565b6000602082840312156105f057600080fd5b6105f98261055b565b9392505050565b6000806040838503121561061357600080fd5b61061c8361055b565b915061062a6020840161055b565b90509250929050565b600181811c9082168061064757607f821691505b60208210810361066757634e487b7160e01b600052602260045260246000fd5b50919050565b634e487b7160e01b600052601160045260246000fd5b818103818111156102785761027861066d565b808201808211156102785761027861066d56fea2646970667358221220bc4560f884ebdaced06b888d9b0b68a9d9920c5a2aa25f33d7bd2fdb534dda3364736f6c63430008220033';

/**
 * Pre-compiled Mintable/Burnable ERC-20 bytecode (Solidity 0.8.34, evmVersion: paris, optimizer: 200 runs).
 * Constructor: (string name, string symbol, uint256 initialSupply)
 * Has owner, mint(onlyOwner), burn(anyone), transferOwnership.
 */
const MINTABLE_DEPLOY_BYTECODE = '0x608060405234801561001057600080fd5b50604051610cfc380380610cfc83398101604081905261002f9161016c565b600061003b8482610274565b5060016100488382610274565b50600380546001600160a01b0319163317905580156100ab576002819055336000818152600460209081526040808320859055518481527fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef910160405180910390a35b505050610336565b634e487b7160e01b600052604160045260246000fd5b600082601f8301126100da57600080fd5b81516001600160401b038111156100f3576100f36100b3565b604051601f8201601f19908116603f011681016001600160401b0381118282101715610121576101216100b3565b60405281815283820160200185101561013957600080fd5b60005b828110156101585760208186018101518383018201520161013c565b506000918101602001919091529392505050565b60008060006060848603121561018157600080fd5b83516001600160401b0381111561019757600080fd5b6101a3868287016100c9565b602086015190945090506001600160401b038111156101c157600080fd5b6101cd868287016100c9565b925050604084015190509250925092565b600181811c908216806101f257607f821691505b60208210810361021257634e487b7160e01b600052602260045260246000fd5b50919050565b601f82111561026f578282111561026f57806000526020600020601f840160051c6020851015610246575060005b90810190601f840160051c0360005b8181101561026b57600083820155600101610255565b5050505b505050565b81516001600160401b0381111561028d5761028d6100b3565b6102a18161029b84546101de565b84610218565b6020601f8211600181146102d557600083156102bd5750848201515b600019600385901b1c1916600184901b17845561032f565b600084815260208120601f198516915b8281101561030557878501518255602094850194600190920191016102e5565b50848210156103235786840151600019600387901b60f8161c191681555b505060018360011b0184555b5050505050565b6109b7806103456000396000f3fe608060405234801561001057600080fd5b50600436106100cf5760003560e01c806342966c681161008c57806395d89b411161006657806395d89b41146101cc578063a9059cbb146101d4578063dd62ed3e146101e7578063f2fde38b1461021257600080fd5b806342966c681461016e57806370a08231146101815780638da5cb5b146101a157600080fd5b806306fdde03146100d4578063095ea7b3146100f257806318160ddd1461011557806323b872dd1461012c578063313ce5671461013f57806340c10f1914610159575b600080fd5b6100dc610225565b6040516100e99190610786565b60405180910390f35b6101056101003660046107f0565b6102b3565b60405190151581526020016100e9565b61011e60025481565b6040519081526020016100e9565b61010561013a36600461081a565b610320565b610147601281565b60405160ff90911681526020016100e9565b61016c6101673660046107f0565b610495565b005b61016c61017c366004610857565b610552565b61011e61018f366004610870565b60046020526000908152604090205481565b6003546101b4906001600160a01b031681565b6040516001600160a01b0390911681526020016100e9565b6100dc6105e7565b6101056101e23660046107f0565b6105f4565b61011e6101f5366004610892565b600560209081526000928352604080842090915290825290205481565b61016c610220366004610870565b61069f565b60008054610232906108c5565b80601f016020809104026020016040519081016040528092919081815260200182805461025e906108c5565b80156102ab5780601f10610280576101008083540402835291602001916102ab565b820191906000526020600020905b81548152906001019060200180831161028e57829003601f168201915b505050505081565b3360008181526005602090815260408083206001600160a01b038716808552925280832085905551919290917f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b9259061030e9086815260200190565b60405180910390a35060015b92915050565b6001600160a01b03831660009081526005602090815260408083203384529091528120548211156103845760405162461bcd60e51b8152602060048201526009602482015268616c6c6f77616e636560b81b60448201526064015b60405180910390fd5b6001600160a01b0384166000908152600460205260409020548211156103bc5760405162461bcd60e51b815260040161037b906108ff565b6001600160a01b0384166000908152600560209081526040808320338452909152812080548492906103ef90849061093b565b90915550506001600160a01b0384166000908152600460205260408120805484929061041c90849061093b565b90915550506001600160a01b0383166000908152600460205260408120805484929061044990849061094e565b92505081905550826001600160a01b0316846001600160a01b03166000805160206109628339815191528460405161048291815260200190565b60405180910390a35060019392505050565b6003546001600160a01b031633146104db5760405162461bcd60e51b81526020600482015260096024820152683737ba1037bbb732b960b91b604482015260640161037b565b80600260008282546104ed919061094e565b90915550506001600160a01b0382166000908152600460205260408120805483929061051a90849061094e565b90915550506040518181526001600160a01b038316906000906000805160206109628339815191529060200160405180910390a35050565b336000908152600460205260409020548111156105815760405162461bcd60e51b815260040161037b906108ff565b33600090815260046020526040812080548392906105a090849061093b565b9250508190555080600260008282546105b9919061093b565b909155505060405181815260009033906000805160206109628339815191529060200160405180910390a350565b60018054610232906108c5565b336000908152600460205260408120548211156106235760405162461bcd60e51b815260040161037b906108ff565b336000908152600460205260408120805484929061064290849061093b565b90915550506001600160a01b0383166000908152600460205260408120805484929061066f90849061094e565b90915550506040518281526001600160a01b0384169033906000805160206109628339815191529060200161030e565b6003546001600160a01b031633146106e55760405162461bcd60e51b81526020600482015260096024820152683737ba1037bbb732b960b91b604482015260640161037b565b6001600160a01b03811661072a5760405162461bcd60e51b815260206004820152600c60248201526b7a65726f206164647265737360a01b604482015260640161037b565b6003546040516001600160a01b038084169216907f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e090600090a3600380546001600160a01b0319166001600160a01b0392909216919091179055565b602081526000825180602084015260005b818110156107b45760208186018101516040868401015201610797565b506000604082850101526040601f19601f83011684010191505092915050565b80356001600160a01b03811681146107eb57600080fd5b919050565b6000806040838503121561080357600080fd5b61080c836107d4565b946020939093013593505050565b60008060006060848603121561082f57600080fd5b610838846107d4565b9250610846602085016107d4565b929592945050506040919091013590565b60006020828403121561086957600080fd5b5035919050565b60006020828403121561088257600080fd5b61088b826107d4565b9392505050565b600080604083850312156108a557600080fd5b6108ae836107d4565b91506108bc602084016107d4565b90509250929050565b600181811c908216806108d957607f821691505b6020821081036108f957634e487b7160e01b600052602260045260246000fd5b50919050565b6020808252600c908201526b1a5b9cdd59999a58da595b9d60a21b604082015260600190565b634e487b7160e01b600052601160045260246000fd5b8181038181111561031a5761031a610925565b8082018082111561031a5761031a61092556feddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3efa26469706673582212205dd491e3da12a9fbeb893f0d82ae13bfc439cb88036854009699bfd0fe98c2f564736f6c63430008220033';

const ERC20_DEPLOY_ABI = [
  'constructor(string name, string symbol, uint256 initialSupply)',
  ...ERC20_ABI,
  'event Transfer(address indexed from, address indexed to, uint256 value)',
  'event Approval(address indexed owner, address indexed spender, uint256 value)',
];

const MINTABLE_DEPLOY_ABI = [
  'constructor(string name, string symbol, uint256 initialSupply)',
  ...MINTABLE_ABI,
  'event Transfer(address indexed from, address indexed to, uint256 value)',
  'event Approval(address indexed owner, address indexed spender, uint256 value)',
  'event OwnershipTransferred(address indexed previousOwner, address indexed newOwner)',
];

/**
 * Pre-compiled Airdrop contract bytecode (Solidity 0.8.34, evmVersion: paris, optimizer: 200 runs).
 * No constructor args — deploy once, use for any ERC-20 token.
 */
const AIRDROP_DEPLOY_BYTECODE = '0x6080604052348015600f57600080fd5b506104ae8061001f6000396000f3fe608060405234801561001057600080fd5b50600436106100365760003560e01c8063025ff12f1461003b578063abdcd94814610050575b600080fd5b61004e61004936600461033e565b610063565b005b61004e61005e3660046103c4565b6101cd565b8281146100a95760405162461bcd60e51b815260206004820152600f60248201526e0d8cadccee8d040dad2e6dac2e8c6d608b1b60448201526064015b60405180910390fd5b8460005b848110156101c457816001600160a01b03166323b872dd338888858181106100d7576100d761041e565b90506020020160208101906100ec9190610434565b8787868181106100fe576100fe61041e565b6040516001600160e01b031960e088901b1681526001600160a01b039586166004820152949093166024850152506020909102013560448201526064016020604051808303816000875af115801561015a573d6000803e3d6000fd5b505050506040513d601f19601f8201168201806040525081019061017e9190610456565b6101bc5760405162461bcd60e51b815260206004820152600f60248201526e1d1c985b9cd9995c8819985a5b1959608a1b60448201526064016100a0565b6001016100ad565b50505050505050565b8360005b838110156102ce57816001600160a01b03166323b872dd338787858181106101fb576101fb61041e565b90506020020160208101906102109190610434565b6040516001600160e01b031960e085901b1681526001600160a01b03928316600482015291166024820152604481018690526064016020604051808303816000875af1158015610264573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906102889190610456565b6102c65760405162461bcd60e51b815260206004820152600f60248201526e1d1c985b9cd9995c8819985a5b1959608a1b60448201526064016100a0565b6001016101d1565b505050505050565b80356001600160a01b03811681146102ed57600080fd5b919050565b60008083601f84011261030457600080fd5b50813567ffffffffffffffff81111561031c57600080fd5b6020830191508360208260051b850101111561033757600080fd5b9250929050565b60008060008060006060868803121561035657600080fd5b61035f866102d6565b9450602086013567ffffffffffffffff81111561037b57600080fd5b610387888289016102f2565b909550935050604086013567ffffffffffffffff8111156103a757600080fd5b6103b3888289016102f2565b969995985093965092949392505050565b600080600080606085870312156103da57600080fd5b6103e3856102d6565b9350602085013567ffffffffffffffff8111156103ff57600080fd5b61040b878288016102f2565b9598909750949560400135949350505050565b634e487b7160e01b600052603260045260246000fd5b60006020828403121561044657600080fd5b61044f826102d6565b9392505050565b60006020828403121561046857600080fd5b8151801515811461044f57600080fdfea26469706673582212203eb0a41af2cb5dfbd501567cc78dee6e5025d68b30071e396c8946dfa9e6937464736f6c63430008220033';

const AIRDROP_ABI = [
  'function airdrop(address token, address[] recipients, uint256[] amounts)',
  'function airdropFixed(address token, address[] recipients, uint256 amount)',
];

/**
 * Solidity source code for the Airdrop contract.
 */
export const AIRDROP_SOURCE_CODE = `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
}

contract Airdrop {
    function airdrop(
        address token,
        address[] calldata recipients,
        uint256[] calldata amounts
    ) external {
        require(recipients.length == amounts.length, "length mismatch");
        IERC20 t = IERC20(token);
        for (uint256 i = 0; i < recipients.length; i++) {
            require(t.transferFrom(msg.sender, recipients[i], amounts[i]), "transfer failed");
        }
    }

    function airdropFixed(
        address token,
        address[] calldata recipients,
        uint256 amount
    ) external {
        IERC20 t = IERC20(token);
        for (uint256 i = 0; i < recipients.length; i++) {
            require(t.transferFrom(msg.sender, recipients[i], amount), "transfer failed");
        }
    }
}
`;

/**
 * Solidity source code for the pre-compiled standard ERC-20 token.
 */
export const ERC20_SOURCE_CODE = `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleToken {
    string public name;
    string public symbol;
    uint8 public constant decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    constructor(string memory _name, string memory _symbol, uint256 _initialSupply) {
        name = _name;
        symbol = _symbol;
        totalSupply = _initialSupply;
        balanceOf[msg.sender] = _initialSupply;
        emit Transfer(address(0), msg.sender, _initialSupply);
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        require(balanceOf[msg.sender] >= amount, "insufficient");
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        emit Transfer(msg.sender, to, amount);
        return true;
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        require(allowance[from][msg.sender] >= amount, "allowance");
        require(balanceOf[from] >= amount, "insufficient");
        allowance[from][msg.sender] -= amount;
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        emit Transfer(from, to, amount);
        return true;
    }
}
`;

/**
 * Solidity source code for the pre-compiled Mintable/Burnable ERC-20 token.
 */
export const MINTABLE_SOURCE_CODE = `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MintableToken {
    string public name;
    string public symbol;
    uint8 public constant decimals = 18;
    uint256 public totalSupply;
    address public owner;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    modifier onlyOwner() {
        require(msg.sender == owner, "not owner");
        _;
    }

    constructor(string memory _name, string memory _symbol, uint256 _initialSupply) {
        name = _name;
        symbol = _symbol;
        owner = msg.sender;
        if (_initialSupply > 0) {
            totalSupply = _initialSupply;
            balanceOf[msg.sender] = _initialSupply;
            emit Transfer(address(0), msg.sender, _initialSupply);
        }
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        require(balanceOf[msg.sender] >= amount, "insufficient");
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        emit Transfer(msg.sender, to, amount);
        return true;
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        require(allowance[from][msg.sender] >= amount, "allowance");
        require(balanceOf[from] >= amount, "insufficient");
        allowance[from][msg.sender] -= amount;
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        emit Transfer(from, to, amount);
        return true;
    }

    function mint(address to, uint256 amount) external onlyOwner {
        totalSupply += amount;
        balanceOf[to] += amount;
        emit Transfer(address(0), to, amount);
    }

    function burn(uint256 amount) external {
        require(balanceOf[msg.sender] >= amount, "insufficient");
        balanceOf[msg.sender] -= amount;
        totalSupply -= amount;
        emit Transfer(msg.sender, address(0), amount);
    }

    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "zero address");
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }
}
`;

export interface TokenInfo {
  address: string;
  name: string;
  symbol: string;
  decimals: number;
  totalSupply: string;
}

export interface PortfolioItem {
  address: string;
  name: string;
  symbol: string;
  decimals: number;
  balance: string;
  raw: string;
}

export interface PortfolioResult {
  owner: string;
  nativeBalance: string;
  tokens: PortfolioItem[];
}

export interface TokenTransfer {
  txHash: string;
  blockHeight: number;
  from: string;
  to: string;
  value: string;
  tokenAddress: string;
  tokenSymbol: string;
}

export interface TransferHistoryResult {
  address: string;
  tokenAddress: string;
  tokenSymbol: string;
  transfers: TokenTransfer[];
  page: number;
  limit: number;
}

export interface LaunchResult {
  token: DeployTokenResult;
  pool: { poolAddress: string; txHash: string; explorerUrl: string };
  liquidity: { lpMinted: string; amountToken: string; amountWQFC: string; txHash: string };
}

export interface TokenBalance {
  token: string;
  symbol: string;
  decimals: number;
  balance: string;
  raw: string;
}

export interface TokenTxResult {
  txHash: string;
  explorerUrl: string;
}

export interface BatchTransferItem {
  to: string;
  amount: string;
}

export interface BatchTransferResult {
  successful: {to: string; amount: string; txHash: string}[];
  failed: {to: string; amount: string; error: string}[];
}

export interface AirdropDeployResult {
  contractAddress: string;
  txHash: string;
  explorerUrl: string;
}

export interface AirdropResult {
  airdropContract: string;
  tokenAddress: string;
  recipientCount: number;
  txHash: string;
  explorerUrl: string;
}

export interface DeployTokenResult {
  contractAddress: string;
  txHash: string;
  explorerUrl: string;
  name: string;
  symbol: string;
  decimals: number;
  totalSupply: string;
  owner: string;
  mintable: boolean;
  verified?: boolean;
}

/** Default caller address for eth_call to avoid QFC testnet 'lack of funds' validation */
const DEFAULT_CALL_FROM = '0x0000000000000000000000000000000000000001';

/**
 * QFCToken — ERC-20 token operations on QFC.
 */
export class QFCToken {
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
   * Deploy a new ERC-20 token on QFC.
   * Uses a pre-compiled contract (Solidity 0.8.34, Paris EVM, optimizer 200 runs).
   * The entire initialSupply is minted to the deployer's address.
   *
   * @param name - token name (e.g. "My Token")
   * @param symbol - token symbol (e.g. "MTK")
   * @param initialSupply - human-readable supply (e.g. "1000000" for 1M tokens with 18 decimals)
   * @param signer - wallet to deploy from (pays gas, receives all tokens)
   * @param mintable - if true, deploy mintable/burnable version with owner (default: false)
   */
  async deploy(
    name: string,
    symbol: string,
    initialSupply: string,
    signer: ethers.Wallet,
    mintable: boolean = false,
  ): Promise<DeployTokenResult> {
    const connected = signer.connect(this.provider);
    const abi = mintable ? MINTABLE_DEPLOY_ABI : ERC20_DEPLOY_ABI;
    const bytecode = mintable ? MINTABLE_DEPLOY_BYTECODE : ERC20_DEPLOY_BYTECODE;
    const factory = new ethers.ContractFactory(abi, bytecode, connected);

    const supplyWei = ethers.parseEther(initialSupply);
    const deployTx = await factory.getDeployTransaction(name, symbol, supplyWei);
    deployTx.gasLimit = mintable ? 1_000_000n : 800_000n;

    const tx = await connected.sendTransaction(deployTx);
    const receipt = await this.waitForReceipt(tx.hash);

    if (receipt.status !== '0x1') {
      throw new Error(`Deploy transaction reverted (tx: ${tx.hash})`);
    }

    const result: DeployTokenResult = {
      contractAddress: receipt.contractAddress,
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/contract/${receipt.contractAddress}`,
      name,
      symbol,
      decimals: 18,
      totalSupply: initialSupply,
      owner: signer.address,
      mintable,
    };

    // Auto-verify on explorer (best-effort, don't fail deployment if verification fails)
    try {
      const sourceCode = mintable ? MINTABLE_SOURCE_CODE : ERC20_SOURCE_CODE;
      const abiCoder = ethers.AbiCoder.defaultAbiCoder();
      const constructorArgs = abiCoder.encode(
        ['string', 'string', 'uint256'],
        [name, symbol, supplyWei],
      ).slice(2); // remove 0x prefix

      const verifyResponse = await fetch(
        `${this.networkConfig.explorerUrl}/api/contracts/verify`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            address: receipt.contractAddress,
            sourceCode,
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
   * Mint new tokens (only works on mintable tokens, caller must be owner).
   * @param tokenAddress - mintable token contract address
   * @param to - recipient address
   * @param amount - human-readable amount (e.g. "1000")
   * @param signer - token owner wallet
   */
  async mint(
    tokenAddress: string,
    to: string,
    amount: string,
    signer: ethers.Wallet,
  ): Promise<TokenTxResult> {
    const connected = signer.connect(this.provider);
    const contract = new ethers.Contract(tokenAddress, MINTABLE_ABI, connected);
    const parsedAmount = ethers.parseEther(amount);
    const tx = await contract.mint(to, parsedAmount);
    const receipt = await this.waitForReceipt(tx.hash);
    return {
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${receipt.blockNumber ? tx.hash : tx.hash}`,
    };
  }

  /**
   * Burn tokens (reduces total supply). Anyone can burn their own tokens.
   * @param tokenAddress - mintable token contract address
   * @param amount - human-readable amount to burn (e.g. "500")
   * @param signer - wallet holding the tokens to burn
   */
  async burn(
    tokenAddress: string,
    amount: string,
    signer: ethers.Wallet,
  ): Promise<TokenTxResult> {
    const connected = signer.connect(this.provider);
    const contract = new ethers.Contract(tokenAddress, MINTABLE_ABI, connected);
    const parsedAmount = ethers.parseEther(amount);
    const tx = await contract.burn(parsedAmount);
    const receipt = await this.waitForReceipt(tx.hash);
    return {
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${receipt.blockNumber ? tx.hash : tx.hash}`,
    };
  }

  /**
   * List contracts deployed by an address.
   * Scans the deployer's transaction history for contract creation transactions
   * (transactions where `to` is null) and returns the created contract addresses.
   * @param owner - deployer address
   */
  async getDeployedTokens(owner: string): Promise<{ address: string; txHash: string; block: number }[]> {
    const results: { address: string; txHash: string; block: number }[] = [];
    const nonce = await this.provider.getTransactionCount(owner);

    for (let i = 0; i < nonce; i++) {
      // Compute the contract address that would be created at each nonce
      const contractAddr = ethers.getCreateAddress({ from: owner, nonce: i });
      const code = await this.provider.getCode(contractAddr);
      if (code !== '0x') {
        // This nonce created a contract — get the tx hash from explorer
        try {
          const response = await fetch(
            `${this.networkConfig.explorerUrl}/api/contract/${contractAddr}`,
          );
          const data = await response.json();
          results.push({
            address: contractAddr,
            txHash: data.data?.creator_tx ?? '',
            block: Number(data.data?.created_at_block ?? 0),
          });
        } catch {
          results.push({ address: contractAddr, txHash: '', block: 0 });
        }
      }
    }
    return results;
  }

  /**
   * Launch a new token with initial DEX liquidity in one call.
   * Steps: deploy token → deploy WQFC pool → wrap QFC → add liquidity.
   *
   * @param name - token name
   * @param symbol - token symbol
   * @param totalSupply - total supply (human-readable, e.g. "1000000")
   * @param liquidityTokenAmount - amount of tokens to add as liquidity (human-readable)
   * @param liquidityQFCAmount - amount of native QFC to pair (human-readable)
   * @param wqfcAddress - deployed WQFC contract address
   * @param signer - wallet (pays gas, receives remaining tokens)
   * @param mintable - deploy as mintable token (default false)
   */
  async launch(
    name: string,
    symbol: string,
    totalSupply: string,
    liquidityTokenAmount: string,
    liquidityQFCAmount: string,
    wqfcAddress: string,
    signer: ethers.Wallet,
    mintable: boolean = false,
  ): Promise<LaunchResult> {
    // Dynamic import to avoid circular dependency
    const { QFCSwap } = await import('./swap.js');
    const swap = new QFCSwap(this.networkConfig.name === 'QFC Testnet' ? 'testnet' : 'mainnet');

    // Step 1: Deploy token
    const token = await this.deploy(name, symbol, totalSupply, signer, mintable);

    // Step 2: Wrap QFC → WQFC
    await swap.wrapQFC(wqfcAddress, liquidityQFCAmount, signer);

    // Step 3: Deploy pool (token ↔ WQFC)
    const pool = await swap.deployPool(token.contractAddress, wqfcAddress, signer);

    // Step 4: Add liquidity
    const liquidity = await swap.addLiquidity(
      pool.poolAddress,
      liquidityTokenAmount,
      liquidityQFCAmount,
      signer,
    );

    return {
      token,
      pool: { poolAddress: pool.poolAddress, txHash: pool.txHash, explorerUrl: pool.explorerUrl },
      liquidity: {
        lpMinted: liquidity.lpMinted,
        amountToken: liquidityTokenAmount,
        amountWQFC: liquidityQFCAmount,
        txHash: liquidity.txHash,
      },
    };
  }

  /** Get token metadata (name, symbol, decimals, totalSupply) */
  async getTokenInfo(tokenAddress: string): Promise<TokenInfo> {
    const contract = new ethers.Contract(tokenAddress, ERC20_ABI, this.provider);
    const callOverrides = { from: DEFAULT_CALL_FROM };
    const [name, symbol, decimals, totalSupply] = await Promise.all([
      contract.name(callOverrides),
      contract.symbol(callOverrides),
      contract.decimals(callOverrides),
      contract.totalSupply(callOverrides),
    ]);
    return {
      address: tokenAddress,
      name,
      symbol,
      decimals: Number(decimals),
      totalSupply: ethers.formatUnits(totalSupply, decimals),
    };
  }

  /** Get token balance for an address */
  async getBalance(tokenAddress: string, owner: string): Promise<TokenBalance> {
    const contract = new ethers.Contract(tokenAddress, ERC20_ABI, this.provider);
    const callOverrides = { from: DEFAULT_CALL_FROM };
    const [symbol, decimals, balance] = await Promise.all([
      contract.symbol(callOverrides),
      contract.decimals(callOverrides),
      contract.balanceOf(owner, callOverrides),
    ]);
    const dec = Number(decimals);
    return {
      token: tokenAddress,
      symbol,
      decimals: dec,
      balance: ethers.formatUnits(balance, dec),
      raw: balance.toString(),
    };
  }

  /**
   * Transfer ERC-20 tokens.
   * @param tokenAddress - token contract address
   * @param to - recipient address
   * @param amount - human-readable amount (e.g. "100.5")
   * @param signer - wallet to sign the transaction
   */
  async transfer(
    tokenAddress: string,
    to: string,
    amount: string,
    signer: ethers.Wallet,
  ): Promise<TokenTxResult> {
    const connected = signer.connect(this.provider);
    const contract = new ethers.Contract(tokenAddress, ERC20_ABI, connected);
    const decimals = await contract.decimals();
    const parsedAmount = ethers.parseUnits(amount, decimals);
    const tx = await contract.transfer(to, parsedAmount);
    const receipt = await this.waitForReceipt(tx.hash);
    if (receipt.status !== '0x1') {
      throw new Error(`Transfer reverted (tx: ${tx.hash})`);
    }
    return {
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${tx.hash}`,
    };
  }

  /**
   * Approve a spender to use tokens on your behalf.
   * @param tokenAddress - token contract address
   * @param spender - address to approve
   * @param amount - human-readable amount (e.g. "1000"), or "max" for unlimited
   * @param signer - wallet to sign the transaction
   */
  async approve(
    tokenAddress: string,
    spender: string,
    amount: string,
    signer: ethers.Wallet,
  ): Promise<TokenTxResult> {
    const connected = signer.connect(this.provider);
    const contract = new ethers.Contract(tokenAddress, ERC20_ABI, connected);
    const decimals = await contract.decimals();
    const parsedAmount =
      amount === 'max' ? ethers.MaxUint256 : ethers.parseUnits(amount, decimals);
    const tx = await contract.approve(spender, parsedAmount);
    const receipt = await this.waitForReceipt(tx.hash);
    if (receipt.status !== '0x1') {
      throw new Error(`Approve reverted (tx: ${tx.hash})`);
    }
    return {
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${tx.hash}`,
    };
  }

  /**
   * Check allowance for a spender.
   * @param tokenAddress - token contract address
   * @param owner - token owner address
   * @param spender - approved spender address
   */
  async getAllowance(
    tokenAddress: string,
    owner: string,
    spender: string,
  ): Promise<string> {
    const contract = new ethers.Contract(tokenAddress, ERC20_ABI, this.provider);
    const callOverrides = { from: DEFAULT_CALL_FROM };
    const [decimals, allowance] = await Promise.all([
      contract.decimals(callOverrides),
      contract.allowance(owner, spender, callOverrides),
    ]);
    return ethers.formatUnits(allowance, decimals);
  }

  /**
   * Get token portfolio for an address — native QFC balance plus all known ERC-20 token balances.
   * Fetches the token list from the explorer API, then queries balanceOf for each token.
   * @param owner - wallet address to check
   */
  async getPortfolio(owner: string): Promise<PortfolioResult> {
    const nativeBalance = await this.provider.getBalance(owner);

    // Fetch known tokens from explorer
    let tokenAddresses: { address: string; name: string | null; symbol: string | null; decimals: number | null }[] = [];
    try {
      const response = await fetch(
        `${this.networkConfig.explorerUrl}/api/tokens?limit=100`,
      );
      const data = await response.json();
      if (data.ok && data.data?.items) {
        tokenAddresses = data.data.items;
      }
    } catch {
      // Explorer unavailable — fall back to empty list
    }

    // Query balanceOf for each token in parallel
    const tokens: PortfolioItem[] = [];
    const results = await Promise.allSettled(
      tokenAddresses.map(async (token) => {
        const contract = new ethers.Contract(token.address, ERC20_ABI, this.provider);
        const co = { from: DEFAULT_CALL_FROM };
        const [balance, name, symbol, decimals] = await Promise.all([
          contract.balanceOf(owner, co),
          token.name ?? contract.name(co),
          token.symbol ?? contract.symbol(co),
          token.decimals ?? contract.decimals(co),
        ]);
        return { address: token.address, name, symbol, decimals: Number(decimals), balance };
      }),
    );

    for (const result of results) {
      if (result.status === 'fulfilled') {
        const { address, name, symbol, decimals, balance } = result.value;
        if (balance > 0n) {
          tokens.push({
            address,
            name,
            symbol,
            decimals,
            balance: ethers.formatUnits(balance, decimals),
            raw: balance.toString(),
          });
        }
      }
    }

    return {
      owner,
      nativeBalance: ethers.formatEther(nativeBalance),
      tokens,
    };
  }

  /**
   * Get transfer history for a specific token, filtered by address.
   * Uses the explorer API to fetch token transfer events.
   * @param tokenAddress - ERC-20 token contract address
   * @param address - filter transfers involving this address (sender or receiver)
   * @param page - page number (default 1)
   * @param limit - results per page (default 20)
   */
  async getTransferHistory(
    tokenAddress: string,
    address?: string,
    page: number = 1,
    limit: number = 20,
  ): Promise<TransferHistoryResult> {
    // Get token symbol for display
    let tokenSymbol = '';
    try {
      const contract = new ethers.Contract(tokenAddress, ERC20_ABI, this.provider);
      tokenSymbol = await contract.symbol({ from: DEFAULT_CALL_FROM });
    } catch {
      tokenSymbol = 'UNKNOWN';
    }

    // Fetch transfers from explorer
    const transfers: TokenTransfer[] = [];
    try {
      const response = await fetch(
        `${this.networkConfig.explorerUrl}/api/tokens/${tokenAddress}?page=${page}&limit=${limit}`,
      );
      const data = await response.json();
      if (data.ok && data.data?.transfers) {
        for (const tx of data.data.transfers) {
          // Filter by address if specified
          if (address && tx.from_address !== address && tx.to_address !== address) {
            continue;
          }
          transfers.push({
            txHash: tx.tx_hash,
            blockHeight: Number(tx.block_height),
            from: tx.from_address,
            to: tx.to_address,
            value: tx.value,
            tokenAddress,
            tokenSymbol,
          });
        }
      }
    } catch {
      // Explorer unavailable
    }

    return {
      address: address ?? '',
      tokenAddress,
      tokenSymbol,
      transfers,
      page,
      limit,
    };
  }

  /**
   * Deploy the Airdrop contract (one-time). Once deployed, use `airdrop()` to batch-transfer
   * any ERC-20 token in a single transaction.
   * @param signer - wallet to deploy from (pays gas)
   */
  async deployAirdrop(signer: ethers.Wallet): Promise<AirdropDeployResult> {
    const connected = signer.connect(this.provider);
    const factory = new ethers.ContractFactory(AIRDROP_ABI, AIRDROP_DEPLOY_BYTECODE, connected);
    const deployTx = await factory.getDeployTransaction();
    deployTx.gasLimit = 800_000n;

    const tx = await connected.sendTransaction(deployTx);
    const receipt = await this.waitForReceipt(tx.hash);

    if (receipt.status !== '0x1') {
      throw new Error(`Airdrop contract deployment reverted (tx: ${tx.hash})`);
    }

    const explorerUrl = `${this.networkConfig.explorerUrl}/contract/${receipt.contractAddress}`;

    // Best-effort source verification
    try {
      const verifyUrl = `${this.networkConfig.explorerUrl}/api/contracts/verify`;
      await fetch(verifyUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          address: receipt.contractAddress,
          sourceCode: AIRDROP_SOURCE_CODE,
          compilerVersion: 'v0.8.34+commit.1c8745a5',
          evmVersion: 'paris',
          optimizationRuns: 200,
        }),
      });
    } catch {
      // Explorer unavailable
    }

    return {
      contractAddress: receipt.contractAddress,
      txHash: tx.hash,
      explorerUrl,
    };
  }

  /**
   * Airdrop ERC-20 tokens to multiple recipients in a single transaction.
   * Requires: (1) a deployed Airdrop contract, (2) token approval for the airdrop contract.
   *
   * Steps handled automatically:
   * 1. Check allowance, approve airdrop contract if needed
   * 2. Call airdrop() or airdropFixed() on the contract
   *
   * @param airdropContract - deployed Airdrop contract address
   * @param tokenAddress - ERC-20 token to distribute
   * @param recipients - array of {to, amount} objects
   * @param signer - wallet holding the tokens
   */
  async airdrop(
    airdropContract: string,
    tokenAddress: string,
    recipients: BatchTransferItem[],
    signer: ethers.Wallet,
  ): Promise<AirdropResult> {
    const connected = signer.connect(this.provider);
    const token = new ethers.Contract(tokenAddress, ERC20_ABI, connected);
    const decimals = await token.decimals();

    // Parse amounts
    const addresses = recipients.map((r) => r.to);
    const amounts = recipients.map((r) => ethers.parseUnits(r.amount, decimals));
    const totalNeeded = amounts.reduce((sum, a) => sum + a, 0n);

    // Check and set allowance
    const currentAllowance = await token.allowance(connected.address, airdropContract);
    if (currentAllowance < totalNeeded) {
      const approveTx = await token.approve(airdropContract, ethers.MaxUint256);
      const approveReceipt = await this.waitForReceipt(approveTx.hash);
      if (approveReceipt.status !== '0x1') {
        throw new Error(`Approval transaction reverted (tx: ${approveTx.hash})`);
      }
    }

    // Check if all amounts are the same (use airdropFixed for gas savings)
    const allSame = amounts.every((a) => a === amounts[0]);

    const airdropCtx = new ethers.Contract(airdropContract, AIRDROP_ABI, connected);
    let tx: ethers.TransactionResponse;

    if (allSame && amounts.length > 0) {
      const txData = await airdropCtx.airdropFixed.populateTransaction(tokenAddress, addresses, amounts[0]);
      txData.gasLimit = BigInt(100_000 + recipients.length * 80_000);
      tx = await connected.sendTransaction(txData);
    } else {
      const txData = await airdropCtx.airdrop.populateTransaction(tokenAddress, addresses, amounts);
      txData.gasLimit = BigInt(100_000 + recipients.length * 80_000);
      tx = await connected.sendTransaction(txData);
    }

    const receipt = await this.waitForReceipt(tx.hash);
    if (receipt.status !== '0x1') {
      throw new Error(`Airdrop transaction reverted (tx: ${tx.hash})`);
    }

    return {
      airdropContract,
      tokenAddress,
      recipientCount: recipients.length,
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${tx.hash}`,
    };
  }

  /**
   * Batch transfer ERC-20 tokens to multiple addresses sequentially.
   * Useful for airdrops and multi-recipient distributions.
   * @param tokenAddress - ERC-20 token contract address
   * @param recipients - array of {to, amount} objects
   * @param signer - wallet to sign the transactions
   */
  async batchTransfer(
    tokenAddress: string,
    recipients: BatchTransferItem[],
    signer: ethers.Wallet,
  ): Promise<BatchTransferResult> {
    const connected = signer.connect(this.provider);
    const contract = new ethers.Contract(tokenAddress, ERC20_ABI, connected);
    const decimals = await contract.decimals();

    const result: BatchTransferResult = { successful: [], failed: [] };

    for (const recipient of recipients) {
      try {
        const parsedAmount = ethers.parseUnits(recipient.amount, decimals);
        const tx = await contract.transfer(recipient.to, parsedAmount);
        const receipt = await this.waitForReceipt(tx.hash);
        if (receipt.status !== '0x1') {
          result.failed.push({ to: recipient.to, amount: recipient.amount, error: 'Transaction reverted' });
        } else {
          result.successful.push({ to: recipient.to, amount: recipient.amount, txHash: tx.hash });
        }
      } catch (err: unknown) {
        const message = err instanceof Error ? err.message : String(err);
        result.failed.push({ to: recipient.to, amount: recipient.amount, error: message });
      }
    }

    return result;
  }
}
