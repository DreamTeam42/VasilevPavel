import requests
from bs4 import BeautifulSoup


def get_general_information(lot_info):
    req = requests.get(lot_info['href'])
    soup = BeautifulSoup(req.text, 'html.parser')
    lots = soup.find_all('div', class_="lot_block")
    for x in lots:
        tmp = x.find_all('div', class_="form-group")
        for z in tmp:
            lot_info[z.find('label', class_="col-sm-4 control-label").get_text().strip()] = \
                z.find('div', class_="form-control-static formInfo").get_text().strip()


def main():
    print("--==Start==--")
    base_url = 'https://www.etp-torgi.ru'
    url = "https://www.etp-torgi.ru/market/?action=search&search_type=all&search_record_on_page=10&search_string=\
    &procedure_stage=4&price_from=&price_to=&currency=0&search_by_date_type=&search_date_start=&search_date_end=\
    &checkbox_privatization_auction=on&checkbox_privatization_public_offer2=\
    on&checkbox_privatization_property_disposal=on&checkbox_privatization_realization=\
    on&checkbox_privatization_confiscated=on&checkbox_rent_auction=on&checkbox_two_parts_auction=\
    on&order_by=date_end&order_dir=desc"
    lot_info = {}
    req = requests.get(url)
    print('Request =>', req.url, '\n\n')
    soup = BeautifulSoup(req.text, 'html.parser')
    tr_elements = soup.find_all('tr', class_="c1")
    lot = tr_elements[0].find_all('td')
    for x in lot:
        print(x, '\n__________________\n')

# 0 - Тип аукциона
# 1 - Номер аукциона
# 2 - Объект торгов
# 3 - Организатор аукциона
# 4 - Месторасположение
# 5 - Начальная цена
# 6 - Дата публикации, Дата окончания приема заявок, Дата рассмотрения заявок,
    # Дата начала аукциона, Дата подведения итогов торгов
# 7 - Состояние
    lot_info['type'] = lot[0].get_text()
    lot_info['auction number'] = lot[1].get_text().split('-')[0][1:]
    lot_info['lot number'] = lot[1].get_text().split('-')[1][0:-1]
    lot_info['href'] = base_url + lot[1].a.get('href')
# TODO:    lot_info['object'] =
    lot_info['organizer'] = lot[3].a.get_text()
    lot_info['organizer_href'] = base_url + lot[3].a.get('href')
# TODO:    lot_info['location'] =
# TODO:    lot_info['prise'] =
    a = lot[6].find_all('span')
    for x in a:
        lot_info[x.get('title').strip()] = x.get_text().strip()
    lot_info['status'] = lot[7].get_text()
    get_general_information(lot_info)

    for key, value in lot_info.items():
        print(key, ':', value)


if __name__ == '__main__':
    main()
