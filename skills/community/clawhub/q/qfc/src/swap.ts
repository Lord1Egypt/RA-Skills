import { ethers } from 'ethers';
import { NetworkName, createProvider, getNetworkConfig } from './provider.js';

const ERC20_ABI = [
  'function approve(address spender, uint256 amount) returns (bool)',
  'function allowance(address owner, address spender) view returns (uint256)',
  'function symbol() view returns (string)',
  'function decimals() view returns (uint8)',
];

const SWAP_ABI = [
  'constructor(address tokenA, address tokenB)',
  'function tokenA() view returns (address)',
  'function tokenB() view returns (address)',
  'function reserveA() view returns (uint256)',
  'function reserveB() view returns (uint256)',
  'function totalSupply() view returns (uint256)',
  'function balanceOf(address) view returns (uint256)',
  'function getReserves() view returns (uint256, uint256)',
  'function getAmountOut(address tokenIn, uint256 amountIn) view returns (uint256)',
  'function addLiquidity(uint256 amountA, uint256 amountB) returns (uint256 lpMinted)',
  'function removeLiquidity(uint256 lpAmount) returns (uint256 amountA, uint256 amountB)',
  'function swap(address tokenIn, uint256 amountIn, uint256 minOut) returns (uint256 amountOut)',
  'event LiquidityAdded(address indexed provider, uint256 amountA, uint256 amountB, uint256 lpMinted)',
  'event LiquidityRemoved(address indexed provider, uint256 amountA, uint256 amountB, uint256 lpBurned)',
  'event Swap(address indexed user, address tokenIn, uint256 amountIn, address tokenOut, uint256 amountOut)',
];

const WQFC_ABI = [
  'function deposit() payable',
  'function withdraw(uint256 amount)',
  'function balanceOf(address) view returns (uint256)',
  'function approve(address spender, uint256 amount) returns (bool)',
  'function allowance(address owner, address spender) view returns (uint256)',
  'function totalSupply() view returns (uint256)',
  'function transfer(address to, uint256 amount) returns (bool)',
  'function transferFrom(address from, address to, uint256 amount) returns (bool)',
  'function name() view returns (string)',
  'function symbol() view returns (string)',
  'function decimals() view returns (uint8)',
];

/**
 * Pre-compiled WQFC (Wrapped QFC) bytecode (Solidity 0.8.34, evmVersion: paris, optimizer: 200 runs).
 * No constructor args.
 */
const WQFC_DEPLOY_BYTECODE = '0x60c0604052600b60809081526a577261707065642051464360a81b60a05260009061002a9082610112565b506040805180820190915260048152635751464360e01b60208201526001906100539082610112565b5034801561006057600080fd5b506101d4565b634e487b7160e01b600052604160045260246000fd5b600181811c9082168061009057607f821691505b6020821081036100b057634e487b7160e01b600052602260045260246000fd5b50919050565b601f82111561010d578282111561010d57806000526020600020601f840160051c60208510156100e4575060005b90810190601f840160051c0360005b81811015610109576000838201556001016100f3565b5050505b505050565b81516001600160401b0381111561012b5761012b610066565b61013f81610139845461007c565b846100b6565b6020601f821160018114610173576000831561015b5750848201515b600019600385901b1c1916600184901b1784556101cd565b600084815260208120601f198516915b828110156101a35787850151825560209485019460019092019101610183565b50848210156101c15786840151600019600387901b60f8161c191681555b505060018360011b0184555b5050505050565b6109c3806101e36000396000f3fe6080604052600436106100a05760003560e01c8063313ce56711610064578063313ce5671461017357806370a082311461019a57806395d89b41146101c7578063a9059cbb146101dc578063d0e30db0146101fc578063dd62ed3e1461020457600080fd5b806306fdde03146100b4578063095ea7b3146100df57806318160ddd1461010f57806323b872dd146101335780632e1a7d4d1461015357600080fd5b366100af576100ad61023c565b005b600080fd5b3480156100c057600080fd5b506100c961031a565b6040516100d69190610792565b60405180910390f35b3480156100eb57600080fd5b506100ff6100fa3660046107fc565b6103a8565b60405190151581526020016100d6565b34801561011b57600080fd5b5061012560045481565b6040519081526020016100d6565b34801561013f57600080fd5b506100ff61014e366004610826565b610415565b34801561015f57600080fd5b506100ad61016e366004610863565b610585565b34801561017f57600080fd5b50610188601281565b60405160ff90911681526020016100d6565b3480156101a657600080fd5b506101256101b536600461087c565b60026020526000908152604090205481565b3480156101d357600080fd5b506100c96106da565b3480156101e857600080fd5b506100ff6101f73660046107fc565b6106e7565b6100ad61023c565b34801561021057600080fd5b5061012561021f36600461089e565b600360209081526000928352604080842090915290825290205481565b600034116102805760405162461bcd60e51b815260206004820152600c60248201526b1e995c9bc819195c1bdcda5d60a21b60448201526064015b60405180910390fd5b336000908152600260205260408120805434929061029f9084906108e7565b9250508190555034600460008282546102b891906108e7565b909155505060405134815233907fe1fffcc4923d04b559f4d29a8bfc6cda04eb5b0d3c460751c2402c5c5cc9109c9060200160405180910390a2604051348152339060009060008051602061096e8339815191529060200160405180910390a3565b60008054610327906108fa565b80601f0160208091040260200160405190810160405280929190818152602001828054610353906108fa565b80156103a05780601f10610375576101008083540402835291602001916103a0565b820191906000526020600020905b81548152906001019060200180831161038357829003601f168201915b505050505081565b3360008181526003602090815260408083206001600160a01b038716808552925280832085905551919290917f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925906104039086815260200190565b60405180910390a35060015b92915050565b6001600160a01b03831660009081526003602090815260408083203384529091528120548211156104745760405162461bcd60e51b8152602060048201526009602482015268616c6c6f77616e636560b81b6044820152606401610277565b6001600160a01b0384166000908152600260205260409020548211156104ac5760405162461bcd60e51b815260040161027790610934565b6001600160a01b0384166000908152600360209081526040808320338452909152812080548492906104df90849061095a565b90915550506001600160a01b0384166000908152600260205260408120805484929061050c90849061095a565b90915550506001600160a01b038316600090815260026020526040812080548492906105399084906108e7565b92505081905550826001600160a01b0316846001600160a01b031660008051602061096e8339815191528460405161057391815260200190565b60405180910390a35060019392505050565b336000908152600260205260409020548111156105b45760405162461bcd60e51b815260040161027790610934565b33600090815260026020526040812080548392906105d390849061095a565b9250508190555080600460008282546105ec919061095a565b9091555050604051600090339083908381818185875af1925050503d8060008114610633576040519150601f19603f3d011682016040523d82523d6000602084013e610638565b606091505b505090508061067b5760405162461bcd60e51b815260206004820152600f60248201526e1d1c985b9cd9995c8819985a5b1959608a1b6044820152606401610277565b60405182815233907f7fcf532c15f0a6db0bd6d0e038bea71d30d808c7d98cb3bf7268a95bf5081b659060200160405180910390a2604051828152600090339060008051602061096e8339815191529060200160405180910390a35050565b60018054610327906108fa565b336000908152600260205260408120548211156107165760405162461bcd60e51b815260040161027790610934565b336000908152600260205260408120805484929061073590849061095a565b90915550506001600160a01b038316600090815260026020526040812080548492906107629084906108e7565b90915550506040518281526001600160a01b03841690339060008051602061096e83398151915290602001610403565b602081526000825180602084015260005b818110156107c057602081860181015160408684010152016107a3565b506000604082850101526040601f19601f83011684010191505092915050565b80356001600160a01b03811681146107f757600080fd5b919050565b6000806040838503121561080f57600080fd5b610818836107e0565b946020939093013593505050565b60008060006060848603121561083b57600080fd5b610844846107e0565b9250610852602085016107e0565b929592945050506040919091013590565b60006020828403121561087557600080fd5b5035919050565b60006020828403121561088e57600080fd5b610897826107e0565b9392505050565b600080604083850312156108b157600080fd5b6108ba836107e0565b91506108c8602084016107e0565b90509250929050565b634e487b7160e01b600052601160045260246000fd5b8082018082111561040f5761040f6108d1565b600181811c9082168061090e57607f821691505b60208210810361092e57634e487b7160e01b600052602260045260246000fd5b50919050565b6020808252600c908201526b1a5b9cdd59999a58da595b9d60a21b604082015260600190565b8181038181111561040f5761040f6108d156feddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3efa2646970667358221220a4c6f56d1d54e8da68fb3018de24281f1fc7aa2bb2cde4b696a1c4eb63bac81364736f6c63430008220033';

/**
 * Solidity source code for the WQFC contract.
 */
export const WQFC_SOURCE_CODE = `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract WQFC {
    string public name = "Wrapped QFC";
    string public symbol = "WQFC";
    uint8 public constant decimals = 18;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    uint256 public totalSupply;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Deposit(address indexed account, uint256 amount);
    event Withdrawal(address indexed account, uint256 amount);

    receive() external payable { deposit(); }

    function deposit() public payable {
        require(msg.value > 0, "zero deposit");
        balanceOf[msg.sender] += msg.value;
        totalSupply += msg.value;
        emit Deposit(msg.sender, msg.value);
        emit Transfer(address(0), msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external {
        require(balanceOf[msg.sender] >= amount, "insufficient");
        balanceOf[msg.sender] -= amount;
        totalSupply -= amount;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "transfer failed");
        emit Withdrawal(msg.sender, amount);
        emit Transfer(msg.sender, address(0), amount);
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
 * Pre-compiled SimpleSwap AMM bytecode (Solidity 0.8.34, evmVersion: paris, optimizer: 200 runs).
 * Constructor: (address tokenA, address tokenB)
 */
const SWAP_DEPLOY_BYTECODE = '0x608060405234801561001057600080fd5b5060405161100038038061100083398101604081905261002f91610130565b806001600160a01b0316826001600160a01b0316036100885760405162461bcd60e51b815260206004820152601060248201526f6964656e746963616c20746f6b656e7360801b60448201526064015b60405180910390fd5b6001600160a01b038216158015906100a857506001600160a01b03811615155b6100e35760405162461bcd60e51b815260206004820152600c60248201526b7a65726f206164647265737360a01b604482015260640161007f565b600080546001600160a01b039384166001600160a01b03199182161790915560018054929093169116179055610163565b80516001600160a01b038116811461012b57600080fd5b919050565b6000806040838503121561014357600080fd5b61014c83610114565b915061015a60208401610114565b90509250929050565b610e8e806101726000396000f3fe608060405234801561001057600080fd5b50600436106100a95760003560e01c806370a082311161007157806370a082311461012d5780639c8f9f231461014d5780639cd441da146101605780639f1d0f5914610173578063ca706bcf14610186578063dc5fa6c51461019957600080fd5b80630902f1ac146100ae5780630fc63d10146100cf57806318160ddd146100fa57806319e36f3b146101115780635f64b55b1461011a575b600080fd5b6002546003545b604080519283526020830191909152015b60405180910390f35b6000546100e2906001600160a01b031681565b6040516001600160a01b0390911681526020016100c6565b61010360045481565b6040519081526020016100c6565b61010360035481565b6001546100e2906001600160a01b031681565b61010361013b366004610d07565b60056020526000908152604090205481565b6100b561015b366004610d29565b6101a2565b61010361016e366004610d42565b610462565b610103610181366004610d64565b61079c565b610103610194366004610d97565b610b85565b61010360025481565b6000806000831180156101c45750336000908152600560205260409020548311155b6102075760405162461bcd60e51b815260206004820152600f60248201526e0696e73756666696369656e74204c5608c1b60448201526064015b60405180910390fd5b6004546002546102179085610dd7565b6102219190610dee565b9150600454600354846102349190610dd7565b61023e9190610dee565b33600090815260056020526040812080549293508592909190610262908490610e10565b92505081905550826004600082825461027b9190610e10565b9250508190555081600260008282546102949190610e10565b9250508190555080600360008282546102ad9190610e10565b909155505060005460405163a9059cbb60e01b8152336004820152602481018490526001600160a01b039091169063a9059cbb906044016020604051808303816000875af1158015610303573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906103279190610e23565b6103665760405162461bcd60e51b815260206004820152601060248201526f1d1c985b9cd9995c904819985a5b195960821b60448201526064016101fe565b60015460405163a9059cbb60e01b8152336004820152602481018390526001600160a01b039091169063a9059cbb906044016020604051808303816000875af11580156103b7573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906103db9190610e23565b61041a5760405162461bcd60e51b815260206004820152601060248201526f1d1c985b9cd9995c908819985a5b195960821b60448201526064016101fe565b604080518381526020810183905290810184905233907f1dc8bb69df2b8e91fbdcbfcf93d951b3f0000f085a95fe3f7946d6161439245d9060600160405180910390a2915091565b600080831180156104735750600082115b6104ad5760405162461bcd60e51b815260206004820152600b60248201526a1e995c9bc8185b5bdd5b9d60aa1b60448201526064016101fe565b600454600003610520576104c96104c48385610dd7565b610c80565b90506000811161051b5760405162461bcd60e51b815260206004820152601e60248201527f696e73756666696369656e7420696e697469616c206c6971756964697479000060448201526064016101fe565b610572565b6000600254600454856105339190610dd7565b61053d9190610dee565b90506000600354600454856105529190610dd7565b61055c9190610dee565b905080821061056b578061056d565b815b925050505b6000546040516323b872dd60e01b8152336004820152306024820152604481018590526001600160a01b03909116906323b872dd906064016020604051808303816000875af11580156105c9573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906105ed9190610e23565b61062c5760405162461bcd60e51b815260206004820152601060248201526f1d1c985b9cd9995c904819985a5b195960821b60448201526064016101fe565b6001546040516323b872dd60e01b8152336004820152306024820152604481018490526001600160a01b03909116906323b872dd906064016020604051808303816000875af1158015610683573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906106a79190610e23565b6106e65760405162461bcd60e51b815260206004820152601060248201526f1d1c985b9cd9995c908819985a5b195960821b60448201526064016101fe565b82600260008282546106f89190610e45565b9250508190555081600360008282546107119190610e45565b92505081905550806004600082825461072a9190610e45565b9091555050336000908152600560205260408120805483929061074e908490610e45565b9091555050604080518481526020810184905290810182905233907f64b83944e79c3ce8d4c297411de637c3e102d064677aac0c163976ebdcd6f50e9060600160405180910390a292915050565b60008083116107da5760405162461bcd60e51b815260206004820152600a6024820152691e995c9bc81a5b9c1d5d60b21b60448201526064016101fe565b6000546001600160a01b038581169116148061080357506001546001600160a01b038581169116145b61083f5760405162461bcd60e51b815260206004820152600d60248201526c34b73b30b634b2103a37b5b2b760991b60448201526064016101fe565b600080546001600160a01b03868116911614908082610863576003546002546108 6a565b6002546003545b9092509050600061087d876103e5610dd7565b90508061088c846103e8610dd7565b6108969190610e45565b6108a08383610dd7565b6108aa9190610dee565b9450858510156108e75760405162461bcd60e51b8152602060048201526008602482015267736c69707061676560c01b60448201526064016101fe565b600085116109255760405162461bcd60e51b815260206004820152600b60248201526a1e995c9bc81bdd5d1c1d5d60aa1b60448201526064016101fe565b60008461093d576000546001600160a01b031661094a565b6001546001600160a01b03165b6040516323b872dd60e01b8152336004820152306024820152604481018a90529091506001600160a01b038a16906323b872dd906064016020604051808303816000875af11580156109a0573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906109c49190610e23565b610a055760405162461bcd60e51b81526020600482015260126024820152711d1c985b9cd9995c881a5b8819985a5b195960721b60448201526064016101fe565b60405163a9059cbb60e01b8152336004820152602481018790526001600160a01b0382169063a9059cbb906044016020604051808303816000875af1158015610a52573d6000803e3d6000fd5b505050506040513d601f19601f82011682018060405250810190610a769190610e23565b610ab85760405162461bcd60e51b81526020600482015260136024820152721d1c985b9cd9995c881bdd5d0819985a5b1959606a1b60448201526064016101fe565b8415610af4578760026000828254610ad09190610e45565b925050819055508560036000828254610ae99190610e10565b90915550610b259050565b8760036000828254610b069190610e45565b925050819055508560026000828254610b1f9190610e10565b90915550505b604080516001600160a01b038b81168252602082018b905283168183015260608101889052905133917f5380cf97d8f645d3c4896da60c053458dca03a3a31cec642ac80e1ddf0d8d02a919081900360800190a250505050509392505050565b600080546001600160a01b0384811691161480610baf57506001546001600160a01b038481169116145b610beb5760405162461bcd60e51b815260206004820152600d60248201526c34b73b30b634b2103a37b5b2b760991b60448201526064016101fe565b600080546001600160a01b03858116911614908082610c0f57600354600254610c16565b6002546003545b915091508160001480610c27575080155b15610c385760009350505050610c7a565b6000610c46866103e5610dd7565b905080610c55846103e8610dd7565b610c5f9190610e45565b610c698383610dd7565b610c739190610dee565b9450505050505b92915050565b60006003821115610ce15750806000610c9a600283610dee565b610ca5906001610e45565b90505b81811015610cdb57905080600281610cc08186610dee565b610cca9190610e45565b610cd49190610dee565b9050610ca8565b50919050565b8115610ceb575060015b919050565b80356001600160a01b0381168114610ceb57600080fd5b600060208284031215610d1957600080fd5b610d2282610cf0565b9392505050565b600060208284031215610d3b57600080fd5b5035919050565b60008060408385031215610d5557600080fd5b50508035926020909101359150565b600080600060608486031215610d7957600080fd5b610d8284610cf0565b95602085013595506040909401359392505050565b60008060408385031215610daa57600080fd5b610db383610cf0565b946020939093013593505050565b634e487b7160e01b600052601160045260246000fd5b8082028115828204841417610c7a57610c7a610dc1565b600082610e0b57634e487b7160e01b600052601260045260246000fd5b500490565b81810381811115610c7a57610c7a610dc1565b600060208284031215610e3557600080fd5b81518015158114610d2257600080fd5b80820180821115610c7a57610c7a610dc156fea26469706673582212201c98b1b7a87e4145c01a14c668b5d42ee06b0d55438ecc0dd9a95826251bbb1a64736f6c63430008220033';

/**
 * Solidity source code for the SimpleSwap AMM contract.
 */
export const SWAP_SOURCE_CODE = `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function transfer(address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

contract SimpleSwap {
    address public tokenA;
    address public tokenB;

    uint256 public reserveA;
    uint256 public reserveB;

    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    event LiquidityAdded(address indexed provider, uint256 amountA, uint256 amountB, uint256 lpMinted);
    event LiquidityRemoved(address indexed provider, uint256 amountA, uint256 amountB, uint256 lpBurned);
    event Swap(address indexed user, address tokenIn, uint256 amountIn, address tokenOut, uint256 amountOut);

    constructor(address _tokenA, address _tokenB) {
        require(_tokenA != _tokenB, "identical tokens");
        require(_tokenA != address(0) && _tokenB != address(0), "zero address");
        tokenA = _tokenA;
        tokenB = _tokenB;
    }

    function getReserves() external view returns (uint256, uint256) {
        return (reserveA, reserveB);
    }

    function addLiquidity(uint256 amountA, uint256 amountB) external returns (uint256 lpMinted) {
        require(amountA > 0 && amountB > 0, "zero amount");
        if (totalSupply == 0) {
            lpMinted = sqrt(amountA * amountB);
            require(lpMinted > 0, "insufficient initial liquidity");
        } else {
            uint256 lpA = (amountA * totalSupply) / reserveA;
            uint256 lpB = (amountB * totalSupply) / reserveB;
            lpMinted = lpA < lpB ? lpA : lpB;
        }
        require(IERC20(tokenA).transferFrom(msg.sender, address(this), amountA), "transferA failed");
        require(IERC20(tokenB).transferFrom(msg.sender, address(this), amountB), "transferB failed");
        reserveA += amountA;
        reserveB += amountB;
        totalSupply += lpMinted;
        balanceOf[msg.sender] += lpMinted;
        emit LiquidityAdded(msg.sender, amountA, amountB, lpMinted);
    }

    function removeLiquidity(uint256 lpAmount) external returns (uint256 amountA, uint256 amountB) {
        require(lpAmount > 0 && balanceOf[msg.sender] >= lpAmount, "insufficient LP");
        amountA = (lpAmount * reserveA) / totalSupply;
        amountB = (lpAmount * reserveB) / totalSupply;
        balanceOf[msg.sender] -= lpAmount;
        totalSupply -= lpAmount;
        reserveA -= amountA;
        reserveB -= amountB;
        require(IERC20(tokenA).transfer(msg.sender, amountA), "transferA failed");
        require(IERC20(tokenB).transfer(msg.sender, amountB), "transferB failed");
        emit LiquidityRemoved(msg.sender, amountA, amountB, lpAmount);
    }

    function swap(address tokenIn, uint256 amountIn, uint256 minOut) external returns (uint256 amountOut) {
        require(amountIn > 0, "zero input");
        require(tokenIn == tokenA || tokenIn == tokenB, "invalid token");
        bool isA = tokenIn == tokenA;
        (uint256 resIn, uint256 resOut) = isA ? (reserveA, reserveB) : (reserveB, reserveA);
        uint256 amountInWithFee = amountIn * 997;
        amountOut = (amountInWithFee * resOut) / (resIn * 1000 + amountInWithFee);
        require(amountOut >= minOut, "slippage");
        require(amountOut > 0, "zero output");
        address tokenOut = isA ? tokenB : tokenA;
        require(IERC20(tokenIn).transferFrom(msg.sender, address(this), amountIn), "transfer in failed");
        require(IERC20(tokenOut).transfer(msg.sender, amountOut), "transfer out failed");
        if (isA) { reserveA += amountIn; reserveB -= amountOut; }
        else { reserveB += amountIn; reserveA -= amountOut; }
        emit Swap(msg.sender, tokenIn, amountIn, tokenOut, amountOut);
    }

    function getAmountOut(address tokenIn, uint256 amountIn) external view returns (uint256) {
        require(tokenIn == tokenA || tokenIn == tokenB, "invalid token");
        bool isA = tokenIn == tokenA;
        (uint256 resIn, uint256 resOut) = isA ? (reserveA, reserveB) : (reserveB, reserveA);
        if (resIn == 0 || resOut == 0) return 0;
        uint256 amountInWithFee = amountIn * 997;
        return (amountInWithFee * resOut) / (resIn * 1000 + amountInWithFee);
    }

    function sqrt(uint256 y) internal pure returns (uint256 z) {
        if (y > 3) {
            z = y;
            uint256 x = y / 2 + 1;
            while (x < z) { z = x; x = (y / x + x) / 2; }
        } else if (y != 0) { z = 1; }
    }
}
`;

export interface WQFCDeployResult {
  wqfcAddress: string;
  txHash: string;
  explorerUrl: string;
}

export interface WrapResult {
  wqfcAddress: string;
  amount: string;
  txHash: string;
  explorerUrl: string;
}

export interface PoolDeployResult {
  poolAddress: string;
  tokenA: string;
  tokenB: string;
  txHash: string;
  explorerUrl: string;
}

export interface PoolInfo {
  poolAddress: string;
  tokenA: { address: string; symbol: string; decimals: number; reserve: string };
  tokenB: { address: string; symbol: string; decimals: number; reserve: string };
  totalSupply: string;
  price: { aPerB: string; bPerA: string };
}

export interface AddLiquidityResult {
  lpMinted: string;
  amountA: string;
  amountB: string;
  txHash: string;
  explorerUrl: string;
}

export interface RemoveLiquidityResult {
  lpBurned: string;
  amountA: string;
  amountB: string;
  txHash: string;
  explorerUrl: string;
}

export interface SwapResult {
  tokenIn: string;
  tokenOut: string;
  amountIn: string;
  amountOut: string;
  txHash: string;
  explorerUrl: string;
}

export interface SwapQuote {
  tokenIn: string;
  tokenOut: string;
  amountIn: string;
  amountOut: string;
  priceImpact: string;
  fee: string;
}

/**
 * QFCSwap — Simple AMM (constant-product x*y=k) for token pairs on QFC.
 */
export class QFCSwap {
  private provider: ethers.JsonRpcProvider;
  private networkConfig;

  constructor(network: NetworkName = 'testnet') {
    this.networkConfig = getNetworkConfig(network);
    this.provider = createProvider(network);
  }

  /** Poll for transaction receipt via raw RPC */
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

  /** Ensure a token has sufficient allowance for a spender, approve max if not */
  private async ensureAllowance(
    tokenAddress: string,
    spender: string,
    amount: bigint,
    signer: ethers.Wallet,
  ): Promise<void> {
    const token = new ethers.Contract(tokenAddress, ERC20_ABI, signer);
    const current = await token.allowance(signer.address, spender);
    if (current < amount) {
      const tx = await token.approve(spender, ethers.MaxUint256);
      const receipt = await this.waitForReceipt(tx.hash);
      if (receipt.status !== '0x1') {
        throw new Error(`Approval failed for ${tokenAddress} (tx: ${tx.hash})`);
      }
    }
  }

  /**
   * Deploy a new liquidity pool for a token pair.
   * @param tokenA - first token address
   * @param tokenB - second token address
   * @param signer - wallet to deploy from
   */
  async deployPool(
    tokenA: string,
    tokenB: string,
    signer: ethers.Wallet,
  ): Promise<PoolDeployResult> {
    const connected = signer.connect(this.provider);
    const factory = new ethers.ContractFactory(SWAP_ABI, SWAP_DEPLOY_BYTECODE, connected);
    const deployTx = await factory.getDeployTransaction(tokenA, tokenB);
    deployTx.gasLimit = 1_500_000n;

    const tx = await connected.sendTransaction(deployTx);
    const receipt = await this.waitForReceipt(tx.hash);

    if (receipt.status !== '0x1') {
      throw new Error(`Pool deployment reverted (tx: ${tx.hash})`);
    }

    const explorerUrl = `${this.networkConfig.explorerUrl}/contract/${receipt.contractAddress}`;

    // Best-effort source verification
    try {
      const constructorArgs = ethers.AbiCoder.defaultAbiCoder()
        .encode(['address', 'address'], [tokenA, tokenB])
        .slice(2);
      const verifyUrl = `${this.networkConfig.explorerUrl}/api/contracts/verify`;
      await fetch(verifyUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          address: receipt.contractAddress,
          sourceCode: SWAP_SOURCE_CODE,
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
      poolAddress: receipt.contractAddress,
      tokenA,
      tokenB,
      txHash: tx.hash,
      explorerUrl,
    };
  }

  /**
   * Get pool info including reserves, token details, and current price.
   */
  async getPoolInfo(poolAddress: string): Promise<PoolInfo> {
    const pool = new ethers.Contract(poolAddress, SWAP_ABI, this.provider);

    const [addrA, addrB, reserves, supply] = await Promise.all([
      pool.tokenA(),
      pool.tokenB(),
      pool.getReserves(),
      pool.totalSupply(),
    ]);

    const tokenAContract = new ethers.Contract(addrA, ERC20_ABI, this.provider);
    const tokenBContract = new ethers.Contract(addrB, ERC20_ABI, this.provider);

    const [symA, decA, symB, decB] = await Promise.all([
      tokenAContract.symbol(),
      tokenAContract.decimals(),
      tokenBContract.symbol(),
      tokenBContract.decimals(),
    ]);

    const resA = reserves[0];
    const resB = reserves[1];
    const fmtA = ethers.formatUnits(resA, decA);
    const fmtB = ethers.formatUnits(resB, decB);

    // Price: how many B per 1 A, and vice versa
    let aPerB = '0';
    let bPerA = '0';
    if (resA > 0n && resB > 0n) {
      // Adjust for decimal differences
      const adjA = Number(fmtA);
      const adjB = Number(fmtB);
      bPerA = (adjB / adjA).toFixed(6);
      aPerB = (adjA / adjB).toFixed(6);
    }

    return {
      poolAddress,
      tokenA: { address: addrA, symbol: symA, decimals: Number(decA), reserve: fmtA },
      tokenB: { address: addrB, symbol: symB, decimals: Number(decB), reserve: fmtB },
      totalSupply: supply.toString(),
      price: { aPerB, bPerA },
    };
  }

  /**
   * Add liquidity to a pool. Both tokens must be approved first (handled automatically).
   * @param poolAddress - deployed pool contract
   * @param amountA - amount of tokenA (human-readable, e.g. "1000")
   * @param amountB - amount of tokenB (human-readable)
   * @param signer - wallet providing liquidity
   */
  async addLiquidity(
    poolAddress: string,
    amountA: string,
    amountB: string,
    signer: ethers.Wallet,
  ): Promise<AddLiquidityResult> {
    const connected = signer.connect(this.provider);
    const pool = new ethers.Contract(poolAddress, SWAP_ABI, this.provider);

    const [addrA, addrB] = await Promise.all([pool.tokenA(), pool.tokenB()]);
    const tokenAContract = new ethers.Contract(addrA, ERC20_ABI, this.provider);
    const tokenBContract = new ethers.Contract(addrB, ERC20_ABI, this.provider);
    const [decA, decB] = await Promise.all([tokenAContract.decimals(), tokenBContract.decimals()]);

    const parsedA = ethers.parseUnits(amountA, decA);
    const parsedB = ethers.parseUnits(amountB, decB);

    // Approve both tokens
    await Promise.all([
      this.ensureAllowance(addrA, poolAddress, parsedA, connected),
      this.ensureAllowance(addrB, poolAddress, parsedB, connected),
    ]);

    const poolConnected = new ethers.Contract(poolAddress, SWAP_ABI, connected);
    const txData = await poolConnected.addLiquidity.populateTransaction(parsedA, parsedB);
    txData.gasLimit = 500_000n;
    const tx = await connected.sendTransaction(txData);
    const receipt = await this.waitForReceipt(tx.hash);

    if (receipt.status !== '0x1') {
      throw new Error(`addLiquidity reverted (tx: ${tx.hash})`);
    }

    // Read LP balance to determine minted amount
    const lpBalance = await pool.balanceOf(connected.address);

    return {
      lpMinted: lpBalance.toString(),
      amountA,
      amountB,
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${tx.hash}`,
    };
  }

  /**
   * Remove liquidity from a pool. Burns LP tokens and returns both tokens.
   * @param poolAddress - deployed pool contract
   * @param lpAmount - amount of LP tokens to burn (raw units)
   * @param signer - wallet that holds LP tokens
   */
  async removeLiquidity(
    poolAddress: string,
    lpAmount: string,
    signer: ethers.Wallet,
  ): Promise<RemoveLiquidityResult> {
    const connected = signer.connect(this.provider);
    const pool = new ethers.Contract(poolAddress, SWAP_ABI, connected);

    const txData = await pool.removeLiquidity.populateTransaction(BigInt(lpAmount));
    txData.gasLimit = 300_000n;
    const tx = await connected.sendTransaction(txData);
    const receipt = await this.waitForReceipt(tx.hash);

    if (receipt.status !== '0x1') {
      throw new Error(`removeLiquidity reverted (tx: ${tx.hash})`);
    }

    // Get token info for formatting
    const poolReader = new ethers.Contract(poolAddress, SWAP_ABI, this.provider);
    const [addrA, addrB] = await Promise.all([poolReader.tokenA(), poolReader.tokenB()]);
    const tokenAContract = new ethers.Contract(addrA, ERC20_ABI, this.provider);
    const tokenBContract = new ethers.Contract(addrB, ERC20_ABI, this.provider);
    const [decA, decB] = await Promise.all([tokenAContract.decimals(), tokenBContract.decimals()]);

    // Calculate amounts returned (proportional to LP share)
    const [resA, resB] = await poolReader.getReserves();

    return {
      lpBurned: lpAmount,
      amountA: ethers.formatUnits(resA, decA),
      amountB: ethers.formatUnits(resB, decB),
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${tx.hash}`,
    };
  }

  /**
   * Get a swap quote (expected output amount) without executing.
   * @param poolAddress - pool contract
   * @param tokenIn - address of input token
   * @param amountIn - human-readable input amount
   */
  async getQuote(
    poolAddress: string,
    tokenIn: string,
    amountIn: string,
  ): Promise<SwapQuote> {
    const pool = new ethers.Contract(poolAddress, SWAP_ABI, this.provider);
    const [addrA, addrB, reserves] = await Promise.all([
      pool.tokenA(),
      pool.tokenB(),
      pool.getReserves(),
    ]);

    const isA = tokenIn.toLowerCase() === addrA.toLowerCase();
    const tokenOut = isA ? addrB : addrA;

    const tokenInContract = new ethers.Contract(tokenIn, ERC20_ABI, this.provider);
    const tokenOutContract = new ethers.Contract(tokenOut, ERC20_ABI, this.provider);
    const [decIn, decOut] = await Promise.all([
      tokenInContract.decimals(),
      tokenOutContract.decimals(),
    ]);

    const parsedIn = ethers.parseUnits(amountIn, decIn);
    const rawOut = await pool.getAmountOut(tokenIn, parsedIn);
    const fmtOut = ethers.formatUnits(rawOut, decOut);

    // Price impact calculation
    const resIn = isA ? reserves[0] : reserves[1];
    const priceImpact = resIn > 0n ? ((Number(parsedIn) / Number(resIn)) * 100).toFixed(2) : '100.00';
    const feeAmount = ethers.formatUnits((parsedIn * 3n) / 1000n, decIn);

    return {
      tokenIn,
      tokenOut,
      amountIn,
      amountOut: fmtOut,
      priceImpact: `${priceImpact}%`,
      fee: `${feeAmount} (0.3%)`,
    };
  }

  /**
   * Execute a token swap.
   * @param poolAddress - pool contract
   * @param tokenIn - address of input token
   * @param amountIn - human-readable input amount
   * @param slippagePct - max slippage percentage (default 1%)
   * @param signer - wallet executing the swap
   */
  async swap(
    poolAddress: string,
    tokenIn: string,
    amountIn: string,
    signer: ethers.Wallet,
    slippagePct: number = 1,
  ): Promise<SwapResult> {
    const connected = signer.connect(this.provider);
    const pool = new ethers.Contract(poolAddress, SWAP_ABI, this.provider);

    const [addrA, addrB] = await Promise.all([pool.tokenA(), pool.tokenB()]);
    const tokenOut = tokenIn.toLowerCase() === addrA.toLowerCase() ? addrB : addrA;

    const tokenInContract = new ethers.Contract(tokenIn, ERC20_ABI, this.provider);
    const tokenOutContract = new ethers.Contract(tokenOut, ERC20_ABI, this.provider);
    const [decIn, decOut] = await Promise.all([
      tokenInContract.decimals(),
      tokenOutContract.decimals(),
    ]);

    const parsedIn = ethers.parseUnits(amountIn, decIn);

    // Get expected output and calculate minOut with slippage
    const expectedOut = await pool.getAmountOut(tokenIn, parsedIn);
    const minOut = (expectedOut * BigInt(Math.floor((100 - slippagePct) * 100))) / 10000n;

    // Approve input token
    await this.ensureAllowance(tokenIn, poolAddress, parsedIn, connected);

    const poolConnected = new ethers.Contract(poolAddress, SWAP_ABI, connected);
    const txData = await poolConnected.swap.populateTransaction(tokenIn, parsedIn, minOut);
    txData.gasLimit = 300_000n;
    const tx = await connected.sendTransaction(txData);
    const receipt = await this.waitForReceipt(tx.hash);

    if (receipt.status !== '0x1') {
      throw new Error(`Swap reverted (tx: ${tx.hash})`);
    }

    return {
      tokenIn,
      tokenOut,
      amountIn,
      amountOut: ethers.formatUnits(expectedOut, decOut),
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${tx.hash}`,
    };
  }

  /**
   * Deploy the canonical WQFC (Wrapped QFC) contract.
   */
  async deployWQFC(signer: ethers.Wallet): Promise<WQFCDeployResult> {
    const connected = signer.connect(this.provider);
    const factory = new ethers.ContractFactory(WQFC_ABI, WQFC_DEPLOY_BYTECODE, connected);
    const deployTx = await factory.getDeployTransaction();
    deployTx.gasLimit = 1_000_000n;

    const tx = await connected.sendTransaction(deployTx);
    const receipt = await this.waitForReceipt(tx.hash);

    if (receipt.status !== '0x1') {
      throw new Error(`WQFC deployment reverted (tx: ${tx.hash})`);
    }

    // Best-effort verification
    try {
      const verifyUrl = `${this.networkConfig.explorerUrl}/api/contracts/verify`;
      await fetch(verifyUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          address: receipt.contractAddress,
          sourceCode: WQFC_SOURCE_CODE,
          compilerVersion: 'v0.8.34+commit.1c8745a5',
          evmVersion: 'paris',
          optimizationRuns: 200,
        }),
      });
    } catch {
      // Explorer unavailable
    }

    return {
      wqfcAddress: receipt.contractAddress,
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/contract/${receipt.contractAddress}`,
    };
  }

  /**
   * Wrap native QFC into WQFC (ERC-20).
   * @param wqfcAddress - deployed WQFC contract address
   * @param amount - amount of QFC to wrap (human-readable, e.g. "10.5")
   * @param signer - wallet holding native QFC
   */
  async wrapQFC(wqfcAddress: string, amount: string, signer: ethers.Wallet): Promise<WrapResult> {
    const connected = signer.connect(this.provider);
    const wqfc = new ethers.Contract(wqfcAddress, WQFC_ABI, connected);
    const parsedAmount = ethers.parseEther(amount);

    const tx = await wqfc.deposit({ value: parsedAmount, gasLimit: 100_000n });
    const receipt = await this.waitForReceipt(tx.hash);
    if (receipt.status !== '0x1') throw new Error(`Wrap failed (tx: ${tx.hash})`);

    return {
      wqfcAddress,
      amount,
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${tx.hash}`,
    };
  }

  /**
   * Unwrap WQFC back to native QFC.
   * @param wqfcAddress - deployed WQFC contract address
   * @param amount - amount of WQFC to unwrap (human-readable)
   * @param signer - wallet holding WQFC
   */
  async unwrapQFC(wqfcAddress: string, amount: string, signer: ethers.Wallet): Promise<WrapResult> {
    const connected = signer.connect(this.provider);
    const wqfc = new ethers.Contract(wqfcAddress, WQFC_ABI, connected);
    const parsedAmount = ethers.parseEther(amount);

    const tx = await wqfc.withdraw(parsedAmount, { gasLimit: 100_000n });
    const receipt = await this.waitForReceipt(tx.hash);
    if (receipt.status !== '0x1') throw new Error(`Unwrap failed (tx: ${tx.hash})`);

    return {
      wqfcAddress,
      amount,
      txHash: tx.hash,
      explorerUrl: `${this.networkConfig.explorerUrl}/txs/${tx.hash}`,
    };
  }

  /**
   * Swap native QFC for a token via WQFC pool (auto-wrap + swap).
   * @param poolAddress - pool with WQFC as one of the tokens
   * @param wqfcAddress - WQFC contract address
   * @param amountQFC - amount of native QFC to swap (human-readable)
   * @param signer - wallet
   * @param slippagePct - max slippage (default 1%)
   */
  async swapQFCForToken(
    poolAddress: string,
    wqfcAddress: string,
    amountQFC: string,
    signer: ethers.Wallet,
    slippagePct: number = 1,
  ): Promise<SwapResult> {
    // Step 1: wrap QFC → WQFC
    await this.wrapQFC(wqfcAddress, amountQFC, signer);
    // Step 2: swap WQFC → token
    return this.swap(poolAddress, wqfcAddress, amountQFC, signer, slippagePct);
  }

  /**
   * Swap a token for native QFC via WQFC pool (swap + auto-unwrap).
   * @param poolAddress - pool with WQFC as one of the tokens
   * @param wqfcAddress - WQFC contract address
   * @param tokenIn - token to sell
   * @param amountIn - amount to sell (human-readable)
   * @param signer - wallet
   * @param slippagePct - max slippage (default 1%)
   */
  async swapTokenForQFC(
    poolAddress: string,
    wqfcAddress: string,
    tokenIn: string,
    amountIn: string,
    signer: ethers.Wallet,
    slippagePct: number = 1,
  ): Promise<SwapResult> {
    // Step 1: swap token → WQFC
    const result = await this.swap(poolAddress, tokenIn, amountIn, signer, slippagePct);
    // Step 2: unwrap all WQFC → QFC
    const connected = signer.connect(this.provider);
    const wqfc = new ethers.Contract(wqfcAddress, WQFC_ABI, connected);
    const balance = await wqfc.balanceOf(connected.address);
    if (balance > 0n) {
      await this.unwrapQFC(wqfcAddress, ethers.formatEther(balance), signer);
    }
    return result;
  }

  /**
   * Get LP token balance for an address in a pool.
   */
  async getLPBalance(poolAddress: string, owner: string): Promise<string> {
    const pool = new ethers.Contract(poolAddress, SWAP_ABI, this.provider);
    const balance = await pool.balanceOf(owner);
    return balance.toString();
  }
}
