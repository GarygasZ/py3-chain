import csv
import logging
import time
from decimal import Decimal

from eth_account import Account
from web3 import Web3

from abiLib.Xen import claim_xen


class PayEthOrToken:
    def __init__(self):
        # 可以去infura申请免费节点 https://infura.io/
        self.web3 = Web3(Web3.HTTPProvider("endpoint"))
        self.wallet = "wallet"
        self.wallet_private_key = "pk"

    def transfer_eth(self, to, value):
        try:
            token_balance = self.web3.fromWei(self.web3.eth.get_balance(self.wallet), "ether")
            if Decimal(token_balance) < Decimal(value):
                return None, "Eth not enough"
            to = Web3.toChecksumAddress(to)
            nonce = self.web3.eth.get_transaction_count(self.wallet)
            tx = {"nonce": nonce,
                  "to": to,
                  "gas": 100000,
                  "gasPrice": self.web3.toWei("50", "gwei"),
                  "value": self.web3.toWei(value, "ether"),
                  "chainId": 1}
            signed_tx = self.web3.eth.account.sign_transaction(tx, self.wallet_private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            return self.web3.toHex(tx_hash), "send success"
        except Exception as e:
            logging.error(f"转账异常: {e}")
            logging.exception(e)
            return None, str(e)


def createNewETHWallet(num):
    wallets = []
    for i in range(0, num, 1):
        account = Account.create()

        privateKey = account._key_obj

        publicKey = privateKey.public_key

        address = publicKey.to_checksum_address()
        wallets.append([i, address, publicKey, privateKey])

    # 文件名随意弄拉
    with open("wallets_20221010.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        # 表头
        csv_writer.writerow(["id", "address", "publicKey", "privateKey"])
        csv_writer.writerows(wallets)

    # Press the green button in the gutter to run the script.


if __name__ == '__main__':
    # createNewETHWallet(100)
    wallets = []
    with open("wallets_20221010.csv", "r") as csv_file:
        f = csv.reader(csv_file)
        headers = next(f)
        for row in f:
            wallets.append(row)

    payer = PayEthOrToken()

    for i in range(2, 4):
        payer.transfer_eth(wallets[i][1], 0.015)
        time.sleep(1000)
        claim_xen(wallets[i][1], wallets[3])
