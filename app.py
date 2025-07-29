from flask import Flask, render_template, request, jsonify, Response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
import tempfile
from io import StringIO

app = Flask(__name__)

@app.route('/')
def home():
    # Use the template for the home page for consistency
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204


def scrape_data(contest_name):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Use StringIO to build the CSV in memory
    output = StringIO()
    writer = csv.writer(output)
    
    header = ['Rank', 'Name', 'Username', 'Score', 'Questions Solved', 'Time']
    writer.writerow(header)

    page = 1
    try:
        while True:
            url = f"https://www.hackerearth.com/challenges/competitive/{contest_name}/leaderboard/page/{page}/"
            driver.get(url)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.align-top"))
            )

            rows = driver.find_elements(By.CSS_SELECTOR, "tbody.align-top tr")
            if not rows:
                break

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
    
    # Move to the beginning of the StringIO buffer to read its content
    output.seek(0)
    return output.getvalue()


def parse_csv_data(csv_string):
    """Converts CSV string to a list of dictionaries, skipping the header."""
    data = []
    # Use DictReader directly on the string
    csv_reader = csv.DictReader(StringIO(csv_string))
    for row in csv_reader:
        data.append(row)
    return data

@app.route('/scrape', methods=['GET'])
def scrape():
    contest_name_raw = request.args.get('contestName', '')
    if contest_name_raw:
        contest_name_slug = contest_name_raw.replace(" ", "-")
        try:
            # Scrape data and get it as a CSV string
            csv_string = scrape_data(contest_name_slug)
            # Parse the string into a list of dictionaries for rendering
            data = parse_csv_data(csv_string)
            return render_template('results.html', data=data, contest_name=contest_name_raw)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'No contest name provided'}), 400

# --- NEW DOWNLOAD ROUTE ---
@app.route('/download_csv')
def download_csv():
    contest_name_raw = request.args.get('contestName', '')
    if not contest_name_raw:
        return "Error: No contest name provided.", 400

    contest_name_slug = contest_name_raw.replace(" ", "-")
    try:
        # Scrape the data again for download
        csv_data = scrape_data(contest_name_slug)
        
        # Create a Flask Response object
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-disposition":
                     f"attachment; filename={contest_name_slug}_leaderboard.csv"}
        )
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True)