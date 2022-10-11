import logging
from web3 import Web3


def claim_xen(wallet, privateKey):
    xen_token_address = Web3.toChecksumAddress('0x06450dEe7FD2Fb8E39061434BAbCFC05599a6Fb8')
    try:
        web3 = Web3(Web3.HTTPProvider())
        data_input = {'chainId': 1,
                      'gas': 190000,
                      'nonce': web3.eth.getTransactionCount(web3.toChecksumAddress(wallet)),
                      'maxFeePerGas': web3.toWei(50, 'gwei'),
                      'maxPriorityFeePerGas': web3.toWei(1.5, 'gwei'),
                      'value': web3.toWei(0, 'ether'),
                      'data': '0x9ff054df0000000000000000000000000000000000000000000000000000000000000001',
                      'to': web3.toChecksumAddress(xen_token_address),
                      'from': wallet
                      }
        signed_txn = web3.eth.account.signTransaction(data_input, privateKey)

        txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        hash = web3.toHex(txn_hash)
        return hash, "成功claim"
    except Exception as e:
        logging.error(f"调用异常: {e}")
        logging.exception(e)
        return None, str(e)


if __name__ == '__main__':
    claim_xen('', '')
