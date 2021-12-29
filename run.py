import os
from string import ascii_letters
from time import sleep
from bs4 import BeautifulSoup
from requests import get
from rich import print
from tqdm import tqdm

ascii_letters += '-+'


def proxynova(response):
    result = []
    x = BeautifulSoup(response.text, 'lxml').find_all('td', {'align': "left"})
    for ipport in enumerate(x):
        if '(\'' in str(ipport[1].find('abbr')):
            result.append(eval(str(ipport[1].find('abbr')).split('(')[1].split(')')[0]) + ':' + x[ipport[0] + 1].
                          text.replace('\n', '').replace(' ', ''))
    return result


data = {
    'https://free-proxy-list.net/#': lambda response: response.text.split('Free proxies from'
                                                                          ' free-proxy-list.net')[1].split('<')[
        0].split('\n'),

    'https://proxylist.geonode.com/api/proxy-list?limit=200&page=1&sort_by=lastChecked&sort_type=desc':
        lambda response: [str(ipport.get('ip')) + ':' + str(ipport.get('port'))
                          for ipport in response.json().get('data')],

    'https://spys.me/proxy.txt': lambda response: [ipport.split(' ')[0] for ipport in
                                                   response.text.split('(+)\n')[1].split('\nFree')[0].split('\n')],

    'https://www.us-proxy.org/#': lambda response: response.text.split('Free proxies from'
                                                                       ' free-proxy-list.net')[1].split('<')[0].split(
        '\n'),
    'https://www.proxynova.com/proxy-server-list/': proxynova,
}


def main(filename='proxies.txt'):
    try:
        proxies_list = open(filename, 'r').read().split('\n')
    except FileNotFoundError:
        print('Файл не найден. Будет создан новый!')
        proxies_list = []

    maximum = len(data)

    print('[white]Начинаю парсить прокси![/white]')

    for url in enumerate(data):
        try:
            resp = get(url[1])
            proxies = data[url[1]](resp)
            if type(proxies) != list:
                proxies = list(proxies)
            proxies_list += proxies
            print('[green]{} из {} сайтов прочеканы[/green]'.format(url[0] + 1, maximum))
        except Exception as e:
            print('[red]Произошла ошибка по адресу[/red] [blue]' + url[1] + '[/blue] :[red]' + str(e) + '[/red]')

    proxies_list = list(set(proxies_list))

    lenght = len(proxies_list)

    print('[white]Прокси успешно спарсились[/white]')
    print()
    print('Всего: [lime]{}[/lime] прокси'.format(lenght))
    print()

    print('[orange]Проверяю на наличие мусора...[/orange]')

    for i in tqdm(proxies_list):
        if True in [z in i for z in ascii_letters]:
            proxies_list.remove(i)

    sleep(1)

    print('[yellow]Мусор был очищен успешно![/yellow]\n'
          'Прошлая длина прокси-листа: [red]{}[/red] прокси\n'
          'Текущая длина: [green]{}[/green] прокси'.format(lenght, len(proxies_list)))

    print('[white]Проверяю на лишние пропуски в файле[/white]')
    try:
        proxies_list.remove('\n')
    except Exception as e:
        print('[yellow]Пропусков не обнаружено[/yellow]: ' + str(e))
    try:
        proxies_list.remove(' ')
    except Exception as e:
        print('[yellow]Пропусков не обнаружено[/yellow]: ' + str(e))

    print('[green]Соединяю все прокси в текст[/green]')
    proxies_txt = '\n'.join(proxies_list)[1:]

    print('[green]Записываю в файл...[/green]')
    open(filename, 'w').write(proxies_txt)
    print('[green]Прокси были успешно записаны в файл [/green][blue]{}[/blue]\n'.format(filename))
    print('Открыть файл? [green]y[/green]/[red]n[/red]: ')
    answer = str(input())
    if answer.lower() == 'y':
        os.startfile(filename)
    print('[orange]Закрываю скрипт![/orange]\n[red]Goodbye![/red]')
    exit()


if __name__ == '__main__':
    print('[green]Введите название файла куда вы хотите сохранить список прокси: [/green]')
    filen = input(' ')
    if '.txt' not in filen:
        filen += '.txt'
    main(filen)
