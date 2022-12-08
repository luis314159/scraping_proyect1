import requests 
from lxml import html as html
import os 
import datetime 

HOME_URL='https://www.larepublica.co/'



"""
links= //h2[@class="headline"]/a/@href
Títuolo=//h2/span/text()
Resumen= //div[@class="lead"]/p/text()
Cuerpo=//div[@class="html-content"]/p/text()

"""


def parse_notice(link,today):
    try:
        response = requests.get(link)

        if response==200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','')
                sumary = parsed.xpath(XPATH_SUMARY)
                body=parsed.xpath(XPATH_BODY)
            except IndexError:
                return 

            with open(f'{today}/{title}.txt','w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(sumary)
                f.write('\n\n')

                for p in body:
                    f.write(p)
                    f.write('\n')
                    

        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)


XPATH_LINK_TO_ARTICLE= '//h2[@class="headline"]/a/@href'
XPATH_TITLE ='//h2/span/text()'
XPATH_SUMARY='//div[@class="lead"]/p/text()'
XPATH_BODY='//div[@class="html-content"]/p/text()'

def parse_home():

    try:
        response = requests.get(HOME_URL)

        if response.status_code ==200:
            home = response.content.decode('utf-8')

            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_notices)

            today = datetime.date.today().strftime('%d-%m-%Y')

            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notices:
                parse_notice(link, today)


        else:
            raise ValueError(f"Error: {response.status_code}")

    except ValueError as ve:
        print(ve)

def run():
    parse_home()


if __name__ == '__main__':
    run()
