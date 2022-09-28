# Script to make a payment of xrp from one account to another
# xrpl testnet faucet https://xrpl.org/xrp-testnet-faucet.html
# xrpl transaction sender https://xrpl.org/tx-sender.html
# xrpl testnet validators https://testnet.xrpl.org/network/validators
# xrpl testnet explorer https://testnet.xrpl.org/

# usage python xrpl_2_make_xrp_payment.py

import json

from xrpl.account import (
    does_account_exist,
    get_account_payment_transactions,
    get_account_transactions,
    get_balance,
    get_next_valid_seq_number,
)
from xrpl.clients import JsonRpcClient
from xrpl.ledger import get_latest_validated_ledger_sequence
from xrpl.models.requests.account_info import AccountInfo
from xrpl.models.transactions import Payment
from xrpl.transaction import (
    safe_sign_and_autofill_transaction,
    safe_sign_transaction,
    send_reliable_submission,
)
from xrpl.utils import drops_to_xrp, xrp_to_drops
from xrpl.wallet import Wallet, generate_faucet_wallet

XRPL_DEVNET_URL = "https://s.devnet.rippletest.net:51234"
XRPL_TESTNET_URL = "https://s.altnet.rippletest.net:51234"
XRPL_MAINNET_URL = "https://s2.ripple.com:51234"

# create a TESTNET network client
XRPL_TESTNET_CLIENT = JsonRpcClient(XRPL_TESTNET_URL)

# TODO replace these values before commit
XRPL_TESTNET_SEED_KEY_ACCOUNT1 = "REPLACE_ME"
XRPL_TESTNET_CLASSIC_ADDRESS_ACCOUNT1 = (
    "REPLACE_ME"  # i.e. account1_wallet.classic_address
)
XRPL_TESTNET_CLASSIC_ADDRESS_ACCOUNT2 = "REPLACE_ME"  # Any external xrpl address 

XRP_AMOUNT = "10000"  # Typically, this is specified as an integer in "drops" of XRP, where 1,000,000 drops equals 1 XRP.


def return_XRPL_wallet_from_seed(seed):
    """Function to return an XRP wallet from a seed i.e. secret"""
    sequence_num = 0
    wallet_from_seed = Wallet(seed, sequence_num)
    print(wallet_from_seed)
    return wallet_from_seed


# Query XRP ledger and create custody wallet -----------------------------------
current_validated_ledger = get_latest_validated_ledger_sequence(XRPL_TESTNET_CLIENT)
account1_wallet = return_XRPL_wallet_from_seed(XRPL_TESTNET_SEED_KEY_ACCOUNT1)
account1_wallet.sequence = get_next_valid_seq_number(
    account1_wallet.classic_address, XRPL_TESTNET_CLIENT
)

# Prepare payment -------------------------------------------------------------
# the xrpl-py library safe_sign_and_autofill_transaction automatically populates the fee, sequence and last_ledger_sequence fields when you create transactions.
my_tx_payment = Payment(
    account=account1_wallet.classic_address,
    amount=XRP_AMOUNT,  # The amount of XRP to send in drops
    destination=XRPL_TESTNET_CLASSIC_ADDRESS_ACCOUNT2,
    # destination_tag=12345,
    # sequence=account1_wallet.sequence,
    # fee="10",
)
print("Payment object:", my_tx_payment)

# Sign transaction -------------------------------------------------------------
# my_tx_payment_signed = safe_sign_transaction(my_tx_payment, account1_wallet) # requires sequence and fee to be supplied in Payment object
my_tx_payment_signed = safe_sign_and_autofill_transaction(
    my_tx_payment, account1_wallet, XRPL_TESTNET_CLIENT
)
max_ledger = my_tx_payment_signed.last_ledger_sequence
tx_payment_signed_id = my_tx_payment_signed.get_hash()

print("Signed transaction:", my_tx_payment_signed)
print("Transaction cost:", drops_to_xrp(my_tx_payment_signed.fee), "XRP")
print("Transaction expires after ledger:", max_ledger)
print("Identifying hash:", tx_payment_signed_id)

# Submit transaction -----------------------------------------------------------
# The xrpl.transaction.send_reliable_submission() method  handles this process all in one call. You can use this
# instead of submit_transaction() wherever it's appropriate for your code to stop and wait for a transaction's
# final result to be confirmed.
tx_response = send_reliable_submission(my_tx_payment_signed, XRPL_TESTNET_CLIENT)
# The xrpl.transaction.send_reliable_submission() method  handles this process all in one call. You can use this instead
# of submit_transaction() wherever it's appropriate for your code to stop and wait for a transaction's final result to be confirmed.

# try:
#     prelim_result = xrpl.transaction.submit_transaction(my_tx_payment_signed, XRPL_TESTNET_CLIENT)
# except xrpl.clients.XRPLRequestFailureException as e:
#     exit(f"Submit failed: {e}")
# print("Preliminary transaction result:", prelim_result)

# Query the XRP Ledger for results ----------------------------------------------

# Look up info about sender account
acct_info = AccountInfo(
    account=XRPL_TESTNET_CLASSIC_ADDRESS_ACCOUNT1,
    ledger_index="validated",
    strict=True,
)
response = XRPL_TESTNET_CLIENT.request(acct_info)
result = response.result
print("response.status: ", response.status)
print(json.dumps(response.result, indent=4, sort_keys=True))

# Look up info about receiver account
acct_info = AccountInfo(
    account=XRPL_TESTNET_CLASSIC_ADDRESS_ACCOUNT2,
    ledger_index="validated",
    strict=True,
)
response = XRPL_TESTNET_CLIENT.request(acct_info)
result = response.result
print("response.status: ", response.status)
print(json.dumps(response.result, indent=4, sort_keys=True))
