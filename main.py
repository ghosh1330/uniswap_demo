
from datetime import datetime, timezone
from web3 import Web3

RPC_URL = "https://ethereum-rpc.publicnode.com"
#information has been found using the uniswap website for this code, not all of this is mine.

web3 = Web3(Web3.HTTPProvider(RPC_URL))

if not web3.is_connected():
    raise ConnectionError("Unable to connect to Ethereum")

if web3.eth.chain_id != 1:
    raise ValueError("Expected Ethereum Mainnet")


POOL_ADDRESS = Web3.to_checksum_address(
    "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
)

POOL_ABI = [
    {
        "name": "liquidity",
        "type": "function",
        "stateMutability": "view",
        "inputs": [],
        "outputs": [{"type": "uint128"}]
    },
    {
        "name": "slot0",
        "type": "function",
        "stateMutability": "view",
        "inputs": [],
        "outputs": [
            {"type": "uint160"},
            {"type": "int24"},
            {"type": "uint16"},
            {"type": "uint16"},
            {"type": "uint16"},
            {"type": "uint8"},
            {"type": "bool"}
        ]
    },
    {
        "name": "fee",
        "type": "function",
        "stateMutability": "view",
        "inputs": [],
        "outputs": [{"type": "uint24"}]
    }
]

pool = web3.eth.contract(
    address=POOL_ADDRESS,
    abi=POOL_ABI
)

block_number = web3.eth.block_number
block = web3.eth.get_block(block_number)

if not web3.eth.get_code(
    POOL_ADDRESS, block_identifier=block_number
):
    raise ValueError("No contract found at this address")

liquidity = pool.functions.liquidity().call(
    block_identifier=block_number
)

slot0 = pool.functions.slot0().call(
    block_identifier=block_number
)

fee = pool.functions.fee().call(
    block_identifier=block_number
)

if fee != 500:
    raise ValueError("Unexpected pool fee tier")

sqrt_price_x96 = slot0[0]
tick = slot0[1]

print("UNISWAP V3 POOL DATA")
print("-----------------------------")
print("Network: Ethereum Mainnet")
print("Pool: USDC/WETH")
print("Pool Address:", POOL_ADDRESS)
print("Fee Tier:", fee / 10000, "%")
print("Active Liquidity (raw):", liquidity)
print("Current Tick:", tick)
print("Sqrt Price X96:", sqrt_price_x96)
print("Ethereum Block:", block_number)
print(
    "Block Timestamp (UTC):",
    datetime.fromtimestamp(
        block["timestamp"], timezone.utc
    ).isoformat()
)
