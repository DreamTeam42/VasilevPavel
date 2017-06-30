import requests
from bs4 import BeautifulSoup


def main():
    print("--==Start==--")
    base_url = 'https://www.etp-torgi.ru'
    url = "https://www.etp-torgi.ru/market/?action=search&search_type=&search_record_on_page=10&search_string=\
    &procedure_stage=4&price_from=&price_to=&currency=0&search_by_date_type=&search_date_start=&search_date_end=\
    &checkbox_privatization_auction=on&checkbox_privatization_public_offer2=\
    on&checkbox_privatization_property_disposal=\
    on&checkbox_privatization_realization=on&checkbox_privatization_confiscated=\
    on&checkbox_rent_auction=on&checkbox_two_parts_auction=on"

    lot_info = {}

    req = requests.get(url)
    print('Request =>', req.url, '\n\n')
    soup = BeautifulSoup(req.text, 'html.parser')
    tr_elements = soup.find_all('tr')
    lot = tr_elements[2].find_all('td')
    for x in lot:
        print(x, '\n__________________\n')
#    print(lot_p[1], '\n__________________\n')
#    print(lot_p[2], '\n__________________\n')
#    print(lot_p[3], '\n__________________\n')
#    print(lot_p[4], '\n__________________\n')
#    print(lot_p[5], '\n__________________\n')
#    print(lot_p[6], '\n__________________\n')
#    print(lot_p[7], '\n__________________\n')
#    slov = {'type': None}

#    for x in lot_info:
#        for key, value in x.items():
#            print(key, value)

    lot_info['type'] = lot[0].get_text()
    lot_info['href'] = base_url + lot[1].a.get('href')
# TODO:    lot_info['object'] =
    lot_info['organizer'] = lot[3].a.get_text()
    lot_info['organizer_href'] = base_url + lot[3].a.get('href')
# TODO:    lot_info['location'] =
# TODO:    lot_info['prise'] =
# даты -??
    lot_info['status'] = lot[7].get_text()

    for key, value in lot_info.items():
        print(key, value)


if __name__ == '__main__':
    main()
