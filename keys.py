import os
import httpx

class Keys:
    def __init__(self):
        self.gpt_token = os.environ.get('GPT_TOKEN')
        self.bot_token = os.environ.get('BOT_TOKEN')
        self.giga_uid = os.environ.get('GIGA_UID')
        self.giga_token = os.environ.get('GIGA_TOKEN')
        self.giga_oauth = self.get_giga_oauth(self.giga_token, self.giga_uid)

    # Get Giga OAuth
    def get_giga_oauth(self, token, uid):

        url = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'

        payload = {
            'scope': 'GIGACHAT_API_PERS'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': uid,
            'Authorization': f'Basic {token}'
        }

        response = httpx.post(url, data=payload, headers=headers, verify=False)
        return response.json()['access_token']

#a = Keys()
#print(a.giga_oauth)
#print(a.bot_token)
#print(a.gpt_token)