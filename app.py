from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

def scrape_data():
    try:
        from bs4 import BeautifulSoup as bs
        from urllib.request import urlopen as uo

        url = 'https://www.worldometers.info/world-population/population-by-country/'
        response = uo(url)
        response_page = response.read()
        soup = bs(response_page, 'html.parser')

        table = soup.find('table', {'id': 'example2'})

        header = []
        for th in table.find_all('th')[:-1]:
            header.append(th.text.strip())

        data = []
        for tr in table.find_all('tr')[1:]:
            row = {}
            for idx, td in enumerate(tr.find_all('td')[:-1]):
                row[header[idx]] = td.text.strip()
            data.append(row)

        df = pd.DataFrame(data=data, columns=header)
        df.to_csv('world_population_data.csv', index=False)

        return data

    except Exception as e:
        print(f"Error occurred while scraping data: {str(e)}")
        return  []
    
@app.route('/')
def index():
    scraped_data = scrape_data()
    return render_template('index.html', data=scraped_data)

if __name__ == '__main__':
    app.run(debug=True)
