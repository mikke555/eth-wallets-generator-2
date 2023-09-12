from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip39WordsNum, Bip44, Bip44Changes, Bip44Coins
import csv

'''
BIP39 proposal provides an algorithm to represent a 128/256 bits master private key + a checksum with a 12/24 word list
BIP44 proposal provides a way to derive a tree of keys from a master key. A derivation path looks like the following:

m / purpose' / coin_type' / account' / change / address_index

ETH derivation path:
m / 44' / 60' / 0' / 0 / 0

m  - master key
44 - purpose: follow the BIP44 standard
60 - coin_type: ETH
0  - account 0, account 1, account 2, ...
0  - change: BIP44 path includes the change level even for non-UTXO blockchains. For ETH is set to 0 or skipped
0  - address 0, address 1, address 2, ...

MetaMask software wallets increase the address_index value: m/44'/60'/0'/0/i
While Ledger Live increases the account index by leaving the address index fixed at zero: m/44'/60'/i'/0/0
'''

WALLET_NUM = 2


def gen_wallets():
    wallets = []

    for _ in range(WALLET_NUM):
        # Generate mnemonic
        mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
        # Generate seed from mnemonic
        seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
        # Construct master key from seed
        master_key = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
        # Derive a key pair of the first address
        bip44_addr = master_key.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)

        pkey = bip44_addr.PrivateKey().Raw().ToHex()
        addr = bip44_addr.PublicKey().ToAddress()

        wallets.append({'Address': addr, 'PK': pkey, 'Mnemonic': mnemonic})

    return wallets


if __name__ == "__main__":
    with open('output.csv', mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Address', 'PK', 'Mnemonic'])
        writer.writeheader()  # Write the column headers
        writer.writerows(gen_wallets())  # Write the data rows
    print(f"{WALLET_NUM} wallets generated")
