from solcx import compile_standard, install_solc
from web3 import Web3
import os
from dotenv import load_dotenv
import random

# we use env to keep private variable separate from codebase becuase we don't want anyone to see them
# we can do so by using a .env file which will store our private environment variables
load_dotenv()

install_solc("0.8.12")

import json

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# compiling
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.12",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache blockchain
url1 = "https://rinkeby.infura.io/v3/f811459be85a4c05bbc5139f90550b42"
url2 = "HTTP://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(url1))
chain_id = 4  # rinkeby chainID
chain_address = "0x00a77A6C1073D5436EE23a30825E234eCec8213f"
chain_PrivKey = os.getenv("private_key")


# ////////////////////////////----------------------------////////////////////////////////////////////
# -----------------------------------------------
# First of all we need to build the contract and make sure we can send transactions to it
# -----------------------------------------------

# creating contract using python
print("Deploying contract.....")
SimpleStorage = web3.eth.contract(abi=abi, bytecode=bytecode)
# nonce is used to get the number of the latest transaction
# everytime we add a node(transaction) to the chain, a new nonce is assigned to it
# nonce are unique and hashed
nonce = web3.eth.getTransactionCount(chain_address)
print("Current number of Nodes: ", nonce)


# Building Trx
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": web3.eth.gas_price,
        "chainId": chain_id,
        "from": chain_address,
        "nonce": nonce,
    }
)

# Signing a Trx
signed_transaction = web3.eth.account.sign_transaction(transaction, chain_PrivKey)

# Sending a Trx
transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
transaction_reciept = web3.eth.wait_for_transaction_receipt(transaction_hash)
print("Contract deployed!")
# ////////////////////////////----------------------------////////////////////////////////////////////


# When working with a contract we need two things
# 1) Contract Address
# 2) Contract ABI

# ------------------------------------------------------
# After the transactions have been set up we build the contract again through its ABI and now we can call its funcs
# ------------------------------------------------------
simple_storage = web3.eth.contract(address=transaction_reciept.contractAddress, abi=abi)
# Call -> Just to see if functions work, doesn't store any value in the contract
# Transact -> This makes state changes to the contract, store values in vars
value = 35
print(simple_storage.functions.retrieve().call())
print("Making state change in contract.....")
store_balance_trx = simple_storage.functions.store(value).buildTransaction(
    {
        "gasPrice": web3.eth.gas_price,
        "chainId": chain_id,
        "from": chain_address,
        "nonce": nonce + 1,
    }
)
store_balance_trx_sign = web3.eth.account.sign_transaction(
    store_balance_trx, chain_PrivKey
)
store_balance_trx_hash = web3.eth.send_raw_transaction(
    store_balance_trx_sign.rawTransaction
)
transaction_reciept = web3.eth.wait_for_transaction_receipt(store_balance_trx_hash)
print(simple_storage.functions.retrieve().call())
print("Contract Updated!")
nonce += 1

print("Adding People with random balances and coins.....")
coins = ["BTC", "ETH", "SOL", "AVAX", "ONE", "LINK", "DOT"]

for i in range(len(coins)):
    rand_balance = random.randint(0, 50)
    rand_coin = coins[random.randint(0, len(coins) - 1)]
    rand_name = chr(ord("a") + random.randint(0, 10))

    store_person_trx = simple_storage.functions.addPerson(
        rand_name, rand_balance, rand_coin
    ).buildTransaction(
        {
            "gasPrice": web3.eth.gas_price,
            "chainId": chain_id,
            "from": chain_address,
            "nonce": nonce + 1,
        }
    )
    store_person_trx_sign = web3.eth.account.sign_transaction(
        store_person_trx, chain_PrivKey
    )
    store_person_trx_hash = web3.eth.send_raw_transaction(
        store_person_trx_sign.rawTransaction
    )
    transaction_reciept = web3.eth.wait_for_transaction_receipt(store_balance_trx_hash)
    nonce += 1

people = simple_storage.functions.getPerson().call()
for p in people:
    print("Name: ", p[2], " Coin: ", p[1], " Balance: ", p[0])


print("Contract Updated!!!")


# 4.30.16
