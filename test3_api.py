import requests
import json
import os

from datetime import date

from requests.exceptions import HTTPError

from config import Config


def app(config, process_date=None):

    if not process_date:
        process_date = str(date.today())

    os.makedirs(os.path.join(config['directory'], process_date), exist_ok=True)

    try:
        for product in config['product_id']:
            config = Config('config.yaml')
            config = config.get_config()
            url_post = {'url_post': config['url_post']}
            login = {'username': config['username'],
                     'password': config['password']}
            headers = {"content-type": "application/json"}
            r = requests.post(url_post, headers=headers, login=json.dumps(login))
            token = r.json()['access_token']
            print(token)

            url_get = {'url_get': config['url_get']}
            data = json.dumps({"date": date})
            headers = {"content-type": "application/json", "Authorization": "JWT " + token}
            response = requests.get(url_get, data=data, headers=headers)
            response.raise_for_status()

            with open(os.path.join(config['directory'], process_date, cproduct+'.json'), 'w') as json_file:
                data = response.json()
                data = data['rates']
                json.dump(data, json_file)

    except HTTPError:
        print('Error!')


if __name__ == '__main__':
    config = Config(os.path.join('.', 'config.yaml'))
    date = ['2021-01-02']
    for dt in date:
        app(
        config=config.get_config('API_app')
        , process_date=dt
            )