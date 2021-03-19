import time
import traceback

import requests
import ujson

API_KEY = 'APIKEY'  # TODO: Read from env variable

INVALID_IDS = [
    # TODO: Fill automatically from error responses
]


def fetch_info(ids):
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': API_KEY}
    result = requests.get(
        'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info',
        params={'id': ','.join(ids)},
        headers=headers
    )
    if result.status_code != 200:
        print(result.text)
    return result.json()


if __name__ == '__main__':
    page_size = 100
    with open('coins-full.json', 'a') as coins_full_file:
        coins_full_file.write('[')
        for i in range(100):
            try:
                results = fetch_info(
                    [y for y in [str(x + page_size * i) for x in range(page_size)] if y not in INVALID_IDS]
                )['data']
                for _, coin in results.items():
                    coins_full_file.write(ujson.dumps(coin) + ',\n')
            except Exception as e:
                print(f'Failed to fetch {i}: {e}')
                traceback.print_exc()

            time.sleep(2)  # We shouldn't exceed the per-minutes limit
        coins_full_file.write(']')
