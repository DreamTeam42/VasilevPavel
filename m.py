import requests
import json
from time import sleep
from bs4 import BeautifulSoup

# Количество элементов на странице
#   на сайте варианты: 10, 20, 40. но можно и другие)
Number_of_items_per_page = '10'
keywords = []
banned_keywords = []
fields = []
# page = '1'
base_url = 'https://www.etp-torgi.ru'


def read_key():
    print('Reading files..')
    with open('keywords.txt') as f:
        for line in f:
            if line != '\n' and line[0] != '#':
                keywords.append(line.strip())
    with open('banned_keywords.txt') as f:
        for line in f:
            if line != '\n' and line[0] != '#':
                banned_keywords.append(line.strip())
    with open('fields.txt') as f:
        for line in f:
            if line != '\n' and line[0] != '#':
                fields.append(line.strip())
    print('Reading is complete\n')


def get_protocol(lot_info):
    print('\tSleep 2 seconds..')
    sleep(2)
    res = requests.get(lot_info['protocol_url'])
    soup = BeautifulSoup(res.text, 'html.parser')
    lot = soup.find('tbody').find_all('tr')[int(lot_info['lot number']) - 1]
    if lot_info['type'] == 'Аукцион. Аренда государственного и муниципального имущества':
        lot = lot.find('div', class_="panel panel-default mte-form-panel")
        lot = lot.find_all('li', class_="list-group-item")
        temp = lot[-5].find('div', class_="col-sm-8")
        lot_info[lot[-5].find('div', class_="col-sm-4 control-label").get_text().strip()] = temp.get_text().strip()
    else:
        lot = lot.find_all('div', class_="panel panel-default mte-form-panel")[1].find('div', class_="row")
        temp = lot.find_all('table', class_="table table-striped")[1].find('tbody').find_all('td')
        s = 'Признать следующего Участника победителем торгов по лоту №' + lot_info['lot number'] +\
            '. Приступить к заключению с ним договора купли-продажи. Участник: ' + temp[1].get_text().strip() +\
            '. Предложение: ' + temp[2].get_text().strip()
        lot_info[lot.find('div', class_="col-sm-4").get_text().strip()[0:-1]] = s


def get_general_information(lot_info):
    print('\tSleep 2 seconds..')
    sleep(2)
    res = requests.get(lot_info['href'])
    soup = BeautifulSoup(res.text, 'html.parser')
    lots = soup.find_all('div', class_="lot_block")
    tmp = lots[int(lot_info['lot number']) - 1].find_all('div', class_="form-group")
    for z in tmp:
        left = z.find('label', class_="col-sm-4 control-label").get_text().strip()
        success = -1
        for line in fields:
            success = left.find(line)
            if success != -1:
                break
        if success == -1:
            continue
        lot_info[left] = \
            z.find('div', class_="form-control-static formInfo").get_text().strip()
    protocol = soup.find('ul', class_="nav nav-tabs")
    protocol_url = protocol.find_all('li')[-1]
    protocol_url = protocol_url.a.get('href')
    lot_info['protocol_url'] = base_url + protocol_url
    if lot_info['status'] == 'Торги состоялись':
        get_protocol(lot_info)


def main():
    print("--==Start==--")
    read_key()
    f = open('data.json', 'w')
    from_ = '0'
#    url = 'https://www.etp-torgi.ru/market/?action=search&search_record_on_page=10&procedure_stage=4&currency=0' +\
# 9        '&checkbox_privatization_auction=on&from=10&page=2'
    url = "https://www.etp-torgi.ru/market/?action=search&search_type=all&search_record_on_page=" +\
          Number_of_items_per_page + "&currency=0&checkbox_privatization_auction=on" +\
          "&checkbox_privatization_public_offer2=on&checkbox_privatization_property_disposal=on" +\
          "&checkbox_privatization_realization=on&checkbox_privatization_confiscated=on" +\
          "&checkbox_rent_auction=on&checkbox_two_parts_auction=on&from="
    lot_info = []
    curr_ind = 0
    res = requests.get(url + from_ + "&page=1")
    print('Request =>', res.url, '\n')
    soup = BeautifulSoup(res.text, 'html.parser')
    last_page = soup.find('ul', class_="pagination pull-left").find_all('li')[-1].a.get('href')
    last_page = int(last_page[(last_page.rfind('page=') + 5):])
    last_page = 1
    for page in range(1, last_page + 1):
        if page != 1:
            from_ = int(Number_of_items_per_page) * page - 1
            res = requests.get(url + str(from_) + "&page=" + str(page))
            print('\tSleep 2 seconds..')
            print('Request =>', res.url, '\n')
            sleep(2)
            soup = BeautifulSoup(res.text, 'html.parser')
        tr_elements = soup.find_all('tr', class_="c1")
        for i in range(0, int(Number_of_items_per_page)):
            lot = tr_elements[i].find_all('td')
            # 0 - Тип аукциона
            # 1 - Номер аукциона
            # 2 - Объект торгов
            # 3 - Организатор аукциона
            # 4 - Месторасположение
            # 5 - Начальная цена
            # 6 - Дата публикации, Дата окончания приема заявок, Дата рассмотрения заявок,
            #       Дата начала аукциона, Дата подведения итогов торгов
            # 7 - Состояние
            success_k = 0
            for x in keywords:
                success_k = lot[2].get_text().find(x)
                if success_k != -1:
                    break
            if success_k == -1:
                print('\tНе подходит! Переход на следующий лот\n')
                print('_____________================_____________\n')
                continue
            success_bk = 0
            for x in banned_keywords:
                success_bk = lot[2].get_text().find(x)
                if success_bk != -1:
                    break
            if success_bk != -1:
                print('\tНе подходит! Переход на следующий лот\n')
                print('_____________================_____________\n')
                continue
#            if success_k == -1 and success_bk == -1:
            lot_info.append({})
            lot_info[curr_ind]['type'] = lot[0].get_text()
            lot_info[curr_ind]['auction number'] = lot[1].get_text().split('-')[0][1:]
            lot_info[curr_ind]['lot number'] = lot[1].get_text().split('-')[1][0:-1]
            lot_info[curr_ind]['href'] = base_url + lot[1].a.get('href')
            lot_info[curr_ind]['organizer'] = lot[3].a.get_text()
            lot_info[curr_ind]['organizer_href'] = base_url + lot[3].a.get('href')
            a = lot[6].find_all('span')
            for x in a:
                lot_info[curr_ind][x.get('title').strip()] = x.get_text().strip()
            lot_info[curr_ind]['status'] = lot[7].get_text()
            get_general_information(lot_info[curr_ind])

            for key, value in lot_info[curr_ind].items():
                print(key, ':', value)
#            f.write(json.dumps(lot_info[curr_ind], sort_keys=True, indent=4))
#            f.write(',\n')
            curr_ind += 1
            print('_____________================_____________\n')
    f.write(json.dumps(lot_info, sort_keys=True, indent=4))
    f.close()
    print('Done! (◕‿◕) ')


if __name__ == '__main__':
    main()
