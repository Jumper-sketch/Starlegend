import asyncio
import json
import requests
from fake_useragent import UserAgent
from data.config import PRIVATE_KEY
from eth_async.client import Client
from eth_async.models import Networks
from data.config import API_OPBNB


class StarLegend:
    def __init__(self, client):
        self.client = client

    async def get_nft_data_count(self) -> dict:
        wallet_address = self.client.account.address
        nft_dict = {}
        api = API_OPBNB
        url_rpc = f'https://opbnb-mainnet.nodereal.io/v1/{api}'

        # Fetching NFT Holdings
        payload_holdings = {
            "jsonrpc": "2.0",
            "method": "nr_getNFTHoldings",
            "params": [
                wallet_address,
                "erc721",  # type token-format
                "0x1",
                "0x14"
            ],
            "id": 1
        }

        headers = {
            'user-agent': UserAgent().random
        }

        response_holdings = requests.post(url_rpc, headers=headers, data=json.dumps(payload_holdings))
        response_holdings.raise_for_status()  # Raise an exception for HTTP errors

        if response_holdings.status_code == 200:
            response_data_holdings = response_holdings.json()

            if 'result' in response_data_holdings:
                result_holdings = response_data_holdings['result']
                total_count_hex = result_holdings.get('totalCount', '0x0')
                details = result_holdings.get('details', [])

                total_count_decimal = int(total_count_hex, 16)
                print(f'Total NFT count: {total_count_decimal}')

                if total_count_decimal > 0 and details:
                    for nft in details:
                        if isinstance(nft, dict):
                            contract_address = nft.get('tokenAddress', '')
                            if contract_address:
                                # Fetching NFT Inventory for each contract address
                                payload_inventory = {
                                    "jsonrpc": "2.0",
                                    "method": "nr_getNFTInventory",
                                    "params": [
                                        wallet_address,
                                        contract_address,
                                        "0x14",
                                        ""
                                    ],
                                    "id": 1
                                }

                                response_inventory = requests.post(url_rpc, headers=headers,
                                                                   data=json.dumps(payload_inventory))
                                response_inventory.raise_for_status()  # Raise an exception for HTTP errors

                                if response_inventory.status_code == 200:
                                    response_data_inventory = response_inventory.json()
                                    if 'result' in response_data_inventory:
                                        result_inventory = response_data_inventory['result']
                                        details_inventory = result_inventory.get('details', [])

                                        if details_inventory:
                                            for item in details_inventory:
                                                token_id = item.get('tokenId', '')
                                                if contract_address in nft_dict:
                                                    nft_dict[contract_address].append(int(token_id, 16))
                                                else:
                                                    nft_dict[contract_address] = [int(token_id, 16)]
                                        else:
                                            print(f"No inventory details found for contract: {contract_address}")
                                else:
                                    print(
                                        f"Error fetching inventory for contract {contract_address}: {response_inventory.status_code}")
                else:
                    print("No NFT holdings found.")
            else:
                print("No result field in holdings response.")
        else:
            print(f"Error fetching holdings: {response_holdings.status_code}")

        return nft_dict
