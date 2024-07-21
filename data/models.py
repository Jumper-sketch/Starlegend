from eth_async.models import RawContract, DefaultABIs
from eth_async.utils.utils import read_json
from eth_async.classes import Singleton

from data.config import ABIS_DIR


class Contracts(Singleton):
    # Arbitrum
    ARBITRUM_WOOFI = RawContract(
        title="WooFi",
        address='0x9aed3a8896a85fe9a8cac52c9b402d092b629a30',
        abi=read_json(path=(ABIS_DIR, 'woofi.json'))
    )

    ARBITRUM_USDC = RawContract(
        title='USDC',
        address='0xaf88d065e77c8cC2239327C5EDb3A432268e5831',
        abi=DefaultABIs.Token
    )

    ARBITRUM_USDC_e = RawContract(
        title='USDC_e',
        address='0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8',
        abi=DefaultABIs.Token
    )

    ARBITRUM_ETH = RawContract(
        title='ETH',
        address='0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
        abi=DefaultABIs.Token
    )

    ARBITRUM_ARB = RawContract(
        title='ARB',
        address='0x912CE59144191C1204E64559FE8253a0e49E6548',
        abi=DefaultABIs.Token
    )

    ARBITRUM_WBTC = RawContract(
        title='WBTC',
        address='0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f',
        abi=DefaultABIs.Token
    )

    ARBITRUM_STARGATE = RawContract(
        title='arbitrum_stargate',
        address='0x53bf833a5d6c4dda888f69c22c88c9f356a41614',
        abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    POLYGON_STARGATE = RawContract(
        title='polygon_stargate',
        address='0x45A01E4e04F14f7A4a6702c74187c5F6222033cd',
        abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    POLYGON_USDC = RawContract(
        title='USDC',
        address='0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',
        abi=DefaultABIs.Token
    )

    AVALANCHE_STARGATE = RawContract(
        title='avalanchen_stargate',
        address='0x45A01E4e04F14f7A4a6702c74187c5F6222033cd',
        abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    AVALANCHE_USDC = RawContract(
        title='USDC',
        address='0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E',
        abi=DefaultABIs.Token
    )

    OPBNB_MINT_TICKETS = RawContract(
        title='MINT_TICKETS',
        address='0xbc106b9473f273492b039a375e9abdf9698ec71d',
        abi=read_json(path=(ABIS_DIR, 'opbnb.json'))
    )

    OPBNB_APPROVE_NFT_SUMMON = RawContract(
        title='approve_nft_summon',
        address='0xda6c7beb3337ab3cfd9dcd2ce2ba50aaf30cdbdd',
        abi=read_json(path=(ABIS_DIR, 'opbnb.json'))
    )

    OPBNB_APPROVE_NFT_ACTIVE = RawContract(
        title='approve_nft_active',
        address='0xCbbE443e580cb01B67114A53fE90df0d51C26581',
        abi=read_json(path=(ABIS_DIR, 'opbnb.json'))
    )

    OPBNB_TRANSFER_NFT = RawContract(
        title='transfer_nft',
        address='0xc0a235e994DE2852Fe3F5e9B25D446de2B11B607',
        abi=read_json(path=(ABIS_DIR, 'opbnb.json'))
    )
