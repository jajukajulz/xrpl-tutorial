# Script to create a completely new and unique pair of keys to be used for xrpl Accounts
# xrpl testnet faucet https://xrpl.org/xrp-testnet-faucet.html
# xrpl transaction sender https://xrpl.org/tx-sender.html
# xrpl testnet validators https://testnet.xrpl.org/network/validators
# xrpl testnet explorer https://testnet.xrpl.org/


# usage python xrpl_1_create_wallet.py
# then write down or store the seed, public key and classic address

from xrpl.clients import JsonRpcClient
from xrpl.core import keypairs
from xrpl.wallet import Wallet, generate_faucet_wallet

XRPL_DEVNET_URL = "https://s.devnet.rippletest.net:51234"
XRPL_TESTNET_URL = "https://s.altnet.rippletest.net:51234"
XRPL_MAINNET_URL = "https://s2.ripple.com:51234"

# generate seed
seed = keypairs.generate_seed()
print("Here's the seed: %s" % seed)

# generate wallet from seed (i.e. a wallet is a set of keys and an address that's been). This is a mathematical
# operation and purely offchain
sequence_num = 0
wallet_from_seed = Wallet(seed, sequence_num)
print(wallet_from_seed)

# create a TESTNET network client
xrpl_testnet_client = JsonRpcClient(XRPL_TESTNET_URL)

# create wallet on the TESTNET and fund with enough XRP to meet the account reserve
# generate_faucet_wallet returns A Wallet on the testnet that contains some amount of XRP.
test_wallet = generate_faucet_wallet(xrpl_testnet_client, wallet_from_seed)
print(test_wallet)
print(
    "View account on https://testnet.xrpl.org/accounts/%s" % test_wallet.classic_address
)
