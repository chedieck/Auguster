from bs4 import BeautifulSoup
import requests
import os

def make_poems_db():
    mainurl = requests.get('http://www.biblio.com.br/conteudo/AugustodosAnjos/augustodosanjosobras.htm')
    soup = BeautifulSoup(mainurl.content, 'html.parser')
    aux = soup.find('table')
    aux = aux.find_all('tr')[-1]
    aux = aux.find_all('a')
    links = [i.attrs['href'] for i in aux]
    print(soup.prettify())

    for link in links:
        if link == 'venusmorta.htm':
            continue
        url = requests.get(f'http://www.biblio.com.br/conteudo/AugustodosAnjos/{link}')
        soup = BeautifulSoup(url.content, 'html.parser')
        all = soup.find_all('body')
        title = all[0].text
        print(title)
        poem  = '\n\n'.join([i.get_text().replace('\r', '') for i in all[1:]])
        name = link.split('.')[0] # remove the htm extension
        with open(f'DB/{name}.txt', 'w') as f:
            f.write(title + '\n')
            f.write(poem)

def concatenate_all_poems():
    all = ''
    for poem in os.listdir('DB'):
        with open(f'DB/{poem}', 'r') as f:
            all += ''.join(f.readlines()[1:]) + '\n\n' #tira o título
    
    with open('all.txt', 'w') as f:
        f.write(all)
