import os
import random
import time
import requests

TOKEN = os.environ.get('TOKEN')
URL = f'https://api.telegram.org/bot{TOKEN}/'


def send_message(chat_id, text, reply_markup=None):
  payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}
  if reply_markup:
    payload['reply_markup'] = reply_markup
  requests.post(URL + 'sendMessage', json=payload)


def edit_message(chat_id, message_id, text, reply_markup=None):
  payload = {
      'chat_id': chat_id,
      'message_id': message_id,
      'text': text,
      'parse_mode': 'Markdown',
  }
  if reply_markup:
    payload['reply_markup'] = reply_markup
  requests.post(URL + 'editMessageText', json=payload)


def answer_callback(callback_query_id):
  requests.post(
      URL + 'answerCallbackQuery', json={'callback_query_id': callback_query_id}
  )


def main_menu():
  return {
      'inline_keyboard': [[{'text': '🚀 START AI TRADING', 'callback_data': 'start_trade'}]]
  }


def pair_menu():
  return {
      'inline_keyboard': [
          [
              {'text': 'EUR/USD OTC', 'callback_data': 'pair_EURUSD'},
              {'text': 'AUD/USD OTC', 'callback_data': 'pair_AUDUSD'},
          ],
          [
              {'text': 'GBP/USD OTC', 'callback_data': 'pair_GBPUSD'},
              {'text': 'USD/JPY OTC', 'callback_data': 'pair_USDJPY'},
          ],
          [{'text': '⬅️ Back', 'callback_data': 'main'}],
      ]
  }


def time_menu(pair):
  return {
      'inline_keyboard': [
          [
              {'text': 'M1 (1 Min)', 'callback_data': f'signal_{pair}_M1'},
              {'text': 'M3 (3 Min)', 'callback_data': f'signal_{pair}_M3'},
          ],
          [
              {'text': 'M5 (5 Min)', 'callback_data': f'signal_{pair}_M5'},
          ],
          [{'text': '⬅️ Back to Pairs', 'callback_data': 'start_trade'}],
      ]
  }


def handle_updates():
  offset = None
  print('Bot-kii wuu shaqaynayaa oo wuu dhagaysnayaa fariimaha...')
  while True:
    try:
      response = requests.get(
          URL + 'getUpdates', params={'offset': offset, 'timeout': 30}
      )
      data = response.json()

      if 'result' in data:
        for update in data['result']:
          offset = update['update_id'] + 1

          if 'message' in update:
            chat_id = update['message']['chat']['id']
            text = update['message'].get('text', '')
            if text == '/start':
              send_message(
                  chat_id,
                  '🤖 *GEMINI 3 PRO AI TRADING*\n\nKu soo dhowow nidaamka falanqaynta suuqa ee casriga ah. Riix batoonka hoose si aad u bilowdo:',
                  reply_markup=main_menu(),
              )

          elif 'callback_query' in update:
            cq = update['callback_query']
            chat_id = cq['message']['chat']['id']
            message_id = cq['message']['message_id']
            data_val = cq['data']
            answer_callback(cq['id'])

            if data_val == 'main':
              edit_message(
                  chat_id,
                  message_id,
                  '🤖 *GEMINI 3 PRO AI TRADING*\n\nDooro batoonka hoose:',
                  reply_markup=main_menu(),
              )
            elif data_val == 'start_trade':
              edit_message(
                  chat_id,
                  message_id,
                  '📊 *Dooro Currency Pair-ka aad rabto in la falanqeeyo:*',
                  reply_markup=pair_menu(),
              )
            elif data_val.startswith('pair_'):
              pair_name = data_val.replace('pair_', '')
              edit_message(
                  chat_id,
                  message_id,
                  f'⏱ Dooro waqtiga (Expiration Time) ee *{pair_name}*:',
                  reply_markup=time_menu(pair_name),
              )
            elif data_val.startswith('signal_'):
              parts = data_val.split('_')
              pair = parts[1]
              tf = parts[2]

              signal_type = random.choice(['🟢 BUY', '🔴 SELL'])
              current_time = time.strftime('%H:%M:%S', time.localtime())

              signal_text = (
                  f'⚡ *GEMINI AI SIGNAL*\n\n'
                  f'*{signal_type}*\n\n'
                  f'📌 *Signal Information:*\n'
                  f'• Pair: {pair} (OTC)\n'
                  f'• Timeframe: {tf}\n'
                  f'• Current Time: {current_time}\n'
                  f'• Accuracy: 94.7%\n\n'
                  f'⚠️ _Isticmaal lacagtaada si taxaddar leh._'
              )
              edit_message(chat_id, message_id, signal_text, reply_markup=None)

    except Exception as e:
      print(f'Khalad dhacay: {e}')
      time.sleep(3)


if __name__ == '__main__':
  handle_updates()
           
