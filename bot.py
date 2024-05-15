import asyncio
from telegram import Bot
from telegram.error import RetryAfter
from config import TOKEN, CHANNEL_ID, COINGECKO
import get_data

async def send_message(bot, chat_id):
    try:
        data = get_data.get_current_prices()
        finnal_data = ''
        finnal_data += f"🟠{data[0]['symbol'].upper()} "
        finnal_data += f"{data[0]['current_price']}$ | "
        finnal_data += f"📈{round(data[0]['price_change_percentage_24h'], 2)}%\n\n"
        finnal_data += f"🔵{data[1]['symbol'].upper()} "
        finnal_data += f"{data[1]['current_price']}$ | "
        finnal_data += f"📈{round(data[1]['price_change_percentage_24h'], 2)}%\n\n"
        finnal_data += get_data.domination()
        finnal_data += ("\n")
        finnal_data += get_data.get_gas()
        await bot.send_message(chat_id=chat_id, text=finnal_data)
        print("Сообщение 1 отправлено в канал.")

        finnal_data = ''
        for coin in data[2:]:
            finnal_data += f"🔹{coin['symbol'].upper()}"
            finnal_data += f" {coin['current_price']}$ | "
            finnal_data += f"{round(coin['price_change_percentage_24h'], 2)}%\n\n"
        await bot.send_message(chat_id=chat_id, text=finnal_data)
        print("Сообщение 2 отправлено в канал.")

    except RetryAfter as e:
        retry_after = e.retry_after
        print(f"Превышен лимит запросов. Повторная попытка через {retry_after} секунд.")
        await asyncio.sleep(retry_after)
    except Exception as e:
        print(f"Ошибка: {str(e)}")


async def main():
    bot = Bot(token=TOKEN)
    await send_message(bot, CHANNEL_ID)

if __name__ == '__main__':
    asyncio.run(main())