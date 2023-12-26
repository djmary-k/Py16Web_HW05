import asyncio
import aiohttp
from datetime import datetime, timedelta

class HttpError(Exception):
    pass

async def get_exchange_rates(date):
    url = f"https://api.privatbank.ua/p24api/exchange_rates?date={date}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                raise HttpError(f"Error status: {response.status} for {url}")

async def main(days):
    try:
        today = datetime.now()
        for i in range(1, days + 1):
            date = (today - timedelta(days=i)).strftime("%d.%m.%Y")
            data = await get_exchange_rates(date)
            print(f"Date: {date}")
            for currency in data['exchangeRate']:
                if currency['currency'] in ['EUR', 'USD']:
                    print(f"{currency['currency']}: {currency['purchaseRateNB']} - {currency['saleRateNB']}")
            print("-" * 30)
    except HttpError as err:
        print(err)

if __name__ == '__main__':
    while True:
        num_of_days = int(input("Введіть кількість днів (від 1 до 10): "))
        if 1 <= num_of_days <= 10:
            asyncio.run(main(num_of_days))
            break
        else:
            print("Невірна кількість днів.")
            continue
