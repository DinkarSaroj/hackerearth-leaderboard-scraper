from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
import tempfile
import csv
from io import StringIO

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
        <head>
            <title>Contest Data Scraper</title>
        </head>
        <body>
            <h1>Enter Contest Name to Scrape Data</h1>
            <form action="/scrape" method="get">
                <input type="text" name="contestName" placeholder="Enter contest name" required>
                <button type="submit">Scrape Data</button>
            </form>
        </body>
    </html>
    '''

@app.route('/favicon.ico')
def favicon():
    return '', 204


def scrape_data(contest_name):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode for background execution
    driver = webdriver.Chrome(options=chrome_options)

    # Temporary file setup to hold the results
    temp_file, temp_file_path = tempfile.mkstemp(suffix='.csv')
    os.close(temp_file)

    with open(temp_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Rank', 'Name', 'Username', 'Score', 'Questions Solved', 'Time'])

        page = 1
        try:
            while True:
                url = f"https://www.hackerearth.com/challenges/competitive/{contest_name}/leaderboard/page/{page}/"
                driver.get(url)

                # Wait for the table to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.align-top"))
                )

                rows = driver.find_elements(By.CSS_SELECTOR, "tbody.align-top tr")
                if not rows:
                    break  # If no rows are found, stop the loop

                for row in rows:
                    rank = row.find_element(By.CSS_SELECTOR, "span.float-left.medium-margin-right.weight-700.dark").text.strip().replace(".","")
                    name = row.find_element(By.CSS_SELECTOR, "div.no-color.hover-link.weight-600").text.strip()
                    username = row.find_element(By.CSS_SELECTOR, "div.gray-text.body-font-small.hover-link").text.strip()
                    score_data = row.find_element(By.CSS_SELECTOR, "td.align-center").text.strip()
                    time_data = row.find_elements(By.CSS_SELECTOR, "td.align-center")[1].text.strip()

                    score, questions_solved = score_data.split()
                    questions_solved = questions_solved.strip('()')

                    writer.writerow([rank, name, username, score, questions_solved, time_data])

                next_buttons = driver.find_elements(By.CSS_SELECTOR, "i.fa.fa-angle-right.dark")
                if next_buttons and next_buttons[0].is_displayed():
                    driver.execute_script("arguments[0].click();", next_buttons[0])
                    page += 1
                else:
                    break

        finally:
            driver.quit()

    # Read the data back from the temporary file
    with open(temp_file_path, 'r', newline='', encoding='utf-8') as file:
        data = file.readlines()
    os.unlink(temp_file_path)  # Clean up the temporary file
    return data


def parse_csv_data(csv_data):
    """Converts CSV data from list of strings to list of dictionaries."""
    data = []
    csv_reader = csv.DictReader(StringIO(''.join(csv_data)))
    for row in csv_reader:
        data.append(row)
    return data

@app.route('/scrape', methods=['GET'])
def scrape():
    contest_name = request.args.get('contestName', '')
    if contest_name:
        contest_name = contest_name.replace(" ", "-")
        try:
            raw_data = scrape_data(contest_name)  # This function should now return the raw CSV data as list of strings
            data = parse_csv_data(raw_data)
            return render_template('results.html', data=data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'No contest name provided'}), 400


if __name__ == '__main__':
    app.run(debug=True)
