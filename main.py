import random
import time

from web3 import Web3
from termcolor import cprint
import config

RPC = "https://arb1.arbitrum.io/rpc"
web3 = Web3(Web3.HTTPProvider(RPC))
gasLimit = 3000000
eth_amount_to_stake = round(random.uniform(0.0001, 0.0003), 6)


def eth_aave_stake(private_key, gasLimit):
    try:

        account = web3.eth.account.privateKeyToAccount(private_key)
        address_wallet = account.address

        contractToken = Web3.toChecksumAddress('0xB5Ee21786D28c5Ba61661550879475976B707099')
        ABI = config.ABI

        contract = web3.eth.contract(address=contractToken, abi=ABI)

        gasPrice = Web3.toWei(0.0000000001, 'ether')
        nonce = web3.eth.get_transaction_count(address_wallet)

        contract_txn = contract.functions.depositETH(
            '0x794a61358D6845594F94dc1DB02A252b5b4814aD',
            str(address_wallet),
            0
        ).buildTransaction({
            'from': address_wallet,
            'value': int(Web3.toWei(eth_amount_to_stake, 'ether')),
            'gas': gasLimit,
            'gasPrice': gasPrice,
            'nonce': nonce,
        })

        signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key=private_key)
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        cprint(f'\n>>> stake ETH | https://arbiscan.io/tx/{web3.toHex(tx_token)} ', 'green')
    except Exception as error:
        cprint(f'\n>>> stake ETH | {address_wallet} | {error}', 'red')


if __name__ == '__main__':
    with open('private_keys.txt', 'r') as key:
        keys_list = [row.strip() for row in key]

        for private_key in keys_list:
            cprint(f'\n=============== start : {private_key} ===============', 'white')

            eth_aave_stake(private_key, gasLimit)
            time.sleep(random.randint(10, 60))
