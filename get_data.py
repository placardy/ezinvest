import requests
from config import COINGECKO, ETHERSCAN

def get_crypto_data(cryptos):
    try:
        crypto_ids = ','.join(cryptos)
        response = requests.get(f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={crypto_ids}&api_key={COINGECKO}')
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong", err)


def get_current_prices():
    cryptos = ['bitcoin', 'ethereum', 'litecoin', 'starknet', 'rss3', 'arbitrum', 'aptos', 'apecoin', '1inch', 'filecoin', 'flow', 'blur']
    data = get_crypto_data(cryptos)
    return data


def domination():
    url = 'https://api.coingecko.com/api/v3/global'
    response = requests.get(url, headers={'X-CMC_PRO_API_KEY': COINGECKO})
    if response.status_code == 200:
        data = response.json()['data']
        bitcoin_dominance = data['market_cap_percentage']['btc']
        return f'⚖️BTC доминация - {round(bitcoin_dominance, 2)}%\n'
    else:
        print(f'Ошибка запроса: {response.status_code}')
domination()

def get_gas():
    finnal_data = ''
    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
    cg_data = cg_response.json()
    eth_price_usd = cg_data['ethereum']['usd']

    # Get gas prices from Etherscan
    etherscan_url = f'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={ETHERSCAN}'
    etherscan_response = requests.get(etherscan_url)
    etherscan_data = etherscan_response.json()

    # Example gas price and gas limit
    gas_price_gwei = etherscan_data['result']['ProposeGasPrice']
    gas_limit = 21000  # Example gas limit for a simple Ethereum transfer

    # Calculate gas fee in USD
    gas_fee_eth = (float(gas_price_gwei) * float(gas_limit)) / 1e9  # Convert from Gwei to Ether
    gas_fee_usd = gas_fee_eth * eth_price_usd
    # finnal_data += f'Ethereum price (USD): {eth_price_usd:.2f}\n'
    finnal_data += f'⚡️Gas price (Gwei) - {gas_price_gwei}\n'
    finnal_data += f'💵Gas fee (USD) - ~{round(gas_fee_usd, 2)}\n'
    return finnal_data
