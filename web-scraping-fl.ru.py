# 0
# Для начала импортируем пакеты, в их числе пакет - datetime, необходимый для автоматического определения текущего времени;
# Пакет time необходим для приостановки исполнения скрипта. Это вторая мера маскировки автоматизированного запроса к сайту;
# Пакет traceback детализирует ошибки.
import datetime, pandas, re, requests, time, traceback
from bs4 import BeautifulSoup

# Для маскировки алгоритмического запроса под запрос обычного пользователя каждый новый запрос подаем с задержкой. Имя pause произвольное
pause = 0.25

# Маскируем запрос с помощью headers
request_params = {'Cookie': 'mrcu=B84762BACEBC1297E8DB79F9F4BC; p=4HUAAEDx9zIA; searchuid=3850772031656409793; _ym_uid=1656763503415284211; s_cp=skipNotificationsTo=1680538790313; _ym_d=1690927228; s=ext=2|octavius=1|fver=0|ww=1536|wh=745|dpr=1.25|rt=1; mr1lad=651c91f428aa140e-300-300-; c=vQUeZQMAIHsTAAAUAAQAM9PZLEV0AgCQcGBmOgsA; b=skwAAIBwXe4DhfiYYZABAAAC; Mpop=1696522232:6d63634c7e570c661905000017031f051c054f6c5150445e05190401041d06415d56475c4b51525b105a545e591f4642:7xmaverick@mail.ru:; mrhc=Y3/Mn6Dv5oNX881At2z0kZV6ZZnf/gssBa/e0Q8sA+w=; i=AQCyuyJlEQATAAigNTYAATkAAZ0AAr8AAcAAAh8BAWABAXoBAXsBAZoBAeoCAWQDAYwDAS4EAVQEAYsEAcIEAWEFAXEFAVwGAgIHATcHAj4HApUHAc4HAdAHAdEHAdIHAdMHAVoIAeIIAQ8JARcJARkJAR8JASAJASIJATwJAV8JAdMJAfEJAfYJAYMKAYQKAUMLAS0cAS4cAXseAtYgAfUgAfYgAfcgAfggARQACFgdIQABfwABjwABGQIBGgIBegIBewIBfwIBhAIBigIBWQUBWwUBYwUBbwUBcAUBmwUBnwUBoQUBpAUBZQYByAsByQsBzAsBzgsBbQ0BcA0B6BAB6RABomMBgAAJAQGBAAoEBAjQB7sBCAQBBAABTgIIrzrjAAEKAQEUAQErAQExAQFbAQGUAQHAAQHSAQGoAgHQBAG2BQG4BQEyCQEzCQE/CQFDCQGnCQFwCgGACgHqCwHtCwHuCwH7CwEHDAEqDAErDAFGDAFHDAGADAGDDAGrDAGsDAGuDAGvDAGwDAGxDAGyDAHPDAH3DAH9DAH+DAEADQECDQEDDQEEDQEGDQEIDQEKDQELDQEODQEuDQExDQE2DQFFDQFsDQFxDQFXDwFfAggxEEoAA2QAAkQIAoYIAgUKBBYKA1IKAakKAqsKAa4KAbAKAsAKAcgKATULAVgLAWYLAWMCCDQRqwwBrAwBsAwBsQwBsgwBzwwB9wwB/QwB/gwBAA0BAw0BBA0BBg0BCA0BCg0BLg0BHw4BkgIIBAEBAAGTAghVHG4AAQECAQICAQcCAQgCAQkCAQ0CAQ4CARMCARcCAWAFAWgFAXQFAXUFAaAFAaEFAaQFAaYFAakFAXoGAcgLAcwLAXANAXgNAWEPAWUPAX8PAaJjAdwECAQBAQAB4QQJAQHiBAoEBAjQBzoFCDQRqwwBrAwBsAwBsQwBsgwBzwwB9wwB/QwB/gwBAA0BAw0BBA0BBg0BCA0BCg0BLg0BHw4B1gYIBAEBAAG9BwgEAYIVASkJCD0U2gIBIwQBJAQBggQBhAQBiAQBjQQBjgQBkwQBQAcBrAcBtwcBuAcBuQcB6AcB6gcB7QcBuggByAsBywsB; VID=2nEi9t3YspYK00000e1GL42K:::a3938b8-a270c56-a3d5a1d-7d51809-0:CAASEEzO8qhC3DKkiaWaBJ_HWuIagAHAyYXBKa1avKLyBgh9CW_BLgr6KuCzXobPOjRTH6zTB4TMcTCglPVkI_cAcwmhAYIVgr03e7gz3lFkCf0RJ4JlfS6EbVIuBhFFumAHM1EaticgZwrCOg_YV0JtcVYRE1yKjJPiLqrco0FyVn9bzEUDxz-GjXvXk397-mSnqmCajQ'
 , 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}

# 1. ПРОМО-ХАРАКТЕРИСТИКИ КОНКУРСОВ И ИХ URL-АДРЕСА СО ВСЕХ СТРАНИЦ С ИХ СПИСКАМИ
df = pandas.DataFrame() # Создаем таблицу
i = 1 # Начальный номер страницы списка конкурсов
while i > 0: # "Вечное" условие
    print(f'Страница №{i} списка конкурсов')
    urlsmmr = f'https://www.fl.ru/konkurs/?page={i}#/' # Текст с переменной вставкой
    response = requests.get(urlsmmr, headers=request_params) # Замаскированно обращаемся по URL-адресу страницы №i списка конкурсов
    if BeautifulSoup(response.text, features="lxml").find_all('div', attrs={'id':'projects-list'}) != []:
        
        # Записываем в новый объект blockS список блоков, содержащих промо-характеристики конкурсов и их адреса
        blockS = str(BeautifulSoup(response.text, features="lxml")\
            .find_all('div', attrs={'id': 'projects-list'})[0].find_all('div', attrs={'class':'b-post'})).split('b-post ')
        
        # Проходим по каждому из блоков
        j = 0
        for block in blockS:
            try:
                urlprjct = 'https://www.fl.ru/' + re.findall(r'/projects/\d+/', block)[0]
                df.loc[urlprjct, 'Закреп конкурса'] = 'post__pin' in block
                df.loc[urlprjct, 'Срочность конкурса'] = 'urgently-1.png' in block
                df.loc[urlprjct, 'Цвет конкурса'] = '_bg_' in block
            except Exception as exc:
                traceback.print_exc()
                print(f'Ошибка в итерации №{j}')
            j =+ 1
    else:
        print(f'Страница №{i} пуста')
        break # Выход из цикла
    i += 1
df

# 2. СОДЕРЖАТЕЛЬНЫЕ ХАРАКТЕРИСТИКИ КОНКУРСОВ И РЕПУТАЦИОННЫЕ ХАРАКТЕРИСТИКИ ИХ ЗАКАЗЧИКОВ
for urlprjct in df.index:
    print(urlprjct)
    time.sleep(pause)
    # Применяем функцию .get() для обращения компьютера по URL-адресу конкурса
    response = requests.get(urlprjct, headers=request_params)
    
    # Добавляем в таблицу графу "Название конкурса"    
    df.loc[urlprjct, "Название конкурса"]\
    = BeautifulSoup(response.text, features="lxml").find_all('h1', attrs={'class': 'text-1 d-flex align-items-center'})[0].get_text().strip()      

    # Бюджет конкурса
    budget = BeautifulSoup(response.text, features="lxml").find_all('div', attrs={'id':'budget_block'})[0].find('span').get_text().strip()
    budget_num = ''
    for j in range(len(budget.split('\xa0')) - 1):
        budget_num += budget.split('\xa0')[j]
    df.loc[urlprjct, "Бюджет"] = int(budget_num)
    
    # Описание конкурса
    dscrptn = BeautifulSoup(response.text, features="lxml")\
        .find_all('div', attrs={'class': 'text-5 text-dark'})[0].get_text().strip()
    dscrptn = dscrptn.replace('\xa0', '')
    while '  ' in dscrptn:
        dscrptn = dscrptn.replace('  ', ' ')
    df.loc[urlprjct, "Описание конкурса"] = dscrptn

    # Раздел конкурса
    df.loc[urlprjct, "Раздел"] = BeautifulSoup(response.text, features="lxml")\
        .find_all('div', attrs={'class':'text-5 mt-8'})[0].get_text()
    
    # Участники, кандидаты, забаненные
    df.loc[urlprjct, "Участники"] = int(BeautifulSoup(response.text, features="lxml")\
        .find_all('div', attrs={'class':'contest-ib contest-party'})[0].find('span', attrs={'id':'stat-freelancers'}).get_text())
    df.loc[urlprjct, "Кандидаты"] = int(BeautifulSoup(response.text, features="lxml")\
        .find_all('div', attrs={'class':'contest-ib contest-party'})[0].find('span', attrs={'id':'stat-candidates'}).get_text())
    df.loc[urlprjct, "В бане"] = int(BeautifulSoup(response.text, features="lxml")\
        .find_all('div', attrs={'class':'contest-ib contest-party'})[0].find('span', attrs={'id':'stat-banned'}).get_text())

    # Дата завершения приёма заявок и статус заказа
    df.loc[urlprjct, "Дата завершения приёма заявок"] = BeautifulSoup(response.text, features="lxml")\
        .find_all('div', attrs={'class':'contest-period-in'})[0].find_all('p')[0].get_text().split('до ')[1]
    df.loc[urlprjct, "Заказ закрыт"] = "Заказ закрыт" in response.text
    
    # Комментарии
    if 'coments-list' in response.text:
        df.loc[urlprjct, "Число ветвлений комментариев"] = int(BeautifulSoup(response.text, features="lxml")\
            .find_all('strong')[0].find('span').get_text())
        df.loc[urlprjct, "Тексты комментариев"] = BeautifulSoup(response.text, features="lxml")\
            .find_all('ul', attrs={'class':'coments-list'})[0].get_text()
        df.loc[urlprjct, "Число комментариев"] = len(re.findall(r'\[\d+\.\d+\.\d+ \| \d+:\d+\]',
            BeautifulSoup(response.text, features="lxml").find_all('ul', attrs={'class':'coments-list'})[0].get_text()))
    else:
        df.loc[urlprjct, "Число ветвлений комментариев"] = 0
        df.loc[urlprjct, "Число комментариев"] = 0
    
    # URL заказчика
    df.loc[urlprjct, "URL заказчика"] = 'https://www.fl.ru' + BeautifulSoup(response.text, features="lxml")\
        .find_all('div', attrs={'class':'d-lg-flex align-items-center'})[0].find('a').get('href')
                                                   
    urlusr = df.loc[urlprjct, "URL заказчика"]
    
    # Применяем функцию .get() для обращения компьютера по URL-адресу конкурса
    time.sleep(pause)
    response = requests.get(urlusr, headers=request_params)
            
    df.loc[urlprjct, "Платный аккаунт"] = "Платный аккаунт" in response.text
                                                       
    df.loc[urlprjct, "Безопасные сделки"] = "Пользователь работал через Безопасную сделку" in response.text
                                                       
    df.loc[urlprjct, "Телефон подтвержден"] = "Телефон подтвержден" in response.text
                                                       
    df.loc[urlprjct, "Email подтвежден"] = "Email подтвежден" in response.text
                                                       
    df.loc[urlprjct, "Паспортные данные проверены"] = "Паспортные данные проверены" in response.text
                                                       
    df.loc[urlprjct, "Данные юридического лица/ИП проверены"] = "Данные юридического лица/ИП проверены" in response.text
    
    # Поиск требуемого элемента без привязки к номеру
    for block in BeautifulSoup(response.text, features="lxml").find_all('td', attrs={'class':'b-layout__td'}):
        if 'На сайте ' in block.get_text():
            break
    
    # На случай отсутствия опыта
    if re.findall(r'На сайте .+\t', block.get_text())[0].strip() == 'На сайте меньше месяца':
        df.loc[urlprjct, "Лет на сайте"] = 0
        df.loc[urlprjct, "Месяцев на сайте"] = 0
    
    # На случай НАЛИЧИЯ опыта в годах
    if re.findall(r'\d+ [лг]+', block.get_text()) != []:
        df.loc[urlprjct, "Лет на сайте"] = int(re.findall(r'\d+ [лг]+', block.get_text())[0].strip().split(' ')[0])
    else:
        df.loc[urlprjct, "Лет на сайте"] = 0
    
    # На случай НАЛИЧИЯ опыта в месяцах
    if re.findall(r'\d+ месяц', block.get_text()) != []: # по аналогии
        df.loc[urlprjct, "Месяцев на сайте"] = int(re.findall(r'\d+ месяц', block.get_text())[0].strip().split(' ')[0])
    else:
        df.loc[urlprjct, "Месяцев на сайте"] = 0
    
    # Поиск требуемого элемента без привязки к номеру
    for block in BeautifulSoup(response.text, features="lxml").find_all('td', attrs={'class':'b-layout__td'}):
        if ('Рейтинг' in block.get_text()) & ('Отзывы' in block.get_text()):
            break

    block = re.sub(r'\n+|\t+|\xa0+', r' ', block.get_text().strip())

    block = re.sub(r'[  ]+', r' ', block)
                                                       
    block = block if ' ' in re.findall(r'Рейтинг *\d*\.*\d+', block)[0] else block.replace('Рейтинг', 'Рейтинг ')

    df.loc[urlprjct, 'Рейтинг'] =\
        float(re.findall(r'Рейтинг *\d*\.*\d+', block)[0].split(' ')[-1]) if 'Рейтинг' in block else 0
                                                       
    df.loc[urlprjct, 'Безопасные сделки'] =\
        int(re.findall(r'Безопасные сделки \d+', block)[0].split(' ')[-1]) if 'Безопасные сделки' in block else 0
                                                       
    df.loc[urlprjct, 'Выбран[а] исполнителем'] =\
        int(re.findall(r'Выбран[а] исполнителем \d+', block)[0].split(' ')[-1]) if 'Выбран' in block else 0
            
    df.loc[urlprjct, 'Отзывы+'] = int(re.findall(r'Отзывы \+ \d+', block)[0].split(' ')[-1]) if 'Отзывы' in block else 0
                                                       
    df.loc[urlprjct, 'Отзывы-'] = int(re.findall(r'- \d+', block)[0].split(' ')[-1]) if 'Отзывы' in block else 0
                                                       
df

today = datetime.date.today().strftime("%Y%m%d")
df.to_excel(f'FL_конкурсы_{today}.xlsx', sheet_name='FL_конкурсы')