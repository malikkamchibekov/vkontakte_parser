import requests
import time
from config import token


# получение количества
def get_users(group_id):
    params = {'access_token': token, 'group_id': group_id, 'v': 5.131}
    r = requests.get('https://api.vk.com/method/groups.getMembers', params=params)
    # print(r.json())
    count = r.json()['response']['count']
    print(f'Количество подписчиков: {count}')
    if count > 1000:
        return count // 1000
    else:
        count = 1
        return count


if __name__ == '__main__':
    get_users(1)
