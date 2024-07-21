import asyncio

from data.config import PRIVATE_KEY
from eth_async.client import Client
from eth_async.models import Networks
from tasks.starlegend import StarLegend


async def main():
    client = Client(private_key=PRIVATE_KEY, network=Networks.opBNB)
    starlegend = StarLegend(client=client)

    print(await starlegend.mint_tickets())

    print(await starlegend.approve_nft())

    print(await starlegend.summon_nft())

    print(await starlegend.process_approve_nft_contracts())

    data = await starlegend.get_nft_data_count()

    print(await starlegend.transfer_nft_for_data(data))


if __name__ == '__main__':
    asyncio.run(main())
