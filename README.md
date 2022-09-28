# XRP Ledger (XRPL) Tutorials

Repo with examples illustrating the use of the XRPL Python SDK (https://github.com/XRPLF/xrpl-py).

Examples include:

- connecting to a network
- creating accounts
- sending transactions
- querying balances

The `rpl-py` library helps with all aspects of interacting with the XRP Ledger, including:

- Key and wallet management
- Serialization
- Transaction Signing
- Connecting to the XRP ledger i.e. a network client
- Methods for inspecting accounts e.g. querying balances

# Assumptions

Familiarity with the XRP ledger and tools

- Testnet explorer https://testnet.xrpl.org/

- Testnet transaction sender (faucet) https://xrpl.org/tx-sender.html

- Source and destination tags https://xrpl.org/become-an-xrp-ledger-gateway.html#source-and-destination-tags

- A Python 3 environment with xrpl-py installed (`pip3 install xrpl-py`)

# Steps (if cloning repo)

Clone repo

`$ git clone https://github.com/jajukajulz/xrpl-tutorial.git`

Change directory and install node dependencies

`$ cd xrpl-tutorial`

Run script twice to create 2 new accounts via (i.e. via SDK). Once complete, make a note of the 3 account mnemonics and save somewhere safe.

`$ python xrpl_1_create_wallet.py`

Fund the 1st account using XRPL transaction sender

`https://xrpl.org/tx-sender.html`

Run script to send funds from the 1st account to the 2nd account. Before running, make sure to update the seeds etc (lookout for REPLACEME placeholders).

`$ python xrpl_2_make_xrp_payment.py`

## References

- xrpl testnet faucet https://xrpl.org/xrp-testnet-faucet.html
- xrpl transaction sender https://xrpl.org/tx-sender.html
- xrpl testnet validators https://testnet.xrpl.org/network/validators
- xrpl testnet explorer https://testnet.xrpl.org/
- XRPL Python SDK https://github.com/XRPLF/xrpl-py
- Official xrpl-py docs https://xrpl-py.readthedocs.io/en/stable/index.html
