# OpenZeppelin 5.x Reference

## Install

```bash
forge install OpenZeppelin/openzeppelin-contracts
# or
npm install @openzeppelin/contracts
```

## ERC-20

```solidity
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract MyToken is ERC20, Ownable {
    constructor(address initialOwner)
        ERC20("MyToken", "MTK")
        Ownable(initialOwner)
    {
        _mint(initialOwner, 1_000_000 * 10**decimals());
    }

    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }
}
```

## ERC-721 (NFT)

```solidity
import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {ERC721URIStorage} from "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract MyNFT is ERC721URIStorage, Ownable {
    uint256 private _nextTokenId;

    constructor(address owner) ERC721("MyNFT", "MNFT") Ownable(owner) {}

    function safeMint(address to, string memory uri) external onlyOwner returns (uint256) {
        uint256 tokenId = _nextTokenId++;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
        return tokenId;
    }
}
```

## Access Control (Roles)

```solidity
import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";

contract MyContract is AccessControl {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");

    constructor(address admin) {
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
        _grantRole(MINTER_ROLE, admin);
    }

    function mint(address to) external onlyRole(MINTER_ROLE) { ... }
}
```

## Upgradeable Contracts (UUPS)

```solidity
// Implementation contract
import {UUPSUpgradeable} from "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import {OwnableUpgradeable} from "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import {Initializable} from "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";

contract MyContractV1 is Initializable, OwnableUpgradeable, UUPSUpgradeable {
    uint256 public value;

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() { _disableInitializers(); }

    function initialize(address owner) public initializer {
        __Ownable_init(owner);
        __UUPSUpgradeable_init();
    }

    function _authorizeUpgrade(address) internal override onlyOwner {}
}

// Deploy with OZ upgrades plugin:
// const proxy = await upgrades.deployProxy(MyContractV1, [owner], { kind: 'uups' })
// const v2 = await upgrades.upgradeProxy(proxy.address, MyContractV2)
```

## ReentrancyGuard

```solidity
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract MyVault is ReentrancyGuard {
    function withdraw() external nonReentrant {
        // safe from reentrancy
    }
}
```

## Pausable

```solidity
import {Pausable} from "@openzeppelin/contracts/utils/Pausable.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract MyContract is Pausable, Ownable {
    function pause() external onlyOwner { _pause(); }
    function unpause() external onlyOwner { _unpause(); }
    function deposit() external whenNotPaused { ... }
}
```

## SafeERC20

```solidity
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract MyContract {
    using SafeERC20 for IERC20;
    // Use safeTransfer, safeTransferFrom, safeApprove
    // Handles non-standard tokens that don't return bool
    token.safeTransfer(recipient, amount);
    token.safeTransferFrom(sender, address(this), amount);
}
```
