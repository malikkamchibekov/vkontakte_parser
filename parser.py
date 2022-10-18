import requests
import datetime
from config import token
import time

# получение количества
def get_offset(group_id):
    """
    group_id - id группы
    """
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

def get_users(group_id, date):
    """
    :param group_id: id группы
    :param date: дата с которой нужно начать анализ группы
    :return: кол-во подписчиков
    """
    active_users = []
    users_with_hidden_visit_time = []
    inactive_users = []
    for offset in range(0, get_offset(group_id) + 1):
        params = {'access_token': token,
                  'v': 5.131,
                  'group_id': group_id,
                  'offset': offset * 1000,
                  'fields': 'last_seen'}
        users = requests.get('https://api.vk.com/method/groups.getMembers', params=params).json()['response']
        for user in users['items']:
            start_point_data = datetime.datetime.strptime(date, '%d.%m.%Y').timestamp()
            try:
                if user['last_seen']['time'] >= start_point_data:
                    active_users.append(user['id'])
                else:
                    inactive_users.append(user['id'])
            except:
                users_with_hidden_visit_time.append(user['id'])
    print(f'Количество пользователей со скрытой датой: {len(users_with_hidden_visit_time)}')
    print(f"Активных подписчиков:{len(active_users)} ({round(len(active_users) / (users['count']) * 100, 2)}%)")
    print(f'Не активные подписчики: {len(inactive_users)}\n')
    return active_users


def parser(group_name: str):
    date = input('Введите дату, с которой хотите отслеживать активность в формате: дд.мм.гггг: ')
    # from_data = '18.10.2022'
    all_active_users = []
    print(f'Анализируем с {date}\n')
    for group in group_name:
        print(f'Группа: {group}')
        try:
            users = get_users(group, date=date)
            all_active_users.extend(users)
            time.sleep(2)
        except Exception as ex:
            print(f'{group} - Oшибка: {ex}\n')
            continue


if __name__ == '__main__':
    group_name = ['g.g.bishkek']
    parser(group_name)
