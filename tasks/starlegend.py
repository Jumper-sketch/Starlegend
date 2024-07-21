import asyncio
import json
from typing import Optional

import requests
from fake_useragent import UserAgent
from web3 import Web3

from data.models import Contracts
from eth_async.models import TxArgs, TokenAmount
from eth_async.utils.utils import generate_random_bytes32
from data.config import API_OPBNB
from tasks.base import Base


class StarLegend(Base):
    async def mint_tickets(self) -> str:
        failed_text = 'Mint failed'
        tx_params = {
            'to': Contracts.OPBNB_MINT_TICKETS.address,
            'data': '0x1249c58b',
            'from': self.client.account.address
        }

        try:
            tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
            receipt = await tx.wait_for_receipt(client=self.client, timeout=200)

            if receipt:
                return f'Successfully minted {tx.hash.hex()}'

        except Exception as e:
            return f'{failed_text}: {str(e)}'

        return f'{failed_text}!'

    async def approve_nft(self, mode: Optional[str] = 'summon',
                          nft_contract_address: Optional[str] = None) -> str:
        failed_text = 'Approve failed'
        nft_contract_address = Web3.to_checksum_address(nft_contract_address)
        if mode == 'summon':
            contract = await self.client.contracts.get(contract_address=Contracts.OPBNB_APPROVE_NFT_SUMMON)
            tx_args = TxArgs(
                to=contract.address,
                approved=True
            )

            tx_params = {
                'to': contract.address,
                'data': contract.encodeABI('setApprovalForAll', args=tx_args.tuple()),
                'from': self.client.account.address
            }

        elif mode == 'active':
            contract = await self.client.contracts.get(contract_address=Contracts.OPBNB_APPROVE_NFT_ACTIVE)
            tx_args = TxArgs(
                to=contract.address,
                approved=True
            )

            tx_params = {
                'to': nft_contract_address,
                'data': contract.encodeABI('setApprovalForAll', args=tx_args.tuple()),
                'from': self.client.account.address
            }
        else:
            return f'Something wrong please check it!'

        try:
            tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
            receipt = await tx.wait_for_receipt(client=self.client, timeout=200)

            if receipt:
                return f'Successfully approved {tx.hash.hex()}'

        except Exception as e:
            return f'{failed_text}: {str(e)}'

        return f'{failed_text}!'

    async def summon_nft(self, count: int = 10) -> str:
        failed_text = 'Summon NFT Failed!'
        contract = await self.client.contracts.get(contract_address=Contracts.OPBNB_MINT_TICKETS)

        random_bytes_value = [await generate_random_bytes32() for _ in range(10)]
        param5 = [Web3.to_bytes(hexstr=value) for value in random_bytes_value]
        value_tx = TokenAmount(0.0001).Wei * count

        tx_args = TxArgs(
            param1=1,
            param2=Contracts.OPBNB_MINT_TICKETS.address,
            param3=0,
            param4=count,
            param5=param5
        )

        tx_params = {
            'from': self.client.account.address,
            'to': Contracts.OPBNB_APPROVE_NFT_SUMMON.address,
            'data': contract.encodeABI('commit', args=tx_args.tuple()),
            "value": value_tx
        }

        try:
            tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
            receipt = await tx.wait_for_receipt(client=self.client, timeout=200)

            if receipt:
                return f'Successfully minted {tx.hash.hex()}'

        except Exception as e:
            return f'{failed_text}: {str(e)}'

        return f'{failed_text}!'

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

    async def process_approve_nft_contracts(self, mode: str = 'active') -> str:
        contracts = await self.get_nft_data_count()
        for contract in contracts:
            print(await self.approve_nft(mode=mode, nft_contract_address=contract))
            print('Sleeping 3 sec...')
            await asyncio.sleep(3)
        return 'All done'

    async def transfer_nft(self, nft_contract_address, token_id: int, chain_id: int = 7):
        nft_contract_address = Web3.to_checksum_address(nft_contract_address)
        failed_text = 'Transfer failed'
        contract = await self.client.contracts.get(contract_address=Contracts.OPBNB_TRANSFER_NFT)

        tx_args = TxArgs(
            _contract=nft_contract_address,
            _tokenId=token_id,
            _chainId=chain_id,
            _spender=contract.address,
            _extraData=b''
        )

        tx_params = {
            'from': self.client.account.address,
            'to': Contracts.OPBNB_APPROVE_NFT_ACTIVE.address,
            'data': contract.encodeABI('transferNFT', args=tx_args.tuple()),
            'value': TokenAmount(0.0008).Wei
        }

        try:
            tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
            receipt = await tx.wait_for_receipt(client=self.client, timeout=200)

            if receipt:
                return f'Successfully transferred NFT #{token_id} to {chain_id} tx: {tx.hash.hex()}'

        except Exception as e:
            return f'{failed_text}: {str(e)}'

        return f'{failed_text}!'

    async def transfer_nft_for_data(
            self,
            data,
            chain_id: Optional[int] = 7,  # Optimism
    ):
        for key, values in data.items():
            print(f'Contract NFT: {key}')
            for item in values:
                print(f'ID NFT: {item}')
                res = await self.transfer_nft(nft_contract_address=key,
                                              token_id=item,
                                              chain_id=chain_id)
                print(res)
                print(f'Sleeping 5 seconds...')
                await asyncio.sleep(5)
